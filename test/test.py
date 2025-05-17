from tabulate import tabulate
import pandas as pd
import pdfplumber
import json
import re

class ClassRoutineExtractor:
    def __init__(self, pdf_path: str, output_csv: str, section: str, group: int, course_name_code_map: dict):
        self.pdf_path = pdf_path
        self.routine_csv = output_csv
        self.section = section
        self.group = group
        self.df = pd.DataFrame()
        self.routine_dict = {}
        self.course_name_code_map = course_name_code_map
        self.course_code = [
            "APTI401",
            "BUPRP",
            "SBC",
            "BCA47111(T)",
            "BCA47111(P)",
            "BCA49112",
            "BCA47113(T)",
            "BCA47113(P)",
            "BCA40201",
            "BCA40202",
        ]
        self.course_name = [
            "Aptitude-IV",
            "Preparatory Paper",
            "Soft Skill Boot Camp",
            "Design and Analysis of Algorithm",
            "Design and Analysis of Algorithm",
            "PHP and MySQL Lab",
            "Full-Stack Development-I",
            "Full-Stack Development-I",
            "Sustainability in Indian Knowledge System",
            "Computer Network"
        ]

    def process(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            table = pdf.pages[0].extract_tables()[0]

            # header = table[0]
            # table_data = table[:]
            table_data = table[5:9]

            for r_index, row in enumerate(table_data):
                # if r_index < 3:
                #     continue

                for c_index, col in enumerate(row):
                    pattern = r'[A-Z]+[0-9]*\s?\([A-Z]\)|[A-Z]+[0-9]*'

                    print(f"Row {r_index}, Column {c_index}: ", end="")

                    if c_index == 0:
                        print(f"Day: {col}", end="\n\n")
                        continue

                    if "gr." in col.lower().replace(" ", "").strip():
                        if f"gr.{self.section}{self.group}".lower() in col.lower().replace(" ", "").strip():
                            text = col.split(f"{self.section}{self.group}")

                            print(f"{len(text)} => {text}")
                        else:
                            print("No", end="\n")
                    else:
                        print(col, end="\n")

                    # normalized_by_regex_pattern_col_value = []
                    # for item in re.findall(pattern, col):
                    #     normalized_by_regex_pattern_col_value.append(item.replace(" ", "").strip())
                    #
                    # if len(normalized_by_regex_pattern_col_value) > 0:
                    #     matched_course_code = [code for code in self.course_code if code.strip() in normalized_by_regex_pattern_col_value]
                    #
                    #     print(matched_course_code, end="")
                    # else:
                    #     print(col, end="")

                    print("")

                print("\n\n")


course_name_code_map = {
    "APTI401": "Aptitude-IV",
    "BUPRP": "Preparatory Paper",
    "SBC": "Soft Skill Boot Camp",
    "BCA47111 (T)": "Design and Analysis of Algorithm",
    "BCA47111 (P)": "Design and Analysis of Algorithm",
    "BCA49112": "PHP and MySQL Lab",
    "BCA47113 (T)": "Full-Stack Development-I",
    "BCA47113 (P)": "Full-Stack Development-I",
    "BCA40201": "Sustainability in Indian Knowledge System",
    "BCA40202": "Computer Network"
}

course_code = [
"APTI401",
"BUPRP",
"SBC",
"BCA47111 (T)",
"BCA47111 (P)",
"BCA49112",
"BCA47113 (T)",
"BCA47113 (P)",
"BCA40201",
"BCA40202",
]

course_name = [
"Aptitude-IV",
"Preparatory Paper",
"Soft Skill Boot Camp",
"Design and Analysis of Algorithm",
"Design and Analysis of Algorithm",
"PHP and MySQL Lab",
"Full-Stack Development-I",
"Full-Stack Development-I",
"Sustainability in Indian Knowledge System",
"Computer Network"
]



if __name__ == "__main__":
    classRoutineExtractor = ClassRoutineExtractor("your_routine.pdf", "your_routine.csv", "G", 2, course_name_code_map)

    classRoutineExtractor.process()