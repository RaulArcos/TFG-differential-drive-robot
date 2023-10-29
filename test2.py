from RobotUcaDetector import detector
import time
import cv2

detector = detector.RobotUcaDetector(model_path='/etc/robotuca/models/yolov7-tiny.pt')

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while cap.isOpened():
        ret, frame = cap.read()
        start_time = time.time()
        boxes, scores, _ = detector.detect(frame)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Inference time: {elapsed_time * 1000} ms")
                                                    
        for i in range(len(boxes)):
            if scores[i] > 0.5:
                x1, y1, x2, y2 = boxes[i]
                color = (0, 255, 0)
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness=2)
                label = f"Score: {scores[i]:.2f}"
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()