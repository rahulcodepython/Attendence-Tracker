# Import the AttendanceExtractor class from the src.attendance_extractor module.
# This class is responsible for extracting and managing attendance data.
from src.attendance_extractor import AttendanceExtractor

# Import the RoutineExtractor class from the src.routine_extractor module.
# This class is responsible for extracting and processing routine data.
from src.routine_extractor import RoutineExtractor

# Import all settings from the settings module.
# This allows the program to use predefined configurations or constants.
from settings import *

# Define a list of strings representing the days of the week.
# These are used to map user input to specific days in the routine.
DAYS: list[str] = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]

# Define the batch year as a string. This is used to identify the batch of students.
BATCH: str = "2025"

# Define the section of the batch as a string. This is used to differentiate between sections.
SECTION: str = "H"

# Define the group number as an integer. This is used to specify the group within the section.
GROUP: int = 2

# Define the filename of the routine PDF file as a string.
# This file contains the schedule for classes.
ROUTINE_FILE: str = "routine.pdf"

# Generate the name of the routine CSV file dynamically based on the section, group, and batch.
# This file will store the processed routine data in a structured format.
ROUTINE_CSV: str = f"routine-{SECTION.lower()}-{GROUP}-{BATCH.lower()}.csv"

# Define a multiline string containing attendance data.
# This data includes course codes, course names, attendance counts, and percentages.
ATTENDANCE_CONTENT: str = """
BCA50114	Software Engineering	12/12	100
BCA50115	Cloud Computing	5/6	83
BCA57116 (T)	Full-stack Development-II	5/5	100
BCA57116 (P)	Full-stack Development-II	12/12	100
BCA57203 (T)	Artificial Intelligence	6/6	100
BCA57203 (P)	Artificial Intelligence	12/12	100
BCA57204 (T)	Machine Learning	6/6	100
BCA57204 (P)	Machine Learning	11/12	92
BUPRP	Preparatory Paper	2/2	100
TBC	Technical Boot Camp	5/7	71
APTI	Aptitude-V	3/3	100
"""

# Print a message indicating the start of the Routine Extractor process.
print("Routine Extractor")

# Create an instance of the AttendanceExtractor class, passing the attendance content as a parameter.
# This initializes the extractor with the provided attendance data.
attendance_extractor = AttendanceExtractor(ATTENDANCE_CONTENT)

# Call the parse_table method of the AttendanceExtractor instance.
# This method processes the attendance data and organizes it into a structured format.
attendance_extractor.parse_table()

# Call the show_attendance_table method of the AttendanceExtractor instance.
# This method displays the attendance data in a tabular format for the user.
attendance_extractor.show_attendance_table()

# Retrieve the mapping of course codes to course names from the AttendanceExtractor instance.
# This dictionary is used to associate course codes with their respective names.
course_codes_names_map = attendance_extractor.course_codes_names_map

# Retrieve detailed attendance information for each course from the AttendanceExtractor instance.
# This dictionary contains attendance counts and percentages for each course.
course_details = attendance_extractor.course_details

# Create an instance of the RoutineExtractor class, passing several parameters:
# - ROUTINE_FILE: The filename of the routine PDF file.
# - ROUTINE_CSV: The filename of the routine CSV file.
# - course_codes_names_map: The mapping of course codes to course names.
# - SECTION: The section of the batch.
# - GROUP: The group within the section.
# This initializes the extractor with the provided routine data and configurations.
routine_extractor = RoutineExtractor(
    ROUTINE_FILE, ROUTINE_CSV, course_codes_names_map, SECTION, GROUP)

# Call the parsed_routine method of the RoutineExtractor instance.
# This method processes the routine data and organizes it into a structured format.
routine_extractor.parsed_routine()

# Call the show_routine_table method of the RoutineExtractor instance.
# This method displays the routine data in a tabular format for the user.
routine_extractor.show_routine_table()

# Retrieve the processed routine data from the RoutineExtractor instance.
# This dictionary contains the schedule for each day, including course codes.
routine_dict = routine_extractor.processed_routine_data()

