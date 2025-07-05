import csv

import pytest

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import load_csv, apply_filter, aggregate_data


@pytest.fixture
def sample_data():
    return [
        {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
        {"name": "galaxy s23 ultra", "brand": "samsung", "price": "1199", "rating": "4.8"},
        {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
    ]


def test_load_csv(tmp_path, sample_data):
    # Create a temporary CSV file
    csv_file = tmp_path / "test.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sample_data[0].keys())
        writer.writeheader()
        writer.writerows(sample_data)

    # Load the CSV file
    loaded_data = load_csv(csv_file)
    assert loaded_data == sample_data


def test_apply_filter(sample_data):
    # Filter by price > 500
    filtered_data = apply_filter(sample_data, "price>500")
    assert len(filtered_data) == 2
    assert all(float(row["price"]) > 500 for row in filtered_data)

    # Filter by brand = apple
    filtered_data = apply_filter(sample_data, "brand=apple")
    assert len(filtered_data) == 1
    assert filtered_data[0]["brand"] == "apple"


def test_aggregate_data(sample_data):
    # Calculate average rating
    avg_rating = aggregate_data(sample_data, "rating", "avg")
    assert avg_rating == 4.766666666666667

    # Calculate minimum price
    min_price = aggregate_data(sample_data, "price", "min")
    assert min_price == 199

    # Calculate maximum rating
    max_rating = aggregate_data(sample_data, "rating", "max")
    assert max_rating == 4.9


def test_invalid_aggregation(sample_data):
    with pytest.raises(ValueError):
        aggregate_data(sample_data, "rating", "invalid")


def test_invalid_filter():
    with pytest.raises(ValueError):
        apply_filter([], "invalid_condition")