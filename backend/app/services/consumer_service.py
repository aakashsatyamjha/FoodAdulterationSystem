"""
Consumer-Oriented Intelligence & Configurable Dietary Preference Service
Evaluates product nutritional thresholds, allergen alerts, and ingredient suitability
against user preferences with clearly demarcated Source-Backed vs Project-Defined guidelines.
"""

import re
from typing import List, Dict, Any, Optional

# Standard Configurable Consumer Rules Repository with Source Citations
CONSUMER_RULES: List[Dict[str, Any]] = [
    {
        "id": "rule_sugar_high",
        "country": "Global / WHO",
        "parameter": "sugar_g",
        "threshold": 15.0,
        "unit": "g / 100g",
        "direction": "max",
        "population": "General Population",
        "source": "WHO Guideline: Sugars intake for adults and children (2015)",
        "source_type": "Source-backed threshold",
        "description": "Foods exceeding 15g total sugars per 100g are classified as high sugar products.",
        "effective_date": "2015-03-04"
    },
    {
        "id": "rule_sugar_low_preference",
        "country": "UK / FSA & EU",
        "parameter": "sugar_g",
        "threshold": 5.0,
        "unit": "g / 100g",
        "direction": "max",
        "population": "Low Sugar Preference / Diabetic Awareness",
        "source": "UK Front-of-pack traffic light nutrition guidance & Regulation (EC) 1924/2006",
        "source_type": "Source-backed threshold",
        "description": "Products with <= 5g sugar per 100g qualify as low sugar (green traffic light).",
        "effective_date": "2016-11-01"
    },
    {
        "id": "rule_sodium_high",
        "country": "India / ICMR-NIN & US FDA",
        "parameter": "sodium_mg",
        "threshold": 600.0,
        "unit": "mg / 100g",
        "direction": "max",
        "population": "General Population",
        "source": "ICMR-NIN Dietary Guidelines for Indians (2024); US FDA Daily Value Guidelines",
        "source_type": "Source-backed threshold",
        "description": "Foods exceeding 600mg sodium per 100g are classified as high sodium.",
        "effective_date": "2024-05-08"
    },
    {
        "id": "rule_sodium_low_preference",
        "country": "US FDA / AHA",
        "parameter": "sodium_mg",
        "threshold": 140.0,
        "unit": "mg / 100g",
        "direction": "max",
        "population": "Low Sodium Preference / Hypertension Awareness",
        "source": "US FDA 21 CFR §101.61 (Low Sodium Claim)",
        "source_type": "Source-backed threshold",
        "description": "Food containing <= 140mg sodium per 100g qualifies for low sodium dietary suitability.",
        "effective_date": "2020-01-01"
    },
    {
        "id": "rule_saturated_fat_high",
        "country": "UK FSA / WHO",
        "parameter": "saturated_fat_g",
        "threshold": 5.0,
        "unit": "g / 100g",
        "direction": "max",
        "population": "General Cardiovascular Health",
        "source": "WHO Healthy Diet Fact Sheet; UK Front-of-Pack Nutritional Criteria",
        "source_type": "Source-backed threshold",
        "description": "Solid foods with > 5g saturated fat per 100g require red/amber traffic light profiling.",
        "effective_date": "2020-04-01"
    },
    {
        "id": "rule_trans_fat_zero",
        "country": "India FSSAI / US FDA / WHO",
        "parameter": "trans_fat_g",
        "threshold": 0.2,
        "unit": "g / 100g",
        "direction": "max",
        "population": "All Consumers",
        "source": "FSSAI Regulation 2.2.2 & US FDA Trans Fat Elimination Rule",
        "source_type": "Source-backed threshold",
        "description": "Trans fats must remain strictly below 0.2g per 100g to be considered virtually trans-fat free.",
        "effective_date": "2022-01-01"
    },
    {
        "id": "rule_protein_rich_preference",
        "country": "FSSAI & EU",
        "parameter": "protein_g",
        "threshold": 8.0,
        "unit": "g / 100g",
        "direction": "min",
        "population": "High Protein Fitness Preference",
        "source": "FSSAI (Advertising and Claims) Regulations & Regulation (EC) 1924/2006",
        "source_type": "Source-backed threshold",
        "description": "Food provides meaningful protein density when supplying >= 8g protein per 100g.",
        "effective_date": "2018-11-19"
    },
    {
        "id": "rule_fiber_rich_preference",
        "country": "ICMR-NIN & EFSA",
        "parameter": "fiber_g",
        "threshold": 3.0,
        "unit": "g / 100g",
        "direction": "min",
        "population": "Digestive Health & Low Glycemic Preference",
        "source": "ICMR-NIN 2024 Guidelines & EFSA Dietary Reference Values for Fibre",
        "source_type": "Source-backed threshold",
        "description": "Products containing >= 3g fiber per 100g qualify as a source of dietary fiber.",
        "effective_date": "2024-05-01"
    },
    {
        "id": "rule_additive_density_preference",
        "country": "FoodGuard Project",
        "parameter": "additives_count",
        "threshold": 3,
        "unit": "additives count",
        "direction": "max",
        "population": "Clean Label / Low-Additive Preference",
        "source": "FoodGuard AI Clean Label Assessment Protocol",
        "source_type": "Project-defined consumer guideline",
        "description": "Alerts consumers seeking whole foods when a single product contains 3 or more synthetic additives.",
        "effective_date": "2025-01-01"
    }
]

