"""
Exam 3, problem 1.

Authors: David Mutchler, Claude Anderson, their colleagues
         and Jack Porter.  October 2013.
"""
# TODO: 1. PUT YOUR NAME IN THE ABOVE LINE.
# COMMIT this problem as soon as you finish it.

import tkinter
from tkinter import ttk

""" A button initially displays 0.
    Clicking it makes its text be 1,
    clicking again makes it 2, etc.
"""


def main():
    root = tkinter.Tk()

    main_frame = ttk.Frame(root, padding=(30, 10), relief='raised')
    main_frame.grid()

    counter_button = ttk.Button(main_frame)
    counter_button['text'] = '0'
    counter_button.grid()
    counter_button['command'] = lambda: countUp(counter_button)

    # TODO: 2. Add code below that makes it so that when the user clicks
    # the button, the number that the button displays is increased by 1.
    # You will most likely need to define an additional function
    # in order to do this.
    #
    # For possible partial credit: If you CANNOT make the button behave
    # as described above, make it do ANYTHING that you think shows
    # what you know about buttons.

    root.mainloop()

def countUp(button):
    change = int(button['text']) + 1
    button['text'] = str(change)

if __name__ == '__main__':
    main()