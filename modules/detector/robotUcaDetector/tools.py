import cv2
import re
import numpy as np
from math import floor
from typing import Tuple

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

##
# Tools class
#
class Tools:
    ##
    #   Gets an int value from the input whether
    #   it is an integer or the string representation of an integer
    #   @param num: integer number
    #   @return: the integer value of the input if it is an int or
    #   the string representation of an integer or None otherwise
    #
    @staticmethod
    def get_int(num):
        out = None
        if isinstance(num, (int)):
            out = num
        elif isinstance(num, (str)):
            try:
                out = int(num)
            except ValueError:
                out = None
        else:
            out = None

        return out

    ##
    #   Gets a boolean value from the input whether
    #   it is an integer, a bool or the string representation of a boolean
    #   @param truefalseval: boolean
    #   @return: the boolean value of the input if it is a boolean, an int or
    #   the string representation of an boolean or None otherwise
    #
    @staticmethod
    def get_bool(truefalseval):
        out = None
        if isinstance(truefalseval, (bool)):
            out = truefalseval
        elif isinstance(truefalseval, (int)):
            try:
                if truefalseval > 0:
                    out = True
                else:
                    out = False
            except ValueError:
                out = None
        elif isinstance(truefalseval, (str)):
            strval = truefalseval.lower()
            if strval == "true":
                out = True
            elif strval == "false":
                out = False
            else:
                out = None
        else:
            out = None

        return out

    ##
    #   Checks if the input is a non empty string
    #   @param string: input
    #   @return: true if the input is a non empty string and false otherwise
    #
    @staticmethod
    def is_str_non_empty(string):
        out = False

        if string is not None and isinstance(string, (str)) and (len(string) > 0):
            out = True

        return out

    ##
    #   Checks if the input is a list of non empty strings
    #   @param l: input
    #   @return: true if the input is a liat of non empty strings and false otherwise
    #
    @staticmethod
    def is_str_non_empty_list(l):
        out = True
        i = 0

        if l is not None and isinstance(l, (list)) and (len(l) > 0):
            while out and i < len(l):
                if not Tools.is_str_non_empty(l[i]):
                    out = False
                i += 1
        else:
            out = False

        return out

    ##
    #  Generates a bounding box string
    #  @param box bounding box to print
    #  @param width with of the image if the points should be converted from relative to absolute coordinates
    #  @param height height with of the image if the points should be converted from relative to absolute coordinates
    #
    #  return the string box(cxX cyY wW hH)
    @staticmethod
    def print_bbox_as_center_w_h(box: list, width: float = 1.0, height: float = 1.0):
        msg = "box("

        x = (box[1] + box[3]) / 2
        y = (box[0] + box[2]) / 2
        w = box[3] - box[1]
        h = box[2] - box[0]

        if width > 1.0 or height > 1.0:
            msg += "cx{} cy{} w{} h{}".format(
                int(x * width), int(y * height), int(w * width), int(h * height)
            )
        else:
            msg += "cx{:.3f} cy{:.3f} w{:.3f} h{:.3f}".format(x, y, w, h)

        msg += ")"

        return msg

    @staticmethod

    ##
    #  Gets the font scale based on image height
    #  @param height image height
    #
    #  @return font scale based on image height
    def get_font_scale(height: int):
        scale = 0.7
        min_h = 80
        max_h = 1080
        min_s = 0.30
        if height <= min_h:
            scale = min_s
        elif height >= max_h:
            scale = 1.0
        else:
            scale = (((height - min_h) * (1.0 - min_s)) / (max_h - min_h)) + min_s

        return scale

    @staticmethod
    ##
    #  Gets white or black color depending on wich will contrast more with the given color
    #  @param color input color
    #  @return withe or black color
    def get_contrast_color(color: Tuple[int, int, int]):
        ccolor = WHITE
        if (color[2] * 0.299 + color[1] * 0.587 + color[0] * 0.114) > 186:
            ccolor = BLACK

        return ccolor

    ##
    #  Adds text to an image
    #  @param image image to add text
    #  @param text text to add
    #  @param scale test scale
    #  @param thickness font thickness
    #  @param position oringin positon for the text (lower left)
    #  @param color text color
    #  @param shadow true if an dark shadow must be added to the text and false otherwise
    #
    @staticmethod
    def put_text(
        image,
        text,
        scale: float,
        thickness: int,
        position: Tuple[int, int],
        color: Tuple[int, int, int],
        shadow=False,
        font: int = cv2.FONT_HERSHEY_SIMPLEX,
        mask=None,
    ):
        if shadow:
            color2 = Tools.get_contrast_color(color)
            cv2.putText(
                image, text, position, font, scale, color2, thickness + 1, cv2.LINE_8
            )
        cv2.putText(image, text, position, font, scale, color, thickness, cv2.LINE_8)

        if mask is not None:
            if shadow:
                cv2.putText(
                    mask,
                    text,
                    position,
                    font,
                    scale,
                    (0, 0, 0),
                    thickness + 1,
                    cv2.LINE_8,
                )
            else:
                cv2.putText(
                    mask, text, position, font, scale, (0, 0, 0), thickness, cv2.LINE_8
                )

    ##
    #  Adds text to an image
    #  @param image image to add text
    #  @param text text to add
    #  @param scale test scale
    #  @param thickness font thickness
    #  @param position oringin positon for the text (lower left)
    #  @param color text color
    #  @param shadow true if an dark shadow must be added to the text and false otherwise
    #
    @staticmethod
    def put_text_scaled(
        image,
        text,
        detection_height: int,
        position: Tuple[int, int],
        color: Tuple[int, int, int],
        shadow=False,
        font: int = cv2.FONT_HERSHEY_SIMPLEX,
        mask=None,
    ):
        thickness = 1
        baseline = 0
        scale = 1.0
        image_height = image.shape[0]

        (label_width, label_height), baseline = cv2.getTextSize(
            text, font, 1.0, thickness
        )

        # proporcinal a la altura de la detección / minimo proporcional al la imagen
        scale = max(float(detection_height) / 8.0, (image_height / 40.0)) / float(
            label_height
        )
        if scale * float(label_height) > image_height * 0.05:
            scale = image_height * 0.05 / float(label_height)

        if color is None:
            color = WHITE

        if shadow:
            color2 = Tools.get_contrast_color(color)
            cv2.putText(
                image, text, position, font, scale, color2, thickness + 1, cv2.LINE_8
            )
        cv2.putText(image, text, position, font, scale, color, thickness, cv2.LINE_8)

        if mask is not None:
            if shadow:
                cv2.putText(
                    mask,
                    text,
                    position,
                    font,
                    scale,
                    (0, 0, 0),
                    thickness + 1,
                    cv2.LINE_8,
                )
            else:
                cv2.putText(
                    mask, text, position, font, scale, (0, 0, 0), thickness, cv2.LINE_8
                )

    ##
    #  Adds text to an image
    #  @param image image to add text
    #  @param text text to add
    #  @param scale test scale
    #  @param thickness font thickness
    #  @param position oringin positon for the text (lower left)
    #  @param bgColor background color
    #
    @staticmethod
    def put_text_bg(
        image,
        text,
        scale: float,
        thickness: int,
        position: Tuple[int, int],
        bg_color: Tuple[int, int, int],
        font: int = cv2.FONT_HERSHEY_SIMPLEX,
        mask=None,
    ):
        color = Tools.get_contrast_color(bg_color)

        cv2.putText(
            image, text, position, font, scale, bg_color, thickness + 2, cv2.LINE_AA
        )
        cv2.putText(image, text, position, font, scale, color, thickness, cv2.LINE_AA)

        if mask is not None:
            cv2.putText(
                mask, text, position, font, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA
            )

    ##
    #  Adds text to an image
    #  @param image image to add text
    #  @param text text to add
    #  @param scale test scale
    #  @param thickness font thickness
    #  @param position oringin positon for the text (lower left)
    #  @param fgColor foreground color
    #
    @staticmethod
    def put_text_fg(
        image,
        text,
        scale: float,
        thickness: int,
        position: Tuple[int, int],
        fg_color: Tuple[int, int, int],
        font: int = cv2.FONT_HERSHEY_SIMPLEX,
        mask=None,
    ):
        color = Tools.get_contrast_color(fg_color)

        cv2.putText(
            image, text, position, font, scale, color, thickness + 2, cv2.LINE_AA
        )
        cv2.putText(
            image, text, position, font, scale, fg_color, thickness, cv2.LINE_AA
        )

        if mask is not None:
            cv2.putText(
                mask, text, position, font, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA
            )

    ##
    # Draws a vector on the image
    # @param img image to draw on
    # @param origin_x x coordinate
    # @param origin_y y coordinate
    # @param v_x length x axis
    # @param v_y length y axis
    # @param color color of vector
    # @param thickness line thickness
    # @param scale scale of vector
    #
    @staticmethod
    def draw_vector(
        img,
        origin_x: int,
        origin_y: int,
        v_x,
        v_y,
        color: Tuple[int, int, int],
        thickness: int,
        scale: float = 1.0,
        mask=None,
    ):
        dst = (int(origin_x + (v_x * scale)), int(origin_y + (v_y * scale)))
        cv2.circle(
            img, (origin_x, origin_y), int(thickness * 1.5), color, -1, cv2.LINE_AA
        )
        cv2.arrowedLine(img, (origin_x, origin_y), dst, color, thickness, cv2.LINE_AA)
        if mask is not None:
            cv2.circle(
                mask, (origin_x, origin_y), int(thickness * 1.5), 0, -1, cv2.LINE_AA
            )
            cv2.arrowedLine(mask, (origin_x, origin_y), dst, 0, thickness, cv2.LINE_AA)

    ##
    # Draws a rectangle
    # @param img image to draw on
    # @param x1 x 1 coordinate
    # @param y1 y 1 coordinate
    # @param x2 x 2 coordinate
    # @param y2 y 2 coordinate
    # @param color color of vector
    # @param thickness line thickness
    # @param lineType Type of line
    #
    @staticmethod
    def draw_rectangle(
        img,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: Tuple[int, int, int],
        thickness: int = 1,
        line_type: int = cv2.LINE_8,
        mask=None,
    ):
        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness, line_type)
        if mask is not None:
            cv2.rectangle(mask, (x1, y1), (x2, y2), BLACK, thickness, line_type)

    ##
    # Draws a circle
    # @param img image to draw on
    # @param x1 x 1 coordinate
    # @param y1 y 1 coordinate
    # @param x2 x 2 coordinate
    # @param y2 y 2 coordinate
    # @param color color of vector
    # @param thickness line thickness
    # @param lineType Type of line
    #
    @staticmethod
    def draw_circle(
        img,
        center: Tuple[int, int],
        radius: int,
        color: Tuple[int, int, int],
        thickness: int = 1,
        mask=None,
    ):
        cv2.circle(img, center, radius=radius, color=color, thickness=thickness)
        if mask is not None:
            cv2.circle(mask, center, radius=radius, color=BLACK, thickness=thickness)

    ##
    # Draws a line
    # @param img image to draw on
    # @param x1 x 1 coordinate
    # @param y1 y 1 coordinate
    # @param x2 x 2 coordinate
    # @param y2 y 2 coordinate
    # @param color color of vector
    # @param thickness line thickness
    # @param lineType Type of line
    #
    @staticmethod
    def draw_line(
        img,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: Tuple[int, int, int],
        thickness: int = 1,
        line_type: int = cv2.LINE_8,
        mask=None,
    ):
        cv2.line(img, (x1, y1), (x2, y2), color, thickness, line_type)
        if mask is not None:
            cv2.line(mask, (x1, y1), (x2, y2), BLACK, thickness, line_type)

    ##
    #  Prints a value for debugging purposes
    #  @param name value name
    #  @param value value
    #
    @staticmethod
    def print_v(name, value):
        print(Tools.v_msg(name, value))

    ##
    #  Prints a value for debugging purposes
    #  @param name value name
    #  @param value value
    #  @return string with the name and the value
    @staticmethod
    def v_msg(name, value):
        return f"{name}: {value}"

    ##
    #  Returns a message containing the given coordinates
    #  @param latitude latitude
    #  @param longitude  longitude
    #  @return a message containing the given coordinates
    @staticmethod
    def format_coordinates(latitude: float, longitude: float):
        if latitude >= 0:
            lat = "N"
        else:
            lat = "S"
        if longitude >= 0:
            lon = "E"
        else:
            lon = "W"

        return f"{abs(latitude):.3f}{lat},{abs(longitude):.3f}{lon}"

    ##
    # Function to combine images of different sizes in horizontal tile
    # @param im_list list of images
    # @param interpolation Interpolation type
    # @return the composition of images
    #
    @staticmethod
    def hconcat_resize_min(im_list: list):
        h_min = min(im.shape[0] for im in im_list)
        im_list_resize = [
            Tools.resize(im, int(im.shape[1] * h_min / im.shape[0]), h_min)
            for im in im_list
        ]
        return cv2.hconcat(im_list_resize)

    ##
    #     Converts a bounding box from absolute (image pixels) value to relative (0-1.0)
    #  @param bbox input bounding box
    #  @param height image height
    #  @param width image width
    #
    #  @return relative bounding box (list of float)
    @staticmethod
    def bbox_absolute_to_relative(bbox: list, height: int, width: int):
        b = [0.0, 0.0, 0.0, 0.0]

        b[0] = bbox[0] / height
        b[1] = bbox[1] / width
        b[2] = bbox[2] / height
        b[3] = bbox[3] / width

        return b

    ##
    #     Converts a bounding box from absolute (image pixels) value to relative (0-1.0)
    #  @param bbox input bounding box
    #  @param height image height
    #  @param width image width
    #
    #  @return relative bounding box (list of float)
    @staticmethod
    def bbox_absolute_to_relative_np(bbox, height: int, width: int):
        b = np.zeros(4, dtype=np.float32)

        b[0] = float(bbox[0] / height)
        b[1] = float(bbox[1] / width)
        b[2] = float(bbox[2] / height)
        b[3] = float(bbox[3] / width)

        return b

    ##
    #     Converts a bounding box from relative (0-1.0) to absolute (image pixels)
    #  @param bbox input bounding box
    #  @param height image height
    #  @param width image width
    #
    #  @return absolute bounding box (list of float
    @staticmethod
    def bbox_relative_to_absolute(bbox: list, height: int, width: int):
        b = [0, 0, 0, 0]

        b[0] = int(bbox[0] * height)
        b[1] = int(bbox[1] * width)
        b[2] = int(bbox[2] * height)
        b[3] = int(bbox[3] * width)

        return b

    ##
    #     Converts a bounding box from relative (0-1.0) to absolute (image pixels)
    #  @param bbox input bounding box
    #  @param height image height
    #  @param width image width
    #
    #  @return absolute bounding box (list of float
    @staticmethod
    def bbox_relative_to_absolute_np(bbox, height: int, width: int):
        b = np.zeros(4, dtype=np.int32)
        b[0] = int(bbox[0] * height)
        b[1] = int(bbox[1] * width)
        b[2] = int(bbox[2] * height)
        b[3] = int(bbox[3] * width)
        return b

    ##
    #  Validate that an IP is valid
    #  @param ip IP address to check
    #
    #  @return True is OK, False in other case
    @staticmethod
    def is_ip_valid(ip):
        regex_ip = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        return re.search(regex_ip, ip)

    ##
    #  Resize image to given size using the most appropiate method
    #
    #  @param frame image to resize
    #  @param width target width
    #  @param height target height
    #  @param isBool image boolean flag
    #
    #  @return resized image
    #
    @staticmethod
    def resize(frame, width: int, height: int, is_bool: bool = False):
        w = frame.shape[1]
        h = frame.shape[0]

        if w == width and h == height:
            out = frame
        elif is_bool:
            out = cv2.resize(frame, (width, height), interpolation=cv2.INTER_NEAREST)
        else:
            out = cv2.resize(
                frame, (width, height), interpolation=cv2.INTER_LINEAR
            )  # seems faster thar AREAA in a lot of cases
        return out

    ##
    #  Resize image to given size using the most appropiate method
    #
    #  @param frame image to resize
    #  @param width target width
    #  @param height target height
    #  @param isBool image boolean flag
    #
    #  @return Success of the operation
    #
    @staticmethod
    def resize_copy(src, width: int, height: int, dst, is_bool: bool = False):
        w = src.shape[1]
        h = src.shape[0]
        ret = True

        if dst.shape[0] != width or dst.shape[1] != height:
            ret = False
        if w == width and h == height:
            dst[:] = src
        elif is_bool:
            cv2.resize(src, (width, height), dst, interpolation=cv2.INTER_NEAREST)
        else:
            cv2.resize(
                src, (width, height), dst, interpolation=cv2.INTER_LINEAR
            )  # seems faster thar AREAA in a lot of cases
        return ret

    ##
    #  Resize image to given scale using the most appropiate method
    #
    #  @param frame image to resize
    #  @param scale scale to resize
    #  @param isBool image boolean flag
    #
    #  @return resized image
    #
    @staticmethod
    def resize_scale(frame, scale: float, is_bool: bool = False, max_height=0):
        w = frame.shape[1]
        h = frame.shape[0]
        width, height
        scaled_height = floor(h * scale)

        if max_height > 1 and scaled_height > max_height:
            width = floor(w * max_height / h)
            height = max_height
            out = cv2.resize(
                frame, (width, height), interpolation=cv2.INTER_LINEAR
            )  # seems faster than AREA in a lot of cases
        else:
            if scale == 1.0:
                out = frame
            else:
                width = floor(w * scale)
                height = floor(h * scale)
                if is_bool:
                    out = cv2.resize(
                        frame, (width, height), interpolation=cv2.INTER_NEAREST
                    )
                else:
                    out = cv2.resize(
                        frame, (width, height), interpolation=cv2.INTER_LINEAR
                    )  # seems faster than AREA in a lot of cases

        return out

    ##
    #  Resize image to given scale using the most appropiate method
    #
    #  @param frame image to resize
    #  @param scale scale to resize
    #  @param isBool image boolean flag
    #
    #  @return Succes of the operation
    #
    @staticmethod
    def resize_scale_copy(
        frame, scale: float, dst, is_bool: bool = False, max_height=0
    ):
        w = frame.shape[1]
        h = frame.shape[0]
        width, height
        scaled_height = floor(h * scale)
        ret = True

        if dst is None:
            ret = False
        elif max_height > 1 and scaled_height > max_height:
            width = floor(w * max_height / h)
            height = max_height
            if dst.shape[1] != width or dst.shape[0] != height:
                ret = False
            else:
                cv2.resize(
                    frame, (width, height), dst, interpolation=cv2.INTER_LINEAR
                )  # seems faster than AREA in a lot of cases
        else:
            if scale == 1.0:
                if dst.shape[1] != frame.shape[1] or dst.shape[0] != frame.shape[0]:
                    ret = False
                else:
                    np.copyto(dst, frame)
            else:
                width = floor(w * scale)
                height = floor(h * scale)
                if dst.shape[1] != width or dst.shape[0] != height:
                    ret = False
                else:
                    if is_bool:
                        cv2.resize(
                            frame, (width, height), dst, interpolation=cv2.INTER_NEAREST
                        )
                    else:
                        cv2.resize(
                            frame, (width, height), dst, interpolation=cv2.INTER_LINEAR
                        )
        return ret


def equalizeHSV(image, equalizeH=False, equalizeS=False, equalizeV=True):
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(imgHSV)

    if equalizeV:
        v = cv2.equalizeHist(v)

    hsv = cv2.merge([h, s, v])
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr
