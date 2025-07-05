# workmate_test_task_processing_csv_file

# CSV Data Processor

A Python script to process CSV files with filtering and aggregation capabilities.

## Usage

### All products
```bash
python main.py --file products.csv
```

### xiaomi products
```bash
python main.py --file products.csv --where "brand=xiaomi"
```
### apple products
```bash
python main.py --file products.csv --where "brand=apple"
```
### raiting avg
```bash
python main.py --file products.csv --aggregate "rating=avg"
```

### rating xiaomi min
```bash
python main.py --file products.csv --where "brand=xiaomi" --aggregate "rating=min"
```

### rating xiaomi max
```bash
python main.py --file products.csv --where "brand=xiaomi" --aggregate "rating=max"
```

### rating apple avg
```bash
python main.py --file products.csv --where "brand=apple" --aggregate "rating=avg"
```







