from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PYTHON_DIR = ROOT / "Python"
sys.path.insert(0, str(PYTHON_DIR))

import FinancialInfo
import PersonalIdentifiers

if __name__ == "__main__":
    financial_input = ROOT / "SQL" / "inputFinancial.csv"
    personal_input = ROOT / "SQL" / "inputPersonal.csv"

    FinancialInfo.anonymize(str(financial_input), "card_number", "masking", str(ROOT / "outputFinancial.csv"))
    PersonalIdentifiers.anonymize(str(personal_input), "name", "masking", str(ROOT / "outputPersonal.csv"))
    print("Example anonymization completed.")
