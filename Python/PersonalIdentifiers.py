import pandas as pd
from faker import Faker
import hashlib
import random
import sys
import os

fake = Faker()

# -----------------------------
# Personal Identifier Functions
# -----------------------------

def mask_name(value):
    if pd.isna(value):
        return value
    parts = value.split()
    masked_parts = []
    for p in parts:
        if len(p) > 1:
            masked_parts.append(p[0] + "*" * (len(p)-1))
        else:
            masked_parts.append("*")
    return " ".join(masked_parts)

def pseudo_name(value):
    return f"user_{fake.random_int(1000, 9999)}"

def token_name(value):
    return "TKN-" + fake.bothify(text="??##??")

def generalize_dob(value):
    """Convert DD-MM-YYYY → MM/YYYY"""
    if pd.isna(value):
        return value
    try:
        day, month, year = value.split("-")
        return f"{month}/{year}"
    except:
        return value

def suppress_dob(value):
    return "[Hidden]"

def generalize_address(value):
    """Return only last two components: City, Country"""
    if pd.isna(value):
        return value
    parts = value.split()
    if len(parts) >= 2:
        return " ".join(parts[-1:]).strip()
    return value

def suppress_address(value):
    """Remove house number / first components"""
    if pd.isna(value):
        return value
    parts = value.split()
    return " ".join(parts[1:]).strip() if len(parts) > 1 else value

def mask_phone(value):
    """Keep first 6 digits, mask rest"""
    if pd.isna(value):
        return value
    value=str(value)
    return value[:6] + "XXXX"

def token_phone(value):
    return "PHN-" + fake.bothify(text="##??##")

def pseudo_email(value):
    return f"user_{fake.random_int(1000,9999)}@anonmail.com"

def token_email(value):
    return "EMAIL-" + fake.bothify(text="??##??")

def token_generic(value):
    return "TKN-" + fake.bothify(text="????##")

def hash_generic(value):
    return hashlib.sha256(value.encode()).hexdigest()[:16]


# -----------------------------
# Technique Mapping
# -----------------------------
TECHNIQUES = {
    "masking": {
        "name": mask_name,
        "phone": mask_phone
    },
    "pseudonymization": {
        "name": pseudo_name,
        "email": pseudo_email
    },
    "tokenization": {
        "name": token_name,
        "phone": token_phone,
        "email": token_email,
        "aadhar": token_generic,
        "pan": token_generic,
        "passport": token_generic,
        "ssn": token_generic
    },
    "generalization": {
        "dob": generalize_dob,
        "address": generalize_address
    },
    "suppression": {
        "dob": suppress_dob,
        "address": suppress_address
    },
    "hashing": {
        "aadhar": hash_generic,
        "pan": hash_generic,
        "passport": hash_generic,
        "ssn": hash_generic
    }
}


# -----------------------------
# Main Anonymization Function
# -----------------------------
def anonymize(input_csv, column, technique):
    df = pd.read_csv(input_csv)

    technique = technique.lower()
    column_key = column.lower()

    if technique not in TECHNIQUES:
        raise ValueError("Invalid technique")

    func = TECHNIQUES[technique].get(column_key, None)
    if func is None:
        raise ValueError(f"Technique '{technique}' not supported for column '{column_key}'")

    # -----------------------------
    # Replace original column
    # -----------------------------
    df[column] = df[column].apply(func)

    output_file = "outputPersonal.csv"
    df.to_csv(output_file, index=False)

    print(f"\nOutput saved to: {output_file}")


# -----------------------------
# CLI Execution
# -----------------------------
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python PersonalIdentifiers.py <input_csv> <column_name> <technique>")
        sys.exit(1)

    anonymize(sys.argv[1], sys.argv[2], sys.argv[3])
