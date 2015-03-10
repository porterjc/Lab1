"""
   Unit tests for the Rectangle class.
   Authors:  Claude Anderson and David Mutchler, October 30, 2013
"""

# You should not have to change this file.
# If you do change it for debugging purposes (such as commenting out
# some of the lines of the test() method) be sure that you uncomment
# before you do your final commit, so your program demonstrates all
# of the Rectangle methods that actually work.

from problem2_provided_point import Point
from problem2_rectangle import Rectangle
import zellegraphics as zg
import problem2_rectangle

def main():
    rt = RectangleTest()
    rt.test()

class RectangleTest(object):

    def __init__(self):
        # make some Rectangles to use for the tests
        self.r0 = Rectangle(Point(50, 25), Point(120, 25))
        self.r1 = Rectangle(Point(10, 10), Point(150, 110))
        self.r2 = Rectangle(Point(120, 20), Point(180, 70))
        self.r3 = Rectangle(Point(160, 70), Point(180, 90))
        self.r4 = Rectangle(Point(80, 120), Point(110, 90))
        self.r5 = Rectangle(Point(250, 60), Point(220, 100))
        self.r6 = Rectangle(Point(200, 110), Point(230, 90))
        self.r7 = Rectangle(Point(70, 80), Point(50, 60))
        self.r8 = Rectangle(Point(50, 80), Point(70, 100))
        # put them into a list so we can use loops to run lots of tests.
        self.rects = [self.r0, self.r1, self.r2, self.r3, self.r4, \
                      self.r5, self.r6, self.r7, self.r8]

    def test(self):
        # Test each method
        self.test_tops()  # Next 4 methods test TO DO 2 and 3
        self.test_bots()
        self.test_lefts()
        self.test_rights()
        self.test_areas()  # Test TO DO 4
        self.test_contains_point()  # Test TO DO 5
        self.test_intersects()  # Test TO DO 6
        self.test_intersection()  # Test TO DO 7
        self.test_largest()  # Test TO DO 8
 #      draw_all_rects(self.rects)  # used to produce the diagram that we provide for you.
                                    # placed in this project.

    def test_tops(self):
        print("\n--------Testing get_min_y method---------")
        tops = [25, 10, 20, 70, 90, 60, 90, 60, 80]
        calculated_tops = []
        for r in self.rects:
            calculated_tops.append(r.get_min_y())
        print("expected:  ", tops)
        print("calculated:", calculated_tops)
        print_result(tops == calculated_tops)

    def test_bots(self):
        print("\n--------Testing get_max_y method---------")
        bots = [25, 110, 70, 90, 120, 100, 110, 80, 100]
        calculated_bots = []
        for r in self.rects:
            calculated_bots.append(r.get_max_y())
        print("expected:  ", bots)
        print("calculated:", calculated_bots)
        print_result(bots == calculated_bots)

    def test_rights(self):
        print("\n--------Testing get_max_x method---------")
        rights = [120, 150, 180, 180, 110, 250, 230, 70, 70]
        calculated_rights = []
        for r in self.rects:
            calculated_rights.append(r.get_max_x())
        print("expected:  ", rights)
        print("calculated:", calculated_rights)
        print_result(rights == calculated_rights)

    def test_lefts(self):
        print("\n--------Testing get_min_x method---------")
        lefts = [50, 10, 120, 160, 80, 220, 200, 50, 50]
        calculated_lefts = []
        for r in self.rects:
            calculated_lefts.append(r.get_min_x())
        print("expected:  ", lefts)
        print("calculated:", calculated_lefts)
        print_result(lefts == calculated_lefts)

    def test_areas(self):
        print("\n--------Testing get_area method---------")
        areas = [0, 14000, 3000, 400, 900, 1200, 600, 400, 400]
        calculated_areas = []
        for r in self.rects:
            calculated_areas.append(r.get_area())
        print("expected:  ", areas)
        print("calculated:", calculated_areas)
        print_result(areas == calculated_areas)

    def test_contains_point(self):
        print("\n--------Testing contains_point method---------")
        points_list = [Point(0, 0),  # above and left of r0
                       Point(100, 200),  # below r1
                       Point(150, 50),  # inside r2
                       Point(200, 80),  # right of r3
                       Point(70, 120),  # left of r4
                       Point(230, 60),  # on top boundary of r5
                       Point(230, 100),  # right boundary of r6
                       Point(70, 80),  # corner of r7
                       Point(50, 100)]  # corner of r8
        contains = [False, False, True, False, False, True, True, True, True]
        calculated_contains = []
        for k in range(len(points_list)):
            calculated_contains.append(self.rects[k].contains_point(points_list[k]))
        print("expected:  ", contains)
        print("calculated:", calculated_contains)
        print_result(contains == calculated_contains)

    def test_intersects(self):
        print("\n--------Testing intersects method---------")
        r0 = self.r0
        r1 = self.r1
        r2 = self.r2
        r4 = self.r4
        r5 = self.r5
        r7 = self.r7
        r8 = self.r8
        # Test intersections of many pairs of rectangles.
        pairs = [(r1, r7), (r5, r4), (r4, r5), (r1, r2), (r2, r1), (r1, r4),
                 (r4, r1), (r7, r8), (r8, r7), (r0, r2), (r2, r0)]
        results = [True, False, False, True, True, True, True,
                   True, True, True, True]
        calculated_intersects = []
        for k in range(len(pairs)):
            calculated_intersects.append(
                 pairs[k][0].intersects(pairs[k][1]))
        print("expected:  ", results)
        print("calculated:", calculated_intersects)
        print_result(results == calculated_intersects)

    def test_intersection(self):
        print("\n--------Testing intersection method---------")
        r0 = self.r0
        r1 = self.r1
        r2 = self.r2
        r4 = self.r4
        r5 = self.r5
        r6 = self.r6
        r7 = self.r7
        r8 = self.r8

        pairs = [(r1, r7), (r5, r4), (r4, r5), (r1, r2),
                 (r2, r1), (r1, r4),
                 (r4, r1), (r7, r8),
                 (r8, r7), (r0, r2),
                 (r2, r0), (r4, r6)]
        results = [Rectangle(Point(50, 60), Point(70, 80)),  # (r1, r7)
                   None,  # (r5, r4)
                   None,  # (r4, r5)
                   Rectangle(Point(120, 20), Point(150, 70)),  # (r1, r2)
                   Rectangle(Point(120, 20), Point(150, 70)),  # (r2, r1)
                   Rectangle(Point(80, 90), Point(110, 110)),  # (r1, r4)
                   Rectangle(Point(80, 90), Point(110, 110)),  # (r4, r1)
                   Rectangle(Point(50, 80), Point(70, 80)),  # (r7, r8)
                   Rectangle(Point(50, 80), Point(70, 80)),  # (r8, r7)
                   Rectangle(Point(120, 25), Point(120, 25)),  # (r0, r2)
                   Rectangle(Point(120, 25), Point(120, 25)),  # (r2, r0)
                   None  # (r4, r6)
                  ]
        calculated_intersections = []
        for k in range(len(pairs)):
            calculated_intersections.append(
                 pairs[k][0].intersection(pairs[k][1]))
        print("expected:  ", results)
        print("calculated:", calculated_intersections)
        print_result(calculated_intersections == results)

    def test_largest(self):
        print("\n--------Testing largest_rectangle method---------")
        rect_sets = (self.rects, self.rects[2:], self.rects[4:],
                     self.rects[0:2], self.rects[0:len(self.rects):2])
        expected = [self.r1, self.r2, self.r5, self.r1, self.r2]
        results = []
        for rect_set in rect_sets:
            results.append(problem2_rectangle.largest_rectangle(rect_set))
        print("expected:  ", expected)
        print("calculated:", results)
        print_result(expected == results)

def print_result(result):
    """ Called by each test method to indicate whether all tests passed """
    if result:
        print('passed')
    else:
        print('FAILED')


""" The next two functions are here for two reasons:
    1.  To produce the diagram that we provided for you,
        so that you can see the sizes and intersections of the rectangles.
    2.  TO allow you to draw two rectangles and the intersection that you calculate,
        in case that visualization helps you with debugging.
"""
def draw_rect_in_window(rect, window, fill=None,
                        text_color='black', name=None):
    zr = rect.zelle_rect()
    zr.setFill(fill)
    top_left = zr.getP1()
    zr.draw(window)
    if name != None:
        text_point = zg.Point(top_left.x + 10, top_left.y + 10)
        text = zg.Text(text_point, name)
        text.setFill(text_color)
        text.draw(window)

def draw_all_rects(rects):
    win = zg.GraphWin("All Rectangles", 260, 180)
    rect_number = 0
    for rect in rects:
        draw_rect_in_window(rect, win, name="r" + str(rect_number))
        rect_number += 1
    win.getMouseWithMessage("click to close", close_it=True)

if __name__ == '__main__':
    main()
