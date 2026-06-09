# Rescue Dog Analytics Dashboard

An end-to-end analytics project built to help a dog rescue organization track operations, identify trends, and improve decision-making.

## Project Overview

This project ingests rescue dog data from Google Sheets, cleans and standardizes inconsistent records using Python, and prepares the data for reporting in Tableau.

The dashboard provides insight into:
- Current dogs available for adoption
- Historical adoption outcomes
- Length of stay for active dogs
- Breed, age, and color trends
- Foster and placement capacity
- Data quality issues requiring attention

## Tech Stack

- Python
- pandas
- NumPy
- Google Sheets
- GitHub
- Tableau Public

## Data Pipeline

```text
Google Sheets
    ↓
Python ETL
    ↓
Data Cleaning & Standardization
    ↓
Calculated Metrics
    ↓
Cleaned CSV
    ↓
Tableau Dashboard
```

## Data Cleaning Performed

Examples of transformations include:

- Combined current and adopted dog datasets
- Standardized breed values
- Standardized color values
- Converted age values into numeric years
- Created age groups and weight groups
- Categorized intake and placement locations
- Calculated days in rescue for active dogs
- Added breed groups and color categories
- Preserved historical records while identifying current availability

## Key Metrics

The dashboard tracks metrics such as:

- Total dogs served
- Dogs currently available
- Total adopted dogs
- Average days in rescue
- Longest-stay dogs
- Intake source distribution
- Breed group distribution
- Foster placement distribution

## Project Structure

```text
rescue-dashboard/
├── clean_rescue_data.py
├── cleaned_rescue_data.csv
├── requirements.txt
└── README.md
```

## Future Enhancements

- Automate refreshes using GitHub Actions
- Export cleaned data directly back to Google Sheets
- Add adoption date tracking
- Build a "Dogs Needing Attention" dashboard
- Implement geographic intake visualizations

## Dashboard

Tableau dashboard link:
*Coming soon*

## About

This project was inspired by volunteer work with a dog rescue organization and was designed to demonstrate practical business analytics skills using real-world, imperfect data.