from RobotUcaDetector import detector
import time
import cv2
import math

detector = detector.RobotUcaDetector(model_path='/etc/robotuca/models/yolov7-tiny.pt')

def main():
    cap = cv2.VideoCapture(0)
    width = 1280
    height = 720
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while cap.isOpened():
        ret, frame = cap.read()
        start_time = time.time()
        boxes, scores = detector.detectPersonOnly(frame)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Inference time: {elapsed_time * 1000} ms")
                                                    
        for i in range(len(boxes)):
            if scores[i] > 0.5:
                x1, y1, x2, y2 = boxes[i]
                fov = 55
                object_width_real_world = 0.55
                box_width = x2 - x1
                normalized_width = box_width / width
                box_area = (x2 - x1) * (y2 - y1)
                box_area_norm = box_area / (width * height)
                box_center = ((x2 + x1) / 2, (y2 + y1) / 2)
                box_center_norm = ((box_center[0] / width), (box_center[1] / height))
                color = (0, 255, 0)
                distance = (object_width_real_world) / (2 * math.tan(math.radians(fov / 2)) * (1280 / box_width))
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness=2)
                label = f"distance: {distance}"
                cv2.putText(frame, label, (int(box_center[0]), int(box_center[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()