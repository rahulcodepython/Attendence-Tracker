# Import the `print_tables` function from the `print_info` module in the same package.
# This function is used later to display tables in a formatted way.
from .print_info import print_tables

# Import the pandas library, which is used for data manipulation and analysis.
# Pandas provides powerful tools for working with tabular data, such as DataFrames.
import pandas as pd


# Define a class named `AttendanceExtractor` to encapsulate functionality related to attendance tracking.
# This class is responsible for parsing attendance data, storing it, and performing operations on it.
class AttendanceExtractor:
    # Define the constructor method for the class.
    # This method initializes the class with the attendance data and sets up necessary attributes.
    def __init__(self, classes: str):
        # Split the input string `classes` into individual rows based on newline characters.
        # Each row represents a line of attendance data.
        self.rows = classes.strip().split("\n")

        # Initialize an empty dictionary to store details about each course.
        # This dictionary will map course codes to their respective attendance details.
        self.course_details = {}

        # Initialize an empty pandas DataFrame to store attendance data in tabular format.
        # This DataFrame will be used for easier manipulation and display of data.
        self.df = pd.DataFrame()

        # Initialize an empty dictionary to map course codes to course names.
        # This mapping is useful for quick lookups of course names based on their codes.
        self.course_codes_names_map = {}

    # Define a method to parse the attendance data and populate the class attributes.
    def parse_table(self):
        # Iterate over each row in the `rows` list.
        # Each row contains tab-separated values representing attendance data for a course.
        for row in self.rows:
            # Check if the row is not empty.
            # Empty rows are skipped to avoid processing invalid data.
            if row:
                # Split the row into individual columns based on tab characters.
                # Each column represents a specific piece of information (e.g., course code, attendance).
                cols = row.split("\t")

                # Check if the row has fewer than 3 columns.
                # Rows with insufficient columns are considered malformed and skipped.
                if len(cols) < 3:
                    continue  # Skip malformed lines

                # Extract the attendance data (attended and occurred) from the third column.
                # The data is in the format "attended/occurred", so it is split by the "/" character.
                attended, occurred = map(int, cols[2].split("/"))

                # Use a try-except block to calculate the attendance percentage.
                # If `occurred` is zero, a `ZeroDivisionError` is caught, and the percentage is set to 0.0.
                try:
                    percentage = round((attended / occurred) * 100, 2)
                except ZeroDivisionError:
                    percentage = 0.0

                # Extract the course code and course name from the first and second columns, respectively.
                # These values are stripped of leading and trailing whitespace for consistency.
                course_code = cols[0].strip()
                course_name = cols[1].strip()

                # Check if the course code is not empty.
                # Only valid course codes are added to the `course_details` dictionary.
                if course_code:
                    # Add the course details to the `course_details` dictionary.
                    # The dictionary stores attendance data and the calculated percentage for each course.
                    self.course_details[course_code] = {
                        "course_name": course_name,
                        "attended": attended,
                        "occurred": occurred,
                        "percentage": percentage
                    }

                    # Add the course code and name to the `course_codes_names_map` dictionary.
                    # This mapping is useful for quick lookups of course names based on their codes.
                    self.course_codes_names_map[course_code] = course_name

        # Call the `parse_dataframe` method to convert the parsed data into a pandas DataFrame.
        self.parse_dataframe()

    # Define a method to convert the parsed attendance data into a pandas DataFrame.
    def parse_dataframe(self):
        # Create a pandas DataFrame from the `course_details` dictionary.
        # The dictionary keys become the index of the DataFrame, and the values become the rows.
        attendance_df = pd.DataFrame.from_dict(
            self.course_details, orient="index")

        # Set the name of the index column to "Course Code".
        # This makes the DataFrame more readable and descriptive.
        attendance_df.index.name = "Course Code"

        # Reset the index of the DataFrame, converting the index into a regular column.
        # This is done to make the DataFrame easier to work with and display.
        attendance_df.reset_index(inplace=True)

        # Rename the columns of the DataFrame to more descriptive names.
        # This improves readability and ensures consistency in column naming.
        attendance_df = attendance_df.rename(columns={
            "course_name": "Course Name",
            "attended": "Attended",
            "occurred": "Occurred",
            "percentage": "Percentage"
        })

        # Assign the modified DataFrame to the `df` attribute of the class.
        # This DataFrame is used for further operations and display.
        self.df = attendance_df

    # Define a method to display the attendance data as a formatted table.
    def show_attendance_table(self):
        # Call the `print_tables` function to display the `df` DataFrame.
        # This function formats the DataFrame into a readable table format.
        print_tables(self.df)

    # Define a method to update attendance data for a specific course.
    def add_classes(self, course_code: str, present: bool):
        # Retrieve the current number of attended classes for the specified course code.
        attended = self.course_details[course_code].get("attended")

        # Retrieve the current number of occurred classes for the specified course code.
        occurred = self.course_details[course_code].get("occurred")

        # Check if the student was present in the class.
        # If `present` is True, increment the `attended` count by 1.
        if present:
            attended += 1

        # Increment the `occurred` count by 1 to reflect the occurrence of a new class.
        occurred += 1

        # Calculate the updated attendance percentage.
        # If `occurred` is zero, the percentage is set to 0.0 to avoid division by zero.
        attendance_percentage = round(
            (attended / occurred) * 100, 2) if occurred != 0 else 0.0

        # Update the attendance details for the specified course code in the `course_details` dictionary.
        # The updated values include the new `attended` count, `occurred` count, and attendance percentage.
        self.course_details[course_code].update({
            "attended": attended,
            "occurred": occurred,
            "percentage": attendance_percentage
        })

    # Define a method to display the overall attendance status across all courses.
    def show_current_attendance_status(self):
        # Calculate the total number of attended classes across all courses.
        attended = self.df["Attended"].sum()

        # Calculate the total number of occurred classes across all courses.
        occurred = self.df["Occurred"].sum()

        # Calculate the overall attendance percentage.
        # If `occurred` is zero, the percentage is set to 0.0 to avoid division by zero.
        percentage = round(attended / occurred * 100,
                           2) if occurred != 0 else 0.0

        # Create a dictionary representing the total attendance row.
        # This row includes the total attended and occurred counts, as well as the overall percentage.
        total_row = {
            "Label": "Total",
            "Attended": attended,
            "Occurred": occurred,
            "Percentage": percentage,
            "Actual Percentage": round(percentage)
        }

        # Call the `print_tables` function to display the total attendance row as a formatted table.
        print_tables(pd.DataFrame([total_row]))
