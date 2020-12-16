"""Create an on-call schedule."""

from datetime import date
from collections import (namedtuple,
                         defaultdict)
from itertools import cycle
import csv
import pyinputplus as pyip
from dateutil.relativedelta import relativedelta
from dateutil.rrule import (MO,
                            SU)


def import_dct_of_teams_employees():
    """
    Import employees from a csv and make a dictionaries by teams. The csv's
    headers should be structured like this:
    employee,team.
    The resulting dictionary should be structured as follows.
    key: team
    values: list of employee email addresses
    """

    dct = defaultdict(list)

    with open("employees.csv") as csv_file:
        f_csv = csv.reader(csv_file)
        headings = next(f_csv)
        assembled_tuple = namedtuple('assembled_tuple', headings)
        for detail in f_csv:
            row = assembled_tuple(*detail)
            dct[int(row.team)].append(row.employee)

    return dct


def assemble_schedule():
    """Call all functions required to build an on-call schedule."""

    def prompt_user_for_start_date():
        """
        Prompt user for a start date. Check to make sure the start date is in
        the future.
        """

        today = date.today()
        start = pyip.inputDate("\nPlease enter a start date (YYYY-MM-DD).\n> ",
                               formats=["%Y-%m-%d"])
        while True:
            if today > start:
                start = pyip.inputDate("\nPlease enter a date in the future."
                                       "\n> ", formats=["%Y-%m-%d"])
            else:
                break
        return start


    def build_list_of_shifts(start):
        """
        Starting with the Monday following the start date specified by the user,
        build a list of twelve on-call shifts that run Monday to Sunday.
        """

        i = 1
        lst = []
        for monday in range(12):
            monday = start + relativedelta(weekday=MO(+i))
            sunday = start + relativedelta(weekday=SU(+i + 1))
            lst.append(str(monday) + " - " + str(sunday))
            i += 1
        return lst


    def get_team_rosters(dct):
        """Make lists of each team's rosters."""

        lst = []
        for email in dct.values():
            lst.append(email)
        return lst


    def build_list_of_schedules(lst2, lst3):
        """Loop through the list of rosters and populate a list of schedules."""

        i = 0
        lst1 = []
        for i in range(len(lst2)):
            dct = {}
            for shift, email in zip(lst3, cycle(lst2[i])):
                dct[str(shift)] = email
            lst1.append(dct)
            i += 1
        return lst1


    def group_schedules_by_shift(lst):
        """
        Using defaultdict, create a dictionary, structured in the following way:
        keys: shifts
        values: list of assignees
        """

        dct1 = defaultdict(list)
        for dct2 in lst:
            for mon, assignments in dct2.items():
                dct1[mon].append(assignments)
        return dct1


    def output_schedule(dct):
        """Output the schedule to the screen."""

        roster_nums = list(employees.keys())
        headers = ["shift"]
        for num in roster_nums:
            header = "assignee_" + str(num)
            headers.append(header)
        print("\nfinalized schedule")
        print("shift", *headers, sep=",")
        for shift, assignments in dct.items():
            print(shift, *assignments, sep=", ")

        return headers


    def write_schedule_to_csv(file_name, lst):
        """Write dictionary to csv."""

        with open(file_name, "w") as out_file:
            out_csv = csv.writer(out_file)
            out_csv.writerow(lst)
            for shift, assignees in finalized_schedule.items():
                keys_values = ((shift, *assignees))
                out_csv.writerow(keys_values)

        print(f'\n"{file_name}" exported successfully\n')


    employees = import_dct_of_teams_employees()
    rosters = get_team_rosters(employees)
    while True:
        if not employees:
            print("please add some employees before creating a schedule")
            break
        start_date = prompt_user_for_start_date()
        shifts = build_list_of_shifts(start_date)
        schedules = build_list_of_schedules(rosters, shifts)
        finalized_schedule = group_schedules_by_shift(schedules)
        headers = output_schedule(finalized_schedule)
        write_schedule_to_csv("schedule.csv", headers)
        break


assemble_schedule()
