import sqlite3
import pandas as pd
import sys
import os

def anonymize_sql(input_csv, column, technique):

    # Load CSV into pandas
    df = pd.read_csv(input_csv)

    # Connect to in-memory SQLite DB
    conn = sqlite3.connect(":memory:")

    # Load the CSV into SQL table
    df.to_sql("personal", conn, index=False, if_exists="replace")

    # Load the SQL script
    with open("anonymizerPersonal.sql", "r") as file:
        sql_script = file.read()

    # Replace placeholders
    sql_script = sql_script.replace(":column", f"'{column}'")
    sql_script = sql_script.replace(":technique", f"'{technique}'")

    # Execute SQL
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()

    # Read updated table back into pandas
    updated_df = pd.read_sql_query("SELECT * FROM personal", conn)

    # Generate output filename
    base_name = os.path.splitext(input_csv)[0]
    output_file = "outputPersonal.csv"

    # Save output CSV
    updated_df.to_csv(output_file, index=False)

    print(f"\n✔ Output generated: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run_sql_anonymizer.py <input_csv> <column> <technique>")
        sys.exit(1)

    anonymize_sql(sys.argv[1], sys.argv[2], sys.argv[3])
