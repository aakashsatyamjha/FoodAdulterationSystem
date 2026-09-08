"""
Global Regulatory Compliance & Cross-Country Comparison Service
Evaluates ingredient compliance against regulatory frameworks across
India (FSSAI), USA (FDA), EU (EFSA), Germany (BVL), and UK (FSA).
"""

from typing import List, Dict, Any, Optional
from .ingredient_intelligence import (
    INGREDIENT_DATABASE,
    SUPPORTED_COUNTRIES,
    get_ingredient_by_id,
    match_ingredient_text
)

# Standardized Status Display Badges & Icons
STATUS_BADGES = {
    "PERMITTED": {
        "label": "Permitted",
        "symbol": "✓",
        "badge_class": "bg-emerald-500/15 text-emerald-500 border-emerald-500/30",
        "category": "pass"
    },
    "PERMITTED_WITH_LIMITS": {
        "label": "Permitted with limits",
        "symbol": "⚠",
        "badge_class": "bg-amber-500/15 text-amber-500 border-amber-500/30",
        "category": "conditional"
    },
    "PERMITTED_WITH_CONDITIONS": {
        "label": "Permitted with conditions / Warning required",
        "symbol": "⚠",
        "badge_class": "bg-amber-500/15 text-amber-500 border-amber-500/30",
        "category": "conditional"
    },
    "RESTRICTED": {
        "label": "Category-specific restriction",
        "symbol": "⚠",
        "badge_class": "bg-orange-500/15 text-orange-500 border-orange-500/30",
        "category": "conditional"
    },
    "NOT_PERMITTED": {
        "label": "Not permitted / Not authorised / Banned",
        "symbol": "✕",
        "badge_class": "bg-rose-500/15 text-rose-500 border-rose-500/30",
        "category": "fail"
    },
    "VERIFICATION_REQUIRED": {
        "label": "Verification required",
        "symbol": "○",
        "badge_class": "bg-blue-500/15 text-blue-500 border-blue-500/30",
        "category": "unknown"
    },
    "INSUFFICIENT_DATA": {
        "label": "Insufficient data in dataset",
        "symbol": "?",
        "badge_class": "bg-slate-500/15 text-slate-400 border-slate-500/30",
        "category": "unknown"
    }
}

COUNTRY_MAP = {
    "IN": "india_status",
    "INDIA": "india_status",
    "US": "usa_status",
    "USA": "usa_status",
    "EU": "eu_status",
    "DE": "germany_status",
    "GERMANY": "germany_status",
    "UK": "uk_status"
}

def get_country_status_key(country_code: str) -> str:
    return COUNTRY_MAP.get(country_code.upper().strip(), "india_status")

