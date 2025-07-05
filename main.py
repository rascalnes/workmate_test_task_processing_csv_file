import argparse
import csv
from typing import List, Dict
from tabulate import tabulate


def parse_filter_condition(condition: str) -> tuple:
    for op in [">", "<", "="]:
        if op in condition:
            column, value = condition.split(op)
            return column.strip(), op, value.strip()
    raise ValueError(f"Invalid filter condition: {condition}")


def apply_filter(data: List[Dict], condition: str) -> List[Dict]:
    column, op, value = parse_filter_condition(condition)

    def compare(row):
        row_value = row[column]
        value_converted = value

        if column in {"price", "rating"}:
            try:
                row_value = float(row_value)
                value_converted = float(value_converted)
            except ValueError:
                raise ValueError(f"Invalid numeric value in filter: {value}")

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
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    numeric_columns = {"price", "rating"}
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

    data = load_csv(args.file)

    if args.where:
        data = apply_filter(data, args.where)

    if args.aggregate:
        column, agg_type = args.aggregate.split("=")
        result = aggregate_data(data, column, agg_type)
        print(tabulate([[result]], headers=[agg_type]))
    else:
        print(tabulate(data, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()