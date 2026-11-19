# Open BIM Library

Library files for [Open BIM Suite](https://github.com/OpenAEC-Foundation/open-bim-suite): materials,
types and objects as IFCX, with an index that says what each file holds. A program lists the
libraries from the index and fetches the one that is asked for, so a library does not have to
be compiled into it.

Dutch: bibliotheekbestanden voor Open BIM Suite, als IFCX, met een index. Een programma toont
de bibliotheken uit de index en haalt alleen op wat gevraagd wordt.

## What is here

| File | Holds |
|---|---|
| [`index.json`](index.json) | every library file with its names, what it is about, how many of each kind of thing it holds, and how many types it has at LOD 200, 300, 350 and 400 |
| `ifcx/general.ifcx` | the library every project starts with: materials, build-ups, linear and system types, a generic object of each group, NL-SfB codes, drawing sets and view templates |
| `ifcx/nl.ifcx` | Dutch materials and types: the INB template, the materials, timber sizes, concrete sections, walls and floors of Project Ocondat, and usual Dutch layered build-ups |
| `ifcx/nl-objects-<trade>.ifcx` | generic objects of usual Dutch sizes, a file per trade (below) |
| `ifcx/nl-types-<what>.ifcx` | linear types of usual Dutch sizes, a file per kind (below) |
| `ifcx/house-style-openaec.ifcx` | the starter house style: colours, typefaces, sheet formats, title block, dimensions |
| `objects/<trade>.json`, `types/<what>.json` | the catalogues the object and type files are built from |
| `tools/generate_objects.py`, `tools/generate_types.py` | write the catalogues |

## Objects

747 object types in eight trades. Each kind has one object at **LOD 200** (generic, about the
right size, to reserve its place) and its usual sizes at **LOD 300** (specific).

| Trade | Groups | Objects |
|---|---|---|
| architecture | doors, windows, stairs, railings | 146 |
| interior | sanitary fittings, kitchens, furniture, appliances | 140 |
| heating | heat emitters (radiators, convectors, manifolds), heat and cold sources (boilers, heat pumps, cylinders, air conditioners) | 167 |
| ventilation | ventilation units (heat recovery, fans, air handling), air terminals (valves, grilles, diffusers, louvres, fire dampers, silencers) | 91 |
| plumbing | water fittings (taps, water heaters, pumps, meters), drains (gullies, roof outlets, chambers, separators) | 58 |
| electrical | electrical equipment (boards, inverters, batteries, charging points), sockets and switches, luminaires, solar panels | 98 |
| safety | fire safety (detectors, call points, extinguishers, hose reels, sprinklers, emergency lighting), security | 29 |
| transport | lifts, platform lifts, escalators | 18 |

An object type has a group, names in Dutch, English, German and French, a size (width, depth,
height), the height it is mounted at, its IFC class and predefined type, its NL-SfB code and
its level of development. The suite draws an object as a box of its size; a door or a window
cuts an opening in the wall it stands in.

## Linear types

362 linear types in seven files. Steel beams and columns are profiles of the suite's steel
table, taken by their designation.

| File | Holds | Types |
|---|---|---|
| structure | steel beams and columns (IPE, HEA, HEB, UPN, SHS, CHS, angles as lintels), glued laminated and sawn timber beams, concrete beams, columns and lintels | 168 |
| foundation | precast driven piles, cast-in-place and screw piles, steel tube piles, timber piles, foundation beams | 35 |
| timber | SLS studs, battens, frame sections, skirtings | 37 |
| facade | mullions of aluminium, steel and timber | 16 |
| pipes | PVC drainage and rainwater pipes, zinc downpipes, copper, multilayer, steel and PE pipes, conduit | 54 |
| ducts | spiral ducts, rectangular ducts, cast-in ducts, flexible hoses | 31 |
| cable-trays | cable trays and ladders, wall and floor trunking | 21 |

A pipe or a hose of no particular material is of the generic material and so LOD 200.

### Levels of development

The levels are those of the BIMForum Level of Development Specification, as offices use them:

- **LOD 200**: a generic element of about the right size, shape and place.
- **LOD 300**: a specific element: its size, its shape and what it is made of are those it will have.
- **LOD 350**: as LOD 300, with what joins it to the elements round it.
- **LOD 400**: worked out to be made: every part and fixing.

The objects here stop at LOD 300. A wall or floor of the generic material is LOD 200, one of
real layers LOD 300, a system with its members LOD 350, a frame worked out to its layers
LOD 400.

## To know

- **The objects are generic, of no manufacturer.** Their sizes are usual Dutch sizes written
  down from general knowledge, not taken from product data. Check a size before you build on
  it.
- The NL-SfB code of an object is the two digits of its group (63 for a luminaire); the Dutch
  BIM basis ILS asks four.
- The IFC classes are those of IFC 4.3.

## Building the files

The IFCX files and the index are built by Open BIM Suite's library crate, so they are exactly
what the suite reads:

```bash
python3 tools/generate_objects.py
```

```bash
python3 tools/generate_types.py
```

```bash
cargo run -p bim-library --example build_library -- PATH/TO/open-bim-library/objects PATH/TO/open-bim-library 2026-11-19T00:00:00Z
```

The last command is run in a checkout of Open BIM Suite.

## Licence

LGPL-3.0-or-later, as Open BIM Suite. The Dutch library contains material of the INB template
and of [Project Ocondat](https://github.com/OpenAEC-Foundation/project-ocondat) of the OpenAEC
Foundation (LGPL-3.0).
