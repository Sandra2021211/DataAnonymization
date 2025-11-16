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
    digits = value.replace("-", "")
    return "XXXX-XXXX-XXXX-" + digits[-4:]

def token_card(value):
    """Random credit/debit token"""
    return "TKN-CC-" + fake.bothify(text="??##")

def mask_account(value):
    """XXXXXXlast4"""
    if pd.isna(value):
        return value
    return "XXXXXX" + str(value)[-4:]

def token_account(value):
    """ACC-TKN-####"""
    return "ACC-TKN-" + fake.bothify(text="####")

def perturb_transaction(value):
    """Add noise ±50"""
    if pd.isna(value):
        return value
    try:
        v = float(value)
        noise = random.uniform(-50, 50)
        return round(v + noise, 2)
    except:
        return value

def generalize_salary(value):
    """Ranges (Lakhs): 857000 → 8–9L"""
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

def token_pan(value):
    """PAN Token"""
    return "TKN-PAN-" + fake.bothify(text="####")

def hash_pan(value):
    """Hash PAN → SHA256 (first 16 chars)"""
    if pd.isna(value):
        return value
    return hashlib.sha256(value.encode()).hexdigest()[:16]


# ---------------------------------
# Technique Mapping (Corrected)
# ---------------------------------
TECHNIQUES = {
    "masking": {
        "card_number": mask_card,
        "bank_account": mask_account
    },
    "tokenization": {
        "card_number": token_card,
        "bank_account": token_account,
        "pan": token_pan
    },
    "perturbation": {
        "transaction_amount": perturb_transaction,
        "salary": perturb_salary
    },
    "generalization": {
        "salary": generalize_salary
    },
    "hashing": {
        "pan": hash_pan
    }
}

# ---------------------------------
# Main Anonymization Function
# ---------------------------------
def anonymize(input_csv, column, technique):
    df = pd.read_csv(input_csv)

    column_key = column.lower()
    technique_key = technique.lower()

    if technique_key not in TECHNIQUES:
        raise ValueError(f"Invalid technique '{technique}'")

    func = TECHNIQUES[technique_key].get(column_key)
    if func is None:
        raise ValueError(f"Technique '{technique}' not supported for column '{column}'")

    # Apply chosen anonymization
    df[column] = df[column].apply(func)

    output_file = "outputFinancial.csv"
    df.to_csv(output_file, index=False)

    print(f"\n✔ Output saved to: {output_file}")


# ---------------------------------
# CLI
# ---------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python FinancialInfo.py <input_csv> <column_name> <technique>")
        sys.exit(1)

    anonymize(sys.argv[1], sys.argv[2], sys.argv[3])
