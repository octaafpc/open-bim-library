#!/usr/bin/env python3
"""Writes the object catalogues of the library: `objects/<trade>.json`.

    python3 tools/generate_objects.py

Each file is a list of object types as `bim-library` reads them (`bim_library::object::ObjectType`).
The objects are generic: usual Dutch sizes and kinds, of no manufacturer. A kind has one object
at LOD 200 (about the right size, to reserve its place) and its usual sizes at LOD 300.

Sizes are width x depth x height in millimetres here and metres in the files; `base` is the
height of the underside above the floor.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "objects"
catalogue = {}


def slug(text):
    out = "".join(c if c.isalnum() else "-" for c in text.lower())
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def add(trade, group, key, names, size, base=0, lod=300, suffix="", **more):
    """One object: `names` nl, en, de, fr; `suffix` a size told after the name."""
    nl, en, de, fr = names
    tail = f" {suffix}" if suffix else ""
    entry = {
        "id": f"nl.{group}.{slug(key + '-' + suffix) if suffix else slug(key)}",
        "group": group,
        "names": {"nl": nl + tail, "en": en + tail, "de": de + tail, "fr": fr + tail},
        "size": [round(v / 1000, 4) for v in size],
        "lod": str(lod),
    }
    if base:
        entry["base"] = round(base / 1000, 4)
    for key_, value in more.items():
        if value:
            entry[key_] = value
    catalogue.setdefault(trade, []).append(entry)


def kind(trade, group, key, names, generic, sizes=(), base=0, label=lambda w, d, h: f"{w} × {h}", **more):
    """A kind of object: a generic one at LOD 200 and its usual sizes at LOD 300. A kind that
    comes in one size alone (a socket, a detector) is that one object, at LOD 300."""
    labelled = [(size, label(*size)) for size in sizes]
    if labelled and all(not text for _, text in labelled):
        add(trade, group, key, names, labelled[0][0], base, 300, **more)
        return
    add(trade, group, key, names, generic, base, 200, **more)
    for size, text in labelled:
        add(trade, group, key, names, size, base, 300, text, **more)


# --- architecture -------------------------------------------------------------------------
A = "architecture"
inner = [(w, 40, h) for h in (2015, 2115, 2315) for w in (730, 780, 830, 880, 930, 980)]
kind(A, "door", "inner-door", ("binnendeur", "inner door", "Innentür", "porte intérieure"), (880, 40, 2315), inner)
kind(A, "door", "outer-door", ("buitendeur", "outer door", "Außentür", "porte extérieure"), (930, 54, 2315), [(w, 54, h) for h in (2115, 2315) for w in (880, 930, 980, 1030)], code="31")
kind(A, "door", "double-door", ("dubbele deur", "double door", "Doppeltür", "porte double"), (1760, 40, 2315), [(w, 40, 2315) for w in (1460, 1660, 1760, 1860)])
kind(A, "door", "sliding-door", ("schuifdeur", "sliding door", "Schiebetür", "porte coulissante"), (930, 40, 2315), [(w, 40, 2315) for w in (830, 930, 1030)], predefined="DOOR")
kind(A, "door", "garage-door", ("garagedeur", "garage door", "Garagentor", "porte de garage"), (2500, 45, 2125), [(w, 45, h) for w, h in ((2375, 2125), (2500, 2125), (2500, 2250), (3000, 2125), (5000, 2125))], predefined="DOOR", code="31")
windows = [(w, 114, h) for w in (600, 900, 1200, 1500, 1800, 2400) for h in (600, 1200, 1500, 2300)]
kind(A, "window", "fixed-window", ("vast raam", "fixed window", "Festverglasung", "fenêtre fixe"), (1200, 114, 1500), windows, base=900)
kind(A, "window", "tilt-turn-window", ("draaikiepraam", "tilt and turn window", "Dreh-Kipp-Fenster", "fenêtre oscillo-battante"), (900, 114, 1500), [(w, 114, h) for w in (600, 800, 900, 1000, 1200) for h in (900, 1200, 1500)], base=900)
kind(A, "window", "roof-window", ("dakraam", "roof window", "Dachfenster", "fenêtre de toit"), (780, 150, 1180), [(w, 150, h) for w, h in ((550, 780), (550, 980), (660, 1180), (780, 980), (780, 1180), (780, 1400), (940, 1400), (1140, 1180), (1340, 980))], predefined="SKYLIGHT", code="37")
kind(A, "window", "skylight-dome", ("lichtkoepel", "rooflight dome", "Lichtkuppel", "lanterneau"), (1000, 1000, 400), [(s, s, 400) for s in (600, 800, 1000, 1200, 1500)], predefined="SKYLIGHT", code="37", label=lambda w, d, h: f"{w} × {d}")
stairs = lambda w, d, h: f"{w} × {d}, {h}"
kind(A, "stair", "straight-stair", ("rechte steektrap", "straight stair", "gerade Treppe", "escalier droit"), (900, 3600, 2800), [(w, 3600, h) for w in (800, 900, 1000, 1200) for h in (2600, 2800, 3000)], label=stairs)
kind(A, "stair", "quarter-turn-stair", ("kwartslagtrap", "quarter-turn stair", "viertelgewendelte Treppe", "escalier quart tournant"), (1800, 2700, 2800), [(1800, 2700, h) for h in (2600, 2800, 3000)], predefined="QUARTER_TURN_STAIR", label=stairs)
kind(A, "stair", "half-turn-stair", ("bordestrap", "half-turn stair with landing", "Podesttreppe", "escalier à palier"), (2100, 3000, 2800), [(w, 3000, h) for w in (1900, 2100, 2500) for h in (2800, 3000, 3400)], predefined="HALF_TURN_STAIR", label=stairs)
kind(A, "stair", "spiral-stair", ("spiltrap", "spiral stair", "Spindeltreppe", "escalier en colimaçon"), (1600, 1600, 2800), [(d, d, 2800) for d in (1400, 1600, 1800, 2000)], predefined="SPIRAL_STAIR", label=lambda w, d, h: f"Ø{w}")
kind(A, "stair", "loft-ladder", ("vlizotrap", "loft ladder", "Bodentreppe", "escalier escamotable"), (600, 1200, 2800), [(w, d, 2800) for w, d in ((600, 1200), (700, 1200), (700, 1400))], predefined="LADDER", label=lambda w, d, h: f"{w} × {d}")
rail = lambda w, d, h: f"{h}"
kind(A, "railing", "balustrade-bars", ("spijlenhekwerk", "balustrade with bars", "Stabgeländer", "garde-corps à barreaux"), (2000, 50, 1000), [(2000, 50, h) for h in (1000, 1100, 1200)], label=rail)
kind(A, "railing", "balustrade-glass", ("glazen balustrade", "glass balustrade", "Glasgeländer", "garde-corps vitré"), (2000, 30, 1000), [(2000, 30, h) for h in (1000, 1100, 1200)], label=rail, material="glass")
kind(A, "railing", "handrail", ("trapleuning", "handrail", "Handlauf", "main courante"), (3000, 60, 50), [(3000, 60, 50)], base=900, predefined="HANDRAIL", label=lambda w, d, h: "Ø42")

# --- interior -----------------------------------------------------------------------------
I = "interior"
box = lambda w, d, h: f"{w} × {d}"
kind(I, "sanitary", "wall-hung-toilet", ("wandcloset", "wall-hung toilet", "Wand-WC", "WC suspendu"), (360, 540, 350), [(360, 540, 350), (360, 480, 350), (360, 700, 350)], base=110, predefined="TOILETPAN", label=box)
kind(I, "sanitary", "floor-standing-toilet", ("staand closet", "floor-standing toilet", "Stand-WC", "WC à poser"), (360, 670, 800), [(360, 670, 800)], predefined="TOILETPAN", label=box)
kind(I, "sanitary", "wash-basin", ("wastafel", "wash basin", "Waschtisch", "lavabo"), (600, 450, 180), [(w, d, 180) for w, d in ((500, 400), (600, 450), (800, 480), (1000, 480), (1200, 480))], base=720, predefined="WASHHANDBASIN", label=box)
kind(I, "sanitary", "hand-rinse-basin", ("fontein", "hand rinse basin", "Handwaschbecken", "lave-mains"), (360, 250, 150), [(360, 250, 150), (400, 220, 150), (450, 300, 150)], base=750, predefined="WASHHANDBASIN", label=box)
kind(I, "sanitary", "shower-tray", ("douchebak", "shower tray", "Duschwanne", "receveur de douche"), (900, 900, 40), [(w, d, 40) for w, d in ((800, 800), (900, 900), (1000, 1000), (1000, 800), (1200, 900), (1400, 900))], predefined="SHOWER", label=box)
kind(I, "sanitary", "bath", ("ligbad", "bath", "Badewanne", "baignoire"), (1700, 750, 580), [(w, d, 580) for w, d in ((1600, 700), (1700, 750), (1800, 800), (1900, 900))], predefined="BATH", label=box)
kind(I, "sanitary", "urinal", ("urinoir", "urinal", "Urinal", "urinoir"), (350, 350, 600), [(350, 350, 600)], base=500, predefined="URINAL", label=box)
kind(I, "sanitary", "utility-sink", ("uitstortgootsteen", "utility sink", "Ausgussbecken", "vidoir"), (500, 350, 220), [(500, 350, 220)], base=600, predefined="SINK", label=box)
units = lambda w, d, h: f"{w}"
kind(I, "kitchen", "base-unit", ("onderkast", "base unit", "Unterschrank", "meuble bas"), (600, 600, 880), [(w, 600, 880) for w in (300, 400, 450, 500, 600, 800, 900, 1000, 1200)], label=units)
kind(I, "kitchen", "wall-unit", ("bovenkast", "wall unit", "Oberschrank", "meuble haut"), (600, 350, 720), [(w, 350, 720) for w in (300, 400, 450, 500, 600, 800, 900, 1000)], base=1450, label=units)
kind(I, "kitchen", "tall-unit", ("hoge kast", "tall unit", "Hochschrank", "colonne"), (600, 600, 2100), [(w, 600, 2100) for w in (450, 600)], label=units)
kind(I, "kitchen", "worktop", ("aanrechtblad", "worktop", "Arbeitsplatte", "plan de travail"), (2400, 620, 40), [(w, 620, 40) for w in (1800, 2400, 3000, 3600)], base=880, label=units)
kind(I, "kitchen", "kitchen-sink", ("spoelbak", "kitchen sink", "Spüle", "évier"), (500, 400, 200), [(w, 400, 200) for w in (400, 500, 800)], base=700, label=units)
kind(I, "kitchen", "kitchen-island", ("kookeiland", "kitchen island", "Kochinsel", "îlot de cuisine"), (2400, 1000, 900), [(w, d, 900) for w, d in ((1800, 900), (2400, 1000), (3000, 1200))], label=box)
kind(I, "furniture", "bed", ("bed", "bed", "Bett", "lit"), (1600, 2000, 500), [(w, d, 500) for w, d in ((900, 2000), (900, 2100), (1400, 2000), (1600, 2000), (1800, 2000), (1800, 2100))], label=box)
kind(I, "furniture", "dining-table", ("eettafel", "dining table", "Esstisch", "table à manger"), (1800, 900, 750), [(w, d, 750) for w, d in ((1200, 800), (1600, 900), (1800, 900), (2000, 1000), (2400, 1000))], label=box)
kind(I, "furniture", "round-table", ("ronde tafel", "round table", "runder Tisch", "table ronde"), (1200, 1200, 750), [(s, s, 750) for s in (900, 1100, 1200, 1400)], label=lambda w, d, h: f"Ø{w}")
kind(I, "furniture", "desk", ("bureau", "desk", "Schreibtisch", "bureau"), (1600, 800, 740), [(w, 800, 740) for w in (1200, 1400, 1600, 1800)], label=box)
kind(I, "furniture", "chair", ("stoel", "chair", "Stuhl", "chaise"), (450, 520, 820), [(450, 520, 820)], label=box)
kind(I, "furniture", "office-chair", ("bureaustoel", "office chair", "Bürostuhl", "siège de bureau"), (650, 650, 1000), [(650, 650, 1000)], label=box)
kind(I, "furniture", "sofa", ("bank", "sofa", "Sofa", "canapé"), (2100, 950, 800), [(w, 950, 800) for w in (1600, 2100, 2500)], label=units)
kind(I, "furniture", "armchair", ("fauteuil", "armchair", "Sessel", "fauteuil"), (850, 850, 800), [(850, 850, 800)], label=box)
kind(I, "furniture", "wardrobe", ("kledingkast", "wardrobe", "Kleiderschrank", "armoire"), (1500, 600, 2000), [(w, 600, h) for w, h in ((1000, 2000), (1500, 2000), (2000, 2000), (2000, 2360), (2500, 2360))], label=lambda w, d, h: f"{w} × {h}")
kind(I, "furniture", "bookcase", ("boekenkast", "bookcase", "Regal", "bibliothèque"), (800, 300, 2000), [(w, 300, 2000) for w in (400, 800, 1000)], label=units)
kind(I, "furniture", "sideboard", ("dressoir", "sideboard", "Sideboard", "buffet"), (1800, 450, 800), [(w, 450, 800) for w in (1200, 1800, 2200)], label=units)
kind(I, "furniture", "meeting-table", ("vergadertafel", "meeting table", "Besprechungstisch", "table de réunion"), (2400, 1200, 740), [(w, 1200, 740) for w in (2000, 2400, 3200, 4000)], label=box)
E_APP = "IfcElectricAppliance"
kind(I, "appliance", "washing-machine", ("wasmachine", "washing machine", "Waschmaschine", "lave-linge"), (600, 600, 850), [(600, 600, 850)], predefined="WASHINGMACHINE", label=box)
kind(I, "appliance", "tumble-dryer", ("wasdroger", "tumble dryer", "Wäschetrockner", "sèche-linge"), (600, 600, 850), [(600, 600, 850)], predefined="TUMBLEDRYER", label=box)
kind(I, "appliance", "dishwasher", ("vaatwasser", "dishwasher", "Geschirrspüler", "lave-vaisselle"), (600, 570, 820), [(450, 570, 820), (600, 570, 820)], predefined="DISHWASHER", label=box)
kind(I, "appliance", "refrigerator", ("koelkast", "refrigerator", "Kühlschrank", "réfrigérateur"), (600, 650, 1850), [(600, 550, 880), (600, 650, 1850), (910, 700, 1780)], predefined="REFRIGERATOR", label=lambda w, d, h: f"{w} × {h}")
kind(I, "appliance", "oven", ("oven", "oven", "Backofen", "four"), (600, 550, 600), [(600, 550, 450), (600, 550, 600)], base=880, predefined="ELECTRICCOOKER", label=lambda w, d, h: f"{w} × {h}")
kind(I, "appliance", "hob", ("kookplaat", "hob", "Kochfeld", "plaque de cuisson"), (600, 520, 50), [(w, 520, 50) for w in (600, 800, 900)], base=880, predefined="ELECTRICCOOKER", label=units)
kind(I, "appliance", "cooker-hood", ("afzuigkap", "cooker hood", "Dunstabzugshaube", "hotte"), (600, 500, 400), [(w, 500, 400) for w in (600, 900)], base=1550, predefined="KITCHENMACHINE", label=units)

# --- heating and cooling ------------------------------------------------------------------
H = "heating"
for depth, kind_nl in ((61, "11"), (100, "22"), (155, "33")):
    sizes = [(l, depth, h) for h in (300, 500, 600, 900) for l in (400, 600, 800, 1000, 1200, 1400, 1600, 2000)]
    kind(H, "heat-emitter", f"panel-radiator-type-{kind_nl}", (f"paneelradiator type {kind_nl}", f"panel radiator type {kind_nl}", f"Flachheizkörper Typ {kind_nl}", f"radiateur panneau type {kind_nl}"), (1000, depth, 600), sizes, base=150, label=lambda w, d, h: f"{h} × {w}")
kind(H, "heat-emitter", "column-radiator", ("ledenradiator", "column radiator", "Gliederheizkörper", "radiateur à colonnes"), (1000, 140, 600), [(l, 140, h) for h in (600, 900) for l in (600, 1000, 1400)], base=150, label=lambda w, d, h: f"{h} × {w}")
kind(H, "heat-emitter", "towel-radiator", ("handdoekradiator", "towel radiator", "Handtuchheizkörper", "sèche-serviettes"), (600, 40, 1200), [(w, 40, h) for w in (500, 600) for h in (800, 1200, 1800)], base=600, label=lambda w, d, h: f"{w} × {h}")
kind(H, "heat-emitter", "convector", ("convector", "convector", "Konvektor", "convecteur"), (1200, 140, 200), [(l, 140, 200) for l in (800, 1200, 1600, 2000)], predefined="CONVECTOR", label=units)
kind(H, "heat-emitter", "trench-convector", ("convectorput", "trench convector", "Unterflurkonvektor", "convecteur de sol"), (2000, 260, 110), [(l, 260, 110) for l in (1200, 2000, 3000)], base=-110, predefined="CONVECTOR", label=units)
kind(H, "heat-emitter", "floor-heating-manifold", ("vloerverwarmingsverdeler", "floor heating manifold", "Fußbodenheizungsverteiler", "collecteur de plancher chauffant"), (600, 120, 500), [(w, 120, 500) for w in (400, 600, 800, 1000)], base=300, **{"class": "IfcDistributionChamberElement"}, predefined="NOTDEFINED", label=units)
kind(H, "heat-emitter", "radiant-panel", ("stralingspaneel", "radiant panel", "Deckenstrahlplatte", "panneau rayonnant"), (1200, 600, 50), [(1200, 600, 50), (3000, 600, 50)], base=2550, label=box)
kind(H, "heat-source", "gas-boiler", ("cv-ketel", "gas boiler", "Gas-Brennwertgerät", "chaudière gaz"), (440, 340, 700), [(440, 340, 700), (520, 400, 800)], base=1200, predefined="WATER", label=box)
kind(H, "heat-source", "heat-pump-outdoor-unit", ("warmtepomp buitenunit", "heat pump outdoor unit", "Wärmepumpe Außeneinheit", "pompe à chaleur unité extérieure"), (1100, 450, 900), [(900, 400, 700), (1100, 450, 900), (1300, 500, 1400)], **{"class": "IfcHeatPump"}, predefined="NOTDEFINED", label=lambda w, d, h: f"{w} × {h}")
kind(H, "heat-source", "heat-pump-indoor-unit", ("warmtepomp binnenunit", "heat pump indoor unit", "Wärmepumpe Inneneinheit", "pompe à chaleur unité intérieure"), (600, 600, 1800), [(600, 600, 1800), (600, 700, 2000)], **{"class": "IfcHeatPump"}, predefined="NOTDEFINED", label=lambda w, d, h: f"{w} × {h}")
kind(H, "heat-source", "ground-source-heat-pump", ("bodemwarmtepomp", "ground source heat pump", "Sole-Wasser-Wärmepumpe", "pompe à chaleur géothermique"), (600, 650, 1500), [(600, 650, 1500)], **{"class": "IfcHeatPump"}, predefined="NOTDEFINED", label=lambda w, d, h: f"{w} × {h}")
kind(H, "heat-source", "hot-water-cylinder", ("boilervat", "hot water cylinder", "Warmwasserspeicher", "ballon d'eau chaude"), (600, 600, 1500), [(d, d, h) for d, h in ((500, 1100), (600, 1300), (600, 1700), (700, 1800))], **{"class": "IfcTank"}, predefined="STORAGE", label=lambda w, d, h: f"Ø{w} × {h}")
kind(H, "heat-source", "buffer-tank", ("buffervat", "buffer tank", "Pufferspeicher", "ballon tampon"), (600, 600, 1500), [(d, d, h) for d, h in ((450, 900), (600, 1500), (800, 1900))], **{"class": "IfcTank"}, predefined="STORAGE", label=lambda w, d, h: f"Ø{w} × {h}")
kind(H, "heat-source", "expansion-vessel", ("expansievat", "expansion vessel", "Ausdehnungsgefäß", "vase d'expansion"), (300, 300, 350), [(d, d, h) for d, h in ((270, 300), (350, 400), (450, 500))], base=1200, **{"class": "IfcTank"}, predefined="EXPANSION", label=lambda w, d, h: f"Ø{w}")
kind(H, "heat-source", "split-air-conditioner-indoor", ("airco binnenunit", "air conditioner indoor unit", "Klimagerät Inneneinheit", "climatiseur unité intérieure"), (800, 200, 300), [(800, 200, 300), (1000, 230, 320)], base=2200, **{"class": "IfcUnitaryEquipment"}, predefined="SPLITSYSTEM", label=units)
kind(H, "heat-source", "split-air-conditioner-outdoor", ("airco buitenunit", "air conditioner outdoor unit", "Klimagerät Außeneinheit", "climatiseur unité extérieure"), (800, 300, 550), [(800, 300, 550), (950, 350, 800)], **{"class": "IfcUnitaryEquipment"}, predefined="SPLITSYSTEM", label=units)
kind(H, "heat-source", "fan-coil-unit", ("ventilatorconvector", "fan coil unit", "Gebläsekonvektor", "ventilo-convecteur"), (1000, 220, 500), [(w, 220, 500) for w in (800, 1000, 1200)], **{"class": "IfcUnitaryEquipment"}, predefined="NOTDEFINED", label=units)
kind(H, "heat-source", "district-heating-unit", ("afleverset stadsverwarming", "district heating unit", "Fernwärme-Übergabestation", "sous-station de chauffage urbain"), (500, 250, 700), [(500, 250, 700)], base=800, **{"class": "IfcHeatExchanger"}, predefined="PLATE", label=box)

# --- ventilation --------------------------------------------------------------------------
V = "ventilation"
kind(V, "ventilation-unit", "heat-recovery-unit", ("wtw-unit", "heat recovery unit", "Lüftungsgerät mit Wärmerückgewinnung", "VMC double flux"), (750, 560, 850), [(680, 530, 760), (750, 560, 850), (850, 600, 1000)], base=900, predefined="AIRHANDLER", label=lambda w, d, h: f"{w} × {h}")
kind(V, "ventilation-unit", "extract-fan-unit", ("mechanische ventilatiebox", "extract fan unit", "Abluftgerät", "VMC simple flux"), (350, 350, 300), [(350, 350, 300), (500, 450, 350)], base=2000, **{"class": "IfcFan"}, predefined="CENTRIFUGALBACKWARDINCLINEDCURVED", label=box)
kind(V, "ventilation-unit", "roof-fan", ("dakventilator", "roof fan", "Dachventilator", "tourelle d'extraction"), (600, 600, 450), [(s, s, 450) for s in (400, 600, 800)], **{"class": "IfcFan"}, predefined="CENTRIFUGALBACKWARDINCLINEDCURVED", label=box)
kind(V, "ventilation-unit", "duct-fan", ("buisventilator", "duct fan", "Rohrventilator", "ventilateur de gaine"), (300, 300, 250), [(d + 100, d + 100, 250) for d in (125, 160, 200, 250, 315)], base=2600, **{"class": "IfcFan"}, predefined="TUBEAXIAL", label=lambda w, d, h: f"Ø{w - 100}")
kind(V, "ventilation-unit", "air-handling-unit", ("luchtbehandelingskast", "air handling unit", "RLT-Gerät", "centrale de traitement d'air"), (3000, 1500, 1500), [(w, d, h) for w, d, h in ((2000, 1000, 1000), (3000, 1500, 1500), (4500, 2000, 2000), (6000, 2400, 2400))], predefined="AIRHANDLER", label=lambda w, d, h: f"{w} × {d} × {h}")
kind(V, "ventilation-unit", "decentral-ventilation-unit", ("decentrale wtw", "decentralised ventilation unit", "dezentrales Lüftungsgerät", "ventilation décentralisée"), (300, 300, 300), [(300, 300, 300)], base=2000, predefined="AIRHANDLER", label=box)
round_ = lambda w, d, h: f"Ø{w}"
kind(V, "air-terminal", "extract-valve", ("afzuigventiel", "extract valve", "Abluftventil", "bouche d'extraction"), (150, 150, 50), [(d + 30, d + 30, 50) for d in (100, 125, 160, 200)], base=2550, predefined="DIFFUSER", label=lambda w, d, h: f"Ø{w - 30}")
kind(V, "air-terminal", "supply-valve", ("toevoerventiel", "supply valve", "Zuluftventil", "bouche de soufflage"), (150, 150, 50), [(d + 30, d + 30, 50) for d in (100, 125, 160, 200)], base=2550, predefined="DIFFUSER", label=lambda w, d, h: f"Ø{w - 30}")
kind(V, "air-terminal", "ceiling-diffuser", ("plafondrooster", "ceiling diffuser", "Deckenluftdurchlass", "diffuseur plafonnier"), (595, 595, 60), [(s, s, 60) for s in (295, 395, 495, 595)], base=2540, predefined="DIFFUSER", label=box)
kind(V, "air-terminal", "wall-grille", ("wandrooster", "wall grille", "Wandgitter", "grille murale"), (300, 40, 150), [(w, 40, h) for w, h in ((200, 100), (300, 100), (300, 150), (400, 150), (500, 200), (600, 300))], base=2300, predefined="GRILLE", label=lambda w, d, h: f"{w} × {h}")
kind(V, "air-terminal", "linear-diffuser", ("lijnrooster", "linear diffuser", "Schlitzdurchlass", "diffuseur linéaire"), (1000, 100, 60), [(l, 100, 60) for l in (600, 1000, 1200, 1500, 2000)], base=2540, predefined="LOUVRE", label=units)
kind(V, "air-terminal", "facade-louvre", ("gevelrooster", "facade louvre", "Wetterschutzgitter", "grille de façade"), (400, 60, 400), [(s, 60, s) for s in (200, 300, 400, 600, 800, 1000)], base=2400, predefined="LOUVRE", label=lambda w, d, h: f"{w} × {h}")
kind(V, "air-terminal", "window-vent", ("ventilatierooster in kozijn", "window vent", "Fensterlüfter", "entrée d'air de fenêtre"), (1000, 100, 60), [(l, 100, 60) for l in (600, 900, 1200, 1500, 1800)], base=2300, predefined="LOUVRE", label=units)
kind(V, "air-terminal", "door-grille", ("deurrooster", "door grille", "Türgitter", "grille de porte"), (450, 40, 90), [(450, 40, 90), (500, 40, 250)], base=200, predefined="GRILLE", label=lambda w, d, h: f"{w} × {h}")
kind(V, "air-terminal", "roof-terminal", ("dakdoorvoer", "roof terminal", "Dachdurchführung", "sortie de toiture"), (300, 300, 600), [(d + 150, d + 150, 600) for d in (125, 160, 200, 250)], predefined="NOTDEFINED", label=lambda w, d, h: f"Ø{w - 150}")
kind(V, "air-terminal", "fire-damper", ("brandklep", "fire damper", "Brandschutzklappe", "clapet coupe-feu"), (250, 350, 250), [(d + 100, 350, d + 100) for d in (100, 125, 160, 200, 250, 315)], base=2600, **{"class": "IfcDamper"}, predefined="FIREDAMPER", label=lambda w, d, h: f"Ø{w - 100}")
kind(V, "air-terminal", "silencer", ("geluiddemper", "silencer", "Schalldämpfer", "silencieux"), (260, 900, 260), [(d + 100, 900, d + 100) for d in (125, 160, 200, 250, 315)], base=2600, **{"class": "IfcDuctSilencer"}, predefined="ROUND", label=lambda w, d, h: f"Ø{w - 100}")
kind(V, "air-terminal", "volume-control-damper", ("volumeregelaar", "volume control damper", "Volumenstromregler", "régulateur de débit"), (250, 400, 250), [(d + 100, 400, d + 100) for d in (125, 160, 200, 250)], base=2600, **{"class": "IfcDamper"}, predefined="CONTROLDAMPER", label=lambda w, d, h: f"Ø{w - 100}")

# --- plumbing and drainage ----------------------------------------------------------------
P = "plumbing"
kind(P, "water-fitting", "basin-tap", ("wastafelkraan", "basin tap", "Waschtischarmatur", "robinet de lavabo"), (50, 150, 150), [(50, 150, 150)], base=900, predefined="FAUCET", label=box)
kind(P, "water-fitting", "kitchen-tap", ("keukenkraan", "kitchen tap", "Küchenarmatur", "robinet de cuisine"), (50, 220, 300), [(50, 220, 300)], base=900, predefined="FAUCET", label=box)
kind(P, "water-fitting", "shower-mixer", ("douchekraan", "shower mixer", "Brausearmatur", "mitigeur de douche"), (300, 100, 100), [(300, 100, 100)], base=1100, predefined="MIXING", label=box)
kind(P, "water-fitting", "bath-mixer", ("badkraan", "bath mixer", "Wannenarmatur", "mitigeur de baignoire"), (280, 180, 100), [(280, 180, 100)], base=750, predefined="MIXING", label=box)
kind(P, "water-fitting", "outside-tap", ("buitenkraan", "outside tap", "Außenzapfstelle", "robinet extérieur"), (80, 150, 100), [(80, 150, 100)], base=600, predefined="DRAWOFFCOCK", label=box)
kind(P, "water-fitting", "washing-machine-tap", ("wasmachinekraan", "washing machine tap", "Geräteanschlussventil", "robinet machine à laver"), (60, 100, 80), [(60, 100, 80)], base=1100, predefined="DRAWOFFCOCK", label=box)
kind(P, "water-fitting", "electric-water-heater", ("elektrische boiler", "electric water heater", "Elektro-Warmwasserspeicher", "chauffe-eau électrique"), (450, 450, 900), [(d, d, h) for d, h in ((260, 400), (450, 600), (450, 900), (520, 1300))], base=1000, **{"class": "IfcTank"}, predefined="STORAGE", label=lambda w, d, h: f"Ø{w} × {h}")
kind(P, "water-fitting", "water-meter", ("watermeter", "water meter", "Wasserzähler", "compteur d'eau"), (190, 100, 120), [(190, 100, 120)], base=300, **{"class": "IfcFlowMeter"}, predefined="WATERMETER", label=box)
kind(P, "water-fitting", "circulation-pump", ("circulatiepomp", "circulation pump", "Umwälzpumpe", "circulateur"), (130, 180, 150), [(130, 180, 150), (180, 250, 220)], base=1000, **{"class": "IfcPump"}, predefined="CIRCULATOR", label=box)
kind(P, "water-fitting", "pressure-booster", ("drukverhogingsinstallatie", "pressure booster set", "Druckerhöhungsanlage", "surpresseur"), (800, 600, 1200), [(800, 600, 1200)], **{"class": "IfcPump"}, predefined="NOTDEFINED", label=box)
kind(P, "water-fitting", "water-softener", ("waterontharder", "water softener", "Enthärtungsanlage", "adoucisseur"), (350, 500, 1100), [(350, 500, 1100)], **{"class": "IfcInterceptor"}, predefined="NOTDEFINED", label=box)
kind(P, "drain", "floor-gully", ("vloerput", "floor gully", "Bodenablauf", "siphon de sol"), (150, 150, 100), [(s, s, 100) for s in (100, 150, 200)], base=-100, predefined="FLOORWASTE", label=box)
kind(P, "drain", "shower-channel", ("douchegoot", "shower channel", "Duschrinne", "caniveau de douche"), (800, 70, 90), [(l, 70, 90) for l in (700, 800, 900, 1000, 1200)], base=-90, predefined="FLOORTRAP", label=units)
kind(P, "drain", "roof-outlet", ("dakafvoer", "roof outlet", "Dachablauf", "avaloir de toiture"), (250, 250, 150), [(d + 150, d + 150, 150) for d in (80, 100, 125)], base=-150, predefined="ROOFDRAIN", label=lambda w, d, h: f"Ø{w - 150}")
kind(P, "drain", "emergency-overflow", ("noodoverstort", "emergency overflow", "Notüberlauf", "trop-plein"), (300, 400, 100), [(300, 400, 100)], predefined="ROOFDRAIN", label=box)
kind(P, "drain", "channel-drain", ("lijngoot", "channel drain", "Entwässerungsrinne", "caniveau"), (1000, 130, 150), [(1000, 130, 150), (1000, 160, 200)], base=-150, predefined="GULLYSUMP", label=lambda w, d, h: f"{d}")
kind(P, "drain", "road-gully", ("straatkolk", "road gully", "Straßenablauf", "avaloir de voirie"), (300, 450, 600), [(300, 450, 600)], base=-600, predefined="GULLYSUMP", label=box)
kind(P, "drain", "inspection-chamber", ("inspectieput", "inspection chamber", "Kontrollschacht", "regard de visite"), (400, 400, 800), [(d, d, 800) for d in (315, 400, 600, 800)], base=-800, **{"class": "IfcDistributionChamberElement"}, predefined="INSPECTIONCHAMBER", label=lambda w, d, h: f"Ø{w}")
kind(P, "drain", "grease-separator", ("vetafscheider", "grease separator", "Fettabscheider", "séparateur de graisses"), (1500, 900, 1300), [(1500, 900, 1300)], base=-1300, **{"class": "IfcInterceptor"}, predefined="GREASE", label=box)
kind(P, "drain", "rainwater-tank", ("regenwatertank", "rainwater tank", "Regenwasserzisterne", "cuve d'eau de pluie"), (2400, 1400, 1500), [(w, d, h) for w, d, h in ((1800, 1200, 1300), (2400, 1400, 1500), (2900, 2000, 2000))], base=-2000, **{"class": "IfcTank"}, predefined="STORAGE", label=lambda w, d, h: f"{w} × {d}")

# --- electrical and lighting --------------------------------------------------------------
E = "electrical"
kind(E, "electrical-equipment", "distribution-board", ("groepenkast", "distribution board", "Verteiler", "tableau de répartition"), (220, 110, 330), [(w, 110, h) for w, h in ((220, 330), (330, 330), (330, 500), (550, 700), (800, 1200))], base=1300, predefined="CONSUMERUNIT", label=lambda w, d, h: f"{w} × {h}")
kind(E, "electrical-equipment", "main-switchboard", ("hoofdverdeler", "main switchboard", "Hauptverteilung", "tableau général"), (800, 400, 2000), [(w, 400, 2000) for w in (600, 800, 1200, 2000)], predefined="DISTRIBUTIONBOARD", label=units)
kind(E, "electrical-equipment", "pv-inverter", ("omvormer", "PV inverter", "Wechselrichter", "onduleur"), (400, 180, 500), [(350, 150, 400), (500, 200, 600)], base=1200, **{"class": "IfcElectricFlowTreatmentDevice"}, predefined="NOTDEFINED", label=lambda w, d, h: f"{w} × {h}")
kind(E, "electrical-equipment", "home-battery", ("thuisbatterij", "home battery", "Heimspeicher", "batterie domestique"), (650, 180, 1100), [(650, 180, 1100)], base=200, **{"class": "IfcElectricFlowStorageDevice"}, predefined="BATTERY", label=lambda w, d, h: f"{w} × {h}")
kind(E, "electrical-equipment", "wall-charger", ("laadpunt aan de wand", "wall charging point", "Wallbox", "borne de recharge murale"), (250, 150, 400), [(250, 150, 400)], base=1000, **{"class": "IfcElectricAppliance"}, predefined="NOTDEFINED", label=box)
kind(E, "electrical-equipment", "charging-post", ("laadpaal", "charging post", "Ladesäule", "borne de recharge"), (250, 250, 1400), [(250, 250, 1400)], **{"class": "IfcElectricAppliance"}, predefined="NOTDEFINED", label=box)
kind(E, "electrical-equipment", "transformer", ("transformator", "transformer", "Transformator", "transformateur"), (1600, 1000, 1700), [(1600, 1000, 1700)], **{"class": "IfcTransformer"}, predefined="NOTDEFINED", label=box)
kind(E, "electrical-equipment", "ups", ("noodstroomvoorziening", "uninterruptible power supply", "USV", "onduleur de secours"), (600, 800, 1400), [(600, 800, 1400)], **{"class": "IfcElectricFlowStorageDevice"}, predefined="UPS", label=box)
kind(E, "electrical-equipment", "data-cabinet", ("patchkast", "data cabinet", "Datenschrank", "baie de brassage"), (600, 600, 1200), [(600, 600, h) for h in (600, 1200, 2000)], **{"class": "IfcElectricAppliance"}, predefined="NOTDEFINED", label=lambda w, d, h: f"{h}")
plate = lambda w, d, h: ""
kind(E, "outlet", "socket-single", ("enkele wandcontactdoos", "single socket", "Einfachsteckdose", "prise simple"), (81, 30, 81), [(81, 30, 81)], base=300, predefined="POWEROUTLET", label=plate)
kind(E, "outlet", "socket-double", ("dubbele wandcontactdoos", "double socket", "Doppelsteckdose", "prise double"), (152, 30, 81), [(152, 30, 81)], base=300, predefined="POWEROUTLET", label=plate)
kind(E, "outlet", "socket-worktop", ("wandcontactdoos boven aanrecht", "worktop socket", "Steckdose über Arbeitsplatte", "prise de plan de travail"), (152, 30, 81), [(152, 30, 81)], base=1250, predefined="POWEROUTLET", label=plate)
kind(E, "outlet", "floor-box", ("vloerdoos", "floor box", "Bodentank", "boîte de sol"), (250, 250, 80), [(250, 250, 80)], base=-80, predefined="POWEROUTLET", label=plate)
kind(E, "outlet", "cooker-connection", ("perilexaansluiting", "cooker connection", "Herdanschlussdose", "prise cuisinière"), (81, 40, 81), [(81, 40, 81)], base=600, predefined="POWEROUTLET", label=plate)
kind(E, "outlet", "switch", ("schakelaar", "switch", "Schalter", "interrupteur"), (81, 20, 81), [(81, 20, 81)], base=1050, **{"class": "IfcSwitchingDevice"}, predefined="TOGGLESWITCH", label=plate)
kind(E, "outlet", "two-way-switch", ("wisselschakelaar", "two-way switch", "Wechselschalter", "va-et-vient"), (81, 20, 81), [(81, 20, 81)], base=1050, **{"class": "IfcSwitchingDevice"}, predefined="TOGGLESWITCH", label=plate)
kind(E, "outlet", "double-switch", ("serieschakelaar", "double switch", "Serienschalter", "double interrupteur"), (81, 20, 81), [(81, 20, 81)], base=1050, **{"class": "IfcSwitchingDevice"}, predefined="TOGGLESWITCH", label=plate)
kind(E, "outlet", "dimmer", ("dimmer", "dimmer", "Dimmer", "variateur"), (81, 30, 81), [(81, 30, 81)], base=1050, **{"class": "IfcSwitchingDevice"}, predefined="DIMMERSWITCH", label=plate)
kind(E, "outlet", "motion-sensor", ("bewegingsmelder", "motion sensor", "Bewegungsmelder", "détecteur de mouvement"), (100, 100, 50), [(100, 100, 50)], base=2550, **{"class": "IfcSensor"}, predefined="MOVEMENTSENSOR", label=plate)
kind(E, "outlet", "thermostat", ("thermostaat", "thermostat", "Raumthermostat", "thermostat"), (90, 25, 90), [(90, 25, 90)], base=1500, **{"class": "IfcController"}, predefined="NOTDEFINED", label=plate)
kind(E, "outlet", "data-outlet", ("data-aansluiting", "data outlet", "Datendose", "prise réseau"), (81, 30, 81), [(81, 30, 81)], base=300, predefined="DATAOUTLET", label=plate)
kind(E, "outlet", "tv-outlet", ("cai-aansluiting", "TV outlet", "Antennendose", "prise TV"), (81, 30, 81), [(81, 30, 81)], base=300, predefined="COMMUNICATIONSOUTLET", label=plate)
kind(E, "outlet", "doorbell", ("deurbel", "doorbell", "Türklingel", "sonnette"), (80, 30, 120), [(80, 30, 120)], base=1300, **{"class": "IfcAlarm"}, predefined="BELL", label=plate)
kind(E, "luminaire", "recessed-spot", ("inbouwspot", "recessed spot", "Einbaustrahler", "spot encastré"), (90, 90, 100), [(d, d, 100) for d in (70, 85, 110, 150, 200)], base=2500, predefined="POINTSOURCE", label=round_)
kind(E, "luminaire", "led-panel", ("led-paneel", "LED panel", "LED-Panel", "dalle LED"), (595, 595, 40), [(w, d, 40) for w, d in ((295, 295), (595, 595), (295, 1195), (595, 1195), (620, 620))], base=2560, predefined="DIRECTIONSOURCE", label=box)
kind(E, "luminaire", "batten-luminaire", ("montagebalk", "batten luminaire", "Lichtleiste", "réglette"), (1200, 60, 70), [(l, 60, 70) for l in (600, 1200, 1500)], base=2530, predefined="DIRECTIONSOURCE", label=units)
kind(E, "luminaire", "waterproof-luminaire", ("waterdicht armatuur", "waterproof luminaire", "Feuchtraumleuchte", "luminaire étanche"), (1270, 90, 90), [(l, 90, 90) for l in (670, 1270, 1570)], base=2510, predefined="DIRECTIONSOURCE", label=units)
kind(E, "luminaire", "linear-luminaire", ("lijnverlichting", "linear luminaire", "Lichtband", "ligne lumineuse"), (2000, 60, 80), [(l, 60, 80) for l in (1000, 1500, 2000, 3000)], base=2520, predefined="DIRECTIONSOURCE", label=units)
kind(E, "luminaire", "pendant", ("hanglamp", "pendant", "Pendelleuchte", "suspension"), (400, 400, 300), [(d, d, 300) for d in (300, 400, 600)], base=1800, predefined="POINTSOURCE", label=round_)
kind(E, "luminaire", "surface-ceiling-luminaire", ("plafonnière", "surface ceiling luminaire", "Deckenleuchte", "plafonnier"), (300, 300, 100), [(d, d, 100) for d in (250, 300, 400)], base=2500, predefined="POINTSOURCE", label=round_)
kind(E, "luminaire", "wall-luminaire", ("wandarmatuur", "wall luminaire", "Wandleuchte", "applique"), (150, 100, 250), [(150, 100, 250)], base=1800, predefined="POINTSOURCE", label=plate)
kind(E, "luminaire", "high-bay", ("hallenarmatuur", "high-bay luminaire", "Hallenleuchte", "luminaire grande hauteur"), (400, 400, 200), [(d, d, 200) for d in (300, 400)], base=6000, predefined="POINTSOURCE", label=round_)
kind(E, "luminaire", "outdoor-wall-light", ("buitenlamp", "outdoor wall light", "Außenwandleuchte", "applique extérieure"), (150, 120, 250), [(150, 120, 250)], base=2000, predefined="POINTSOURCE", label=plate)
kind(E, "luminaire", "bollard-light", ("lichtpaaltje", "bollard light", "Pollerleuchte", "borne lumineuse"), (150, 150, 900), [(150, 150, h) for h in (600, 900)], predefined="POINTSOURCE", label=lambda w, d, h: f"{h}")
kind(E, "luminaire", "lighting-column", ("lichtmast", "lighting column", "Lichtmast", "mât d'éclairage"), (200, 200, 6000), [(200, 200, h) for h in (4000, 6000, 8000)], predefined="POINTSOURCE", label=lambda w, d, h: f"{h}")
kind(E, "luminaire", "led-strip", ("ledstrip", "LED strip", "LED-Streifen", "ruban LED"), (1000, 12, 8), [(l, 12, 8) for l in (1000, 2000, 5000)], base=2500, predefined="DIRECTIONSOURCE", label=units)
kind(E, "solar-panel", "pv-panel", ("zonnepaneel", "PV panel", "PV-Modul", "panneau photovoltaïque"), (1134, 1722, 30), [(1134, 1722, 30), (1134, 1762, 30), (1134, 2278, 35), (1303, 2384, 35)], predefined="SOLARPANEL", label=box)
kind(E, "solar-panel", "solar-collector", ("zonnecollector", "solar collector", "Solarkollektor", "capteur solaire"), (1200, 2100, 90), [(1200, 2100, 90)], predefined="SOLARCOLLECTOR", label=box)

# --- fire and security --------------------------------------------------------------------
S = "safety"
kind(S, "fire-safety", "smoke-detector", ("rookmelder", "smoke detector", "Rauchmelder", "détecteur de fumée"), (110, 110, 50), [(110, 110, 50)], base=2550, predefined="SMOKESENSOR", label=plate)
kind(S, "fire-safety", "heat-detector", ("hittemelder", "heat detector", "Wärmemelder", "détecteur de chaleur"), (110, 110, 50), [(110, 110, 50)], base=2550, predefined="HEATSENSOR", label=plate)
kind(S, "fire-safety", "co-detector", ("koolmonoxidemelder", "carbon monoxide detector", "CO-Melder", "détecteur de monoxyde de carbone"), (110, 110, 40), [(110, 110, 40)], base=2550, predefined="COSENSOR", label=plate)
kind(S, "fire-safety", "manual-call-point", ("handbrandmelder", "manual call point", "Handfeuermelder", "déclencheur manuel"), (90, 50, 90), [(90, 50, 90)], base=1400, **{"class": "IfcAlarm"}, predefined="MANUALPULLBOX", label=plate)
kind(S, "fire-safety", "sounder-beacon", ("sirene met flitser", "sounder beacon", "Signalgeber", "sirène avec flash"), (100, 100, 100), [(100, 100, 100)], base=2400, **{"class": "IfcAlarm"}, predefined="SIREN", label=plate)
kind(S, "fire-safety", "fire-alarm-panel", ("brandmeldcentrale", "fire alarm panel", "Brandmelderzentrale", "centrale incendie"), (450, 130, 400), [(450, 130, 400)], base=1300, **{"class": "IfcController"}, predefined="NOTDEFINED", label=plate)
kind(S, "fire-safety", "fire-extinguisher", ("brandblusser", "fire extinguisher", "Feuerlöscher", "extincteur"), (160, 160, 520), [(130, 130, 400), (160, 160, 520), (180, 180, 620)], base=900, **{"class": "IfcFireSuppressionTerminal"}, predefined="NOTDEFINED", label=lambda w, d, h: {400: "2 kg", 520: "6 kg", 620: "9 kg"}[h])
kind(S, "fire-safety", "fire-hose-reel", ("brandslanghaspel", "fire hose reel", "Wandhydrant", "robinet d'incendie armé"), (700, 250, 700), [(700, 250, 700), (800, 250, 800)], base=900, **{"class": "IfcFireSuppressionTerminal"}, predefined="HOSEREEL", label=lambda w, d, h: f"{w} × {h}")
kind(S, "fire-safety", "sprinkler-head", ("sprinklerkop", "sprinkler head", "Sprinklerkopf", "tête de sprinkler"), (60, 60, 60), [(60, 60, 60)], base=2540, **{"class": "IfcFireSuppressionTerminal"}, predefined="SPRINKLER", label=plate)
kind(S, "fire-safety", "dry-riser-outlet", ("aansluiting droge blusleiding", "dry riser outlet", "Trockensteigleitung Entnahmestelle", "prise de colonne sèche"), (300, 200, 400), [(300, 200, 400)], base=800, **{"class": "IfcFireSuppressionTerminal"}, predefined="DRYHYDRANT", label=plate)
kind(S, "fire-safety", "emergency-luminaire", ("noodverlichting", "emergency luminaire", "Notleuchte", "bloc de secours"), (350, 60, 130), [(350, 60, 130)], base=2300, **{"class": "IfcLightFixture"}, predefined="SECURITYLIGHTING", code="63", label=plate)
kind(S, "fire-safety", "exit-sign", ("vluchtrouteaanduiding", "exit sign", "Rettungszeichenleuchte", "signalisation d'évacuation"), (350, 50, 180), [(350, 50, 180)], base=2200, **{"class": "IfcSign"}, predefined="NOTDEFINED", label=plate)
kind(S, "fire-safety", "smoke-vent", ("rookluik", "smoke vent", "Rauchabzug", "exutoire de fumée"), (1200, 1200, 400), [(s, s, 400) for s in (1000, 1200, 1500)], **{"class": "IfcDamper"}, predefined="SMOKEDAMPER", label=box)
kind(S, "security", "dome-camera", ("domecamera", "dome camera", "Dome-Kamera", "caméra dôme"), (130, 130, 100), [(130, 130, 100)], base=2500, predefined="CAMERA", label=plate)
kind(S, "security", "bullet-camera", ("buitencamera", "bullet camera", "Außenkamera", "caméra extérieure"), (90, 250, 90), [(90, 250, 90)], base=3000, predefined="CAMERA", label=plate)
kind(S, "security", "intercom-outdoor-station", ("intercom buitenpost", "intercom outdoor station", "Türsprechstelle", "platine de rue"), (130, 40, 250), [(130, 40, 250)], base=1300, **{"class": "IfcCommunicationsAppliance"}, predefined="NOTDEFINED", label=plate)
kind(S, "security", "intercom-indoor-station", ("intercom binnenpost", "intercom indoor station", "Innensprechstelle", "poste intérieur"), (160, 30, 200), [(160, 30, 200)], base=1400, **{"class": "IfcCommunicationsAppliance"}, predefined="NOTDEFINED", label=plate)
kind(S, "security", "card-reader", ("kaartlezer", "card reader", "Kartenleser", "lecteur de badge"), (80, 25, 120), [(80, 25, 120)], base=1100, **{"class": "IfcSensor"}, predefined="IDENTIFIERSENSOR", label=plate)
kind(S, "security", "alarm-panel", ("alarmcentrale", "intruder alarm panel", "Einbruchmelderzentrale", "centrale d'alarme"), (300, 100, 300), [(300, 100, 300)], base=1400, **{"class": "IfcController"}, predefined="NOTDEFINED", label=plate)
kind(S, "security", "pir-detector", ("inbraakdetector", "intruder detector", "Bewegungsmelder Einbruch", "détecteur d'intrusion"), (60, 50, 110), [(60, 50, 110)], base=2300, **{"class": "IfcSensor"}, predefined="MOVEMENTSENSOR", label=plate)
kind(S, "security", "door-contact", ("magneetcontact", "door contact", "Magnetkontakt", "contact de porte"), (60, 15, 15), [(60, 15, 15)], base=2100, **{"class": "IfcSensor"}, predefined="CONTACTSENSOR", label=plate)

# --- transport ----------------------------------------------------------------------------
T = "transport"
lifts = lambda w, d, h: f"{w} × {d}"
kind(T, "lift", "passenger-lift", ("personenlift", "passenger lift", "Personenaufzug", "ascenseur"), (1600, 1750, 3400), [(w, d, 3400) for w, d in ((1500, 1650), (1600, 1750), (1650, 2400), (2000, 2500))], predefined="ELEVATOR", label=lifts)
kind(T, "lift", "bed-lift", ("beddenlift", "bed lift", "Bettenaufzug", "monte-malades"), (2400, 3000, 3600), [(2400, 3000, 3600)], predefined="ELEVATOR", label=lifts)
kind(T, "lift", "goods-lift", ("goederenlift", "goods lift", "Lastenaufzug", "monte-charge"), (2200, 2600, 3600), [(w, d, 3600) for w, d in ((1800, 2200), (2200, 2600), (2800, 3400))], predefined="ELEVATOR", label=lifts)
kind(T, "lift", "platform-lift", ("plateaulift", "platform lift", "Plattformlift", "plateforme élévatrice"), (1400, 1600, 2600), [(1400, 1600, 2600)], predefined="LIFTINGGEAR", label=lifts)
kind(T, "lift", "stair-lift", ("traplift", "stair lift", "Treppenlift", "monte-escalier"), (650, 700, 1100), [(650, 700, 1100)], predefined="LIFTINGGEAR", label=lifts)
kind(T, "lift", "escalator", ("roltrap", "escalator", "Fahrtreppe", "escalier mécanique"), (1600, 12000, 4500), [(w, 12000, 4500) for w in (1200, 1600)], predefined="ESCALATOR", label=lambda w, d, h: f"{w}")

OUT.mkdir(exist_ok=True)
total = 0
for trade, objects in catalogue.items():
    ids = [o["id"] for o in objects]
    assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
    (OUT / f"{trade}.json").write_text("[\n" + ",\n".join("  " + json.dumps(o, ensure_ascii=False) for o in objects) + "\n]\n", encoding="utf-8")
    by_lod = {lod: sum(o["lod"] == lod for o in objects) for lod in ("200", "300")}
    print(f"{trade}: {len(objects)} objects ({by_lod['200']} at LOD 200, {by_lod['300']} at LOD 300)")
    total += len(objects)
print("total", total)
