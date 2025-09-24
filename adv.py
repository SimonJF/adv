#!/usr/bin/env python3
import sys
import os.path
import json

# Data
GRADE_TABLE = { 'A1': 22, 'A2': 21, 'A3': 20, 'A4': 19, 'A5': 18, \
                'B1': 17, 'B2': 16, 'B3': 15, \
                'C1': 14, 'C2': 13, 'C3': 12, \
                'D1': 11, 'D2': 10, 'D3': 9, \
                'E1': 8,  'E2': 7,  'E3': 6, \
                'F1': 5,  'F2': 4,  'F3': 3, \
                'G1': 2,  'G2': 1,  'H': 0
              }

INV_GRADE_TABLE = dict([(v, k) for k, v in GRADE_TABLE.items()])
JSON_FILE = os.path.join("data", "glasgow.json")

#
def parse_float(s: str) -> float:
    try:
        return float(s)
    except ValueError:
        print(f'Invalid float: {s}')

# Functions
def get_course_name(courses: list[dict], code: str) -> None:
    def strip_compsci(code: str) -> str:
        return code.replace("COMPSCI", "")

    code = strip_compsci(code.upper())

    # Iterate through courses and return the first that matches the code
    for course in courses:
        if "course_code" in course and strip_compsci(course["course_code"]) == code:
            print(course["name"])
            return
    print("Course code not found.")

def get_course_code(courses: list[dict], query: str) -> None:
    # Make query string lowercase
    query = query.lower()

    # Returns true if the query is a substring of the course name or matches any alias
    def matches(course):
        return course["name"].lower().startswith(query) or query in course["aliases"]

    # Gather a list of all courses that match the query
    results = [course for course in courses if matches(course)]
    if len(results) == 0:
        print("No matches.")

    for course in results:
        print(f'{course["course_code"]}: ({course["name"]})')

def grade_to_gpa(grade: str) -> int:
    grade = grade.upper()
    if grade in GRADE_TABLE:
        return GRADE_TABLE[grade]
    else:
        print("Invalid grade.")
        sys.exit(1)

def gpa_to_grade(gpa: float) -> str:
    if gpa in INV_GRADE_TABLE:
        return INV_GRADE_TABLE[gpa]
    else:
        print(f'Invalid grade point: {gpa}.')
        sys.exit(1)

def print_gpa_to_grade(gpa: str) -> None:
    print(gpa_to_grade(parse_float(gpa)))

# Aggregates grades across a programme
def aggregate_grades(grade_list: list[str]) -> None:
    def parse_entry(entry):
        entry_split = entry.split("@")
        grade_point = grade_to_gpa(entry_split[0])
        creds = 10
        if len(entry_split) > 1:
            creds = int(entry_split[1])
        return (grade_point, creds)

    entries = [parse_entry(entry) for entry in grade_list]
    total_creds = sum([creds for (gp, creds) in entries])
    # Calculate credit-weighted average
    gpa = sum([grade_point * creds for (grade_point, creds) in entries]) / total_creds
    rounded = round(gpa)
    agg_grade = gpa_to_grade(rounded)
    print(f'Credit-weighted average: {gpa}')
    print(f'Rounded GPA: {rounded}')
    print(f'Aggregated Grade: {agg_grade}')

# Aggregates grades across a course. Percentages must add to 100.
def aggregate_course_grades(grade_list: list[str]) -> None:
    def parse_entry(entry):
        entry_split = entry.split("@")
        if len(entry_split) < 2:
            print("Must specify weighting for each component. For example, ./adv -cagg a2@80 b2@20")
        grade_point = grade_to_gpa(entry_split[0])
        weight = int(entry_split[1])
        return (grade_point, weight)

    entries = [parse_entry(entry) for entry in grade_list]
    total_weight = sum([weight for (gp, weight) in entries])
    if total_weight != 100:
        print("Component weight must sum to 100")
        sys.exit(1)

    gpa = sum([grade_point * (float(weight) / 100) for (grade_point, weight) in entries])
    rounded = round(gpa)
    agg_grade = gpa_to_grade(rounded)

    print(f'Component-weighted average: {gpa}')
    print(f'Rounded GPA: {rounded}')
    print(f'Aggregated Grade: {agg_grade}')



# IO
def load_json() -> list[dict]:
    with open(JSON_FILE, 'r') as f:
        contents = f.read()
        return json.loads(contents)

def main() -> None:
    def quit_with_usage():
        print("Usage: adv.py (-c <name> | -n <code> | -gpa <grade> | -g <gpa> | -cagg <grades...> | -agg <grades...>)")
        sys.exit(1)

    course_json = load_json()
    args = sys.argv[1:]
    if not args:
        quit_with_usage()

    flag = args[0]

    if flag == "-n" and len(args) == 2:
        get_course_name(course_json, args[1])
    elif flag == "-c" and len(args) > 1:
        name = " ".join(args[1:])
        get_course_code(course_json, name)
    elif flag == "-gpa" and len(args) == 2:
        print(grade_to_gpa(args[1]))
    elif flag == "-g" and len(args) == 2:
        print_gpa_to_grade(int(args[1]))
    elif flag == "-agg" and len(args) > 1:
        grades = args[1:]
        aggregate_grades(grades)
    elif flag == "-cagg" and len(args) > 1:
        grades = args[1:]
        aggregate_course_grades(grades)
    else:
        quit_with_usage()


if __name__ == "__main__":
    main()
