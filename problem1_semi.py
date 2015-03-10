""" Final exam, problem 1.

Semi-trailer (or tractor-trailer or truck-trailer) is a common name for
the combination vehicle that is shown in the
   problem1_image_of_semi.jpg   file in this project.

Here (below) are some definitions associated with semi-trailers.
  ** ASK YOUR INSTRUCTOR FOR HELP
     IF YOU DO NOT UNDERSTAND THE FOLLOWING DEFINITIONS.
  **

The TARE WEIGHT of a semi-trailer is its weight when it is not carrying
any cargo, i.e., the combined weight of the truck, trailer, driver, etc.
Of course that weight can vary based on the weight of the driver, the
amount of fuel in the tank, etc.  But for this problem, we will assume
that tare weight is a constant, for any given semi-trailer.
For example, one semi-trailer might have tare weight of 36,000 pounds
and another semi-trailer might have a tare weight of 31,000 pounds.

All units in this problem are pounds.

The CARGO WEIGHT is the weight of the goods that are currently
in the semi-trailer.  For example, a semi-trailer might have 10,000
pounds of goods, so that its cargo weight is 10,000.  Later, it might
have another 3,500 pounds of goods loaded, in which case its cargo
weight is then 13,500.  If still later 2,200 pounds of goods are
UN-loaded, its cargo weight would then be 11,300.

The GROSS WEIGHT is the tare weight plus the cargo weight. That is, it
is the combined weight of the truck, empty trailer, driver and cargo.

In the U.S., the MAXIMUM LEGAL GROSS WEIGHT is 80,000 pounds.

  ** ASK YOUR INSTRUCTOR FOR HELP  ** NOW **  IF YOU ARE NOT SURE
     WHAT WE MEAN BY THE PHRASES:
       -- semi-trailer
       -- tare weight
       -- cargo weight
       -- gross weight
       -- maximum legal gross weight.

YOUR TASKS:

OVERVIEW: You must write a Semi class that simulates weight conditions
of a semi-trailer. You will first write the headers for the class and
all of its methods. Then you will fill in the details of the methods
(including the constructor) one-by-one.
FOLLOW THE ORDER OF THE TASKS at the bottom of this file.

The Semi class's constructor requires an argument that represents
the tare weight (an integer), and a second argument (also an integer)
that represents the initial cargo weight of this Semi.

After you write your constructor, you are to write and test the following
methods in the Semi class.  For each method, it must conform to both
the description here and the test code in the    problem1_test_semi.py
file.  (So spell your method names carefully, just as written!)
All arguments are to be ints unless we specified otherwise.
After you write each method, RUN OUR TEST CODE to verify that it works.

1. get_gross_weight.  Returns the current gross weight of this Semi.

2. get_remaining_capacity.  Returns the amount of additional cargo
     weight that can be added to this Semi without exceeding the legal
     limit on gross weight.

3. is_legal.  Returns True or False based on:
     Is the current gross weight of this Semi less than or equal to
     the legal limit?  (If so, return True, else return False.)

4. load.  Given a weight of new cargo, increases this Semi's current
     cargo weight by the given weight. (Thus, this method simulates
     loading the new cargo into this Semi.)  For example, if the
     current cargo weight of this Semi is 12,000 and the given weight
     is 2,700, then this method should change this Semi's current
     cargo weight to 14,700.

5. unload.  Given a weight of some of the existing cargo,
     reduces this Semi's current cargo weight by the given weight.
     (Thus, this method simulates UN-loading some of the existing cargo
     from this Semi.)  For example, if the current cargo weight of this
     Semi is 12,000 and the given weight is 2,700, then this method
     should change this Semi's current cargo weight to 9,300.
     BUT:
       -- If the current cargo weight of this Semi is less than the
          given weight (i.e., is less than the weight of the cargo
          to be unloaded), sets the new current cargo weight to ZERO.
          (For example, if the current cargo weight of this Semi is
          8,000 and the given weight is 8,500, then this method should
          set this Semi's current cargo weight to 0, not -500.)

6. transfer.  This method has 3 parameters (in the following order):
       -- Another Semi
       -- A weight of cargo to be transfered
       -- A Boolean value (True or False).
     If the given Boolean value is True, this method simulates transfering
     cargo of the given weight FROM this Semi TO the other Semi.
     If the given Boolean value is False, this method simulates transfering
     cargo of the given weight from the OTHER Semi to THIS Semi.

       So for example, if this Semi has current cargo weight 5,000
       and the given Semi has current cargo weight 12,700, and if the
       given weight of cargo to be transfered is 600, then:
         -- If the given Boolean value is True, this method results in
              this Semi having 4,400 as its current cargo weight and
              the other Semi having 13,300 as its current cargo weight.
         -- If the given Boolean value is False, this method results in
              this Semi having 5,600 as its current cargo weight and
              the other Semi having 12,100 as its current cargo weight.

     BUT: If the attempt to do this transfer would result in a negative
            cargo weight in one of the involved Semis, the transfer does
            NOT happen.

       So for example: if this Semi has current cargo weight 5,000
       and the given Semi has current cargo weight 12,700, and if the
       given weight of cargo to be transfered is 9,000, then:
         -- If the given Boolean value is True, this method does NOT
              change the current cargo weight of EITHER Semi
              (since doing so would make this Semi have a negative
              cargo weight).
         -- If the given Boolean value is False, this method results in
              this Semi having 14,000 as its current cargo weight and
              the other Semi having 3,700 as its current cargo weight.

7. largest_capacity.  This method has one parameter:
       -- Another Semi.
     This method returns the Semi (either this one or the given one)
     whose remaining capacity (as in method #2 above) is larger.
     If there is a tie, you may return either Semi (your choice).

Authors: David Mutchler, Claude Anderson, their colleagues
         and Jack Porter.  November 2013.
"""
# TODO: 1. PUT YOUR NAME IN THE ABOVE LINE.
#          COMMIT each problem as soon as you finish it
#          (or even more often).

