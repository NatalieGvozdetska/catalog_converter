"""
Sample Unstructured Datasets for SpecStream AI.
Provides realistic sample documents (Industrial Hardware Spec Sheet, Electrical Sensors PDF, Lab Equipment CSV)
with extracted visual bounding box mock coordinates and structured item representations.
"""

SAMPLE_CATALOGS = {
    "industrial_fasteners": {
        "id": "industrial_fasteners",
        "title": "Vortex Fasteners & Hardware Spec Sheet 2026.pdf",
        "file_type": "pdf",
        "supplier_name": "Vortex Industrial Fasteners GmbH",
        "doc_preview": {
            "header": "VORTEX INDUSTRIAL FASTENERS - PRODUCT CATALOG 2026",
            "subtitle": "High Tensile Metric Fasteners DIN / ISO Standards",
            "raw_text": """
VORTEX INDUSTRIAL FASTENERS - SPECS & PRICING
Supplier ID: VTX-88421 | Date: 2026-05-15

Item #1: Hexagon Head Bolt ISO 4017 / DIN 933
Part No: VTX-HB-M8-30-A2
Specs: Size M8 x 30mm | Material Stainless Steel A2-70 | Thread Pitch 1.25mm | Full Thread
Price: $0.45 per PC | MOQ: 100 | Weight: 0.018 kg
Keywords: hex bolt, m8 screw, stainless bolt, ISO 4017

Item #2: Heavy Duty Hexagon Nut DIN 934
Part No: VTX-HN-M8-A4
Specs: Size M8 | Material Marine Grade Stainless Steel A4-80 | Pitch 1.25mm
Price: $0.22 per PC | MOQ: 100
Keywords: hex nut, m8 nut, din 934, stainless steel

Item #3: High Precision Plain Washer ISO 7089
Part No: VTX-PW-M8-ST
Specs: Inner Diameter 8.4mm | Outer Diameter 16mm | Thickness 1.6mm | Steel Zinc Plated
Price: $0.08 per PC | MOQ: 500
Keywords: flat washer, m8 washer, iso 7089

Item #4: Socket Head Cap Screw ISO 4762
Part No: VTX-SC-M10-40-88
Specs: Size M10 x 40mm | Steel Grade 8.8 Black Oxide | Allen Socket 8mm
Price: $0.85 per PC | MOQ: 50
Keywords: socket head screw, allen cap bolt, m10 bolt
            """
        },
        "bounding_boxes": [
            {"item_idx": 0, "x": 5, "y": 18, "w": 90, "h": 16, "label": "Item 1: VTX-HB-M8-30-A2"},
            {"item_idx": 1, "x": 5, "y": 36, "w": 90, "h": 16, "label": "Item 2: VTX-HN-M8-A4"},
            {"item_idx": 2, "x": 5, "y": 54, "w": 90, "h": 14, "label": "Item 3: VTX-PW-M8-ST"},
            {"item_idx": 3, "x": 5, "y": 70, "w": 90, "h": 16, "label": "Item 4: VTX-SC-M10-40-88"}
        ],
        "items": [
            {
                "supplier_item_id": "VTX-HB-M8-30-A2",
                "title": "Hexagon Head Bolt ISO 4017 / DIN 933 M8x30 A2",
                "description": "High tensile stainless steel A2-70 hexagon head bolt with full metric thread M8 x 30mm.",
                "price": 0.45,
                "currency": "EUR",
                "uom": "C62",
                "mpn": "VTX-HB-M8-30-A2",
                "manufacturer": "Vortex Industrial",
                "specs": {
                    "Thread Size": "M8",
                    "Length": "30 mm",
                    "Material": "Stainless Steel A2-70",
                    "Standard": "DIN 933 / ISO 4017",
                    "Thread Pitch": "1.25 mm"
                },
                "keywords": ["hex bolt", "m8 screw", "stainless bolt", "din 933"],
                "eclass_code": "23-11-01-01"
            },
            {
                "supplier_item_id": "VTX-HN-M8-A4",
                "title": "Heavy Duty Hexagon Nut DIN 934 M8 A4",
                "description": "Marine grade stainless steel A4-80 hexagon fastening nut for corrosive environments.",
                "price": 0.22,
                "currency": "EUR",
                "uom": "C62",
                "mpn": "VTX-HN-M8-A4",
                "manufacturer": "Vortex Industrial",
                "specs": {
                    "Thread Size": "M8",
                    "Material": "Stainless Steel A4-80",
                    "Standard": "DIN 934",
                    "Height": "6.5 mm"
                },
                "keywords": ["hex nut", "m8 nut", "din 934", "marine grade"],
                "eclass_code": "23-11-07-01"
            },
            {
                "supplier_item_id": "VTX-PW-M8-ST",
                "title": "High Precision Plain Washer ISO 7089 Form A M8",
                "description": "Zinc plated steel flat washer for uniform load distribution under bolt heads.",
                "price": 0.08,
                "currency": "EUR",
                "uom": "C62",
                "mpn": "VTX-PW-M8-ST",
                "manufacturer": "Vortex Industrial",
                "specs": {
                    "Inner Diameter": "8.4 mm",
                    "Outer Diameter": "16.0 mm",
                    "Thickness": "1.6 mm",
                    "Material": "Zinc Plated Steel"
                },
                "keywords": ["flat washer", "m8 washer", "iso 7089", "zinc washer"],
                "eclass_code": "23-09-01-01"
            },
            {
                "supplier_item_id": "VTX-SC-M10-40-88",
                "title": "Socket Head Cap Screw ISO 4762 M10x40 8.8",
                "description": "High strength grade 8.8 steel socket head cap screw with internal hex socket drive.",
                "price": 0.85,
                "currency": "EUR",
                "uom": "C62",
                "mpn": "VTX-SC-M10-40-88",
                "manufacturer": "Vortex Industrial",
                "specs": {
                    "Thread Size": "M10",
                    "Length": "40 mm",
                    "Material Grade": "Steel 8.8 Black Oxide",
                    "Drive Size": "8 mm Hex Socket"
                },
                "keywords": ["socket head screw", "allen bolt", "m10 bolt", "grade 8.8"],
                "eclass_code": "23-11-01-02"
            }
        ]
    },

    "electrical_automation": {
        "id": "electrical_automation",
        "title": "AeroTech Cable Glands & Sensor Data Sheet.png",
        "file_type": "image",
        "supplier_name": "AeroTech Components BV",
        "doc_preview": {
            "header": "AEROTECH INDUSTRIAL CABLE ACCESSORIES & SENSORS",
            "subtitle": "IP68 Enclosure Cable Glands & Inductive Switches",
            "raw_text": """
AEROTECH COMPONENTS - AUTOMATION ACCESSORIES
Doc Reference: ATC-2026-CAT-04

[Image Region 1: M20 Metallic Gland]
Model: ATC-CG-M20-BR
Description: Brass Nickel-Plated Cable Gland M20x1.5 with Neoprene O-ring seal.
Specs: Clamping 6-12mm | IP Rating IP68 (5 bar) | Temp -40°C to +100°C
Price: €3.40 / Piece | Pack: 10 pcs
Keywords: cable gland, m20 gland, ip68, brass gland

[Image Region 2: Inductive Proximity Sensor M12]
Model: ATC-SEN-IND-M12
Description: Shielded M12 Inductive Proximity Switch PNP Normally Open (NO).
Specs: Sensing Dist 4mm | Voltage 10-30V DC | Cable 2m PUR | LED Status
Price: €18.90 / Piece
Keywords: proximity sensor, inductive switch, pnp sensor, m12 switch

[Image Region 3: Flexible Control Cable PUR 4G1.5]
Model: ATC-CAB-PUR-4G15
Description: High flexibility oil-resistant PUR shielded control cable 4 cores x 1.5mm2.
Specs: 4G1.5mm2 | Rated Voltage 300/500V | Temp -30°C to +80°C | Color Grey RAL 7001
Price: €2.85 / Meter
Keywords: control cable, pur cable, 4g1.5 wire, flexible cable
            """
        },
        "bounding_boxes": [
            {"item_idx": 0, "x": 4, "y": 20, "w": 92, "h": 22, "label": "Region 1: Cable Gland M20"},
            {"item_idx": 1, "x": 4, "y": 45, "w": 92, "h": 24, "label": "Region 2: Sensor M12 PNP"},
            {"item_idx": 2, "x": 4, "y": 72, "w": 92, "h": 22, "label": "Region 3: Control Cable 4G1.5"}
        ],
        "items": [
            {
                "supplier_item_id": "ATC-CG-M20-BR",
                "title": "Brass Nickel-Plated Cable Gland M20x1.5 IP68",
                "description": "Industrial M20 cable gland connection with strain relief and IP68 waterproof neoprene O-ring.",
                "price": 3.40,
                "currency": "EUR",
                "uom": "C62",
                "mpn": "ATC-CG-M20-BR",
                "manufacturer": "AeroTech BV",
                "specs": {
                    "Thread Size": "M20 x 1.5",
                    "Clamping Range": "6 - 12 mm",
                    "IP Protection": "IP68",
                    "Material": "Brass Nickel-Plated"
                },
                "keywords": ["cable gland", "m20 gland", "ip68", "strain relief"],
                "eclass_code": "27-14-11-06"
            },
            {
                "supplier_item_id": "ATC-SEN-IND-M12",
                "title": "Shielded Inductive Proximity Sensor M12 PNP NO",
                "description": "Non-contact inductive switch detecting metallic objects up to 4mm sensing range.",
                "price": 18.90,
                "currency": "EUR",
                "uom": "C62",
                "mpn": "ATC-SEN-IND-M12",
                "manufacturer": "AeroTech BV",
                "specs": {
                    "Sensing Distance": "4 mm",
                    "Operating Voltage": "10-30V DC",
                    "Output Function": "PNP Normally Open (NO)",
                    "Housing Size": "M12 Threaded"
                },
                "keywords": ["proximity sensor", "inductive switch", "pnp sensor", "m12 switch"],
                "eclass_code": "27-27-01-01"
            },
            {
                "supplier_item_id": "ATC-CAB-PUR-4G15",
                "title": "Flexible Shielded Control Cable PUR 4G1.5 mm2",
                "description": "Oil-resistant, high flex poly-urethane industrial power and signaling cable.",
                "price": 2.85,
                "currency": "EUR",
                "uom": "MTR",
                "mpn": "ATC-CAB-PUR-4G15",
                "manufacturer": "AeroTech BV",
                "specs": {
                    "Number of Cores": "4",
                    "Conductor Cross-Section": "1.5 mm2",
                    "Rated Voltage": "300/500V",
                    "Sheath Material": "PUR Polyurethane"
                },
                "keywords": ["control cable", "pur cable", "4g1.5 wire", "flexible cable"],
                "eclass_code": "27-06-18-01"
            }
        ]
    },

    "lab_equipment": {
        "id": "lab_equipment",
        "title": "BioTech Laboratory Precision Supplies.csv",
        "file_type": "csv",
        "supplier_name": "BioTech Lab Solutions Inc.",
        "doc_preview": {
            "header": "RAW SUPPLIER EXPORT - BIOTECH LAB SOLUTIONS",
            "subtitle": "Unstructured CSV catalog table import",
            "raw_text": """
SKU,Item_Name,Raw_Desc,Unit_Price,Currency,Package_Unit,Manufacturer
BT-MIC-4K,4K Digital Stereo Microscope,High resolution 4K inspection camera with 200x optical zoom LED ring light,1250.00,USD,EA,BioTech Scientific
BT-SCL-500,Precision Micro Scale 500g,Digital analytical laboratory balance with 0.001g readability and tare calibration,420.00,USD,EA,BioTech Scientific
BT-GGL-UV,Industrial Safety Spectacles UV400,Impact resistant anti-fog protective eyewear EN 166 compliant,12.50,USD,PK,BioTech Safety
            """
        },
        "bounding_boxes": [],
        "items": [
            {
                "supplier_item_id": "BT-MIC-4K",
                "title": "4K Digital Stereo Inspection Microscope 200x Zoom",
                "description": "High resolution 4K optical inspection microscope with integrated adjustable LED ring light.",
                "price": 1250.00,
                "currency": "USD",
                "uom": "C62",
                "mpn": "BT-MIC-4K",
                "manufacturer": "BioTech Scientific",
                "specs": {
                    "Magnification": "Up to 200x",
                    "Camera Resolution": "4K Ultra HD",
                    "Illumination": "LED Ring Light",
                    "Display Interface": "HDMI / USB-C"
                },
                "keywords": ["microscope", "digital microscope", "optical inspection", "4k camera"],
                "eclass_code": "32-01-01-01"
            },
            {
                "supplier_item_id": "BT-SCL-500",
                "title": "Precision Analytical Balance Scale 500g / 0.001g",
                "description": "High accuracy digital laboratory weighing balance with motorized internal calibration.",
                "price": 420.00,
                "currency": "USD",
                "uom": "C62",
                "mpn": "BT-SCL-500",
                "manufacturer": "BioTech Scientific",
                "specs": {
                    "Capacity": "500 g",
                    "Readability": "0.001 g (1 mg)",
                    "Pan Diameter": "90 mm",
                    "Calibration": "Internal Automatic"
                },
                "keywords": ["lab scale", "digital balance", "analytical scale", "precision scale"],
                "eclass_code": "32-02-04-02"
            },
            {
                "supplier_item_id": "BT-GGL-UV",
                "title": "Anti-Fog UV400 Safety Eyewear Spectacles",
                "description": "Impact-resistant polycarbonate protective safety glasses complying with EN 166 safety standard.",
                "price": 12.50,
                "currency": "USD",
                "uom": "P1",
                "mpn": "BT-GGL-UV",
                "manufacturer": "BioTech Safety",
                "specs": {
                    "Lens Coating": "Anti-Fog / Scratch Resistant",
                    "UV Protection": "UV400 100%",
                    "Standard": "EN 166 / ANSI Z87.1",
                    "Lens Material": "Polycarbonate"
                },
                "keywords": ["safety glasses", "protective goggles", "ppe", "eye protection"],
                "eclass_code": "40-01-01-01"
            }
        ]
    }
}
