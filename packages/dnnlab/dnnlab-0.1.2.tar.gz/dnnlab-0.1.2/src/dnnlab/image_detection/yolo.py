# Copyright 2019 Tobias Höfer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""
YOLOv2
-------------
+ Batch Normalization to feature extractor model - no need for dropout
+ Convolutional With Anchor Boxes (fully convolutional)
+ Dimension Clusters
+ Direct location prediction

YOLOv2 uses a few tricks to improve training and increase performance.
Like Overfeat and SSD we use a fully-convolutional model, but we still train on
whole images, not hard negatives. Like Faster R-CNN we adjust priors on bounding
boxes instead of predicting the width and height outright. However, we still
predict the x and y coordinates directly. The full details are in the paper.
"""
import logging
import os
import time
from datetime import datetime
import numpy as np

import tensorflow as tf

from dnnlab.errors.dnnlab_exceptions import ModelNotCompiledError
from dnnlab.losses import yolo_loss
from dnnlab.losses import extract_model_output, extract_label, yolo_grid

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # FATAL
logging.getLogger("tensorflow").setLevel(logging.FATAL)


class YOLO(object):
    """Implements a yolo learning model.

        Typical usage example:

        feature_extractor -> keras.model (pretrained or from scratch) /
                             final output_layer should have fixed
                             spatial resolution:
                                (grid_size, grid_size, num_channels)
                             but num_channels can vary.

        # Define forward path.
        grid_size = 7
        n_bounding_boxes = 2
        class_list = ["foo", "bar"]
        feature_extractor = tf.keras.models.Sequential/Custom/Functional
        yolo = YOLO(feature_extractor, grid_size, n_bounding_boxes, n_classes)

        # Define optimizer.
        yolo.compile(optimizer="adam", lr=1e-4)

        # Start training process.
        yolo.fit(x,y,x_val,y_val, EPOCHS, BATCH_SIZE, save_ckpt=5)

        # Export both models.
        yolo.export()

        use gan.restore("relative_path_to_logs") to continue training after
        a break.


    Attributes:
        feature_extractor (keras.model): Basic nn feature extractor.
        grid_h (int): Grid size.
        grid_w (int): Grid size.
        anchors (int): Number of bounding boxes per grid cell.
        n_classes (int): Number of different objects.
        init_timestamp (str): Acts as a unique folder identifier.
        logdir (str): Top level logdir.
        tensorboard (str): Path to tensorboard summary files.
        ckpt_dir (str): Path to ckpt files.
        ckpt_manager (tf.train.CheckpointManager): Deletes old checkpoints.
        checkpoint (tf.train.Checkpoint): Groups trackable objects, saving and
            restoring them.
    """
    def __init__(self,
                 feature_extractor,
                 grid_h,
                 grid_w,
                 anchors,
                 class_list,
                 complete_model=None):
        """TODO

        Args:
        The more bounding boxes, the more objects can be detected in close
        neighborhood.

        """
        self.feature_extractor = feature_extractor
        self.grid_h = grid_h
        self.grid_w = grid_w
        self.anchors = anchors
        self.boxes = len(anchors) // 2
        self.class_list = class_list
        self.n_classes = len(class_list)
        self.optimizer = None
        self.complete_model = complete_model
        if self.complete_model is None:
            self.model = self._append_classifier()
        else:
            self.model = self.complete_model
        self.init_timestamp = "YOLO-" + datetime.now().strftime(
            "%d%m%Y-%H%M%S")
        self.logdir = os.path.join("logs", self.init_timestamp)
        self.tensorboard = os.path.join(self.logdir, "tensorboard")
        self.ckpt_dir = os.path.join(self.logdir, "ckpts")
        self.ckpt_manager = None
        self.checkpoint = None
        self.colors = tf.constant([(253, 165, 15)], dtype=tf.float32) / 255.

    def summary(self):
        return self.model.summary()

    def predict(self,
                img,
                text_format=True,
                max_number_bb=100,
                iou_threshold=0.4,
                class_conf_threshold=0.25):
        # TODO readable output
        # non-max surpression
        # confidence threshold
        # + visualization
        prediction = self.model.predict(img)
        selected_boxes, selected_confidence, selected_classes = self.decode_yolo_output(
            prediction,
            self.anchors,
            max_number_bb=max_number_bb,
            iou_threshold=iou_threshold,
            class_conf_threshold=class_conf_threshold)

        if text_format:
            for obj, cl, box in zip(selected_confidence, selected_classes,
                                    selected_boxes):
                print("Confidence: {}".format(obj))
                print("Class: {}".format(self.class_list[tf.cast(
                    cl, dtype=tf.int32)]))
                print("Box: {}".format(box))
                print("")
        else:

            # Swap xy coordinates for bullshit tensorflow draw_bounding_boxes
            x1 = selected_boxes[..., 0:1]
            y1 = selected_boxes[..., 1:2]
            x2 = selected_boxes[..., 2:3]
            y2 = selected_boxes[..., 3:4]

            boxes_yx = tf.concat([y1, x1, y2, x2], axis=-1)

            # Append batch dim.
            boxes_yx = tf.cast(tf.expand_dims(boxes_yx, 0), dtype=tf.float32)

            return tf.image.draw_bounding_boxes(tf.cast(img, dtype=tf.float32),
                                                boxes_yx, self.colors)

    def _append_classifier(self):
        self.feature_extractor.add(
            # 1x1 convolution.
            tf.keras.layers.Conv2D(filters=(self.boxes * (5 + self.n_classes)),
                                   kernel_size=(1, 1),
                                   strides=(1, 1),
                                   padding="same"))
        # Reshape to specific yolov2 output:
        # (bs, grid, grid, anchors, (x,y,w,h,objectivness, n_classes))
        self.feature_extractor.add(
            tf.keras.layers.Reshape(
                (self.grid_h, self.grid_w, self.boxes, 5 + self.n_classes)))

        return self.feature_extractor

    def compile(self, optimizer="adam", lr=1e-4):
        """Defines the optimization part of the learning algorithm to our
        learning model.

        Args:
            optimizer (str, optional): Optimizer. Defaults to "adam".
            lr_gen (Float, optional): Learning rate generator. Defaults to 1e4.
            lr_disc (Float, optional): Learning rate discriminator.
                Defaults to 1e4.
        """
        # TODO: more optimizer
        if optimizer == "adam":
            self.optimizer = tf.keras.optimizers.Adam(lr)

        if self.checkpoint is None:
            self.checkpoint = tf.train.Checkpoint(optimizer=self.optimizer,
                                                  model=self.model)
            self.ckpt_manager = tf.train.CheckpointManager(self.checkpoint,
                                                           self.ckpt_dir,
                                                           max_to_keep=5)

    def fit(self,
            training_data,
            validation_data,
            epochs,
            batch_size,
            len_dataset,
            save_ckpt=5,
            verbose=1,
            max_outputs=2,
            initial_step=0,
            lambda_coord=1.0,
            lambda_obj=5.0,
            lambda_noobj=1.0,
            lambda_class=1.0,
            iou_threshold=0.4,
            class_conf_threshold=0.25,
            mlflow=False):
        """Trains both models for n EPOCHS. Saves ckpts every n EPOCHS.
        The training loop together with the optimization algorithm define the
        learning algorithm.

        Args:
            dataset (tf.dataset): tf.Dataset with
                shape(None, width, height, depth).
            epochs (int): Number of epochs.
            batch_size (int): Batch length.
            save_ckpt (int): Save ckpts every n Epochs.
            verbose (int, optional): Keras Progbar verbose lvl. Defaults to 1.
            max_outputs (int, optional): Number of images shown in TB.
                Defaults to 2.

        Raises:
            ModelNotCompiledError: Raise if model is not compiled.
        """
        if self.optimizer is None:
            raise ModelNotCompiledError("use compile() first.")
        if mlflow:
            import mlflow

        # Retrace workaround @function signature only tensors.
        step = tf.Variable(initial_step, name="step", dtype=tf.int64)

        num_batches = len_dataset / batch_size

        # Keras Progbar
        progbar = tf.keras.utils.Progbar(target=num_batches, verbose=verbose)
        file_writer = tf.summary.create_file_writer(self.tensorboard)
        eval_file_writer = tf.summary.create_file_writer(
            os.path.join(self.tensorboard, "eval"))
        file_writer.set_as_default()
        for epoch in range(epochs):
            step_float = 1
            start = time.time()
            for elements in training_data:
                images = elements[0]
                labels = elements[1]

                tb_prediction, tb_label = self.train_step(
                    images, labels, batch_size, step, max_outputs, file_writer,
                    lambda_coord, lambda_obj, lambda_noobj, lambda_class,
                    iou_threshold, class_conf_threshold)
                # TODO Workaround.
                with file_writer.as_default():
                    tf.summary.image("label", tb_label, step=step)
                    tf.summary.image("prediction", tb_prediction, step=step)

                file_writer.flush()
                progbar.update(current=(step_float))
                step_float += 1
                step.assign(step + 1)

            # Save the model every n epochs
            if (epoch + 1) % save_ckpt == 0:
                ckpt_save_path = self.ckpt_manager.save()
                print("\nSaving checkpoint for epoch {} at {}".format(
                    epoch + 1, ckpt_save_path))

            print(" - Epoch {} finished after {} sec".format(
                epoch + 1, int(time.time() - start)))

            print("Start validation loop...")
            # Run a validation loop at the end of each epoch.
            val_loss = []
            for elements in validation_data:
                images = elements[0]
                labels = elements[1]
                val_logits = self.model(images)
                # Loss
                loss = yolo_loss(labels,
                                 val_logits,
                                 self.anchors,
                                 step=step,
                                 is_training=False)
                val_loss.append(loss)
                # Update val metrics TODO
                # val_acc_metric(y_batch_val, val_logits)
            val_loss = tf.reduce_mean(val_loss)
            with eval_file_writer.as_default():
                # Todo into same graph in tb. Verbose lvl
                tf.summary.scalar("total_loss", val_loss, step=step)
            eval_file_writer.flush()
            if mlflow:
                mlflow.log_metric("val_loss",
                                  val_loss.numpy(),
                                  step=step_float)
            # val_acc = val_acc_metric.result()
            # val_acc_metric.reset_states()
            # print('Validation acc: %s' % (float(val_acc), ))
            print("...Done\n")

    def restore(self, ckpt_path):
        """Restore model weights from the latest checkpoint.

        Args:
            ckpt_path (str): Relative path to ckpt files.

        Raises:
            ModelNotCompiledError: Raise if model is not compiled.
        """

        restore_path = os.path.dirname(ckpt_path)
        self.logdir = restore_path
        self.tensorboard = os.path.join(self.logdir, "tensorboard")
        self.ckpt_dir = os.path.join(self.logdir, "ckpts")
        if self.ckpt_manager is None:
            raise ModelNotCompiledError("use compile() first.")
        self.ckpt_manager = tf.train.CheckpointManager(self.checkpoint,
                                                       self.ckpt_dir,
                                                       max_to_keep=5)
        # if a checkpoint exists, restore the latest checkpoint.
        if self.ckpt_manager.latest_checkpoint:
            self.checkpoint.restore(self.ckpt_manager.latest_checkpoint)
            print("Latest checkpoint restored!!")
        else:
            print("Can not find ckpt files at {}".format(ckpt_path))

    def export(self, model_format="hdf5"):
        """Exports the trained models in hdf5 or SavedModel format.

        Args:
            model_format (str, optional): SavedModel or HDF5. Defaults to hdf5.
        """
        model_dir = os.path.join(self.logdir, "models")
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        if model_format == "hdf5":
            self.model.save(os.path.join(model_dir, "yolo.h5"))

        elif model_format == "SavedModel":
            self.generator.save(os.path.join(model_dir, "yolo"))

    @tf.function
    def train_step(self, x, y, batch_size, step, max_outputs, file_writer,
                   lambda_coord, lambda_obj, lambda_noobj, lambda_class,
                   iou_threshold, class_confidence):
        """Decorated function (@tf.function) that creates a callable tensorflow
        graph from a python function.
        """
        # TODO(Tobi): Trace keras.models graph to visualize in tensorboard.
        with file_writer.as_default():
            with tf.GradientTape() as tape:
                # Predict
                start_time = time.time()
                prediction = self.model(x, training=True)
                end_time = time.time()
                img_per_second = (end_time - start_time) / batch_size
                tf.summary.scalar("img/sec", img_per_second, step=step)

                # Bounding box prediction to tensorboard.
                tb_prediction = self._prediction_to_tensorboard(
                    x, prediction, max_outputs, step, iou_threshold,
                    class_confidence)
                # Bounding box label to tensorboard.
                tb_label = self._prediction_to_tensorboard(
                    x,
                    tf.cast(y, dtype=tf.float32),
                    max_outputs,
                    step,
                    iou_threshold,
                    class_confidence,
                    label=True)

                # Loss
                loss = yolo_loss(y,
                                 prediction,
                                 self.anchors,
                                 lambda_coord,
                                 lambda_obj,
                                 lambda_noobj,
                                 lambda_class,
                                 step=step)

            # Calculate gradient.
            gradient = tape.gradient(loss, self.model.trainable_variables)

            # Apply gradient to weights.
            self.optimizer.apply_gradients(
                zip(gradient, self.model.trainable_variables))

            # Piece of shit workaround
            return tb_prediction, tb_label

    def evaluate(self, dataset, batch_size, verbose=1):
        """TODO(): Returns loss and metrics (map, recall) for object detection.

        Args:
            dataset ([type]): [description]
            batch_size ([type]): [description]
            verbose (int, optional): [description]. Defaults to 1.
        """
        pass

    def decode_yolo_output(self,
                           predictions,
                           anchors,
                           max_number_bb=100,
                           iou_threshold=0.4,
                           class_conf_threshold=0.25,
                           tb=False,
                           label=False):
        """[summary] TODO for batch prediction. Only works for single prediction

        Args:
            predictions ([type]): [description]
            anchors ([type]): [description]
            max_number_bb (int, optional): [description]. Defaults to 10.
            iou_threshold (float, optional): [description]. Defaults to 0.4.
            class_confidence (float, optional): [description]. Defaults to 0.6.
            tb (bool, optional): [description]. Defaults to False.
        """

        batch_size = tf.cast(tf.shape(predictions)[0], dtype=tf.float32)
        # TODO wrong order?
        grid_h = tf.cast(tf.shape(predictions)[1], dtype=tf.float32)
        grid_w = tf.cast(tf.shape(predictions)[2], dtype=tf.float32)
        n_boxes = tf.cast(tf.shape(predictions)[3], dtype=tf.float32)
        n_classes = tf.shape(predictions)[4] - 5

        grid_coord = yolo_grid(1, grid_h, grid_w, n_boxes)
        if label:
            p_box_xy, p_box_wh, p_box_conf, p_box_class = extract_label(
                predictions, tb=True)
        else:
            p_box_xy, p_box_wh, p_box_conf, p_box_class = extract_model_output(
                predictions, grid_coord, anchors)

        # Process xywh - coordinates
        # Convert from grid units to IMG coordinates [(0,1), (0,1)].
        # TODO validate next
        p_box_xy = p_box_xy / grid_w
        p_box_wh = p_box_wh / grid_w
        # From center coords (xcenter, ycenter) & width & height to:
        # (xmin,ymin), (x_max,ymax).
        bb_xymin = p_box_xy - p_box_wh / 2.
        bb_xymax = p_box_xy + p_box_wh / 2.

        # Shape (1, grid, grid, anchors, 4).
        boxes = tf.concat([bb_xymin, bb_xymax], axis=-1)

        # Filter predictions with class_conf below obj threshold.
        # class_confidence = box_confidence * class probability
        class_confidence = p_box_conf * tf.nn.softmax(
            tf.cast(p_box_class, dtype=tf.float32))

        if label:
            masked_class_confidence = class_confidence
        else:
            mask = class_confidence > class_conf_threshold
            masked_class_confidence = class_confidence * tf.cast(
                mask, dtype=tf.float32)

        # Get index of class with highest logit
        # p_box_class shape (1, 16, 16, 5, 20)
        # tf.argmax output shape -> (1, 16, 16, 5)
        masked_classes = tf.argmax(masked_class_confidence, axis=-1)
        masked_confidence = tf.reduce_max(masked_class_confidence, axis=-1)

        # flattened tensor length
        shape = grid_h * grid_w * n_boxes
        # For tf non-max suppresion input.
        boxes = tf.reshape(boxes, shape=(shape, 4))

        # Flatten classes
        masked_classes = tf.cast(tf.reshape(masked_classes, shape=[shape]),
                                 dtype=tf.float32)

        # Flatten class_confidence.
        masked_confidence = tf.reshape(masked_confidence, shape=[shape])

        if tb:
            return masked_classes, masked_confidence, boxes
        selected_indices = []

        # apply multiclass NMS
        for c in range(n_classes):
            class_mask = tf.cast(tf.math.equal(masked_classes, c),
                                 dtype=tf.float32)
            score_mask = tf.cast(masked_confidence > 0, dtype=tf.float32)
            mask = class_mask * score_mask
            # Prunes away boxes that have high intersection-over-union (IOU)
            # overlap with previously selected boxes. Run nms independently for
            # each class.
            selected_indices_per_class = tf.image.non_max_suppression(
                boxes, masked_confidence * mask, max_number_bb, iou_threshold,
                0.0)

            selected_indices.append(selected_indices_per_class)

        # Flatten nested list.
        selected_indices = tf.concat(selected_indices, axis=-1)
        selected_boxes = tf.gather(boxes, selected_indices)
        selected_confidence = tf.gather(masked_confidence, selected_indices)
        selected_classes = tf.gather(masked_classes, selected_indices)

        return selected_boxes, selected_confidence, selected_classes

    def _prediction_to_tensorboard(self,
                                   input,
                                   prediction,
                                   max_outputs,
                                   step,
                                   iou_threshold,
                                   class_conf_threshold,
                                   label=False):
        tb_imgs = []
        for img in range(max_outputs):
            classes, confidence, boxes = self.decode_yolo_output(
                tf.expand_dims(prediction[img, :, :, :], 0),
                self.anchors,
                class_conf_threshold=class_conf_threshold,
                tb=True,
                label=label)

            # Apply multiclass NMS.
            selected_indices = []
            for c in range(self.n_classes):
                # only include boxes of the current class, with > 0 confidence
                class_mask = tf.cast(tf.equal(classes,
                                              tf.cast(c, dtype=tf.float32)),
                                     dtype=tf.float32)
                conf_mask = tf.cast(confidence > 0, dtype=tf.float32)
                mask = class_mask * conf_mask

                # Prunes away boxes that have high intersection-over-union (IOU)
                # overlap with previously selected boxes. Run nms independently
                # for each cl.
                selected_indices_per_class = tf.image.non_max_suppression(
                    boxes, confidence * mask, 1000, iou_threshold, 0.0)

                selected_indices.append(selected_indices_per_class)

            # Flatten nested list.
            selected_indices = tf.concat(selected_indices, axis=-1)
            selected_boxes = tf.gather(boxes, selected_indices)
            selected_classes = tf.gather(classes, selected_indices)
            selected_confidence = tf.gather(confidence, selected_indices)
            selected_boxes = tf.cast(tf.expand_dims(selected_boxes, 0),
                                     dtype=tf.float32)

            # Swap xy coordinates for bullshit tensorflow draw_bounding_boxes.
            x1 = selected_boxes[..., 0:1]
            y1 = selected_boxes[..., 1:2]
            x2 = selected_boxes[..., 2:3]
            y2 = selected_boxes[..., 3:4]
            boxes_yx = tf.concat([y1, x1, y2, x2], axis=-1)

            tb_img = tf.image.draw_bounding_boxes(
                tf.cast(tf.expand_dims(input[img, :, :, :], 0),
                        dtype=tf.float32), boxes_yx, self.colors)
            tb_imgs.append(tb_img)

        tb_output = tf.concat(tb_imgs, axis=0)
        #tf.summary.image("prediction", tb_output, step=step)
        return tb_output
