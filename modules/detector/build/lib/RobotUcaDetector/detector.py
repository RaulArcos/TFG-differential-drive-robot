import yolov7

class RobotUcaDetector:
    def __init__(self, model_path='/etc/robotuca/models/yolov7.pt', device = '0', trace=False, size=640, half=False):
        self._model = yolov7.load(model_path, device, trace=trace, size=size, hf_model=half)
        self._model.conf = 0.25
        self._model.iou = 0.45
    
    def detect(self, img, size = 720, augment = True):
        results = self._model(img, size=720, augment=True)
        predictions = results.pred[0]
        boxes = predictions[:, :4]
        scores = predictions[:, 4]
        categories = predictions[:, 5]
        return boxes, scores, categories
    
    def detect_person_only(self, img, size = 720, augment = True):
        boxes, scores, categories = self.detect(img)

        person_boxes = []
        person_scores = []

        for i in range(len(boxes)):
            if categories[i] == 0:
                person_boxes.append(boxes[i])
                person_scores.append(scores[i])
        
        return person_boxes, person_scores