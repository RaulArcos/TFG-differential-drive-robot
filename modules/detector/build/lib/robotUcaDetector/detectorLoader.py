from robotUcaDetector.tools import Tools
##
#      Class DetectorLoader
#
#      Loads detector object  with the correct framework object specified in config
#
class DetectorLoader:
    ## Implemented frameworks
    _TRUSTED_DETECTOR_FRAMEWORKS = ["darkYolo"]

    ##
    #  Instantiates the detector object
    #
    #   @return detector
    #
    @staticmethod
    def create(type: str):
        if type not in __class__._TRUSTED_DETECTOR_FRAMEWORKS:
            return None
    
        if type == "darkYolo":
            from .detectors import DarknetObjectDetector
            return DarknetObjectDetector()
        
        # return None