# Start an infinite loop to repeatedly prompt the user for input.
# This loop allows the user to mark attendance for different days.
while True:
    # Print instructions for the user to select a day for attendance calculation.
    print("Add day for calculation")
    print("Enter 1 for MONDAY")
    print("Enter 2 for TUESDAY")
    print("Enter 3 for WEDNESDAY")
    print("Enter 4 for THURSDAY")
    print("Enter 5 for FRIDAY")
    print("Enter 6 for SATURDAY")

    try:
        # Prompt the user to enter a number corresponding to a day of the week.
        # Convert the input to an integer.
        day_input: int = int(input("Enter the day: "))
    except (ValueError, KeyboardInterrupt):
        # Handle invalid input or user interruption.
        # Print an error message and exit the program with a status code of 1.
        print("\nInvalid input or interrupted by user")
        exit(1)

    # Use a match-case statement to map the user's input to a day of the week.
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
            # Handle invalid input by printing an error message and exiting the program.
            print("Invalid input")
            exit(1)

    try:
        # Prompt the user to select an attendance marking mode.
        # The user can choose to mark all present, all absent, or custom attendance.
        input_value = input(
            "Press 'P' for all present \nPress 'A' for all absent \nPress 'M' for custom attendance \n: ")
    except (IndexError, KeyboardInterrupt):
        # Handle invalid input or user interruption.
        # Print an error message and exit the program with a status code of 1.
        print("\nProgram is closed forcefully.")
        exit(1)

    # Extract the first character of the user's input, convert it to lowercase, and strip any whitespace.
    # This ensures the input is in a consistent format for comparison.
    parsed_input_value = input_value[0].strip().lower()

    # Initialize an empty list to store attendance marking data for the selected day.
    attendance_marked_dict = []

    # Check if the user selected the "all present" mode.
    if parsed_input_value == "p":
        # Iterate over the list of course codes for the selected day in the routine dictionary.
        for i in routine_dict[day]:
            # Skip empty or invalid course codes.
            if i is None or len(i) <= 0:
                continue

            # Retrieve the course name for the current course code from the course details dictionary.
            course_name = course_details[i].get("course_name")

            # Set the attendance mark to True, indicating the student is present.
            attendance_mark = True

            # Append a dictionary containing the course code and attendance mark to the list.
            attendance_marked_dict.append({i: attendance_mark})

    # Check if the user selected the "all absent" mode.
    elif parsed_input_value == "a":
        # Iterate over the list of course codes for the selected day in the routine dictionary.
        for i in routine_dict[day]:
            # Skip empty or invalid course codes.
            if i is None or len(i) <= 0:
                continue

            # Retrieve the course name for the current course code from the course details dictionary.
            course_name = course_details[i].get("course_name")

            # Set the attendance mark to False, indicating the student is absent.
            attendance_mark = False

            # Append a dictionary containing the course code and attendance mark to the list.
            attendance_marked_dict.append({i: attendance_mark})

    # Handle the "custom attendance" mode.
    else:
        # Iterate over the list of course codes for the selected day in the routine dictionary.
        for i in routine_dict[day]:
            # Skip empty or invalid course codes.
            if i is None or len(i) <= 0:
                continue

            # Retrieve the course name for the current course code from the course details dictionary.
            course_name = course_details[i].get("course_name")

            try:
                # Prompt the user to mark attendance for the current course.
                # The user can enter "y" for present or "n" for absent.
                attendance_mark_input = input(
                    f"Mark attendance for {course_name} (y/n): ")
            except (IndexError, KeyboardInterrupt):
                # Handle invalid input or user interruption.
                # Print an error message and exit the program with a status code of 1.
                print("\nProgram is closed forcefully.")
                exit(1)

            # Convert the user's input to lowercase and check if it is "y".
            # Set the attendance mark to True for "y" and False otherwise.
            attendance_mark = attendance_mark_input[0].lower() == "y"

            # Append a dictionary containing the course code and attendance mark to the list.
            attendance_marked_dict.append({i: attendance_mark})

    # Print a message indicating the attendance status before marking.
    print("Before")

    # Call the show_current_attendance_status method of the AttendanceExtractor instance.
    # This method displays the current attendance status for all courses.
    attendance_extractor.show_current_attendance_status()

    # Iterate over the list of attendance marking data.
    for i in attendance_marked_dict:
        # Iterate over the course code and attendance mark in each dictionary.
        for course_code, present in i.items():
            # Call the add_classes method of the AttendanceExtractor instance.
            # This method updates the attendance data for the specified course code.
            # The "present" parameter indicates whether the student is present or absent.
            attendance_extractor.add_classes(course_code, present)

    # Print a message indicating the attendance status after marking.
    print("After")

    # Call the parse_dataframe method of the AttendanceExtractor instance.
    # This method processes the updated attendance data and organizes it into a structured format.
    attendance_extractor.parse_dataframe()

    # Call the show_current_attendance_status method of the AttendanceExtractor instance.
    # This method displays the updated attendance status for all courses.
    attendance_extractor.show_current_attendance_status()
