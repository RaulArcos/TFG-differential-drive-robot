import numpy as np
import time
import threading
from .active_area import Region, ActiveArea
from .detectorLoader import DetectorLoader
from .detectionDescriptor import DetectionDescriptor
from .grid import GridSize
from .tools import equalizeHSV
from .box_size_filter import BoxSizeFilter

class Detector():
    def __init__(self):
        ## list of detection classes
        self.classes_list = None
        self.type_of_model = "darkYolo"
        self.path_to_model = "/etc/robotuca/models/"
        np.set_printoptions(precision=3)
        self._detector = DetectorLoader.create(self.type_of_model)
        self._loadModel()

        # tensorflow params
        ## tensorflow object detector
        self._detector = None
        ## detector ready (after first inference) flag
        self._ready = False
        ## detector level
        self._model_loaded = False
        ## Filter detections by box size
        self.box_size_filter = BoxSizeFilter()

        ## image preprocess flag
        self._image_preprocess = False
        ## grid mode
        self._grid_size = GridSize()
        ## overlap rate
        self._overlap_rate = 0.05
        ## detections threshold
        self._detection_threshold = 0.3
        ## non maximum supression threshold
        self._nms_threshold = 0.5
        self._active_area = ActiveArea()

    def _loadModel(self):
        if self._model_loaded:
            print("INFO", "Detector model already loaded")
            return

        try:
            self._model_loaded = self._detector.loadModel(
                self.path_to_model, self.classes_list, nms_threshold=0.3
            )
        except Exception:
            print("ERROR", "Could not load model, exiting app..")
            raise SystemExit

    def run_job(self):
        if self._ready and self._model_loaded:
            self.runNormalInferenceOperation()
        elif not self._ready:
            self._ready = True

        return True

    def clean_init(self):
        self._log("DEBUG", "clean_init")
        self.context.destroy()
        self._videoClient.close()

        return True

   
    def _inference_on_frame(self, _frame):
        if not self._ready:
            # First blank inference
            return self._detector.blankInference()

        # Pre-process the image
        image = equalizeHSV(_frame) if self._image_preprocess else _frame
        height = image.shape[0]
        width = image.shape[1]

        grid_x, grid_y = self._grid_size.compute_grid_size(
            width / self._detector.model_width, height / self._detector.model_height
        )

        n_cells = grid_x * grid_y

        if n_cells <= 1:
            return self._inference(image)
        else:
            return self._inference_on_multiple_cells(
                image, height, width, grid_x, grid_y, n_cells
            )

    def _inference_on_multiple_cells(
        self, image, height, width, grid_x, grid_y, n_cells
    ):
        boxes = np.asarray([])
        scores = np.array([])
        classes = np.array([])
        ndetections = 0
        
        w_step = int(width / grid_x)
        h_step = int(height / grid_y)
        w_margin = int(width * self._overlap_rate)
        h_margin = int(height * self._overlap_rate)

        for i in range(n_cells):
            x = w_step * (i % grid_x)
            y = h_step * (i // grid_x)

            x1 = max(x - w_margin, 0)
            y1 = max(y - h_margin, 0)
            x2 = min(width - 1, x + w_step + w_margin)
            y2 = min(height - 1, y + h_step + h_margin)
            i_w = x2 - x1
            i_h = y2 - y1

            if not self._active_area.check_active_cell(x1, x2, y1, y2, width, height):
                continue

            cell_boxes, cell_scores, cell_classes, cell_n_detections = self._inference(image[y1:y2, x1:x2])

            if cell_n_detections is not None and cell_n_detections > 0:
                ndetections += cell_n_detections
                scores = np.concatenate((scores, cell_scores))
                classes = np.concatenate((classes, cell_classes))
                for b in cell_boxes:
                    #    sub img w/h  sub img start x/y  image w/h
                    b[0] = (b[0] * i_h + y1) / height
                    b[1] = (b[1] * i_w + x1) / width
                    b[2] = (b[2] * i_h + y1) / height
                    b[3] = (b[3] * i_w + x1) / width

                boxes = np.concatenate((boxes, cell_boxes))
                #self._log("INFO", f"Inference {i+1}/{n_cells} - Detections: {res[3]}")

        return boxes, scores, classes, ndetections

    def _inference(self, frame):
        # boxes, scores, classes, n_detections = self._detector.inference_object(frame, self._detection_threshold, self._nms_threshold)
        return self._detector.inference_object(
            frame, self._detection_threshold, self._nms_threshold
        )

    def _get_frame(self):
        if self._videoClient is None:
            return None, None

        n_frame, frame = self._videoClient.get_frame()
            
        if frame is None:
            time.sleep(0.001)
            return None, None

        return n_frame, frame

    def runNormalInferenceOperation(self):
        n_frame, frame = self._get_frame()
        
        if n_frame is None:
            return

        boxes, scores, classes, n_detections = self._inference_on_frame(frame)

        (
            filtered_boxes,
            filtered_scores,
            filtered_classes,
            filtered_detections,
        ) = self.box_size_filter.filter_boxes(boxes, scores, classes)
        if self._detector_level == Detector.DETECTOR_SECONDARY:
            self.send_from_sw11(n_frame, filtered_boxes, filtered_classes)
        else:
            self.send_from_sw01(
                n_frame,
                filtered_boxes,
                filtered_scores,
                filtered_classes,
                filtered_detections,
            )
    def runNormalInferenceOperationCustomFrame(self, frame):
        boxes, scores, classes, n_detections = self._inference_on_frame(frame)

        (
            filtered_boxes,
            filtered_scores,
            filtered_classes,
            filtered_detections,
        ) = self.box_size_filter.filter_boxes(boxes, scores, classes)
        return(
            filtered_boxes,
            filtered_scores,
            filtered_classes,
            filtered_detections,
            )