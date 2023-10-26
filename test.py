from robotUcaDetector.detector import Detector
import cv2
import time

def main():
    detector = Detector()
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # Width
    cap.set(4, 720)   # Height
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            filtered_boxes, filtered_scores, filtered_classes, filtered_detections = detector.runNormalInferenceOperationCustomFrame(frame)
            print(filtered_boxes)
            cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    detector.unload()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()