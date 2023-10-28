import math


class BoxSizeFilter:
    def __init__(self) -> None:
        ## Filter detections less than value
        self._box_size_filter_lower: int = 0
        ## Filter detections greater than value
        self._box_size_filter_upper: int = 1

    @property
    def box_size_filter_lower(self):
        return self._box_size_filter_lower

    @box_size_filter_lower.setter
    def box_size_filter_lower(self, box_size_filter_lower: float):
        if not 0 <= float(box_size_filter_lower) <= 1:
            self.box_size_filter_lower = 0
        else:
            self._box_size_filter_lower = box_size_filter_lower

    @property
    def box_size_filter_upper(self):
        return self._box_size_filter_upper

    @box_size_filter_upper.setter
    def box_size_filter_upper(self, box_size_filter_upper: float):
        if not 0 <= float(box_size_filter_upper) <= 1:
            self.box_size_filter_upper = 1
        else:
            self._box_size_filter_upper = box_size_filter_upper

    def _check_properties(self):
        if float(self.box_size_filter_lower) >= float(self.box_size_filter_upper):
            self.box_size_filter_upper = 1
            self.box_size_filter = 0

    ##
    #  Filters out boxes smaller/greater than threshold
    #  @param top x coordinate top left
    #  @param left y coordinate top left
    #  @param bottom x coordinate bottom right
    #  @param right y coordinate bottom right
    #
    #  @return True if the box is between the threshold, Flase if discarded
    #
    def _get_box_area(self, left, top, right, bottom):
        norm_box_diagonal = math.sqrt((right - left) ** 2 + (bottom - top) ** 2)

        return not(norm_box_diagonal < float(
            self.box_size_filter_lower
        ) or norm_box_diagonal > float(self.box_size_filter_upper))

    def filter_boxes(self, boxes, scores, classes):
        boxes_list = boxes.tolist()
        scores_list = scores.tolist()
        classes_list = classes.tolist()
        filtered_boxes = []
        filtered_scores = []
        filtered_classes = []
        filtered_detections = 0
        for index in range(len(boxes_list)):
            if self._get_box_area(
                boxes_list[index][1],
                boxes_list[index][0],
                boxes_list[index][3],
                boxes_list[index][2],
            ):
                filtered_boxes.append(boxes_list[index])
                filtered_scores.append(scores_list[index])
                filtered_classes.append(classes_list[index])
                filtered_detections += 1

        return filtered_boxes, filtered_scores, filtered_classes, filtered_detections
