"""
Open Food Facts Service & Offline Catalog
Retrieves real-time product information from Open Food Facts API
with an offline fallback catalog of popular packaged foods and test cases.
"""

import requests
from typing import Dict, Any, Optional

# Rich catalog of popular packaged foods for reliable offline/instant testing
OFFLINE_PRODUCT_CATALOG = {
    "8901058852813": {
        "barcode": "8901058852813",
        "product_name": "Maggi 2-Minute Masala Noodles",
        "brand": "Nestle",
        "category": "Instant Noodles & Snacks",
        "ingredients": "Refined wheat flour (Maida), Palm oil, Iodised salt, Wheat gluten, Mineral (Calcium carbonate), Thickeners (508, 412), Acidity regulators (501(i), 500(i)), Humectant (451(i)), Hydrolysed groundnut protein, Mixed spices (Dehydrated onion, Coriander powder, Red chilli powder, Turmeric powder, Dried garlic, Cumin powder, Aniseed, Black pepper, Fenugreek, Ginger, Clove, Nutmeg, Cardamom), Noodle powder, Sugar, Edible starch, Flavour enhancer (635), Palm oil, Colour (150d).",
        "nutrition": {
            "energy_kcal": 427,
            "sugar_g": 2.2,
            "sodium_mg": 1020,
            "saturated_fat_g": 6.8,
            "trans_fat_g": 0.12,
            "protein_g": 8.0,
            "fiber_g": 3.6
        },
        "image_url": "https://images.openfoodfacts.org/images/products/890/105/885/2813/front_en.11.400.jpg"
    },
    "7622210817014": {
        "barcode": "7622210817014",
        "product_name": "Oreo Original Sandwich Cookies",
        "brand": "Cadbury / Mondelez",
        "category": "Biscuits & Confectionery",
        "ingredients": "Wheat flour, Sugar, Palm oil, Rapeseed oil, Fat-reduced cocoa powder 4.5 %, Wheat starch, Glucose-fructose syrup, Raising agents (potassium carbonates, ammonium carbonates, sodium carbonates), Salt, Emulsifiers (soya lecithin, sunflower lecithin), Flavouring (vanillin).",
        "nutrition": {
            "energy_kcal": 471,
            "sugar_g": 38.0,
            "sodium_mg": 380,
            "saturated_fat_g": 5.2,
            "trans_fat_g": 0.0,
            "protein_g": 5.4,
            "fiber_g": 3.0
        },
        "image_url": "https://images.openfoodfacts.org/images/products/762/221/081/7014/front_en.114.400.jpg"
    },
    "8901491101837": {
        "barcode": "8901491101837",
        "product_name": "Lay's India's Magic Masala Potato Chips",
        "brand": "Lay's (PepsiCo)",
        "category": "Snacks & Chips",
        "ingredients": "Potato, Edible Vegetable Oil (Palmolein, Rice Bran Oil), Seasoning (Spices and Condiments, Iodised Salt, Maltodextrin, Black Salt, Sugar, Tomato Powder, Acidity Regulators (330, 296), Flavour Enhancers (627, 631), Anticaking Agent (551), Colour (160c)).",
        "nutrition": {
            "energy_kcal": 555,
            "sugar_g": 4.5,
            "sodium_mg": 790,
            "saturated_fat_g": 14.5,
            "trans_fat_g": 0.1,
            "protein_g": 7.0,
            "fiber_g": 4.2
        },
        "image_url": "https://images.openfoodfacts.org/images/products/890/149/110/1837/front_en.11.400.jpg"
    },
    "5449000000996": {
        "barcode": "5449000000996",
        "product_name": "Coca-Cola Original Taste",
        "brand": "The Coca-Cola Company",
        "category": "Carbonated Soft Drinks",
        "ingredients": "Carbonated water, Sugar, Colour (Caramel E150d), Phosphoric acid, Natural flavourings including caffeine.",
        "nutrition": {
            "energy_kcal": 42,
            "sugar_g": 10.6,
            "sodium_mg": 4,
            "saturated_fat_g": 0.0,
            "trans_fat_g": 0.0,
            "protein_g": 0.0,
            "fiber_g": 0.0
        },
        "image_url": "https://images.openfoodfacts.org/images/products/544/900/000/0996/front_en.448.400.jpg"
    },
    "8901262010047": {
        "barcode": "8901262010047",
        "product_name": "Amul Pure Cow Ghee",
        "brand": "Amul",
        "category": "Dairy Products",
        "ingredients": "100% Clarified Milk Fat (Milk Fat from Cow Milk).",
        "nutrition": {
            "energy_kcal": 900,
            "sugar_g": 0.0,
            "sodium_mg": 0,
            "saturated_fat_g": 62.0,
            "trans_fat_g": 3.0,
            "protein_g": 0.0,
            "fiber_g": 0.0
        },
        "image_url": "https://images.openfoodfacts.org/images/products/890/126/201/0047/front_en.9.400.jpg"
    },
    "8901719101038": {
        "barcode": "8901719101038",
        "product_name": "Parle-G Original Gluco Biscuits",
        "brand": "Parle",
        "category": "Biscuits & Bakery",
        "ingredients": "Wheat flour (maida), Sugar, Refined palm oil, Invert sugar syrup, Raising agents (503(ii), 500(ii)), Salt, Milk solids, Artificial vanilla and milk flavouring substances, Emulsifier (diacetyl tartaric and fatty acid esters of glycerol), Dough conditioner (223).",
        "nutrition": {
            "energy_kcal": 454,
            "sugar_g": 26.5,
            "sodium_mg": 280,
            "saturated_fat_g": 6.5,
            "trans_fat_g": 0.0,
            "protein_g": 6.5,
            "fiber_g": 1.5
        },
        "image_url": "https://images.openfoodfacts.org/images/products/890/171/910/1038/front_en.11.400.jpg"
    },
    "8901030018503": {
        "barcode": "8901030018503",
        "product_name": "Kissan Fresh Tomato Ketchup",
        "brand": "Kissan (HUL)",
        "category": "Sauces & Condiments",
        "ingredients": "Water, Tomato paste (28%), Sugar, Salt, Acidity regulator (260), Thickeners (1422, 415), Preservative (211), Spices and condiments, Onion powder, Garlic powder.",
        "nutrition": {
            "energy_kcal": 138,
            "sugar_g": 28.0,
            "sodium_mg": 890,
            "saturated_fat_g": 0.1,
            "trans_fat_g": 0.0,
            "protein_g": 1.2,
            "fiber_g": 1.1
        },
        "image_url": "https://images.openfoodfacts.org/images/products/890/103/001/8503/front_en.11.400.jpg"
    },
    "9990000000001": {
        "barcode": "9990000000001",
        "product_name": "Adulterated Turmeric Sample (Test Case)",
        "brand": "Spurious / Non-Branded",
        "category": "Spices & Condiments",
        "ingredients": "Turmeric powder, Lead chromate color enhancer, Metanil yellow dye, Insoluble chalk powder, Wheat starch filler.",
        "nutrition": {
            "energy_kcal": 280,
            "sugar_g": 2.0,
            "sodium_mg": 150,
            "saturated_fat_g": 1.5,
            "trans_fat_g": 0.0,
            "protein_g": 4.5,
            "fiber_g": 10.0
        },
        "image_url": ""
    },
    "9990000000002": {
        "barcode": "9990000000002",
        "product_name": "Spurious Synthetic Milk Formulation (Test Case)",
        "brand": "Non-Standard Bulk Dairy",
        "category": "Dairy Products",
        "ingredients": "Water, Urea nitrogen spiker, Commercial detergent foaming agent, Low-grade refined vegetable oil, Caustic soda neutralizer.",
        "nutrition": {
            "energy_kcal": 160,
            "sugar_g": 0.5,
            "sodium_mg": 850,
            "saturated_fat_g": 12.0,
            "trans_fat_g": 3.5,
            "protein_g": 1.5,
            "fiber_g": 0.0
        },
        "image_url": ""
    }
}

