"""
F1 Lab — Project 3: Qualifying Prophet
Modeling Pipeline

Trains two models:
1. Classifier: Predicts if a driver makes Q3 (binary).
2. Regressor: Predicts exact grid position (1-20).
"""

from __future__ import annotations

import sys
import json
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, mean_absolute_error
from sklearn.model_selection import StratifiedKFold
import xgboost as xgb

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
SEASON = 2024

FEATURE_COLS = [
    "FP1_PaceDelta",
    "FP2_PaceDelta",
    "FP3_PaceDelta",
    "Best_Practice_Delta",
    "Pace_Improvement_FP2_to_FP3",
    "FP1_TeammateGap",
    "FP2_TeammateGap",
    "FP3_TeammateGap",
]

def load_features() -> pd.DataFrame:
    path = DATA_DIR / f"qualifying_features_{SEASON}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Run feature_engineering.py first: {path}")
    return pd.read_parquet(path)


def train_classifier(df: pd.DataFrame) -> tuple[xgb.XGBClassifier, dict, pd.DataFrame]:
    """Train XGBoost to predict if driver makes Q3."""
    X = df[FEATURE_COLS].values
    y = df["Made_Q3"].astype(int).values

    # Time-aware split: use last 25% of races as test
    unique_rounds = sorted(df["Round"].unique())
    split_idx = int(len(unique_rounds) * 0.75)
    split_round = unique_rounds[split_idx]
    
    train_mask = df["Round"] <= split_round
    test_mask = df["Round"] > split_round

    X_train, X_test = X[train_mask], X[test_mask]
    y_train, y_test = y[train_mask], y[test_mask]
    print(f"  Train: {len(X_train)} | Test: {len(X_test)}")

    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss"
    )
    
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    metrics = {
        "accuracy": float(acc),
        "confusion_matrix": cm.tolist(),
        "feature_importance": dict(zip(FEATURE_COLS, map(float, model.feature_importances_))),
    }
    
    print(f"  Accuracy: {acc*100:.1f}%")
    print(f"  Confusion Matrix:\n{cm}")

    test_df = df[test_mask].copy()
    test_df["Q3_Pred"] = y_pred
    test_df["Q3_Prob"] = y_prob
    
    return model, metrics, test_df


def train_regressor(df: pd.DataFrame) -> tuple[xgb.XGBRegressor, dict, pd.DataFrame]:
    """Train XGBoost to predict exact grid position."""
    X = df[FEATURE_COLS].values
    y = df["Position"].values

    unique_rounds = sorted(df["Round"].unique())
    split_idx = int(len(unique_rounds) * 0.75)
    split_round = unique_rounds[split_idx]
    
    train_mask = df["Round"] <= split_round
    test_mask = df["Round"] > split_round

    X_train, X_test = X[train_mask], X[test_mask]
    y_train, y_test = y[train_mask], y[test_mask]

    model = xgb.XGBRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # We predict continuous position. Need to rank them 1-20 per race
    test_df = df[test_mask].copy()
    test_df["Raw_Pred_Position"] = y_pred
    
    # Rank within each race to get actual discrete predicted grid position
    test_df["Predicted_Grid"] = test_df.groupby("EventName")["Raw_Pred_Position"].rank(method="first")
    
    mae_raw = mean_absolute_error(test_df["Position"], test_df["Raw_Pred_Position"])
    mae_ranked = mean_absolute_error(test_df["Position"], test_df["Predicted_Grid"])
    
    metrics = {
        "mae_raw": float(mae_raw),
        "mae_ranked": float(mae_ranked),
        "feature_importance": dict(zip(FEATURE_COLS, map(float, model.feature_importances_))),
    }
    
    print(f"  MAE (Raw): {mae_raw:.2f} positions")
    print(f"  MAE (Ranked): {mae_ranked:.2f} positions")

    return model, metrics, test_df


def main():
    print("=" * 60)
    print(f"🔮 F1 Lab — Qualifying Prophet Modeling ({SEASON})")
    print("=" * 60)

    df = load_features()
    print(f"Loaded {len(df)} qualifying records\n")

    print("🟢 Model 1: Q3 Classification")
    clf_model, clf_metrics, clf_test = train_classifier(df)

    print("\n🟢 Model 2: Grid Position Regression")
    reg_model, reg_metrics, reg_test = train_regressor(df)

    # Save artifacts
    clf_model.save_model(str(MODEL_DIR / "xgb_q3_classifier.json"))
    reg_model.save_model(str(MODEL_DIR / "xgb_grid_regressor.json"))
    
    with open(MODEL_DIR / "metrics.json", "w") as f:
        json.dump({
            "classification": clf_metrics,
            "regression": reg_metrics
        }, f, indent=2)
        
    # Combine test predictions
    test_preds = clf_test.copy()
    test_preds["Predicted_Grid"] = reg_test["Predicted_Grid"]
    test_preds["Raw_Pred_Position"] = reg_test["Raw_Pred_Position"]
    
    test_preds.to_parquet(DATA_DIR / f"quali_test_preds_{SEASON}.parquet", index=False)
    
    print(f"\n💾 All models and metrics saved to {MODEL_DIR}")


if __name__ == "__main__":
    main()
