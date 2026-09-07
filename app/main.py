"""
SpecStream AI - "Zero-Schema" Multi-Modal Catalog Ingestor.
FastAPI Main Application Web Server & REST API.
"""

import os
import json
import logging
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.models.catalog_schema import (
    CatalogItem, CatalogItemValidation, ExtractedCatalog,
    EClassMatch, BMEcatHeaderConfig
)
from app.services.vector_search import vector_engine
from app.services.schema_validator import validate_item
from app.services.extractor import parse_pdf_bytes, parse_image_bytes, parse_csv_bytes, parse_text_bytes
from app.services.exporter import generate_bmecat_xml, generate_cxml, generate_enterprise_csv
from app.data.sample_catalogs import SAMPLE_CATALOGS
from app.data.eclass_db import ECLASS_7_1_DATABASE, UNECE_UOM_CODES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("specstream")

app = FastAPI(
    title="SpecStream AI - Zero-Schema Catalog Ingestor",
    description="Multi-modal supplier catalog ingestion, Pydantic validation, eCl@ss vector search, and BMEcat XML export.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExportRequest(BaseModel):
    items: List[CatalogItem]
    format: str = "bmecat"  # "bmecat" | "cxml" | "csv"
    config: Optional[BMEcatHeaderConfig] = None


class MatchEClassRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    specs: Optional[Dict[str, str]] = None
    keywords: Optional[List[str]] = None


# --- REST API Endpoints ---

@app.get("/api/samples")
def get_sample_catalogs():
    """Returns available sample catalog metadata for 1-click ingest."""
    samples = []
    for key, data in SAMPLE_CATALOGS.items():
        samples.append({
            "id": key,
            "title": data["title"],
            "supplier_name": data["supplier_name"],
            "file_type": data["file_type"],
            "item_count": len(data["items"])
        })
    return {"samples": samples}


@app.get("/api/sample/{sample_id}", response_model=ExtractedCatalog)
def get_sample_catalog_data(sample_id: str):
    """Loads a specific pre-baked sample catalog dataset."""
    if sample_id not in SAMPLE_CATALOGS:
        raise HTTPException(status_code=404, detail="Sample catalog not found")

    sample = SAMPLE_CATALOGS[sample_id]
    items = [CatalogItem(**item_dict) for item_dict in sample["items"]]
    validations = [validate_item(item) for item in items]

    return ExtractedCatalog(
        catalog_id=f"CAT-SAMPLE-{sample_id}",
        title=sample["title"],
        supplier_name=sample["supplier_name"],
        file_type=sample["file_type"],
        doc_preview=sample["doc_preview"],
        bounding_boxes=sample["bounding_boxes"],
        items=items,
        validations=validations
    )


@app.post("/api/extract", response_model=ExtractedCatalog)
async def extract_catalog_file(
    file: UploadFile = File(...),
    api_key: Optional[str] = Form(None)
):
    """Ingests uploaded PDF, Image, CSV, or Text catalog file and performs multimodal AI extraction."""
    filename = file.filename or "uploaded_file"
    file_bytes = await file.read()

    # Check environment variable or form parameter for Gemini API key
    effective_api_key = api_key or os.getenv("GEMINI_API_KEY", "")

    ext = filename.split(".")[-1].lower() if "." in filename else ""

    if ext == "csv":
        return parse_csv_bytes(file_bytes, filename)
    elif ext in ["pdf"]:
        return parse_pdf_bytes(file_bytes, filename, api_key=effective_api_key)
    elif ext in ["png", "jpg", "jpeg", "webp"]:
        return parse_image_bytes(file_bytes, filename, api_key=effective_api_key)
    elif ext in ["txt", "text", "spec", "md"]:
        return parse_text_bytes(file_bytes, filename)
    else:
        return parse_pdf_bytes(file_bytes, filename, api_key=effective_api_key)


@app.post("/api/validate", response_model=CatalogItemValidation)
def validate_catalog_item(item: CatalogItem):
    """Validates single item against Pydantic schema rules."""
    return validate_item(item)


@app.post("/api/match-eclass", response_model=List[EClassMatch])
def match_eclass_code(req: MatchEClassRequest):
    """Runs vector search cosine similarity to match product specs to eCl@ss 7.1 codes."""
    return vector_engine.search(
        title=req.title,
        description=req.description or "",
        specs=req.specs or {},
        keywords=req.keywords or [],
        top_k=5
    )


@app.get("/api/eclass/all")
def get_all_eclass_categories():
    """Returns list of all available eCl@ss 7.1 categories."""
    return {"categories": ECLASS_7_1_DATABASE, "uom_codes": UNECE_UOM_CODES}


@app.post("/api/export")
def export_catalog(req: ExportRequest):
    """Generates BMEcat 1.2 XML, cXML, or Enterprise CSV export content."""
    config = req.config or BMEcatHeaderConfig()

    if req.format == "cxml":
        content = generate_cxml(req.items, config)
        media_type = "application/xml"
        filename = f"{config.catalog_id}_cxml.xml"
    elif req.format == "csv":
        content = generate_enterprise_csv(req.items)
        media_type = "text/csv"
        filename = f"{config.catalog_id}_catalog.csv"
    else:
        content = generate_bmecat_xml(req.items, config)
        media_type = "application/xml"
        filename = f"{config.catalog_id}_bmecat.xml"

    return {
        "format": req.format,
        "filename": filename,
        "content": content
    }


# Static Files Mount & SPA serving
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>SpecStream AI Server Running</h1>"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
