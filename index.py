from tabulate import tabulate
import pandas as pd
import pdfplumber
import json



pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.width', None)    # Prevent line wrapping so wide dataframes are shown in one row
pd.set_option('display.max_colwidth', None)  # or use a large int value like 1000 if using older pandas


class RoutineExtractor:
    def __init__(self, pdf_path: str, output_csv: str, subject_course_code: dict):
        self.pdf_path = pdf_path
        self.routine_csv = output_csv
        self.subject_course_code_dict = subject_course_code
        self.df = pd.DataFrame()
        self.routine_dict = {}
        self.course_name_map = {
            code: data["course_name"].lower()
            for code, data in self.subject_course_code_dict.items()
            if data.get("course_name")
        }

    def refine_course_data(self, raw_entry):
        raw_entry_list = raw_entry.split("\n")
        return raw_entry_list[0]

    def extract_routine_table(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            table = pdf.pages[0].extract_tables()[0]

            header = table[0]
            table_data = table[1:]

            for r_index, row in enumerate(table_data):
                for c_index, col in enumerate(row):
                    if c_index == 0:
                        continue
                    table_data[r_index][c_index] = self.refine_course_data(
                        col)

            self.df = pd.DataFrame(table_data, columns=header)
            self.refine_dataframe_columns()

    def refine_dataframe_columns(self):
        if "Time Slot" in self.df.columns:
            self.df.set_index("Time Slot", inplace=True)
            local_df = self.df.T  # now days are index, time slots are columns
            local_df.reset_index(inplace=True)
            local_df.rename(columns={"index": "Day"}, inplace=True)

    def save_to_csv(self):
        self.df.to_csv(self.routine_csv, index=False)

    def processed_routine_data(self):
        for _, row in self.df.iterrows():
            day = row["Days"].strip().upper()
            self.routine_dict[day] = row.iloc[1:].tolist()

        return self.routine_dict

    def print_df_routine_table(self):
        print(tabulate(self.df.fillna(""), headers='keys', tablefmt='grid'))

    def print_df_routine_dict(self):
        self.processed_routine_data()
        print(json.dumps(self.routine_dict, indent=4, sort_keys=True))

    def process(self):
        self.extract_routine_table()

    def load_routine_from_csv(self):
        self.df = pd.read_csv(self.routine_csv)
        self.refine_dataframe_columns()
        self.df = self.df.fillna("")

class AttendanceExtractor:
    def __init__(self, classes:str, output_csv: str):
        self.rows = classes.strip().split("\n")
        self.table_data = []
        self.course_details = {}
        self.attendance_csv = output_csv
        self.df = pd.DataFrame()

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

                    self.table_data.append([
                        course_code,
                        course_name,
                        attended,
                        occurred,
                        percentage
                    ])

        self.parse_dataframe()

    def parse_dataframe(self):
        attendance_df = pd.DataFrame.from_dict(self.course_details, orient="index")
        attendance_df.index.name = "Course Code"
        attendance_df.reset_index(inplace=True)
        attendance_df = attendance_df.rename(columns={
            "course_name": "Course Name",
            "attended": "Attended",
            "occurred": "Occurred",
            "percentage": "Percentage"
        })

        self.df = attendance_df.fillna("")

    def save_to_csv(self):
        self.df.to_csv(self.attendance_csv, index=False)

    def print_df_attendance_table(self):
        print(tabulate(self.df.fillna(""), headers='keys', tablefmt='grid'))

    def print_df_attendance_dict(self):
        print(json.dumps(self.course_details, indent=4, sort_keys=True))

    def add_classes(self, course_code: str, present: bool):
        attended = self.course_details[course_code].get("attended")
        occurred = self.course_details[course_code].get("occurred")

        if present:
            attended += 1
        occurred += 1

        attendance_percentage = round((attended / occurred) * 100, 2) if occurred != 0 else 0.0

        self.course_details[course_code].update({
            "attended": attended,
            "occurred": occurred,
            "percentage": attendance_percentage
        })

    def print_current_attendance_status(self):
        attended = self.df["Attended"].sum()
        occurred = self.df["Occurred"].sum()

        percentage = round(attended / occurred * 100, 2) if occurred != 0 else 0.0

        total_row = {
            "Label": "Total",
            "Attended": attended,
            "Occurred": occurred,
            "Percentage": percentage,
            "Actual Percentage": round(percentage)
        }

        df = pd.DataFrame([total_row])

        print(tabulate(df.fillna(""), headers='keys', tablefmt='grid'))

    def process(self):
        self.parse_table()


ROUTINE_FILE = "./your_routine.pdf"
ROUTINE_CSV = "routine.csv"
ATTENDANCE_CSV = "attendance.csv"
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]

ATTENDANCE_CONTENT = """
APTI401	Aptitude-IV	9/14	64
BUPRP	Preparatory Paper	1/1	100
SBC	Soft Skill Boot Camp	25/29	86
BCA47111 (T)	Design and Analysis of Algorithm	23/27	85
BCA47111 (P)	Design and Analysis of Algorithm	44/59	75
BCA49112	PHP and MySQL Lab	40/53	75
BCA47113 (T)	Full-Stack Development-I	20/30	67
BCA47113 (P)	Full-Stack Development-I	45/60	75
BCA40201	Sustainability in Indian Knowledge System	48/60	80
BCA40202	Computer Network	50/59	85
"""

print("Routine Extractor")

attendance_extractor = AttendanceExtractor(ATTENDANCE_CONTENT, ATTENDANCE_CSV)
attendance_extractor.process()
attendance_extractor.print_df_attendance_table()  # Print attendance table
attendance_extractor.print_current_attendance_status()
course_details = attendance_extractor.course_details


routine_extractor = RoutineExtractor(ROUTINE_FILE, ROUTINE_CSV, course_details)
routine_extractor.load_routine_from_csv()
# routine_extractor.process()
routine_extractor.print_df_routine_table()  # Print routine table
routine_dict = routine_extractor.processed_routine_data()


# Print the refined data as dictionary
# routine_extractor.print_df_routine_dict()
# attendance_extractor.print_df_attendance_dict()

while True:
    print("Add day for prediction")
    print("Enter 1 for MONDAY")
    print("Enter 2 for TUESDAY")
    print("Enter 3 for WEDNESDAY")
    print("Enter 4 for THURSDAY")
    print("Enter 5 for FRIDAY")
    print("Enter 6 for SATURDAY")

    day_input: int = int(input("Enter the day: "))

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


    input_value = input("Press 'P' for all present \nPress 'A' for all absent \nPress 'M' for custom attendance \n: ")
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

            attendance_mark_input = input(f"Mark attendance for {course_name} (y/n): ")
            attendance_mark = attendance_mark_input[0].lower() == "y"

            attendance_marked_dict.append({i: attendance_mark})

    print("Before")
    # attendance_extractor.print_df_attendance_table()
    attendance_extractor.print_current_attendance_status()

    for i in attendance_marked_dict:
        for course_code, present in i.items():
            attendance_extractor.add_classes(course_code, present)

    print("After")
    attendance_extractor.parse_dataframe()
    # attendance_extractor.print_df_attendance_table()
    attendance_extractor.print_current_attendance_status()
