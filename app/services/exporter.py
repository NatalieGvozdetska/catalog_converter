"""
Multi-Format Enterprise Exporter for SpecStream AI.
Generates valid BMEcat 1.2 XML, cXML (Commerce XML), and Enterprise CSV catalog exports.
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import io
import csv
from typing import List
from app.models.catalog_schema import CatalogItem, BMEcatHeaderConfig
from app.data.eclass_db import ECLASS_7_1_DATABASE


def generate_bmecat_xml(items: List[CatalogItem], config: BMEcatHeaderConfig) -> str:
    """Generates standard-compliant BMEcat 1.2 XML document string."""
    bmecat = ET.Element("BMECAT", attrib={"version": "1.2", "xmlns": "http://www.bmecat.org/bmecat/1.2"})

    # HEADER Section
    header = ET.SubElement(bmecat, "HEADER")

    catalog = ET.SubElement(header, "CATALOG")
    ET.SubElement(catalog, "LANGUAGE").text = config.language
    ET.SubElement(catalog, "CATALOG_ID").text = config.catalog_id
    ET.SubElement(catalog, "CATALOG_VERSION").text = "1.0"
    ET.SubElement(catalog, "CATALOG_NAME").text = config.catalog_name
    ET.SubElement(catalog, "DATETIME", attrib={"type": "generation_date"}).text = config.generation_date
    ET.SubElement(catalog, "CURRENCY").text = config.currency

    supplier = ET.SubElement(header, "SUPPLIER")
    ET.SubElement(supplier, "SUPPLIER_ID").text = config.supplier_id
    ET.SubElement(supplier, "SUPPLIER_NAME").text = config.supplier_name

    buyer = ET.SubElement(header, "BUYER")
    ET.SubElement(buyer, "BUYER_NAME").text = config.buyer_name

    # T_NEW_CATALOG Section
    t_new = ET.SubElement(bmecat, "T_NEW_CATALOG")

    for item in items:
        article = ET.SubElement(t_new, "ARTICLE")

        # Supplier Article ID
        ET.SubElement(article, "SUPPLIER_AID").text = item.supplier_item_id

        # ARTICLE_DETAILS
        details = ET.SubElement(article, "ARTICLE_DETAILS")
        ET.SubElement(details, "DESCRIPTION_SHORT").text = item.title[:80]
        ET.SubElement(details, "DESCRIPTION_LONG").text = item.description

        if item.manufacturer:
            ET.SubElement(details, "MANUFACTURER_NAME").text = item.manufacturer
        if item.mpn:
            ET.SubElement(details, "MANUFACTURER_AID").text = item.mpn

        for kw in item.keywords[:5]:
            ET.SubElement(details, "KEYWORD").text = kw

        # ARTICLE_FEATURES (eCl@ss classification & technical specs)
        if item.eclass_code or item.specs:
            features = ET.SubElement(article, "ARTICLE_FEATURES")
            if item.eclass_code:
                ET.SubElement(features, "REFERENCE_FEATURE_SYSTEM_NAME").text = "eCl@ss-7.1"
                ET.SubElement(features, "REFERENCE_FEATURE_GROUP_ID").text = item.eclass_code

            for key, val in item.specs.items():
                feat = ET.SubElement(features, "FEATURE")
                ET.SubElement(feat, "FNAME").text = key
                ET.SubElement(feat, "FVALUE").text = str(val)

        # ARTICLE_ORDER_DETAILS
        order_details = ET.SubElement(article, "ARTICLE_ORDER_DETAILS")
        ET.SubElement(order_details, "ORDER_UNIT").text = item.uom or "C62"
        ET.SubElement(order_details, "CONTENT_UNIT").text = item.uom or "C62"
        ET.SubElement(order_details, "NO_CU_PER_OU").text = "1"

        # ARTICLE_PRICE_DETAILS
        price_details = ET.SubElement(article, "ARTICLE_PRICE_DETAILS")
        price_elem = ET.SubElement(price_details, "ARTICLE_PRICE", attrib={"price_type": "net"})
        ET.SubElement(price_elem, "PRICE_AMOUNT").text = f"{item.price:.2f}"
        ET.SubElement(price_elem, "PRICE_CURRENCY").text = item.currency or "EUR"

    # Pretty format XML string
    rough_string = ET.tostring(bmecat, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def generate_cxml(items: List[CatalogItem], config: BMEcatHeaderConfig) -> str:
    """Generates standard cXML (Commerce XML) catalog document string."""
    cxml = ET.Element("cXML", attrib={"payloadID": f"CATALOG-{config.catalog_id}@specstream.ai", "timestamp": f"{config.generation_date}T10:00:00+00:00"})

    header = ET.SubElement(cxml, "Header")
    from_node = ET.SubElement(header, "From")
    ET.SubElement(ET.SubElement(from_node, "Credential", attrib={"domain": "DUNS"}), "Identity").text = config.supplier_id

    to_node = ET.SubElement(header, "To")
    ET.SubElement(ET.SubElement(to_node, "Credential", attrib={"domain": "NetworkID"}), "Identity").text = config.buyer_name

    request = ET.SubElement(cxml, "Request")
    index = ET.SubElement(request, "Index")

    for item in items:
        contract_item = ET.SubElement(index, "ContractItem")
        ET.SubElement(contract_item, "SupplierID").text = config.supplier_id
        ET.SubElement(contract_item, "SupplierPartID").text = item.supplier_item_id

        item_detail = ET.SubElement(contract_item, "ItemDetail")
        unit_price = ET.SubElement(item_detail, "UnitPrice")
        money = ET.SubElement(unit_price, "Money", attrib={"currency": item.currency or "EUR"})
        money.text = f"{item.price:.2f}"

        desc = ET.SubElement(item_detail, "Description", attrib={"xml:lang": "en"})
        desc.text = item.title

        ET.SubElement(item_detail, "UnitOfMeasure").text = item.uom or "C62"
        ET.SubElement(item_detail, "Classification", attrib={"domain": "eCl@ss"}).text = item.eclass_code or "23-11-01-01"

    rough_string = ET.tostring(cxml, encoding="utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def generate_enterprise_csv(items: List[CatalogItem]) -> str:
    """Generates enterprise CSV catalog string."""
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Supplier_Item_ID", "Title", "Description", "Price", "Currency",
        "UOM", "MPN", "Manufacturer", "eCl@ss_7.1_Code", "Technical_Specs"
    ])

    for item in items:
        specs_str = "; ".join([f"{k}:{v}" for k, v in item.specs.items()])
        writer.writerow([
            item.supplier_item_id, item.title, item.description,
            f"{item.price:.2f}", item.currency, item.uom,
            item.mpn, item.manufacturer, item.eclass_code, specs_str
        ])

    return output.getvalue()
