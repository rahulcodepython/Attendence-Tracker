from .print_info import print_tables
import pandas as pd


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
