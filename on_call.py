"""Create an on-call schedule."""

from datetime import date
from collections import namedtuple
from collections import defaultdict
from itertools import cycle
import csv
import pyinputplus as pyip
from dateutil.relativedelta import relativedelta
from dateutil.rrule import MO


def import_list_of_employees():
    """
    Import employees from a csv and make a dictionaries by teams. The csv's
    headers should be structured like this:
    emloyee,team.
    The resulting dictionary should be structured as follows.
    key - team
    employees - list of employee email addresses
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


def make_list_of_shifts():
    """
    For the range between the user specified start and end dates, build a
    list of start dates. Loop through shifts and flag any weeks containing US
    holidays.
    """


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


def build_list_of_mondays(start):
    i = 1
    lst = []
    for monday in range(12):
        monday = start + relativedelta(weekday=MO(+i))
        lst.append(monday)
        i += 1
    return lst


def get_list_of_teams():
    # lst1 = []
    lst2 = []

    for team, employee in employees.items():
        lst1 = []
        for email in employee:
            lst1.append(email)
        lst2.append(lst1)

    return lst2


def prompt_user_for_date(user_prompt, formats=['%Y-%m-%d']):
    return pyip.inputDate(user_prompt)


def assemble_schedule():
    dct = defaultdict(list)
    for i in schedules:
        for mon, assignments in i.items():
            dct[mon].append(assignments)
    return dct


def output_schedule():
    print("\nfinalized schedule")
    for mon, assignments in finalized_schedule.items():
        print(mon, *assignments, sep=", ")
    print("\n")


def build_schedule(an_int):
    dct = {}
    for mon, email in zip(mondays, cycle(teams[an_int])):
        dct[str(mon)] = email
    return dct


def build_list_of_schedules():
    i = 0
    lst = []
    for i in range(len(teams)):
        lst.append(build_schedule(i))
        i += 1
    return lst


def write_schedule_to_csv(file_name):
    """Write dictionary to csv."""

    with open(file_name, "w") as out_file:
        out_csv = csv.writer(out_file)
        out_csv.writerow(["date","assignees"])
        for mon, assignees in finalized_schedule.items():
            keys_values = (mon, *assignees)
            out_csv.writerow(keys_values)

    print(f'"{file_name}" exported successfully')


start_date = prompt_user_for_start_date()
mondays = build_list_of_mondays(start_date)
employees, teams = import_list_of_employees()
teams = get_list_of_teams()
schedules = build_list_of_schedules()
finalized_schedule = assemble_schedule()
output_schedule()
write_schedule_to_csv("schedule.csv")
