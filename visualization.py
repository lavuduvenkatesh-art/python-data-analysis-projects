import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR / "data" / "processed" / "clean_sales_data.csv"
)


def create_visualizations():

    df = pd.read_csv(DATA_PATH)

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"])

    # Create charts folder
    charts_folder = BASE_DIR / "data" / "processed" / "charts"
    charts_folder.mkdir(parents=True, exist_ok=True)

    # --------------------------------
    # 1. Revenue by Product
    # --------------------------------

    product_sales = (
        df.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))
    product_sales.plot(kind="bar")
    plt.title("Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        charts_folder / "revenue_by_product.png"
    )

    plt.close()

    # --------------------------------
    # 2. Revenue by City
    # --------------------------------

    city_sales = (
        df.groupby("City")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))
    city_sales.plot(kind="bar")
    plt.title("Revenue by City")
    plt.xlabel("City")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        charts_folder / "revenue_by_city.png"
    )

    plt.close()

    # --------------------------------
    # 3. Monthly Revenue
    # --------------------------------

    monthly_sales = (
        df.groupby(df["Date"].dt.to_period("M"))["Revenue"]
        .sum()
    )

    monthly_sales.index = monthly_sales.index.astype(str)

    plt.figure(figsize=(10, 6))
    monthly_sales.plot(kind="line", marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        charts_folder / "monthly_revenue.png"
    )

    plt.close()

    print("All visualizations created successfully!")
    print(f"Charts saved in: {charts_folder}")


if __name__ == "__main__":
    create_visualizations()