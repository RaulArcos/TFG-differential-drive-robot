import tensorflow as tf
import numpy as np

# Enable eager execution
tf.compat.v1.enable_eager_execution()


##
#  This class manages a TF 2 object detector
#
class TF2ObjectDetector:
    ##
    #  Constructor of the class
    #
    def __init__(self):
        ## list of detection classes
        self._classesList = None
        ## nn model path
        self._modelPath = ""

        ## tensorflow model
        self._model = None
        ## detector ready (after first inference) flag
        self._ready = False

    ##
    #  Checks if the detector is ready (first inference executed yet)
    #  @return true if the detector is ready and false otherwise
    def isReady(self):
        return self._ready

    ##
    #  Executes and inference with a blank image -> first inference can be very hard
    #     and applying an inference after de data is ready can be needed to start
    #     inferencing rapidly from the first frame
    #  @param size size of the black image (width and height of a square image)
    #  @return object detection inference from a blank Image
    def blankInference(self, size=640):
        blankImage = np.zeros((size, size, 3), np.uint8)
        return self.inference_object(blankImage)

    ##
    #  Loads the given model
    #  @param modelPath  path of the model infernce graph
    #  @param classes_list    classes thar will be returned on inference. If classes is none or empty
    #                    the inference will return every class type
    #  @return True if the model was succesfully loaded, False otherwise
    def loadModel(self, modelPath, classes_list=None):
        ret = False

        self._modelPath = modelPath
        self._classesList = classes_list

        if self._modelPath is not None and len(self._modelPath) > 0:
            # Load saved model and build the detection function
            path_saved_model = self._modelPath + "/saved_model"
            self._model = tf.saved_model.load(path_saved_model)
            ret = True

        return ret

    ##
    #   Converts input to tensor and performs an inference
    #
    #   @param image   image frame to detect objects in it
    #   @param dtype   input type
    #
    #   @return  inferred tensor
    #
    def _inference(self, image, dtype=None):
        image_np = np.asarray(image)
        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        if dtype:
            input_tensor = tf.convert_to_tensor(image_np, dtype)
        else:
            input_tensor = tf.convert_to_tensor(image_np)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        # Run inference
        inference = self._model(input_tensor)

        return inference

    ##
    #   Detects objects in the given frame by applying an inference on
    #   the configured model and filters the results to just the classes desired
    #
    #   @param image   image frame to detect objects in it
    #
    #   @return  detected objects tuple: - list of bounding boxes of the detected objects
    #                                    - list of scores obtained for the detected objects
    #                                    - list of the classes of the detected objects
    #                                    - number of classes detected (only the filtered ones)
    #
    def inference_object(
        self, image, threshold: float = 0.3, nms_threshold: float = 0.5
    ):
        boxes = np.array([])
        scores = np.array([])
        classes = np.array([])

        output_dict = self._inference(image)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(output_dict.pop("num_detections"))
        if num_detections != 0:
            output_dict = {
                key: value[0, :num_detections].numpy()
                for key, value in output_dict.items()
            }
            output_dict["num_detections"] = num_detections

            # detection_classes should be ints.
            output_dict["detection_classes"] = output_dict["detection_classes"].astype(
                np.int64
            )

            boxes = output_dict["detection_boxes"]
            scores = output_dict["detection_scores"]
            classes = output_dict["detection_classes"]

        # mask to filter the classes and the values > 0
        if self._classesList is not None and len(self._classesList) > 0:
            mask = np.isin(classes, self._classesList) & (scores > 0.0)
        else:
            mask = scores > 0.0

        if not self._ready:
            self._ready = True

        return boxes[mask], scores[mask], classes[mask], len(classes[mask])

    ##
    #   Detects objects in the given frame by applying an inference on
    #   the configured model and No filter is applied
    #
    #   @param image   image frame to detect objects in it
    #   @param dtype   input type
    #
    #   @return  inferred tensor
    #
    def inference_tensor(self, image, dtype=None):
        tensor = self._inference(image, dtype)

        if not self._ready:
            self._ready = True

        return tensor

    ##
    #   Clean the model
    #
    def closeModel(self):
        self._model = None