# Animal-derived ingredients for vegetarian/vegan screening
ANIMAL_DERIVED_MARKERS = [
    {"pattern": r"\b(gelatin|gelatine)\b", "name": "Gelatin", "non_veg": True, "non_vegan": True, "reason": "Animal-derived collagen from bovine/porcine skin and bones."},
    {"pattern": r"\b(carmine|cochineal|carminic\s*acid|e120|ins\s*120|ci\s*75470)\b", "name": "Carmine / Cochineal (E120)", "non_veg": True, "non_vegan": True, "reason": "Natural red pigment extracted from crushed female cochineal insects."},
    {"pattern": r"\b(tallow|lard|animal\s*fat|dripping|suet)\b", "name": "Animal Fat / Lard", "non_veg": True, "non_vegan": True, "reason": "Rendered fat of animal origin."},
    {"pattern": r"\b(rennet|animal\s*rennet)\b", "name": "Animal Rennet", "non_veg": True, "non_vegan": True, "reason": "Enzyme complex extracted from stomach mucosa of young ruminants."},
    {"pattern": r"\b(isinglass)\b", "name": "Isinglass", "non_veg": True, "non_vegan": True, "reason": "Clarifying agent derived from fish bladders."},
    {"pattern": r"\b(bone\s*char)\b", "name": "Bone Char", "non_veg": True, "non_vegan": True, "reason": "Charred animal bones used in sugar decolourisation."},
    {"pattern": r"\b(milk|milk\s*solids|milk\s*fat|butter|cheese|paneer|ghee|casein|caseinate|whey|whey\s*protein|lactose|curd|yogurt)\b", "name": "Dairy / Milk Solids", "non_veg": False, "non_vegan": True, "reason": "Bovine dairy derivative."},
    {"pattern": r"\b(egg|eggs|egg\s*powder|egg\s*albumin|albumen|ovotransferrin)\b", "name": "Egg / Egg Albumin", "non_veg": True, "non_vegan": True, "reason": "Poultry egg derivative."},
    {"pattern": r"\b(honey|beeswax|e901|ins\s*901|royal\s*jelly|propolis)\b", "name": "Honey / Beeswax (E901)", "non_veg": False, "non_vegan": True, "reason": "Bee-derived product (not vegan)."},
    {"pattern": r"\b(shellac|confectioner'?s\s*glaze|resinous\s*glaze|e904|ins\s*904)\b", "name": "Shellac (E904)", "non_veg": False, "non_vegan": True, "reason": "Resin secreted by the female lac bug on trees."}
]

# Gluten and common allergen markers
GLUTEN_MARKERS = [
    {"pattern": r"\b(wheat|wheat\s*flour|maida|atta|refined\s*wheat|semolina|sooji|suji|durum|spelt|kamut|emmer|einkorn|triticale)\b", "name": "Wheat / Wheat Flour"},
    {"pattern": r"\b(barley|barley\s*malt|malt\s*extract|malt\s*flavouring|maltodextrin\s*from\s*wheat)\b", "name": "Barley / Malt"},
    {"pattern": r"\b(rye|rye\s*flour)\b", "name": "Rye"},
    {"pattern": r"\b(gluten|vital\s*wheat\s*gluten)\b", "name": "Gluten"}
]

