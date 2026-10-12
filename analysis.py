import sqlite3
import pandas as pd
from pathlib import Path


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "sales.db"


def get_connection():
    """Connect to SQLite database."""
    return sqlite3.connect(DATABASE_PATH)


def run_analysis():

    connection = get_connection()

    print("\n========== SALES ANALYSIS ==========\n")

    # 1. Total revenue
    query = """
    SELECT SUM(Revenue) AS Total_Revenue
    FROM sales;
    """

    result = pd.read_sql_query(query, connection)
    print("Total Revenue:")
    print(result)

    # 2. Revenue by product
    query = """
    SELECT Product,
           SUM(Revenue) AS Revenue
    FROM sales
    GROUP BY Product
    ORDER BY Revenue DESC;
    """

    result = pd.read_sql_query(query, connection)

    print("\nRevenue by Product:")
    print(result)

    # 3. Revenue by city
    query = """
    SELECT City,
           SUM(Revenue) AS Revenue
    FROM sales
    GROUP BY City
    ORDER BY Revenue DESC;
    """

    result = pd.read_sql_query(query, connection)

    print("\nRevenue by City:")
    print(result)

    # 4. Revenue by category
    query = """
    SELECT Category,
           SUM(Revenue) AS Revenue
    FROM sales
    GROUP BY Category
    ORDER BY Revenue DESC;
    """

    result = pd.read_sql_query(query, connection)

    print("\nRevenue by Category:")
    print(result)

    # 5. Customer revenue
    query = """
    SELECT CustomerID,
           SUM(Revenue) AS Revenue
    FROM sales
    GROUP BY CustomerID
    ORDER BY Revenue DESC;
    """

    result = pd.read_sql_query(query, connection)

    print("\nRevenue by Customer:")
    print(result)

    connection.close()


if __name__ == "__main__":
    run_analysis()