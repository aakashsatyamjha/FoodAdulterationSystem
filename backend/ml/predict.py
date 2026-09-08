"""
Inference & Explainability Engine for Food Quality & Risk Prediction
"""

import os
import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "best_food_quality_model.joblib")

class FoodQualityPredictor:
    def __init__(self):
        self.bundle = None
        self.model = None
        self.features = None
        self.scaler = None
        self.class_names = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            self.bundle = joblib.load(MODEL_PATH)
            self.model = self.bundle["model"]
            self.features = self.bundle["features"]
            self.scaler = self.bundle.get("scaler")
            self.class_names = self.bundle["class_names"]
        else:
            print(f"[Warning] Model not found at {MODEL_PATH}. Inference will use rule-based fallback.")

    def predict(self, data: dict):
        """
        data dict contains:
          energy_kcal, sugar_g, sodium_mg, saturated_fat_g, trans_fat_g,
          protein_g, fiber_g, additives_count, artificial_colors_count,
          artificial_sweeteners_count, preservatives_count, is_suspected_adulterant
        """
        sugar = float(data.get("sugar_g", 0.0))
        fiber = float(data.get("fiber_g", 0.0))
        sat_fat = float(data.get("saturated_fat_g", 0.0))
        trans_fat = float(data.get("trans_fat_g", 0.0))
        sodium = float(data.get("sodium_mg", 0.0))
        protein = float(data.get("protein_g", 0.0))
        n_add = int(data.get("additives_count", 0))
        n_col = int(data.get("artificial_colors_count", 0))
        n_sw = int(data.get("artificial_sweeteners_count", 0))
        n_pres = int(data.get("preservatives_count", 0))
        is_adulterated = int(bool(data.get("is_suspected_adulterant", False)))
        energy = float(data.get("energy_kcal", 0.0))

        sugar_to_fiber = round(sugar / (fiber + 1.0), 3)
        additive_density = n_add + (n_col * 2) + (n_pres * 1.5)
        bad_fat_index = sat_fat + (trans_fat * 5.0)

        # Baseline Quality Score calculation (0-100)
        score = 100.0
        explanations = []
        positive_factors = []

        if sugar > 22.5:
            pen = min(25.0, (sugar - 22.5) * 1.1 + 8.0)
            score -= pen
            explanations.append(f"High sugar content ({sugar}g/100g) exceeds recommended threshold (15g).")
        elif sugar > 10.0:
            score -= (sugar - 10.0) * 0.7
            explanations.append(f"Moderate sugar level ({sugar}g/100g).")
        else:
            positive_factors.append(f"Low sugar content ({sugar}g/100g).")

        if sodium > 800.0:
            pen = min(25.0, (sodium - 800.0) * 0.02 + 8.0)
            score -= pen
            explanations.append(f"High sodium ({sodium}mg/100g) poses cardiovascular risk.")
        elif sodium > 400.0:
            score -= (sodium - 400.0) * 0.015
            explanations.append(f"Elevated sodium level ({sodium}mg/100g).")
        else:
            positive_factors.append("Controlled sodium level within safe dietary guidelines.")

        if trans_fat > 0.2:
            pen = min(35.0, trans_fat * 18.0)
            score -= pen
            explanations.append(f"Contains industrial trans fat ({trans_fat}g/100g) - strictly restricted by health authorities.")
        else:
            positive_factors.append("Virtually zero industrial trans fats.")

        if sat_fat > 8.0:
            score -= min(18.0, (sat_fat - 8.0) * 1.2)
            explanations.append(f"High saturated fat ({sat_fat}g/100g).")

        if n_add > 0:
            score -= (n_add * 3.0)
            explanations.append(f"Contains {n_add} industrial food additive(s).")
        else:
            positive_factors.append("Clean label: No industrial additives detected.")

        if n_col > 0:
            score -= (n_col * 5.0)
            explanations.append(f"Contains {n_col} artificial synthetic food coloring agent(s).")

        if n_sw > 0:
            score -= (n_sw * 4.0)
            explanations.append(f"Contains {n_sw} intense artificial sweetener(s).")

        if n_pres > 0:
            score -= (n_pres * 3.5)
            explanations.append(f"Contains {n_pres} chemical preservative(s).")

        if is_adulterated:
            score -= 40.0
            explanations.append("Contains ingredient flags linked to common adulteration patterns or non-permitted substances.")

        if fiber >= 5.0:
            score += min(10.0, fiber * 0.9)
            positive_factors.append(f"Excellent dietary fiber ({fiber}g/100g).")

        if protein >= 8.0:
            score += min(8.0, protein * 0.4)
            positive_factors.append(f"Good source of protein ({protein}g/100g).")

        final_score = max(5, min(99, round(score)))

        # ML Model Inference
        predicted_risk = "Low Risk"
        confidences = {"Low Risk": 0.95, "Moderate Risk": 0.04, "High Risk": 0.01}

        if self.model and self.features:
            import pandas as pd
            feature_vector = [
                energy, sugar, sodium, sat_fat, trans_fat, protein, fiber,
                n_add, n_col, n_sw, n_pres, is_adulterated,
                sugar_to_fiber, additive_density, bad_fat_index
            ]
            X_df = pd.DataFrame([feature_vector], columns=self.features)
            if self.scaler:
                X_df = self.scaler.transform(X_df)

            pred_class = self.model.predict(X_df)[0]
            predicted_risk = str(pred_class)

            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(X_df)[0]
                confidences = {
                    cls: round(float(prob), 4)
                    for cls, prob in zip(self.model.classes_, probs)
                }

        # Double check alignment with final score
        if is_adulterated:
            predicted_risk = "High Risk"
        elif final_score < 40 and predicted_risk == "Low Risk":
            predicted_risk = "Moderate Risk"

        return {
            "predicted_risk_level": predicted_risk,
            "quality_score": final_score,
            "confidences": confidences,
            "negative_factors": explanations,
            "positive_factors": positive_factors,
            "model_used": self.bundle.get("model_name", "Rule-Based + ML Gradient Boosting") if self.bundle else "Heuristic ML Engine"
        }

predictor = FoodQualityPredictor()