def evaluate_country_compliance(
    ingredients_text: str,
    country_code: str = "IN",
    category: str = "Packaged Food"
) -> Dict[str, Any]:
    """
    Evaluates whether a food product is permitted, conditional, or not permitted in a specific country.
    Returns structured checklist and transparent justification.
    """
    country_key = get_country_status_key(country_code)
    country_meta = next((c for c in SUPPORTED_COUNTRIES if c["code"] == country_code.upper() or c["name"].upper() == country_code.upper()), SUPPORTED_COUNTRIES[0])

    matched_ingredients = match_ingredient_text(ingredients_text)
    
    passed_criteria = []
    conditional_criteria = []
    failed_criteria = []
    
    # 1. Base criteria: Ingredients recognition
    if matched_ingredients:
        passed_criteria.append({
            "title": "Ingredient Identification",
            "detail": f"Recognized {len(matched_ingredients)} categorized substances in ingredient intelligence database."
        })
    else:
        passed_criteria.append({
            "title": "Standard Whole Food Formulation",
            "detail": "Formulation consists of conventional dietary ingredients with zero high-risk additives or restricted substances flagged."
        })

    # 2. Check each matched ingredient against country status
    for item in matched_ingredients:
        c_status = item.get(country_key, {})
        status_code = c_status.get("code", "INSUFFICIENT_DATA")
        status_text = c_status.get("status", "Unknown")
        condition = c_status.get("condition", "")
        max_limit = c_status.get("max_limit", "")
        source = c_status.get("source", "")
        ing_name = item["common_name"]

        if status_code == "NOT_PERMITTED":
            failed_criteria.append({
                "ingredient": ing_name,
                "ins_e_number": item["ins_e_number"],
                "status": status_text,
                "status_code": status_code,
                "title": f"{ing_name} is not permitted or prohibited",
                "detail": condition or f"Prohibited under {country_meta['authority']} regulations ({max_limit}).",
                "source": source
            })
        elif status_code in ["PERMITTED_WITH_LIMITS", "PERMITTED_WITH_CONDITIONS", "RESTRICTED"]:
            conditional_criteria.append({
                "ingredient": ing_name,
                "ins_e_number": item["ins_e_number"],
                "status": status_text,
                "status_code": status_code,
                "title": f"{ing_name} permitted under specific limits/conditions",
                "detail": condition or f"Permissible limit: {max_limit}.",
                "source": source
            })
        elif status_code == "PERMITTED":
            passed_criteria.append({
                "ingredient": ing_name,
                "ins_e_number": item["ins_e_number"],
                "status": status_text,
                "status_code": status_code,
                "title": f"{ing_name} authorized for use",
                "detail": condition or f"Complies with {country_meta['authority']} standards under GMP.",
                "source": source
            })

    # 3. Determine Overall Country Verdict
    if failed_criteria:
        verdict = "FAIL"
        verdict_text = "Regulatory Screening: Potential Non-Compliance"
        summary = f"Contains {len(failed_criteria)} substance(s) not authorised or restricted under {country_meta['name']} ({country_meta['authority']}) standards."
    elif conditional_criteria:
        verdict = "CONDITIONAL"
        verdict_text = "Regulatory Screening: Conditional / Limits Apply"
        summary = f"Permitted in {country_meta['name']} subject to quantitative limits ({len(conditional_criteria)} condition(s) detected)."
    else:
        verdict = "PASS"
        verdict_text = "Regulatory Screening: Compliant under Available Dataset"
        summary = f"All recognized ingredients are authorized under {country_meta['name']} ({country_meta['authority']}) regulations."

    return {
        "country_code": country_meta["code"],
        "country_name": country_meta["name"],
        "authority": country_meta["authority"],
        "full_authority": country_meta["full_authority"],
        "framework": country_meta["framework"],
        "flag": country_meta["flag"],
        "verdict": verdict,
        "verdict_text": verdict_text,
        "summary": summary,
        "passed_criteria": passed_criteria,
        "conditional_criteria": conditional_criteria,
        "failed_criteria": failed_criteria,
        "total_criteria_evaluated": len(passed_criteria) + len(conditional_criteria) + len(failed_criteria)
    }

