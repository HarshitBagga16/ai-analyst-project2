import pandas as pd


def analyze_csv(file):

    df = pd.read_csv(file)

    # -------------------------
    # Basic preprocessing
    # -------------------------

    df["date"] = pd.to_datetime(df["date"] , errors="coerce")

    df["revenue"] = df["quantity"] * df["unit_price"]

    # -------------------------
    # Dataset information
    # -------------------------

    shape = df.shape

    columns = df.columns.tolist()

    data_types = df.dtypes.astype(str).to_dict()

    missing_values = df.isnull().sum().to_dict()

    # -------------------------
    # Statistics
    # -------------------------

    statistics = df.describe().to_dict()

    # -------------------------
    # IQR
    # -------------------------

    numeric_df = df.select_dtypes(include="number")

    Q1 = numeric_df.quantile(0.25)
    Q3 = numeric_df.quantile(0.75)

    IQR = Q3 - Q1

    # -------------------------
    # Business analysis
    # -------------------------

    total_revenue = df["revenue"].sum()

    average_revenue = df["revenue"].mean()

    total_quantity = df["quantity"].sum()

    revenue_by_region = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    revenue_by_product = (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    monthly_revenue = (
        df.groupby(df["date"].dt.to_period("M"))["revenue"]
        .sum()
    )

    # -------------------------
    # Important findings
    # -------------------------

    highest_region = revenue_by_region.idxmax()

    highest_region_revenue = revenue_by_region.max()

    highest_product = revenue_by_product.idxmax()

    highest_product_revenue = revenue_by_product.max()

    # -------------------------
    # Return everything
    # -------------------------

    results = {

        "dataset_info": {
            "shape": shape,
            "columns": columns,
            "data_types": data_types,
            "missing_values": missing_values,
        },

        "statistics": statistics,

        "IQR": IQR.to_dict(),

        "business_analysis": {
            "total_revenue": total_revenue,
            "average_revenue": average_revenue,
            "total_quantity": total_quantity,

            "revenue_by_region":
                revenue_by_region.to_dict(),

            "revenue_by_product":
                revenue_by_product.to_dict(),

            "monthly_revenue":
                {
                    str(k): float(v)
                    for k, v in monthly_revenue.items()
                },

            "highest_region":
                highest_region,

            "highest_region_revenue":
                highest_region_revenue,

            "highest_product":
                highest_product,

            "highest_product_revenue":
                highest_product_revenue,
        }
    }

    return df, results