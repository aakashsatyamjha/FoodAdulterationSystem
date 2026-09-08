"""
Centralized Ingredient Intelligence & Knowledge Base Service
Contains comprehensive regulatory status, functions, risks, cross-country differences,
and consumer concerns across India (FSSAI), USA (FDA), EU (EFSA), Germany (BVL), and UK (FSA).
"""

import re
from typing import List, Dict, Any, Optional

# Supported Countries and their governing regulatory authorities
SUPPORTED_COUNTRIES = [
    {
        "code": "IN",
        "name": "India",
        "authority": "FSSAI",
        "full_authority": "Food Safety and Standards Authority of India",
        "framework": "Food Safety and Standards Act (2006) & Regulations (2011/2024)",
        "flag": "🇮🇳"
    },
    {
        "code": "US",
        "name": "USA",
        "authority": "FDA",
        "full_authority": "U.S. Food and Drug Administration",
        "framework": "Federal Food, Drug, and Cosmetic Act (FD&C Act) / 21 CFR",
        "flag": "🇺🇸"
    },
    {
        "code": "EU",
        "name": "European Union",
        "authority": "EFSA",
        "full_authority": "European Food Safety Authority",
        "framework": "Regulation (EC) No 1333/2008 on Food Additives",
        "flag": "🇪🇺"
    },
    {
        "code": "DE",
        "name": "Germany",
        "authority": "BVL / BMEL",
        "full_authority": "Federal Office of Consumer Protection and Food Safety",
        "framework": "EU Regulation 1333/2008 with German National Additives Decrees",
        "flag": "🇩🇪"
    },
    {
        "code": "UK",
        "name": "United Kingdom",
        "authority": "FSA",
        "full_authority": "UK Food Standards Agency",
        "framework": "Retained EU Law Regulation 1333/2008 & UK Food Law",
        "flag": "🇬🇧"
    }
]

