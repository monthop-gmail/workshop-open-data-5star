"""
Data Validation for AI-Ready Energy Statistics
Level 6: ตรวจสอบคุณภาพข้อมูลก่อนใช้กับ AI/ML

รัน: python validation.py
"""

import json
import csv
from pathlib import Path
from typing import Any


# Validation Rules
VALID_REGION_CODES = {"TH-C", "TH-N", "TH-NE", "TH-S", "TH-E"}
MIN_YEAR = 2500
MAX_YEAR = 2600


class ValidationError(Exception):
    """Custom validation error"""
    pass


class DataValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.records_checked = 0

    def validate_record(self, record: dict, row_num: int) -> bool:
        """ตรวจสอบ record เดียว"""
        is_valid = True

        # Required fields
        required_fields = [
            "region_code", "region_th", "region_en",
            "year", "consumption_gwh", "customers", "growth_rate"
        ]

        for field in required_fields:
            if field not in record or record[field] is None or record[field] == "":
                self.errors.append(f"Row {row_num}: Missing required field '{field}'")
                is_valid = False

        if not is_valid:
            return False

        # Region code validation
        if record["region_code"] not in VALID_REGION_CODES:
            self.errors.append(
                f"Row {row_num}: Invalid region_code '{record['region_code']}'. "
                f"Must be one of {VALID_REGION_CODES}"
            )
            is_valid = False

        # Year validation
        try:
            year = int(record["year"])
            if not (MIN_YEAR <= year <= MAX_YEAR):
                self.errors.append(
                    f"Row {row_num}: Year {year} out of range [{MIN_YEAR}, {MAX_YEAR}]"
                )
                is_valid = False
        except (ValueError, TypeError):
            self.errors.append(f"Row {row_num}: Invalid year value '{record['year']}'")
            is_valid = False

        # Consumption validation
        try:
            consumption = float(record["consumption_gwh"])
            if consumption <= 0:
                self.errors.append(
                    f"Row {row_num}: consumption_gwh must be positive, got {consumption}"
                )
                is_valid = False
            if consumption > 100000:  # Sanity check
                self.warnings.append(
                    f"Row {row_num}: consumption_gwh={consumption} seems unusually high"
                )
        except (ValueError, TypeError):
            self.errors.append(
                f"Row {row_num}: Invalid consumption_gwh value '{record['consumption_gwh']}'"
            )
            is_valid = False

        # Customers validation
        try:
            customers = int(record["customers"])
            if customers <= 0:
                self.errors.append(
                    f"Row {row_num}: customers must be positive, got {customers}"
                )
                is_valid = False
        except (ValueError, TypeError):
            self.errors.append(
                f"Row {row_num}: Invalid customers value '{record['customers']}'"
            )
            is_valid = False

        # Growth rate validation
        try:
            growth = float(record["growth_rate"])
            if not (-100 <= growth <= 100):
                self.errors.append(
                    f"Row {row_num}: growth_rate {growth} out of range [-100, 100]"
                )
                is_valid = False
        except (ValueError, TypeError):
            self.errors.append(
                f"Row {row_num}: Invalid growth_rate value '{record['growth_rate']}'"
            )
            is_valid = False

        self.records_checked += 1
        return is_valid

    def validate_jsonl(self, filepath: str) -> bool:
        """ตรวจสอบไฟล์ JSONL"""
        print(f"\nValidating JSONL: {filepath}")
        all_valid = True

        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                try:
                    record = json.loads(line.strip())
                    if not self.validate_record(record, i):
                        all_valid = False
                except json.JSONDecodeError as e:
                    self.errors.append(f"Row {i}: Invalid JSON - {e}")
                    all_valid = False

        return all_valid

    def validate_csv(self, filepath: str) -> bool:
        """ตรวจสอบไฟล์ CSV"""
        print(f"\nValidating CSV: {filepath}")
        all_valid = True

        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, record in enumerate(reader, 2):  # Start at 2 (header is row 1)
                if not self.validate_record(record, i):
                    all_valid = False

        return all_valid

    def check_duplicates(self, records: list) -> bool:
        """ตรวจสอบข้อมูลซ้ำ"""
        seen_keys = set()
        has_duplicates = False

        for i, record in enumerate(records, 1):
            key = (record.get("region_code"), record.get("year"))
            if key in seen_keys:
                self.errors.append(
                    f"Row {i}: Duplicate record for region={key[0]}, year={key[1]}"
                )
                has_duplicates = True
            seen_keys.add(key)

        return not has_duplicates

    def check_completeness(self, records: list) -> bool:
        """ตรวจสอบความครบถ้วนของข้อมูล"""
        regions_found = {r.get("region_code") for r in records}
        missing_regions = VALID_REGION_CODES - regions_found

        if missing_regions:
            self.warnings.append(f"Missing data for regions: {missing_regions}")
            return False

        return True

    def print_report(self):
        """แสดงรายงานผลการตรวจสอบ"""
        print("\n" + "=" * 60)
        print("DATA VALIDATION REPORT")
        print("=" * 60)

        print(f"\nRecords checked: {self.records_checked}")

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   - {error}")
        else:
            print("\n✅ No errors found!")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   - {warning}")

        print("\n" + "=" * 60)

        if self.errors:
            print("RESULT: ❌ FAILED - Data is NOT AI-ready")
            return False
        else:
            print("RESULT: ✅ PASSED - Data is AI-ready!")
            return True


def main():
    """Main validation routine"""
    data_dir = Path(__file__).parent / "data"

    validator = DataValidator()

    # Validate JSONL
    jsonl_path = data_dir / "energy_stats.jsonl"
    if jsonl_path.exists():
        validator.validate_jsonl(str(jsonl_path))

    # Validate CSV
    csv_path = data_dir / "energy_stats_clean.csv"
    if csv_path.exists():
        validator.validate_csv(str(csv_path))

    # Load records for additional checks
    records = []
    if jsonl_path.exists():
        with open(jsonl_path, "r", encoding="utf-8") as f:
            records = [json.loads(line) for line in f]

    # Check duplicates and completeness
    if records:
        validator.check_duplicates(records)
        validator.check_completeness(records)

    # Print report
    is_valid = validator.print_report()

    return 0 if is_valid else 1


if __name__ == "__main__":
    exit(main())
