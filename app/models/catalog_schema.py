"""
Pydantic v2 Schemas for SpecStream AI.
Enforces strict schema validation contracts for extracted catalog items,
validation diagnostics, eCl@ss vector matches, and export settings.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator


class ValidationIssue(BaseModel):
    field: str
    severity: str  # "ERROR" | "WARNING"
    code: str
    message: str


class CatalogItem(BaseModel):
    supplier_item_id: str = Field(..., description="Unique supplier SKU or item identifier")
    title: str = Field(..., min_length=3, description="Standardized product title")
    description: str = Field(..., min_length=10, description="Detailed product specification summary")
    price: float = Field(..., gt=0, description="Unit price, must be greater than zero")
    currency: str = Field(default="EUR", description="ISO 4217 Currency code (e.g., EUR, USD, GBP)")
    uom: str = Field(default="C62", description="UN/ECE Recommendation 20 Unit of Measure (e.g., C62, MTR, KGM, P1)")
    mpn: Optional[str] = Field(default="", description="Manufacturer Part Number")
    manufacturer: Optional[str] = Field(default="", description="Manufacturer Brand Name")
    specs: Dict[str, str] = Field(default_factory=dict, description="Key-Value technical specs (e.g., Voltage, Thread Size)")
    keywords: List[str] = Field(default_factory=list, description="Search & indexing keywords")
    eclass_code: Optional[str] = Field(default="", description="Mapped 8-digit eCl@ss 7.1 taxonomy code")

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        valid_currencies = {"EUR", "USD", "GBP", "CHF", "CAD", "AUD", "JPY"}
        upper_v = v.upper().strip()
        if upper_v not in valid_currencies:
            raise ValueError(f"Unrecognized ISO currency '{v}'. Must be one of {sorted(list(valid_currencies))}")
        return upper_v


class CatalogItemValidation(BaseModel):
    supplier_item_id: str
    status: str  # "VALID" | "WARNING" | "ERROR"
    score: int  # Quality score 0 - 100
    issues: List[ValidationIssue] = Field(default_factory=list)


class EClassMatch(BaseModel):
    code: str
    name: str
    segment: str
    main_group: str
    description: str
    confidence: float  # Percentage score 0.0 - 100.0
    matched_terms: List[str] = Field(default_factory=list)


class DocumentBoundingBox(BaseModel):
    item_idx: int
    x: float
    y: float
    w: float
    h: float
    label: str


class DocumentPreview(BaseModel):
    header: str = ""
    subtitle: str = ""
    raw_text: str = ""


class ExtractedCatalog(BaseModel):
    catalog_id: str
    title: str
    supplier_name: str
    file_type: str
    doc_preview: DocumentPreview
    bounding_boxes: List[DocumentBoundingBox] = Field(default_factory=list)
    items: List[CatalogItem] = Field(default_factory=list)
    validations: List[CatalogItemValidation] = Field(default_factory=list)


class BMEcatHeaderConfig(BaseModel):
    catalog_id: str = "CAT-2026-001"
    catalog_name: str = "Standard Supplier Catalog 2026"
    supplier_name: str = "Supplier Inc."
    supplier_id: str = "SUP-10042"
    buyer_name: str = "Enterprise Procurement Corp"
    currency: str = "EUR"
    language: str = "eng"
    generation_date: str = "2026-08-30"
