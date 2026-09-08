"""
FSSAI (Food Safety and Standards Authority of India) Explanation Service
Provides detailed reasoning for why the Indian Government / FSSAI has licensed
a particular packaged food product, and whether the product is adulterated or not.
Based on FSS Act 2006 and FSS Regulations 2011 (with amendments up to 2025).
"""

from typing import Dict, Any

# ---------------------------------------------------------------------------
# Category-specific FSSAI regulation mapping
# ---------------------------------------------------------------------------
_CATEGORY_RULES: Dict[str, Dict[str, Any]] = {
    "dairy": {
        "regulation": "FSS (Milk and Milk Products) Regulations 2.1.1",
        "why_approved": (
            "Dairy products are approved under FSS (Milk and Milk Products) Regulations because they meet "
            "minimum fat/SNF (Solids Not Fat) thresholds, pass microbiological safety tests (zero Salmonella / Listeria), "
            "and use only FSSAI-permitted processing aids. FSSAI ensures the product is free from synthetic milk "
            "adulterants such as urea, detergent, starch, and caustic soda."
        ),
        "key_standards": [
            "Cow milk: min 3.5% fat, 8.5% SNF (Solids Not Fat)",
            "Zero tolerance for urea, detergent, caustic soda, starch",
            "Reichert-Meissl value >= 28 for ghee purity",
            "Pasteurisation mandatory -- label must declare it",
        ],
    },
    "snack": {
        "regulation": "FSS (Food Products Standards) Regulation 2.12 -- Extruded and Fried Snacks",
        "why_approved": (
            "Snack products receive FSSAI approval when they use food-grade oils within permissible Total Polar Compound (TPC) "
            "limits (max 25% TPC for reused oil), restrict antioxidants (TBHQ/BHA) to <=200 mg/kg of fat, "
            "and declare all artificial colours and flavour enhancers. The product must be free from non-permitted dyes "
            "and industrial adulterants."
        ),
        "key_standards": [
            "TBHQ / BHA antioxidant limit: <= 200 mg/kg of fat",
            "Permitted colours (Sunset Yellow INS 110, Tartrazine INS 102) <= 100 mg/kg -- must be declared",
            "Reused cooking oil TPC limit: <= 25%",
            "Must display: vegetarian (green) or non-vegetarian (brown) symbol",
        ],
    },
    "beverage": {
        "regulation": "FSS Regulation 2.3.30 -- Carbonated and Non-Carbonated Beverages",
        "why_approved": (
            "Beverages are licensed by FSSAI after verifying that added sweeteners (Aspartame, Acesulfame-K, Sucralose) "
            "remain within maximum concentration limits, caffeine does not exceed 145 mg/kg (or 300 mg/kg for energy drinks), "
            "and caramel colouring (INS 150d) meets 4-MEI safety thresholds. Microbial counts (yeast/mould below 2 cfu/ml) are mandatory."
        ),
        "key_standards": [
            "Caffeine limit: <= 145 mg/kg (soft drinks), <= 300 mg/kg (energy drinks)",
            "Must label: 'Contains Artificial Sweetener' and 'Not Recommended for Children'",
            "Microbiological: Yeast/mould below 2 cfu/ml",
            "4-MEI threshold monitoring for caramel colour (INS 150d)",
        ],
    },
    "noodle": {
        "regulation": "FSS Regulation 2.4.6.1 -- Instant Noodles and Pasta",
        "why_approved": (
            "Instant noodles are approved because they comply with permitted acidity regulators (INS 500/501), "
            "humectants (INS 451), and flavour enhancers in tastemaker sachets. Lead levels must be below 2.5 mg/kg. "
            "FSSAI mandates labelling of MSG content and common allergens such as wheat (gluten)."
        ),
        "key_standards": [
            "Lead limit: below 2.5 mg/kg (post-2015 Maggi-era mandatory audit)",
            "Total dietary ash <= 0.5%; acid insoluble ash <= 0.1%",
            "Must declare: 'Contains / No Added MSG'",
            "Allergen: Wheat (Gluten) must be declared",
        ],
    },
    "bakery": {
        "regulation": "FSS Regulation 2.4.15 -- Bakery Products and Biscuits",
        "why_approved": (
            "Bakery products are licensed after verifying that raising agents (INS 503, INS 500), emulsifiers "
            "(Soy Lecithin INS 322), and any permitted preservatives are within GMP limits. "
            "Critically, FSSAI banned Potassium Bromate (E924) in all Indian bakery products since June 2016, "
            "and industrial trans-fat must not exceed 2% of total fat (FSSAI Jan 2022 mandate)."
        ),
        "key_standards": [
            "Potassium Bromate (E924) -- BANNED in India since June 2016",
            "Industrial trans-fat limit: <= 2% of total fat (from Jan 1, 2022)",
            "Must declare: Maida (refined wheat flour) percentage",
            "Vegetarian / Non-vegetarian symbol mandatory",
        ],
    },
    "spice": {
        "regulation": "FSS Regulation 2.9 -- Spices and Condiments",
        "why_approved": (
            "Spice products are approved when purity tests confirm minimum volatile oil content, curcuminoid levels, "
            "and the absence of non-permitted dyes (Metanil Yellow, Sudan dyes, Lead Chromate). "
            "Extraneous matter must be under 1% by weight. Products must carry an AGMARK / FSSAI certification number."
        ),
        "key_standards": [
            "Total ash <= 9.0% (turmeric), <= 8.0% (chilli powder)",
            "Zero tolerance for Metanil Yellow, Sudan dyes, Lead Chromate",
            "Extraneous matter <= 1.0% by weight",
            "Irradiation / ethylene oxide treatment must be disclosed on label",
        ],
    },
    "confectionery": {
        "regulation": "FSS (Food Products Standards) Regulation 2.7 -- Sugars and Confectionery",
        "why_approved": (
            "Confectionery items get FSSAI approval when they contain only permitted food colours within allowed limits, "
            "and artificial sweeteners (if used) are within maximum permissible levels. Products must clearly label "
            "allergens such as nuts, milk, and gelatin source (vegetarian/non-vegetarian)."
        ),
        "key_standards": [
            "Azo dyes (Tartrazine, Sunset Yellow) <= 100 mg/kg -- must be labelled",
            "Saccharin <= 500 mg/kg; Aspartame <= 10,000 mg/kg",
            "Heavy metals (Lead below 2.5 ppm, Arsenic below 1.1 ppm)",
            "Gelatin source (bovine/porcine) must be declared",
        ],
    },
    "generic": {
        "regulation": "FSS (Licensing and Registration of Food Businesses) Regulations 2011",
        "why_approved": (
            "Packaged food products in India must obtain a Central or State FSSAI licence depending on their annual turnover. "
            "Approval is granted when the business demonstrates compliance with GMP (Good Manufacturing Practices), "
            "uses only ingredients from the FSSAI positive list (Schedules A and B), and ensures heavy metals, "
            "pesticide residues, and microbiological counts are within statutory limits. "
            "The 14-digit FSSAI licence number printed on the pack is proof of this certification."
        ),
        "key_standards": [
            "Heavy metals: Lead below 2.5 ppm, Arsenic below 1.1 ppm, Cadmium below 1.5 ppm",
            "Pesticide residues must be below MRLs (Maximum Residue Limits)",
            "Only FSSAI Schedule A and B ingredients / additives permitted",
            "14-digit FSSAI licence number mandatory on pack",
        ],
    },
}

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_fssai_info(
    product_name: str,
    category: str,
    adulteration_indicators: list,
    risk_level: str,
) -> Dict[str, Any]:
    """
    Return structured FSSAI regulatory context for display in the Product Analysis UI.

    Returns a dict with:
      - approved (bool)              : whether product appears compliant
      - licence_status (str)         : short status label
      - regulation (str)             : specific FSS regulation reference
      - why_approved (str)           : detailed human-readable explanation
      - key_standards (list)         : bullet points of numerical / categorical thresholds
      - adulteration_verdict (str)   : plain-English verdict on whether the product is adulterated
      - consumer_note (str)          : safety vs health distinction notice
    """
    cat_lower = (category or "").lower()

    # Pick the closest category rules
    rules = _CATEGORY_RULES["generic"]
    for key in _CATEGORY_RULES:
        if key in cat_lower:
            rules = _CATEGORY_RULES[key]
            break

    is_adulterated = len(adulteration_indicators) > 0
    is_high_risk = "high" in (risk_level or "").lower()

    if is_adulterated:
        licence_status = "NON-COMPLIANT / POTENTIAL FSSAI VIOLATION"
        approved = False
        adulteration_verdict = (
            f"{product_name} has FAILED adulteration screening. "
            "The presence of prohibited substances violates Section 59 of the Food Safety and Standards Act (2006). "
            "Such products are subject to immediate recall, prosecution, and cancellation of FSSAI licence. "
            "DO NOT CONSUME -- report to FSSAI Helpline 1800-112-100."
        )
    elif is_high_risk:
        licence_status = "CAUTION -- Elevated Risk Profile"
        approved = True
        adulteration_verdict = (
            f"{product_name} did not trigger banned-substance flags, meaning it is not overtly adulterated. "
            "However, its nutritional or additive profile places it in the High Risk category. "
            "It likely contains industrial additives, high sugar / sodium, or trans-fats that remain technically "
            "within FSSAI-permitted GMP limits but are not ideal for regular consumption."
        )
    else:
        licence_status = "FSSAI LICENSED AND MARKET-PERMITTED"
        approved = True
        adulteration_verdict = (
            f"{product_name} passed AI-based adulteration screening. "
            "No banned dyes, synthetic adulterants, or prohibited heavy metal markers were detected. "
            "The product appears compliant with Indian food safety standards for its category. "
            "(Note: AI screening is indicative -- a certified NABL-accredited lab test provides legal confirmation.)"
        )

    consumer_note = (
        "FSSAI approval means the product is manufactured under Good Manufacturing Practices (GMP) and is "
        "safe from acute toxicity or adulteration. It does NOT guarantee that the product is 'healthy' "
        "for daily consumption -- high sugar, sodium, or saturated fat content are dietary moderation concerns, "
        "which is exactly why FSSAI mandates Nutritional Facts labelling on every pack."
    )

    return {
        "approved": approved,
        "licence_status": licence_status,
        "regulation": rules["regulation"],
        "why_approved": rules["why_approved"],
        "key_standards": rules["key_standards"],
        "adulteration_verdict": adulteration_verdict,
        "consumer_note": consumer_note,
    }


def get_fssai_reason(product_name: str, category: str) -> str:
    """Backwards-compatible helper -- returns plain text explanation."""
    info = get_fssai_info(product_name, category, [], "Low Risk")
    return info["why_approved"]
