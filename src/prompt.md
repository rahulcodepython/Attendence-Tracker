import re
from rapidfuzz import fuzz
import pandas as pd
from .print_info import print_tables
I have build a cli application to calculate the percentage of attendance of a day. I will take a pdf file as input which is the actual routine of the class and also some other info. and then in terminal it asks us to input a day and which classes we will attend or not. current attendance status must also give then It will calculate the attendance percentage. now it is in cli form. I want to build a gui application. can u build this using tkinter.  in my application I have to show many tables. and also a input form. so can u build this also I need some mordern design 


```python
+----+---------------+-------------------------------------------+------------+------------+--------------+
|    | Course Code   | Course Name                               |   Attended |   Occurred |   Percentage |
+====+===============+===========================================+============+============+==============+
|  0 | APTI401       | Aptitude-IV                               |          9 |         14 |        64.29 |
+----+---------------+-------------------------------------------+------------+------------+--------------+
|  1 | BUPRP         | Preparatory Paper                         |          1 |          1 |       100    |
+----+---------------+-------------------------------------------+------------+------------+--------------+
|  2 | SBC           | Soft Skill Boot Camp                      |         25 |         29 |        86.21 |
+----+---------------+-------------------------------------------+------------+------------+--------------+
|  3 | BCA47111(T)   | Design and Analysis of Algorithm          |         23 |         28 |        82.14 |
+----+---------------+-------------------------------------------+------------+------------+--------------+
|  4 | BCA47111(P)   | Design and Analysis of Algorithm          |         44 |         59 |        74.58 |
+----+---------------+-------------------------------------------+------------+------------+--------------+
|  5 | BCA49112      | PHP and MySQL Lab                         |         40 |         53 |        75.47 |
+----+---------------+-------------------------------------------+------------+------------+--------------+
|  6 | BCA47113(T)   | Full-Stack Development-I                  |         20 |         30 |        66.67 |
+----+---------------+-------------------------------------------+------------+------------+--------------+
|  7 | BCA47113(P)   | Full-Stack Development-I                  |         45 |         60 |        75    |
+----+---------------+-------------------------------------------+------------+------------+--------------+
|  8 | BCA40201      | Sustainability in Indian Knowledge System |         48 |         60 |        80    |
+----+---------------+-------------------------------------------+------------+------------+--------------+
|  9 | BCA40202      | Computer Network                          |         50 |         59 |        84.75 |
+----+---------------+-------------------------------------------+------------+------------+--------------+
+----+--------+---------------+----------------+-----------------+-----------------+----------------+---------------+---------------+---------------+---------------+---------------+---------------+
|    | Days   | 8:00 - 9:00   | 9:00 - 10:00   | 10:00 - 11:00   | 11:00 - 12:00   | 12:00 - 1:00   | 1:00 - 2:00   | 2:00 - 3:00   | 3:00 - 4:00   | 4:00 - 5:00   | 5:00 - 6:00   | 6:00 - 7:00   |
+====+========+===============+================+=================+=================+================+===============+===============+===============+===============+===============+===============+
|  0 | MON    |               |                |                 |                 |                |               |               |               |               |               |               |
+----+--------+---------------+----------------+-----------------+-----------------+----------------+---------------+---------------+---------------+---------------+---------------+---------------+
|  1 | TUE    |               | BCA40202       | BCA40202        |                 | BCA49112       |               |               |               |               |               |               |
+----+--------+---------------+----------------+-----------------+-----------------+----------------+---------------+---------------+---------------+---------------+---------------+---------------+
|  2 | WED    |               |                | SBC             |                 | BCA40201       | BCA40201      |               | BCA47113(P)   | BCA47113(P)   | BCA47113(P)   |               |
+----+--------+---------------+----------------+-----------------+-----------------+----------------+---------------+---------------+---------------+---------------+---------------+---------------+
|  3 | THU    |               |                | SBC             |                 | BCA40202       | BCA47113(P)   |               | BCA47111(P)   | BCA47111(P)   | BCA47111(P)   |               |
+----+--------+---------------+----------------+-----------------+-----------------+----------------+---------------+---------------+---------------+---------------+---------------+---------------+
|  4 | FRI    |               |                | BCA40201        |                 | BCA47111(T)    |               |               | BCA49112      | BCA49112      | BCA49112      |               |
+----+--------+---------------+----------------+-----------------+-----------------+----------------+---------------+---------------+---------------+---------------+---------------+---------------+
|  5 | SAT    |               | BCA40201       | BCA40202        | BCA47111(P)     |                | BCA47111(T)   | BCA47113(T)   | BCA47113(T)   | APTI401       |               |               |
+----+--------+---------------+----------------+-----------------+-----------------+----------------+---------------+---------------+---------------+---------------+---------------+---------------+
Add day for calculation
Enter 1 for MONDAY
Enter 2 for TUESDAY
Enter 3 for WEDNESDAY
Enter 4 for THURSDAY
Enter 5 for FRIDAY
Enter 6 for SATURDAY
Enter the day: 2
Press 'P' for all present 
Press 'A' for all absent 
Press 'M' for custom attendance 
: p
Before
+----+---------+------------+------------+--------------+---------------------+
|    | Label   |   Attended |   Occurred |   Percentage |   Actual Percentage |
+====+=========+============+============+==============+=====================+
|  0 | Total   |        305 |        393 |        77.61 |                  78 |
+----+---------+------------+------------+--------------+---------------------+
After
+----+---------+------------+------------+--------------+---------------------+
|    | Label   |   Attended |   Occurred |   Percentage |   Actual Percentage |
+====+=========+============+============+==============+=====================+
|  0 | Total   |        308 |        396 |        77.78 |                  78 |
+----+---------+------------+------------+--------------+---------------------+
Add day for calculation
Enter 1 for MONDAY
Enter 2 for TUESDAY
Enter 3 for WEDNESDAY
Enter 4 for THURSDAY
Enter 5 for FRIDAY
Enter 6 for SATURDAY
Enter the day:
```




