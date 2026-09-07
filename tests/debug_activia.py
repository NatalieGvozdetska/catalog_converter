"""
Diagnostic script to trace why DANONE Activia got assigned to 27-14-11-06 (Cable Gland).
"""

from app.services.vector_search import vector_engine

title = "DANONE Activia mit natürlichen Bifidus-Kulturen, versch. Sorten, 3,5 % Fett im Milchanteil"
matches = vector_engine.search(title=title, top_k=5)

print("=== Vector Search Diagnostic for DANONE Activia ===")
for m in matches:
    print(f"Code: {m.code} | Name: {m.name} | Conf: {m.confidence}% | Matched Terms: {m.matched_terms}")
