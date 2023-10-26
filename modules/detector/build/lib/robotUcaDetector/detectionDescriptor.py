from robotUcaDetector.tools import Tools

##
#   Detected target object
#
class DetectionDescriptor(object):
    ##
    #   Constructor of the class
    #
    #   @param id:          id
    #   @param label:       object class
    #   @param center:      center of the bbox
    #   @param box:         bounding box of the detection
    #   @param size:        size of the detection
    #   @param dd_dict      dictionary to reconstruct an object
    #
    def __init__(
        self,
        id,
        label=0,
        center=[0.0, 0.0],
        box=[0.0, 0.0, 0.0, 0.0],
        size=0.0,
        dd_dict=None,
    ):
        if dd_dict is None:
            ## id
            self._id = id
            ## label
            self._label = label
            ## bounding box
            self._box = [float(box[0]), float(box[1]), float(box[2]), float(box[3])]
            ## center
            self._center = center
            ## size
            self._size = size

        if dd_dict is not None:
            ## id
            self._id = dd_dict["id"]
            ## label
            self._label = dd_dict["label"]
            ## bounding box
            self._box = dd_dict["box"]
            ## center
            self._center = tuple(dd_dict["center"])
            ## size
            self._size = dd_dict["size"]

    ##
    #  Returns the string representation of the object
    #
    def __str__(self):
        return f"#{self._id}: label({self._label}, center({self._center}, box({Tools.print_bbox_as_center_w_h(self._box)} - )"

    ##
    #  Returns the representation of the object as a string
    #
    def __repr__(self):
        return f"#{self._id}: label({self._label}, center({self._center}, box({Tools.print_bbox_as_center_w_h(self._box)} - )"

    ##
    #  Gets the id of the object
    #
    def getId(self):
        return self._id

    ##
    #  Gets the label of the object
    #
    def getLabel(self):
        return self._label

    ##
    #  Sets the bounding box of the detection
    #
    #  @param box:    new bounding box
    #
    def setBBox(self, box):
        self._box = box

    ##
    #  Gets the bounding box of the object
    #
    def getBBox(self):
        return self._box

    ##
    #  Sets the center of the detection
    #
    #  @param center:    new center
    #
    def setCenter(self, center):
        self._center = center

    ##
    #  Gets the center of the object
    #
    def getCenter(self):
        return self._center

    ##
    #  Sets the size of the detection
    #
    #  @param size:    new size
    #
    def setSize(self, size):
        self._size = size

    ##
    #  Gets the size of the object
    #
    def getSize(self):
        return self._size


    ##
    #  Return serializable representation of the object
    #
    def getSerializableObject(self):
        return {
            "id": self._id,
            "label": self._label,
            "size": self._size,
            "center": list(self._center),
            "box": self._box,
        }
