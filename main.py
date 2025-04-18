CLASS_ROUTINE = dict(
    MONDAY=[''],
    TUESDAY=['COMPUTER_NETWORK', 'COMPUTER_NETWORK',
             '', 'PHP_LAB', '', '', '', '', ''],
    WEDNESDAY=['', 'SOFT_SKILL', 'ENGLISH', 'IKS', 'IKS', '',
               'FULL_STACK_LAB', 'FULL_STACK_LAB', 'FULL_STACK_LAB'],
    THURSDAY=['', 'SOFT_SKILL', '', 'COMPUTER_NETWORK',
              'FULL_STACK_LAB', '', 'DAA_LAB', 'DAA_LAB', 'DAA_LAB'],
    FRIDAY=['', 'IKS', '', 'DAA', '', 'ENGLISH',
            'PHP_LAB', 'PHP_LAB', 'PHP_LAB'],
    SATURDAY=['IKS', 'COMPUTER_NETWORK', 'DAA_LAB', '',
              'DAA', 'FULL_STACK', 'FULL_STACK', 'APTI', ''],
)

TOTAL_CLASSES_BY_SUBJECT = dict(
    COMPUTER_NETWORK=45,
    FULL_STACK=22,
    FULL_STACK_LAB=48,
    DAA=21,
    DAA_LAB=47,
    IKS=43,
    PHP_LAB=40,
    SOFT_SKILL=22,
    APTI=11,
    ENGLISH=0
)

TOTAL_CLASSES_ATTENDED_BY_SUBJECT = dict(
    COMPUTER_NETWORK=42,
    FULL_STACK=18,
    FULL_STACK_LAB=39,
    DAA=20,
    DAA_LAB=37,
    IKS=40,
    PHP_LAB=32,
    SOFT_SKILL=21,
    APTI=8,
    ENGLISH=0
)

ATTENDANCE_PERCENTAGE_BY_SUBJECT = dict(
    COMPUTER_NETWORK=93.33,
    FULL_STACK=81.82,
    FULL_STACK_LAB=81.25,
    DAA=95.24,
    DAA_LAB=78.72,
    IKS=93.02,
    PHP_LAB=80.00,
    SOFT_SKILL=95.45,
    APTI=72.73,
    ENGLISH=0
)
# create a function to calculate overall percentage of attendance


def calculate_overall_attendance_percentage():
    """
    Calculates and prints the overall attendance percentage based on the total 
    number of classes and the number of attended classes for all subjects. 
    The percentage is rounded to two decimal places for absolute value and 
    then converted to a rounded integer for the final output.

    The function handles the case where the total number of classes is zero 
    to avoid a ZeroDivisionError. In such cases, the overall attendance 
    percentage is set to 0.0.

    Returns:
        int: The overall attendance percentage rounded to the nearest integer.

    Prints:
        - Absolute overall attendance percentage rounded to two decimal places.
        - Overall attendance percentage rounded to the nearest integer.

    Example:
        If TOTAL_CLASSES_BY_SUBJECT = {'Math': 50, 'Science': 50} and 
        TOTAL_CLASSES_ATTENDED_BY_SUBJECT = {'Math': 45, 'Science': 40}, 
        the function will calculate:
            total_classes = 100
            total_attended_classes = 85
            absolute percentage = 85.0%
            rounded percentage = 85%
    """
    total_classes = sum(TOTAL_CLASSES_BY_SUBJECT.values())
    total_attended_classes = sum(TOTAL_CLASSES_ATTENDED_BY_SUBJECT.values())
    try:
        overall_percentage = (total_attended_classes / total_classes) * 100
    except ZeroDivisionError:
        overall_percentage = 0.0
    attendance = round(overall_percentage, 2)
    print(f"Absolute overall Attendance Percentage: {attendance}%")
    # CONVERT the percentage into round figures like if the percentage is 90.33 then it will be 90 and if the percentage is 90.50 then it will be 91
    if attendance - int(attendance) >= 0.5:
        attendance = int(attendance) + 1
    else:
        attendance = int(attendance)
    print(f"Overall Attendance Percentage: {attendance}%")
    return attendance

# create a function to calculate the attendance percentage by subject , store them in a dictionary and print them


def calculate_attendance_percentage():
    attendance_percentage = {}
    for subject in TOTAL_CLASSES_BY_SUBJECT:
        total_classes = TOTAL_CLASSES_BY_SUBJECT[subject]
        attended_classes = TOTAL_CLASSES_ATTENDED_BY_SUBJECT[subject]
        try:
            percentage = (attended_classes / total_classes) * 100
        except ZeroDivisionError:
            percentage = 0.0
        attendance_percentage[subject] = round(percentage, 2)
        print(f"{subject}: {attendance_percentage[subject]}%")

