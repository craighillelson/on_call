"""Create an on-call schedule."""

from datetime import date
from collections import namedtuple
from collections import defaultdict
from itertools import cycle
import csv
import pyinputplus as pyip
from dateutil.relativedelta import relativedelta
from dateutil.rrule import MO, SU


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
            start = pyip.inputDate("\nPlease enter a date in the future.\n> ",
                                   formats=["%Y-%m-%d"])
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


def import_list_of_employees():
    """
    Import employees from a csv and make a dictionaries by teams. The csv's
    headers should be structured like this:
    emloyee,team.
    The resulting dictionary should be structured as follows.
    key - team
    values - list of employee email addresses
    """

    dct = defaultdict(list)

    with open("employees.csv") as csv_file:
        f_csv = csv.reader(csv_file)
        headings = next(f_csv)
        assembled_tuple = namedtuple('assembled_tuple', headings)
        for detail in f_csv:
            row = assembled_tuple(*detail)
            dct[int(row.team)].append(row.employee)

    lst = list(dct.keys())

    return dct, lst


def get_team_rosters():
    """Make lists of each team's rosters."""

    lst = []
    for email in employees.values():
        lst.append(email)
    return lst


def build_list_of_schedules():
    """Loop through the list of rosters and populate a list of schedules."""

    i = 0
    lst = []
    for i in range(len(rosters)):
        lst.append(build_schedule(i))
        i += 1
    return lst


def build_schedule(an_int):
    """
    Looping through shifts and cycling through employees for each team roster,
    assigning each shift to one team member.
    """

    dct = {}
    for shift, email in zip(shifts, cycle(rosters[an_int])):
        dct[str(shift)] = email
    return dct


def group_schedules_by_shift():
    """
    Using defaultdict, create a dictionary, making shifts the keys lists
    of assignees the values.
    """

    dct1 = defaultdict(list)
    for dct2 in schedules:
        for mon, assignments in dct2.items():
            dct1[mon].append(assignments)
    return dct1


def output_schedule():
    """Output the schedule to the screen."""

    print("\nfinalized schedule")
    print("shift, asssignees")
    for shift, assignments in finalized_schedule.items():
        print(shift, *assignments, sep=", ")
    print("\n")


def write_schedule_to_csv(file_name):
    """Write dictionary to csv."""

    with open(file_name, "w") as out_file:
        out_csv = csv.writer(out_file)
        out_csv.writerow(["shift","assignees"])
        for mon, assignees in finalized_schedule.items():
            keys_values = (mon, *assignees)
            out_csv.writerow(keys_values)

    print(f'"{file_name}" exported successfully\n')


start_date = prompt_user_for_start_date()
shifts = build_list_of_shifts(start_date)
employees, teams = import_list_of_employees()
rosters = get_team_rosters()
schedules = build_list_of_schedules()
finalized_schedule = group_schedules_by_shift()
output_schedule()
write_schedule_to_csv("schedule.csv")
