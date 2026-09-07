"""
Unit tests for SpecStream AI Python backend services.
Tests Pydantic models, vector embedding taxonomy matcher, schema validator, and BMEcat exporter.
"""

import unittest
from pydantic import ValidationError
from app.models.catalog_schema import CatalogItem, BMEcatHeaderConfig
from app.services.schema_validator import validate_item
from app.services.vector_search import vector_engine
from app.services.exporter import generate_bmecat_xml, generate_cxml, generate_enterprise_csv


class TestSpecStreamBackend(unittest.TestCase):

    def setUp(self):
        self.valid_item = CatalogItem(
            supplier_item_id="TEST-BOLT-001",
            title="Hexagon Head Bolt DIN 933 M8x30 A2",
            description="Stainless steel A2-70 hexagon bolt for heavy machinery assembly.",
            price=0.45,
            currency="EUR",
            uom="C62",
            mpn="TEST-BOLT-001",
            manufacturer="Vortex Hardware",
            specs={"Thread": "M8", "Length": "30mm"},
            keywords=["hex bolt", "din 933", "m8"],
            eclass_code="23-11-01-01"
        )

    def test_pydantic_item_validation_valid(self):
        val = validate_item(self.valid_item)
        self.assertEqual(val.status, "VALID")
        self.assertGreaterEqual(val.score, 90)

    def test_pydantic_schema_rejection_on_invalid_input(self):
        # Verify Pydantic rejects invalid parameters during schema creation
        with self.assertRaises(ValidationError):
            CatalogItem(
                supplier_item_id="ID",
                title="A",  # min length 3 required
                description="Short",
                price=-5.0,  # price > 0 required
                currency="EUR"
            )

    def test_schema_validator_warning_flags(self):
        # Create item missing optional MPN and with non-standard UOM
        item = CatalogItem(
            supplier_item_id="SKU-WARN-01",
            title="Standard Steel Washer Form A",
            description="Zinc plated flat steel washer for structural load distribution.",
            price=0.15,
            currency="EUR",
            uom="PCS_CUSTOM",
            mpn="",
            eclass_code=""
        )
        val = validate_item(item)
        self.assertEqual(val.status, "WARNING")
        self.assertTrue(any(i.code == "NON_STANDARD_UOM" for i in val.issues))
        self.assertTrue(any(i.code == "UNCLASSIFIED_ECLASS" for i in val.issues))

    def test_vector_search_matching(self):
        results = vector_engine.search(
            title="Inductive Proximity Sensor M12 PNP",
            description="Non-contact electromagnetic detection switch",
            top_k=3
        )
        self.assertTrue(len(results) > 0)
        top_match = results[0]
        self.assertEqual(top_match.code, "27-27-01-01")
        self.assertGreaterEqual(top_match.confidence, 50.0)

    def test_bmecat_xml_generation(self):
        config = BMEcatHeaderConfig(
            catalog_id="TEST-CAT-001",
            supplier_name="Test Supplier Inc.",
            buyer_name="Enterprise Procurement Corp"
        )
        xml_str = generate_bmecat_xml([self.valid_item], config)
        self.assertIn('<BMECAT', xml_str)
        self.assertIn('version="1.2"', xml_str)
        self.assertIn('<SUPPLIER_AID>TEST-BOLT-001</SUPPLIER_AID>', xml_str)
        self.assertIn('<REFERENCE_FEATURE_GROUP_ID>23-11-01-01</REFERENCE_FEATURE_GROUP_ID>', xml_str)
        self.assertIn('<PRICE_AMOUNT>0.45</PRICE_AMOUNT>', xml_str)

    def test_cxml_generation(self):
        config = BMEcatHeaderConfig(catalog_id="TEST-CAT-001")
        cxml_str = generate_cxml([self.valid_item], config)
        self.assertIn('<cXML', cxml_str)
        self.assertIn('<SupplierPartID>TEST-BOLT-001</SupplierPartID>', cxml_str)

    def test_csv_generation(self):
        csv_str = generate_enterprise_csv([self.valid_item])
        self.assertIn("Supplier_Item_ID,Title,Description", csv_str)
        self.assertIn("TEST-BOLT-001", csv_str)


if __name__ == "__main__":
    unittest.main()
