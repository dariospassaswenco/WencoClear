# read_employees.py

import pandas as pd

def read_employees(file_path):
    """
    Reads the employee data from an Excel file and processes the dataframe.

    :param file_path: Path to the Excel file.
    :return: Processed dataframe
    """
    try:
        # Read the Excel file into a dataframe
        df = pd.read_excel(file_path)

        # Split the "Employee (First, Last)" column into "first_name" and "last_name"
        df[['first_name', 'last_name']] = df['Employee (First, Last) '].str.split(',', expand=True)
        df = df.drop(columns=['Employee (First, Last) '])

        # Rename the columns to match the database schema
        df = df.rename(columns={
            'Position': 'position_id',
            'shop_type': 'type_id',
            'wenco_id': 'wenco_id'
        })

        # Print the dataframe for testing
        print(df)

        # Return the dataframe for further use
        return df
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None

# Test the function
if __name__ == "__main__":
    test_file_path = r"C:\Users\Wenco\Documents\employees.xlsx"  # Replace with the actual path
    read_employees(test_file_path)