def fetch_product_by_barcode(barcode: str) -> Optional[Dict[str, Any]]:
    clean_code = str(barcode).strip()
    
    # 1. Check local rich catalog first
    if clean_code in OFFLINE_PRODUCT_CATALOG:
        prod = OFFLINE_PRODUCT_CATALOG[clean_code].copy()
        prod["source"] = "Local Food Catalog / Verified Standards"
        return prod

    # 2. Query Open Food Facts API
    try:
        url = f"https://world.openfoodfacts.org/api/v2/product/{clean_code}.json"
        headers = {"User-Agent": "FoodQualityAdulterationDetector/1.0 (academic-project; contact@foodqualityai.edu)"}
        resp = requests.get(url, headers=headers, timeout=4.0)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == 1 and "product" in data:
                p = data["product"]
                nutriments = p.get("nutriments", {})
                
                # Extract clean nutrition values
                energy = nutriments.get("energy-kcal_100g", nutriments.get("energy-kcal", 0))
                sugar = nutriments.get("sugars_100g", nutriments.get("sugars", 0.0))
                sodium = nutriments.get("sodium_100g", nutriments.get("sodium", 0.0)) * 1000 # convert to mg
                sat_fat = nutriments.get("saturated-fat_100g", nutriments.get("saturated-fat", 0.0))
                trans_fat = nutriments.get("trans-fat_100g", nutriments.get("trans-fat", 0.0))
                protein = nutriments.get("proteins_100g", nutriments.get("proteins", 0.0))
                fiber = nutriments.get("fiber_100g", nutriments.get("fiber", 0.0))

                return {
                    "barcode": clean_code,
                    "product_name": p.get("product_name", f"Product #{clean_code}"),
                    "brand": p.get("brands", "Unknown Brand"),
                    "category": p.get("categories", "Packaged Food").split(",")[0].strip(),
                    "ingredients": p.get("ingredients_text", p.get("ingredients_text_en", "")),
                    "nutrition": {
                        "energy_kcal": round(float(energy or 0), 1),
                        "sugar_g": round(float(sugar or 0), 1),
                        "sodium_mg": round(float(sodium or 0), 1),
                        "saturated_fat_g": round(float(sat_fat or 0), 1),
                        "trans_fat_g": round(float(trans_fat or 0), 2),
                        "protein_g": round(float(protein or 0), 1),
                        "fiber_g": round(float(fiber or 0), 1)
                    },
                    "image_url": p.get("image_front_url", ""),
                    "source": "Open Food Facts Live Global Database"
                }
    except Exception as err:
        print(f"[OpenFoodFacts] Live query error: {err}")

    return None

def get_sample_barcodes() -> list:
    """Returns list of curated barcodes for instant UI demo and quick testing."""
    return [
        {"barcode": code, "name": item["product_name"], "brand": item["brand"], "category": item["category"]}
        for code, item in OFFLINE_PRODUCT_CATALOG.items()
    ]
