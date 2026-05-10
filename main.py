from pathlib import Path
from analyzer.parser import load_csv
from analyzer.column_detector import detect_columns

BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / "data" / "full_test_results.csv"

def main():
    print("=" * 55)
    print("       CSV TEST RESULTS ANALYZER")
    print("=" * 55)

    # Step 1: Load the CSV
    df = load_csv(CSV_FILE)
    if df is None:
        return

    # Step 2: Detect columns
    column_info = detect_columns(df)

    # Step 3: Print what we found
    print("COLUMNS DETECTED")
    print("-" * 55)
    print(f"Total columns       : {column_info['total_columns']}")
    print(f"Core found          : {column_info['found_core']}")
    print(f"Extended found      : {column_info['found_extended']}")

    if column_info["missing_core"]:
        print(f"Core missing        : {column_info['missing_core']}")

    if column_info["unknown_columns"]:
        print(f"Unknown columns     : {column_info['unknown_columns']}")

    # Step 4: Print available analyses
    print("\nAVAILABLE ANALYSES")
    print("-" * 55)
    for analysis, is_available in column_info["available_analyses"].items():
        label = analysis.replace("_", " ").title()
        mark = "✔" if is_available else "✘"
        print(f"  {mark}  {label}")

if __name__ == "__main__":
    main()