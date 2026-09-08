"""
Model Training and Comparison Pipeline
Trains and benchmarks:
1. Logistic Regression
2. Decision Tree Classifier
3. Random Forest Classifier
4. Gradient Boosting Classifier

Evaluates accuracy, precision, recall, F1-score, confusion matrix, and feature importances.
Saves the best model to disk along with comparison metrics.
"""

import json
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

FEATURE_COLS = [
    "energy_kcal",
    "sugar_g",
    "sodium_mg",
    "saturated_fat_g",
    "trans_fat_g",
    "protein_g",
    "fiber_g",
    "additives_count",
    "artificial_colors_count",
    "artificial_sweeteners_count",
    "preservatives_count",
    "is_suspected_adulterant"
]

TARGET_COL = "risk_level"
CLASS_NAMES = ["Low Risk", "Moderate Risk", "High Risk"]

def train_and_evaluate_models():
    data_path = os.path.join(os.path.dirname(__file__), "data", "food_products_dataset.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Run dataset_generator.py first.")

    df = pd.read_csv(data_path)
    print(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns.")

    # Data Cleaning
    df = df.dropna(subset=FEATURE_COLS + [TARGET_COL])
    
    # Feature Engineering
    # 1. Sugar to fiber ratio (higher = worse quality)
    df["sugar_to_fiber_ratio"] = df.apply(lambda r: round(r["sugar_g"] / (r["fiber_g"] + 1.0), 3), axis=1)
    # 2. Additive density score
    df["additive_density"] = df["additives_count"] + df["artificial_colors_count"]*2 + df["preservatives_count"]*1.5
    # 3. Bad fat index
    df["bad_fat_index"] = df["saturated_fat_g"] + (df["trans_fat_g"] * 5.0)

    extended_features = FEATURE_COLS + ["sugar_to_fiber_ratio", "additive_density", "bad_fat_index"]

    X = df[extended_features]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize candidate algorithms
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=120, max_depth=8, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
    }

    comparison_results = {}
    best_model_name = None
    best_f1 = -1.0
    trained_model_objs = {}

    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        if name == "Logistic Regression":
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
        rec = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
        f1 = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))
        cm = confusion_matrix(y_test, y_pred, labels=CLASS_NAMES).tolist()
        report = classification_report(y_test, y_pred, target_names=CLASS_NAMES, output_dict=True, zero_division=0)

        # Feature importances or coefficients
        feat_imp = {}
        if hasattr(model, "feature_importances_"):
            for feat, imp in zip(extended_features, model.feature_importances_):
                feat_imp[feat] = round(float(imp), 4)
        elif hasattr(model, "coef_"):
            # Average absolute coefficients across classes
            mean_coefs = np.mean(np.abs(model.coef_), axis=0)
            for feat, coef in zip(extended_features, mean_coefs):
                feat_imp[feat] = round(float(coef), 4)

        comparison_results[name] = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "confusion_matrix": cm,
            "classification_report": report,
            "feature_importance": feat_imp
        }

        print(f"Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}")

        trained_model_objs[name] = model
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name

    print(f"\nBest Model: {best_model_name} with F1-score: {best_f1:.4f}")

    # Save artifacts
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(models_dir, exist_ok=True)

    # Save best model bundle
    best_bundle = {
        "model_name": best_model_name,
        "model": trained_model_objs[best_model_name],
        "scaler": scaler if best_model_name == "Logistic Regression" else None,
        "features": extended_features,
        "class_names": CLASS_NAMES,
        "f1_score": best_f1
    }
    model_save_path = os.path.join(models_dir, "best_food_quality_model.joblib")
    joblib.dump(best_bundle, model_save_path)
    print(f"Saved best model bundle to {model_save_path}")

    # Save comparison metrics JSON for frontend exploration
    metrics_save_path = os.path.join(models_dir, "model_comparison_metrics.json")
    output_meta = {
        "best_model": best_model_name,
        "class_names": CLASS_NAMES,
        "features": extended_features,
        "sample_count": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "models": comparison_results
    }
    with open(metrics_save_path, "w", encoding="utf-8") as f:
        json.dump(output_meta, f, indent=2)
    print(f"Saved comparison metrics to {metrics_save_path}")

    return output_meta

if __name__ == "__main__":
    train_and_evaluate_models()
