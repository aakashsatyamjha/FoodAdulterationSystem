"""
Food Adulteration & Quality Knowledge Base Service
Analyzes ingredient text for suspicious substances, harmful additives,
and non-permitted adulterant markers according to FSSAI, FDA, and WHO standards.
"""

import re
from typing import List, Dict, Any

# Authoritative Adulterant & Hazardous Substances Database
ADULTERATION_PATTERNS = [
    {
        "pattern": r"(metanil\s*yellow|acid\s*yellow\s*36|ci\s*13065)",
        "name": "Metanil Yellow",
        "category_risk": "Spices (Turmeric), Sweets, Pulses",
        "hazard_type": "Prohibited Synthetic Non-Permitted Dye",
        "severity": "CRITICAL",
        "reason": "Non-permitted toxic dye frequently used illegally to color turmeric, dals, and biryani. Neurotoxic and hepatotoxic; strictly banned by FSSAI & FDA.",
        "confidence": 0.95
    },
    {
        "pattern": r"(sudan\s*(i|ii|iii|iv|dye|red)|solvent\s*red)",
        "name": "Sudan Dye (I - IV)",
        "category_risk": "Red Chilli Powder, Paprika",
        "hazard_type": "Carcinogenic Industrial Colorant",
        "severity": "CRITICAL",
        "reason": "Industrial azo chemical dye banned worldwide in food. Classified as Group 3 genotoxic carcinogen by IARC.",
        "confidence": 0.98
    },
    {
        "pattern": r"(lead\s*chromate|chrome\s*yellow)",
        "name": "Lead Chromate",
        "category_risk": "Turmeric, Yellow Spices",
        "hazard_type": "Heavy Metal Poisoning Agent",
        "severity": "CRITICAL",
        "reason": "Extremely toxic chemical compound used by unethical manufacturers to brighten turmeric root powder. Causes severe neurological damage and kidney toxicity.",
        "confidence": 0.99
    },
    {
        "pattern": r"(argemone\s*(oil|mexicana))",
        "name": "Argemone Oil",
        "category_risk": "Mustard Oil, Edible Oils",
        "hazard_type": "Toxic Weed Oil Adulterant",
        "severity": "CRITICAL",
        "reason": "Toxic oil from Argemone mexicana weed; adulteration causes Epidemic Dropsy, cardiac arrest, and blindness. Strictly banned.",
        "confidence": 0.95
    },
    {
        "pattern": r"(potassium\s*bromate|e924)",
        "name": "Potassium Bromate (E924)",
        "category_risk": "Bakery, Bread, Buns",
        "hazard_type": "Banned Dough Conditioner / Potential Carcinogen",
        "severity": "HIGH",
        "reason": "Banned in India (FSSAI 2016) and the EU as a potential carcinogen (IARC 2B). Often illegally substituted in unbranded bakeries.",
        "confidence": 0.92
    },
    {
        "pattern": r"(detergent|caustic\s*soda|sodium\s*hydroxide\s*trace|urea)",
        "name": "Synthetic Milk Formulation Markers (Detergent/Urea)",
        "category_risk": "Dairy, Milk, Paneer",
        "hazard_type": "Synthetic Milk Chemical Adulterants",
        "severity": "CRITICAL",
        "reason": "Markers commonly used in spurious synthetic milk concoctions to artificially simulate density, lather, and nitrogen/protein content.",
        "confidence": 0.94
    },
    {
        "pattern": r"(melamine)",
        "name": "Melamine",
        "category_risk": "Milk, Infant Formula, Protein Powders",
        "hazard_type": "Illegal Protein Spiker / Kidney Toxin",
        "severity": "CRITICAL",
        "reason": "Nitrogen-rich compound used fraudulently to artificially inflate apparent protein test readings (Kjeldahl method). Causes kidney stones and failure.",
        "confidence": 0.99
    },
    {
        "pattern": r"(mineral\s*oil|paraffin\s*oil|liquid\s*paraffin)",
        "name": "Mineral Oil / Liquid Paraffin",
        "category_risk": "Edible Oils, Black Pepper, Pulses",
        "hazard_type": "Petroleum Derivative / Non-Nutritive Adulterant",
        "severity": "HIGH",
        "reason": "Cheap hydrocarbon oil used to glaze pulses or dilute edible cooking oils. Impairs fat-soluble vitamin absorption and causes intestinal damage.",
        "confidence": 0.90
    },
    {
        "pattern": r"(chalk\s*powder|calcium\s*carbonate\s*filler|plaster\s*of\s*paris)",
        "name": "Chalk / Mineral Bulking Agents",
        "category_risk": "Flour, Milk, Spices, Sugar",
        "hazard_type": "Inorganic Filler Adulteration",
        "severity": "HIGH",
        "reason": "Insoluble mineral powders added to bulk out flour, sugar, or dairy products for weight fraud.",
        "confidence": 0.88
    },
    {
        "pattern": r"(titanium\s*dioxide|e171)",
        "name": "Titanium Dioxide (E171)",
        "category_risk": "Confectionery, Sauces, White Glazes",
        "hazard_type": "Banned Food Whitening Agent (EU Banned)",
        "severity": "MEDIUM",
        "reason": "Nanoparticle whitening agent banned in the European Union in 2022 due to genotoxicity concerns.",
        "confidence": 0.85
    }
]

