"""
Test script for eCl@ss taxonomy matching accuracy across food, beverage, lab, and industrial items.
"""

import unittest
from app.services.vector_search import VectorSearchEngine

engine = VectorSearchEngine()

test_cases = [
    ("Ehrmann Almighurt Joghurt gekühlt", "16-01-01-01", "Dairy product / Yogurt"),
    ("Jacobs Krönung Kaffee gemahlen", "16-02-01-01", "Coffee / Tea"),
    ("Söhnlein Brillant Sekt trocken", "16-03-02-01", "Wine / Sekt"),
    ("Persil Waschmittel 100 WL", "29-11-01-01", "Detergent / Laundry care"),
    ("Nutella Nuss-Nugat-Creme", "16-07-01-01", "Confectionery / Chocolate"),
    ("Volumetric flasks BLAUBRAND class A", "32-01-02-01", "Laboratory glassware"),
    ("Hexagon head bolt M8x30 DIN 933", "23-11-01-01", "Hexagon head bolt")
]

print("=== eCl@ss Taxonomy Matching Accuracy Test ===")
for title, expected_code, expected_name in test_cases:
    matches = engine.search(title=title, top_k=1)
    matched = matches[0] if matches else None
    code = matched.code if matched else "NONE"
    name = matched.name if matched else "NONE"
    conf = matched.confidence if matched else 0
    status = "✓ PASS" if code == expected_code else f"✗ FAIL (Expected {expected_code})"
    print(f"[{status}] '{title}' -> {code} ({name}) [{conf}% confidence]")
