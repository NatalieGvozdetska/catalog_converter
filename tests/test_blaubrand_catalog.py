"""
Test script for Article Boundary Chunking on BLAUBRAND Laboratory Volumetric Instruments catalog (Page 7).
"""

import unittest
from app.services.extractor import _parse_article_blocks, parse_pdf_bytes

blaubrand_page_7_text = """
VOLUMETRIC INSTRUMENTS
7
Ordering information
1 Volumetric flasks

Volumetric flasks, BLAUBRAND®, class A, DE-M
Boro 3.3. DIN EN ISO 1042. Calibrated to contain (TC, In).

Capacity ml Description Closure option Cat. No.
5 - 10000 with ISO batch certificate PP/PE stopper 37233 - 37293
with ISO individual certificate PP/PE stopper 937233 - 937293
5 - 5000 with ISO batch certificate glass stopper 37256 - 37294
with ISO individual certificate glass stopper 937256 - 937294
10 - 1000 with ISO batch certificate, beaded rim without stopper 37045 - 37053
with ISO individual certificate, beaded rim without stopper 937045 - 937053
5 - 2000 with USP batch certificate PP stopper 36938 - 36954
with USP individual certificate PP stopper 956938 - 956954
with USP batch certificate glass stopper 36968 - 36984
with USP individual certificate glass stopper 956968 - 956984

Volumetric flasks, BLAUBRAND®, class A, DE-M, amber
Boro 3.3. DIN EN ISO 1042. Calibrated to contain (TC, In).

Capacity ml Description Closure option Cat. No.
5 - 1000 with ISO batch certificate PP stopper 37401 - 37413
with ISO individual certificate PP stopper 937401 - 937413
with ISO batch certificate glass stopper 37438 - 37453
with ISO individual certificate glass stopper 937438 - 937453
5 - 1000 with USP batch certificate PP stopper 37481 - 37491
with USP individual certificate PP stopper 957481 - 957491
with USP batch certificate glass stopper 37461 - 37471
with USP individual certificate glass stopper 957461 - 957471
"""

lines = [l.strip() for l in blaubrand_page_7_text.split('\n') if len(l.strip()) > 0]
blocks = _parse_article_blocks(lines)

print(f"=== Article Boundary Recognition Result ===")
print(f"Total Article Blocks Identified: {len(blocks)}\n")

for idx, b in enumerate(blocks):
    print(f"Article #{idx+1}:")
    print(f"  Title: {b['title']}")
    print(f"  Extracted Cat Numbers: {b['cat_numbers'][:5]}")
    print(f"  Total context lines aggregated: {len(b['lines'])}\n")
