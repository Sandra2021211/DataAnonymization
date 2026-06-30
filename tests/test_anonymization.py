import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Python"))

import FinancialInfo
import PersonalIdentifiers


def test_financial_anonymization_writes_output(tmp_path):
    input_csv = tmp_path / "financial.csv"
    output_csv = tmp_path / "masked.csv"
    input_csv.write_text(
        "card_number,bank_account\n4111111111111111,1234567890\n",
        encoding="utf-8",
    )

    FinancialInfo.anonymize(str(input_csv), "card_number", "masking", str(output_csv))

    assert output_csv.exists()
    df = pd.read_csv(output_csv)
    assert df.loc[0, "card_number"].startswith("XXXX-XXXX-XXXX-")
    assert str(df.loc[0, "bank_account"]) == "1234567890"


def test_personal_anonymization_writes_output(tmp_path):
    input_csv = tmp_path / "personal.csv"
    output_csv = tmp_path / "masked_personal.csv"
    input_csv.write_text(
        "name,email\nJane Doe,jane@example.com\n",
        encoding="utf-8",
    )

    PersonalIdentifiers.anonymize(str(input_csv), "name", "masking", str(output_csv))

    assert output_csv.exists()
    df = pd.read_csv(output_csv)
    assert df.loc[0, "name"] == "J*** D**"
    assert df.loc[0, "email"] == "jane@example.com"
