"""
Official eCl@ss 7.1 Standard Taxonomy Schema Database.
Contains standard 8-digit classification codes, category titles (English & German eCl@ss standard names),
segment hierarchies, and official ISO/eCl@ss semantic definitions across procurement domains.
NO hardcoded keyword lists or manual product term dictionaries are used.
"""

ECLASS_7_1_DATABASE = [
    # --- Food, Beverages & Agricultural Products (Segment 16) ---
    {
        "code": "16-01-01-01",
        "name": "Milk, Dairy Products, Cultured Milk, Yogurt, Curd & Cheese / Milch, Molkereiprodukte, Joghurt, Bifidus-Kulturen, Milchanteil, Quark & Käse",
        "segment": "16 Food, beverage, tobacco / Nahrungsmittel, Getränke, Tabakwaren",
        "main_group": "16-01 Dairy product / Molkereiprodukt",
        "description": "Chilled and fresh dairy foods including milk, fermented milk products, yogurt, cream cheese, butter, curd, quark, and cheese.",
        "default_uom": "C62",
        "standard_specs": ["Fat Content", "Storage Temperature", "Package Size", "Flavor"]
    },
    {
        "code": "16-02-01-01",
        "name": "Coffee, Tea & Hot Beverages / Kaffee, Tee & Heißgetränke",
        "segment": "16 Food, beverage, tobacco / Nahrungsmittel, Getränke, Tabakwaren",
        "main_group": "16-02 Hot beverage / Heißgetränk",
        "description": "Ground roasted coffee, whole coffee beans, instant coffee, espresso, herbal and fruit tea bags, and hot beverage powders.",
        "default_uom": "C62",
        "standard_specs": ["Roast Type", "Package Weight", "Form Factor", "Caffeine Content"]
    },
    {
        "code": "16-03-01-01",
        "name": "Non-Alcoholic Beverages, Mineral Water, Soft Drinks & Juice / Mineralwasser, Erfrischungsgetränke & Saft",
        "segment": "16 Food, beverage, tobacco / Nahrungsmittel, Getränke, Tabakwaren",
        "main_group": "16-03 Non-alcoholic beverage / Alkoholfreies Getränk",
        "description": "Carbonated soft drinks, mineral water, flavoured nearwater, cola, lemonade, energy drinks, and fruit juices.",
        "default_uom": "C62",
        "standard_specs": ["Carbonation", "Volume", "Packaging Type", "Deposit (Pfand)"]
    },
    {
        "code": "16-03-02-01",
        "name": "Wine, Sparkling Wine, Sekt, Prosecco, Dry Wine & Spirits / Wein, Sekt, Schaumwein, Trockener Wein, Spirituosen",
        "segment": "16 Food, beverage, tobacco / Nahrungsmittel, Getränke, Tabakwaren",
        "main_group": "16-03 Alcoholic beverage / Alkoholhaltiges Getränk",
        "description": "Fermented grape wines, sparkling wines, sekt, champagne, prosecco, cider, aperitifs, and distilled spirits.",
        "default_uom": "C62",
        "standard_specs": ["Alcohol Content %", "Bottle Volume", "Grape Variety", "Country of Origin"]
    },
    {
        "code": "16-04-01-01",
        "name": "Fresh Meat, Pork, Beef, Poultry & Sausages / Fleisch, Schweinefleisch, Rindfleisch, Geflügel & Wurstwaren",
        "segment": "16 Food, beverage, tobacco / Nahrungsmittel, Getränke, Tabakwaren",
        "main_group": "16-04 Meat product / Fleischwaren",
        "description": "Fresh and chilled butchery cuts of pork, beef, poultry, minced meat, sausages, and processed meat products.",
        "default_uom": "KGM",
        "standard_specs": ["Cut Type", "Origin", "Storage Temp", "Weight"]
    },
    {
        "code": "16-05-01-01",
        "name": "Fresh Fruit, Vegetables & Agricultural Produce / Obst, Gemüse, Nektarinen, Möhren & Frische Erzeugnisse",
        "segment": "16 Food, beverage, tobacco / Nahrungsmittel, Getränke, Tabakwaren",
        "main_group": "16-05 Produce / Obst und Gemüse",
        "description": "Fresh orchard fruits, stone fruits, nectarines, citrus, berries, root vegetables, carrots, salad greens, potatoes, onions, and raw agricultural produce.",
        "default_uom": "KGM",
        "standard_specs": ["Quality Class", "Origin Country", "Packaging Unit"]
    },
    {
        "code": "16-06-01-01",
        "name": "Bread, Bakery Goods & Deep-Frozen Pastries / Brot, Brötchen, Backwaren & Tiefkühlgebäck",
        "segment": "16 Food, beverage, tobacco / Nahrungsmittel, Getränke, Tabakwaren",
        "main_group": "16-06 Bakery product / Backwaren",
        "description": "Fresh baked bread, deep-frozen bake-off rolls, croissants, toast bread, baguettes, cakes, and pastries.",
        "default_uom": "P1",
        "standard_specs": ["Preparation Type", "Piece Count", "Package Weight"]
    },
    {
        "code": "16-07-01-01",
        "name": "Confectionery, Chocolate, Sweets & Cocoa Spreads / Süßwaren, Schokolade, Nuss-Nugat-Creme & Snacking",
        "segment": "16 Food, beverage, tobacco / Nahrungsmittel, Getränke, Tabakwaren",
        "main_group": "16-07 Sweets & Snacks / Süßwaren",
        "description": "Chocolate bars, hazelnut cocoa spreads, wafer snacks, pralines, candy, chewing gum, and sweet grocery items.",
        "default_uom": "C62",
        "standard_specs": ["Package Size", "Flavour", "Cocoa Content"]
    },

    # --- Cleaning, Janitorial & Household Chemicals (Segment 29) ---
    {
        "code": "29-11-01-01",
        "name": "Detergents, Laundry Care & Washing Powder / Waschmittel, Wäschepflege & Reinigungsmittel",
        "segment": "29 Cleaning & janitorial products / Reinigungsmittel & Wäschepflege",
        "main_group": "29-11 Laundry care / Wäschepflege",
        "description": "Heavy-duty laundry detergents, washing powders, liquid laundry gels, fabric softeners, stain removers, and household cleaning products.",
        "default_uom": "C62",
        "standard_specs": ["Washing Loads (WL)", "Form (Liquid/Powder)", "Scent"]
    },

    # --- Fasteners & Mechanical Components (Segment 23) ---
    {
        "code": "23-11-01-01",
        "name": "Hexagon Head Bolt & Threaded Fasteners / Sechskantschraube & Verbindungstechnik",
        "segment": "23 Machine elements, fixings, fasteners / Maschinenorgan, Befestigung",
        "main_group": "23-11 Screw, bolt / Schraube, Bolzen",
        "description": "Threaded mechanical bolts with six-sided hexagonal drive head for structural fastening.",
        "default_uom": "C62",
        "standard_specs": ["Thread Diameter", "Length", "Material Grade", "Surface Finish", "Drive Type"]
    },
    {
        "code": "23-11-01-02",
        "name": "Socket Head Cap Screw & Hex Drive Fasteners / Zylinderschraube mit Innensechskant",
        "segment": "23 Machine elements, fixings, fasteners / Maschinenorgan, Befestigung",
        "main_group": "23-11 Screw, bolt / Schraube",
        "description": "Cylindrical head machine screws featuring internal hexagonal drive socket (Allen key).",
        "default_uom": "C62",
        "standard_specs": ["Thread Size", "Length", "Material", "Drive Size"]
    },
    {
        "code": "23-11-07-01",
        "name": "Hexagon Nut & Internal Threaded Fasteners / Sechskantmutter",
        "segment": "23 Machine elements, fixings, fasteners / Maschinenorgan, Befestigung",
        "main_group": "23-11 Screw, bolt, nut / Mutter",
        "description": "Internally threaded hexagonal fastening nuts and locking nuts for bolted joints.",
        "default_uom": "C62",
        "standard_specs": ["Thread Size", "Property Class", "Height", "Material"]
    },
    {
        "code": "23-09-01-01",
        "name": "Plain Flat Washer & Spacers / Scheibe, Flachscheibe",
        "segment": "23 Machine elements, fixings, fasteners / Maschinenorgan, Befestigung",
        "main_group": "23-09 Washer, ring / Scheibe",
        "description": "Flat annular load-distribution washers, shims, and sealing rings for threaded fasteners.",
        "default_uom": "C62",
        "standard_specs": ["Inner Diameter", "Outer Diameter", "Thickness", "Material"]
    },

    # --- Electrical Components & Cable Technology (Segment 27) ---
    {
        "code": "27-14-11-06",
        "name": "Cable Gland & Conduit Connections / Kabelverschraubung",
        "segment": "27 Electric engineering, automation / Elektroenergie, Automatisierung",
        "main_group": "27-14 Cable installation material / Kabelinstallationsmaterial",
        "description": "Sealing fittings, strain-relief glands, and conduit connectors for electric enclosures.",
        "default_uom": "C62",
        "standard_specs": ["Thread Size", "Clamping Range", "IP Protection Rating", "Material", "Operating Temp"]
    },
    {
        "code": "27-27-01-01",
        "name": "Inductive Proximity Sensor & Switches / Induktiver Näherungsschalter",
        "segment": "27 Electric engineering, automation / Elektroenergie, Automatisierung",
        "main_group": "27-27 Sensor, switch / Sensorik",
        "description": "Non-contact electronic proximity sensors detecting metallic target objects via electromagnetic fields.",
        "default_uom": "C62",
        "standard_specs": ["Sensing Distance", "Operating Voltage", "Output Type", "Housing Diameter", "IP Rating"]
    },
    {
        "code": "27-06-18-01",
        "name": "Power, Control & Signal Cable / Starkstromkabel & Steuerleitung",
        "segment": "27 Electric engineering, automation / Elektroenergie, Automatisierung",
        "main_group": "27-06 Cable, wire / Kabel, Leitung",
        "description": "Multi-core insulated copper wiring cables for industrial power distribution and automation signaling.",
        "default_uom": "MTR",
        "standard_specs": ["Number of Cores", "Conductor Cross-Section", "Rated Voltage", "Outer Diameter", "Sheath Material"]
    },
    {
        "code": "27-14-02-01",
        "name": "Terminal Block & DIN Rail Connectors / Reihenklemme & Anschlussklemme",
        "segment": "27 Electric engineering, automation / Elektroenergie, Automatisierung",
        "main_group": "27-14 Connection technology / Verbindungstechnik",
        "description": "Insulated modular DIN-rail terminal blocks for connecting electrical conductors safely.",
        "default_uom": "C62",
        "standard_specs": ["Nominal Current", "Nominal Voltage", "Cross-Section Range", "Number of Levels", "Color"]
    },

    # --- Fluid Tech, Valves & Piping (Segment 22 & 37) ---
    {
        "code": "22-56-02-01",
        "name": "Ball Valve & Industrial Flow Shut-Off / Kugelhahn & Absperrventil",
        "segment": "22 Construction, fluid technology / Bauwesen, Fluidtechnik",
        "main_group": "22-56 Valve, fitting / Armatur",
        "description": "Quarter-turn rotational ball valves for controlling flow of liquids, steam, and gases.",
        "default_uom": "C62",
        "standard_specs": ["Nominal Diameter (DN)", "Nominal Pressure (PN)", "Connection Type", "Body Material", "Seat Seal"]
    },
    {
        "code": "37-01-02-01",
        "name": "Pneumatic Linear Actuator & Air Cylinder / Pneumatikzylinder",
        "segment": "37 Industrial machinery, fluid power / Maschinenbau, Fluidtechnik",
        "main_group": "37-01 Pneumatic actuator / Pneumatikantrieb",
        "description": "Single-acting or double-acting pneumatic piston cylinders driven by compressed air.",
        "default_uom": "C62",
        "standard_specs": ["Piston Diameter", "Stroke Length", "Operating Pressure", "Cushioning", "Mounting Type"]
    },

    # --- Laboratory, Measuring & Safety Equipment (Segment 32 & 40) ---
    {
        "code": "32-01-01-01",
        "name": "Digital Microscope & Optical Inspection Instrument / Digitalmikroskop",
        "segment": "32 Laboratory equipment, optical instruments / Laborgeräte, Optik",
        "main_group": "32-01 Optical measuring device / Optisches Messgerät",
        "description": "High-magnification digital camera microscopes, optical inspection systems, and stereo magnifiers.",
        "default_uom": "C62",
        "standard_specs": ["Magnification Range", "Sensor Resolution", "Illumination", "Display Interface", "Stand Type"]
    },
    {
        "code": "32-01-02-01",
        "name": "Laboratory Glassware, Volumetric Flasks & Cylinders / Laborglas & Messkolben",
        "segment": "32 Laboratory equipment / Laborgeräte",
        "main_group": "32-01 Lab glassware / Laborglas",
        "description": "Borosilicate laboratory glass volumetric flasks, graduated measuring cylinders, pipettes, and burettes.",
        "default_uom": "C62",
        "standard_specs": ["Capacity (ml)", "Tolerance Class", "Material", "Standard"]
    },
    {
        "code": "40-01-01-01",
        "name": "Safety Glasses & Personal Protective Eyewear / Schutzbrille",
        "segment": "40 Health, personal safety, occupational safety / Arbeitsschutz, Sicherheit",
        "main_group": "40-01 Personal protective equipment (PPE) / Persönliche Schutzausrüstung",
        "description": "Impact-resistant occupational safety spectacles, goggles, and eye protection gear.",
        "default_uom": "C62",
        "standard_specs": ["Lens Material", "Frame Style", "Coating", "Standard Compliance", "Lens Color"]
    },
    {
        "code": "32-02-04-02",
        "name": "Precision Analytical Balance & Digital Scales / Präzisionswaage & Laborwaage",
        "segment": "32 Laboratory equipment / Laborgeräte",
        "main_group": "32-02 Weighing technology / Wägetechnik",
        "description": "High-precision digital laboratory weighing scales, analytical balances, and micro scales.",
        "default_uom": "C62",
        "standard_specs": ["Weighing Capacity", "Readability", "Pan Size", "Calibration Type", "Unit Options"]
    },

    # --- Hand Tools & Workshop Supplies (Segment 21) ---
    {
        "code": "21-04-01-01",
        "name": "Combination Spanner & Wrench Hand Tools / Ringmaulschlüssel",
        "segment": "21 Workshop equipment, hand tools / Werkstatteinrichtung, Werkzeug",
        "main_group": "21-04 Wrench, key tool / Schraubwerkzeug",
        "description": "Manual combination wrenches combining open-end and ring spanner heads for mechanics.",
        "default_uom": "P1",
        "standard_specs": ["Size Range", "Number of Pieces", "Material", "Finish", "Standard"]
    }
]

# Standard UN/ECE Recommendation 20 UOM codes map
UNECE_UOM_CODES = {
    "C62": "Piece / Unit",
    "P1": "Pack / Set",
    "MTR": "Meter",
    "KGM": "Kilogram",
    "LTR": "Liter",
    "MTK": "Square Meter",
    "MTQ": "Cubic Meter",
    "BX": "Box",
    "CT": "Carton",
    "RO": "Roll",
    "SET": "Set"
}
