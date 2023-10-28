import tensorflow.compat.v1 as tf
import numpy as np


# Enable eager execution
tf.compat.v1.enable_eager_execution()
# Disable tf2 behaviour
tf.disable_v2_behavior()


##
#  This class manages a TF 1 object detector
#
class TF1ObjectDetector:
    ##
    #  Constructor of the class
    #
    def __init__(self):
        ## list of detection classes
        self._classesList = None
        ## nn model path
        self._modelPath = ""

        # tensorflow params

        ## image converted to a tensor
        self._imageTensor = None
        ## detections bounding boxes
        self._detectionBoxes = None
        ## detections scores
        self._detectionScores = None
        ## detections classes
        self._detectionClasses = None
        ## number of detections
        self._numDetections = None
        ## tensorflow session
        self._sess = None
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
            self._modelPath += "/frozen_inference_graph.pb"
            detection_graph = tf.Graph()

            with detection_graph.as_default():
                od_graph_def = tf.GraphDef()
                with tf.gfile.GFile(self._modelPath, "rb") as f:
                    od_graph_def.ParseFromString(f.read())
                    tf.import_graph_def(od_graph_def, name="")

                self._sess = tf.Session(graph=detection_graph)

            self._imageTensor = detection_graph.get_tensor_by_name("image_tensor:0")
            self._detectionBoxes = detection_graph.get_tensor_by_name(
                "detection_boxes:0"
            )
            self._detectionScores = detection_graph.get_tensor_by_name(
                "detection_scores:0"
            )
            self._detectionClasses = detection_graph.get_tensor_by_name(
                "detection_classes:0"
            )
            self._numDetections = detection_graph.get_tensor_by_name("num_detections:0")
            ret = True

        self._ready = ret

        return ret

    ##
    #   Detects objects in the given frame by applying an inference on
    #   the configured model and filters the results to just the classes desired
    #
    #   @param frame   image frame to detect objects in it
    #
    #   @return  detected objects tuple: - list of bounding boxes of the detected objects
    #                                    - list of scores obtained for the detected objects
    #                                    - list of the classes of the detected objects
    #                                    - number of classes detected (only the filtered ones)
    #
    def inference_object(
        self, frame, threshold: float = 0.3, nms_threshold: float = 0.5
    ):
        frame_expanded = np.expand_dims(frame, axis=0)

        (boxes, scores, classes, n_detections) = self._sess.run(
            [
                self._detectionBoxes,
                self._detectionScores,
                self._detectionClasses,
                self._numDetections,
            ],
            feed_dict={self._imageTensor: frame_expanded},
        )
        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        classes = np.squeeze(classes)
        # n_detections = np.squeeze(n_detections)

        # mascara para filtrar las clases de interes y los valores > 0
        if self._classesList is not None and len(self._classesList) > 0:
            mask = np.isin(classes, self._classesList) & (scores > 0.0)
        else:
            mask = scores > 0.0

        if not self._ready:
            self._ready = True

        return boxes[mask], scores[mask], classes[mask], len(classes[mask])

    ##
    #   Clean the model
    #
    def closeModel(self):
        self._imageTensor = None
        self._detectionBoxes = None
        self._detectionScores = None
        self._detectionClasses = None
        self._numDetections = None
        self._sess = None
