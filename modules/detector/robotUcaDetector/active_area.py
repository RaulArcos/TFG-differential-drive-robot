from enum import Enum


class Region(Enum):
    ## Region of image down
    DOWN = 0
    ## Region of image top
    TOP = 1
    ## Region of image right
    RIGHT = 2
    ## Region of image left
    LEFT = 3

    @staticmethod
    def new(name: str):
        return Region[name.upper()]

    def __str__(self) -> str:
        return self.name.lower()


class ActiveArea:
    def __init__(self) -> None:
        ## Region of images to precess
        self._region: Region = Region.TOP
        ## Portion of image to process
        self._portion: float = 1.0

    def set_region(self, region: Region):
        self._region = region

    def set_portion(self, portion: float):
        self._portion = portion

    ##
    #  Check if a cell is in active area, given the cell limits
    #
    #  @param x1      x value of top-left cell point
    #  @param x2      x value of bottom-right cell point
    #  @param y1      y value of top-left cell point
    #  @param y2      y value of bottom-right cell point
    #  @param width   image width
    #  @param height   image height
    #
    #  @return True if part of cell belongs to active area
    #
    def check_active_cell(self, x1, x2, y1, y2, width, height):
        if self._region == Region.TOP:
            s_y2 = self._portion * height
            if y1 < s_y2:
                return True
        elif self._region == Region.DOWN:
            s_y1 = (1 - self._portion) * height
            if y2 > s_y1:
                return True
        elif self._region == Region.RIGHT:
            s_x1 = (1 - self._portion) * width
            if x2 > s_x1:
                return True
        elif self._region == Region.LEFT:
            s_x2 = self._portion * width
            if x1 < s_x2:
                return True

        return False
