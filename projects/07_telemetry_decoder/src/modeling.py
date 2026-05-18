"""
F1 Lab — Project 7: Telemetry Decoder
Time Series Modeling

Trains a Random Forest classifier to identify a driver purely
from their Speed, Throttle, and Brake traces.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "projects" / "07_telemetry_decoder" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def train_model():
    print("=" * 60)
    print("🧠 F1 Lab — Telemetry Model Training")
    print("=" * 60)
    
    path = DATA_DIR / "telemetry_2025_R1.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Missing data: {path}. Run data_collection.py first.")
        
    df = pd.read_parquet(path)
    
    # Target variable
    y = df["Driver"]
    
    # Feature columns (Speed_0 ... Brake_299)
    # We exclude Driver and LapNumber
    X = df.drop(columns=["Driver", "LapNumber"])
    
    print(f"Dataset Shape: {X.shape[0]} laps, {X.shape[1]} telemetry features")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    print("Training Random Forest Classifier on time series arrays...")
    clf = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    cm = confusion_matrix(y_test, preds, labels=clf.classes_)
    
    print(f"\n✅ Model Accuracy (Blind Driver ID): {acc * 100:.1f}%")
    print(f"Classes: {clf.classes_}")
    print("Confusion Matrix:")
    print(cm)
    
    # Find feature importances
    # Which parts of the track / which pedals give the driver away the most?
    importances = clf.feature_importances_
    features = X.columns
    
    imp_df = pd.DataFrame({"Feature": features, "Importance": importances})
    imp_df = imp_df.sort_values("Importance", ascending=False).head(20)
    
    print("\n🔍 Top 5 Most Identifying Telemetry Moments:")
    print(imp_df.head(5).to_string(index=False))
    
    # Save the feature importance for visualization
    imp_df.to_csv(MODEL_DIR / "telemetry_importance.csv", index=False)
    
    # Save confusion matrix 
    cm_dict = {
        "classes": clf.classes_.tolist(),
        "matrix": cm.tolist(),
        "accuracy": float(acc)
    }
    with open(MODEL_DIR / "telemetry_metrics.json", "w") as f:
        json.dump(cm_dict, f, indent=4)
        
    print(f"\n💾 Saved metrics to {MODEL_DIR}")


if __name__ == "__main__":
    train_model()
