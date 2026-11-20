# =====================================================================
# COMMUNITY WATER CONSUMPTION AND BILLING MANAGEMENT SYSTEM
# NCV Level 4 | Advanced Python | Individual Practical Assessment
# Compiled by Dr HD Masethe
# ---------------------------------------------------------------------
# This program reads water_readings.txt, validates every record,
# calculates progressive water bills, classifies consumption,
# ranks the top five consumers manually (no sorted/max/min),
# and writes billing_report.txt and errors.log.
# =====================================================================

# ---------------------------------------------------------------------
# SECTION 1: GLOBAL CONSTANTS AND CONFIGURATION
# ---------------------------------------------------------------------

INPUT_FILE   = "water_readings.txt"
REPORT_FILE  = "billing_report.txt"
ERROR_FILE   = "errors.log"

FREE_LIMIT        = 6      # kL free
LOW_BAND_LIMIT    = 20     # kL end of band 2
RATE_BAND_2       = 8.50   # R per kL for 6 < kL <= 20
RATE_BAND_3       = 12.00  # R per kL for kL > 20

LOW_LIMIT         = 20     # LOW: 0-20 kL
MODERATE_LIMIT    = 50     # MODERATE: 20 < kL <= 50, HIGH: > 50


# ---------------------------------------------------------------------
# SECTION 2: FILE HANDLING (Q1)
# ---------------------------------------------------------------------

def read_input_file(filename):
    """Q1: Read all lines from the input file; handle a missing file."""
    try:
        with open(filename, "r") as infile:
            lines = infile.readlines()
        print("Input file '" + filename + "' read successfully.")
        print("Total lines read: " + str(len(lines)))
        return lines
    except FileNotFoundError:
        print("ERROR: The file '" + filename + "' was not found.")
        print("Please place water_readings.txt in the same folder as this program.")
        return []
    except IOError:
        print("ERROR: Could not read '" + filename + "'.")
        return []


# ---------------------------------------------------------------------
# SECTION 3: FIELD CLEANING AND VALIDATION (Q2, Q3)
# ---------------------------------------------------------------------

def split_and_clean(line):
    """Q2: Split a raw line into cleaned fields.
       Returns a list of 5 cleaned strings, or the raw field list
       if the field count is not 5 (so validator can reject it)."""
    raw_fields = line.strip().split(",")
    cleaned = []
    for field in raw_fields:
        cleaned.append(field.strip())
    return cleaned


def validate_record(fields, seen_meters):
    """Q3: Validate one record against all rejection rules.
       Returns (record_dict, None) on success,
       or (None, reason_string) on rejection."""
    # --- Rule 1: exactly 5 fields ---
    if len(fields) != 5:
        return None, "wrong number of fields (expected 5, got " + str(len(fields)) + ")"

    meter, name, prev_str, curr_str, area = fields

    # --- Rule 2: no missing/blank fields ---
    if meter == "":
        return None, "missing meter number"
    if name == "":
        return None, "missing household name"
    if prev_str == "":
        return None, "missing previous reading"
    if curr_str == "":
        return None, "missing current reading"
    if area == "":
        return None, "missing area"

    # --- Rule 3: duplicate meter number ---
    if meter in seen_meters:
        return None, "duplicate meter number '" + meter + "'"

    # --- Rule 4: numeric readings ---
    try:
        previous = float(prev_str)
    except ValueError:
        return None, "non-numeric previous reading '" + prev_str + "'"
    try:
        current = float(curr_str)
    except ValueError:
        return None, "non-numeric current reading '" + curr_str + "'"

    # --- Rule 5: negative readings ---
    if previous < 0:
        return None, "negative previous reading (" + prev_str + ")"
    if current < 0:
        return None, "negative current reading (" + curr_str + ")"

    # --- Rule 6: current must not be below previous ---
    if current < previous:
        return None, ("current reading (" + curr_str +
                      ") is below previous reading (" + prev_str + ")")

    record = {
        "meter":     meter,
        "name":      name,
        "previous":  previous,
        "current":   current,
        "area":      area,
    }
    return record, None


# ---------------------------------------------------------------------
# SECTION 4: CONSUMPTION AND BILLING CALCULATIONS (Q4, Q5)
# ---------------------------------------------------------------------

def calculate_consumption(record):
    """Q4: Monthly consumption in kL = current - previous."""
    return record["current"] - record["previous"]


