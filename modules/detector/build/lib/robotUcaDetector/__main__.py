import sys
from robotUcaDetector.detector import Detector


if __name__ == "__main__":
    detector = Detector(*tuple(sys.argv[1:]))