# Comprehensive Centralized Ingredient Database
INGREDIENT_DATABASE: List[Dict[str, Any]] = [
    # ── Synthetic Colors & Dyes ──
    {
        "id": "tartrazine",
        "common_name": "Tartrazine",
        "scientific_name": "Trisodium 5-hydroxy-1-(4-sulfonatophenyl)-4-(4-sulfonatophenylazo)pyrazole-3-carboxylate",
        "ins_e_number": "INS 102 / E102 / FD&C Yellow 5",
        "category": "Food Colouring",
        "function": "Synthetic Azo Lemon-Yellow Dye",
        "aliases": ["tartrazine", "ins 102", "e102", "yellow 5", "fd&c yellow no. 5", "ci 19140"],
        "food_categories": ["Confectionery", "Beverages", "Snacks", "Sauces", "Instant Noodles"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "100 mg/kg in permitted foods",
            "condition": "FSSAI Regulation 2.12: Mandatory declaration on label 'Contains Permitted Synthetic Food Colour'",
            "source": "FSSAI Food Safety and Standards (Food Products Standards and Food Additives) Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Good Manufacturing Practice (GMP)",
            "condition": "Must be listed specifically by name (FD&C Yellow No. 5) due to allergic sensitivities",
            "source": "US FDA 21 CFR §74.705"
        },
        "eu_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "50 mg/kg to 500 mg/kg depending on food category",
            "condition": "Mandatory warning label required: 'May have an adverse effect on activity and attention in children'",
            "source": "Regulation (EC) No 1333/2008, Annex V (Southampton Six)"
        },
        "germany_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "EU baseline limits apply",
            "condition": "Mandatory German warning label required: 'Kann Aktivität und Aufmerksamkeit bei Kindern beeinträchtigen'",
            "source": "BVL / Regulation (EC) No 1333/2008"
        },
        "uk_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "UK statutory limits apply",
            "condition": "Mandatory child hyperactivity warning label required",
            "source": "UK Food Standards Agency (FSA)"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Azo dye allergy / hives", "Asthma trigger in aspirin-sensitive individuals", "Childhood hyperactivity"],
        "evidence_source": "EFSA Scientific Opinion on Tartrazine (2009); Southampton Study (2007)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "While permitted in India and the US with label disclosure, the EU, Germany, and UK mandate an explicit health warning regarding childhood hyperactivity under Annex V of Regulation 1333/2008."
    },
    {
        "id": "sunset_yellow",
        "common_name": "Sunset Yellow FCF",
        "scientific_name": "Disodium 6-hydroxy-5-[(4-sulfophenyl)azo]-2-naphthalenesulfonate",
        "ins_e_number": "INS 110 / E110 / FD&C Yellow 6",
        "category": "Food Colouring",
        "function": "Synthetic Orange-Red Azo Dye",
        "aliases": ["sunset yellow", "sunset yellow fcf", "ins 110", "e110", "yellow 6", "fd&c yellow no. 6", "ci 15985"],
        "food_categories": ["Beverages", "Sweets", "Snacks", "Jams"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "100 mg/kg max",
            "condition": "Must be declared on label",
            "source": "FSSAI Food Additives Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP",
            "condition": "Certified color additive batch certification required",
            "source": "US FDA 21 CFR §74.706"
        },
        "eu_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Lowered ADI (0-4 mg/kg bw/day)",
            "condition": "Mandatory warning label required: 'May have an adverse effect on activity and attention in children'",
            "source": "EFSA Scientific Opinion 2014; Regulation (EC) 1333/2008"
        },
        "germany_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "EU Annex II & V limits apply",
            "condition": "Mandatory warning label in German language",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "UK FSA Annex V",
            "condition": "Mandatory warning label required",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Azo dye allergy", "Hyperactivity in children", "Petroleum-derived additive"],
        "evidence_source": "EFSA Journal 2014;12(7):3765",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "EU and Germany reduced the Acceptable Daily Intake (ADI) and require child hyperactivity warnings, whereas India and the USA permit standard use with general label disclosure."
    },
    {
        "id": "allura_red",
        "common_name": "Allura Red AC",
        "scientific_name": "Disodium 6-hydroxy-5-[(2-methoxy-5-methyl-4-sulfophenyl)azo]-2-naphthalenesulfonate",
        "ins_e_number": "INS 129 / E129 / FD&C Red 40",
        "category": "Food Colouring",
        "function": "Synthetic Red Azo Dye",
        "aliases": ["allura red", "allura red ac", "red 40", "fd&c red no. 40", "ins 129", "e129", "ci 16035"],
        "food_categories": ["Candy", "Beverages", "Bakery", "Cereals"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "100 mg/kg max in designated foods",
            "condition": "Declaration mandatory",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Widely permitted under GMP",
            "condition": "Labeling as FD&C Red No. 40 mandatory",
            "source": "US FDA 21 CFR §74.340"
        },
        "eu_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Strict limits per category",
            "condition": "Mandatory warning label on childhood attention and activity",
            "source": "Regulation (EC) No 1333/2008 Annex V"
        },
        "germany_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "EU baseline applies",
            "condition": "Mandatory warning label in German",
            "source": "BVL Regulation"
        },
        "uk_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "UK statutory limits",
            "condition": "Mandatory warning label",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Gut microbiome alterations", "Hypersensitivity / hives", "Southampton Six dye warning"],
        "evidence_source": "Nature Communications gut inflammation study (2022); EFSA (2012)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "One of the most common red dyes in the US and India, but subject to mandatory behavioral warning labels in the EU, Germany, and the UK."
    },
    {
        "id": "erythrosine",
        "common_name": "Erythrosine / Red No. 3",
        "scientific_name": "Disodium 2-(2,4,5,7-tetraiodo-6-oxido-3-oxoxanthen-9-yl)benzoate",
        "ins_e_number": "INS 127 / E127 / FD&C Red No. 3",
        "category": "Food Colouring",
        "function": "Synthetic Cherry-Pink Organoiodine Dye",
        "aliases": ["erythrosine", "red 3", "fd&c red no. 3", "ins 127", "e127", "ci 45430"],
        "food_categories": ["Cocktail Cherries", "Canned Fruits", "Decorations"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "100 mg/kg in permitted foods",
            "condition": "Restricted list of food products",
            "source": "FSSAI Regulations 2.12"
        },
        "usa_status": {
            "status": "Category-specific restriction",
            "code": "RESTRICTED",
            "max_limit": "Banned in cosmetics/external drugs (1990); currently under active FDA phase-out review for foods",
            "condition": "Allowed only in specified food items (e.g. maraschino cherries)",
            "source": "US FDA 21 CFR §74.303; California AB 418 Food Safety Act"
        },
        "eu_status": {
            "status": "Category-specific restriction",
            "code": "RESTRICTED",
            "max_limit": "200 mg/kg ONLY in cocktail/candied cherries and Bigarreaux cherries",
            "condition": "Strictly prohibited in all other food and beverage categories",
            "source": "EFSA Scientific Opinion on Erythrosine; Reg (EC) 1333/2008 Annex II"
        },
        "germany_status": {
            "status": "Category-specific restriction",
            "code": "RESTRICTED",
            "max_limit": "Only permitted for candied/cocktail cherries",
            "condition": "Prohibited in general confectionery, baked goods, and beverages",
            "source": "BVL / German Food Additives Regulation"
        },
        "uk_status": {
            "status": "Category-specific restriction",
            "code": "RESTRICTED",
            "max_limit": "Only cocktail cherries",
            "condition": "Prohibited in general foods",
            "source": "UK FSA"
        },
        "risk_classification": "High",
        "consumer_concerns": ["Thyroid hormone disruption", "Thyroid tumor evidence in animal models", "Endocrine interference"],
        "evidence_source": "EFSA Journal 2011;9(1):1854; California Food Safety Act (2023)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "In the EU and Germany, Erythrosine is legally banned in all foods except cocktail/glacé cherries due to thyroid tumorigenesis risks. In India and the US, it remains permitted in a wider range of foods, though US states (e.g. California) have enacted bans."
    },
    {
        "id": "titanium_dioxide",
        "common_name": "Titanium Dioxide",
        "scientific_name": "Titanium(IV) oxide",
        "ins_e_number": "INS 171 / E171",
        "category": "Food Colouring / Opacifier",
        "function": "Mineral Whitening Agent & Opacifier",
        "aliases": ["titanium dioxide", "ins 171", "e171", "ci 77891", "titania"],
        "food_categories": ["Confectionery", "Chewing Gum", "White Sauces", "Frosting"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Up to 1.0% by weight in chewing gum and icing",
            "condition": "Must meet FSSAI purity specifications",
            "source": "FSSAI Food Product Standards & Additives Regs"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "May not exceed 1.0% by weight of the food",
            "condition": "Under FDA safety review following European reassessments",
            "source": "US FDA 21 CFR §73.575"
        },
        "eu_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Banned in food)",
            "condition": "Banned across the European Union since August 7, 2022 (Regulation EU 2022/63)",
            "source": "Commission Regulation (EU) 2022/63; EFSA ANS Panel (2021)"
        },
        "germany_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Banned in food)",
            "condition": "Strictly enforced ban following EU Regulation 2022/63",
            "source": "BVL Germany / EU 2022/63"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Under ongoing FSA review; not yet banned in UK",
            "condition": "UK FSA concluded evidence insufficient for outright ban as of 2023",
            "source": "UK Food Standards Agency statement on Titanium Dioxide"
        },
        "risk_classification": "High",
        "consumer_concerns": ["Nanoparticle accumulation in organs", "Genotoxicity & DNA damage concerns", "Inflammatory bowel aggravation"],
        "evidence_source": "EFSA Scientific Opinion on the safety evaluation of Titanium Dioxide (E171) as a food additive (2021)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "EFSA concluded in 2021 that E171 can no longer be considered safe due to genotoxicity concerns of nanoparticles, leading to an outright EU and German ban in 2022. The US FDA and UK FSA still permit it up to 1% by weight."
    },
    {
        "id": "ponceau_4r",
        "common_name": "Ponceau 4R",
        "scientific_name": "Trisodium 2-hydroxy-1-(4-sulfonato-1-naphthylazo)naphthalene-6,8-disulfonate",
        "ins_e_number": "INS 124 / E124 / Cochineal Red A",
        "category": "Food Colouring",
        "function": "Synthetic Strawberry-Red Azo Dye",
        "aliases": ["ponceau 4r", "ins 124", "e124", "cochineal red a", "ci 16255"],
        "food_categories": ["Sweets", "Beverages", "Desserts", "Syrups"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "100 mg/kg max",
            "condition": "Permitted in specified packaged food categories",
            "source": "FSSAI Regulations 2.12"
        },
        "usa_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "Banned in food",
            "condition": "Not listed on US FDA approved color additives list",
            "source": "US FDA Color Additive Status List"
        },
        "eu_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Strict max levels; ADI reduced to 0.7 mg/kg bw",
            "condition": "Mandatory warning label on childhood attention and activity",
            "source": "Regulation (EC) No 1333/2008 Annex V"
        },
        "germany_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "EU baseline applies",
            "condition": "Mandatory German warning label",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "UK statutory limits",
            "condition": "Mandatory warning label",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Azo dye hypersensitivity", "Asthma flare-ups", "Childhood hyperactivity"],
        "evidence_source": "EFSA ANS Panel Opinion (2009); US FDA Color Regulations",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Ponceau 4R is not approved for food use in the USA by the FDA, whereas it is permitted in India with general limits and in the EU/Germany under strict usage limits and mandatory warning labels."
    },
    {
        "id": "azorubine",
        "common_name": "Azorubine / Carmoisine",
        "scientific_name": "Disodium 4-hydroxy-3-[(4-sulfonato-1-naphthyl)azo]naphthalene-1-sulfonate",
        "ins_e_number": "INS 122 / E122",
        "category": "Food Colouring",
        "function": "Synthetic Red-to-Maroon Azo Dye",
        "aliases": ["azorubine", "carmoisine", "ins 122", "e122", "ci 14720"],
        "food_categories": ["Jellies", "Beverages", "Confectionery", "Sauces"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "100 mg/kg max",
            "condition": "Permitted synthetic color",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "Banned in food",
            "condition": "Not an authorized food color in the United States",
            "source": "US FDA Color Additive Status List"
        },
        "eu_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Strict limits; ADI 4 mg/kg bw",
            "condition": "Mandatory warning label required on childhood hyperactivity",
            "source": "Regulation (EC) No 1333/2008 Annex V"
        },
        "germany_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "EU baseline applies",
            "condition": "Mandatory German warning label",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "UK statutory limits",
            "condition": "Mandatory warning label",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Allergic skin reactions", "Intolerance in aspirin-sensitive persons", "Childhood hyperactivity"],
        "evidence_source": "EFSA Scientific Opinion 2009",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Not permitted by the US FDA in food products. Permitted in India and the EU/Germany with mandatory European child behavior warning labels."
    },
    {
        "id": "brilliant_blue",
        "common_name": "Brilliant Blue FCF",
        "scientific_name": "Disodium 2-({4-[N-ethyl(4-sulfonatobenzyl)amino]phenyl}{4-[N-ethyl(4-sulfonatobenzyl)iminio]cyclohexa-2,5-dien-1-ylidene}methyl)benzenesulfonate",
        "ins_e_number": "INS 133 / E133 / FD&C Blue 1",
        "category": "Food Colouring",
        "function": "Synthetic Blue Triarylmethane Dye",
        "aliases": ["brilliant blue", "brilliant blue fcf", "blue 1", "fd&c blue no. 1", "ins 133", "e133", "ci 42090"],
        "food_categories": ["Beverages", "Ice Cream", "Candy", "Frosting"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "100 mg/kg max",
            "condition": "Declaration mandatory",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP",
            "condition": "Certified color additive batch testing required",
            "source": "US FDA 21 CFR §74.101"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Category specific limits (e.g. 50-200 mg/kg)",
            "condition": "Not part of Southampton Six; no behavioral warning required",
            "source": "EFSA Scientific Opinion 2010"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU baseline applies",
            "condition": "Complies with EU Regulation 1333/2008",
            "source": "BVL"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits",
            "condition": "Permitted food color",
            "source": "UK FSA"
        },
        "risk_classification": "Low-to-Moderate",
        "consumer_concerns": ["Synthetic dye sensitivity", "Rare allergic reactions"],
        "evidence_source": "EFSA Journal 2010;8(11):1853",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Broadly approved in India, USA, EU, Germany, and the UK with quantitative limits. It was not implicated in the Southampton study, so no behavioral warning is mandated in Europe."
    },
    {
        "id": "fast_green_fcf",
        "common_name": "Fast Green FCF / Green 3",
        "scientific_name": "Disodium 3-[[4-[[4-(dimethylamino)phenyl]-[4-[ethyl-[(3-sulfonatophenyl)methyl]azaniumylidene]cyclohexa-2,5-dien-1-ylidene]methyl]phenyl]-ethylamino]methylbenzenesulfonate",
        "ins_e_number": "INS 143 / E143 / FD&C Green No. 3",
        "category": "Food Colouring",
        "function": "Synthetic Sea-Green Triarylmethane Dye",
        "aliases": ["fast green", "fast green fcf", "green 3", "fd&c green no. 3", "ins 143", "e143"],
        "food_categories": ["Desserts", "Beverages", "Confectionery"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "100 mg/kg max",
            "condition": "Permitted in specified foods",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP",
            "condition": "Certified color additive batch testing required",
            "source": "US FDA 21 CFR §74.203"
        },
        "eu_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "Banned in food",
            "condition": "Not included on the EU positive list of authorized food additives",
            "source": "Regulation (EC) No 1333/2008 Annex II"
        },
        "germany_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "Banned in food",
            "condition": "Prohibited in food formulations",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "Banned in food",
            "condition": "Not on UK authorized list",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Synthetic dye", "Poor gastrointestinal absorption"],
        "evidence_source": "Joint FAO/WHO Expert Committee on Food Additives (JECFA)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Approved for use in India and the US, but not authorized on the EU/Germany/UK approved food additives list due to historical lack of submission/interest by manufacturers."
    },
    {
        "id": "quinoline_yellow",
        "common_name": "Quinoline Yellow",
        "scientific_name": "Disodium 2-(1,3-dioxoinden-2-yl)quinolinedisulfonate",
        "ins_e_number": "INS 104 / E104",
        "category": "Food Colouring",
        "function": "Synthetic Greenish-Yellow Dye",
        "aliases": ["quinoline yellow", "ins 104", "e104", "ci 47005"],
        "food_categories": ["Sweets", "Beverages", "Ices"],
        "india_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "Not on FSSAI permitted synthetic colours list",
            "condition": "FSSAI permits only 8 synthetic dyes (102, 110, 122, 124, 127, 129, 132, 133)",
            "source": "FSSAI Food Product Standards Regulations 2.12"
        },
        "usa_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "Banned in food",
            "condition": "Not an FDA-approved color additive for ingestible food",
            "source": "US FDA Color Additive Status List"
        },
        "eu_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Strict low limits (0.5 mg/kg bw ADI)",
            "condition": "Mandatory warning label required regarding childhood hyperactivity",
            "source": "Regulation (EC) No 1333/2008 Annex V"
        },
        "germany_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "EU baseline applies",
            "condition": "Mandatory warning label in German",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "UK statutory limits",
            "condition": "Mandatory warning label",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Allergic dermatitis", "Hyperactivity in children"],
        "evidence_source": "EFSA Scientific Opinion 2009",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Not permitted in food in the USA or India, but permitted in the EU and Germany subject to strict ADI limits and mandatory child behavioral warning labels."
    },

    # ── Preservatives & Antioxidants ──
    {
        "id": "tbhq",
        "common_name": "TBHQ",
        "scientific_name": "Tertiary butylhydroquinone",
        "ins_e_number": "INS 319 / E319",
        "category": "Preservative / Antioxidant",
        "function": "Synthetic Lipid Antioxidant",
        "aliases": ["tbhq", "tertiary butylhydroquinone", "ins 319", "e319"],
        "food_categories": ["Vegetable Oils", "Fried Snacks", "Instant Noodles", "Crackers"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "200 mg/kg of fat content max",
            "condition": "FSSAI Regulation 2.12: Strict limit calculated based on fat fraction",
            "source": "FSSAI Food Additives Regulations"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Up to 0.02% (200 ppm) of fat/oil content",
            "condition": "Must not exceed 0.02% alone or in combination with BHA/BHT",
            "source": "US FDA 21 CFR §172.185"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "200 mg/kg of fat in fats and frying oils; prohibited in infant foods",
            "condition": "EFSA lowered ADI to 0-0.7 mg/kg bw in 2004",
            "source": "Regulation (EC) No 1333/2008 Annex II"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU baseline limits apply",
            "condition": "Strict adherence to fat-fraction thresholds",
            "source": "BVL / German Food Additives Decree"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "200 mg/kg of fat",
            "condition": "Permitted antioxidant",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Cellular oxidative stress at elevated doses", "Vision changes reported at toxic doses in animal studies", "Synthetic preservative concern"],
        "evidence_source": "EFSA Scientific Opinion on TBHQ (2004); US FDA Toxicology Panels",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Globally permitted in vegetable fats and fried snacks up to 200 mg/kg of fat, but European toxicology evaluations set a stricter Acceptable Daily Intake (ADI) compared to US FDA thresholds."
    },
    {
        "id": "bha",
        "common_name": "BHA (Butylated Hydroxyanisole)",
        "scientific_name": "2-tert-butyl-4-hydroxyanisole and 3-tert-butyl-4-hydroxyanisole mixture",
        "ins_e_number": "INS 320 / E320",
        "category": "Preservative / Antioxidant",
        "function": "Synthetic Phenolic Antioxidant",
        "aliases": ["bha", "butylated hydroxyanisole", "ins 320", "e320"],
        "food_categories": ["Oils", "Cereals", "Chewing Gum", "Snack Foods"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "200 mg/kg of fat max",
            "condition": "Subject to total antioxidant cap when used in combination with BHT/TBHQ",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "0.02% (200 ppm) of fat content",
            "condition": "Listed as GRAS; classified as reasonably anticipated to be a human carcinogen by NTP",
            "source": "US FDA 21 CFR §182.3169; US NTP 15th Report on Carcinogens"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Lowered ADI (0-1.0 mg/kg bw/day); restricted usage categories",
            "condition": "Under continuous EFSA endocrine disruptor evaluation",
            "source": "EFSA Journal 2011;9(10):2392"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU Annex II limits",
            "condition": "Subject to strict monitoring in infant and organic food categories",
            "source": "BVL / BMEL"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits",
            "condition": "Permitted antioxidant",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate-to-High",
        "consumer_concerns": ["Endocrine disruption / estrogenic activity", "Classified as suspected carcinogen by California Prop 65 & US NTP"],
        "evidence_source": "US National Toxicology Program (NTP); EFSA Re-evaluation of BHA (2011)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Permitted under quantitative limits across US, India, and EU, but subject to stringent consumer advocacy pushback and California Proposition 65 cancer warning listings in the US."
    },
    {
        "id": "bht",
        "common_name": "BHT (Butylated Hydroxytoluene)",
        "scientific_name": "2,6-di-tert-butyl-4-methylphenol",
        "ins_e_number": "INS 321 / E321",
        "category": "Preservative / Antioxidant",
        "function": "Synthetic Phenolic Antioxidant",
        "aliases": ["bht", "butylated hydroxytoluene", "ins 321", "e321"],
        "food_categories": ["Cereals", "Potato Chips", "Oils", "Chewing Gum"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "200 mg/kg of fat max",
            "condition": "Total antioxidant limits apply",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "0.02% of fat content",
            "condition": "FDA GRAS additive",
            "source": "US FDA 21 CFR §182.3173"
        },
        "eu_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Lowered ADI (0.25 mg/kg bw/day); strictly limited food categories",
            "condition": "Under EFSA scrutiny for potential endocrine effects",
            "source": "EFSA Journal 2012;10(3):2588"
        },
        "germany_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "EU baseline applies",
            "condition": "Restricted application in food products",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "UK statutory limits",
            "condition": "Permitted antioxidant",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Potential endocrine disruption", "Hepatic enzyme induction in high animal doses"],
        "evidence_source": "EFSA Scientific Opinion on BHT (2012)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Allowed across all jurisdictions, though the EU and Germany enforce a much lower ADI (0.25 mg/kg bw) than the US FDA."
    },
    {
        "id": "sodium_benzoate",
        "common_name": "Sodium Benzoate",
        "scientific_name": "Sodium benzenecarboxylate",
        "ins_e_number": "INS 211 / E211",
        "category": "Preservative",
        "function": "Antimicrobial / Antifungal Preservative",
        "aliases": ["sodium benzoate", "ins 211", "e211", "benzoate of soda"],
        "food_categories": ["Carbonated Soft Drinks", "Pickles", "Fruit Juices", "Sauces"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "100 ppm to 1000 ppm depending on category (e.g. 120 ppm in carbonated drinks)",
            "condition": "FSSAI Regulation 2.12 restricts max ppm by category",
            "source": "FSSAI Food Additives Regulations"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Not to exceed 0.1% (1,000 ppm) by weight",
            "condition": "Must monitor benzene formation if formulated with Ascorbic Acid (Vitamin C)",
            "source": "US FDA 21 CFR §184.1733; FDA Benzene in Beverages Guidance"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "150 mg/l in beverages, up to 1000 mg/kg in sauces",
            "condition": "EFSA ADI: 5 mg/kg bw/day (expressed as benzoic acid)",
            "source": "Regulation (EC) No 1333/2008 Annex II"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU Annex II limits",
            "condition": "Must avoid heat/light exposure in formulations containing Vitamin C to prevent benzene trace",
            "source": "BVL / Federal Institute for Risk Assessment (BfR)"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits",
            "condition": "Permitted preservative",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Can react with Ascorbic Acid (Vitamin C) to form carcinogenic benzene", "Hyperactivity in sensitive children when combined with azo dyes"],
        "evidence_source": "US FDA Benzene Survey (2006); EFSA ANS Panel (2016); Southampton Study (2007)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Permitted globally with strict limits (0.1%), but requires careful formulation control in Europe, Germany, and the US to prevent benzene formation when combined with Vitamin C."
    },
    {
        "id": "potassium_sorbate",
        "common_name": "Potassium Sorbate",
        "scientific_name": "Potassium (2E,4E)-hexa-2,4-dienoate",
        "ins_e_number": "INS 202 / E202",
        "category": "Preservative",
        "function": "Antifungal and Antimicrobial Preservative",
        "aliases": ["potassium sorbate", "ins 202", "e202", "sorbate"],
        "food_categories": ["Cheese", "Yogurt", "Baked Goods", "Beverages", "Dried Fruits"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "1000 ppm to 2000 ppm depending on product",
            "condition": "FSSAI permitted preservative class II",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP (generally 0.1% to 0.3%)",
            "condition": "US FDA GRAS status",
            "source": "US FDA 21 CFR §182.3640"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EFSA ADI: 11 mg/kg bw/day",
            "condition": "Category specific limits in Annex II",
            "source": "EFSA Journal 2019;17(3):5625"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU baseline applies",
            "condition": "Standard EU limits",
            "source": "BVL"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits",
            "condition": "Permitted preservative",
            "source": "UK FSA"
        },
        "risk_classification": "Low",
        "consumer_concerns": ["Mild skin / mucous membrane sensitivity in rare individuals"],
        "evidence_source": "EFSA Scientific Opinion (2019)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "One of the most universally accepted and benign preservatives across India, USA, EU, Germany, and the UK, metabolizing naturally into water and carbon dioxide in the human body."
    },
    {
        "id": "sodium_nitrite",
        "common_name": "Sodium Nitrite",
        "scientific_name": "Sodium nitrite",
        "ins_e_number": "INS 250 / E250",
        "category": "Preservative / Color Fixative",
        "function": "Curing Agent / Anti-Botulism Preservative",
        "aliases": ["sodium nitrite", "ins 250", "e250", "curing salt"],
        "food_categories": ["Processed Meats", "Sausages", "Bacon", "Cured Ham"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Max 150 mg/kg in meat products",
            "condition": "Residual nitrite capped strictly at 100 mg/kg",
            "source": "FSSAI Food Product Standards (Meat & Poultry)"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Up to 200 ppm in cured meats; ascorbate/erythorbate mandatory in bacon to block nitrosamines",
            "condition": "FDA & USDA regulated",
            "source": "US FDA 21 CFR §172.175; 9 CFR §424.21"
        },
        "eu_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Strict lowered limits adopted in 2023 (Commission Regulation EU 2023/2108)",
            "condition": "Added limits lowered to 50-100 mg/kg to minimize carcinogenic nitrosamine formation",
            "source": "Regulation (EU) 2023/2108; EFSA Nitrites Opinion (2017)"
        },
        "germany_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Strictest EU tier for Nitrite Curing Salt (Pökelsalz)",
            "condition": "Strict limits to prevent nitrosamines in heated meat dishes",
            "source": "BVL / German Meat Hygiene Regulations"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits (150 mg/kg)",
            "condition": "Permitted meat curing agent",
            "source": "UK FSA"
        },
        "risk_classification": "High",
        "consumer_concerns": ["Forms carcinogenic N-nitrosamines when heated with proteins", "WHO IARC Group 1 carcinogen classification for processed meat"],
        "evidence_source": "IARC Monographs Vol 114; EFSA Scientific Opinion (2017); EU 2023/2108",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "While required globally to prevent deadly Clostridium botulinum growth in cured meats, the EU and Germany drastically tightened allowable added levels in 2023 to minimize carcinogenic nitrosamine formation, whereas US and Indian thresholds remain higher."
    },
    {
        "id": "sodium_metabisulphite",
        "common_name": "Sodium Metabisulphite",
        "scientific_name": "Disodium disulfite",
        "ins_e_number": "INS 223 / E223",
        "category": "Preservative / Antioxidant / Bleaching Agent",
        "function": "Sulfite Preservative & Anti-browning Agent",
        "aliases": ["sodium metabisulphite", "sodium metabisulfite", "ins 223", "e223", "disodium disulfite"],
        "food_categories": ["Biscuits", "Dried Fruits", "Wines", "Fruit Juices", "Potato Flakes"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Calculated as SO2 (e.g. 50 ppm in biscuits, 1000 ppm in dried fruit)",
            "condition": "FSSAI Regulation 2.12: Mandatory declaration if SO2 > 10 mg/kg",
            "source": "FSSAI Food Additives Regulations"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "GMP; strictly prohibited on raw fruits/vegetables intended to be served fresh (salad bars)",
            "condition": "Mandatory label warning if sulfites >= 10 ppm",
            "source": "US FDA 21 CFR §182.3766; 21 CFR §101.100"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Category specific limits as SO2; ADI 0.7 mg/kg bw",
            "condition": "Mandatory allergen declaration if > 10 mg/kg",
            "source": "Regulation (EC) No 1333/2008 Annex II"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU baseline applies",
            "condition": "Allergen marking mandatory in German ('Enthält Sulfite')",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits",
            "condition": "Allergen declaration required if > 10 ppm",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Severe bronchospasm in asthmatic consumers", "Major regulated food allergen (Sulfites > 10 ppm)"],
        "evidence_source": "EFSA Scientific Opinion on the re-evaluation of sulfur dioxide (2016)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Universally regulated as a major allergen: mandatory warning label if concentration exceeds 10 mg/kg (10 ppm) due to life-threatening bronchospasms in sulfite-sensitive asthmatics."
    },

    # ── Banned Adulterants & Prohibited Substances ──
    {
        "id": "potassium_bromate",
        "common_name": "Potassium Bromate",
        "scientific_name": "Potassium bromate",
        "ins_e_number": "INS 924 / E924",
        "category": "Dough Conditioner / Flour Improver",
        "function": "Oxidizing Flour Treatment Agent",
        "aliases": ["potassium bromate", "ins 924", "e924", "bromated flour"],
        "food_categories": ["Bread", "Buns", "Bakery Mixes"],
        "india_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (BANNED in India since June 20, 2016)",
            "condition": "Strictly prohibited by FSSAI Gazette Notification No. 1-104/FSSAI/SP (Fortified/Wheat)",
            "source": "FSSAI Order 2016 Banning Potassium Bromate"
        },
        "usa_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Up to 50 ppm in bromated flour",
            "condition": "FDA urged voluntary discontinuation in 1991; banned in California under the California Food Safety Act (effective 2027)",
            "source": "US FDA 21 CFR §137.155; California Health and Safety Code §114094.5"
        },
        "eu_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (BANNED across EU since 1990)",
            "condition": "Classified as genotoxic carcinogen; strictly illegal in all food",
            "source": "Regulation (EC) No 1333/2008; IARC Group 2B classification"
        },
        "germany_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (BANNED)",
            "condition": "Strictly illegal in German baking",
            "source": "BVL / German Food Safety Code"
        },
        "uk_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (BANNED in UK since 1990)",
            "condition": "Prohibited under UK Bread and Flour Regulations",
            "source": "UK Bread and Flour Regulations"
        },
        "risk_classification": "Critical",
        "consumer_concerns": ["Genotoxic carcinogen (kidney and thyroid tumors in animals)", "Kidney toxicity"],
        "evidence_source": "IARC Monographs Vol 73 (1999); FSSAI Ban Order (2016)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Potassium Bromate is banned in India (since 2016), the EU (since 1990), Germany, and the UK as a recognized carcinogen. However, it is still technically allowed at the US federal level in bromated flours (up to 50 ppm), though state-level bans (California) take effect by 2027."
    },
    {
        "id": "brominated_vegetable_oil",
        "common_name": "Brominated Vegetable Oil (BVO)",
        "scientific_name": "Brominated vegetable oil",
        "ins_e_number": "INS 443 / BVO",
        "category": "Emulsifier / Weighting Agent",
        "function": "Citrus Flavoring Emulsifier in Soda",
        "aliases": ["brominated vegetable oil", "bvo", "ins 443"],
        "food_categories": ["Citrus Sodas", "Sports Drinks"],
        "india_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Banned in India)",
            "condition": "FSSAI does not permit BVO in beverages",
            "source": "FSSAI Regulations 2.3.30"
        },
        "usa_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (FDA revoked food authorization July 2024)",
            "condition": "FDA Final Rule revoked regulation authorizing BVO in food effective August 2, 2024",
            "source": "US FDA Final Rule 89 FR 55048 (July 3, 2024)"
        },
        "eu_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Banned across EU since 2008)",
            "condition": "Not included on the EU positive list of food additives",
            "source": "Regulation (EC) No 1333/2008"
        },
        "germany_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (BANNED)",
            "condition": "Strictly illegal",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (BANNED)",
            "condition": "Prohibited in UK",
            "source": "UK FSA"
        },
        "risk_classification": "Critical",
        "consumer_concerns": ["Bioaccumulation of bromine in fat tissue", "Thyroid and heart toxicity in animal studies"],
        "evidence_source": "US FDA Toxicological Re-evaluation (2024); EFSA",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "BVO is now prohibited across all major jurisdictions, after the US FDA revoked its authorization in July 2024, harmonizing with longstanding bans in India, the EU, Germany, and the UK."
    },
    {
        "id": "azodicarbonamide",
        "common_name": "Azodicarbonamide (ADA)",
        "scientific_name": "1,1'-Azobisformamide",
        "ins_e_number": "INS 927a / E927a / ADA",
        "category": "Dough Conditioner / Bleaching Agent",
        "function": "Flour Maturing & Dough Strengthening Agent",
        "aliases": ["azodicarbonamide", "ada", "ins 927a", "e927a", "azobisformamide"],
        "food_categories": ["Commercial Bread", "Burger Buns", "Tortillas"],
        "india_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Prohibited in bread/bakery flour)",
            "condition": "FSSAI banned ADA alongside Potassium Bromate for flour treatment",
            "source": "FSSAI Standards for Bakery"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Up to 45 ppm (0.0045%) in flour",
            "condition": "FDA approved as dough conditioner; banned in California from 2027",
            "source": "US FDA 21 CFR §172.806"
        },
        "eu_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (BANNED across EU)",
            "condition": "Banned as food additive and banned in food contact materials (Directive 2004/1/EC)",
            "source": "Regulation (EC) No 1333/2008; Directive 2004/1/EC"
        },
        "germany_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (BANNED)",
            "condition": "Prohibited in baking formulations",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (BANNED in UK)",
            "condition": "Prohibited in UK flour",
            "source": "UK FSA"
        },
        "risk_classification": "High",
        "consumer_concerns": ["Breaks down into semicarbazide (suspected carcinogen) upon baking", "Respiratory sensitization and asthma in industrial bakery workers"],
        "evidence_source": "EFSA Scientific Panel on food additives (2005); WHO CICAD 16",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Banned in India, the EU, Germany, and the UK due to semicarbazide breakdown products, but still permitted in the US at up to 45 ppm."
    },
    {
        "id": "metanil_yellow",
        "common_name": "Metanil Yellow",
        "scientific_name": "Sodium 3-[(4-anilinophenyl)azo]benzenesulfonate",
        "ins_e_number": "Acid Yellow 36 / CI 13065",
        "category": "Non-Permitted Industrial Dye / Adulterant",
        "function": "Industrial Leather/Textile Dye (Illegal in Food)",
        "aliases": ["metanil yellow", "acid yellow 36", "ci 13065"],
        "food_categories": ["Spices (Turmeric)", "Pulses (Arhar Dal)", "Sweets (Laddoo)", "Biryani"],
        "india_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Strictly Criminalized Food Adulterant)",
            "condition": "Strictly illegal under FSS Act Section 59; punishable with imprisonment",
            "source": "FSSAI Adulteration Screening Standards"
        },
        "usa_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Illegal in Food)",
            "condition": "Not an approved color additive; adulterant under FD&C Act",
            "source": "US FDA FD&C Act §402(a)"
        },
        "eu_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Banned worldwide in food)",
            "condition": "Illegal non-food industrial chemical",
            "source": "Regulation (EC) No 1333/2008"
        },
        "germany_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Illegal)",
            "condition": "Strict border control import rejection under RASFF",
            "source": "BVL / RASFF"
        },
        "uk_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Illegal)",
            "condition": "Prohibited toxic chemical",
            "source": "UK FSA"
        },
        "risk_classification": "Critical",
        "consumer_concerns": ["Severe hepatotoxicity and testicular degeneration", "Neurotoxic and carcinogenic industrial azo dye"],
        "evidence_source": "Toxicology literature; FSSAI Guidance on Food Adulteration",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Non-permitted toxic dye worldwide. Frequently found as an illegal adulterant in unbranded turmeric and pulses to mask low quality."
    },
    {
        "id": "sudan_dyes",
        "common_name": "Sudan Dyes (I - IV)",
        "scientific_name": "Sudan I: 1-(phenylazo)-2-naphthol; Sudan IV: 1-{[2-methyl-4-[(2-methylphenyl)azo]phenyl]azo}-2-naphthol",
        "ins_e_number": "Solvent Red 1 / 23 / 24",
        "category": "Non-Permitted Industrial Dye / Adulterant",
        "function": "Industrial Solvent Red Dye (Illegal in Food)",
        "aliases": ["sudan dye", "sudan i", "sudan ii", "sudan iii", "sudan iv", "solvent red"],
        "food_categories": ["Chilli Powder", "Paprika", "Curry Powder", "Palm Oil"],
        "india_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Strictly Illegal Adulterant)",
            "condition": "Mandatory testing for chilli exports and domestic spices",
            "source": "FSSAI Spices Standards"
        },
        "usa_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Banned in Food)",
            "condition": "Import Alert 99-08: Automatic detention of food products containing Sudan dyes",
            "source": "US FDA Import Alert 99-08"
        },
        "eu_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Zero tolerance; RASFF alert priority)",
            "condition": "Emergency measures on hot chilli and curry products (Decision 2004/92/EC)",
            "source": "Commission Decision 2004/92/EC"
        },
        "germany_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Zero tolerance)",
            "condition": "Import rejection and product recall mandatory",
            "source": "BVL / RASFF"
        },
        "uk_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Zero tolerance)",
            "condition": "Prohibited carcinogen",
            "source": "UK FSA"
        },
        "risk_classification": "Critical",
        "consumer_concerns": ["Genotoxic carcinogen (IARC Group 3)", "Bladder and liver tumors in laboratory testing"],
        "evidence_source": "EFSA Scientific Opinion on Sudan Dyes (2005); IARC Monographs",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Strict zero-tolerance ban globally. Industrial azo dyes used illegally to impart vivid red color to adulterated spice powders."
    },
    {
        "id": "lead_chromate",
        "common_name": "Lead Chromate",
        "scientific_name": "Lead(II) chromate (PbCrO4)",
        "ins_e_number": "Chrome Yellow / Pigment Yellow 34",
        "category": "Heavy Metal Poison / Industrial Pigment",
        "function": "Industrial Pigment (Illegal Adulterant)",
        "aliases": ["lead chromate", "chrome yellow", "pigment yellow 34"],
        "food_categories": ["Turmeric Powder", "Whole Turmeric Roots"],
        "india_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Severe Criminal Adulteration)",
            "condition": "Violates FSS Act Section 59; subject to heavy criminal prosecution",
            "source": "FSSAI Turmeric Quality Directives"
        },
        "usa_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Poisonous Adulterant)",
            "condition": "Import Alert 28-13 for lead contamination in turmeric",
            "source": "US FDA Import Alert 28-13"
        },
        "eu_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Strictly Prohibited)",
            "condition": "Maximum levels for Lead in spices: 0.80 mg/kg total lead (Regulation EU 2021/1317)",
            "source": "Regulation (EU) 2021/1317"
        },
        "germany_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0%",
            "condition": "Immediate recall and seizure under Heavy Metal regulations",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Not authorised",
            "code": "NOT_PERMITTED",
            "max_limit": "0%",
            "condition": "Prohibited toxic heavy metal",
            "source": "UK FSA"
        },
        "risk_classification": "Critical",
        "consumer_concerns": ["Irreversible brain damage & neurodevelopmental deficits in children", "Kidney failure & cardiovascular damage from heavy metal accumulation"],
        "evidence_source": "Stanford University Turmeric Lead Study (2019); WHO Lead Guidelines",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Zero tolerance worldwide. Highly hazardous heavy metal compound added illegally to brighten low-quality turmeric."
    },

    # ── Sweeteners ──
    {
        "id": "aspartame",
        "common_name": "Aspartame",
        "scientific_name": "Methyl L-alpha-aspartyl-L-phenylalaninate",
        "ins_e_number": "INS 951 / E951",
        "category": "Artificial Sweetener",
        "function": "High-Intensity Non-Nutritive Sweetener",
        "aliases": ["aspartame", "ins 951", "e951", "nutrasweet", "equal"],
        "food_categories": ["Diet Sodas", "Chewing Gum", "Sugar-Free Sweets", "Yogurt"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "700 ppm in carbonated drinks; 1000 ppm in confectionery",
            "condition": "Mandatory warning: 'CONTAINS ASPARTAME. NOT RECOMMENDED FOR CHILDREN. NOT FOR PHENYLKETONURICS'",
            "source": "FSSAI Regulation 2.4.5"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "ADI: 50 mg/kg bw/day",
            "condition": "Mandatory warning label: 'PHENYLKETONURICS: CONTAINS PHENYLALANINE'",
            "source": "US FDA 21 CFR §172.804"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "ADI: 40 mg/kg bw/day",
            "condition": "Mandatory label: 'contains a source of phenylalanine' / 'with sweetener(s)'",
            "source": "EFSA Scientific Opinion (2013); Regulation (EC) No 1333/2008"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU baseline applies",
            "condition": "Mandatory German label: 'enthält eine Phenylalaninquelle'",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits",
            "condition": "Mandatory Phenylketonuria warning",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Hazardous for individuals with Phenylketonuria (PKU)", "WHO IARC classified as Group 2B (possibly carcinogenic to humans) in 2023"],
        "evidence_source": "WHO IARC Monographs (2023); JECFA Evaluation (2023); EFSA (2013)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Permitted globally with an Acceptable Daily Intake of 40-50 mg/kg bw. In 2023, WHO IARC classified it as possibly carcinogenic (Group 2B), though JECFA, US FDA, and EFSA reaffirmed that current intake levels remain within safe bounds."
    },
    {
        "id": "acesulfame_k",
        "common_name": "Acesulfame Potassium (Ace-K)",
        "scientific_name": "Potassium 6-methyl-2,2-dioxo-2H-1,2lambda6,3-oxathiazin-4-olate",
        "ins_e_number": "INS 950 / E950 / Ace-K",
        "category": "Artificial Sweetener",
        "function": "High-Intensity Calorie-Free Sweetener",
        "aliases": ["acesulfame k", "acesulfame potassium", "ace-k", "ins 950", "e950"],
        "food_categories": ["Diet Soft Drinks", "Protein Shakes", "Desserts", "Bakery"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "300 ppm in soft drinks; 1000 ppm in confectionery",
            "condition": "Mandatory declaration of artificial sweetener",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "ADI: 15 mg/kg bw/day",
            "condition": "FDA approved general purpose sweetener",
            "source": "US FDA 21 CFR §172.800"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "ADI: 9 mg/kg bw/day",
            "condition": "Category specific limits in Annex II",
            "source": "EFSA ANS Panel Re-evaluation (2016)"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU Annex II limits",
            "condition": "Standard EU labeling requirements",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits",
            "condition": "Permitted sweetener",
            "source": "UK FSA"
        },
        "risk_classification": "Low-to-Moderate",
        "consumer_concerns": ["Contains methylene chloride breakdown traces in low-grade synthesis", "Persistent in environment / wastewater"],
        "evidence_source": "EFSA Scientific Opinion (2016); JECFA",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Broadly approved in all jurisdictions; frequently blended with Sucralose or Aspartame to mask bitter aftertastes."
    },
    {
        "id": "sucralose",
        "common_name": "Sucralose",
        "scientific_name": "1,6-Dichloro-1,6-dideoxy-beta-D-fructofuranosyl 4-chloro-4-deoxy-alpha-D-galactopyranoside",
        "ins_e_number": "INS 955 / E955 / Splenda",
        "category": "Artificial Sweetener",
        "function": "Chlorinated High-Intensity Sweetener",
        "aliases": ["sucralose", "ins 955", "e955", "splenda"],
        "food_categories": ["Beverages", "Baked Goods", "Dairy", "Syrups"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "300 ppm in carbonated water; 750 ppm in bakery",
            "condition": "Mandatory label declaration of artificial sweetener",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "ADI: 5 mg/kg bw/day",
            "condition": "Approved as general-purpose sweetener",
            "source": "US FDA 21 CFR §172.831"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "ADI: 15 mg/kg bw/day",
            "condition": "Annex II limits per category",
            "source": "Regulation (EC) No 1333/2008 Annex II"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU baseline applies",
            "condition": "Standard EU rules",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits",
            "condition": "Permitted sweetener",
            "source": "UK FSA"
        },
        "risk_classification": "Low-to-Moderate",
        "consumer_concerns": ["Potential gut microbiome alterations at high intake", "May generate chloropropanols if heated above 120°C in baking"],
        "evidence_source": "German Federal Institute for Risk Assessment (BfR) Opinion on heating Sucralose (2019); EFSA (2017)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Widely authorized across US, EU, Germany, UK, and India, though German health authorities (BfR) issue specific warnings against heating sucralose above baking temperatures due to possible toxic chlorinated byproduct formation."
    },
    {
        "id": "cyclamate",
        "common_name": "Cyclamate (Sodium / Calcium Cyclamate)",
        "scientific_name": "Sodium cyclohexylsulfamate",
        "ins_e_number": "INS 952 / E952",
        "category": "Artificial Sweetener",
        "function": "Low-Calorie Sweetener",
        "aliases": ["cyclamate", "sodium cyclamate", "calcium cyclamate", "ins 952", "e952"],
        "food_categories": ["Diet Beverages", "Tabletop Sweeteners", "Canned Fruits"],
        "india_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (Not approved under FSSAI)",
            "condition": "FSSAI does not include Cyclamate on its approved artificial sweeteners list",
            "source": "FSSAI Approved Sweeteners Regulations"
        },
        "usa_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (BANNED in USA since 1969)",
            "condition": "Banned by FDA after 1969 rat studies indicated bladder tumor risk; FDA petition re-reviews remain unapproved",
            "source": "US FDA 21 CFR §189.135"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "ADI: 7 mg/kg bw/day (expressed as cyclamic acid)",
            "condition": "Authorized in specified beverage and dessert categories under Regulation 1333/2008",
            "source": "Regulation (EC) No 1333/2008 Annex II; EFSA ANS Panel (2016)"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU baseline applies",
            "condition": "Complies with EU Annex II",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits",
            "condition": "Permitted sweetener",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Metabolized by gut bacteria to cyclohexylamine in some individuals", "Historical bladder cancer controversies"],
        "evidence_source": "US FDA Ban History (1969); EFSA Scientific Opinion (2016)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Major regulatory conflict: Cyclamate has been strictly banned in the US since 1969 and is not approved in India, but it is legally permitted and widely used in the EU, Germany, and the UK with an ADI of 7 mg/kg bw."
    },
    {
        "id": "saccharin",
        "common_name": "Saccharin",
        "scientific_name": "2H-1lambda6,2-benzothiazol-1,1,3-trione",
        "ins_e_number": "INS 954 / E954",
        "category": "Artificial Sweetener",
        "function": "Intense Non-Caloric Sweetener",
        "aliases": ["saccharin", "sodium saccharin", "ins 954", "e954", "sweet'n low"],
        "food_categories": ["Diet Soft Drinks", "Tabletop Sweeteners", "Canned Fruits"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "100 ppm in carbonated water; 500 ppm in pan masala / supari",
            "condition": "Mandatory statutory declaration",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Up to 12 mg/fluid oz in beverages",
            "condition": "US Congress removed cancer warning label mandate in 2000 after human irrelevance of rat bladder mechanism was proven",
            "source": "US FDA 21 CFR §180.37"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "ADI: 5 mg/kg bw/day",
            "condition": "Category limits in Annex II",
            "source": "Regulation (EC) No 1333/2008"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU baseline applies",
            "condition": "Standard EU rules",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits",
            "condition": "Permitted sweetener",
            "source": "UK FSA"
        },
        "risk_classification": "Low-to-Moderate",
        "consumer_concerns": ["Metallic/bitter aftertaste", "Historical cancer debates (now resolved in humans)"],
        "evidence_source": "US NTP Delisting Review; EFSA (2014)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Permitted across all jurisdictions with quantitative limits after extensive toxicological reviews established that rodent-specific bladder precipitate mechanisms do not apply to humans."
    },

    # ── Flavor Enhancers & Acidity Regulators ──
    {
        "id": "msg",
        "common_name": "Monosodium Glutamate (MSG)",
        "scientific_name": "Sodium 2-aminopentanedioate",
        "ins_e_number": "INS 621 / E621 / MSG",
        "category": "Flavour Enhancer",
        "function": "Umami / Savory Flavour Enhancer",
        "aliases": ["msg", "monosodium glutamate", "ins 621", "e621", "glutamate", "flavour enhancer (621)"],
        "food_categories": ["Instant Noodles", "Snacks", "Soups", "Seasoning Mixes", "Fast Food"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Good Manufacturing Practice (GMP) in designated food categories",
            "condition": "Must not be added to infant foods; mandatory label declaration: 'Contains Monosodium Glutamate'",
            "source": "FSSAI Regulation 2.12 & FSSAI 2016 MSG Guidance Circular"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP (Generally Recognized as Safe)",
            "condition": "Must be declared on ingredient label as 'Monosodium Glutamate'",
            "source": "US FDA 21 CFR §182.1"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Max 10 g/kg (1%) in food individually or in combination with other glutamates",
            "condition": "EFSA established group ADI of 30 mg/kg bw/day in 2017",
            "source": "EFSA Scientific Opinion on Glutamates (2017); Reg (EC) 1333/2008"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU baseline limits (10 g/kg)",
            "condition": "Mandatory declaration in German: 'Geschmacksverstärker: Mononatriumglutamat'",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits (10 g/kg)",
            "condition": "Permitted flavour enhancer",
            "source": "UK FSA"
        },
        "risk_classification": "Low-to-Moderate",
        "consumer_concerns": ["Hypersensitivity / 'MSG symptom complex' in a small subset of individuals", "High sodium contribution to diet"],
        "evidence_source": "EFSA Re-evaluation of glutamic acid and glutamates (2017); US FDA Review on MSG",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Recognized as safe globally when used within limits. In 2017, EFSA established a numerical group ADI (30 mg/kg bw) to prevent headaches and blood pressure spikes from extreme consumption, whereas US FDA and FSSAI regulate it under GMP."
    },
    {
        "id": "citric_acid",
        "common_name": "Citric Acid",
        "scientific_name": "2-hydroxypropane-1,2,3-tricarboxylic acid",
        "ins_e_number": "INS 330 / E330",
        "category": "Acidity Regulator / Antioxidant Synergist",
        "function": "Natural Organic Acid & Acidulant",
        "aliases": ["citric acid", "ins 330", "e330", "acidity regulator (330)"],
        "food_categories": ["Beverages", "Jams", "Candies", "Snacks", "Sauces"],
        "india_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Good Manufacturing Practice (GMP)",
            "condition": "Permitted general food additive",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP (GRAS additive)",
            "condition": "Unrestricted food use under GMP",
            "source": "US FDA 21 CFR §184.1033"
        },
        "eu_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis (GMP)",
            "condition": "Group I food additive",
            "source": "Regulation (EC) No 1333/2008 Annex II"
        },
        "germany_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Standard EU Group I rules",
            "source": "BVL"
        },
        "uk_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Permitted acidity regulator",
            "source": "UK FSA"
        },
        "risk_classification": "Low",
        "consumer_concerns": ["Can cause dental enamel erosion in high-acid sour candies and soft drinks"],
        "evidence_source": "JECFA; EFSA",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Universally accepted and safe across all countries as a natural intermediate in human cellular metabolism (Krebs Cycle)."
    },
    {
        "id": "sodium_bicarbonate",
        "common_name": "Sodium Bicarbonate (Baking Soda)",
        "scientific_name": "Sodium hydrogen carbonate",
        "ins_e_number": "INS 500ii / E500ii",
        "category": "Raising Agent / Acidity Regulator",
        "function": "Chemical Leavening Agent",
        "aliases": ["sodium bicarbonate", "baking soda", "ins 500ii", "ins 500(ii)", "e500ii", "e500(ii)", "raising agent (500ii)"],
        "food_categories": ["Bakery", "Biscuits", "Cakes", "Pancake Mixes"],
        "india_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Good Manufacturing Practice (GMP)",
            "condition": "Permitted raising agent",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP (GRAS)",
            "condition": "Standard leavening agent",
            "source": "US FDA 21 CFR §184.1736"
        },
        "eu_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Group I food additive",
            "source": "Regulation (EC) No 1333/2008"
        },
        "germany_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Standard EU rules",
            "source": "BVL"
        },
        "uk_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Permitted raising agent",
            "source": "UK FSA"
        },
        "risk_classification": "Low",
        "consumer_concerns": ["Contributes to dietary sodium content"],
        "evidence_source": "JECFA; EFSA",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Universally permitted as a harmless chemical leavener across all international jurisdictions."
    },

    # ── Emulsifiers, Stabilizers & Thickeners ──
    {
        "id": "lecithin",
        "common_name": "Lecithin (Soy / Sunflower)",
        "scientific_name": "Phosphatidylcholine mixture",
        "ins_e_number": "INS 322 / E322",
        "category": "Emulsifier",
        "function": "Natural Phospholipid Emulsifier",
        "aliases": ["lecithin", "soy lecithin", "sunflower lecithin", "ins 322", "ins 322i", "e322", "emulsifier (322)"],
        "food_categories": ["Chocolates", "Bakery", "Spreads", "Margarine"],
        "india_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP",
            "condition": "Must disclose source allergen if derived from soy",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP (GRAS)",
            "condition": "Must declare 'Soy' under FALCPA if derived from soybean",
            "source": "US FDA 21 CFR §184.1400"
        },
        "eu_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Mandatory allergen declaration if soy-derived (Regulation EU 1169/2011)",
            "source": "Regulation (EC) No 1333/2008"
        },
        "germany_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Allergen marking mandatory in German ('Sojalecithin')",
            "source": "BVL"
        },
        "uk_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Soy allergen declaration required",
            "source": "UK FSA"
        },
        "risk_classification": "Low",
        "consumer_concerns": ["Soy allergy trigger if soy-derived", "GMO awareness (if derived from conventional US GM soy)"],
        "evidence_source": "EFSA Scientific Opinion on Lecithins (2020)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Broadly approved and considered safe globally; regulatory requirements focus on mandatory soy allergen labeling."
    },
    {
        "id": "pgpr",
        "common_name": "PGPR (Polyglycerol Polyricinoleate)",
        "scientific_name": "Polyglycerol polyricinoleate",
        "ins_e_number": "INS 476 / E476",
        "category": "Emulsifier",
        "function": "Viscosity Reducer in Chocolate Manufacturing",
        "aliases": ["pgpr", "polyglycerol polyricinoleate", "ins 476", "e476", "emulsifier (476)"],
        "food_categories": ["Chocolate Coatings", "Candy Bars", "Low-Fat Spreads"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Max 0.5% in chocolate products",
            "condition": "FSSAI permitted emulsifier in chocolate and confectionery",
            "source": "FSSAI Regulations 2.4.15"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Up to 0.3% in chocolate formulations",
            "condition": "FDA GRAS Notice GRN 000216",
            "source": "US FDA GRAS Inventory"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Up to 5 g/kg (0.5%) in cocoa products; ADI increased to 25 mg/kg bw in 2017",
            "condition": "Annex II limits apply",
            "source": "EFSA Scientific Opinion (2017); Reg (EC) 1333/2008"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU baseline applies (max 5 g/kg)",
            "condition": "Standard EU rules",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits",
            "condition": "Permitted emulsifier",
            "source": "UK FSA"
        },
        "risk_classification": "Low",
        "consumer_concerns": ["Manufactured from castor bean oil and glycerol; used to substitute expensive cocoa butter"],
        "evidence_source": "EFSA Re-evaluation of PGPR (2017)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Approved globally up to 0.3-0.5% in chocolate products to improve flow properties during enrobing."
    },
    {
        "id": "guar_gum",
        "common_name": "Guar Gum",
        "scientific_name": "Cyamopsis tetragonoloba galactomannan",
        "ins_e_number": "INS 412 / E412",
        "category": "Thickener / Stabilizer",
        "function": "Plant Hydrocolloid Thickening Agent",
        "aliases": ["guar gum", "ins 412", "e412", "stabilizer (412)"],
        "food_categories": ["Ice Cream", "Sauces", "Bakery", "Dairy Desserts", "Gluten-Free Foods"],
        "india_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP (Major domestic Indian agricultural crop)",
            "condition": "Permitted stabilizer",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "0.35% to 2.0% depending on food category",
            "condition": "FDA GRAS additive",
            "source": "US FDA 21 CFR §184.1339"
        },
        "eu_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis (Group I additive)",
            "condition": "Prohibited in dehydrated foods intended for rehydration on ingestion (choking hazard)",
            "source": "Regulation (EC) No 1333/2008"
        },
        "germany_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Standard EU rules",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Permitted thickener",
            "source": "UK FSA"
        },
        "risk_classification": "Low",
        "consumer_concerns": ["Can cause mild bloating or gas at high doses due to soluble fiber fermentation"],
        "evidence_source": "EFSA Scientific Opinion on Guar Gum (2017)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Universally authorized natural plant fiber. India is the world's largest producer and exporter of food-grade guar gum."
    },
    {
        "id": "xanthan_gum",
        "common_name": "Xanthan Gum",
        "scientific_name": "Xanthomonas campestris polysaccharide",
        "ins_e_number": "INS 415 / E415",
        "category": "Thickener / Stabilizer",
        "function": "Fermentation Polysaccharide Stabilizer",
        "aliases": ["xanthan gum", "ins 415", "e415", "stabilizer (415)"],
        "food_categories": ["Salad Dressings", "Sauces", "Gluten-Free Bakery", "Beverages"],
        "india_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP",
            "condition": "Permitted stabilizer",
            "source": "FSSAI Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP (GRAS)",
            "condition": "General food use approved",
            "source": "US FDA 21 CFR §172.695"
        },
        "eu_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Group I food additive; prohibited in jelly mini-cups",
            "source": "Regulation (EC) No 1333/2008"
        },
        "germany_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Standard EU rules",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Quantum Satis",
            "condition": "Permitted thickener",
            "source": "UK FSA"
        },
        "risk_classification": "Low",
        "consumer_concerns": ["Digestive sensitivity / laxative effect at very high intakes"],
        "evidence_source": "EFSA Re-evaluation of Xanthan Gum (2017)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Broadly approved across all countries; essential hydrocolloid in modern food science and gluten-free baking."
    },
    {
        "id": "datem",
        "common_name": "DATEM (Diacetyl Tartaric Acid Esters of Mono- and Diglycerides)",
        "scientific_name": "Diacetyl tartaric acid esters of mono- and diglycerides",
        "ins_e_number": "INS 472e / E472e / DATEM",
        "category": "Emulsifier / Dough Conditioner",
        "function": "Dough Volume & Crumb Texture Enhancer",
        "aliases": ["datem", "diacetyl tartaric acid esters", "ins 472e", "e472e", "emulsifier (472e)"],
        "food_categories": ["Bread", "Buns", "Biscuits", "Rusk"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Up to 1.0% in bakery products",
            "condition": "FSSAI permitted emulsifier",
            "source": "FSSAI Regulations 2.4.15"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP (GRAS additive)",
            "condition": "Standard bread conditioner",
            "source": "US FDA 21 CFR §184.1101"
        },
        "eu_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Max 5 g/kg to 10 g/kg in bakery",
            "condition": "Annex II limits apply",
            "source": "Regulation (EC) No 1333/2008"
        },
        "germany_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "EU baseline applies",
            "condition": "Standard EU rules",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "UK statutory limits",
            "condition": "Permitted emulsifier",
            "source": "UK FSA"
        },
        "risk_classification": "Low",
        "consumer_concerns": ["Synthetic emulsifier; vegetarian source verification needed (can be derived from plant or animal fats)"],
        "evidence_source": "EFSA Scientific Opinion on DATEM (2020)",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Universally permitted dough conditioner used as a safe alternative to banned oxidizing agents like Potassium Bromate and Azodicarbonamide."
    },

    # ── Dietary Fats & Industrial Ingredients ──
    {
        "id": "palm_oil",
        "common_name": "Palm Oil / Palm Olein",
        "scientific_name": "Elaeis guineensis mesocarp oil",
        "ins_e_number": "Palm Oil / Fractionated Palm Olein",
        "category": "Edible Fat / Vegetable Oil",
        "function": "High-Yield Saturated Frying & Baking Fat",
        "aliases": ["palm oil", "palmolein", "palm olein", "refined palm oil", "fractionated palm olein", "rdb palmolein"],
        "food_categories": ["Instant Noodles", "Potato Chips", "Biscuits", "Chocolates", "Margarine"],
        "india_status": {
            "status": "Permitted with limits",
            "code": "PERMITTED_WITH_LIMITS",
            "max_limit": "Must meet FSSAI acid value, saponification, and iodine value standards",
            "condition": "Total trans fat in oil must not exceed 2% by weight (FSSAI Jan 2022 mandate)",
            "source": "FSSAI Food Safety and Standards (Packaging and Labelling) Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "Must disclose saturated fat on Nutrition Facts panel",
            "condition": "Used extensively as replacement for banned partially hydrogenated trans fats",
            "source": "US FDA Food Labeling Requirements"
        },
        "eu_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Strict maximum limits on 3-MCPD and Glycidyl Fatty Acid Esters (GE) (Regulation EU 2018/290)",
            "condition": "Mandatory specific vegetable oil declaration on label: 'Palm oil' (cannot hide as generic 'vegetable oil')",
            "source": "Regulation (EU) No 1169/2011; Regulation (EU) 2018/290 (Process Contaminants)"
        },
        "germany_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Strict enforcement of 3-MCPD / GE limits in infant foods and consumer goods",
            "condition": "High consumer pushback; extensive voluntary certification (RSPO)",
            "source": "BVL / German Federal Ministry of Food and Agriculture"
        },
        "uk_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Process contaminant limits apply",
            "condition": "Specific oil labeling required",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["High saturated fat content (approx 50% palmitic acid)", "Process contaminants (3-MCPD and Glycidyl Esters) formed during high-temperature refining", "Deforestation and environmental sustainability concerns"],
        "evidence_source": "EFSA Scientific Opinion on 3-MCPD and Glycidyl Esters in Palm Oil (2016); WHO/NIN Guidelines",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "While permitted everywhere as cooking oil, the EU and Germany require specific label transparency (no generic 'vegetable oil' hiding) and enforce strict legal limits on carcinogenic process contaminants (3-MCPD and Glycidyl Esters) formed during industrial high-temperature refining."
    },
    {
        "id": "trans_fats",
        "common_name": "Partially Hydrogenated Oils (Industrial Trans Fat)",
        "scientific_name": "Industrial trans-isomerized triglycerides",
        "ins_e_number": "PHO / Vanaspati / Shortening",
        "category": "Industrial Fat",
        "function": "Solidified Hydrogenated Fat with Long Shelf Life",
        "aliases": ["partially hydrogenated oil", "partially hydrogenated vegetable oil", "vanaspati", "dalda", "hydrogenated fat", "trans fat"],
        "food_categories": ["Commercial Bakery", "Pastries", "Frosting", "Margarine", "Fried Street Foods"],
        "india_status": {
            "status": "Category-specific restriction",
            "code": "RESTRICTED",
            "max_limit": "Max 2% of total fat by weight (FSSAI January 1, 2022 regulation)",
            "condition": "Mandatory 'Trans Fat Free' label only if trans fat < 0.2g per 100g",
            "source": "FSSAI Gazette Notification on Trans Fat Limits (2021)"
        },
        "usa_status": {
            "status": "Not permitted",
            "code": "NOT_PERMITTED",
            "max_limit": "0% (FDA revoked GRAS status for Partially Hydrogenated Oils)",
            "condition": "PHOs banned from US food supply since June 2018 (extended compliance 2020)",
            "source": "US FDA Final Determination on Partially Hydrogenated Oils (80 FR 34650)"
        },
        "eu_status": {
            "status": "Category-specific restriction",
            "code": "RESTRICTED",
            "max_limit": "Max 2 grams per 100 grams of fat (Regulation EU 2019/649)",
            "condition": "Strict legal cap across all retail and B2B food products",
            "source": "Commission Regulation (EU) 2019/649"
        },
        "germany_status": {
            "status": "Category-specific restriction",
            "code": "RESTRICTED",
            "max_limit": "Max 2g / 100g fat",
            "condition": "Enforced in commercial bakeries and catering",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Category-specific restriction",
            "code": "RESTRICTED",
            "max_limit": "Max 2g / 100g fat",
            "condition": "UK statutory limits apply",
            "source": "UK FSA"
        },
        "risk_classification": "Critical",
        "consumer_concerns": ["Major cardiovascular risk: directly raises LDL (bad) cholesterol and lowers HDL (good) cholesterol", "Directly linked by WHO to 500,000 premature coronary heart disease deaths annually"],
        "evidence_source": "WHO REPLACE Action Package (2018); US FDA Final Rule; FSSAI Mandate",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "The US FDA banned Partially Hydrogenated Oils entirely by revoking GRAS status, whereas India, the EU, Germany, and the UK legally capped industrial trans-fats at a strict maximum of 2% of total fat."
    },
    {
        "id": "high_fructose_corn_syrup",
        "common_name": "High Fructose Corn Syrup (HFCS)",
        "scientific_name": "Glucose-fructose syrup / Isoglucose",
        "ins_e_number": "HFCS-55 / HFCS-42 / Isoglucose",
        "category": "Nutritive Sweetener",
        "function": "Liquid Corn Starch-Derived Sweetener",
        "aliases": ["high fructose corn syrup", "hfcs", "glucose-fructose syrup", "isoglucose", "corn syrup"],
        "food_categories": ["Soft Drinks", "Ketchup", "Processed Cereals", "Candy", "Sauces"],
        "india_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP (Sugar labeling applies)",
            "condition": "Must declare total added sugars on nutrition panel",
            "source": "FSSAI Packaging and Labelling Regulations"
        },
        "usa_status": {
            "status": "Permitted",
            "code": "PERMITTED",
            "max_limit": "GMP (Widely used standard sweetener in US beverages)",
            "condition": "Must declare Added Sugars on Nutrition Facts panel",
            "source": "US FDA 21 CFR §184.1866"
        },
        "eu_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Historically restricted by EU production quotas; labeled as 'Glucose-Fructose Syrup' or 'Isoglucose'",
            "condition": "Subject to strict labeling rules under Regulation EU 1169/2011",
            "source": "Regulation (EU) No 1169/2011"
        },
        "germany_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "Standard EU rules",
            "condition": "German consumer goods heavily favor beet sugar over isoglucose",
            "source": "BVL Guidelines"
        },
        "uk_status": {
            "status": "Permitted with restrictions",
            "code": "PERMITTED_WITH_CONDITIONS",
            "max_limit": "UK statutory rules",
            "condition": "Labeled as Glucose-Fructose Syrup",
            "source": "UK FSA"
        },
        "risk_classification": "Moderate",
        "consumer_concerns": ["Rapid liver fructose overload linked to Non-Alcoholic Fatty Liver Disease (NAFLD)", "Spikes insulin resistance, visceral adiposity, and metabolic syndrome"],
        "evidence_source": "Harvard T.H. Chan School of Public Health; WHO Sugar Guidelines",
        "dataset_source": "Packaged Food Regulatory Database 2025",
        "last_verified_date": "2025-01-15",
        "cross_country_reason": "Heavily utilized in the USA due to agricultural corn subsidies, whereas the EU and Germany historically constrained isoglucose production via agricultural quotas, resulting in European formulations using traditional beet/cane sucrose instead."
    }
]