def calculate_bill(consumption):
    """Q5: Progressive tariff across three bands.
       First 6 kL free, next 14 kL @ R8.50, remainder @ R12.00."""
    bill = 0.0

    # Band 1: first 6 kL free (no charge)
    if consumption <= FREE_LIMIT:
        return 0.0

    # Band 2: above 6 up to 20 kL @ R8.50
    if consumption <= LOW_BAND_LIMIT:
        bill += (consumption - FREE_LIMIT) * RATE_BAND_2
        return bill

    # Full band 2 is charged when consumption > 20
    bill += (LOW_BAND_LIMIT - FREE_LIMIT) * RATE_BAND_2   # 14 kL
    # Band 3: above 20 kL @ R12.00
    bill += (consumption - LOW_BAND_LIMIT) * RATE_BAND_3
    return bill


# ---------------------------------------------------------------------
# SECTION 5: CONSUMPTION CLASSIFICATION (Q6)
# ---------------------------------------------------------------------

def classify_consumption(consumption):
    """Q6: LOW = 0-20 kL, MODERATE = above 20 up to 50 kL,
       HIGH = above 50 kL."""
    if consumption <= LOW_LIMIT:
        return "LOW"
    elif consumption <= MODERATE_LIMIT:
        return "MODERATE"
    else:
        return "HIGH"


# ---------------------------------------------------------------------
# SECTION 6: MANUAL TOP-FIVE RANKING (Q7)
# ---------------------------------------------------------------------

def rank_top_five(valid_records):
    """Q7: Manually rank the five highest-consuming households.
       Uses only loops and comparisons - NO sorted(), max() or min()."""
    # Step 1: Build a parallel list of (consumption, meter) pairs
    pairs = []
    for meter in valid_records:
        cons = calculate_consumption(valid_records[meter])
        pairs.append([cons, meter])

    # Step 2: Selection-sort style pass to place top 5 at the front
    # We only need the top 5, so we scan/swap at most 5 times.
    n = len(pairs)
    top_count = 5
    if n < top_count:
        top_count = n

    for i in range(top_count):
        max_index = i
        for j in range(i + 1, n):
            if pairs[j][0] > pairs[max_index][0]:
                max_index = j
        if max_index != i:
            temp = pairs[i]
            pairs[i] = pairs[max_index]
            pairs[max_index] = temp

    # Step 3: Return the first top_count entries
    return pairs[:top_count]


# ---------------------------------------------------------------------
# SECTION 7: REPORT AND ERROR-LOG WRITING (Q8)
# ---------------------------------------------------------------------

def write_report(valid_records, top_five):
    """Q8a: Write billing_report.txt with all valid household info,
       categories, top five and a summary."""

    # ---- Compute aggregates with loops (no sum()) ----
    total_consumption = 0.0
    total_bill = 0.0
    low_count = 0
    moderate_count = 0
    high_count = 0

    for meter in valid_records:
        rec = valid_records[meter]
        cons = calculate_consumption(rec)
        bill = calculate_bill(cons)
        label = classify_consumption(cons)

        total_consumption += cons
        total_bill += bill
        if label == "LOW":
            low_count += 1
        elif label == "MODERATE":
            moderate_count += 1
        else:
            high_count += 1

    with open(REPORT_FILE, "w") as rep:
        rep.write("=" * 78 + "\n")
        rep.write("COMMUNITY WATER CONSUMPTION AND BILLING REPORT\n")
        rep.write("=" * 78 + "\n\n")

        # ---- Household billing information ----
        rep.write("VALID HOUSEHOLD BILLING INFORMATION\n")
        rep.write("-" * 78 + "\n")
        rep.write("{:<8} {:<22} {:<14} {:>9} {:>9} {:>11} {:>12}\n".format(
            "Meter", "Household", "Area", "Previous", "Current",
            "Consumption", "Bill (R)"))
        rep.write("-" * 78 + "\n")

        for meter in valid_records:
            rec = valid_records[meter]
            cons = calculate_consumption(rec)
            bill = calculate_bill(cons)
            rep.write("{:<8} {:<22} {:<14} {:>9.1f} {:>9.1f} {:>11.1f} {:>12.2f}\n".format(
                rec["meter"], rec["name"], rec["area"],
                rec["previous"], rec["current"], cons, bill))

        # ---- Consumption categories ----
        rep.write("\n")
        rep.write("CONSUMPTION CATEGORIES\n")
        rep.write("-" * 78 + "\n")
        rep.write("{:<8} {:<22} {:>11} {:<10}\n".format(
            "Meter", "Household", "Consumption", "Category"))
        rep.write("-" * 78 + "\n")
        for meter in valid_records:
            rec = valid_records[meter]
            cons = calculate_consumption(rec)
            label = classify_consumption(cons)
            rep.write("{:<8} {:<22} {:>11.1f} {:<10}\n".format(
                rec["meter"], rec["name"], cons, label))

        # ---- Top five consumers ----
        rep.write("\n")
        rep.write("TOP FIVE HIGHEST-CONSUMING HOUSEHOLDS (MANUAL RANKING)\n")
        rep.write("-" * 78 + "\n")
        rep.write("{:<5} {:<8} {:<22} {:>11} {:>12} {:<10}\n".format(
            "Rank", "Meter", "Household", "Consumption", "Bill (R)", "Category"))
        rep.write("-" * 78 + "\n")
        rank = 1
        for entry in top_five:
            cons = entry[0]
            meter = entry[1]
            rec = valid_records[meter]
            bill = calculate_bill(cons)
            label = classify_consumption(cons)
            rep.write("{:<5} {:<8} {:<22} {:>11.1f} {:>12.2f} {:<10}\n".format(
                rank, rec["meter"], rec["name"], cons, bill, label))
            rank += 1

        # ---- Summary ----
        rep.write("\n")
        rep.write("SUMMARY\n")
        rep.write("-" * 78 + "\n")
        rep.write("Total valid households        : " + str(len(valid_records)) + "\n")
        rep.write("Total consumption (kL)        : {:.1f}\n".format(total_consumption))
        rep.write("Total revenue billed (R)      : {:.2f}\n".format(total_bill))
        rep.write("LOW consumption households    : " + str(low_count) + "\n")
        rep.write("MODERATE consumption households: " + str(moderate_count) + "\n")
        rep.write("HIGH consumption households   : " + str(high_count) + "\n")
        rep.write("=" * 78 + "\n")

    print("Report written to '" + REPORT_FILE + "'.")


