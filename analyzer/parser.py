# analyzer/parser.py
# -------------------------------------------------------
# Responsibility: Reading and parsing the input CSV file.
# This is the only file in the project that reads from disk.
# Every other module receives a clean DataFrame from here.
# -------------------------------------------------------

import pandas as pd    
from pathlib import Path

def load_csv(file_path):
    """
    Reads a CSV file and returns a clean pandas DataFrame.
    If anything goes wrong, it prints a clear error and returns None.

    file_path: a string or Path object pointing to the CSV file
    """

    # Step 1: Convert to a Path object
    # This works whether the user passed a string or a Path
    file_path = Path(file_path)

    # Step 2: Check if the file actually exists on disk
    # No point trying to open something that isn't there
    if not file_path.exists():
        print(f"\n[ERROR] File not found: {file_path}")
        print("Make sure your CSV file is inside the 'data' folder.\n")
        return None

    # Step 3: Check the file has a .csv extension
    # .suffix gives us the file extension e.g. ".csv", ".txt", ".xlsx"
    if file_path.suffix.lower() != ".csv":
        print(f"\n[ERROR] '{file_path.name}' is not a CSV file.")
        print("Please provide a file that ends with .csv\n")
        return None

    # Step 4: Try to read the file
    # We use try/except because many things can go wrong when reading files
    # (file is corrupted, file is open in Excel, encoding issues, etc.)
    try:

        # pd.read_csv() reads the CSV and returns a DataFrame
        df = pd.read_csv(file_path)

        # Step 5: Check if the file is completely empty
        if df.empty:
            print(f"\n[ERROR] '{file_path.name}' is empty.")
            print("Please provide a CSV file that contains data.\n")
            return None

        # Step 6: Clean up column names
        # .str.strip() removes accidental spaces from column names
        # Without this, "Status " and "Status" would be treated as different columns
        df.columns = df.columns.str.strip()

        # Step 7: Clean up all text values in the DataFrame
        # This removes accidental spaces from every cell that contains text
        # lambda is a small one-line function — here it strips spaces from text columns
        # dtype == "object" means the column contains text (strings)
        df = df.apply(
            lambda col: col.str.strip() if col.dtype == "object" else col
        )

        # Step 8: Tell the user everything loaded successfully
        print(f"\n[OK] Successfully loaded: {file_path.name}")
        print(f"     Total test cases found: {len(df)}")
        print(f"     Total columns found: {len(df.columns)}\n")

        # Step 9: Return the clean DataFrame to whoever called this function
        return df

    # If pandas couldn't read the file for any reason, catch the error here
    except Exception as e:
        print(f"\n[ERROR] Could not read the file.")
        print(f"        Reason: {e}\n")
        return None