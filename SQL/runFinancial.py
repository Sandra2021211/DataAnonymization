import sqlite3
import pandas as pd
import sys
import os

def anonymize_sql(input_csv, column, technique):

    # Load CSV into pandas
    df = pd.read_csv(input_csv)

    # Connect to in-memory SQLite DB
    conn = sqlite3.connect(":memory:")

    # Load CSV into SQL table called 'financial'
    df.to_sql("financial", conn, index=False, if_exists="replace")

    # Load the SQL anonymizer file
    with open("anonymizerFinancial.sql", "r") as file:
        sql_script = file.read()

    # Replace placeholders with quotes so SQL evaluates correctly
    sql_script = sql_script.replace(":column", f"'{column}'")
    sql_script = sql_script.replace(":technique", f"'{technique}'")

    # Execute the SQL script
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()

    # Read updated results back into pandas
    updated_df = pd.read_sql_query("SELECT * FROM financial", conn)

    # Output file
    output_file = "outputFinancial.csv"

    # Save output CSV
    updated_df.to_csv(output_file, index=False)

    print(f"\n✔ Output generated: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python runFinancial.py <input_csv> <column> <technique>")
        sys.exit(1)

    anonymize_sql(sys.argv[1], sys.argv[2], sys.argv[3])