# create a function to attend a class, here you have to increase the total classes by 1 and increase or decrease as attend or not to the subject


def attend_class(subject, attended=True):
    if subject in TOTAL_CLASSES_BY_SUBJECT:
        TOTAL_CLASSES_BY_SUBJECT[subject] += 1
        if attended:
            TOTAL_CLASSES_ATTENDED_BY_SUBJECT[subject] += 1
        else:
            TOTAL_CLASSES_ATTENDED_BY_SUBJECT[subject] += 0
    else:
        print("Subject not found.")


def attend_class_by_day(day, attendance=None):
    subjects = list(CLASS_ROUTINE[day])
    print("Subjects for Saturday:", subjects)
    if attendance is None:
        print("All classes attended")
        attendance = ['Y'] * len(subjects)
    else:
        print("Classes attended:", attendance)
        attendance = list(attendance)

    for i in range(len(subjects)):
        if subjects[i] == '':
            continue

        if attendance[i] == 'Y':
            attend_class(subjects[i], True)
        else:
            attend_class(subjects[i], False)


def go_to_collage(day, attendance=None):
    """
    Simulates attending college on a specific day and calculates the change in overall attendance percentage.
    This function takes the day of the week and optional attendance data, calculates the overall attendance 
    percentage before and after attending classes on the given day, and prints the change in attendance percentage.
    Args:
        day (str): The day of the week (e.g., "Monday", "Tuesday"). It is case-insensitive.
        attendance (dict, optional): A dictionary containing attendance data for the day. Defaults to None.
    Usage:
        # Example 1: Attend college on Monday without providing specific attendance data
        go_to_collage("Monday")
        # Example 2: Attend college on Wednesday with specific attendance data
        attendance_data = {"Math": True, "Science": False, "History": True}
        go_to_collage("Wednesday", attendance=attendance_data)
    Notes:
        - The function assumes the existence of helper functions `calculate_overall_attendance_percentage` 
          and `attend_class_by_day` to handle attendance calculations and updates.
        - The attendance percentage change is printed as a percentage value.
    """
    print(f"Before {day.lower()} attendance Percentage:")
    # calculate_attendance_percentage()
    before_overall_attendance_percentage = calculate_overall_attendance_percentage()
    attend_class_by_day(day, attendance)
    print(f"After {day.lower()} attendance Percentage:")
    # calculate_attendance_percentage()
    after_overall_attendance_percentage = calculate_overall_attendance_percentage()
    print(
        f"Attendance Percentage Change: {after_overall_attendance_percentage - before_overall_attendance_percentage}%")

    print("\n\n")


def main():
    """
    Main function to track attendance for different days of the week.

    This function calls the `go_to_collage` function with specific days and optional attendance data.
    The `go_to_collage` function is invoked multiple times with different parameters to simulate
    attendance tracking for various days.

    Function Calls:
    - `go_to_collage('SATURDAY')`: Tracks attendance for Saturday without additional data.
    - `go_to_collage('TUESDAY')`: Tracks attendance for Tuesday without additional data.
    - `go_to_collage('WEDNESDAY', ['', 'Y', 'Y', 'Y', 'Y', '', 'N', 'N', 'N'])`: Tracks attendance for Wednesday with specific attendance data.
    - `go_to_collage('THURSDAY', ['', 'Y', '', 'Y', 'Y', '', 'N', 'N', 'N'])`: Tracks attendance for Thursday with specific attendance data.
    - `go_to_collage('FRIDAY')`: Tracks attendance for Friday without additional data.
    - `go_to_collage('SATURDAY')`: Tracks attendance for Saturday without additional data.

    Note:
    - The `go_to_collage` function is assumed to handle attendance tracking logic for the specified day.
    - The optional attendance data is represented as a list of strings, where 'Y' indicates presence,
        'N' indicates absence, and an empty string indicates no data.
    """
    # go_to_collage('SATURDAY', ['N', 'N', 'N', '', 'N', 'N', 'N', 'N', ''])
    go_to_collage('SATURDAY')
    go_to_collage('TUESDAY')
    go_to_collage('WEDNESDAY', ['', 'Y', 'Y', 'Y', 'Y', '', 'N', 'N', 'N'])
    go_to_collage('THURSDAY', ['', 'Y', '', 'Y', 'Y', '', 'N', 'N', 'N'])
    go_to_collage('FRIDAY')
    go_to_collage('SATURDAY')


if __name__ == '__main__':
    main()
