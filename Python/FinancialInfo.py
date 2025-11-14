import pandas as pd
from faker import Faker
import hashlib
import random
import sys

fake = Faker()

# ---------------------------------
# Financial Functions
# ---------------------------------

def mask_card(value):
    """XXXX-XXXX-XXXX-last4"""
    if pd.isna(value):
        return value
    value = value.replace("-", "")
    return "XXXX-XXXX-XXXX-" + value[-4:]

def token_card(value):
    return "TKN-CC-" + fake.bothify(text="??##")

def mask_account(value):
    """XXXXXXlast4"""
    if pd.isna(value):
        return value
    return "XXXXXX" + value[-4:]

def token_account(value):
    return "ACC-TKN-" + fake.bothify(text="####")

def perturb_transaction(value):
    """Add small noise e.g., ±50"""
    if pd.isna(value):
        return value
    try:
        value = float(value)
        noise = random.uniform(-50, 50)
        return round(value + noise, 2)
    except:
        return value

def generalize_salary(value):
    """₹857000 → 8–9L"""
    if pd.isna(value):
        return value
    try:
        v = int(value)
        lakhs = v // 100000
        return f"{lakhs}–{lakhs+1}L"
    except:
        return value

def perturb_salary(value):
    """Add noise ±5000"""
    if pd.isna(value):
        return value
    try:
        v = int(value)
        noise = random.randint(-5000, 5000)
        return v + noise
    except:
        return value

def token_taxid(value):
    return "TKN-PAN-" + fake.bothify(text="####")

def hash_taxid(value):
    return hashlib.sha256(value.encode()).hexdigest()[:16]

# ---------------------------------
# Technique Mapping
# ---------------------------------
TECHNIQUES = {
    "masking": {
        "credit_card": mask_card,
        "debit_card": mask_card,
        "bank_account": mask_account
    },
    "tokenization": {
        "credit_card": token_card,
        "debit_card": token_card,
        "bank_account": token_account,
        "tax_id": token_taxid
    },
    "perturbation": {
        "transaction_amount": perturb_transaction,
        "salary": perturb_salary
    },
    "generalization": {
        "salary": generalize_salary
    },
    "hashing": {
        "tax_id": hash_taxid
    }
}

# ---------------------------------
# Main Anonymization Function
# ---------------------------------
def anonymize(input_csv, column, technique):
    df = pd.read_csv(input_csv)

    technique = technique.lower()
    column_key = column.lower()

    if technique not in TECHNIQUES:
        raise ValueError("Invalid technique")

    func = TECHNIQUES[technique].get(column_key, None)
    if func is None:
        raise ValueError(f"Technique '{technique}' not supported for column '{column_key}'")

    # Replace original column
    df[column] = df[column].apply(func)

    output_file = "outputFinancial.csv"
    df.to_csv(output_file, index=False)

    print(f"\nOutput saved to: {output_file}")


# ---------------------------------
# CLI
# ---------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python FinancialInfo.py <input_csv> <column_name> <technique>")
        sys.exit(1)

    anonymize(sys.argv[1], sys.argv[2], sys.argv[3])
