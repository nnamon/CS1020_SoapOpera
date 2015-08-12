#! /usr/bin/python

# How many days problem.
# Given two inputs of the form ddmmmyy, find the number of days between the two
# dates.

# Proposed solution:
# There are three units we have to deal with:
# Days (dd), Months (mm), Years (yy)
#
# When finding the difference between days, its simply a matter of finding the
# difference between the two numbers. This is assuming the month and year values
# are the same.
#
# However, months have differing values and the year affects whether Februrary
# has 28 days or 29 days. So finding an algebraic solution might be complex.
#
# I propose an incremental approach that iteratively calculates the number of
# day by walking in steps of months from the first date given. For each month,
# we may determine the number of days by checking the index of the month in the
# year and by checking if the year is a leap year. Once the month and year
# matches the second date given, we may subtract the start and end date offsets
# from our days total to obtain the total number of days.
#
# Sub Problems (Problem Specific):
# 1. Determining number of days in a month.
# 2. Determining if the year is a leap year.
# 3. Removing the start and end offsets from our total days in a month.
#
# Sub Problems (Implementation Specific):
# 1. Receiving the two values as inputs.
# 2. Validating the two values as inputs.
# 3. Parsing the two values as inputs.
# 4. Keeping state of the incremental computation.
# 5. Presenting the results of the computation.
#
# Please refer to the below code and commentary for the breakdown of my
# solution.
#
# Enjoy, amon

import argparse


class DateFormat:
    # We use a class to represent our date format to group parsing related
    # functionality.

    def __init__(self, v):
        # Implementation Sub Problem 2
        # We use a custom argument type to parse the user defined string.
        # The conditions our string must satisfy are:
        # 1. Of length 6:
        if len(v) != 6:
            raise argparse.ArgumentTypeError("Must be of length 6")
        # 2. Must be numerical
        elif not v.isdigit():
            raise argparse.ArgumentTypeError("All characters must be numerical")

        # Implementation Sub Problem 3
        # Now that the format has matched, we want to ensure that the input
        # makes semantic sense while parsing (i.e. the date actually exists).
        # For example, there is no such date as the 32nd of December 1992.

        # Parsing the year: Given only two numbers to represent the year, this
        # can be tricky as 15 can be understood as 2015 while 93 can be
        # understood as 1993. We will take the following interpretation:
        # 70-99 as 1970-1999 (1970 is the start of unix epoch time)
        # 00-69 as 2000-2069

        yeardigits = int(v[4:])
        if yeardigits < 70:
            self.year = 2000 + yeardigits
        else:
            self.year = 1900 + yeardigits

        # Parsing the month: This value can only be between 1-12.
        monthdigits = int(v[2:4])
        if not 1 <= monthdigits <= 12:
            raise argparse.ArgumentTypeError("Months must be between 1-12")
        else:
            self.month = monthdigits

        # Parsing the day: This value takes into account whether the day exists
        # given the number of days in the month and whether the year is a leap
        # year (in the case of Februrary).

        daydigits = int(v[:2])
        if daydigits > DateFormat.days_in_month(self.month, self.year):
            raise argparse.ArgumentTypeError("That date does not exist!")
        self.day = daydigits

    @staticmethod
    def days_in_month(month, year):
        # Problem Specific Sub Problem 1
        # If the month is February, check if the year is a leap year. If the
        # year is a leap year, February has 29 days, else it has 28 days.
        if month == 2:
            if DateFormat.is_leap_year(year):
                return 29
            else:
                return 28
        else:
            # If the month isn't February, we may get the number of days in
            # the month by looking up the following table:
            day_months = [31, -1, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            return day_months[month-1]

    @staticmethod
    def is_leap_year(year):
        # Problem Specific Sub Problem 2
        # We may determine if the year is a leap year from the following code:
        # Pseudocode from https://en.wikipedia.org/wiki/Leap_year
        if not year % 4 == 0:
            return False
        elif not year % 100 == 0:
            return True
        elif not year % 400 == 0:
            return False
        else:
            return True

    def __repr__(self):
        # Pretty printing
        return "%02d-%02d-%d" % (self.day, self.month, self.year)

    def is_larger(self, other):
        if self.year > other.year:
            return True
        elif self.month > other.month:
            return True
        elif self.day > other.day:
            return True
        else:
            return False


def calculate_days(dateone, datetwo):
    # Given two DateFormats, calculate the number of dates between the two.

    # Implementation Sub Problem 4
    # First, we determine which is the starting date to increment.
    # We do this by comparing the two dates and setting the starting date to the
    # smaller date.

    if dateone.is_larger(datetwo):
        start = datetwo
        end = dateone
    else:
        start = dateone
        end = datetwo

    # We keep state of the total number of days so far
    total_days = 0
    current_month = start.month
    current_year = start.year
    while True:
        # At each step, we will find the number of days in the current month,
        # then add it to the total number of days.
        total_days += DateFormat.days_in_month(current_month, current_year)
        if current_month == end.month and current_year == end.year:
            break
        else:
            # Increment the month, (and the year if we overflow the months)
            current_month += 1
            if current_month == 13:
                current_month = 1
                current_year += 1

    # Once the month and year targets have been met, we settle the start
    # and end date offsets
    start_offset = start.day
    end_offset = DateFormat.days_in_month(end.month, end.year) - end.day
    total_days = total_days - (start_offset + end_offset)
    return total_days


def main():
    # Implementation Sub Problem 1
    # Our solution is to use an argument parser to receive the two dates as a
    # string.
    parser = argparse.ArgumentParser(description="Find the number of days "
                                     "between two dates. The two dates must be "
                                     "in the form ddmmyy. The number of days "
                                     "does not include the end date.")
    parser.add_argument("date_one", type=DateFormat, help="Date One")
    parser.add_argument("date_two", type=DateFormat, help="Date Two")

    args = parser.parse_args()

    # Given our arguments, we pass it to calculate_days() to do all our work.
    days_between = calculate_days(args.date_one, args.date_two)

    # Implementation Sub Problem 5
    # We do a simple print :)
    print("Number of days between %s and %s: %d" % (args.date_one,
                                                    args.date_two,
                                                    days_between))

if __name__ == "__main__":
    main()
