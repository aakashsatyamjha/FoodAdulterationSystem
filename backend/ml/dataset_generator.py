"""
Dataset Generator for Food Quality & Adulteration Classification
Generates a realistic, diverse dataset of 3,500+ food products across multiple categories
with nutritional values, additive profiles, adulterant indicators, and quality risk labels.
"""

import random
import csv
import os

CATEGORIES = {
    "Dairy": {
        "products": [
            ("Whole Cow Milk", ["milk", "vitamin d3"], 62, 4.8, 44, 3.2, 0.0, 3.2, 0.0, 0, 0, 0, 0, 0, 92, "Low Risk"),
            ("Skimmed Milk", ["skimmed milk", "vitamin a", "vitamin d3"], 35, 4.9, 50, 0.2, 0.0, 3.4, 0.0, 0, 0, 0, 0, 0, 95, "Low Risk"),
            ("Standard Processed Cheese", ["milk", "salt", "cheese cultures", "enzymes", "sodium phosphate", "annatto"], 320, 1.2, 1150, 21.0, 0.5, 18.0, 0.0, 3, 1, 0, 1, 0, 58, "Moderate Risk"),
            ("Adulterated Low-Cost Paneer", ["milk solids", "vegetable oil", "starch", "sulfuric acid trace", "detergent trace"], 290, 3.5, 480, 18.0, 2.5, 9.0, 0.0, 4, 0, 0, 2, 1, 22, "High Risk"),
            ("Greek Plain Yogurt", ["cultured pasteurized nonfat milk", "live active cultures"], 59, 3.6, 36, 0.4, 0.0, 10.0, 0.0, 0, 0, 0, 0, 0, 96, "Low Risk"),
            ("Flavored Fruit Yogurt", ["milk", "sugar", "strawberries", "modified corn starch", "carmine color", "potassium sorbate"], 110, 16.5, 65, 1.5, 0.0, 4.0, 0.5, 3, 1, 0, 1, 0, 64, "Moderate Risk"),
            ("Synthetic Milk Sample", ["urea", "detergent", "refined vegetable oil", "caustic soda", "water"], 180, 0.5, 820, 14.0, 4.2, 1.2, 0.0, 5, 0, 0, 3, 1, 12, "High Risk"),
            ("Fresh Butter", ["pasteurized cream", "salt"], 717, 0.1, 576, 51.4, 0.0, 0.9, 0.0, 0, 0, 0, 0, 0, 75, "Moderate Risk"),
            ("Adulterated Butter with Animal Fat & Starch", ["milk fat", "animal tallow", "starch", "yellow dye 5", "preservative"], 680, 0.5, 620, 52.0, 3.8, 0.5, 0.0, 4, 1, 0, 2, 1, 24, "High Risk"),
            ("Cottage Cheese (Paneer)", ["pasteurized milk", "citric acid"], 265, 1.2, 22, 17.0, 0.0, 18.3, 0.0, 0, 0, 0, 0, 0, 88, "Low Risk")
        ]
    },
    "Snacks": {
        "products": [
            ("Roasted Chickpeas", ["chickpeas", "olive oil", "sea salt"], 364, 2.1, 280, 1.2, 0.0, 19.0, 17.0, 0, 0, 0, 0, 0, 94, "Low Risk"),
            ("Commercial Potato Crisps", ["potatoes", "palm oil", "salt", "monosodium glutamate", "flavor enhancer 635", "dextrose"], 536, 0.8, 750, 12.0, 0.4, 6.5, 3.2, 4, 0, 0, 1, 0, 48, "Moderate Risk"),
            ("Extruded Spicy Puffs", ["corn meal", "palm olein", "maltodextrin", "sunset yellow fcf", "tartrazine", "tbhq", "msg", "artificial flavors"], 550, 4.2, 1280, 16.5, 1.2, 5.0, 1.5, 7, 2, 0, 2, 1, 28, "High Risk"),
            ("Baked Whole Grain Crackers", ["whole wheat flour", "canola oil", "sea salt", "malt extract"], 420, 2.5, 390, 1.8, 0.0, 9.0, 7.5, 0, 0, 0, 0, 0, 86, "Low Risk"),
            ("Processed Nacho Chips", ["corn", "vegetable fat", "whey powder", "disodium guanylate", "artificial cheese flavor", "yellow 6 lake"], 495, 2.0, 920, 9.5, 0.8, 6.8, 4.0, 5, 1, 0, 1, 0, 52, "Moderate Risk"),
            ("Fried Street-Style Savory Mix", ["refined flour", "re-used palm oil", "metanil yellow", "excess salt", "msg"], 560, 1.5, 1450, 22.0, 3.5, 6.0, 1.0, 6, 2, 0, 2, 1, 18, "High Risk"),
            ("Organic Trail Mix", ["almonds", "walnuts", "raisins", "sunflower seeds", "pumpkin seeds"], 490, 18.0, 15, 4.2, 0.0, 15.0, 8.0, 0, 0, 0, 0, 0, 92, "Low Risk"),
            ("Instant Fried Noodles", ["wheat flour", "palm oil", "salt", "guar gum", "flavor enhancer 621", "caramel iv", "sodium polyphosphate"], 460, 2.8, 1760, 9.8, 0.5, 9.2, 2.5, 5, 1, 0, 2, 0, 42, "Moderate Risk")
        ]
    },
    "Beverages": {
        "products": [
            ("Cold Pressed Orange Juice", ["100% freshly pressed oranges"], 45, 8.8, 2, 0.1, 0.0, 0.7, 1.5, 0, 0, 0, 0, 0, 91, "Low Risk"),
            ("Carbonated Cola Drink", ["carbonated water", "high fructose corn syrup", "caramel color iv", "phosphoric acid", "caffeine", "artificial flavors"], 42, 10.6, 12, 0.0, 0.0, 0.0, 0.0, 4, 1, 0, 1, 0, 38, "Moderate Risk"),
            ("Diet Soda with Multiple Sweeteners", ["carbonated water", "aspartame", "acesulfame potassium", "caramel iv", "sodium benzoate", "phosphoric acid"], 1, 0.0, 35, 0.0, 0.0, 0.0, 0.0, 5, 1, 2, 1, 0, 45, "Moderate Risk"),
            ("Pure Green Tea Bag", ["100% organic green tea leaves"], 1, 0.0, 1, 0.0, 0.0, 0.2, 0.0, 0, 0, 0, 0, 0, 98, "Low Risk"),
            ("Low-Cost Synthetic Fruit Drink", ["water", "invert sugar syrup", "metanil yellow", "citric acid", "clouding agent", "artificial mango flavor", "potassium metabisulphite"], 56, 14.5, 45, 0.0, 0.0, 0.0, 0.0, 6, 2, 0, 2, 1, 25, "High Risk"),
            ("Energy Drink with High Caffeine", ["carbonated water", "sucrose", "glucose", "taurine", "caffeine", "inositol", "niacinamide", "pyridoxine", "color e133", "sodium benzoate"], 48, 12.0, 80, 0.0, 0.0, 0.4, 0.0, 6, 1, 0, 2, 0, 35, "Moderate Risk"),
            ("Coconut Water 100% Pure", ["pure tender coconut water"], 19, 3.2, 25, 0.1, 0.0, 0.7, 1.1, 0, 0, 0, 0, 0, 95, "Low Risk")
        ]
    },
    "Bakery & Confectionery": {
        "products": [
            ("100% Whole Wheat Sourdough", ["whole wheat flour", "water", "sourdough culture", "sea salt"], 240, 1.5, 420, 0.5, 0.0, 10.5, 6.0, 0, 0, 0, 0, 0, 90, "Low Risk"),
            ("Industrial White Sandwich Bread", ["refined wheat flour", "sugar", "yeast", "palm oil", "calcium propionate", "emulsifier 481", "flour treatment agent 300"], 265, 4.8, 510, 1.2, 0.1, 8.0, 2.0, 4, 0, 0, 2, 0, 59, "Moderate Risk"),
            ("Cream-Filled Sandwich Cookies", ["refined wheat flour", "sugar", "hydrogenated palm oil", "cocoa", "high fructose corn syrup", "soy lecithin", "vanillin", "artificial chocolate flavor", "tbhq"], 485, 38.0, 360, 9.5, 1.8, 4.5, 2.0, 5, 0, 0, 2, 1, 30, "High Risk"),
            ("Dark Chocolate 85%", ["cocoa mass", "cocoa butter", "cane sugar", "vanilla beans"], 580, 14.0, 15, 28.0, 0.0, 8.5, 11.0, 0, 0, 0, 0, 0, 84, "Low Risk"),
            ("Synthetic Colored Hard Candies", ["sugar", "liquid glucose", "allura red", "brilliant blue fcf", "tartrazine", "artificial fruit flavor", "citric acid"], 390, 72.0, 80, 0.0, 0.0, 0.0, 0.0, 5, 3, 0, 1, 1, 26, "High Risk"),
            ("Oat & Honey Granola Bar", ["rolled oats", "honey", "almonds", "crisped rice", "sunflower oil", "salt"], 410, 15.0, 180, 2.2, 0.0, 8.5, 5.5, 0, 0, 0, 0, 0, 82, "Low Risk")
        ]
    },
    "Spices & Condiments": {
        "products": [
            ("Pure Ground Turmeric Powder", ["100% turmeric rhizome powder"], 312, 3.2, 38, 2.8, 0.0, 9.7, 22.0, 0, 0, 0, 0, 0, 97, "Low Risk"),
            ("Adulterated Turmeric with Metanil Yellow", ["turmeric powder", "lead chromate trace", "chalk powder", "metanil yellow color"], 250, 2.0, 180, 1.5, 0.0, 5.0, 12.0, 3, 1, 0, 0, 1, 15, "High Risk"),
            ("Pure Red Chilli Powder", ["100% dried red chillies"], 318, 7.2, 30, 3.5, 0.0, 12.0, 27.0, 0, 0, 0, 0, 0, 94, "Low Risk"),
            ("Adulterated Chilli Powder with Sudan Dye", ["red chilli powder", "brick powder trace", "sudan i dye", "salt", "mineral oil"], 280, 4.0, 650, 4.0, 0.0, 6.0, 14.0, 4, 1, 0, 0, 1, 12, "High Risk"),
            ("Commercial Tomato Ketchup", ["tomato paste", "sugar", "distilled vinegar", "salt", "onion powder", "sodium benzoate", "potassium sorbate", "pectin"], 115, 24.5, 950, 0.1, 0.0, 1.4, 1.5, 3, 0, 0, 2, 0, 54, "Moderate Risk"),
            ("Pure Extra Virgin Olive Oil", ["100% extra virgin cold pressed olive oil"], 884, 0.0, 2, 14.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 89, "Low Risk"),
            ("Adulterated Mustard Oil with Argemone", ["mustard oil", "argemone oil", "mineral oil", "butter yellow dye"], 884, 0.0, 5, 12.0, 1.5, 0.0, 0.0, 3, 1, 0, 0, 1, 10, "High Risk")
        ]
    }
}