# Fast lookup indexes
_BY_ID: Dict[str, Dict[str, Any]] = {ing["id"]: ing for ing in INGREDIENT_DATABASE}

def get_all_ingredients() -> List[Dict[str, Any]]:
    """Returns full catalog of recognized ingredients with complete regulatory data."""
    return INGREDIENT_DATABASE

def get_ingredient_by_id(ing_id: str) -> Optional[Dict[str, Any]]:
    """Look up single ingredient by normalized identifier."""
    return _BY_ID.get(ing_id.lower().strip())

def search_ingredients(query: str) -> List[Dict[str, Any]]:
    """Searches ingredients by name, alias, INS/E number, or category."""
    q = query.lower().strip()
    if not q:
        return INGREDIENT_DATABASE
    results = []
    for ing in INGREDIENT_DATABASE:
        if (q in ing["id"] or 
            q in ing["common_name"].lower() or 
            q in ing["scientific_name"].lower() or 
            q in ing["ins_e_number"].lower() or 
            q in ing["category"].lower() or
            any(q in alias.lower() for alias in ing["aliases"])):
            results.append(ing)
    return results

def match_ingredient_text(raw_text: str) -> List[Dict[str, Any]]:
    """
    Parses raw ingredient text (from OCR or label) and maps each identified item
    to its normalized intelligence database entry.
    """
    if not raw_text:
        return []

    matched_items = []
    seen_ids = set()
    cleaned_lower = raw_text.lower()

    # Split into candidate tokens / phrases
    # Handles commas, semicolons, brackets, newlines
    tokens = re.split(r'[,;:\n\r\(\)\[\]]+', cleaned_lower)
    tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]

    # 1. Match each known database item against tokens or full text
    for ing in INGREDIENT_DATABASE:
        ing_id = ing["id"]
        if ing_id in seen_ids:
            continue

        matched = False
        matched_phrase = ""

        # Check aliases
        for alias in ing["aliases"]:
            # Use regex word boundary check where appropriate
            escaped_alias = re.escape(alias)
            pattern = rf'(?:^|[\s,;:\(\)\[\]]){escaped_alias}(?:$|[\s,;:\(\)\[\]])'
            if re.search(pattern, cleaned_lower):
                matched = True
                matched_phrase = alias
                break

        if matched:
            seen_ids.add(ing_id)
            matched_items.append({
                "database_id": ing["id"],
                "common_name": ing["common_name"],
                "scientific_name": ing["scientific_name"],
                "ins_e_number": ing["ins_e_number"],
                "category": ing["category"],
                "function": ing["function"],
                "risk_classification": ing["risk_classification"],
                "consumer_concerns": ing["consumer_concerns"],
                "matched_text": matched_phrase or ing["common_name"],
                "india_status": ing["india_status"],
                "usa_status": ing["usa_status"],
                "eu_status": ing["eu_status"],
                "germany_status": ing["germany_status"],
                "uk_status": ing["uk_status"],
                "cross_country_reason": ing["cross_country_reason"],
                "evidence_source": ing["evidence_source"]
            })

    return matched_items

def get_supported_countries() -> List[Dict[str, Any]]:
    """Returns list of supported countries, codes, authorities, and flags."""
    return SUPPORTED_COUNTRIES
