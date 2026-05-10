# column_detector.py
# Responsibility: Detect which columns are present in the loaded DataFrame
# and determine which analyses the tool can perform based on those columns.
# This file does NOT read the CSV — parser.py does that.
# This file ONLY inspects what columns the DataFrame has.


# ── Column Definitions ────────────────────────────────────────────────────────
# These are the core columns our tool expects in a basic CSV file
CORE_COLUMNS = [
    "Test ID",
    "Test Case Name",
    "Status",
    "Priority",
    "Assigned To",
    "Notes"
]

# These are extended columns that may or may not exist in the CSV
# Each one unlocks additional analyses if present
EXTENDED_COLUMNS = [
    "Expected Result",
    "Actual Result",
    "Test Suite",
    "Execution Time (s)",
    "Environment",
    "Browser / Device",
    "Sprint / Cycle",
    "Defect ID",
    "Date Executed",
    "Automated / Manual"
]





# ── Helper Function ───────────────────────────────────────────────────────────

def _check(col, found_columns):
    """
    A small private helper function.
    Returns True if a column name exists in the found columns list.
    The underscore at the start (_) is a Python convention meaning
    'this function is only meant to be used inside this file'.

    col:            the column name we are checking for e.g. "Status"
    found_columns:  the list of columns we actually found in the CSV
    """
    return col in found_columns


# ── Main Function ─────────────────────────────────────────────────────────────

def detect_columns(df):
    """
    Inspects a pandas DataFrame and returns a dictionary describing
    which columns were found and which analyses are available.

    df: the pandas DataFrame returned by parser.py
    """
    # Step 1: Get the real column names from the DataFrame
    # df.columns gives us an Index object — we convert it to a plain list
    actual_columns = list(df.columns)

    # Step 2: Find which CORE columns are present
    # List comprehension: for each column in CORE_COLUMNS,
    # keep it only if it exists in the actual CSV columns
    found_core = [col for col in CORE_COLUMNS if col in actual_columns]

    # Step 3: Find which EXTENDED columns are present
    found_extended = [col for col in EXTENDED_COLUMNS if col in actual_columns]

    # Step 4: Find any columns we don't recognize at all
    # These are columns the user has in their CSV that our tool doesn't know about
    known_columns = CORE_COLUMNS + EXTENDED_COLUMNS
    unknown_columns = [col for col in actual_columns if col not in known_columns]

    # Step 5: Find which CORE columns are completely missing
    # This helps us warn the user if something important is absent
    missing_core = [col for col in CORE_COLUMNS if col not in actual_columns]

    # Step 6: Build the available analyses dictionary
    # Each key is an analysis name, each value is True or False
    # True means we have the columns needed to perform that analysis
    # False means a required column is missing so we must skip it
    available_analyses = {
        # Basic analyses — need core columns
        "status_breakdown":         _check("Status", found_core),
        "priority_breakdown":       _check("Priority", found_core),
        "tester_breakdown":         _check("Assigned To", found_core),

        # Extended analyses — need specific extended columns
        "expected_vs_actual":       _check("Expected Result", found_extended)
                                    and _check("Actual Result", found_extended),

        "suite_breakdown":          _check("Test Suite", found_extended),
        "execution_time_analysis":  _check("Execution Time (s)", found_extended),
        "environment_breakdown":    _check("Environment", found_extended),
        "browser_breakdown":        _check("Browser / Device", found_extended),
        "sprint_info":              _check("Sprint / Cycle", found_extended),
        "defect_tracking":          _check("Defect ID", found_extended),
        "timeline_analysis":        _check("Date Executed", found_extended),
        "auto_vs_manual":           _check("Automated / Manual", found_extended),
    }

    # Step 7: Return everything as one clean dictionary
    # Every other file in the project will use this dictionary
    # to decide what it can and cannot do
    return {
        "all_columns":          actual_columns,
        "found_core":           found_core,
        "found_extended":       found_extended,
        "unknown_columns":      unknown_columns,
        "missing_core":         missing_core,
        "available_analyses":   available_analyses,
        "total_columns":        len(actual_columns),
    }