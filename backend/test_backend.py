"""
Comprehensive Backend & Multi-Criteria Food Safety Test Script
Tests all 4 pillars, regulatory comparisons, consumer rules, decision trace, and endpoints.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.app.main import app

def run_all_tests():
    client = TestClient(app)
    print("=" * 70)
    print("RUNNING FOODGUARD AI 4-PILLAR PLATFORM TESTS")
    print("=" * 70)

    # 1. Health Check
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health = res.json()
    print(f"[OK] Health check passed: {health['service']} (v{health['version']})")
    print(f"     Total ingredients indexed: {health['total_ingredients_in_database']}")

    # 2. Supported Countries
    res = client.get("/api/countries")
    assert res.status_code == 200 and len(res.json()) >= 5
    countries = res.json()
    print(f"[OK] Supported countries verified ({len(countries)}): {[c['name'] for c in countries]}")

    # 3. Centralized Regulatory Ingredients Catalog
    res = client.get("/api/regulatory/ingredients")
    assert res.status_code == 200 and len(res.json()) >= 20
    print(f"[OK] Regulatory ingredients catalog loaded: {len(res.json())} ingredients.")

    # 4. Search Ingredient (Tartrazine)
    res = client.get("/api/regulatory/ingredients?search=Tartrazine")
    assert res.status_code == 200 and len(res.json()) > 0
    tart = res.json()[0]
    print(f"[OK] Tartrazine query check:")
    print(f"     India: {tart['india_status']['status']} | EU: {tart['eu_status']['status']}")
    print(f"     Cross-Country Rationale: {tart['cross_country_reason'][:75]}...")

    # 5. Consumer Rules
    res = client.get("/api/consumer/rules")
    assert res.status_code == 200 and len(res.json()) >= 5
    print(f"[OK] Consumer rules loaded: {len(res.json())} rules with source citations.")

    # 6. Barcode Lookup: Maggi Noodles (Multi-Criteria Evaluation)
    res = client.get("/api/barcode/8901058852813?country=IN")
    assert res.status_code == 200, f"Barcode scan failed: {res.text}"
    data = res.json()
    print(f"[OK] Maggi Noodles Multi-Criteria Analysis:")
    print(f"     Score: {data['quality_score']}/100 | Overall Verdict: {data['overall_assessment']}")
    print(f"     Pillar 1 Adulteration: {data['adulteration']['status']}")
    print(f"     Pillar 2 Risk: {data['risk']['risk_tier']} (Overall: {data['risk']['overall_risk_pct']}%)")
    print(f"     Pillar 3 Regulatory (India): {data['regulatory']['selected_country']['verdict']}")
    print(f"     Pillar 4 Consumer: {data['consumer']['verdict']}")
    print(f"     Decision Trace Steps: {len(data['decision_trace']['steps'])} steps executed.")

    # 7. Adulterated Turmeric Test (Lead Chromate + Metanil Yellow)
    res = client.get("/api/barcode/9990000000001?country=IN")
    assert res.status_code == 200
    data = res.json()
    print(f"[OK] Adulterated Turmeric Test:")
    print(f"     Overall Assessment: {data['overall_assessment']}")
    print(f"     Adulteration Status: {data['adulteration']['status']} (Critical Flags: {data['adulteration']['has_critical_flags']})")
    assert data["adulteration"]["has_critical_flags"] is True

    # 8. Cross-Country Regulatory Comparison Endpoint
    res = client.get("/api/regulatory/compare?ingredients=Sugar, Palm Oil, Titanium Dioxide, Tartrazine, TBHQ&country=DE")
    assert res.status_code == 200
    comp = res.json()
    print(f"[OK] Cross-Country Comparison Check:")
    print(f"     Divergent ingredients found: {comp['comparison']['divergence_count']}")
    print(f"     Germany Verdict: {comp['selected_country_compliance']['verdict']}")

    # 9. Consumer Preferences Suitability Endpoint
    res = client.post("/api/consumer/evaluate", json={
        "ingredients": "Wheat flour, Sugar, Palm Oil, Cocoa butter, Soy Lecithin",
        "nutrition": { "sugar_g": 38.0, "sodium_mg": 120.0 },
        "preferences": { "low_sugar": True, "vegetarian": True, "vegan": True }
    })
    assert res.status_code == 200
    cons_res = res.json()
    print(f"[OK] Consumer Preferences Evaluation:")
    print(f"     Verdict: {cons_res['verdict']} | Concerns count: {len(cons_res['concerns'])}")

    # 10. Dashboard Stats
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    stats = res.json()
    print(f"[OK] Dashboard Stats: {stats['products_scanned_count']} scans, {stats['regulatory_conflicts_count']} regulatory conflicts.")

    # 11. Chatbot Contextual Query
    res = client.post("/api/chat", json={
        "message": "Why is Titanium Dioxide banned in the EU but permitted in the US?",
        "context": None
    })
    assert res.status_code == 200
    chat_out = res.json()
    print(f"[OK] Chatbot AI Assistant Query Response received ({len(chat_out['response_text'])} chars).")

    print("\n" + "=" * 70)
    print("ALL 11 BACKEND, REGULATORY & MULTI-CRITERIA TESTS PASSED!")
    print("=" * 70)

if __name__ == "__main__":
    run_all_tests()
