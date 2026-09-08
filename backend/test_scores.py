from backend.app.services.decision_engine import run_multi_criteria_evaluation

samples = [
    ("Adulterated Turmeric", "Pure Turmeric powder, Metanil Yellow industrial dye, Lead Chromate yellow pigment", "IN"),
    ("Commercial Instant Noodles", "Wheat Flour (Maida), Palm Oil, Salt, Wheat Gluten, Flavour Enhancer (INS 635), Acidity Regulator (INS 330), Sugar", "IN"),
    ("Bread with Potassium Bromate (in India)", "Refined Wheat Flour, Potassium Bromate, Titanium Dioxide, Sugar, Palm Oil, Water, Yeast", "IN"),
    ("Bread with Potassium Bromate (in EU)", "Refined Wheat Flour, Potassium Bromate, Titanium Dioxide, Sugar, Palm Oil, Water, Yeast", "EU"),
    ("Fresh Toned Milk", "Pasteurised Toned Milk, Vitamin A, Vitamin D2. Fat 3.0%, SNF 8.5%", "IN")
]

for name, ing, c in samples:
    res = run_multi_criteria_evaluation(
        product_name=name,
        brand="TestBrand",
        category="Packaged Food",
        ingredients_text=ing,
        selected_country=c
    )
    score = res.get("quality_score")
    verdict = res.get("final_verdict_badge")
    assessment = res.get("overall_assessment")
    risk_info = res.get("risk", {})
    overall_risk = risk_info.get("overall_risk_pct")
    ing_risk = risk_info.get("ingredient_risk_pct")
    reg_risk = risk_info.get("regulatory_risk_pct")
    cons_risk = risk_info.get("consumer_risk_pct")
    
    print(f"=== {name} [{c}] ===")
    print(f"  Quality Score: {score}/100")
    print(f"  Verdict: {verdict} ({assessment})")
    print(f"  Overall Risk: {overall_risk}% (Ingredient: {ing_risk}%, Regulatory: {reg_risk}%, Consumer: {cons_risk}%)")
    print()
