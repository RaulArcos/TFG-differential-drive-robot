from video_client import *
import cv2

if __name__ == '__main__':
    video_client = gstVideoClient()
    video_client.init()
    while(True):
        _, frame = video_client.get_frame()
        cv.imshow('frame', frame)
        cv2.destroyAllWindows()
            

