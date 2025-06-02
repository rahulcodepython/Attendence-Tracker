import pandas as pd


pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
# Prevent line wrapping so wide dataframes are shown in one row
pd.set_option('display.width', None)
# or use a large int value like 1000 if using older pandas
pd.set_option('display.max_colwidth', None)
