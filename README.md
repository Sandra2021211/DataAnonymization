# Data Anonymization

A small data privacy project that demonstrates common anonymization and masking techniques for financial and personal data using Python and SQL.

## What this project does

This repository shows how to transform sensitive values in CSV data using techniques such as:

- masking
- tokenization
- pseudonymization
- generalization
- suppression
- hashing

It includes both Python-based implementations and SQL-based approaches, making it useful for demonstrating data handling, privacy-preserving transformations, and basic ETL-style workflows.

## Project structure

- Python/FinancialInfo.py — financial data anonymization logic
- Python/PersonalIdentifiers.py — personal identifier anonymization logic
- SQL/ — SQL-based anonymization examples and sample inputs
- tests/ — lightweight regression tests
- examples/usage_example.py — quick example script

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Quick start

### Python example

```bash
python Python/FinancialInfo.py SQL/inputFinancial.csv card_number masking
python Python/PersonalIdentifiers.py SQL/inputPersonal.csv name masking
```

### Run the example script

```bash
python examples/usage_example.py
```

### Run tests

```bash
pytest -q
```

## Portfolio value

This project is useful for showcasing:

- Python scripting and data processing
- SQL-based transformations
- practical understanding of privacy concepts
- simple CLI and file-processing workflows

## Future improvements

Possible next steps include:

- adding a web interface or dashboard
- supporting JSON/Parquet input formats
- adding stronger validation and logging
- integrating a real database instead of CSV-based examples