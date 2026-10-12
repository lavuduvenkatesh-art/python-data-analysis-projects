import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR / "data" / "processed" / "clean_sales_data.csv"
)

MODEL_OUTPUT = (
    BASE_DIR / "data" / "processed" / "customer_segments.csv"
)


def create_customer_segments():

    # Load cleaned data
    df = pd.read_csv(DATA_PATH)

    # Convert date
    df["Date"] = pd.to_datetime(df["Date"])

    # Reference date
    reference_date = df["Date"].max()

    # Create RFM table
    rfm = df.groupby("CustomerID").agg(
        Recency=("Date", lambda x:
                 (reference_date - x.max()).days),

        Frequency=("OrderID", "count"),

        Monetary=("Revenue", "sum")
    ).reset_index()

    print("\n========== RFM ANALYSIS ==========\n")
    print(rfm)

    # Select features
    features = [
        "Recency",
        "Frequency",
        "Monetary"
    ]

    X = rfm[features]

    # Standardize data
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # K-Means clustering
    kmeans = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    rfm["Cluster"] = kmeans.fit_predict(X_scaled)

    # Give meaningful customer segment names
    cluster_summary = (
        rfm.groupby("Cluster")[features]
        .mean()
    )

    # Rank clusters by monetary value
    cluster_order = (
        cluster_summary["Monetary"]
        .sort_values()
        .index
        .tolist()
    )

    segment_names = {
        cluster_order[0]: "Low Value",
        cluster_order[1]: "Medium Value",
        cluster_order[2]: "High Value"
    }

    rfm["Segment"] = rfm["Cluster"].map(segment_names)

    # Save results
    rfm.to_csv(MODEL_OUTPUT, index=False)

    print("\n========== CUSTOMER SEGMENTS ==========\n")
    print(rfm)

    print("\nCustomer segment counts:")
    print(rfm["Segment"].value_counts())

    print("\nCustomer segmentation completed successfully!")
    print(f"Saved to: {MODEL_OUTPUT}")


if __name__ == "__main__":
    create_customer_segments()