"""
Example: Machine Learning with Scikit-learn
Level 6: AI-Ready Government Data

รัน: pip install pandas scikit-learn
     python sklearn_example.py

หมายเหตุ: Dataset นี้มีแค่ 5 records - เหมาะสำหรับ demo เท่านั้น
         Production ML ต้องใช้ข้อมูลหลายปี/หลายจังหวัด
"""

import json
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


def load_data():
    """โหลดข้อมูล"""
    data_dir = Path(__file__).parent.parent / "data"
    jsonl_path = data_dir / "energy_stats.jsonl"

    records = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))

    return pd.DataFrame(records)


def prepare_features(df: pd.DataFrame):
    """เตรียม features สำหรับ ML"""
    print("\n" + "=" * 60)
    print("FEATURE ENGINEERING")
    print("=" * 60)

    # Select features
    feature_cols = ["customers", "growth_rate", "population"]
    target_col = "consumption_gwh"

    X = df[feature_cols].copy()
    y = df[target_col].copy()

    print(f"\nFeatures: {feature_cols}")
    print(f"Target: {target_col}")
    print(f"Samples: {len(df)}")

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("\nFeature Statistics (before scaling):")
    print(df[feature_cols].describe().round(2).to_string())

    return X_scaled, y, scaler, feature_cols


def train_models(X, y, feature_names):
    """ทดสอบ model หลายตัว"""
    print("\n" + "=" * 60)
    print("MODEL TRAINING & EVALUATION")
    print("=" * 60)

    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(n_estimators=10, random_state=42)
    }

    results = []

    # Leave-One-Out Cross Validation (เหมาะกับ dataset เล็ก)
    loo = LeaveOneOut()

    for name, model in models.items():
        print(f"\n--- {name} ---")

        # Cross-validation
        scores = cross_val_score(model, X, y, cv=loo, scoring="neg_mean_squared_error")
        rmse_scores = np.sqrt(-scores)

        # Fit on all data for coefficients
        model.fit(X, y)

        # Predictions
        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))

        print(f"  R² Score: {r2:.4f}")
        print(f"  RMSE: {rmse:,.2f} GWh")
        print(f"  LOO CV RMSE: {rmse_scores.mean():,.2f} ± {rmse_scores.std():,.2f}")

        # Feature importance
        if hasattr(model, "coef_"):
            print(f"  Coefficients:")
            for feat, coef in zip(feature_names, model.coef_):
                print(f"    {feat}: {coef:,.2f}")
        elif hasattr(model, "feature_importances_"):
            print(f"  Feature Importance:")
            for feat, imp in zip(feature_names, model.feature_importances_):
                print(f"    {feat}: {imp:.4f}")

        results.append({
            "model": name,
            "r2": r2,
            "rmse": rmse,
            "cv_rmse_mean": rmse_scores.mean(),
            "cv_rmse_std": rmse_scores.std()
        })

    return pd.DataFrame(results)


def predict_example(df: pd.DataFrame, scaler, model):
    """ตัวอย่างการทำนาย"""
    print("\n" + "=" * 60)
    print("PREDICTION EXAMPLE")
    print("=" * 60)

    # สมมติเราต้องการทำนายสำหรับภูมิภาคใหม่
    print("\nScenario: Predict consumption for a hypothetical new region")
    print("  - Customers: 5,000,000")
    print("  - Growth Rate: 3.5%")
    print("  - Population: 5,000,000")

    new_data = np.array([[5000000, 3.5, 5000000]])
    new_data_scaled = scaler.transform(new_data)

    prediction = model.predict(new_data_scaled)
    print(f"\n  Predicted Consumption: {prediction[0]:,.0f} GWh")

    # Compare with actual data
    print("\nComparison with actual regions:")
    for _, row in df.iterrows():
        print(f"  {row['region_th']:25} Actual: {row['consumption_gwh']:>10,.0f} GWh")


def anomaly_detection(df: pd.DataFrame, X_scaled):
    """ตรวจจับความผิดปกติ"""
    print("\n" + "=" * 60)
    print("ANOMALY DETECTION")
    print("=" * 60)

    from sklearn.ensemble import IsolationForest

    # Fit Isolation Forest
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    anomaly_labels = iso_forest.fit_predict(X_scaled)

    print("\nAnomaly Detection Results:")
    for i, (_, row) in enumerate(df.iterrows()):
        status = "⚠️ Anomaly" if anomaly_labels[i] == -1 else "✅ Normal"
        print(f"  {row['region_th']:25} {status}")

    # Highlight interesting patterns
    print("\nNote: ภาคตะวันออกมี consumption_per_capita สูงผิดปกติ")
    print("      เนื่องจากมีโรงงานอุตสาหกรรมมาก (EEC)")


def main():
    print("=" * 60)
    print("SCIKIT-LEARN EXAMPLE - Level 6 AI-Ready Data")
    print("=" * 60)

    # Load data
    df = load_data()
    print(f"\nLoaded {len(df)} records")

    # Prepare features
    X_scaled, y, scaler, feature_names = prepare_features(df)

    # Train models
    results_df = train_models(X_scaled, y, feature_names)

    # Show results summary
    print("\n" + "=" * 60)
    print("MODEL COMPARISON SUMMARY")
    print("=" * 60)
    print(results_df.to_string(index=False))

    # Best model
    best_idx = results_df["r2"].idxmax()
    best_model_name = results_df.loc[best_idx, "model"]
    print(f"\nBest Model: {best_model_name}")

    # Prediction example
    best_model = LinearRegression()
    best_model.fit(X_scaled, y)
    predict_example(df, scaler, best_model)

    # Anomaly detection
    anomaly_detection(df, X_scaled)

    print("\n" + "=" * 60)
    print("⚠️  IMPORTANT NOTES:")
    print("  - This dataset has only 5 samples (demo only)")
    print("  - Real ML requires more data (multiple years/provinces)")
    print("  - Results should not be used for actual predictions")
    print("=" * 60)


if __name__ == "__main__":
    main()
