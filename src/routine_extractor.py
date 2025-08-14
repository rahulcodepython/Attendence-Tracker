# Importing the pandas library, which is used for data manipulation and analysis.
import pandas as pd

# Importing the pdfplumber library, which is used to extract text and tables from PDF files.
import pdfplumber

# Importing the Path class from the pathlib module, which is used for handling filesystem paths.
from pathlib import Path

# Importing the print_tables function from the print_info module in the current package.
# This function is used to display tables in a readable format.
from .print_info import print_tables

# Importing the RefineColumn class from the refine_column module in the current package.
# This class is used to process and refine individual columns of the extracted table data.
from .refine_column import RefineColumn


# Defining the RoutineExtractor class, which encapsulates the functionality for extracting,
# processing, and saving routine data from a PDF file.
class RoutineExtractor:
    # The constructor (__init__) initializes the RoutineExtractor object with the necessary parameters.
    def __init__(self, input_file: str, output_csv: str, course_codes_names_map: dict, section: str, group: int):
        # Storing the root path of the project by getting the parent directory of the current file's location.
        self.root_path = Path(__file__).parent.parent

        # Constructing the full path to the input PDF file by joining the root path with the "public" directory and the input file name.
        self.input_file_path = Path.joinpath(
            self.root_path, "public", input_file)

        # Constructing the full path to the output CSV file by joining the root path with the "public" directory and the output file name.
        self.output_csv = Path.joinpath(
            self.root_path, "public", output_csv)

        # Storing the mapping of course codes to course names, which will be used to refine table data.
        self.course_codes_names_map = course_codes_names_map

        # Initializing an empty pandas DataFrame to store the processed routine data.
        self.df = pd.DataFrame()

        # Initializing an empty dictionary to store the routine data in a structured format.
        self.routine_dict = {}

        # Storing the section name (e.g., "A", "B") for filtering or refining table data.
        self.section = section

        # Storing the group number (e.g., 1, 2) for filtering or refining table data.
        self.group = group

    # Defining the parsed_routine method, which extracts and processes routine data from the input PDF file.
    def parsed_routine(self):
        # Opening the input PDF file using pdfplumber to extract its content.
        with pdfplumber.open(self.input_file_path) as pdf:
            # Extracting the first table from the first page of the PDF file.
            table = pdf.pages[0].extract_tables()[0]

            # Extracting the header row (column names) from the table.
            header = table[3]

            # Extracting the rows containing routine data (Monday to Saturday) from the table.
            table_data = table[4:]  # from Monday to Saturday

            # Iterating over each row and column in the extracted table data to refine the column values.
            for r_index, row in enumerate(table_data):
                for c_index, col in enumerate(row):
                    # Skipping the first column (e.g., "Time Slot") since it doesn't need refinement.
                    if c_index == 0:
                        continue

                    # Refining the column value using the RefineColumn class if the value is non-empty.
                    # The RefineColumn class processes the column value based on the course codes mapping,
                    # section, and group provided during initialization.
                    table_data[r_index][c_index] = RefineColumn(
                        col, self.course_codes_names_map, self.section, self.group).refine() if col and len(col) > 0 else None

            # Creating a pandas DataFrame from the refined table data, using the extracted header as column names.
            routine_dataframe = pd.DataFrame(table_data, columns=header)

            # Checking if the "Time Slot" column exists in the DataFrame.
            if "Time Slot" in routine_dataframe.columns:
                # Setting the "Time Slot" column as the index of the DataFrame for better organization.
                routine_dataframe.set_index("Time Slot", inplace=True)

                # Transposing the DataFrame to switch rows and columns, making it easier to work with days as rows.
                routine_dataframe = routine_dataframe.T

                # Resetting the index of the DataFrame to convert the index into a regular column.
                routine_dataframe.reset_index(inplace=True)

                # Renaming the "index" column to "Day" for clarity.
                routine_dataframe.rename(
                    columns={"index": "Day"}, inplace=True)

            # Storing the processed routine data in the object's DataFrame attribute.
            self.df = routine_dataframe

    # Defining the save_to_csv method, which saves the processed routine data to a CSV file.
    def save_to_csv(self):
        # Using pandas' to_csv method to save the DataFrame to the specified output CSV file.
        # The index parameter is set to False to exclude the index column from the CSV file.
        self.df.to_csv(self.output_csv, index=False)

    # Defining the show_routine_table method, which displays the routine data in a readable table format.
    def show_routine_table(self):
        # Calling the print_tables function to print the DataFrame in a formatted way.
        print_tables(self.df)

    # Defining the processed_routine_data method, which converts the routine data into a dictionary format.
    def processed_routine_data(self):
        # Iterating over each row in the DataFrame to populate the routine dictionary.
        for _, row in self.df.iterrows():
            # Extracting the day name from the "Days" column and converting it to uppercase for consistency.
            day = row["Days"].strip().upper()

            # Storing the routine data for the day as a list of values from the remaining columns in the row.
            self.routine_dict[day] = row.iloc[1:].tolist()

        # Returning the routine dictionary, which contains the processed routine data organized by day.
        return self.routine_dict
