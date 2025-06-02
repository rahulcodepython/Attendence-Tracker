from src.attendance_extractor import AttendanceExtractor
from src.routine_extractor import RoutineExtractor
from settings import *


DAYS: list[str] = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
BATCH: str = "2023"
SECTION: str = "G"
GROUP: int = 2
ROUTINE_FILE: str = "routine.pdf"
ROUTINE_CSV: str = f"routine-{SECTION.lower()}-{GROUP}-{BATCH.lower()}.csv"
ATTENDANCE_CONTENT: str = """
APTI401	Aptitude-IV	9/14	64
BUPRP	Preparatory Paper	1/1	100
SBC	Soft Skill Boot Camp	25/29	86
BCA47111(T)	Design and Analysis of Algorithm	23/28	82
BCA47111(P)	Design and Analysis of Algorithm	44/59	75
BCA49112	PHP and MySQL Lab	40/53	75
BCA47113(T)	Full-Stack Development-I	20/30	67
BCA47113(P)	Full-Stack Development-I	45/60	75
BCA40201	Sustainability in Indian Knowledge System	48/60	80
BCA40202	Computer Network	50/59	85
"""

print("Routine Extractor")

attendance_extractor = AttendanceExtractor(ATTENDANCE_CONTENT)
attendance_extractor.parse_table()
attendance_extractor.show_attendance_table()
course_codes_names_map = attendance_extractor.course_codes_names_map
course_details = attendance_extractor.course_details

routine_extractor = RoutineExtractor(
    ROUTINE_FILE, ROUTINE_CSV, course_codes_names_map, SECTION, GROUP)
routine_extractor.parsed_routine()
routine_extractor.show_routine_table()
routine_dict = routine_extractor.processed_routine_data()


while True:
    print("Add day for calculation")
    print("Enter 1 for MONDAY")
    print("Enter 2 for TUESDAY")
    print("Enter 3 for WEDNESDAY")
    print("Enter 4 for THURSDAY")
    print("Enter 5 for FRIDAY")
    print("Enter 6 for SATURDAY")

    try:
        day_input: int = int(input("Enter the day: "))
    except (ValueError, KeyboardInterrupt):
        print("\nInvalid input or interrupted by user")
        exit(1)

    match day_input:
        case 1:
            day = "MON"
        case 2:
            day = "TUE"
        case 3:
            day = "WED"
        case 4:
            day = "THU"
        case 5:
            day = "FRI"
        case 6:
            day = "SAT"
        case _:
            print("Invalid input")
            exit(1)

    try:
        input_value = input(
            "Press 'P' for all present \nPress 'A' for all absent \nPress 'M' for custom attendance \n: ")
    except (IndexError, KeyboardInterrupt):
        print("\nProgram is closed forcefully.")
        exit(1)

    parsed_input_value = input_value[0].strip().lower()
    attendance_marked_dict = []

    if parsed_input_value == "p":
        for i in routine_dict[day]:
            if i is None or len(i) <= 0:
                continue

            course_name = course_details[i].get("course_name")
            attendance_mark = True

            attendance_marked_dict.append({i: attendance_mark})

    elif parsed_input_value == "a":
        for i in routine_dict[day]:
            if i is None or len(i) <= 0:
                continue

            course_name = course_details[i].get("course_name")
            attendance_mark = False

            attendance_marked_dict.append({i: attendance_mark})

    else:
        for i in routine_dict[day]:
            if i is None or len(i) <= 0:
                continue

            course_name = course_details[i].get("course_name")

            try:
                attendance_mark_input = input(
                    f"Mark attendance for {course_name} (y/n): ")
            except (IndexError, KeyboardInterrupt):
                print("\nProgram is closed forcefully.")
                exit(1)

            attendance_mark = attendance_mark_input[0].lower() == "y"

            attendance_marked_dict.append({i: attendance_mark})

    print("Before")
    attendance_extractor.show_current_attendance_status()

    for i in attendance_marked_dict:
        for course_code, present in i.items():
            attendance_extractor.add_classes(course_code, present)

    print("After")
    attendance_extractor.parse_dataframe()
    attendance_extractor.show_current_attendance_status()