ALLERGEN_REGISTRY = [
    {"pattern": r"\b(peanut|peanuts|groundnut|groundnuts|arachis\s*oil)\b", "name": "Peanuts", "severity": "High"},
    {"pattern": r"\b(almond|almonds|cashew|cashews|kaju|badam|walnut|walnuts|pistachio|pistachios|pista|hazelnut|hazelnuts|pecan|macadamia|brazil\s*nut)\b", "name": "Tree Nuts", "severity": "High"},
    {"pattern": r"\b(milk|milk\s*solids|milk\s*fat|butter|cheese|casein|whey|lactose)\b", "name": "Milk / Dairy", "severity": "Moderate"},
    {"pattern": r"\b(egg|eggs|egg\s*powder|egg\s*albumin)\b", "name": "Egg", "severity": "High"},
    {"pattern": r"\b(soy|soya|soybean|soybeans|soy\s*lecithin|soy\s*protein|tofu)\b", "name": "Soy / Soybean", "severity": "Moderate"},
    {"pattern": r"\b(wheat|maida|gluten|barley|rye)\b", "name": "Wheat / Gluten", "severity": "Moderate"},
    {"pattern": r"\b(fish|cod|salmon|tuna|anchovy|anchovies|gelatin\s*fish|fish\s*oil)\b", "name": "Fish", "severity": "High"},
    {"pattern": r"\b(shrimp|prawn|prawns|crab|lobster|crustacean|shellfish|mussel|clam|oyster)\b", "name": "Crustaceans / Shellfish", "severity": "High"},
    {"pattern": r"\b(sesame|sesame\s*seeds|til|gingelly\s*oil|tahini)\b", "name": "Sesame", "severity": "High"},
    {"pattern": r"\b(mustard|mustard\s*seeds|mustard\s*oil|sarson|rai)\b", "name": "Mustard", "severity": "Moderate"},
    {"pattern": r"\b(sulphite|sulfite|metabisulphite|metabisulfite|sulphur\s*dioxide|sulfur\s*dioxide|e220|e221|e222|e223|e224|ins\s*223)\b", "name": "Sulfites (> 10 ppm)", "severity": "Moderate"}
]

def get_all_consumer_rules() -> List[Dict[str, Any]]:
    """Returns configured consumer rules database with source tags."""
    return CONSUMER_RULES

