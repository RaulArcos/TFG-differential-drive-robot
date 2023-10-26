import cv2
import numpy as np
import re
import os

try:
    from .cyolo import *
except Exception:
    pass


##
#  Helper bbox class
#
class BBox(np.ndarray):
    ##
    #  Creates bbox instance
    #  @param x, y, w, h   bbox coordinates
    #  @param prob         probability detection
    #  @param name         class name
    #  @param class_id     yolo class id
    #
    def __new__(cls, x, y, w, h, prob, name, class_id):
        cls.name = ""
        cls.prob = 0
        obj = np.asarray([x, y, w, h]).view(cls)
        obj.x, obj.y, obj.w, obj.h = obj.view()
        obj.name = name
        obj.prob = prob
        obj.class_id = class_id

        return obj

    ##
    #  bbox object to string converter
    #
    def __str__(self):
        x, y, w, h = self.view()
        string = f"x: {x}, y: {y}, w: {w}, h: {h}, "
        string += f"probability: {self.prob}, name: {self.name}"

        return string

    ##
    #  Converts relative x, y, w, h values to relative y1, x1, y2, x2 coordinates
    #
    def to_yxyx(self):
        x, y, w, h = self.view()

        return np.array([float(y), float(x), float(y + h), float(x + w)])


##
#  This class manages a (Darknet) yolo based object detector
#
class DarkYoloObjectDetector:
    ##
    #  Constructor of the class
    #
    def __init__(self):
        # NN and metadata
        self.net_main = None
        self.meta_main = None

        ## list of detection classes
        self._classesList = None

        # model parameters
        self.threshold = None
        self.hier_threshold = None
        self.nms = None

        ## detector ready (after first inference) flag
        self._ready = False

    @property
    def model_width(self):
        return self.height

    @property
    def model_height(self):
        return self.width

    ##
    #  Checks if the detector is ready (first inference executed yet)
    #  @return true if the detector is ready and false otherwise
    def isReady(self):
        return self._ready

    ##
    #  Executes and inference with a blank image -> first inference can be very hard
    #     and applying an inference after de data is ready can be needed to start
    #     inferencing rapidly from the first frame
    #
    def blankInference(self):
        self._ready = True
        return np.array([]), np.array([]), np.array([]), 0

    ##
    #  Loads the given model
    #  @param modelPath             path of model .cfg .weights .data and .names files
    #  @param classes_list          classes thar will be returned on inference. If classes is none or empty
    #                               the inference will return every class type
    #  @param detection_threshold   detection threshold
    #  @param hier_threshold        hierarchical threshold
    #  @param nms_threshold         NMS threshold
    #
    #  @return True if the model was loaded succesfully, False if not
    #
    def loadModel(
        self,
        modelPath,
        classes_list=None,
        detection_threshold=0.0,
        hier_threshold=0.0,
        nms_threshold=0.0,
    ):
        ret = False
        self._classesList = classes_list
        print(modelPath)
        print(classes_list)

        config_path = os.path.join(modelPath, "yolo-obj.cfg")
        weights_path = os.path.join(modelPath, "yolo-obj.weights")
        data_path = os.path.join(modelPath, "obj.data")

        if not os.path.exists(config_path):
            raise ValueError(f"Invalid config path: {os.path.abspath(config_path)}")
        if not os.path.exists(weights_path):
            raise ValueError(f"Invalid weight path: {os.path.abspath(weights_path)}")
        if not os.path.exists(data_path):
            raise ValueError(f"Invalid data file path: {os.path.abspath(data_path)}")

        self.net_main = load_net_custom(
            config_path.encode("ascii"), weights_path.encode("ascii"), 0, 1
        )
        self.meta_main = load_meta(data_path.encode("ascii"))

        self.height = lib.network_height(self.net_main)
        self.width = lib.network_width(self.net_main)

        with open(data_path) as metaFH:
            meta_contents = metaFH.read()
            match = re.search(
                "names *= *(.*)$", meta_contents, re.IGNORECASE | re.MULTILINE
            )
            if match:
                result = match.group(1)
            else:
                result = None
            if os.path.exists(result):
                with open(result) as namesFH:
                    names_list = namesFH.read().strip().split("\n")
                    self.alt_names = [x.strip() for x in names_list]
                    ret = True

        self.threshold = detection_threshold
        self.hier_threshold = hier_threshold
        self.nms = nms_threshold
        print("loaded darkyolo object detector model")

        return ret

    ##
    #   Clean the model
    #
    def closeModel(self):
        del self.net_main
        self.net_main = None
        del self.meta_main
        self.meta_main = None

##
# Auxiliary fuction for darkyolo.
# Converts an array to an image class object and to a numpy array
#
# @param arr The array to convert to IMAGE class
#
# @return the array transformed into IMAGE, and original array
#
    def array_to_image(arr):
        arr = arr.transpose(2, 0, 1)
        c = arr.shape[0]
        h = arr.shape[1]
        w = arr.shape[2]
        arr = np.ascontiguousarray(arr.flat, dtype=np.float32) / 255.0
        data = arr.ctypes.data_as(POINTER(c_float))
        im = IMAGE(w, h, c, data)
        return im, arr


    ##
    #   Detects objects in the given frame by applying an inference on
    #   the configured model and filters the results to just the classes desired
    #
    #   @param image           image frame to detect objects in it
    #   @param threshold       detection threshold
    #   @param nms_threshold   NMS threshold
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
        rgb = False

        self.nms = nms_threshold
        self.threshold = threshold

        ret = boxes, scores, classes, 0

        image = cv2.resize(
            image, (self.width, self.height), interpolation=cv2.INTER_CUBIC
        )[:, :, ::-1]
        if not rgb:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        im, arr = array_to_image(image)

        num = c_int(0)
        pnum = pointer(num)

        predict_image(self.net_main, im)
        dets = get_network_boxes(
            self.net_main,
            im.w,
            im.h,
            self.threshold,
            self.hier_threshold,
            None,
            0,
            pnum,
            0,
        )
        num = pnum[0]

        if not self._ready:
            self._ready = True

        if self.nms:
            do_nms_sort(dets, num, self.meta_main.classes, self.nms)

        boxes_l = []
        scores_l = []
        classes_l = []
        for j in range(num):
            for i in range(self.meta_main.classes):
                if dets[j].prob[i] > 0:
                    b = dets[j].bbox

                    # coordinates as percentage
                    x = (b.x - b.w / 2) / self.width
                    y = (b.y - b.h / 2) / self.height
                    w = b.w / self.width
                    h = b.h / self.height

                    bbox = BBox(x, y, w, h, dets[j].prob[i], self.alt_names[i], i)

                    boxes_l.append(bbox.to_yxyx())
                    scores_l.append(bbox.prob)
                    classes_l.append(bbox.class_id + 1)  # yolo classes start from 0

        free_detections(dets, num)

        if num > 0:
            # convert lists to arrays
            boxes = np.array(boxes_l, dtype=np.float)
            scores = np.array(scores_l)
            classes = np.array(classes_l)

            # mask to filter the classes and the values > 0
            if self._classesList is not None and len(self._classesList) > 0:
                mask = np.isin(classes, self._classesList) & (scores > 0.0)
            else:
                mask = scores > 0.0

            # detection_classes should be ints
            classes = classes.astype(np.int64)

            if len(classes[mask]) > 0:
                ret = boxes[mask], scores[mask], classes[mask], len(classes[mask])

        return ret

