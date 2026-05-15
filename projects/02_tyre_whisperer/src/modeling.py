"""
F1 Lab — Project 2: The Tyre Whisperer
Modeling Pipeline

Trains regression models to predict tyre degradation:
1. Polynomial regression per compound (baseline)
2. XGBoost regressor (primary)
3. Cliff detection via rolling degradation rate
"""

from __future__ import annotations

import sys
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
SEASON = 2024

FEATURE_COLS = [
    "TyreAge", "TyreAgeSq", "CompoundOrdinal",
    "IsSoft", "IsMedium", "IsHard",
    "TyreAge_x_Compound", "TrackTemp_x_TyreAge",
    "TrackTemp", "AirTemp", "Humidity", "WindSpeed",
    "FuelLoad", "Stint", "RollingDegRate",
    "CircuitAvgDeg", "CircuitStdDeg",
]
TARGET_COL = "FuelCorrectedDelta"


def load_features() -> pd.DataFrame:
    path = DATA_DIR / f"tyre_features_{SEASON}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Run feature_engineering.py first: {path}")
    return pd.read_parquet(path)


def train_polynomial_baseline(df: pd.DataFrame, degree: int = 3) -> dict:
    """Fit polynomial per compound — interpretable baseline."""
    results = {}
    for compound in ["SOFT", "MEDIUM", "HARD"]:
        cdf = df[df["Compound"] == compound]
        if len(cdf) < 50:
            continue
        X = cdf["TyreAge"].values
        y = cdf[TARGET_COL].values
        coeffs = np.polyfit(X, y, degree)
        y_pred = np.poly1d(coeffs)(X)
        results[compound] = {
            "coefficients": coeffs.tolist(),
            "mae": float(mean_absolute_error(y, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y, y_pred))),
            "r2": float(r2_score(y, y_pred)),
            "n_samples": len(cdf),
        }
        print(f"  {compound}: MAE={results[compound]['mae']:.4f}s  R²={results[compound]['r2']:.4f}")
    return results


def train_xgboost_model(df: pd.DataFrame) -> tuple[xgb.XGBRegressor, dict, pd.DataFrame]:
    """Train XGBoost with time-aware split (later rounds as test)."""
    X = df[FEATURE_COLS].values
    y = df[TARGET_COL].values

    unique_rounds = sorted(df["Round"].unique())
    split_round = unique_rounds[int(len(unique_rounds) * 0.8)]
    train_mask = df["Round"] <= split_round
    test_mask = df["Round"] > split_round

    X_train, X_test = X[train_mask], X[test_mask]
    y_train, y_test = y[train_mask], y[test_mask]
    print(f"  Train: {len(X_train)} laps | Test: {len(X_test)} laps")

    model = xgb.XGBRegressor(
        n_estimators=300, max_depth=6, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8, reg_alpha=0.1,
        reg_lambda=1.0, random_state=42, n_jobs=-1,
    )
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    y_pred = model.predict(X_test)
    metrics = {
        "test_mae": float(mean_absolute_error(y_test, y_pred)),
        "test_rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        "test_r2": float(r2_score(y_test, y_pred)),
        "feature_importance": dict(zip(FEATURE_COLS, map(float, model.feature_importances_))),
    }
    print(f"  Test MAE: {metrics['test_mae']:.4f}s  R²: {metrics['test_r2']:.4f}")

    cv = cross_val_score(model, X, y, cv=5, scoring="neg_mean_absolute_error")
    metrics["cv_mae"] = float(-cv.mean())
    print(f"  5-Fold CV MAE: {metrics['cv_mae']:.4f}s")

    test_df = df[test_mask].copy()
    test_df["Predicted"] = y_pred
    return model, metrics, test_df


def detect_cliff_points(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    """Detect the lap where degradation accelerates beyond threshold × average."""
    cliff_data = []
    for (driver, stint, rnd), g in df.groupby(["Driver", "Stint", "Round"]):
        g = g.sort_values("TyreAge")
        if len(g) < 5:
            continue
        deltas = g[TARGET_COL].values
        ages = g["TyreAge"].values
        lap_deg = np.diff(deltas)
        avg_deg = max(np.mean(lap_deg[:max(3, len(lap_deg) // 2)]), 0.01)
        cliff_lap = None
        for i, deg in enumerate(lap_deg):
            if deg > avg_deg * threshold and ages[i + 1] > 5:
                cliff_lap = int(ages[i + 1])
                break
        cliff_data.append({
            "Driver": driver, "Stint": stint, "Round": rnd,
            "EventName": g["EventName"].iloc[0],
            "Compound": g["Compound"].iloc[0],
            "StintLength": len(g),
            "CliffLap": cliff_lap, "HasCliff": cliff_lap is not None,
        })
    return pd.DataFrame(cliff_data)


def main():
    print("=" * 60)
    print(f"🛞  Tyre Degradation Modeling ({SEASON})")
    print("=" * 60)

    df = load_features()
    print(f"Loaded {len(df)} laps\n")

    print("📈 Polynomial baselines:")
    poly = train_polynomial_baseline(df)

    print("\n🌲 XGBoost model:")
    model, metrics, test_preds = train_xgboost_model(df)

    print("\n🏔️  Cliff detection:")
    cliff_df = detect_cliff_points(df)
    pct = cliff_df["HasCliff"].mean() * 100
    print(f"  {cliff_df['HasCliff'].sum()}/{len(cliff_df)} stints with cliff ({pct:.1f}%)")

    # Save artifacts
    model.save_model(str(MODEL_DIR / "xgb_tyre_degradation.json"))
    with open(MODEL_DIR / "metrics.json", "w") as f:
        json.dump({"polynomial": poly, "xgboost": metrics}, f, indent=2)
    cliff_df.to_parquet(DATA_DIR / f"tyre_cliffs_{SEASON}.parquet", index=False)
    test_preds.to_parquet(DATA_DIR / f"tyre_test_preds_{SEASON}.parquet", index=False)
    print(f"\n💾 All artifacts saved to {MODEL_DIR} and {DATA_DIR}")


if __name__ == "__main__":
    main()