# Concerning Additives & Ultra-Processing Markers
CONCERNING_ADDITIVES = [
    {
        "pattern": r"(tbhq|tertiary\s*butylhydroquinone|e319)",
        "name": "TBHQ (Tertiary Butylhydroquinone / E319)",
        "type": "Synthetic Antioxidant / Preservative",
        "risk_level": "Moderate",
        "concern": "High doses linked to cellular damage, vision disturbances, and biochemical stress. Recommended intake must not be exceeded."
    },
    {
        "pattern": r"(bha|butylated\s*hydroxyanisole|e320|bht|butylated\s*hydroxytoluene|e321)",
        "name": "BHA / BHT (E320 / E321)",
        "type": "Synthetic Preservative",
        "risk_level": "Moderate",
        "concern": "Suspected endocrine disruptors and potential carcinogens according to several international toxicology panels."
    },
    {
        "pattern": r"(tartrazine|yellow\s*5|e102)",
        "name": "Tartrazine (FD&C Yellow 5 / E102)",
        "type": "Synthetic Azo Dye",
        "risk_level": "Moderate",
        "concern": "Linked to hyperactivity in sensitive children (Southampton Study warning) and allergic hives/asthma flare-ups."
    },
    {
        "pattern": r"(sunset\s*yellow\s*fcf|yellow\s*6|e110)",
        "name": "Sunset Yellow FCF (Yellow 6 / E110)",
        "type": "Synthetic Azo Dye",
        "risk_level": "Moderate",
        "concern": "Mandatory warning label in Europe: 'May have an adverse effect on activity and attention in children'."
    },
    {
        "pattern": r"(allura\s*red|red\s*40|e129)",
        "name": "Allura Red AC (Red 40 / E129)",
        "type": "Synthetic Petroleum-Derived Dye",
        "risk_level": "Moderate",
        "concern": "Petroleum-derived coloring agent; linked to gut inflammation and behavioral sensitivity."
    },
    {
        "pattern": r"(brilliant\s*blue\s*fcf|blue\s*1|e133)",
        "name": "Brilliant Blue FCF (Blue 1 / E133)",
        "type": "Synthetic Triarylmethane Dye",
        "risk_level": "Low-to-Moderate",
        "concern": "Poorly absorbed synthetic colorant with hypersensitivity risks."
    },
    {
        "pattern": r"(caramel\s*(color\s*)?(iii|iv|3|4)|e150c|e150d|ammonia\s*caramel)",
        "name": "Caramel Color IV (Sulfite Ammonia Caramel / E150d)",
        "type": "Processed Colorant",
        "risk_level": "Moderate",
        "concern": "Manufacturing byproducts may contain 4-MEI (4-Methylimidazole), listed by California Proposition 65 as a potential carcinogen."
    },
    {
        "pattern": r"(aspartame|e951|acesulfame\s*(potassium|k)|e950|sucralose|e955)",
        "name": "Intense Artificial Sweeteners (Aspartame/Ace-K/Sucralose)",
        "type": "Non-Nutritive Sweetener",
        "risk_level": "Moderate",
        "concern": "IARC classified Aspartame as 2B ('possibly carcinogenic to humans'). Emerging research shows disruption of gut microbiome diversity."
    },
    {
        "pattern": r"(partially\s*hydrogenated|hydrogenated\s*vegetable\s*oil|vanaspati|trans\s*fat)",
        "name": "Partially Hydrogenated Oils / Industrial Trans Fat",
        "type": "Dangerous Lipid Derivative",
        "risk_level": "High",
        "concern": "WHO REPLACE campaign goal: eliminate industrial trans fats globally. Dramatically raises LDL cholesterol and coronary heart disease risk."
    },
    {
        "pattern": r"(high\s*fructose\s*corn\s*syrup|hfcs|liquid\s*glucose|invert\s*sugar)",
        "name": "High Fructose Corn Syrup / Refined Liquid Syrups",
        "type": "Refined Caloric Sweetener",
        "risk_level": "Moderate",
        "concern": "Rapidly metabolizes in the liver; linked to non-alcoholic fatty liver disease (NAFLD), insulin resistance, and visceral obesity."
    },
    {
        "pattern": r"(monosodium\s*glutamate|msg|flavor\s*enhancer\s*621|e621)",
        "name": "Monosodium Glutamate (MSG / E621)",
        "type": "Flavor Enhancer",
        "risk_level": "Low-to-Moderate",
        "concern": "May induce mild headache, flushing, or sweating in sensitive individuals ('MSG symptom complex')."
    },
    {
        "pattern": r"(sodium\s*benzoate|e211|potassium\s*sorbate|e202)",
        "name": "Benzoates & Sorbates (E211 / E202)",
        "type": "Chemical Preservative",
        "risk_level": "Low-to-Moderate",
        "concern": "When Sodium Benzoate is combined with ascorbic acid (Vitamin C) in acidic beverages, trace levels of benzene (a known carcinogen) may form."
    },
    {
        "pattern": r"(palm\s*oil|palm\s*olein|palmolein)",
        "name": "Palm Oil / Palm Olein",
        "type": "High Saturated Fat Oil",
        "risk_level": "Low-to-Moderate",
        "concern": "Contains ~50% saturated palmitic acid. Environmental and cardiovascular concerns when consumed excessively."
    }
]

