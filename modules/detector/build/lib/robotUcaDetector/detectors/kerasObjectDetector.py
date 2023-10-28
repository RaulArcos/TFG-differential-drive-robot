import tensorflow as tf

from os.path import splitext

# Enable eager execution
tf.compat.v1.enable_eager_execution()


##
#  This class manages a keras object detector
#
class KerasObjectDetector:
    ##
    #  Constructor of the class
    #
    def __init__(self):
        ## list of detection classes
        self._classesList = None
        ## nn model path
        self._modelPath = ""
        ## nn weights path
        self._weightsPath = ""

        ## Keras model
        self._model = None

        ## detector ready (after first inference) flag
        self._ready = False

    ##
    #  Loads the given model
    #
    #  @param modelPath        path of the model inference graph
    #  @param weightsPath      path to the model weights
    #  @param classes_list     classes thar will be returned on inference. If classes is none or empty
    #                             the inference will return every class type
    #
    #  @return true if model is correctly loaded
    def loadModel(self, modelPath, weightsPath, classes_list=None):
        ret = False

        self._modelPath = modelPath
        self._weightsPath = weightsPath
        self._classesList = classes_list
        if self._modelPath is not None and len(self._modelPath) > 0:
            try:
                mPath = splitext(self._modelPath)[0]
                with open("%s.json" % mPath, "r") as json_file:
                    model_json = json_file.read()
                    json_file.close()
                self._model = tf.keras.models.model_from_json(
                    model_json, custom_objects={}
                )

                if self._weightsPath is not None and len(self._weightsPath) > 0:
                    wPath = splitext(self._weightsPath)[0]
                    self._model.load_weights("%s.h5" % wPath)
                    ret = True
            except Exception as e:
                print(e)
                ret = False
                return ret

        self._ready = ret

        return ret

    ##
    #  Gets Keras model
    #
    def getModel(self):
        return self._model

    ##
    #  Gets ready var
    #
    def isReady(self):
        return self._ready

    ##
    #   Cleans the model
    #
    def closeModel(self):
        return
