import cv2
import numpy as np
import tensorflow.compat.v1 as tf


# Disable tf2 behaviour
tf.disable_v2_behavior()


##
#   Class implemented to manage super resolution
#   models and operations.
#
class SRUpscale(object):
    ##
    #   Constructor of the class
    #
    def __init__(self):
        ## sr model to use
        self.graph = None
        ## srmodel name
        self.model = None
        ## scale of the model
        self.scale = None
        ## tensorflow session
        self.sess = None
        ## Logger of the class
        self.logger = None

    ##
    #   Initialize and load model
    #
    #   @param model model to load
    #   @param scale scale of the model
    #
    def init(self, model, scale):
        if model and scale:
            self.model = model
            self.scale = scale
            self._log(
                "INFO",
                "Upscale model set to '%s' and scale %dx" % (self.model, self.scale),
            )
            self.loadUpscaleModel()
        else:
            self._log(
                "ERROR",
                "Upscale model set to '%s' and scale %sx"
                % (str(self.model), str(self.scale)),
            )

    ##
    #   Set the logger of the class
    #
    #   @param logger Logger to be set
    #
    def setLogger(self, logger):
        self.logger = logger

    ##
    #   logs a message through the logger
    #
    #   @param level: log level
    #   @param msg: message
    #   @param name: name which with you want to log
    #
    def _log(self, level, msg, name=None):
        if self.logger:
            self.logger.send_message(level, msg, name)
        else:
            print(level + " " + msg)

    ##
    #   Load model
    #
    #   @param path_to_pb path to model
    #
    def load_pb(self, path_to_pb):
        with tf.gfile.GFile(path_to_pb, "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, name="")
            return graph

    ##
    #   Load EDSR model
    #
    #   @param scale scale of the model
    #
    def loadEDSRpb(self, scale):
        # Read model
        pbPath = "./modelos/tf1/EDSR/models/EDSR_x{}.pb".format(scale)
        # Get graph
        self.graph = self.load_pb(pbPath)
        self.sess = tf.Session(graph=self.graph)

    ##
    #   Load ESPCN model
    #
    #   @param scale scale of the model
    #
    def loadESPCNpb(self, scale):
        pbPath = "./modelos/tf1/ESPCN/export/ESPCN_x{}.pb".format(scale)
        self.graph = self.load_pb(pbPath)
        self.sess = tf.Session(graph=self.graph)

    ##
    #   Load FSRCNN model
    #
    #   @param scale scale of the model
    #   @param small is the tiny model or not
    #
    def loadFSRCNNpb(self, scale, small):
        pbPath = "./modelos/tf1/FSRCNN/models/FSRCNN_x{}.pb".format(scale)
        if small:
            pbPath = "./modelos/tf1/FSRCNN/models/FSRCNN-small_x{}.pb".format(scale)
        # Get graph
        self.graph = self.load_pb(pbPath)
        self.sess = tf.Session(graph=self.graph)

    ##
    #   Load LapSRN model
    #
    #   @param scale scale of the model
    #
    def loadLapSRNpb(self, scale):
        pbPath = "./modelos/tf1/LapSRN/export/LapSRN_x{}.pb".format(scale)
        self.graph = self.load_pb(pbPath)
        self.sess = tf.Session(graph=self.graph)

    ##
    #   Perform the upscaling on the given image
    #
    #   @param img   img to scale
    #
    #   @return scaled image with EDSR
    #
    def upscaleEDSRpb(self, img):
        self._log("INFO", "Upscale image with EDSR to %dx" % (self.scale))
        meanbgr = np.asarray([103.1545782, 111.561547, 114.35629928])

        fullimg = img
        floatimg = fullimg.astype(np.float32) - meanbgr
        LR_input_ = floatimg.reshape(1, floatimg.shape[0], floatimg.shape[1], 3)

        LR_tensor = self.graph.get_tensor_by_name("IteratorGetNext:0")
        HR_tensor = self.graph.get_tensor_by_name("NHWC_output:0")

        output = self.sess.run(HR_tensor, feed_dict={LR_tensor: LR_input_})
        Y = output[0]
        HR_image = (Y + meanbgr).clip(min=0, max=255)
        HR_image = (HR_image).astype(np.uint8)

        bicubic_image = cv2.resize(
            fullimg, None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_CUBIC
        )

        return HR_image

    ##
    #   Perform the upscaling on the given image
    #
    #   @param img   img to scale
    #
    #   @return scaled image with ESPCN
    #
    def upscaleESPCNpb(self, img):
        self._log("INFO", "Upscale image with ESPCN to %dx" % (self.scale))
        fullimg = img
        width = fullimg.shape[0]
        height = fullimg.shape[1]

        cropped = fullimg[
            0 : (width - (width % self.scale)), 0 : (height - (height % self.scale)), :
        ]
        floatimg = cropped.astype(np.float32) / 255.0

        # Convert to YCbCr color space
        imgYCbCr = cv2.cvtColor(floatimg, cv2.COLOR_BGR2YCrCb)
        imgY = imgYCbCr[:, :, 0]

        LR_input_ = imgY.reshape(1, imgY.shape[0], imgY.shape[1], 1)
        LR_tensor = self.graph.get_tensor_by_name("IteratorGetNext:0")
        HR_tensor = self.graph.get_tensor_by_name("NHWC_output:0")

        output = self.sess.run(HR_tensor, feed_dict={LR_tensor: LR_input_})

        Y = output[0]
        Cr = np.expand_dims(
            cv2.resize(
                imgYCbCr[:, :, 1],
                None,
                fx=self.scale,
                fy=self.scale,
                interpolation=cv2.INTER_CUBIC,
            ),
            axis=2,
        )
        Cb = np.expand_dims(
            cv2.resize(
                imgYCbCr[:, :, 2],
                None,
                fx=self.scale,
                fy=self.scale,
                interpolation=cv2.INTER_CUBIC,
            ),
            axis=2,
        )

        HR_image_YCrCb = np.concatenate((Y, Cr, Cb), axis=2)
        HR_image = ((cv2.cvtColor(HR_image_YCrCb, cv2.COLOR_YCrCb2BGR)) * 255.0).clip(
            min=0, max=255
        )
        HR_image = (HR_image).astype(np.uint8)

        return HR_image

    ##
    #   Perform the upscaling on the given image
    #
    #   @param img   img to scale
    #
    #   @return scaled image with FSRCNN
    #
    def upscaleFSRCNNpb(self, img):
        self._log("INFO", "Upscale image with FSRCNN to %dx" % (self.scale))

        fullimg = img
        width = fullimg.shape[0]
        height = fullimg.shape[1]

        cropped = fullimg[
            0 : (width - (width % self.scale)), 0 : (height - (height % self.scale)), :
        ]

        # to ycrcb and normalize
        img_ycc = cv2.cvtColor(cropped, cv2.COLOR_BGR2YCrCb)
        img_y = img_ycc[:, :, 0]
        floatimg = img_y.astype(np.float32) / 255.0

        LR_input_ = floatimg.reshape(1, floatimg.shape[0], floatimg.shape[1], 1)

        LR_tensor = self.graph.get_tensor_by_name("IteratorGetNext:0")
        HR_tensor = self.graph.get_tensor_by_name("NHWC_output:0")

        output = self.sess.run(HR_tensor, feed_dict={LR_tensor: LR_input_})

        # post-process
        Y = output[0]
        Y = (Y * 255.0).clip(min=0, max=255)
        Y = (Y).astype(np.uint8)

        # Merge with Chrominance channels Cr/Cb
        Cr = np.expand_dims(
            cv2.resize(
                img_ycc[:, :, 1],
                None,
                fx=self.scale,
                fy=self.scale,
                interpolation=cv2.INTER_CUBIC,
            ),
            axis=2,
        )
        Cb = np.expand_dims(
            cv2.resize(
                img_ycc[:, :, 2],
                None,
                fx=self.scale,
                fy=self.scale,
                interpolation=cv2.INTER_CUBIC,
            ),
            axis=2,
        )
        HR_image = cv2.cvtColor(
            np.concatenate((Y, Cr, Cb), axis=2), cv2.COLOR_YCrCb2BGR
        )

        return HR_image

    ##
    #   Perform the upscaling on the given image
    #
    #   @param img   img to scale
    #
    #   @return scaled image with LapSRN
    #
    def upscaleLapSRNpb(self, img):
        self._log("INFO", "Upscale image with LapSRN to %dx" % (self.scale))

        fullimg = img
        width = fullimg.shape[0]
        height = fullimg.shape[1]

        cropped = fullimg[
            0 : (width - (width % self.scale)), 0 : (height - (height % self.scale)), :
        ]
        floatimg = cropped.astype(np.float32) / 255.0

        # Convert to YCbCr color space
        imgYCbCr = cv2.cvtColor(floatimg, cv2.COLOR_BGR2YCrCb)
        imgY = imgYCbCr[:, :, 0]

        LR_input_ = imgY.reshape(1, imgY.shape[0], imgY.shape[1], 1)
        LR_tensor = self.graph.get_tensor_by_name("IteratorGetNext:0")
        HR_tensor = self.graph.get_tensor_by_name("NCHW_output:0")

        output = self.sess.run(HR_tensor, feed_dict={LR_tensor: LR_input_})

        Y = output[0][0]
        Y = Y.reshape(Y.shape[0], Y.shape[1], 1)
        Cr = np.expand_dims(
            cv2.resize(
                imgYCbCr[:, :, 1],
                None,
                fx=self.scale,
                fy=self.scale,
                interpolation=cv2.INTER_CUBIC,
            ),
            axis=2,
        )
        Cb = np.expand_dims(
            cv2.resize(
                imgYCbCr[:, :, 2],
                None,
                fx=self.scale,
                fy=self.scale,
                interpolation=cv2.INTER_CUBIC,
            ),
            axis=2,
        )

        HR_image_YCrCb = np.concatenate((Y, Cr, Cb), axis=2)
        HR_image = ((cv2.cvtColor(HR_image_YCrCb, cv2.COLOR_YCrCb2BGR)) * 255.0).clip(
            min=0, max=255
        )
        HR_image = (HR_image).astype(np.uint8)

        return HR_image

    ##
    #   Perform the upscaling on the given image
    #
    #   @param img   img to scale
    #
    #   @return scaled image with the defined model of the class
    #
    def upscaleImg(self, img):
        HR_Image = None
        if self.model == "EDSR":
            HR_Image = self.upscaleEDSRpb(img)
        elif self.model == "ESPCN":
            HR_Image = self.upscaleESPCNpb(img)
        elif self.model == "FSRCNN":
            HR_Image = self.upscaleFSRCNNpb(img)
        elif self.model == "LapSRN":
            HR_Image = self.upscaleLapSRNpb(img)
        elif self.model == "interpolator":
            self._log("INFO", "Upscale image with interpolator to %dx" % (self.scale))
            HR_Image = cv2.resize(
                img, None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_CUBIC
            )
        else:
            self._log(
                "ERROR",
                "Invalid upscale model defined to upscale image '%s'" % (self.model),
            )

        return HR_Image

    ##
    #   Load the model
    #
    def loadUpscaleModel(self):
        if self.model == "EDSR":
            self.loadEDSRpb(self.scale)
        elif self.model == "ESPCN":
            self.loadESPCNpb(self.scale)
        elif self.model == "FSRCNN":
            self.loadFSRCNNpb(self.scale, False)
        elif self.model == "LapSRN":
            self.loadLapSRNpb(self.scale)
        elif self.model == "interpolator":
            pass
        else:
            self._log(
                "ERROR",
                "Invalid upscale model defined to be loaded '%s'" % (self.model),
            )


if __name__ == "__main__":
    """data = {
        "__srmodels": ["EDSR", "ESPCN", "FSRCNN", "LapSRN"],
        "__srscales": [[2, 3, 4], [2, 3, 4], [2, 3, 4], [2, 4, 8]],
        "model": "LapSRN" ,
        "scale": 4,
        "pathToImg": "input.png"
    }
    model = data["model"]
    scale = data["scale"]
    pathToImg = data["pathToImg"]

    img = cv2.imread(pathToImg,3)
    start = time.time()

    HR_Image = upscaleImg(model, scale, img)
    print("TIEMPO DE INFERENCIA: ", time.time()-start)

    cv2.imshow('Original image', img)
    cv2.imshow('Upscaled image', HR_Image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
