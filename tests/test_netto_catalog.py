"""
Test script for Article Boundary Chunking on Netto Retail Catalog Page 1 text.
"""

import unittest
from app.services.extractor import _ai_layout_agnostic_chunker, parse_pdf_bytes

netto_page_1_text = """
Montag, 31.08.26 – Samstag, 05.09.26
SPAR GANZ NAH

Söhnlein Brillant Sekt trocken oder alkoholfrei
0,75 Liter
2.69 UVP 4.29 –37%

Jacobs Krönung Kaffee gemahlen oder ganze Bohnen, versch. Sorten
500 g
5.99 UVP 9.99 –40%

Ehrmann Almighurt Joghurt gekühlt, versch. Sorten
100 g – 150 g
0.29 0.89 –67%

Schweine-Nacken/Kamm ohne Knochen
100 g
0.66 1.19 –44%

Möhren Deutschland, Kl. I
2 kg Beutel
1.29 UVP 1.79 –27%

Nektarinen Italien/Spanien, Kl. I
1 kg Schale
1.69 UVP 2.19 –22%

Coppenrath & Wiese Brötchen tiefgekühlt, versch. Sorten
450 g – 540 g
1.49 2.29 –34%

Philadelphia Frischkäse/-zubereitung gekühlt, versch. Sorten
100 g – 195 g
0.99 2.29 –56%

Kinder Riegel, Duplo oder Kinder Country versch. Sorten
327 g – 420 g
4.44 UVP 5.39 –17%

Persil Waschmittel versch. Sorten
76 Waschladungen – 100 Waschladungen
16.99 UVP 27.99 –39%

Nutella Nuss-Nugat-Creme
825 g
4.44 UVP 5.79 –23%

Gerolsteiner Mineralwasser oder Nearwater versch. Sorten
6 x 1,5 Liter
4.69 6.54 –28%

Paulaner Spezi oder Zero koffeinhaltig
20 x 0,5 Liter
9.99 UVP 16.49 –39%
"""

lines = [l.strip() for l in netto_page_1_text.split('\n') if len(l.strip()) >= 2]
blocks = _ai_layout_agnostic_chunker(lines)

print("=== Netto Retail Catalog Boundary Recognition Result ===")
print(f"Total Article Blocks Identified: {len(blocks)}\n")

for idx, b in enumerate(blocks, 1):
    price_str = f"€{b['price']}" if b.get('price') else "No price"
    print(f"Article #{idx}: {b['title']} -> Price: {price_str}")
