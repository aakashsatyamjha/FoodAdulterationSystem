"""
Context-Aware Food Safety Assistant Service (FoodGuard AI Assistant)
Provides intelligent, multi-criteria reasoning for product inquiries, cross-country regulatory comparisons,
health risk drivers, ingredient functions, and consumer dietary suitability.
"""

import re
from typing import Dict, Any, List, Optional
from .ingredient_intelligence import INGREDIENT_DATABASE, get_ingredient_by_id, search_ingredients

def process_chat_message(
    user_query: str,
    context: Optional[Dict[str, Any]] = None,
    history: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Analyzes user message within the context of active product analysis report,
    global regulatory rules, risk drivers, and consumer preferences.
    """
    query = (user_query or "").strip().lower()
    product = context.get("currentAnalysis") if context else None
    user_prefs = context.get("userPreferences") if context else None
    
    product_card = None
    ingredient_card = None
    followup_suggestions = []
    response_text = ""

    # Attach Product Context Card if product is available in conversation context
    if product:
        product_card = {
            "name": product.get("product_name", "Packaged Product"),
            "brand": product.get("brand", "N/A"),
            "score": product.get("quality_score", 50),
            "risk": product.get("final_verdict_badge") or product.get("risk_level", "Moderate Risk"),
            "category": product.get("category", "Packaged Food")
        }

    # ─────────────────────────────────────────────────────────────
    # CONTEXT-AWARE QUERY RESOLUTION (Product in Active Session)
    # ─────────────────────────────────────────────────────────────
    
    # Question 1: "Why did this product get [score]?" / "Why this score?" / "Explain score"
    if product and any(p in query for p in ["why did this product get", "why this score", "why the score", "explain score", "score breakdown", "how did foodguard reach"]):
        score = product.get("quality_score", 50)
        overall = product.get("overall_assessment") or product.get("final_explanation", "")
        
        # Risk breakdown
        risk_obj = product.get("risk", {})
        neg_factors = risk_obj.get("negative_factors", product.get("negative_factors", []))
        pos_factors = risk_obj.get("positive_factors", product.get("positive_factors", []))
        
        # Adulteration & Regulatory
        adult_obj = product.get("adulteration", {})
        reg_obj = product.get("regulatory", {})
        selected_c = reg_obj.get("selected_country", {})

        response_text = (
            f"**Food Safety & Quality Score Breakdown for {product.get('product_name', 'this product')} ({score}/100):**\n\n"
            f"• **Overall Multi-Criteria Verdict:** {product.get('final_verdict_badge', 'Assessed')} - *{product.get('final_explanation', '')}*\n"
            f"• **Adulteration Status:** {adult_obj.get('status', 'Screened')} ({adult_obj.get('summary', 'No critical industrial markers')})\n"
            f"• **Regulatory Compliance ({selected_c.get('country_name', 'Selected Region')}):** {selected_c.get('verdict', 'Evaluated')} ({selected_c.get('summary', '')})\n"
            f"• **Risk Multi-Tier Breakdown:** Overall Risk {risk_obj.get('overall_risk_pct', 50)}% | Ingredient Risk {risk_obj.get('ingredient_risk_pct', 40)}% | Regulatory Risk {risk_obj.get('regulatory_risk_pct', 30)}% | Consumer Risk {risk_obj.get('consumer_risk_pct', 30)}%.\n\n"
        )
        if neg_factors:
            response_text += "**Key Risk Factors Impacting Score:**\n" + "\n".join([f"  - ⚠️ {factor}" for factor in neg_factors[:4]]) + "\n\n"
        if pos_factors:
            response_text += "**Positive Nutritional Drivers:**\n" + "\n".join([f"  - ✓ {factor}" for factor in pos_factors[:3]]) + "\n"

        followup_suggestions = [
            "Which ingredient caused the regulatory warning?",
            "Is this product allowed in Germany or the EU?",
            "Is this suitable for my dietary preferences?"
        ]

    # Question 2: Cross-Country Regulatory Differences / Country Legality
    elif any(p in query for p in ["germany", "eu", "usa", "america", "india", "uk", "allowed in", "permitted in", "legal in", "cross-country", "why different"]):
        # Check target country
        target_country = "Germany / EU"
        if "usa" in query or "america" in query: target_country = "USA (FDA)"
        elif "india" in query: target_country = "India (FSSAI)"
        elif "germany" in query: target_country = "Germany (BVL)"
        elif "eu" in query or "europe" in query: target_country = "European Union (EFSA)"
        elif "uk" in query: target_country = "United Kingdom (FSA)"

        if product and "regulatory" in product:
            reg_data = product["regulatory"]
            div_ings = reg_data.get("divergent_ingredients", [])
            selected_eval = reg_data.get("selected_country", {})

            if div_ings:
                response_text = (
                    f"**Global Regulatory Comparison for {product.get('product_name', 'this product')} regarding {target_country}:**\n\n"
                    f"The analysis identified **{len(div_ings)} ingredient(s)** with significant international regulatory divergences:\n\n"
                )
                for div in div_ings[:3]:
                    response_text += (
                        f"• **{div['name']} ({div.get('ins_e_number', '')})**:\n"
                        f"  - *Divergence Reason:* {div['reason']}\n"
                        f"  - *Evidence Source:* {div['source']}\n"
                    )
                response_text += (
                    f"\n**Verdict for {selected_eval.get('country_name', 'Selected Region')} ({selected_eval.get('authority', 'Agency')}):** "
                    f"`{selected_eval.get('verdict', 'PASS')}` - {selected_eval.get('summary', '')}"
                )
            else:
                response_text = (
                    f"**Global Regulatory Compliance for {product.get('product_name', 'this product')} in {target_country}:**\n\n"
                    f"All recognized ingredients in this product formulation meet the baseline food additive standards under {target_country} regulatory frameworks without critical cross-border conflicts."
                )
        else:
            response_text = (
                f"**Why do food regulations differ between India, USA, EU, and Germany?**\n\n"
                f"• **Precautionary Principle (EU / Germany / EFSA):** The EU bans or mandates warning labels on additives (e.g. Titanium Dioxide E171, Potassium Bromate, Southampton azo dyes) whenever potential genotoxicity or child behavioral risks arise.\n"
                f"• **Risk Assessment Approach (US FDA):** The US FDA requires definitive proof of significant consumer harm before enacting federal bans, allowing substances like Titanium Dioxide (up to 1%) and Azodicarbonamide.\n"
                f"• **FSSAI Standards (India):** Focuses heavily on combating economic food adulteration (banning non-permitted toxic industrial dyes like Metanil Yellow, Sudan dyes, and Lead Chromate) while maintaining quantitative limits on synthetic colors and preservatives."
            )

        followup_suggestions = [
            "Why is Titanium Dioxide banned in the EU?",
            "What is the difference between FSSAI and FDA standards?",
            "Why did this product get this score?"
        ]

    # Question 3: Consumer Dietary Preferences Suitability
    elif any(p in query for p in ["suitable", "preference", "vegan", "vegetarian", "low sugar", "low sodium", "gluten", "diabetic", "can i eat"]):
        if product and "consumer" in product:
            cons = product["consumer"]
            concerns = cons.get("concerns", [])
            matched = cons.get("matched_preferences", [])
            allergens = cons.get("detected_allergens", [])

            response_text = f"**Consumer Preference & Suitability Report for {product.get('product_name', 'this product')}:**\n\n"
            if concerns:
                response_text += "**⚠️ Potential Preference Concerns:**\n" + "\n".join([f"• {c}" for c in concerns]) + "\n\n"
            if matched:
                response_text += "**✓ Matched Dietary Preferences:**\n" + "\n".join([f"• {m}" for m in matched]) + "\n\n"
            if allergens:
                response_text += f"**Regulated Allergens Detected:** {', '.join(allergens)}.\n\n"
            response_text += "*Note: FoodGuard provides educational screening against configured thresholds and does not provide individual medical diagnosis.*"
        else:
            response_text = (
                "**FoodGuard Consumer Intelligence Profile:**\n\n"
                "You can configure personalized dietary preferences in the **Consumer Intelligence** tab:\n"
                "• **Nutritional Ceilings:** Low Sugar (<= 5g/100g), Low Sodium (<= 140mg/100g), High Protein (>= 8g/100g)\n"
                "• **Dietary Frameworks:** Vegetarian, Vegan, Gluten-Free Awareness, Allergen Awareness\n"
                "• **Processing Preferences:** Low-Additive / Clean-Label preference\n\n"
                "Every scanned food will be individually checked against your active profile with transparent reasoning."
            )
        followup_suggestions = [
            "What are the high-sugar thresholds?",
            "How does FoodGuard detect hidden non-vegetarian ingredients?",
            "Which ingredient caused the regulatory warning?"
        ]

    # Question 4: Specific Ingredient Inquiries (e.g. "What is TBHQ?", "What is Tartrazine?")
    elif any(term in query for term in ["what is", "tell me about", "is", "explain"]) and any(ing["id"] in query or ing["common_name"].lower() in query for ing in INGREDIENT_DATABASE):
        matched_ing = None
        for ing in INGREDIENT_DATABASE:
            if ing["id"] in query or ing["common_name"].lower() in query or any(alias.lower() in query for alias in ing["aliases"]):
                matched_ing = ing
                break

        if matched_ing:
            ingredient_card = {
                "name": matched_ing["common_name"],
                "category": matched_ing["category"],
                "function": matched_ing["function"],
                "risk": matched_ing["risk_classification"],
                "ins": matched_ing["ins_e_number"]
            }
            response_text = (
                f"**Ingredient Intelligence: {matched_ing['common_name']} ({matched_ing['ins_e_number']})**\n\n"
                f"• **Function & Category:** {matched_ing['function']} ({matched_ing['category']})\n"
                f"• **Risk Classification:** {matched_ing['risk_classification']}\n"
                f"• **India (FSSAI) Status:** {matched_ing['india_status']['status']} - {matched_ing['india_status']['condition']}\n"
                f"• **USA (FDA) Status:** {matched_ing['usa_status']['status']} - {matched_ing['usa_status']['condition']}\n"
                f"• **EU (EFSA) Status:** {matched_ing['eu_status']['status']} - {matched_ing['eu_status']['condition']}\n"
                f"• **Germany (BVL) Status:** {matched_ing['germany_status']['status']} - {matched_ing['germany_status']['condition']}\n"
                f"• **Cross-Country Rationale:** {matched_ing['cross_country_reason']}\n"
                f"• **Evidence Citation:** *{matched_ing['evidence_source']}*"
            )
            followup_suggestions = [
                f"Why is {matched_ing['common_name']} regulated differently in the EU?",
                "What are concerning additives in packaged food?",
                "Scan a food product"
            ]
        else:
            response_text = "I could not find detailed specifications for that specific substance in the primary database."

    # Question 5: Adulteration & Chemical Screening (Metanil Yellow, Lead Chromate, Sudan, Urea)
    elif any(a in query for a in ["metanil", "lead chromate", "sudan", "adulterant", "adulteration", "urea", "argemone", "melamine"]):
        response_text = (
            "**Adulteration Screening & Prohibited Substances in FoodGuard:**\n\n"
            "FoodGuard continuously screens for known high-risk adulteration patterns:\n"
            "1. **Metanil Yellow & Lead Chromate in Turmeric/Spices:** Banned toxic industrial chemicals added for artificial yellow tint; strictly illegal and neurotoxic.\n"
            "2. **Sudan Dyes (I-IV) in Chilli:** Industrial carcinogenic solvent dyes added to exhausted red chilli powder.\n"
            "3. **Argemone Oil in Mustard Oil:** Toxic weed seed oil causing Epidemic Dropsy and cardiac failure.\n"
            "4. **Synthetic Milk Markers (Urea/Detergents):** Chemicals used to simulate protein readings and lather in counterfeit milk.\n\n"
            "*Important Safety Note: AI screening provides rapid preliminary identification. Laboratory chemical testing (HPLC, GC-MS, ICP-MS) is required for certified legal confirmation.*"
        )
        followup_suggestions = [
            "How do I test turmeric purity at home?",
            "What is FSSAI standard for spices?",
            "Why is Metanil Yellow banned?"
        ]

    # Default Educational AI Response Handler
    else:
        response_text = (
            "**FoodGuard AI Food Safety & Regulatory Intelligence Assistant**\n\n"
            "I can assist you across all four FoodGuard pillars:\n"
            "1. **Adulteration Screening:** Explain chemical adulterant signatures and home testing methods (FSSAI DART).\n"
            "2. **Health Risk Assessment:** Break down nutritional risk scores, bad fats, and additive densities.\n"
            "3. **Global Regulatory Compliance:** Compare regulatory legality across India (FSSAI), USA (FDA), EU (EFSA), and Germany (BVL).\n"
            "4. **Consumer Decision Support:** Evaluate whether a scanned product fits your active dietary preferences (Low Sugar, Low Sodium, Vegan, Vegetarian, Gluten-Free)."
        )
        followup_suggestions = [
            "Why did this product get its score?",
            "Is this product allowed in Germany?",
            "What are the four pillars of FoodGuard?"
        ]

    return {
        "response_text": response_text,
        "product_card": product_card,
        "ingredient_card": ingredient_card,
        "followup_suggestions": followup_suggestions
    }
