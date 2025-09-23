import sys

GRADE_TABLE = { 'A1': 22, 'A2', 21, 'A3': 20, 'A4': 19, 'A5': 18, \
                'B1': 17, 'B2': 16, 'B3': 15, \
                'C1': 14, 'C2': 13, 'C3': 12, \
                'D1': 11, 'D2': 10, 'D3': 9, \
                'E1': 8,  'E2': 7,  'E3': 6, \
                'F1': 5,  'F2': 4,  'F3': 3, \
                'G1': 2,  'G2': 1,  'H': 0
              }

JSON_FILE = "glasgow.json"

def get_course_name(code):
    # placeholder
    pass

def get_course_code(name):
    # placeholder
    pass

def grade_to_gpa(grade):
    # placeholder
    pass

def gpa_to_grade(gpa):
    # placeholder
    pass

def aggregate_grades(grade_list):
    # placeholder
    pass


def load_json():
    with open('r', JSON_FILE) as f:
        contents = f.read()
        return json.loads()

def main():
    course_json = load_json()
    args = sys.argv[1:]
    if not args:
        print("Usage: script.py (-c <name> | -n <code> | -gpa <grade> | -grade <gpa> | -agg <grades...>)")
        sys.exit(1)

    flag = args[0]

    if flag == "-c" and len(args) == 2:
        get_course_name(args[1])
    elif flag == "-n" and len(args) > 1:
        name = " ".join(args[1:])
        get_course_code(args[1])
    elif flag == "-gpa" and len(args) == 2:
        grade_to_gpa(args[1])
    elif flag == "-grade" and len(args) == 2:
        gpa_to_grade(args[1])
    elif flag == "-agg" and len(args) > 1:
        grades = args[1:]  # all remaining arguments
        aggregate_grades(grades)
    else:
        print("Invalid usage.")
        sys.exit(1)



if __name__ == "__main__":
    main()
