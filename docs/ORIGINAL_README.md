# Automatic EDA Assistant

Generates a reproducible Markdown exploratory-data-analysis report with dataset health checks, descriptive statistics, correlations, and anomaly counts.

## Usage
```bash
pip install -r requirements.txt
python src/eda_report.py sample/data.csv --output outputs/report.md
```

The report includes observations that are derived from transparent rules so readers can verify them.
