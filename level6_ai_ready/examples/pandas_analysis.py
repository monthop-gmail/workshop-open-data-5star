"""
Example: Data Analysis with Pandas
Level 6: AI-Ready Government Data

รัน: pip install pandas pyarrow matplotlib
     python pandas_analysis.py
"""

import pandas as pd
from pathlib import Path


def load_data():
    """โหลดข้อมูลจาก Parquet หรือ CSV"""
    data_dir = Path(__file__).parent.parent / "data"

    # ลอง Parquet ก่อน (เร็วกว่า)
    parquet_path = data_dir / "energy_stats.parquet"
    if parquet_path.exists():
        print("Loading from Parquet...")
        return pd.read_parquet(parquet_path)

    # Fallback to CSV
    csv_path = data_dir / "energy_stats_clean.csv"
    print("Loading from CSV...")
    return pd.read_csv(csv_path)


def basic_analysis(df: pd.DataFrame):
    """การวิเคราะห์พื้นฐาน"""
    print("\n" + "=" * 60)
    print("BASIC ANALYSIS")
    print("=" * 60)

    print("\n1. Dataset Info:")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Memory: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")

    print("\n2. Data Types:")
    print(df.dtypes.to_string())

    print("\n3. Statistical Summary:")
    print(df.describe().to_string())

    print("\n4. Missing Values:")
    print(df.isnull().sum().to_string())


def regional_comparison(df: pd.DataFrame):
    """เปรียบเทียบระหว่างภูมิภาค"""
    print("\n" + "=" * 60)
    print("REGIONAL COMPARISON")
    print("=" * 60)

    # Sort by consumption
    df_sorted = df.sort_values("consumption_gwh", ascending=False)

    print("\nRanking by Electricity Consumption:")
    print("-" * 50)
    for i, (_, row) in enumerate(df_sorted.iterrows(), 1):
        bar = "█" * int(row["consumption_gwh"] / 2000)
        print(f"{i}. {row['region_th']:25} {row['consumption_gwh']:>10,.0f} GWh {bar}")

    print("\nRanking by Growth Rate:")
    print("-" * 50)
    df_growth = df.sort_values("growth_rate", ascending=False)
    for i, (_, row) in enumerate(df_growth.iterrows(), 1):
        bar = "█" * int(row["growth_rate"] * 5)
        print(f"{i}. {row['region_th']:25} {row['growth_rate']:>6.1f}% {bar}")


def calculate_metrics(df: pd.DataFrame):
    """คำนวณ metrics เพิ่มเติม"""
    print("\n" + "=" * 60)
    print("CALCULATED METRICS")
    print("=" * 60)

    # Total
    total_consumption = df["consumption_gwh"].sum()
    total_customers = df["customers"].sum()
    avg_growth = df["growth_rate"].mean()

    print(f"\nNational Total:")
    print(f"  Total Consumption: {total_consumption:,.0f} GWh")
    print(f"  Total Customers: {total_customers:,} households")
    print(f"  Average Growth: {avg_growth:.2f}%")

    # Percentage share
    print("\nRegional Share of Total Consumption:")
    df["share_pct"] = (df["consumption_gwh"] / total_consumption * 100).round(1)
    for _, row in df.iterrows():
        print(f"  {row['region_th']:25} {row['share_pct']:>5.1f}%")

    # Efficiency (consumption per customer)
    print("\nConsumption per Customer (GWh per million customers):")
    df["consumption_per_million"] = (df["consumption_gwh"] / (df["customers"] / 1_000_000)).round(2)
    for _, row in df.sort_values("consumption_per_million", ascending=False).iterrows():
        print(f"  {row['region_th']:25} {row['consumption_per_million']:>8,.0f} GWh/M customers")


def prepare_for_ml(df: pd.DataFrame):
    """เตรียมข้อมูลสำหรับ Machine Learning"""
    print("\n" + "=" * 60)
    print("ML DATA PREPARATION")
    print("=" * 60)

    # Select features
    feature_cols = ["customers", "growth_rate"]
    target_col = "consumption_gwh"

    X = df[feature_cols]
    y = df[target_col]

    print(f"\nFeatures (X):")
    print(X.to_string())

    print(f"\nTarget (y): {target_col}")
    print(y.to_string())

    # Normalization example
    from sklearn.preprocessing import StandardScaler, MinMaxScaler

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("\nStandardized Features:")
    X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols, index=df["region_th"])
    print(X_scaled_df.round(3).to_string())

    # One-hot encoding for region
    print("\nOne-Hot Encoded Regions:")
    region_dummies = pd.get_dummies(df["region_code"], prefix="region")
    print(region_dummies.to_string())

    return X_scaled, y


def create_visualization(df: pd.DataFrame):
    """สร้าง visualization (ถ้ามี matplotlib)"""
    try:
        import matplotlib.pyplot as plt

        print("\n" + "=" * 60)
        print("CREATING VISUALIZATIONS")
        print("=" * 60)

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Bar chart - Consumption
        ax1 = axes[0]
        df_sorted = df.sort_values("consumption_gwh", ascending=True)
        colors = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6"]
        ax1.barh(df_sorted["region_th"], df_sorted["consumption_gwh"], color=colors)
        ax1.set_xlabel("Consumption (GWh)")
        ax1.set_title("Electricity Consumption by Region (2566)")
        for i, v in enumerate(df_sorted["consumption_gwh"]):
            ax1.text(v + 500, i, f"{v:,.0f}", va="center")

        # Bar chart - Growth Rate
        ax2 = axes[1]
        df_growth = df.sort_values("growth_rate", ascending=True)
        ax2.barh(df_growth["region_th"], df_growth["growth_rate"], color=colors)
        ax2.set_xlabel("Growth Rate (%)")
        ax2.set_title("Growth Rate by Region (2566)")
        for i, v in enumerate(df_growth["growth_rate"]):
            ax2.text(v + 0.1, i, f"{v:.1f}%", va="center")

        plt.tight_layout()

        output_path = Path(__file__).parent.parent / "data" / "visualization.png"
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        print(f"✅ Saved visualization: {output_path}")

        plt.close()

    except ImportError:
        print("\n⚠️  matplotlib not installed - skipping visualization")
        print("   Install with: pip install matplotlib")


def main():
    print("=" * 60)
    print("PANDAS ANALYSIS EXAMPLE - Level 6 AI-Ready Data")
    print("=" * 60)

    # Load data
    df = load_data()

    # Run analyses
    basic_analysis(df)
    regional_comparison(df)
    calculate_metrics(df)

    # ML preparation
    try:
        from sklearn.preprocessing import StandardScaler
        prepare_for_ml(df)
    except ImportError:
        print("\n⚠️  scikit-learn not installed - skipping ML preparation")

    # Visualization
    create_visualization(df)

    print("\n" + "=" * 60)
    print("✅ Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
