import sqlite3
import pandas as pd
from pathlib import Path


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA = (
    BASE_DIR / "data" / "processed" / "clean_sales_data.csv"
)

DATABASE_PATH = (
    BASE_DIR / "database" / "sales.db"
)


def create_database():
    """Create SQLite database and load cleaned sales data."""

    # Read cleaned data
    df = pd.read_csv(PROCESSED_DATA)

    # Create database folder if it doesn't exist
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to SQLite
    connection = sqlite3.connect(DATABASE_PATH)

    # Store data in sales table
    df.to_sql(
        "sales",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

    print("Database created successfully!")
    print(f"Database location: {DATABASE_PATH}")
    print(f"Records inserted: {len(df)}")


if __name__ == "__main__":
    create_database()