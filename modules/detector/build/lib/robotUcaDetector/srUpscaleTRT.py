import tensorrt as trt

# import pycuda.autoinit
# import pycuda.driver as cuda
import cv2
import numpy as np


##
#   Simple helper data class that's a little nicer to use than a 2-tuple.
#
class HostDeviceMem(object):
    ##
    #   class constructor
    #   @param host_mem host memory
    #   @param device_mem device memory
    def __init__(self, host_mem, device_mem):
        ## host name
        self.host = host_mem
        ## device name
        self.device = device_mem

    ##
    #   str method
    def __str__(self):
        return "Host:\n" + str(self.host) + "\nDevice:\n" + str(self.device)

    ##
    #   representation method
    def __repr__(self):
        return self.__str__()


##
#   Class implemented to manage super resolution
#   models and operations.
#
class SRUpscaleTRT(object):
    ##
    #   Constructor of the class
    #
    def __init__(self):
        ## sr model to use
        self.engine = None
        ## srmodel name
        self.model = None
        ## scale of the model
        self.scale = None
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

            if model != "interpolator":
                ## tensorrt logger
                self.trt_logger = trt.Logger(trt.Logger.INFO)
                # load TensorRT engine
                self.loadUpscaleModel()
                ## cuda stream
                self.stream = None
                ## cuda context
                self.context = None
                # allocate resources
                try:
                    self.context = self.engine.create_execution_context()
                    self.input, self.output, self.stream = self._allocate_buffers(
                        self.engine
                    )
                except Exception as e:
                    raise RuntimeError("fail to allocate CUDA resources") from e
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
    #   Allocates all host/device in/out buffers required for an engine.
    #
    #   @param engine: trt engine
    #
    #   @return allocated resources and CUDA stream
    #
    def _allocate_buffers(self, engine):
        h_input = cuda.pagelocked_empty(
            trt.volume(engine.get_binding_shape(0)), dtype=np.float32
        )
        h_output = cuda.pagelocked_empty(
            trt.volume(engine.get_binding_shape(1)), dtype=np.float32
        )
        # Allocate device memory for inputs and outputs.
        d_input = cuda.mem_alloc(h_input.nbytes)
        d_output = cuda.mem_alloc(h_output.nbytes)
        # Create a stream in which to copy inputs/outputs and run inference.
        stream = cuda.Stream()

        return (
            HostDeviceMem(h_input, d_input),
            HostDeviceMem(h_output, d_output),
            stream,
        )

    ##
    #    Performs inference with TensorRT serialized engine
    #
    #    @param img: image to augment
    #
    #   @return the host output.
    #
    def _do_inference(self, img):
        # Set host input to the image
        self.input.host = np.ascontiguousarray(img)
        # Transfer input data to the GPU.
        cuda.memcpy_htod_async(self.input.device, self.input.host, self.stream)
        # Run inference.
        self.context.execute_async_v2(
            bindings=[int(self.input.device), int(self.output.device)],
            stream_handle=self.stream.handle,
        )
        # Transfer predictions back from the GPU.
        cuda.memcpy_dtoh_async(self.output.host, self.output.device, self.stream)
        # Synchronize the stream
        self.stream.synchronize()
        # Return the host output.
        return self.output.host

    ##
    #   Load model
    #
    #   @param path_to_engine path to model
    #
    #   @return trt engine
    #
    def load_engine(self, path_to_engine):
        with open(path_to_engine, "rb") as f, trt.Runtime(self.trt_logger) as runtime:
            return runtime.deserialize_cuda_engine(f.read())

    ##
    #   Load EDSR model
    #
    #   @param scale scale of the model
    #
    def loadEDSR(self, scale):
        # Read model
        enginePath = "./modelos/tf1/EDSR/models/EDSR_x{}.trt".format(scale)
        # Get engine
        self.engine = self.load_engine(enginePath)

    ##
    #   Load ESPCN model
    #
    #   @param scale scale of the model
    #
    def loadESPCN(self, scale):
        enginePath = "./modelos/tf1/ESPCN/export/ESPCN_x{}.trt".format(scale)
        self.engine = self.load_engine(enginePath)

    ##
    #   Load FSRCNN model
    #
    #   @param scale scale of the model
    #   @param small is the tiny model or not
    #
    def loadFSRCNN(self, scale, small):
        if small:
            enginePath = "./modelos/tf1/FSRCNN/models/FSRCNN-small_x{}.trt".format(
                scale
            )
        else:
            enginePath = "./modelos/tf1/FSRCNN/models/FSRCNN_x{}.trt".format(scale)
        # Get engine
        self.engine = self.load_engine(enginePath)

    ##
    #   Load LapSRN model
    #
    #   @param scale scale of the model
    #
    def loadLapSRN(self, scale):
        enginePath = "./modelos/tf1/LapSRN/export/LapSRN_x{}.trt".format(scale)
        self.engine = self.load_engine(enginePath)

    ##
    #   Load BSD model
    #
    #   @param scale scale of the model
    #
    def loadBSD(self, scale):
        enginePath = "./modelos/yolo/trt/super_resolution_bsd500.trt"
        self.engine = self.load_engine(enginePath)

    ##
    #   Perform the upscaling on the given image
    #
    #   @param img   img to scale
    #
    #   @return scaled image with EDSR
    #
    def upscaleEDSR(self, img):
        self._log("INFO", "Upscale image with EDSR to %dx" % (self.scale))
        meanbgr = np.asarray([103.1545782, 111.561547, 114.35629928])

        fullimg = img
        width = fullimg.shape[0]
        height = fullimg.shape[1]
        floatimg = fullimg.astype(np.float32) - meanbgr
        LR_input_ = floatimg.reshape(1, floatimg.shape[0], floatimg.shape[1], 3)

        output = self._do_inference(LR_input_)

        Y = np.asarray(output).reshape((width * self.scale, height * self.scale, 3))
        HR_image = (Y + meanbgr).clip(min=0, max=255)
        HR_image = (HR_image).astype(np.uint8)

        return HR_image

    ##
    #   Perform the upscaling on the given image
    #
    #   @param img   img to scale
    #
    #   @return scaled image with ESPCN
    #
    def upscaleESPCN(self, img):
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

        output = self._do_inference(LR_input_)

        # postprocess
        Y = np.asarray(output).reshape((width * self.scale, height * self.scale, 1))
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
    def upscaleFSRCNN(self, img):
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

        output = self._do_inference(LR_input_)

        # post-process
        Y = np.asarray(output).reshape((width * self.scale, height * self.scale, 1))
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
    def upscaleLapSRN(self, img):
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

        output = self._do_inference(LR_input_)

        Y = np.asarray(output).reshape((width * self.scale, height * self.scale, 1))
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
    #   @return scaled image with BSD
    #
    def upscaleBSD(self, img):
        self._log("INFO", "Upscale image with BSD to %dx" % (self.scale))
        fullimg = img
        width = fullimg.shape[0]
        height = fullimg.shape[1]

        self._log("WARNING", "fullimg.shape " + str(fullimg.shape))

        cropped = fullimg[
            0 : (width - (width % self.scale)), 0 : (height - (height % self.scale)), :
        ]
        floatimg = cropped.astype(np.float32) / 255.0

        # Convert to YCbCr color space
        imgYCbCr = cv2.cvtColor(floatimg, cv2.COLOR_BGR2YCrCb)
        imgY = imgYCbCr[:, :, 0]
        self._log("WARNING", "imgY.shape " + str(imgY.shape))

        LR_input_ = imgY.reshape(1, imgY.shape[0], imgY.shape[1], 1)
        self._log("WARNING", "LR_input_.shape " + str(LR_input_.shape))

        output = self._do_inference(LR_input_)
        self._log("WARNING", "output.shape " + str(output.shape))

        # Y = np.asarray(output).reshape((width*self.scale, height*self.scale, 1))
        HR_image_YCrCb = np.asarray(output).reshape((963, 1443, 3))
        """Cr = np.expand_dims(cv2.resize(imgYCbCr[:, :, 1], None, fx=self.scale, fy=self.scale,
                                       interpolation=cv2.INTER_CUBIC), axis=2)
        Cb = np.expand_dims(cv2.resize(imgYCbCr[:, :, 2], None, fx=self.scale, fy=self.scale,
                                       interpolation=cv2.INTER_CUBIC), axis=2)
        
        HR_image_YCrCb = np.concatenate((Y, Cr, Cb), axis=2)
        """
        HR_image = ((cv2.cvtColor(HR_image_YCrCb, cv2.COLOR_YCrCb2BGR)) * 255.0).clip(
            min=0, max=255
        )
        HR_image = (HR_image).astype(np.uint8)
        self._log("WARNING", "HR_image.shape " + str(HR_image.shape))

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
            HR_Image = self.upscaleEDSR(img)
        elif self.model == "ESPCN":
            HR_Image = self.upscaleESPCN(img)
        elif self.model == "FSRCNN":
            HR_Image = self.upscaleFSRCNN(img)
        elif self.model == "LapSRN":
            HR_Image = self.upscaleLapSRN(img)
        elif self.model == "interpolator":
            self._log("INFO", "Upscale image with interpolator to %dx" % (self.scale))
            HR_Image = cv2.resize(
                img, None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_CUBIC
            )
        elif self.model == "BSD":
            HR_image = self.upscaleBSD(img)
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
            self.loadEDSR(self.scale)
        elif self.model == "ESPCN":
            self.loadESPCN(self.scale)
        elif self.model == "FSRCNN":
            self.loadFSRCNN(self.scale, False)
        elif self.model == "LapSRN":
            self.loadLapSRN(self.scale)
        elif self.model == "interpolator":
            pass
        elif self.model == "BSD":
            self.loadBSD(self.scale)
        else:
            self._log(
                "ERROR",
                "Invalid upscale model defined to be loaded '%s'" % (self.model),
            )