this is my output in cli form. now i want to build a gui application using tkinter. I need this type of table. if U need the code I can attache to it.

```
# main.py

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
```

```
# attendance_extractor.py

class AttendanceExtractor:
    def __init__(self, classes: str):
        self.rows = classes.strip().split("\n")
        self.course_details = {}
        self.df = pd.DataFrame()
        self.course_codes_names_map = {}

    def parse_table(self):
        for row in self.rows:
            if row:
                cols = row.split("\t")

                if len(cols) < 3:
                    continue  # Skip malformed lines

                attended, occurred = map(int, cols[2].split("/"))

                try:
                    percentage = round((attended / occurred) * 100, 2)
                except ZeroDivisionError:
                    percentage = 0.0

                course_code = cols[0].strip()
                course_name = cols[1].strip()

                if course_code:
                    self.course_details[course_code] = {
                        "course_name": course_name,
                        "attended": attended,
                        "occurred": occurred,
                        "percentage": percentage
                    }
                    self.course_codes_names_map[course_code] = course_name

        self.parse_dataframe()

    def parse_dataframe(self):
        attendance_df = pd.DataFrame.from_dict(
            self.course_details, orient="index")
        attendance_df.index.name = "Course Code"
        attendance_df.reset_index(inplace=True)
        attendance_df = attendance_df.rename(columns={
            "course_name": "Course Name",
            "attended": "Attended",
            "occurred": "Occurred",
            "percentage": "Percentage"
        })

        self.df = attendance_df

    def show_attendance_table(self):
        print_tables(self.df)

    def add_classes(self, course_code: str, present: bool):
        attended = self.course_details[course_code].get("attended")
        occurred = self.course_details[course_code].get("occurred")

        if present:
            attended += 1
        occurred += 1

        attendance_percentage = round(
            (attended / occurred) * 100, 2) if occurred != 0 else 0.0

        self.course_details[course_code].update({
            "attended": attended,
            "occurred": occurred,
            "percentage": attendance_percentage
        })

    def show_current_attendance_status(self):
        attended = self.df["Attended"].sum()
        occurred = self.df["Occurred"].sum()

        percentage = round(attended / occurred * 100,
                           2) if occurred != 0 else 0.0

        total_row = {
            "Label": "Total",
            "Attended": attended,
            "Occurred": occurred,
            "Percentage": percentage,
            "Actual Percentage": round(percentage)
        }

        print_tables(pd.DataFrame([total_row]))
```

