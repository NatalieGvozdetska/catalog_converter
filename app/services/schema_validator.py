"""
Schema Validation Service for SpecStream AI.
Executes Pydantic-driven strict validation rules on extracted catalog items,
returning granular diagnostic messages, validation status flags, and quality scores.
"""

import re
from typing import List
from app.models.catalog_schema import CatalogItem, CatalogItemValidation, ValidationIssue
from app.data.eclass_db import UNECE_UOM_CODES


def validate_item(item: CatalogItem) -> CatalogItemValidation:
    """Evaluates catalog item against enterprise catalog quality and Pydantic rules."""
    issues: List[ValidationIssue] = []
    score = 100

    # 1. Supplier Item ID check
    if not item.supplier_item_id or len(item.supplier_item_id.strip()) == 0:
        issues.append(ValidationIssue(
            field="supplier_item_id",
            severity="ERROR",
            code="MISSING_ID",
            message="Supplier Item SKU ID is missing or empty."
        ))
        score -= 30

    # 2. Title validation
    if not item.title or len(item.title.strip()) < 3:
        issues.append(ValidationIssue(
            field="title",
            severity="ERROR",
            code="TITLE_TOO_SHORT",
            message="Item title is too short or missing (minimum 3 characters required)."
        ))
        score -= 25

    # 3. Description quality check
    if not item.description or len(item.description.strip()) < 10:
        issues.append(ValidationIssue(
            field="description",
            severity="WARNING",
            code="DESCRIPTION_SPARSE",
            message="Description is brief. Detailed specifications improve procurement searchability."
        ))
        score -= 10

    # 4. Price check
    if item.price is None or item.price <= 0:
        issues.append(ValidationIssue(
            field="price",
            severity="ERROR",
            code="INVALID_PRICE",
            message="Unit price must be a positive number greater than 0.00."
        ))
        score -= 30
    elif item.price > 100000:
        issues.append(ValidationIssue(
            field="price",
            severity="WARNING",
            code="HIGH_PRICE_ANOMALY",
            message="Price exceeds $100,000. Verify unit of measure scale."
        ))
        score -= 5

    # 5. UN/ECE Unit of Measure check
    uom_code = item.uom.upper().strip() if item.uom else ""
    if not uom_code:
        issues.append(ValidationIssue(
            field="uom",
            severity="ERROR",
            code="MISSING_UOM",
            message="Unit of Measure (UOM) is required."
        ))
        score -= 20
    elif uom_code not in UNECE_UOM_CODES:
        issues.append(ValidationIssue(
            field="uom",
            severity="WARNING",
            code="NON_STANDARD_UOM",
            message=f"UOM '{item.uom}' is non-standard. Enterprise systems prefer UN/ECE codes (e.g. C62 for Piece, MTR for Meter)."
        ))
        score -= 10

    # 6. MPN check
    if not item.mpn or len(item.mpn.strip()) == 0:
        issues.append(ValidationIssue(
            field="mpn",
            severity="WARNING",
            code="MISSING_MPN",
            message="Manufacturer Part Number (MPN) is omitted."
        ))
        score -= 5

    # 7. eCl@ss classification check
    if not item.eclass_code:
        issues.append(ValidationIssue(
            field="eclass_code",
            severity="WARNING",
            code="UNCLASSIFIED_ECLASS",
            message="Item is not yet mapped to an eCl@ss 7.1 classification code."
        ))
        score -= 15
    elif not re.match(r'^\d{2}-\d{2}-\d{2}-\d{2}$', item.eclass_code):
        issues.append(ValidationIssue(
            field="eclass_code",
            severity="WARNING",
            code="INVALID_ECLASS_FORMAT",
            message=f"eCl@ss code '{item.eclass_code}' should follow standard 8-digit format XX-XX-XX-XX."
        ))
        score -= 10

    # Determine overall status
    has_errors = any(i.severity == "ERROR" for i in issues)
    has_warnings = any(i.severity == "WARNING" for i in issues)

    if has_errors:
        status = "ERROR"
    elif has_warnings:
        status = "WARNING"
    else:
        status = "VALID"

    return CatalogItemValidation(
        supplier_item_id=item.supplier_item_id or "UNKNOWN",
        status=status,
        score=max(0, score),
        issues=issues
    )