def generate_sample_variations(base_sample, category, index):
    name, ing_list, energy, sugar, sodium, sat_fat, trans_fat, protein, fiber, \
    n_additives, n_colors, n_sweeteners, n_preservatives, is_adulterated, score, base_risk = base_sample
    
    # Introduce realistic variations
    jitter_factor = random.uniform(0.85, 1.15)
    var_energy = max(0, round(energy * jitter_factor, 1))
    var_sugar = max(0.0, round(sugar * random.uniform(0.85, 1.2), 1))
    var_sodium = max(0, round(sodium * random.uniform(0.85, 1.2), 1))
    var_sat_fat = max(0.0, round(sat_fat * random.uniform(0.85, 1.2), 1))
    var_trans_fat = max(0.0, round(trans_fat + (0.0 if trans_fat == 0 else random.uniform(-0.1, 0.3)), 2))
    var_protein = max(0.0, round(protein * random.uniform(0.9, 1.1), 1))
    var_fiber = max(0.0, round(fiber * random.uniform(0.9, 1.1), 1))
    
    # Calculate score based on nutritional parameters and additives
    calculated_score = 100.0
    if var_sugar > 25:
        calculated_score -= min(30, (var_sugar - 25) * 1.2 + 10)
    elif var_sugar > 10:
        calculated_score -= (var_sugar - 10) * 0.8
        
    if var_sodium > 800:
        calculated_score -= min(25, (var_sodium - 800) * 0.02 + 10)
    elif var_sodium > 400:
        calculated_score -= (var_sodium - 400) * 0.015
        
    if var_sat_fat > 10:
        calculated_score -= min(20, (var_sat_fat - 10) * 1.0 + 5)
        
    if var_trans_fat > 0.5:
        calculated_score -= min(35, var_trans_fat * 15)
        
    calculated_score -= (n_additives * 3.5)
    calculated_score -= (n_colors * 5.0)
    calculated_score -= (n_sweeteners * 4.0)
    calculated_score -= (n_preservatives * 3.0)
    
    if is_adulterated:
        calculated_score -= 40
        
    calculated_score += min(10, var_fiber * 0.8)
    calculated_score += min(8, var_protein * 0.4)
    
    calculated_score = max(5, min(99, round(calculated_score)))
    
    if is_adulterated or calculated_score < 40 or var_trans_fat > 1.5:
        risk_level = "High Risk"
    elif calculated_score < 70 or var_sugar > 18 or var_sodium > 600 or n_additives >= 3:
        risk_level = "Moderate Risk"
    else:
        risk_level = "Low Risk"
        
    barcode = f"890{random.randint(100000000, 999999999)}"
    sample_name = f"{name} #{index}" if index > 0 else name
    ingredients_str = ", ".join(ing_list)
    
    return {
        "barcode": barcode,
        "product_name": sample_name,
        "category": category,
        "ingredients": ingredients_str,
        "energy_kcal": var_energy,
        "sugar_g": var_sugar,
        "sodium_mg": var_sodium,
        "saturated_fat_g": var_sat_fat,
        "trans_fat_g": var_trans_fat,
        "protein_g": var_protein,
        "fiber_g": var_fiber,
        "additives_count": n_additives,
        "artificial_colors_count": n_colors,
        "artificial_sweeteners_count": n_sweeteners,
        "preservatives_count": n_preservatives,
        "is_suspected_adulterant": is_adulterated,
        "quality_score": calculated_score,
        "risk_level": risk_level
    }

def generate_dataset(output_path, target_count=3500):
    rows = []
    all_templates = []
    for cat, data in CATEGORIES.items():
        for product in data["products"]:
            all_templates.append((cat, product))
            
    for i in range(target_count):
        cat, prod = random.choice(all_templates)
        row = generate_sample_variations(prod, cat, i)
        rows.append(row)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"[Dataset Generator] Successfully generated {len(rows)} samples into {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "data", "food_products_dataset.csv")
    generate_dataset(out, target_count=3500)
