import yolov7
import cv2
import time

model = yolov7.load('/etc/robotuca/models/yolov7.pt', '0', trace=False, size=640, hf_model=False)
# set model parameters
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold

def main():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        results = model(frame, size=640, augment=True)
        predictions = results.pred[0]
        boxes = predictions[:, :4] # x1, y1, x2, y2
        scores = predictions[:, 4]
        categories = predictions[:, 5]
        
        for i in range(len(boxes)):
            if scores[i] > 0.5:
                x1, y1, x2, y2 = boxes[i]
                category = int(categories[i])
                color = (0, 255, 0)  # This example uses green (BGR format)
                
                # Draw the rectangle on the frame
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness=2)
                label = f"Category: {category}, Score: {scores[i]:.2f}"
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()