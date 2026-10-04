"""3D benchmark cases: the instruction sent to the agent.

There is no expected geometry yet. Add an "expected" entry ({"outline": ..., "holes": [...]})
using the 3D outline types from data/system_promt.txt; cases_2d.compare() checks it the same way.
"""

CASES = [
    # Full information
    {
        "section": "Full information",
        "instruction": "Create a rectangular box 100 mm wide (X), 60 mm deep (Y) and 40 mm high (Z), "
                       "centered at the origin (0, 0, 0).",
    },
    {
        "section": "Full information",
        "instruction": "Create a cube with side length 50 mm, base centered at the origin (0, 0, 0), extending "
                       "along +Z. Add a through hole with a diameter of 20 mm along Z at the center of the cube.",
    },
    {
        "section": "Full information",
        "instruction": "Create a cylinder with a diameter of 80 mm and a height of 120 mm. Place the center "
                       "of the bottom face at the origin (0, 0, 0), axis along +Z.",
    },
    {
        "section": "Full information",
        "instruction": "Create a tube with an outer diameter of 60 mm, an inner diameter of 50 mm and a "
                       "length of 200 mm. Place the center of the bottom face at the origin (0, 0, 0), axis along +Z.",
    },
    {
        "section": "Full information",
        "instruction": "Create a sphere with a radius of 40 mm centered at the origin (0, 0, 0).",
    },
    {
        "section": "Full information",
        "instruction": "Create a pointed cone with a base diameter of 100 mm, a top diameter of 0 mm and a "
                       "height of 150 mm. Place the center of the base at the origin (0, 0, 0), apex along +Z.",
    },
    {
        "section": "Full information",
        "instruction": "Create a square plate 120 x 120 mm, 10 mm thick (Z), centered at the origin (0, 0, 0). "
                       "Add four through holes with a diameter of 9 mm, one in each corner, with centers 15 mm "
                       "from both adjacent edges.",
    },
    {
        "section": "Full information",
        "instruction": "Create a regular hexagonal prism with a circumradius of 30 mm and a height of 25 mm "
                       "(Z), centered at the origin (0, 0, 0). Add a through hole with a diameter of 16 mm "
                       "along Z at its center.",
    },
    {
        "section": "Full information",
        "instruction": "Create a box 150 mm wide (X), 80 mm deep (Y) and 30 mm high (Z) with one corner at "
                       "(0, 0, 0), extending along +X, +Y and +Z. Cut a rectangular pocket 100 x 40 mm, 10 mm "
                       "deep, centered on the top face.",
    },
    {
        "section": "Full information",
        "instruction": "Create a disc with a diameter of 160 mm and a thickness of 12 mm (Z), centered at the "
                       "origin (0, 0, 0). Add six through holes with a diameter of 11 mm, evenly spaced on a "
                       "120 mm bolt circle, the first hole on the positive X axis.",
    },
    # Partial information
    {
        "section": "Partial information",
        "instruction": "Create a square plate 10 mm thick (Z) with a central through hole for an M10 bolt.",
        "missing": "plate size, M10 clearance hole diameter (from the bolt clearance table).",
    },
    {
        "section": "Partial information",
        "instruction": "Create the standard mounting plate \"MP-200\" as a solid, 8 mm thick (Z).",
        "missing": "plate size, fillet radius, hole diameter and positions (from the part catalog).",
    },
    {
        "section": "Partial information",
        "instruction": "Create the standard mounting plate \"MP-150\" as a 3D solid.",
        "missing": "plate thickness (not in the catalog), plate size, hole diameter and positions (from the "
                   "part catalog).",
    },
    {
        "section": "Partial information",
        "instruction": "Create a circular flange 15 mm thick (Z) with six bolt holes evenly spaced on the "
                       "bolt circle.",
        "missing": "outer diameter, bolt circle diameter, hole diameter (from company design rules).",
    },
    {
        "section": "Partial information",
        "instruction": "Create a circular flange with an outer diameter of 200 mm and eight through holes for "
                       "M12 bolts, evenly spaced on the standard bolt circle.",
        "missing": "flange thickness, bolt circle diameter (from company design rules), M12 clearance hole "
                   "diameter (from the bolt clearance table).",
    },
    {
        "section": "Partial information",
        "instruction": "Create a rectangular plate 200 mm wide (X) and 5 mm thick (Z), centered at the origin "
                       "(0, 0, 0). Add two through holes on the X axis, symmetric about the center, at the "
                       "default hole spacing.",
        "missing": 'plate height, hole diameter, "default hole spacing" (from company design rules).',
    },
    {
        "section": "Partial information",
        "instruction": "Create an equilateral triangular plate 8 mm thick (Z), vertex pointing +Y, with a "
                       "through hole for an M6 bolt at its centroid.",
        "missing": "triangle side length, M6 clearance hole diameter.",
    },
    {
        "section": "Partial information",
        "instruction": "Create a cylinder with a height of 50 mm (Z) and a coaxial through hole for an M16 bolt.",
        "missing": "cylinder diameter, position, M16 clearance hole diameter (from the bolt clearance "
                   "table).",
    },
    {
        "section": "Partial information",
        "instruction": "Create a square plate 12 mm thick (Z) with standard bolt holes in all four corners.",
        "missing": "plate size, default fastener and hole diameter, corner hole offset (from company design "
                   "rules).",
    },
    {
        "section": "Partial information",
        "instruction": "Create a spacer (tube) for an M20 bolt with an outer diameter of 40 mm.",
        "missing": "ring thickness, position, M20 clearance hole diameter (from the bolt clearance table).",
    },
]
