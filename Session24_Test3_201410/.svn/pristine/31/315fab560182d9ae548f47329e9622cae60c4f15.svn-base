'''
Created on Oct 8, 2013

@authors: David Mutchler and Claude Anderson
'''

# This class definition was developed as part of the live
# coding exercise during the Session 16 class meeting.
# You should not need to change this code, and doing so
# might cause some of the provided tests to fail.

import math
import zellegraphics as zg

class Point(object):
    '''
    Represents a point in 2-dimensions (no graphics) with
    very simple properties and functionality
    '''

    def __init__(self, x, y):
        '''
        Constructor
        '''
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point(" + str(self.x) + "," + str(self.y) + ")"

    def move_by(self, dx, dy):
        """
        Move this point by the given amounts in the given directions
        """
        self.x += dx
        self.y += dy

    def distance_from(self, otherPoint):
        """
        Computees and returns the distance froim this point to another point
        """
        dx = self.x - otherPoint.x
        dy = self.y - otherPoint.y
        return math.sqrt(dx * dx + dy * dy)

    def farthest_point(self, point_list):
        """
        Returns the Point from non-empty point_list
        that is closest to this one
        """
        # We can have students write this one.  It will somewhat
        # reinforce things we have just done, but also be good test practice.
        farthest_so_far = point_list[0]
        for k in range (1, len(point_list)):
            if self.distance_from(point_list[k]) > self.distance_from(farthest_so_far):
                farthest_so_far = point_list[k]
        return farthest_so_far

    def zelle_point(self):
        return zg.Point(self.x, self.y)

if __name__ == '__main__':
    # some unit tests for the Point class.
    p1 = Point(1, 2)
    p2 = Point(-2, 6)
    print(p1, p2)
    print("Distance between points {} and {} is {}".format(p1, p2, p1.distanceFrom(p2)))
    p2.move_by(-2, 8)
    print("Distance between points {} and {} is  now {}".format(p1, p2, p1.distanceFrom(p2)))

