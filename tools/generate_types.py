#!/usr/bin/env python3
"""Writes the catalogues of linear types of the library: `types/<what>.json`.

    python3 tools/generate_types.py

Each file is a list of linear types: beams, columns, piles, pipes, ducts, cable trays, mullions
and skirtings of usual Dutch sizes, of no manufacturer. An entry is a linear type as
`bim-library` reads it (`bim_library::LinearType`: id, role, material, profile, name), or a
steel profile by its designation in the suite's steel table (`{"id", "role", "designation"}`),
which the builder turns into a type with that profile's shape.

Sizes are millimetres here and metres in the files. Materials are keys of the Dutch library.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "types"
catalogue = {}


def slug(text):
    out = "".join(c if c.isalnum() else "-" for c in text.lower())
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def m(mm):
    return round(mm / 1000, 5)


def add(what, role, material, name, profile):
    catalogue.setdefault(what, []).append({"id": f"nl.{role}.{slug(name)}", "role": role, "material": material, "profile": profile, "name": name})


def steel(what, role, designation):
    catalogue.setdefault(what, []).append({"id": f"nl.{role}.{slug(designation)}", "role": role, "designation": designation})


def rect(w, d):
    return {"kind": "rectangle", "width": m(w), "depth": m(d)}


def tube(d, t):
    return {"kind": "chs", "d": m(d), "t": m(t)}


def box(h, b, t):
    return {"kind": "rhs", "h": m(h), "b": m(b), "t": m(t), "r_out": 0.0, "r_in": 0.0}


# --- structure: steel beams and columns of the steel table, timber and concrete ------------
S = "structure"
for size in (80, 100, 120, 140, 160, 180, 200, 220, 240, 270, 300, 330, 360, 400, 450, 500, 550, 600):
    steel(S, "beam", f"IPE {size}")
for series in ("HEA", "HEB"):
    for size in (100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 400, 450, 500, 600):
        steel(S, "beam", f"{series} {size}")
        if size <= 400:
            steel(S, "column", f"{series} {size}")
for size in (80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300):
    steel(S, "beam", f"UPN {size}")
for s, t in ((80, 5), (100, 5), (100, 8), (120, 6), (120, 8), (140, 8), (150, 8), (160, 8), (180, 10), (200, 8), (200, 10), (250, 10), (300, 10)):
    steel(S, "column", f"SHS {s}x{s}x{t}")
for d, t in ((114.3, 5), (139.7, 5), (168.3, 6.3), (219.1, 8), (273, 10), (323.9, 10)):
    steel(S, "column", f"CHS {d:g}x{t:g}")
for w, d in ((90, 270), (90, 315), (115, 315), (115, 360), (140, 405), (140, 450), (140, 495), (160, 540), (160, 585), (180, 630), (200, 720)):
    add(S, "beam", "timber", f"GL24h {w}x{d}", rect(w, d))
for w, d in ((44, 146), (44, 171), (59, 156), (59, 196), (71, 171), (71, 196), (71, 221), (71, 246), (96, 196), (96, 246)):
    add(S, "beam", "spruce", f"vuren balk {w}x{d}", rect(w, d))
for s in (120, 140, 160, 180, 200):
    add(S, "column", "timber", f"GL24h kolom {s}x{s}", rect(s, s))
for w, d in ((200, 400), (250, 500), (300, 500), (300, 600), (350, 700), (400, 800), (500, 1000)):
    add(S, "beam", "concrete", f"betonbalk {w}x{d}", rect(w, d))
for s in (200, 250, 300, 350, 400, 500, 600):
    add(S, "column", "concrete", f"betonkolom {s}x{s}", rect(s, s))
for d in (300, 400, 500, 600):
    add(S, "column", "concrete", f"betonkolom rond {d}", {"kind": "circle", "diameter": m(d)})
for w, d in ((100, 65), (100, 100), (120, 100), (150, 100)):
    add(S, "beam", "precast-concrete", f"betonlatei {w}x{d}", rect(w, d))
for l, t in ((80, 8), (100, 8), (100, 10), (120, 10), (150, 12)):
    steel(S, "beam", f"L {l}x{l}x{t}")

# --- foundations: piles ---------------------------------------------------------------------
F = "foundation"
for s in (180, 220, 250, 290, 320, 350, 380, 400, 450):
    add(F, "pile", "precast-concrete", f"prefab heipaal {s}x{s}", rect(s, s))
for d in (270, 320, 360, 410, 460, 510, 560, 610):
    add(F, "pile", "concrete", f"vibropaal rond {d}", {"kind": "circle", "diameter": m(d)})
for d in (300, 350, 400, 450, 500, 600):
    add(F, "pile", "concrete", f"schroefpaal rond {d}", {"kind": "circle", "diameter": m(d)})
for d, t in ((114.3, 6.3), (168.3, 8), (219.1, 10), (273, 10), (323.9, 12.5)):
    add(F, "pile", "steel", f"stalen buispaal {d:g}x{t:g}", tube(d, t))
for d in (200, 250, 300):
    add(F, "pile", "timber", f"houten paal rond {d}", {"kind": "circle", "diameter": m(d)})
for w, d in ((400, 500), (500, 600), (600, 800), (800, 1000)):
    add(F, "beam", "concrete", f"funderingsbalk {w}x{d}", rect(w, d))

# --- timber members: studs, battens, rafters ------------------------------------------------
T = "timber"
for w, d in ((38, 63), (38, 89), (38, 120), (38, 140), (38, 184), (38, 235), (38, 286)):
    add(T, "member", "spruce", f"SLS {w}x{d}", rect(w, d))
for w, d in ((11, 22), (15, 28), (18, 45), (22, 32), (22, 50), (25, 38), (28, 45), (28, 70), (32, 50), (44, 70), (44, 96), (59, 59), (70, 70), (96, 96)):
    add(T, "member", "spruce", f"vuren lat {w}x{d}", rect(w, d))
for w, d in ((45, 70), (45, 90), (67, 67), (67, 90), (67, 114), (67, 139), (90, 114), (90, 139)):
    add(T, "mullion", "meranti", f"kozijnhout {w}x{d}", rect(w, d))
for w, d in ((12, 55), (12, 70), (15, 90), (18, 120), (18, 140)):
    add(T, "skirting", "mdf", f"plint MDF {w}x{d}", rect(w, d))
for w, d in ((14, 70), (18, 90), (22, 120)):
    add(T, "skirting", "oak", f"plint eiken {w}x{d}", rect(w, d))

# --- facade: mullions of curtain walls ------------------------------------------------------
G = "facade"
for b, h in ((50, 60), (50, 100), (50, 125), (50, 150), (50, 175), (60, 150), (60, 180), (60, 225)):
    add(G, "mullion", "aluminium", f"aluminium stijl {b}x{h}", box(h, b, 2.5))
for b, h in ((50, 80), (50, 120), (60, 140), (60, 180)):
    add(G, "mullion", "steel", f"stalen stijl {b}x{h}", box(h, b, 3))
for b, h in ((60, 120), (60, 160), (80, 200), (80, 240)):
    add(G, "mullion", "timber", f"houten stijl {b}x{h}", rect(b, h))

# --- pipes ----------------------------------------------------------------------------------
P = "pipes"
for d, t in ((32, 3), (40, 3), (50, 3), (75, 3), (90, 3), (110, 3.2), (125, 3.2), (160, 4), (200, 4.9), (250, 6.2), (315, 7.7)):
    add(P, "pipe", "pvc", f"PVC afvoer {d}", tube(d, t))
for d, t in ((70, 1.5), (80, 1.5), (100, 1.8), (125, 2.2)):
    add(P, "pipe", "pvc", f"PVC hemelwaterafvoer {d}", tube(d, t))
for d, t in ((80, 0.7), (100, 0.7), (120, 0.8)):
    add(P, "pipe", "zinc", f"zinken hemelwaterafvoer {d}", tube(d, t))
for d, t in ((12, 1), (15, 1), (18, 1), (22, 1), (28, 1), (35, 1.2), (42, 1.2), (54, 1.5)):
    add(P, "pipe", "copper", f"koperen leiding {d}", tube(d, t))
for d, t in ((16, 2), (20, 2.25), (26, 3), (32, 3), (40, 3.5), (50, 4), (63, 4.5)):
    add(P, "pipe", "generic", f"meerlagenbuis {d}", tube(d, t))
for dn, d, t in ((15, 21.3, 2.6), (20, 26.9, 2.6), (25, 33.7, 3.2), (32, 42.4, 3.2), (40, 48.3, 3.2), (50, 60.3, 3.6), (65, 76.1, 3.6), (80, 88.9, 4), (100, 114.3, 4.5), (125, 139.7, 5), (150, 168.3, 5)):
    add(P, "pipe", "steel", f"stalen leiding DN{dn}", tube(d, t))
for d, t in ((20, 2), (25, 2.3), (32, 3), (40, 3.7), (50, 4.6), (63, 5.8), (90, 8.2), (110, 10)):
    add(P, "pipe", "generic", f"PE waterleiding {d}", tube(d, t))
for d, t in ((16, 1.5), (19, 1.5)):
    add(P, "pipe", "pvc", f"installatiebuis {d}", tube(d, t))

# --- ducts ----------------------------------------------------------------------------------
D = "ducts"
for d in (80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800):
    add(D, "duct", "galvanised-steel", f"spirobuis {d}", tube(d, 0.5 if d <= 315 else 0.8))
for w, h in ((200, 100), (300, 100), (300, 150), (300, 200), (400, 200), (400, 300), (500, 250), (500, 300), (600, 300), (600, 400), (800, 400), (1000, 400), (1000, 500), (1200, 600)):
    add(D, "duct", "galvanised-steel", f"rechthoekig kanaal {w}x{h}", box(h, w, 0.8))
for w, h in ((110, 54), (140, 50), (204, 60), (220, 55)):
    add(D, "duct", "pvc", f"instortkanaal {w}x{h}", box(h, w, 2))
for d in (75, 90):
    add(D, "duct", "generic", f"flexibele luchtslang {d}", tube(d, 2))

# --- cable trays ----------------------------------------------------------------------------
C = "cable-trays"
for w in (60, 100, 150, 200, 300, 400, 500, 600):
    add(C, "cable-tray", "galvanised-steel", f"kabelgoot {w}x60", rect(w, 60))
for w in (100, 200, 300, 400, 500, 600):
    add(C, "cable-tray", "galvanised-steel", f"kabelladder {w}x100", rect(w, 100))
for w, h in ((60, 40), (90, 55), (130, 60), (170, 60)):
    add(C, "cable-tray", "pvc", f"wandgoot {w}x{h}", rect(w, h))
for w, h in ((200, 38), (250, 38), (350, 48)):
    add(C, "cable-tray", "galvanised-steel", f"vloergoot {w}x{h}", rect(w, h))

OUT.mkdir(exist_ok=True)
total = 0
for what, types in catalogue.items():
    ids = [t["id"] for t in types]
    assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
    (OUT / f"{what}.json").write_text("[\n" + ",\n".join("  " + json.dumps(t, ensure_ascii=False) for t in types) + "\n]\n", encoding="utf-8")
    print(f"{what}: {len(types)} types")
    total += len(types)
print("total", total)