# Common Allergens
COMMON_ALLERGENS = [
    {"name": "Gluten / Wheat", "pattern": r"(wheat|gluten|barley|rye|spelt|semolina|maida)"},
    {"name": "Dairy / Milk", "pattern": r"(milk|cream|cheese|butter|casein|whey|lactose)"},
    {"name": "Peanuts", "pattern": r"(peanut|groundnut|arachis)"},
    {"name": "Tree Nuts", "pattern": r"(almond|walnut|cashew|pistachio|hazelnut|macadamia)"},
    {"name": "Soy", "pattern": r"(soy|soya|soybean|lecithin)"},
    {"name": "Eggs", "pattern": r"(egg|albumin|egg\s*powder)"},
    {"name": "Fish & Seafood", "pattern": r"(fish|prawn|shrimp|crab|crustacean)"},
    {"name": "Sulfites", "pattern": r"(sulfite|sulphite|metabisulphite|e220|e221|e222|e223|e224)"}
]

def analyze_ingredients_text(ingredients_raw: str, category: str = "General") -> Dict[str, Any]:
    """
    Parses and cross-references ingredient list against adulterants and concerning additives.
    """
    if not ingredients_raw:
        return {
            "parsed_ingredients": [],
            "adulteration_indicators": [],
            "concerning_additives": [],
            "detected_allergens": [],
            "has_critical_flags": False,
            "adulteration_confidence": 0.0,
            "risk_verdict": "Low Risk",
            "safety_disclaimer": DISCLAIMER_TEXT
        }

    text_lower = ingredients_raw.lower()
    
    # Clean and split into individual ingredient tokens
    split_tokens = re.split(r"[,;:\n\r\(\)]+", text_lower)
    parsed_ingredients = [t.strip() for t in split_tokens if len(t.strip()) > 1]

    # 1. Adulteration Detection
    adulteration_flags = []
    max_adulteration_conf = 0.0

    for item in ADULTERATION_PATTERNS:
        match = re.search(item["pattern"], text_lower)
        if match:
            adulteration_flags.append({
                "substance": item["name"],
                "matched_text": match.group(0),
                "hazard_type": item["hazard_type"],
                "severity": item["severity"],
                "reason": item["reason"],
                "confidence": item["confidence"],
                "target_category": item["category_risk"]
            })
            if item["confidence"] > max_adulteration_conf:
                max_adulteration_conf = item["confidence"]

    # 2. Additive & Quality Issues Detection
    concerning_additives = []
    for add in CONCERNING_ADDITIVES:
        match = re.search(add["pattern"], text_lower)
        if match:
            concerning_additives.append({
                "name": add["name"],
                "matched_text": match.group(0),
                "type": add["type"],
                "risk_level": add["risk_level"],
                "concern": add["concern"]
            })

    # 3. Allergen Detection
    detected_allergens = []
    for allergen in COMMON_ALLERGENS:
        if re.search(allergen["pattern"], text_lower):
            detected_allergens.append(allergen["name"])

    # Categorize overall screening status
    has_critical = len(adulteration_flags) > 0
    if has_critical:
        risk_verdict = "High Risk"
    elif len(concerning_additives) >= 3:
        risk_verdict = "Moderate Risk"
    elif len(concerning_additives) > 0:
        risk_verdict = "Moderate Risk"
    else:
        risk_verdict = "Low Risk"

    return {
        "parsed_ingredients": parsed_ingredients[:35],
        "adulteration_indicators": adulteration_flags,
        "concerning_additives": concerning_additives,
        "detected_allergens": detected_allergens,
        "has_critical_flags": has_critical,
        "adulteration_confidence": round(max_adulteration_conf, 2),
        "risk_verdict": risk_verdict,
        "safety_disclaimer": DISCLAIMER_TEXT
    }

DISCLAIMER_TEXT = (
    "AI-BASED SCREENING ASSESSMENT NOTICE: This evaluation is generated via artificial intelligence, "
    "optical character recognition, and food safety heuristics. The flags displayed represent potential "
    "risk indicators and formulation screening based on listed ingredients. It does NOT constitute a legally "
    "certified laboratory chemical confirmation of adulteration."
)
