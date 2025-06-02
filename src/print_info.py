from tabulate import tabulate
import pandas as pd


def print_tables(df: pd.DataFrame):
    if df.empty:
        print("No data to display.")
        return

    print(tabulate(df.fillna(""), headers='keys', tablefmt='grid'))


def print_dict_as_table(data: dict):
    if not data:
        print("No data to display.")
        return

    df = pd.DataFrame.from_dict(data, orient='index')
    df.reset_index(inplace=True)
    df.columns = ['Key'] + list(df.columns[1:])

    print(tabulate(df.fillna(""), headers='keys', tablefmt='grid'))
