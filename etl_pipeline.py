import pandas as pd
from pathlib import Path


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR / "data" / "raw" / "sales_data.csv"
PROCESSED_DATA = BASE_DIR / "data" / "processed" / "clean_sales_data.csv"


def load_data():
    """Load raw sales data."""
    df = pd.read_csv(RAW_DATA)
    print("Raw data loaded successfully!")
    print(f"Rows: {len(df)}")
    return df


def clean_data(df):
    """Clean and transform sales data."""

    # Remove duplicate records
    df = df.drop_duplicates()

    # Convert date column
    df["Date"] = pd.to_datetime(df["Date"])

    # Handle missing values
    df["Quantity"] = df["Quantity"].fillna(0)
    df["Price"] = df["Price"].fillna(df["Price"].median())

    # Create revenue column
    df["Revenue"] = df["Quantity"] * df["Price"]

    return df


def save_data(df):
    """Save cleaned data."""
    PROCESSED_DATA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA, index=False)

    print("Cleaned data saved successfully!")
    print(f"Saved to: {PROCESSED_DATA}")


if __name__ == "__main__":
    data = load_data()
    cleaned_data = clean_data(data)
    save_data(cleaned_data)

    print("\nETL pipeline completed successfully!")