def write_error_log(rejected):
    """Q8b: Write errors.log listing every rejected record and reason."""
    with open(ERROR_FILE, "w") as err:
        err.write("=" * 78 + "\n")
        err.write("REJECTED RECORDS - ERROR LOG\n")
        err.write("=" * 78 + "\n")
        err.write("Total rejected records: " + str(len(rejected)) + "\n")
        err.write("-" * 78 + "\n\n")

        for entry in rejected:
            err.write("Line " + str(entry["line_no"]) + ": ")
            err.write("REASON: " + entry["reason"] + "\n")
            err.write("  Raw: " + entry["raw"].strip() + "\n\n")

    print("Error log written to '" + ERROR_FILE + "'.")


# ---------------------------------------------------------------------
# SECTION 8: MAIN PROGRAM - ORCHESTRATION (Q2-Q10)
# ---------------------------------------------------------------------

def main():
    """Main driver: read -> validate -> calculate -> rank -> output."""

    print("=" * 60)
    print(" WATER BILLING MANAGEMENT SYSTEM - PROCESSING STARTED")
    print("=" * 60)

    # ---- Q1: Read input ----
    lines = read_input_file(INPUT_FILE)
    if len(lines) == 0:
        print("No data to process. Exiting.")
        return

    # ---- Q2/Q3: Validate and store valid records ----
    valid_records = {}
    rejected = []
    seen_meters = {}

    line_no = 0
    for raw_line in lines:
        line_no += 1

        # Skip completely blank lines (they are not records)
        if raw_line.strip() == "":
            continue

        fields = split_and_clean(raw_line)
        record, reason = validate_record(fields, seen_meters)

        if record is None:
            rejected.append({
                "line_no": line_no,
                "raw": raw_line,
                "reason": reason,
            })
        else:
            valid_records[record["meter"]] = record
            seen_meters[record["meter"]] = True

    # ---- Q4/Q5/Q6 are applied on demand above ----

    # ---- Q7: Manual top five ranking ----
    top_five = rank_top_five(valid_records)

    # ---- Q8: Write report and error log ----
    write_report(valid_records, top_five)
    write_error_log(rejected)

    # ---- Q8: Display accepted and rejected totals ----
    print("\n" + "-" * 60)
    print("PROCESSING COMPLETE")
    print("-" * 60)
    print("Accepted (valid) records : " + str(len(valid_records)))
    print("Rejected records         : " + str(len(rejected)))
    print("Top five ranked households:")
    rank = 1
    for entry in top_five:
        rec = valid_records[entry[1]]
        print("  " + str(rank) + ". " + rec["meter"] + " - " +
              rec["name"] + " : " + str(entry[0]) + " kL")
        rank += 1
    print("-" * 60)


# ---------------------------------------------------------------------
# SECTION 9: PROGRAM ENTRY POINT
# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()