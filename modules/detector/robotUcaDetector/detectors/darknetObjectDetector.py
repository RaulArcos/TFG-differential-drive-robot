import cv2
import numpy as np
import os
import darknet
import random


##
#  This class manages a (Darknet) yolo based object detector
#
class DarknetObjectDetector:
    ##
    #  Constructor of the class
    #
    def __init__(self):
        # NN
        self.network = None

        ## list of detection classes and parameters
        self._classesList = None
        self._filter_dets = False
        self.discarded_dets = []
        self.classes_id = {}

        # model parameters
        self.threshold = None
        self.hier_threshold = None
        self.nms = None
        self.net_width = None
        self.net_height = None
        self.class_names = None
        self.class_colors = random.seed(3)

        ## detector ready (after first inference) flag
        self._ready = False

        ##cuda stream for parallel ops
        self.stream = cv2.cuda_Stream()

    @property
    def model_width(self):
        return self.net_width

    @property
    def model_height(self):
        return self.net_height

    ##
    #  Checks if the detector is ready (first inference executed yet)
    #  @return true if the detector is ready and false otherwise
    #
    def isReady(self):
        return self._ready

    ##
    #  Executes and inference with a blank image -> first inference can be very hard
    #     and applying an inference after de data is ready can be needed to start
    #     inferencing rapidly from the first frame
    #
    def blankInference(self):
        blank_image = np.ones((10000, 10000, 3), np.uint8) * 255
        self.inference_object(blank_image)
        self._ready = True
        print("Blank Inference done, detector ready  !!")

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
        ret = True
        try:
            config_path = os.path.join(modelPath, "yolo-obj.cfg")
            weights_path = os.path.join(modelPath, "yolo-obj.weights")
            data_path = os.path.join(modelPath, "obj.data")
            random.seed(
                3
            )  # deterministic bbox colors, ignore for now as colors are determined by videomanager
            network, class_names, class_colors = darknet.load_network(
                config_path, data_path, weights_path, 1
            )
            self.network = network
            self.net_width = darknet.network_width(network)
            self.net_height = darknet.network_height(network)
            if self._classesList is None:
                self._classesList = class_names
            else:
                self._filter_dets = True
                for class_name in class_names:
                    if class_name not in self._classesList:
                        self.discarded_dets.append(class_name)
            self.class_names = class_names
            self.class_colors = class_colors

            self.threshold = detection_threshold
            self.hier_threshold = hier_threshold
            self.nms = nms_threshold

            for i in range(0, len(class_names)):
                self.classes_id[class_names[i]] = int(i + 1)

        except Exception as e:
            print(str(e))
            ret = False

        return ret

    ##
    #   Clean the model
    #
    def closeModel(self):
        del self.network
        self.network = None
        self._ready = False

    ##
    #   Detects objects in the given frame by applying an inference on
    #   the configured model and filters the results to just the classes desired
    #   wrapper function for parent detector
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
        frame = self.preprocess(image)
        dets = self.image_detection(frame, threshold, nms_threshold)

        if self._filter_dets:
            filtered_dets = []
            for det in dets:
                if not any(remove == det[0] for remove in self.discarded_dets):
                    filtered_dets.append(det)
            ret = self.postprocess(filtered_dets)
        else:
            ret = self.postprocess(dets)
        return ret

    ##
    #  prepare frame for detection
    #
    #  @param image   image to preprocess, must be in cv2 format
    #
    #  @return output image   returns the image in cpu memory resized to the net and rgb format for darknet
    #
    def preprocess(self, image):
        in_gpu = cv2.cuda_GpuMat()
        out_gpu = cv2.cuda_GpuMat()
        in_gpu.upload(image)
        out_gpu = cv2.cuda.resize(
            in_gpu,
            (self.net_width, self.net_height),
            interpolation=cv2.INTER_AREA,
            stream=self.stream,
        )
        out_gpu = cv2.cuda.cvtColor(out_gpu, cv2.COLOR_BGR2RGB, stream=self.stream)
        return out_gpu.download()

    ##
    #  post process detections for data transmission
    #
    #  @param detections list of detections in darknet format to filter and convert to np arrays
    #
    #  @return  detected objects tuple:  - list of bounding boxes of the detected objects
    #                                    - list of scores obtained for the detected objects
    #                                    - list of the classes of the detected objects
    #                                    - number of classes detected (only the filtered ones)
    #
    def postprocess(self, detections):
        boxes = []
        scores = []
        classes = []

        for det in detections:
            box = det[-1]
            x = max(0.0, (box[0] - box[2] / 2) / self.model_width)
            y = max(0.0, (box[1] - box[3] / 2) / self.model_height)
            w = min(1.0 - x, box[2] / self.model_width)
            h = min(1.0 - y, box[3] / self.model_height)
            boxes.append((x, y, w, h))
            scores.append(float(det[1]) / 100.0)
            classes.append(self.classes_id[det[0]])
        return np.asarray(boxes), np.asarray(scores), np.asarray(classes), len(classes)

    ##
    #  Actual inference on image
    #
    #  @param image  the image to infer upon
    #  @param thresh the minimum threshold for an object to be detected
    #  @nms_thresh hierarchichal thresh , determines how close the detections should be grouped together to be considered a single object
    #
    #  @return detections list containing detections coordinates, scores and classnames
    #
    def image_detection(self, image, thresh, nms_thresh):
        # Darknet doesn't accept numpy images.
        # Create one with image we reuse for each detect
        darknet_image = darknet.make_image(self.net_width, self.net_height, 3)
        darknet.copy_image_from_bytes(darknet_image, image.tobytes())
        ## actual detection
        detections = darknet.detect_image(
            self.network,
            self.class_names,
            darknet_image,
            thresh=thresh,
            hier_thresh=thresh,
            nms=nms_thresh,
        )
        darknet.free_image(darknet_image)
        # image = darknet.draw_boxes(detections, image, class_colors)
        # del darknet_image
        return detections
