import argparse
import csv
from typing import List, Dict
from tabulate import tabulate


def parse_filter_condition(condition: str) -> tuple:
    """
    Parses a filter condition string into column, operator, and value.
    Example: "price>500" -> ("price", ">", "500")
    """
    for op in [">", "<", "="]:
        if op in condition:
            column, value = condition.split(op)
            return column.strip(), op, value.strip()
    raise ValueError(f"Invalid filter condition: {condition}")


def apply_filter(data: List[Dict], condition: str) -> List[Dict]:
    """
    Applies a filter condition to the data.
    """
    column, op, value = parse_filter_condition(condition)

    def compare(row):
        row_value = row[column]
        # Convert to float if the value is numeric
        try:
            row_value = float(row_value)
            value_converted = float(value)
        except ValueError:
            pass  # Keep as string for text comparison

        if op == ">":
            return row_value > value_converted
        elif op == "<":
            return row_value < value_converted
        elif op == "=":
            return row_value == value_converted
        else:
            raise ValueError(f"Unsupported operator: {op}")

    return [row for row in data if compare(row)]


def aggregate_data(data: List[Dict], column: str, agg_type: str) -> float:
    """
    Performs aggregation on a numeric column.
    """
    values = [float(row[column]) for row in data]
    if agg_type == "avg":
        return sum(values) / len(values)
    elif agg_type == "min":
        return min(values)
    elif agg_type == "max":
        return max(values)
    else:
        raise ValueError(f"Unsupported aggregation type: {agg_type}")


def load_csv(file_path: str) -> List[Dict]:
    """
    Loads data from a CSV file into a list of dictionaries.
    Converts numeric columns to floats.
    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # Detect numeric columns and convert values to float
    numeric_columns = {"price", "rating"}  # Define numeric columns explicitly
    for row in data:
        for col in numeric_columns:
            if col in row:
                row[col] = float(row[col])

    return data


def main():
    parser = argparse.ArgumentParser(description="CSV Data Processor")
    parser.add_argument("--file", required=True, help="Path to the CSV file")
    parser.add_argument(
        "--where",
        help='Filter condition, e.g., "price>500" or "brand=apple"',
    )
    parser.add_argument(
        "--aggregate",
        help='Aggregation operation, e.g., "rating=avg" or "price=max"',
    )

    args = parser.parse_args()

    # Load data from CSV
    data = load_csv(args.file)

    # Apply filter if specified
    if args.where:
        data = apply_filter(data, args.where)

    # Perform aggregation if specified
    if args.aggregate:
        column, agg_type = args.aggregate.split("=")
        result = aggregate_data(data, column, agg_type)
        print(tabulate([[result]], headers=[agg_type]))
    else:
        # Display filtered data as a table
        print(tabulate(data, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()