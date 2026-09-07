"""
Test AI Core Head Noun Extraction & Language Classification.
"""

from app.services.vector_search import extract_core_product_head_noun_and_language, vector_engine

items = [
    "Ehrmann Almighurt Joghurt gekühlt",
    "Jacobs Krönung Kaffee gemahlen",
    "Söhnlein Brillant Sekt trocken",
    "DANONE Activia mit natürlichen Bifidus-Kulturen, versch. Sorten",
    "Volumetric flasks BLAUBRAND class A",
    "Hexagon head bolt M8x30 DIN 933"
]

print("=== AI Core Head Noun & Language Preprocessing Test ===")
for item in items:
    core_noun, lang = extract_core_product_head_noun_and_language(item)
    matches = vector_engine.search(title=item, top_k=1)
    matched = matches[0] if matches else None
    print(f"Input: '{item}'")
    print(f" -> Core Head Noun: '{core_noun}' | Language: '{lang}'")
    print(f" -> eClass Code: {matched.code} ({matched.name}) [{matched.confidence}%]\n")