def evaluate_consumer_suitability(
    ingredients_text: str,
    nutrition: Dict[str, float],
    preferences: Optional[Dict[str, bool]] = None,
    custom_thresholds: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Evaluates personal suitability against user-selected dietary preferences and nutritional thresholds.
    Does NOT make unsupported medical claims; provides factual, rule-backed explanations.
    """
    if preferences is None:
        preferences = {
            "low_sugar": False,
            "low_sodium": False,
            "high_protein": False,
            "vegetarian": True,
            "vegan": False,
            "gluten_free": False,
            "allergen_safe": False,
            "low_additives": False,
            "low_processed": False
        }

    sugar = float(nutrition.get("sugar_g", 0.0))
    sodium = float(nutrition.get("sodium_mg", 0.0))
    sat_fat = float(nutrition.get("saturated_fat_g", 0.0))
    trans_fat = float(nutrition.get("trans_fat_g", 0.0))
    protein = float(nutrition.get("protein_g", 0.0))
    fiber = float(nutrition.get("fiber_g", 0.0))

    ing_lower = (ingredients_text or "").lower()

    results = []
    matched_preferences = []
    concerns = []
    
    # 1. Low Sugar Evaluation
    if preferences.get("low_sugar"):
        threshold = custom_thresholds.get("sugar_max", 5.0) if custom_thresholds else 5.0
        if sugar <= threshold:
            results.append({
                "preference": "Low Sugar",
                "status": "PASS",
                "badge": "✓ Suitable",
                "detail": f"Sugar level ({sugar}g/100g) is within your configured preference threshold (<= {threshold}g/100g).",
                "source": "WHO Sugar Guidelines & UK Front-of-pack criteria",
                "source_type": "Source-backed threshold"
            })
            matched_preferences.append("Low Sugar")
        else:
            results.append({
                "preference": "Low Sugar",
                "status": "CONCERN",
                "badge": "⚠ Consumer Concern",
                "detail": f"May not be suitable for your selected low-sugar preference. Sugar content ({sugar}g/100g) exceeds the configured threshold of {threshold}g/100g.",
                "source": "WHO Sugar Guidelines & UK Front-of-pack criteria",
                "source_type": "Source-backed threshold"
            })
            concerns.append(f"Sugar ({sugar}g/100g) exceeds preferred threshold ({threshold}g).")

    # 2. Low Sodium Evaluation
    if preferences.get("low_sodium"):
        threshold = custom_thresholds.get("sodium_max", 140.0) if custom_thresholds else 140.0
        if sodium <= threshold:
            results.append({
                "preference": "Low Sodium",
                "status": "PASS",
                "badge": "✓ Suitable",
                "detail": f"Sodium content ({sodium}mg/100g) is within your low sodium threshold (<= {threshold}mg/100g).",
                "source": "US FDA Low Sodium Rule & ICMR-NIN 2024 Guidelines",
                "source_type": "Source-backed threshold"
            })
            matched_preferences.append("Low Sodium")
        else:
            results.append({
                "preference": "Low Sodium",
                "status": "CONCERN",
                "badge": "⚠ Consumer Concern",
                "detail": f"May not be suitable for your selected low-sodium preference. Sodium level ({sodium}mg/100g) exceeds the configured limit of {threshold}mg/100g.",
                "source": "US FDA Low Sodium Rule & ICMR-NIN 2024 Guidelines",
                "source_type": "Source-backed threshold"
            })
            concerns.append(f"Sodium ({sodium}mg/100g) exceeds preferred threshold ({threshold}mg).")

    # 3. High Protein Evaluation
    if preferences.get("high_protein"):
        threshold = custom_thresholds.get("protein_min", 8.0) if custom_thresholds else 8.0
        if protein >= threshold:
            results.append({
                "preference": "High Protein",
                "status": "PASS",
                "badge": "✓ Suitable",
                "detail": f"Provides good protein density ({protein}g/100g), meeting your requirement (>= {threshold}g/100g).",
                "source": "FSSAI (Advertising & Claims) Regulations & Regulation (EC) 1924/2006",
                "source_type": "Source-backed threshold"
            })
            matched_preferences.append("High Protein")
        else:
            results.append({
                "preference": "High Protein",
                "status": "CONCERN",
                "badge": "⚠ Consumer Concern",
                "detail": f"Protein content ({protein}g/100g) is lower than your preferred threshold of {threshold}g/100g.",
                "source": "FSSAI (Advertising & Claims) Regulations",
                "source_type": "Source-backed threshold"
            })
            concerns.append(f"Protein ({protein}g/100g) is below target ({threshold}g).")

    # 4. Vegetarian Evaluation
    if preferences.get("vegetarian"):
        non_veg_found = []
        for marker in ANIMAL_DERIVED_MARKERS:
            if marker["non_veg"] and re.search(marker["pattern"], ing_lower):
                non_veg_found.append(f"{marker['name']} ({marker['reason']})")

        if not non_veg_found:
            results.append({
                "preference": "Vegetarian",
                "status": "PASS",
                "badge": "✓ Suitable",
                "detail": "No non-vegetarian or meat-derived ingredients detected in formulation.",
                "source": "FSSAI Labelling Regulations (Green Veg Logo Standard)",
                "source_type": "Source-backed threshold"
            })
            matched_preferences.append("Vegetarian")
        else:
            results.append({
                "preference": "Vegetarian",
                "status": "CONCERN",
                "badge": "✕ Unsuitable for Vegetarian Diet",
                "detail": f"May not be suitable for vegetarian preference. Detected animal-derived ingredient(s): {', '.join(non_veg_found)}.",
                "source": "FSSAI Green/Brown Dot Labelling Standard",
                "source_type": "Source-backed threshold"
            })
            concerns.append(f"Non-vegetarian ingredient detected: {', '.join(non_veg_found)}")

    # 5. Vegan Evaluation
    if preferences.get("vegan"):
        non_vegan_found = []
        for marker in ANIMAL_DERIVED_MARKERS:
            if marker["non_vegan"] and re.search(marker["pattern"], ing_lower):
                non_vegan_found.append(f"{marker['name']} ({marker['reason']})")

        if not non_vegan_found:
            results.append({
                "preference": "Vegan (100% Plant-Based)",
                "status": "PASS",
                "badge": "✓ Suitable",
                "detail": "No animal, dairy, egg, or insect-derived ingredients detected.",
                "source": "The Vegan Society Standard & FSSAI Vegan Regulations 2022",
                "source_type": "Source-backed threshold"
            })
            matched_preferences.append("Vegan")
        else:
            results.append({
                "preference": "Vegan (100% Plant-Based)",
                "status": "CONCERN",
                "badge": "✕ Unsuitable for Vegan Diet",
                "detail": f"Contains animal or animal-byproduct ingredients: {', '.join(non_vegan_found)}.",
                "source": "FSSAI (Vegan Foods) Regulations 2022",
                "source_type": "Source-backed threshold"
            })
            concerns.append(f"Non-vegan ingredient detected: {', '.join(non_vegan_found)}")

    # 6. Gluten-Free Awareness
    if preferences.get("gluten_free"):
        gluten_found = []
        for marker in GLUTEN_MARKERS:
            if re.search(marker["pattern"], ing_lower):
                gluten_found.append(marker["name"])

        if not gluten_found:
            results.append({
                "preference": "Gluten Awareness",
                "status": "PASS",
                "badge": "✓ No Gluten Ingredients Detected",
                "detail": "No wheat, barley, rye, or gluten ingredients identified in the ingredient list.",
                "source": "Codex Alimentarius Standard for Foods for Special Dietary Use for Persons Intolerant to Gluten (CXS 118-1979)",
                "source_type": "Source-backed threshold"
            })
            matched_preferences.append("Gluten-Free")
        else:
            results.append({
                "preference": "Gluten Awareness",
                "status": "CONCERN",
                "badge": "⚠ Contains Gluten Ingredients",
                "detail": f"Contains gluten-bearing grains: {', '.join(gluten_found)}. Not suitable for individuals with Celiac Disease without dedicated certified gluten-free testing.",
                "source": "Codex Standard CXS 118-1979 & US FDA 21 CFR §101.91",
                "source_type": "Source-backed threshold"
            })
            concerns.append(f"Gluten-bearing grain detected: {', '.join(gluten_found)}")

    # 7. Allergen Awareness
    detected_allergens = []
    for alg in ALLERGEN_REGISTRY:
        if re.search(alg["pattern"], ing_lower):
            detected_allergens.append(alg["name"])

    if preferences.get("allergen_safe"):
        if not detected_allergens:
            results.append({
                "preference": "Allergen Awareness",
                "status": "PASS",
                "badge": "✓ Clean Allergen Profile",
                "detail": "None of the standard Major-9 priority food allergens were detected in label text.",
                "source": "US FALCPA / FASTER Act & FSSAI Allergen Declaration Regulations",
                "source_type": "Source-backed threshold"
            })
        else:
            results.append({
                "preference": "Allergen Awareness",
                "status": "CONCERN",
                "badge": "⚠ Regulated Allergens Present",
                "detail": f"Detected major priority food allergen(s): {', '.join(detected_allergens)}. Verify allergen warning label for cross-contact notices.",
                "source": "Regulation (EU) No 1169/2011 Annex II & FSSAI Regulations",
                "source_type": "Source-backed threshold"
            })

    # Overall Consumer Suitability Verdict
    active_preference_count = sum(1 for v in preferences.values() if v)
    if not active_preference_count:
        suitability_verdict = "NOT_CONFIGURED"
        suitability_summary = "No active consumer preferences selected. Set up your Food Profile for personalized suitability screening."
    elif concerns:
        suitability_verdict = "CONCERN"
        suitability_summary = f"Product flagged {len(concerns)} concern(s) against your active dietary preferences."
    else:
        suitability_verdict = "SUITABLE"
        suitability_summary = f"Product matches all {active_preference_count} of your active dietary preferences."

    return {
        "verdict": suitability_verdict,
        "summary": suitability_summary,
        "results": results,
        "matched_preferences": matched_preferences,
        "concerns": concerns,
        "detected_allergens": detected_allergens,
        "rules_evaluated": len(results),
        "available_rules": CONSUMER_RULES
    }