```


class RefineColumn:
    def __init__(self, col_value: str, course_codes_names_map: dict, section: str, group: int):
        self.col_value = col_value
        self.section = section
        self.group = group
        self.course_codes_pattern = list(set(course_codes_names_map.keys()))
        self.course_names_pattern = list(set(course_codes_names_map.values()))
        self.course_codes_names_map = course_codes_names_map

    def fuzzy_match_course_code(self, input_str, threshold=95):
        input_strs = input_str.strip().split('\n')

        for input_str in input_strs:
            for code in self.course_codes_pattern:
                score = fuzz.ratio(input_str, code)
                if score >= threshold:
                    return code

        return None

    def fuzzy_match_course_name(self, input_str, threshold=60):
        for course in self.course_names_pattern:
            score = fuzz.partial_ratio(course.lower(), input_str.lower())
            if score >= threshold:
                return course

        return None

    def extract_course_codes_from_raw_text_regex(self, text: str) -> str:
        return self.fuzzy_match_course_code(text)

    def extract_course_names_from_raw_text_regex(self, text):
        course_name = self.fuzzy_match_course_name(text)

        if course_name is None:
            return None

        # Use a reverse lookup dictionary for efficiency
        if not hasattr(self, '_name_to_code'):
            self._name_to_code = {v: k for k,
                                  v in self.course_codes_names_map.items()}
        return self._name_to_code.get(course_name)

    def extract_class_blocks(self, text: str):
        # Normalize line breaks and clean up the text
        text = text.strip().replace('\r\n', '\n').replace('\r', '\n')

        # Split by double newlines or more to separate potential blocks
        # Then filter out empty strings
        potential_blocks = [block.strip()
                            for block in re.split(r'\n\s*\n', text) if block.strip()]

        # If no clear separation, try to identify blocks by subject code pattern
        if len(potential_blocks) == 1:
            # Look for subject codes that start new blocks
            subject_pattern = r'^[A-Z]{3,5}\d{3,6}\s?\(?[TP]?\)?'
            lines = text.split('\n')

            blocks = []
            current_block = []

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Check if this line starts a new block (subject code at the beginning)
                if re.match(subject_pattern, line) and current_block:
                    # Save previous block
                    blocks.append('\n'.join(current_block))
                    current_block = [line]
                else:
                    current_block.append(line)

            # Don't forget the last block
            if current_block:
                blocks.append('\n'.join(current_block))

            return blocks

    def extract_groups_list(self, col_value: str, threshold=80) -> list:
        candidates = re.findall(
            r'\(?\bgr?\s*\.?\s*[a-zA-Z]\s*\d+\)?', col_value, flags=re.IGNORECASE)

        matches = []

        for candidate in candidates:
            cleaned = re.sub(r'[^A-Za-z0-9.]', '', candidate).lower()
            score = fuzz.ratio(
                cleaned, f"gr.{self.section.lower()}{self.group}")

            if score >= threshold:
                number_match = re.search(r'(\d+)', cleaned)
                if number_match:
                    matches.append(number_match.group(1))

        return matches

    def refine(self) -> str:
        if len(self.col_value) == 0:
            return None

        actual_course_code = None
        list_of_groups = self.extract_groups_list(self.col_value)

        if len(list_of_groups) == 0:
            actual_course_code = self.extract_course_codes_from_raw_text_regex(
                self.col_value)

            if actual_course_code is None:
                actual_course_code = self.extract_course_names_from_raw_text_regex(
                    self.col_value)
        else:
            list_of_all_classes: list[str] = self.extract_class_blocks(
                self.col_value)

            my_group_index = list_of_groups.index(
                str(self.group)) if str(self.group) in list_of_groups else -1

            if my_group_index == -1:
                return None

            my_classes = list_of_all_classes[my_group_index]

            actual_course_code = self.extract_course_codes_from_raw_text_regex(
                my_classes)

            if actual_course_code is None:
                actual_course_code = self.extract_course_names_from_raw_text_regex(
                    my_classes)

        return actual_course_code

```

import pandas as pd
import pdfplumber
from pathlib import Path
from .print_info import print_tables
from .refine_column import RefineColumn


class RoutineExtractor:
    def __init__(self, input_file: str, output_csv: str, course_codes_names_map: dict, section: str, group: int):
        self.root_path = Path(__file__).parent.parent
        self.input_file_path = Path.joinpath(
            self.root_path, "public", input_file)
        self.output_csv = Path.joinpath(
            self.root_path, "public", output_csv)

        self.course_codes_names_map = course_codes_names_map
        self.df = pd.DataFrame()
        self.routine_dict = {}

        self.section = section
        self.group = group

    def parsed_routine(self):
        with pdfplumber.open(self.input_file_path) as pdf:
            table = pdf.pages[0].extract_tables()[0]

            header = table[3]
            table_data = table[4:]  # from Monday to Saturday
            # table_data = table[5:6]  # for Tuesday only
            # table_data = table[6:7]  # for Wednesday only
            # table_data = table[8:9]  # for Friday only

            for r_index, row in enumerate(table_data):
                for c_index, col in enumerate(row):
                    if c_index == 0:
                        continue

                    table_data[r_index][c_index] = RefineColumn(
                        col, self.course_codes_names_map, self.section, self.group).refine() if len(col) > 0 else None

            routine_dataframe = pd.DataFrame(table_data, columns=header)

            if "Time Slot" in routine_dataframe.columns:
                routine_dataframe.set_index("Time Slot", inplace=True)
                routine_dataframe = routine_dataframe.T
                routine_dataframe.reset_index(inplace=True)
                routine_dataframe.rename(
                    columns={"index": "Day"}, inplace=True)

            self.df = routine_dataframe

    def save_to_csv(self):
        self.df.to_csv(self.output_csv, index=False)

    def show_routine_table(self):
        print_tables(self.df)

    def load_routine_from_csv(self):
        self.df = pd.read_csv(self.output_csv)
        self.refine_dataframe_columns()
        self.df = self.df.fillna("")

    def processed_routine_data(self):
        for _, row in self.df.iterrows():
            day = row["Days"].strip().upper()
            self.routine_dict[day] = row.iloc[1:].tolist()

        return self.routine_dict
