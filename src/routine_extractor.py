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