def build_cross_country_comparison(ingredients_text: str) -> Dict[str, Any]:
    """
    Generates a matrix comparing regulatory status across all supported countries
    (India, USA, EU, Germany, UK) for every recognized ingredient.
    Highlights cross-country differences and provides evidence-backed explanations.
    """
    matched_ingredients = match_ingredient_text(ingredients_text)
    
    matrix_rows = []
    divergent_ingredients = []

    for item in matched_ingredients:
        in_status = item.get("india_status", {})
        us_status = item.get("usa_status", {})
        eu_status = item.get("eu_status", {})
        de_status = item.get("germany_status", {})
        uk_status = item.get("uk_status", {})

        in_code = in_status.get("code", "INSUFFICIENT_DATA")
        us_code = us_status.get("code", "INSUFFICIENT_DATA")
        eu_code = eu_status.get("code", "INSUFFICIENT_DATA")
        de_code = de_status.get("code", "INSUFFICIENT_DATA")
        uk_code = uk_status.get("code", "INSUFFICIENT_DATA")

        # Check if countries disagree in classification
        unique_codes = {in_code, us_code, eu_code, de_code, uk_code}
        has_divergence = len(unique_codes) > 1

        row = {
            "id": item["database_id"],
            "common_name": item["common_name"],
            "scientific_name": item["scientific_name"],
            "ins_e_number": item["ins_e_number"],
            "category": item["category"],
            "function": item["function"],
            "risk": item["risk_classification"],
            "has_divergence": has_divergence,
            "cross_country_reason": item.get("cross_country_reason") or "Reason not available in current dataset.",
            "evidence_source": item.get("evidence_source", "Regulatory Toxicology Literature"),
            "statuses": {
                "IN": {
                    "country": "India",
                    "authority": "FSSAI",
                    "status": in_status.get("status", "Unknown"),
                    "code": in_code,
                    "badge": STATUS_BADGES.get(in_code, STATUS_BADGES["INSUFFICIENT_DATA"]),
                    "limit": in_status.get("max_limit", ""),
                    "condition": in_status.get("condition", ""),
                    "source": in_status.get("source", "")
                },
                "US": {
                    "country": "USA",
                    "authority": "FDA",
                    "status": us_status.get("status", "Unknown"),
                    "code": us_code,
                    "badge": STATUS_BADGES.get(us_code, STATUS_BADGES["INSUFFICIENT_DATA"]),
                    "limit": us_status.get("max_limit", ""),
                    "condition": us_status.get("condition", ""),
                    "source": us_status.get("source", "")
                },
                "EU": {
                    "country": "European Union",
                    "authority": "EFSA",
                    "status": eu_status.get("status", "Unknown"),
                    "code": eu_code,
                    "badge": STATUS_BADGES.get(eu_code, STATUS_BADGES["INSUFFICIENT_DATA"]),
                    "limit": eu_status.get("max_limit", ""),
                    "condition": eu_status.get("condition", ""),
                    "source": eu_status.get("source", "")
                },
                "DE": {
                    "country": "Germany",
                    "authority": "BVL",
                    "status": de_status.get("status", "Unknown"),
                    "code": de_code,
                    "badge": STATUS_BADGES.get(de_code, STATUS_BADGES["INSUFFICIENT_DATA"]),
                    "limit": de_status.get("max_limit", ""),
                    "condition": de_status.get("condition", ""),
                    "source": de_status.get("source", "")
                },
                "UK": {
                    "country": "United Kingdom",
                    "authority": "FSA",
                    "status": uk_status.get("status", "Unknown"),
                    "code": uk_code,
                    "badge": STATUS_BADGES.get(uk_code, STATUS_BADGES["INSUFFICIENT_DATA"]),
                    "limit": uk_status.get("max_limit", ""),
                    "condition": uk_status.get("condition", ""),
                    "source": uk_status.get("source", "")
                }
            }
        }
        matrix_rows.append(row)

        if has_divergence:
            divergent_ingredients.append({
                "name": item["common_name"],
                "ins_e_number": item["ins_e_number"],
                "reason": item.get("cross_country_reason", "Regulatory standards and acceptable daily intakes differ between regional food safety agencies."),
                "source": item.get("evidence_source", "Official Gazette / EFSA / FDA"),
                "statuses": row["statuses"]
            })

    # Summary stats across countries
    country_summaries = {}
    for c in SUPPORTED_COUNTRIES:
        code = c["code"]
        eval_res = evaluate_country_compliance(ingredients_text, country_code=code)
        country_summaries[code] = {
            "country_name": c["name"],
            "authority": c["authority"],
            "flag": c["flag"],
            "verdict": eval_res["verdict"],
            "verdict_text": eval_res["verdict_text"],
            "failed_count": len(eval_res["failed_criteria"]),
            "conditional_count": len(eval_res["conditional_criteria"]),
            "passed_count": len(eval_res["passed_criteria"])
        }

    return {
        "matrix": matrix_rows,
        "divergent_ingredients": divergent_ingredients,
        "divergence_count": len(divergent_ingredients),
        "total_ingredients_analyzed": len(matched_ingredients),
        "country_summaries": country_summaries,
        "supported_countries": SUPPORTED_COUNTRIES
    }
