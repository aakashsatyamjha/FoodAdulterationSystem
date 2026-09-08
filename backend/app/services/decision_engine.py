"""
Multi-Criteria Food Safety Decision Engine & Decision Trace Service
Synthesizes Adulteration Screening, Health Risk Assessment, Global Regulatory Compliance,
and Consumer Intelligence into an explainable, multi-dimensional Food Safety Report.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from .adulteration_service import analyze_ingredients_text, DISCLAIMER_TEXT
from .ingredient_intelligence import match_ingredient_text, get_supported_countries
from .regulatory_service import evaluate_country_compliance, build_cross_country_comparison
from .consumer_service import evaluate_consumer_suitability
from ...ml.predict import predictor

def run_multi_criteria_evaluation(
    product_name: str,
    brand: str,
    category: str,
    ingredients_text: str,
    nutrition_dict: Optional[Dict[str, float]] = None,
    barcode: Optional[str] = None,
    scan_type: str = "manual",
    selected_country: str = "IN",
    user_preferences: Optional[Dict[str, bool]] = None,
    custom_thresholds: Optional[Dict[str, float]] = None,
    image_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes all 4 FoodGuard pillars sequentially and generates an explainable Decision Trace.
    Never short-circuits on first failure; evaluates every applicable criterion.
    """
    if nutrition_dict is None:
        nutrition_dict = {
            "energy_kcal": 0.0,
            "sugar_g": 0.0,
            "sodium_mg": 0.0,
            "saturated_fat_g": 0.0,
            "trans_fat_g": 0.0,
            "protein_g": 0.0,
            "fiber_g": 0.0
        }

    decision_steps = []

    # ── STEP 1: Ingredient Identification & Normalization ──
    matched_ingredients = match_ingredient_text(ingredients_text)
    decision_steps.append({
        "step_num": 1,
        "title": "Ingredient Identification & Entity Normalization",
        "status": "PASS" if matched_ingredients else "INFO",
        "detail": f"Matched {len(matched_ingredients)} standardized food ingredients against the centralized intelligence database.",
        "icon": "ListChecks"
    })

    # ── PILLAR 1: Adulteration Screening (AI & Chemical Rules) ──
    adulteration_res = analyze_ingredients_text(ingredients_text, category)
    has_critical_adulterant = adulteration_res.get("has_critical_flags", False)
    adulteration_indicators = adulteration_res.get("adulteration_indicators", [])

    if has_critical_adulterant:
        adulteration_status = "HIGH CONCERN"
        adulteration_badge = "✕ High Concern / Adulterant Flagged"
        adulteration_summary = f"Detected {len(adulteration_indicators)} indicator(s) associated with banned or hazardous adulteration patterns."
        step_status = "FAIL"
    elif adulteration_indicators:
        adulteration_status = "MEDIUM CONCERN"
        adulteration_badge = "⚠ Medium Concern"
        adulteration_summary = f"Flagged {len(adulteration_indicators)} suspicious formulation marker(s)."
        step_status = "CONDITIONAL"
    else:
        adulteration_status = "LOW CONCERN"
        adulteration_badge = "✓ Low Concern"
        adulteration_summary = "No known industrial chemical adulterants or non-permitted dye signatures detected."
        step_status = "PASS"

    decision_steps.append({
        "step_num": 2,
        "title": "Pillar 1: Adulteration Screening",
        "status": step_status,
        "detail": adulteration_summary,
        "icon": "ShieldAlert" if has_critical_adulterant else "ShieldCheck"
    })

    # If nutrition was not explicitly provided (e.g. from OCR label text), estimate baseline from ingredients keywords
    if not nutrition_dict or (nutrition_dict.get("energy_kcal", 0.0) == 0.0 and nutrition_dict.get("sugar_g", 0.0) == 0.0 and nutrition_dict.get("sodium_mg", 0.0) == 0.0):
        ing_lower = ingredients_text.lower()
        est_sugar = 0.0
        est_sodium = 45.0
        est_sat_fat = 0.5
        est_trans_fat = 0.0
        est_protein = 2.0
        est_fiber = 1.0
        est_energy = 120.0

        if any(w in ing_lower for w in ["sugar", "sucrose", "glucose", "corn syrup", "fructose", "maltose", "dextrose", "jaggery", "tastemaker"]):
            est_sugar += 16.5
        if any(w in ing_lower for w in ["salt", "sodium", "ins 621", "msg", "monosodium glutamate", "ins 635", "baking powder", "soda"]):
            est_sodium += 620.0
        if any(w in ing_lower for w in ["palm oil", "hydrogenated", "shortening", "vanaspati", "butter", "lard", "tallow", "fat"]):
            est_sat_fat += 9.5
            if "hydrogenated" in ing_lower or "vanaspati" in ing_lower:
                est_trans_fat += 0.8
        if any(w in ing_lower for w in ["milk", "dairy", "whey", "protein", "soya", "egg", "peanut", "cashew", "almond"]):
            est_protein += 8.0
        if any(w in ing_lower for w in ["whole wheat", "oats", "fiber", "bran", "psyllium", "flaxseed"]):
            est_fiber += 6.0

        nutrition_dict = {
            "energy_kcal": est_energy,
            "sugar_g": est_sugar,
            "sodium_mg": est_sodium,
            "saturated_fat_g": est_sat_fat,
            "trans_fat_g": est_trans_fat,
            "protein_g": est_protein,
            "fiber_g": est_fiber
        }

    # ── ML Model Inference for Quality Scoring & Explanations ──
    concerning_additives = list(adulteration_res.get("concerning_additives", []))
    for ing in matched_ingredients:
        concerning_additives.append({
            "name": ing.get("common_name", "Additive"),
            "matched_text": ing.get("common_name", ""),
            "type": ing.get("function", "Food Additive"),
            "risk_level": ing.get("risk_classification", "Moderate"),
            "concern": ing.get("cross_country_reason", "")
        })

    n_additives = len(concerning_additives)
    n_colors = sum(1 for a in concerning_additives if any(k in a.get("type", "").lower() for k in ["dye", "color", "colour", "pigment"]))
    n_sweeteners = sum(1 for a in concerning_additives if any(k in a.get("type", "").lower() for k in ["sweetener", "sugar substitute"]))
    n_preservatives = sum(1 for a in concerning_additives if any(k in a.get("type", "").lower() for k in ["preservative", "antioxidant", "conditioner", "agent"]))
    is_adulterated_flag = 1 if has_critical_adulterant else 0

    ml_input = {
        "energy_kcal": nutrition_dict.get("energy_kcal", 0.0),
        "sugar_g": nutrition_dict.get("sugar_g", 0.0),
        "sodium_mg": nutrition_dict.get("sodium_mg", 0.0),
        "saturated_fat_g": nutrition_dict.get("saturated_fat_g", 0.0),
        "trans_fat_g": nutrition_dict.get("trans_fat_g", 0.0),
        "protein_g": nutrition_dict.get("protein_g", 0.0),
        "fiber_g": nutrition_dict.get("fiber_g", 0.0),
        "additives_count": n_additives,
        "artificial_colors_count": n_colors,
        "artificial_sweeteners_count": n_sweeteners,
        "preservatives_count": n_preservatives,
        "is_suspected_adulterant": is_adulterated_flag
    }

    ml_res = predictor.predict(ml_input)

    # ── PILLAR 2: Health & Risk Assessment ──
    # Compute multi-dimensional risk scores (0% to 100%)
    # 1. Ingredient Risk (based on severity of additives and toxicity markers)
    ing_risk_points = 0
    for ing in matched_ingredients:
        r = ing.get("risk_classification", "Low").lower()
        if r == "critical":
            ing_risk_points += 45
        elif r == "high":
            ing_risk_points += 25
        elif r == "moderate":
            ing_risk_points += 15
        elif r == "low-to-moderate":
            ing_risk_points += 8
    if has_critical_adulterant:
        ing_risk_points += 60
    if n_additives > 3:
        ing_risk_points += (n_additives - 3) * 5
    ingredient_risk_pct = min(100, max(5, ing_risk_points))

    # 2. Regulatory Risk & Multi-Country Pre-Evaluation (IN, US, EU, DE, UK)
    cross_country_data = build_cross_country_comparison(ingredients_text)
    
    all_country_codes = ["IN", "US", "EU", "DE", "UK"]
    all_country_evaluations = {}
    country_summaries = {}
    for c_code in all_country_codes:
        eval_res = evaluate_country_compliance(ingredients_text, country_code=c_code, category=category)
        all_country_evaluations[c_code] = eval_res
        country_summaries[c_code] = {
            "country_code": c_code,
            "country_name": eval_res["country_name"],
            "authority": eval_res["authority"],
            "full_authority": eval_res.get("full_authority", eval_res["authority"]),
            "flag": eval_res["flag"],
            "verdict": eval_res["verdict"],
            "verdict_text": eval_res["verdict_text"],
            "summary": eval_res["summary"],
            "passed_criteria": eval_res["passed_criteria"],
            "conditional_criteria": eval_res["conditional_criteria"],
            "failed_criteria": eval_res["failed_criteria"],
            "total_criteria_evaluated": eval_res.get("total_criteria_evaluated", 0)
        }
        
    selected_country_eval = all_country_evaluations.get(selected_country, all_country_evaluations["IN"])
    
    reg_risk_points = 0
    if selected_country_eval["verdict"] == "FAIL":
        reg_risk_points += 75
    elif selected_country_eval["verdict"] == "CONDITIONAL":
        reg_risk_points += 40
    if cross_country_data["divergence_count"] > 0:
        reg_risk_points += cross_country_data["divergence_count"] * 12
    regulatory_risk_pct = min(100, max(5, reg_risk_points))

    # 3. Consumer Risk (based on nutritional extremes and user profile conflicts)
    consumer_eval = evaluate_consumer_suitability(
        ingredients_text=ingredients_text,
        nutrition=nutrition_dict,
        preferences=user_preferences,
        custom_thresholds=custom_thresholds
    )
    
    sugar_val = float(nutrition_dict.get("sugar_g", 0.0))
    sodium_val = float(nutrition_dict.get("sodium_mg", 0.0))
    sat_val = float(nutrition_dict.get("saturated_fat_g", 0.0))
    trans_val = float(nutrition_dict.get("trans_fat_g", 0.0))

    consumer_risk_points = 0
    if sugar_val > 22.5: consumer_risk_points += 30
    elif sugar_val > 10.0: consumer_risk_points += 15
    if sodium_val > 800.0: consumer_risk_points += 30
    elif sodium_val > 400.0: consumer_risk_points += 15
    if sat_val > 8.0: consumer_risk_points += 20
    if trans_val > 0.2: consumer_risk_points += 40
    if len(consumer_eval.get("concerns", [])) > 0:
        consumer_risk_points += len(consumer_eval["concerns"]) * 15
    consumer_risk_pct = min(100, max(5, consumer_risk_points))

    # 4. Overall Holistic Risk Calculation
    overall_risk_pct = min(100, max(5, round(
        (ingredient_risk_pct * 0.40) + 
        (regulatory_risk_pct * 0.35) + 
        (consumer_risk_pct * 0.25)
    )))

    if overall_risk_pct >= 65 or has_critical_adulterant:
        risk_tier = "High Risk"
    elif overall_risk_pct >= 30:
        risk_tier = "Moderate Risk"
    else:
        risk_tier = "Low Risk"

    # ── Holistic Multi-Pillar Quality & Safety Score (0-100) ──
    base_ml_score = ml_res["quality_score"]
    safety_score = max(5, 100 - overall_risk_pct)

    if has_critical_adulterant:
        quality_score = max(5, min(22, safety_score))
    elif selected_country_eval["verdict"] == "FAIL":
        quality_score = max(10, min(38, round(safety_score * 0.7 + base_ml_score * 0.3)))
    elif selected_country_eval["verdict"] == "CONDITIONAL" or cross_country_data["divergence_count"] > 0:
        quality_score = max(25, min(65, round(safety_score * 0.6 + base_ml_score * 0.4)))
    elif risk_tier == "Moderate Risk" or consumer_eval["verdict"] == "CONCERN":
        quality_score = max(40, min(72, round(safety_score * 0.5 + base_ml_score * 0.5)))
    else:
        quality_score = max(75, min(98, round(safety_score * 0.4 + base_ml_score * 0.6)))

    # ── Why This Product is Not 100/100 (Score Deduction Audit) ──
    score_deductions = []
    
    if has_critical_adulterant:
        for ind in adulteration_indicators:
            score_deductions.append({
                "factor": ind.get("substance", "Adulterant Marker"),
                "category": "Adulteration / Toxic Marker",
                "impact": "-45 to -60 pts",
                "points_deducted": 50,
                "reason": f"Prohibited industrial chemical marker: {ind.get('reason', 'Strictly banned adulterant')}.",
                "prohibited_in": "India (FSSAI), USA (FDA), EU (EFSA), Germany (BVL), UK (FSA)"
            })
            
    for ing in matched_ingredients:
        ing_name = ing.get("common_name", "Additive")
        ins_code = ing.get("ins_e_number", "INS Additive")
        risk_cls = ing.get("risk_classification", "Moderate")
        
        in_code = ing.get("india_status", {}).get("code", "")
        us_code = ing.get("usa_status", {}).get("code", "")
        eu_code = ing.get("eu_status", {}).get("code", "")
        de_code = ing.get("germany_status", {}).get("code", "")
        uk_code = ing.get("uk_status", {}).get("code", "")
        
        prohibited_countries = []
        if in_code == "NOT_PERMITTED": prohibited_countries.append("India (FSSAI)")
        if us_code == "NOT_PERMITTED": prohibited_countries.append("USA (FDA)")
        if eu_code == "NOT_PERMITTED": prohibited_countries.append("EU (EFSA)")
        if de_code == "NOT_PERMITTED": prohibited_countries.append("Germany (BVL)")
        if uk_code == "NOT_PERMITTED": prohibited_countries.append("UK (FSA)")
        
        if prohibited_countries:
            pts = 35 if risk_cls.lower() in ["critical", "high"] else 20
            score_deductions.append({
                "factor": f"{ing_name} ({ins_code})",
                "category": "Statutory Regulatory Prohibition",
                "impact": f"-{pts} pts",
                "points_deducted": pts,
                "reason": f"Banned or unapproved in {', '.join(prohibited_countries)}. {ing.get('cross_country_reason', '')}",
                "prohibited_in": ", ".join(prohibited_countries)
            })
        elif risk_cls.lower() in ["high", "moderate", "low-to-moderate"]:
            pts = 15 if risk_cls.lower() == "high" else (10 if risk_cls.lower() == "moderate" else 5)
            score_deductions.append({
                "factor": f"{ing_name} ({ins_code})",
                "category": "Food Additive / Formulation Limit",
                "impact": f"-{pts} pts",
                "points_deducted": pts,
                "reason": f"Subject to regulatory exposure caps and statutory warning labels. {ing.get('cross_country_reason', '')}",
                "prohibited_in": "Permitted with limits"
            })
            
    if sugar_val > 22.5:
        score_deductions.append({
            "factor": f"High Sugar Content ({sugar_val}g/100g)",
            "category": "Nutritional Risk",
            "impact": "-18 pts",
            "points_deducted": 18,
            "reason": "Exceeds WHO/FSSAI high sugar threshold (15g/100g).",
            "prohibited_in": "None (Nutritional Guideline)"
        })
    elif sugar_val > 10.0:
        score_deductions.append({
            "factor": f"Moderate Sugar Level ({sugar_val}g/100g)",
            "category": "Nutritional Risk",
            "impact": "-8 pts",
            "points_deducted": 8,
            "reason": "Elevated added sugar content.",
            "prohibited_in": "None (Nutritional Guideline)"
        })
        
    if sodium_val > 800.0:
        score_deductions.append({
            "factor": f"High Sodium ({sodium_val}mg/100g)",
            "category": "Cardiovascular Risk",
            "impact": "-18 pts",
            "points_deducted": 18,
            "reason": "Exceeds daily baseline sodium recommendations.",
            "prohibited_in": "None (Nutritional Guideline)"
        })
    elif sodium_val > 400.0:
        score_deductions.append({
            "factor": f"Elevated Sodium ({sodium_val}mg/100g)",
            "category": "Cardiovascular Risk",
            "impact": "-8 pts",
            "points_deducted": 8,
            "reason": "Moderate-to-high sodium content.",
            "prohibited_in": "None (Nutritional Guideline)"
        })
        
    if sat_val > 8.0:
        score_deductions.append({
            "factor": f"High Saturated Fat ({sat_val}g/100g)",
            "category": "Lipid Profile Risk",
            "impact": "-12 pts",
            "points_deducted": 12,
            "reason": "Rich in saturated fats (e.g. palm oil / hydrogenated fats).",
            "prohibited_in": "None (Nutritional Guideline)"
        })
        
    if trans_val > 0.2:
        score_deductions.append({
            "factor": f"Industrial Trans Fat ({trans_val}g/100g)",
            "category": "Strict Legal Cap",
            "impact": "-25 pts",
            "points_deducted": 25,
            "reason": "Exceeds WHO & FSSAI mandatory 2% trans-fat cap in fats/oils.",
            "prohibited_in": "Restricted globally"
        })

    decision_steps.append({
        "step_num": 3,
        "title": "Pillar 2: Health & Risk Assessment",
        "status": "FAIL" if risk_tier == "High Risk" else ("CONDITIONAL" if risk_tier == "Moderate Risk" else "PASS"),
        "detail": f"Overall Risk Score: {overall_risk_pct}% (Ingredient Risk: {ingredient_risk_pct}%, Regulatory Risk: {regulatory_risk_pct}%, Consumer Risk: {consumer_risk_pct}%).",
        "icon": "Activity"
    })

    # ── PILLAR 3: Global Regulatory Compliance ──
    decision_steps.append({
        "step_num": 4,
        "title": f"Pillar 3: Regulatory Compliance ({selected_country_eval['country_name']})",
        "status": selected_country_eval["verdict"],
        "detail": selected_country_eval["summary"],
        "icon": "Scale"
    })

    if cross_country_data["divergence_count"] > 0:
        decision_steps.append({
            "step_num": 5,
            "title": "Cross-Country Regulatory Divergence",
            "status": "CONDITIONAL",
            "detail": f"Identified {cross_country_data['divergence_count']} ingredient(s) with divergent regulatory statuses between India, USA, EU, Germany, and the UK.",
            "icon": "Globe"
        })

    # ── PILLAR 4: Consumer Intelligence ──
    if consumer_eval["verdict"] == "CONCERN":
        consumer_step_status = "CONDITIONAL"
    elif consumer_eval["verdict"] == "SUITABLE":
        consumer_step_status = "PASS"
    else:
        consumer_step_status = "INFO"

    decision_steps.append({
        "step_num": 6,
        "title": "Pillar 4: Consumer Suitability & Preference Matching",
        "status": consumer_step_status,
        "detail": consumer_eval["summary"],
        "icon": "UserCheck"
    })

    # ── FINAL DECISION ENGINE SYNTHESIS ──
    if has_critical_adulterant:
        overall_assessment = "HIGH CONCERN: BANNED / ADULTERANT SIGNATURE DETECTED"
        final_verdict_badge = "High Concern"
        final_explanation = "Product failed critical adulteration screening due to presence of hazardous or non-permitted industrial markers."
    elif selected_country_eval["verdict"] == "FAIL":
        overall_assessment = "REGULATORY CONCERN: NON-COMPLIANT IN SELECTED REGION"
        final_verdict_badge = "Regulatory Concern"
        final_explanation = f"Product contains substances not authorized or prohibited under {selected_country_eval['country_name']} ({selected_country_eval['authority']}) regulations."
    elif cross_country_data["divergence_count"] > 0:
        overall_assessment = "CONDITIONAL / COUNTRY-DEPENDENT REGULATORY STATUS"
        final_verdict_badge = "Country Dependent"
        final_explanation = f"Product legality and permissible additive levels vary across international jurisdictions ({cross_country_data['divergence_count']} ingredient divergence(s))."
    elif risk_tier == "Moderate Risk" or consumer_eval["verdict"] == "CONCERN":
        overall_assessment = "MODERATE CONCERN: FORMULATION & DIETARY LIMITS APPLY"
        final_verdict_badge = "Moderate Concern"
        final_explanation = "Product is legally compliant but carries elevated nutritional or consumer preference concerns."
    else:
        overall_assessment = "SAFE / LOW CONCERN: MEETS GLOBAL SCREENING BASELINE"
        final_verdict_badge = "Low Concern"
        final_explanation = "All ingredients pass adulteration screening, comply with regulatory standards in the selected region, and align with health baselines."

    return {
        "product_name": product_name,
        "brand": brand,
        "barcode": barcode,
        "category": category,
        "scan_type": scan_type,
        "quality_score": quality_score,
        "overall_assessment": overall_assessment,
        "final_verdict_badge": final_verdict_badge,
        "final_explanation": final_explanation,
        "safety_disclaimer": DISCLAIMER_TEXT,
        
        # Pillar 1: Adulteration Screening
        "adulteration": {
            "status": adulteration_status,
            "badge": adulteration_badge,
            "summary": adulteration_summary,
            "has_critical_flags": has_critical_adulterant,
            "confidence": adulteration_res.get("adulteration_confidence", 0.0),
            "indicators": adulteration_indicators,
            "model_used": ml_res["model_used"],
            "ml_confidences": ml_res["confidences"],
            "disclaimer": "AI-based screening is a preliminary algorithmic check and not a laboratory chemical confirmation of adulteration."
        },

        # Pillar 2: Health & Risk Assessment
        "risk": {
            "risk_tier": risk_tier,
            "overall_risk_pct": overall_risk_pct,
            "ingredient_risk_pct": ingredient_risk_pct,
            "regulatory_risk_pct": regulatory_risk_pct,
            "consumer_risk_pct": consumer_risk_pct,
            "negative_factors": ml_res["negative_factors"],
            "positive_factors": ml_res["positive_factors"],
            "concerning_additives": concerning_additives
        },

        # Pillar 3: Global Regulatory Compliance
        "regulatory": {
            "selected_country": selected_country_eval,
            "country_summaries": country_summaries,
            "country_evaluations": all_country_evaluations,
            "cross_country_comparison": cross_country_data,
            "divergent_ingredients": cross_country_data["divergent_ingredients"],
            "divergence_count": cross_country_data["divergence_count"]
        },

        # Pillar 4: Consumer Intelligence
        "consumer": consumer_eval,

        # Why Not 100/100 Detailed Point Deductions
        "score_deductions": score_deductions,

        # Decision Trace & Criteria Audit Trail
        "decision_trace": {
            "steps": decision_steps,
            "total_steps": len(decision_steps),
            "matched_ingredients_count": len(matched_ingredients),
            "passed_criteria_count": len(selected_country_eval["passed_criteria"]),
            "conditional_criteria_count": len(selected_country_eval["conditional_criteria"]),
            "failed_criteria_count": len(selected_country_eval["failed_criteria"])
        },

        # Ingredients & Nutrition Raw Context
        "matched_ingredients": matched_ingredients,
        "parsed_ingredients": adulteration_res.get("parsed_ingredients", []),
        "nutrition": nutrition_dict,
        "image_url": image_url,
        "created_at": datetime.utcnow()
    }

