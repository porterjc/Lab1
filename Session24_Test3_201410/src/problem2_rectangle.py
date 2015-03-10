"""
Exam 3, problem 2.

Authors: David Mutchler, Claude Anderson, their colleagues
         and Jack Porter.  October 2013.
"""
# TODO: 1. PUT YOUR NAME IN THE ABOVE LINE.
# COMMIT this problem EVERY time you finish a PART of it.

import problem2_provided_point
from problem2_provided_point import Point
import zellegraphics as zg
import random

#-----------------------------------------------------------------------
# STUDENTS:  Read the   problem2.pdf   file attached.
#-----------------------------------------------------------------------


class Rectangle(object):
    """
    Represents a rectangle in two dimensions.  For simplicity, we
    also allow "degenerate" rectangles which consist of a single point
    or a horizontal or vertical line, due to the two points passed to the
    constructor having the same x- and/or y-coordinate.
    """
    # MAJOR HINT:  Python's built-in max() and min() functions will be
    #    VERY helpful because they:
    #    1. Suggest ways for you to think about solutions to this
    #       problem more clearly.
    #    2. Greatly reduce the need for  if  statements in a solution.
    #         (Our solution, using max and min in many places,
    #         contains only three  ifs  in our entire solution.
    #          Your mileage may vary.)
    # REMINDER: The call  max(3, 5)  returns 5.  min(3, 5)  returns 3.

    def __init__(self, p1, p2):
        """
        Initialize this rectangle, given that the arguments are Point
        objects that are opposite corners of the rectangle.

        Preconditions:
          -- The arguments are Point objects (per the Point class
             definition in the   problem2_provided_point  file).
          -- The coordinates of both points are integers.
        """

        self.p1 = p1
        self.p2 = p2
        self.maxX = max(p1.x, p2.x)
        self.maxY = max(p1.y, p2.y)
        self.minX = min(p1.x, p2.x)
        self.minY = min(p1.y, p2.y)

        # TODO: 2.  Decide what to store as instance variables (fields).
        # Then write this constructor.  While you certainly can use the
        # values of p1 and p2 as the fields, other values (that you can
        # calculate from p1 and p2) may make the various  methods easier
        # to write.
        #  ** One possible way to do it:
        #  ** store the minimum and maximum x and y values as the fields.

    def get_min_y(self):
        """
        Returns the minimum y-value among all points in this Rectangle.
        For example, if the opposite corners are (100, 20) and (80, 31),
        then this function should return 20.
        """
        # TODO: 3.  Implement and test this method and the three other
        # similarly-named methods, testing as follows:
        #
        #   ** RUN the    problem2_provided_rectangle_test.py   progam
        #   ** to test this method and ALL of the other methods that
        #   ** you must write.  RUN THAT PROGRAM OFTEN -- EVERY time
        #   ** that you implement another method or function!
        return self.minY  # REPLACE this STUB by code that works correctly.

    def get_max_y(self):
        """
        Returns the maximum y-value among all points in this Rectangle.
        For example, if the opposite corners are (100, 20) and (80, 31),
        then this function should return 31.
        """
        # TODO: 3 (continued).  Implement and test this method and the
        #    three other similarly-named methods, per the comment in
        #    the   get_min_y   method above.
        return self.maxY  # REPLACE this STUB by code that works correctly.

    def get_min_x(self):
        """
        Returns the minimum x-value among all points in this Rectangle.
        For example, if the opposite corners are (100, 20) and (80, 31),
        then this function should return 80.
        """
        # TODO: 3 (continued).  Implement and test this method and the
        #    three other similarly-named methods, per the comment in
        #    the   get_min_y   method above.
        #
        # Replace the following STUB by code that works correctly.
        # There should NOT be any randomness in your answer -- the
        # randomness is here only to make the testing more helpful.
        # return random.randrange(99999)
        return self.minX

    def get_max_x(self):
        """
        Returns the maximum x-value among all points in this Rectangle.
        For example, if the opposite corners are (100, 20) and (80, 31),
        then this function should return 100.
        """
        # TODO: 3 (continued).  Implement and test this method and the
        #    three other similarly-named methods, per the comment in
        #    the   get_min_y   method above.
        return self.maxX  # REPLACE this STUB by code that works correctly.

    def __repr__(self):
        # Nothing for you to do here.  This method will be called when
        # the test code needs to print a rectangle. Also, you may want
        # to print a rectangle object yourself at some point for
        # debugging purposes.
        return "Rect([" + str(self.get_min_x()) + "," + str(self.get_min_y()) + \
                  "],[" + str(self.get_max_x()) + "," + str(self.get_max_y()) + "])"

    def get_area(self):
        """ Returns the area of this rectangle (width times height)  """
        # TODO: 4.  Implement and test this method.
        # HINT:  Calling the methods from "TODO #3" may be helpful.
        return (self.get_max_x() - self.get_min_x()) * (self.get_max_y() - self.get_min_y())

    def contains_point(self, p):
        """
        Returns a boolean value (True or False) that indicates whether
        or not this rectangle contains the given Point p.  (If p is on
        a boundary or corner of the rectangle, we'll say that the
        rectangle "contains" p, so return True in that case.)
        PRECONDITION:  The argument p is a Point whose coordinates are
        integers (so there is no need to worry about roundoff errors).
        """
        # TODO: 5.  Implement and test this method.
        # HINT:  Calling the methods from "TODO #3" makes the solution
        #        to this problem MUCH simpler than some other approaches.
        # ** READ THE ABOVE HINT - IT REALLY IS HELPFUL! **
        if p.y <= self.get_max_y() and p.y >= self.get_min_y() and p.x <= self.get_max_x() and p.x >= self.get_min_x():
            return True
        else:
            return False


    def intersects(self, other_rect):
        """
        Returns a boolean value (True or False) indicating whether or
        not this rectangle and other_rect have at least one point
        in common.
        PRECONDITION:  other_rect is also a Rectangle.
        """
        # TODO: 6. Implement and test this method.
        # HINT:  contains_point   (which you just implemented) may be
        #        VERY helpful in your implementation, because:
        #   ** If two rectangles intersect, at least one of them
        #   ** contains one of the CORNER points of the other rectangle.
        #   ** READ THE ABOVE HINT - IT REALLY IS HELPFUL! **
        # ANOTHER HINT:  In our own solution, we found it helpful to
        # write a new method to handle part of this task.
        if self.contains_point(other_rect.p1) or self.contains_point(other_rect.p2):
            return True
        else:
            return False

    def intersection(self, other_rect):
        """
        Returns a new Rectangle representing the intersection of
        this rectangle and other_rect if there is one;
        otherwise returns None.
        PRECONDITION: other_rect is also a Rectangle object.

        NOTE: It is possible that the intersection Rectangle is
        "degenerate", i.e. represents a single point (its opposite
        corner points are the same) or a line.  You do not need to check
        for or reject such rectangles.  Just return them without using
        any special tests for this situation.
        """
        # TODO: 7.  Implement and test this method.
        # HINT:  calling the   intersects   method is a way to
        #        easily determine when you should return None.
        # HINT:  max() and min() are especially helpful
        #        in the implementation of this method.
        point1 = None
        point2 = None
        Rect = None
        if self.intersects(other_rect) == True:
            if max(other_rect.p1.x, self.p1.x) == self.get_max_x():
                if other_rect.p2.y > self.get_max_y():
                    point1 = Point(other_rect.p1.x, self.get_max_y() - (other_rect.p1.y - self.get_min_y()))
                    point2 = Point(self.get_max_x(), self.get_max_y())
                    Rect = Rectangle(point1, point2)
                    return Rect
                if other_rect.p2.y < self.get_max_y():
                    point1 = Point(other_rect.p1.x, self.get_max_y() - (other_rect.p1.y - self.get_min_y()))
                    point2 = Point(self.get_max_x(), self.get_max_y())
                    Rect = Rectangle(point1, point2)
                    return Rect


           # elif self.contains_point(other_rect.p1) and other_rect.p2.x < self.get_max_x() and other_rect.p2.y < self.get_max_y():

        elif self.intersects(other_rect) == False:
            return None

    def __eq__(self, other_rect):
        """
        Returns True if and only if the two rectangles have the same
        size, shape, and location. FWIW: This method is called if the
        user uses == to compare two rectangles.
        """
        # Nothing for you to do.  We wrote this method for you.
        if not isinstance(other_rect, Rectangle):
            return False
        return self.get_max_x() == other_rect.get_max_x() and \
               other_rect.get_min_x() == other_rect.get_min_x() and \
               self.get_max_y() == other_rect.get_max_y() and \
               self.get_min_y() == other_rect.get_min_y()

    def zelle_rect(self):
        """
        Returns a zellegraphics rectangle with the same boundaries
        as this one.
        """
        # Nothing for you to do.  We wrote this method for you.
        return zg.Rectangle(zg.Point(self.get_min_x(), self.get_min_y()),
                            zg.Point(self.get_max_x(), self.get_max_y()))

#  ---------------End of the Rectangle class definition   -------------


def largest_rectangle(rects):
    """ Returns the Rectangle in  rects  that has the largest area.
        Does not modify rects.

        PRECONDITION:  rects is a nonempty sequence of Rectangles.
    """
    # NOTE:  This is a function that is NOT part of the Rectangle class
    #        definition.
    # TODO: 8. Implement and test this function.

    areas = []
    for k in range(len(rects)):
        areas.append(rects[k].get_area())
    ind = areas.index(max(areas))

    return rects[ind]

