# Import the tabulate function from the 'tabulate' library
# This library is used to display tabular data (like lists or DataFrames)
# in a well-formatted ASCII table. It supports multiple formatting styles such as 'grid', 'pipe', etc.
from tabulate import tabulate

# Import pandas as pd, a powerful data analysis and manipulation library
# Pandas allows us to easily create and work with DataFrames, which are like
# spreadsheet tables with labeled rows and columns.
import pandas as pd


# Define a function named 'print_tables' that takes a pandas DataFrame as input
# This function will print the DataFrame as a table with borders and headers
# so that it is human-readable in the console or terminal.
def print_tables(df: pd.DataFrame):
    # First, check if the DataFrame is empty using the 'empty' attribute.
    # A DataFrame is considered empty if it has no rows or no columns.
    if df.empty:
        # If the DataFrame is empty, print a friendly message to inform the user.
        # This prevents trying to display an empty table which would be meaningless.
        print("No data to display.")
        # Exit the function early since there is no data to process or display.
        return

    # If the DataFrame has data, we proceed to display it.
    # 'fillna("")' replaces any missing (NaN) values with an empty string
    # so that the table output looks clean without "nan" text in cells.
    # 'values.tolist()' converts the DataFrame into a list of lists,
    # where each inner list is a row of values from the DataFrame.
    # 'headers=list(df.columns)' specifies that the column names from the DataFrame
    # will be used as the table headers in the output.
    # 'tablefmt="grid"' tells tabulate to draw the table with grid lines around each cell,
    # making it look like a well-bordered spreadsheet.
    print(
        tabulate(
            # Step 1: Replace NaN with '' and turn the table into rows for printing.
            df.fillna("").values.tolist(),
            # Step 2: Use DataFrame's column names as table headers.
            headers=list(df.columns),
            # Step 3: Format table with visible cell borders for clarity.
            tablefmt='grid'
        )
    )


# Define a function named 'print_dict_as_table' that takes a dictionary as input.
# This function will print the dictionary contents as a table, even if
# the dictionary is nested or has multiple values per key.
def print_dict_as_table(data: dict):
    # Check if the dictionary is empty.
    # If it's empty, there is nothing to display and trying to create a table would be pointless.
    if not data:
        # Inform the user that there is no data to print.
        print("No data to display.")
        # Exit the function early to prevent unnecessary processing.
        return

    # Convert the dictionary into a pandas DataFrame.
    # 'from_dict(data, orient="index")' treats the dictionary keys as the index (row labels)
    # and the values as the data for each row.
    # This is especially useful if the dictionary values themselves are lists or dictionaries.
    df = pd.DataFrame.from_dict(data, orient='index')

    # Reset the index so that the former dictionary keys are turned into a regular column.
    # Without this, the keys would remain as index labels and would not appear as part of the table body.
    # After this step, the table will have a numeric index (0, 1, 2, ...) and a separate column for the keys.
    df.reset_index(inplace=True)

    # Rename the first column (which contains the original dictionary keys) to 'Key'
    # so that it has a clear and descriptive header.
    # 'list(df.columns[1:])' keeps the names of all other columns exactly as they are.
    df.columns = ['Key'] + list(df.columns[1:])

    # Prepare the DataFrame for display.
    # 'fillna("")' replaces any missing values with empty strings for a cleaner appearance.
    # 'values.tolist()' converts each row into a Python list so that 'tabulate' can print it.
    # 'headers="keys"' tells tabulate to automatically use the DataFrame's column names as the table headers.
    # 'tablefmt="grid"' draws clear grid borders around every cell for better readability.
    print(
        tabulate(
            # Step 1: Replace NaNs and prepare row data for tabulate.
            df.fillna("").values.tolist(),
            # Step 2: Use column names as table headers automatically.
            headers='keys',
            # Step 3: Use grid borders for a structured and readable table.
            tablefmt='grid'
        )
    )
