from robotUcaDetector.yolo_with_plugins import TrtYOLO
import numpy as np


##
#  This class manages a tensorrt yolo based object detector
#
class TrtYoloObjectDetector:
    ##
    #  Constructor of the class
    #
    def __init__(self):
        ## list of detection classes
        self._classesList = None
        ## nn model path
        self._modelPath = ""

        ## tensorrt model
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
    #  @return empty numpy arrays
    def blankInference(self, size=640):
        # blankImage = np.zeros((size, size, 3), np.uint8)       ->   it seems that the model does it already on loading
        # return self.inference_object(blankImage)
        self._ready = True
        return np.array([]), np.array([]), np.array([]), 0

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
            # Load saved model
            try:
                n_classes = max(self._classesList)
                self._model = TrtYOLO(self._modelPath, n_classes)
                ret = True
            except Exception as e:
                print("Error al cargar YOLO!!!")
                print(e)
                self._model = None

        return ret

    ##
    #   Clean the model
    #
    def closeModel(self):
        del self._model
        self._model = None

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
        boxes_yolo = np.array([])
        boxes = np.array([])
        scores = np.array([])
        classes_yolo = np.array([])

        ret = boxes, scores, classes_yolo, 0
        h = image.shape[0]
        w = image.shape[1]

        if self._model is not None:
            boxes_yolo, scores, classes_yolo = self._model.detect(
                image, conf_th=threshold, nms_threshold=nms_threshold
            )

            if not self._ready:
                self._ready = True

            if len(boxes_yolo) > 0:
                # adapt from yolo classes (starting in 0)
                classes = np.array(classes_yolo)
                len_aux = len(classes)
                for i in range(len_aux):
                    classes[i] += 1

                # mask to filter the classes and the values > 0
                if self._classesList is not None and len(self._classesList) > 0:
                    mask = np.isin(classes, self._classesList) & (scores > 0.0)
                else:
                    mask = scores > 0.0

                # detection_classes should be ints.
                classes = classes.astype(np.int64)

                # boxes from absolute [x1,y1,x2,y2] int to relative [y1,x1,y2,x2] float
                boxes = np.array(boxes_yolo, dtype=np.float)
                for i, box in enumerate(boxes_yolo):
                    box = np.asarray(
                        [float(box[1]), float(box[0]), float(box[3]), float(box[2])]
                    )
                    boxes[i] = np.array(box, dtype=np.float)
                len_aux = len(boxes)
                for i in range(len_aux):
                    box = boxes[i]
                    boxes[i][0] = box[0] / h
                    boxes[i][1] = box[1] / w
                    boxes[i][2] = box[2] / h
                    boxes[i][3] = box[3] / w

                if len(classes) > 0:
                    ret = boxes[mask], scores[mask], classes[mask], len(classes[mask])

        return ret
