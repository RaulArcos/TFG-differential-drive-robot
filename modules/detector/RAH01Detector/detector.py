import yolov7
import cv2

class RAH01Detector:
    def __init__(self, model_path='/etc/rah01/models/yolov7.pt', device = '0', trace=False, size=416, half=False):
        self._model = yolov7.load(model_path, device, trace=trace, size=size, hf_model=half)
        self._model.conf = 0.25
        self._model.iou = 0.45
    
    def detect(self, img, size = 720, augment = True):
        results = self._model(img, size=416, augment=False)
        predictions = results.pred[0]
        boxes = predictions[:, :4]
        scores = predictions[:, 4]
        categories = predictions[:, 5]
        return boxes, scores, categories
    
    def drawDetections(self, img, boxes, scores, categories):
        # img = yolov7.draw_boxes(img, boxes, scores, categories)
        for i in range(len(boxes)):
            if categories[i] == 0:
                x1, y1, x2, y2 = boxes[i]
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(img, str(int(scores[i] * 100)) + "%", (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return img
    
    def detectPersonOnly(self, img, size = 720, augment = True):
        boxes, scores, categories = self.detect(img)
        person_boxes = []
        person_scores = []
        for i in range(len(boxes)):
            if categories[i] == 0 and scores[i] > 0.6:
                person_boxes.append(boxes[i])
                person_scores.append(scores[i])
        
        return person_boxes, person_scores