# TODO: 2. At the BOTTOM of this file,
#          write the Semi class's header line, then write the header
#          lines for the constructor and the seven required methods
#          (plus   pass   statements where needed), so that:
#             When you run the   problem1_test_semi.py   module,
#               there is no "red ink" in the console (although you will fail
#               all the tests at this point, of course).
#
#       ** YOU SHOULD BE ABLE TO GET THE ABOVE TO WORK BY YOURSELF.
#          BUT IF YOU REALLY CANNOT, ASK YOUR INSTRUCTOR FOR GUIDANCE.

# TODO: 3. Write the details of the Semi class's constructor, per the
#            description above.  Test using   problem1_test_semi.py.
# TODO: 4. Implement and test the   get_gross_weight         method.
# TODO: 5. Implement and test the   get_remaining_capacity   method.
# TODO: 6. Implement and test the   is_legal   method.
# TODO: 7. Implement and test the   load       method.
# TODO: 8. Implement and test the   unload     method.
# TODO: 9. Implement and test the   transfer   method.
# TODO: 10. Implement and test the  largest_capacity   method.

class Semi(object):

    def __init__(self, tare_weight, cargo):
        self.tare_weight = tare_weight
        self.cargo = cargo


    def get_gross_weight(self):
        return (self.tare_weight + self.cargo)

    def get_remaining_capacity(self):
        return MAX_LEGAL_GROSS - self.get_gross_weight()

    def is_legal(self):
        if self.get_gross_weight() < MAX_LEGAL_GROSS:
            return True
        return False

    def load(self, new_cargo):
        self.cargo += new_cargo

    def unload(self, unload_amount):
        if self.cargo <= unload_amount:
            self.cargo = 0
        self.cargo -= unload_amount

    def transfer(self, other_semi, transfer_total, sending):
        if sending:
            if self.cargo >= transfer_total:
                self.cargo -= transfer_total
                other_semi.cargo += transfer_total
        else:
            if other_semi.cargo >= transfer_total:
                self.cargo += transfer_total
                other_semi.cargo -= transfer_total

    def largest_capacity(self, other_semi):
        if self.get_remaining_capacity() > other_semi.get_remaining_capacity():
            return self
        elif self.get_remaining_capacity() < other_semi.get_remaining_capacity():
            return other_semi
        else:
            return self

MAX_LEGAL_GROSS = 80000
