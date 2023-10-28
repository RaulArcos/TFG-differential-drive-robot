import yolov7

class RobotUcaDetector:
    def __init__(self, model_path='/etc/robotuca/models/yolov7.pt', device = '0', trace=False, size=640, half=False, hf_model=False):
        self._model = yolov7.load('/etc/robotuca/models/yolov7.pt', '0', trace=False, size=640, hf_model=False)
        self._model.conf = 0.25
        self._model.iou = 0.45
    
    def detect(self, img):
        results = self._model(img, size=640, augment=True)
        predictions = results.pred[0]
        boxes = predictions[:, :4]
        scores = predictions[:, 4]
        categories = predictions[:, 5]
        return boxes, scores, categories