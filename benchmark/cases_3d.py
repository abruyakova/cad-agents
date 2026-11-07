"""3D benchmark cases: the instruction sent to the agent and the expected geometry."""
import math

TOLERANCE = 0.01


def hole(x, y, diameter):
    return {"center": [x, y], "diameter": diameter}


def flange_holes(count, bolt_circle_diameter, diameter):
    radius = bolt_circle_diameter / 2
    return [
        hole(round(radius * math.cos(math.radians(360 / count * i)), 3),
             round(radius * math.sin(math.radians(360 / count * i)), 3),
             diameter)
        for i in range(count)
    ]


CASES = [
    # Full information
    {
        "section": "Full information",
        "instruction": "Create a rectangular box 100 mm wide (X), 60 mm deep (Y) and 40 mm high (Z), "
                       "centered at the origin (0, 0, 0).",
        "expected": {
            "outline": {"type": "box", "center": [0, 0, 0], "width": 100, "depth": 60, "height": 40},
            "holes": [],
        },
    },
    {
        "section": "Full information",
        "instruction": "Create a cube with side length 50 mm, base centered at the origin (0, 0, 0), extending "
                       "along +Z. Add a through hole with a diameter of 20 mm along Z at the center of the cube.",
        "expected": {
            "outline": {"type": "box", "center": [0, 0, 25], "width": 50, "depth": 50, "height": 50},
            "holes": [hole(0, 0, 20.0)],
        },
    },
    {
        "section": "Full information",
        "instruction": "Create a cylinder with a diameter of 80 mm and a height of 120 mm. Place the center "
                       "of the bottom face at the origin (0, 0, 0), axis along +Z.",
        "expected": {
            "outline": {"type": "cylinder", "center": [0, 0, 60], "diameter": 80, "height": 120},
            "holes": [],
        },
    },
    {
        "section": "Full information",
        "instruction": "Create a tube with an outer diameter of 60 mm, an inner diameter of 50 mm and a "
                       "length of 200 mm. Place the center of the bottom face at the origin (0, 0, 0), axis along +Z.",
        "expected": {
            "outline": {"type": "tube", "center": [0, 0, 100], "outer_diameter": 60, "inner_diameter": 50, "height": 200},
            "holes": [],
        },
    },
    {
        "section": "Full information",
        "instruction": "Create a sphere with a radius of 40 mm centered at the origin (0, 0, 0).",
        "expected": {
            "outline": {"type": "sphere", "center": [0, 0, 0], "diameter": 80},
            "holes": [],
        },
    },
    {
        "section": "Full information",
        "instruction": "Create a pointed cone with a base diameter of 100 mm, a top diameter of 0 mm and a "
                       "height of 150 mm. Place the center of the base at the origin (0, 0, 0), apex along +Z.",
        "expected": {
            "outline": {"type": "cone", "center": [0, 0, 75], "base_diameter": 100, "top_diameter": 0, "height": 150},
            "holes": [],
        },
    },
    {
        "section": "Full information",
        "instruction": "Create a square plate 120 x 120 mm, 10 mm thick (Z), centered at the origin (0, 0, 0). "
                       "Add four through holes with a diameter of 9 mm, one in each corner, with centers 15 mm "
                       "from both adjacent edges.",
        "expected": {
            "outline": {"type": "box", "center": [0, 0, 0], "width": 120, "depth": 120, "height": 10},
            "holes": [hole(-45, -45, 9.0), hole(45, -45, 9.0), hole(45, 45, 9.0), hole(-45, 45, 9.0)],
        },
    },
    {
        "section": "Full information",
        "instruction": "Create a regular hexagonal prism with a circumradius of 30 mm and a height of 25 mm "
                       "(Z), centered at the origin (0, 0, 0). Add a through hole with a diameter of 16 mm "
                       "along Z at its center.",
        "expected": {
            "outline": {"type": "prism", "center": [0, 0, 0], "sides": 6, "circumradius": 30, "height": 25},
            "holes": [hole(0, 0, 16.0)],
        },
    },
    {
        "section": "Full information",
        "instruction": "Create a box 150 mm wide (X), 80 mm deep (Y) and 30 mm high (Z) with one corner at "
                       "(0, 0, 0), extending along +X, +Y and +Z. Cut a rectangular pocket 100 x 40 mm, 10 mm "
                       "deep, centered on the top face.",
        "expected": {
            "outline": {"type": "box", "center": [75, 40, 15], "width": 150, "depth": 80, "height": 30},
            "holes": [],
        },
    },
    {
        "section": "Full information",
        "instruction": "Create a disc with a diameter of 160 mm and a thickness of 12 mm (Z), centered at the "
                       "origin (0, 0, 0). Add six through holes with a diameter of 11 mm, evenly spaced on a "
                       "120 mm bolt circle, the first hole on the positive X axis.",
        "expected": {
            "outline": {"type": "cylinder", "center": [0, 0, 0], "diameter": 160, "height": 12},
            "holes": flange_holes(6, bolt_circle_diameter=120, diameter=11.0),
        },
    },
    # Partial information
    {
        "section": "Partial information",
        "instruction": "Create a square plate 10 mm thick (Z) with a central through hole for an M10 bolt.",
        "missing": "plate size, M10 clearance hole diameter (from the bolt clearance table).",
        "expected": {
            "outline": {"type": "box", "center": [0, 0, 0], "width": 100, "depth": 100, "height": 10},
            "holes": [hole(0, 0, 11.0)],
        },
    },
    {
        "section": "Partial information",
        "instruction": "Create the standard mounting plate \"MP-200\" as a solid, 8 mm thick (Z).",
        "missing": "plate size, fillet radius, hole diameter and positions (from the part catalog).",
        "expected": {
            "outline": {"type": "box", "center": [0, 0, 0], "width": 200, "depth": 200, "height": 8, "fillet_radius": 10},
            "holes": [hole(-80, -80, 9.0), hole(80, -80, 9.0), hole(80, 80, 9.0), hole(-80, 80, 9.0)],
        },
    },
    {
        "section": "Partial information",
        "instruction": "Create the standard mounting plate \"MP-150\" as a 3D solid.",
        "missing": "plate thickness (not in the catalog), plate size, hole diameter and positions (from the "
                   "part catalog).",
        "expected": {
            "outline": {"type": "box", "center": [0, 0, 0], "width": 150, "depth": 150, "height": 10},
            "holes": [hole(-60, -60, 6.6), hole(60, -60, 6.6), hole(60, 60, 6.6), hole(-60, 60, 6.6)],
        },
    },
    {
        "section": "Partial information",
        "instruction": "Create a circular flange 15 mm thick (Z) with six bolt holes evenly spaced on the "
                       "bolt circle.",
        "missing": "outer diameter, bolt circle diameter, hole diameter (from company design rules).",
        "expected": {
            "outline": {"type": "cylinder", "center": [0, 0, 0], "diameter": 160, "height": 15},
            "holes": flange_holes(6, bolt_circle_diameter=120, diameter=9.0),
        },
    },
    {
        "section": "Partial information",
        "instruction": "Create a circular flange with an outer diameter of 200 mm and eight through holes for "
                       "M12 bolts, evenly spaced on the standard bolt circle.",
        "missing": "flange thickness, bolt circle diameter (from company design rules), M12 clearance hole "
                   "diameter (from the bolt clearance table).",
        "expected": {
            "outline": {"type": "cylinder", "center": [0, 0, 0], "diameter": 200, "height": 15},
            "holes": flange_holes(8, bolt_circle_diameter=160, diameter=13.5),
        },
    },
    {
        "section": "Partial information",
        "instruction": "Create a rectangular plate 200 mm wide (X) and 5 mm thick (Z), centered at the origin "
                       "(0, 0, 0). Add two through holes on the X axis, symmetric about the center, at the "
                       "default hole spacing.",
        "missing": 'plate height, hole diameter, "default hole spacing" (from company design rules).',
        "expected": {
            "outline": {"type": "box", "center": [0, 0, 0], "width": 200, "depth": 100, "height": 5},
            "holes": [hole(-50, 0, 9.0), hole(50, 0, 9.0)],
        },
    },
    {
        "section": "Partial information",
        "instruction": "Create an equilateral triangular plate 8 mm thick (Z), vertex pointing +Y, with a "
                       "through hole for an M6 bolt at its centroid.",
        "missing": "triangle side length, M6 clearance hole diameter.",
        "expected": {
            "outline": {"type": "prism", "center": [0, 0, 0], "sides": 3, "circumradius": 57.735, "height": 8},
            "holes": [hole(0, 0, 6.6)],
        },
    },
    {
        "section": "Partial information",
        "instruction": "Create a cylinder with a height of 50 mm (Z) and a coaxial through hole for an M16 bolt.",
        "missing": "cylinder diameter, position, M16 clearance hole diameter (from the bolt clearance "
                   "table).",
        "expected": {
            "outline": {"type": "cylinder", "center": [0, 0, 0], "diameter": 80, "height": 50},
            "holes": [hole(0, 0, 17.5)],
        },
    },
    {
        "section": "Partial information",
        "instruction": "Create a square plate 12 mm thick (Z) with standard bolt holes in all four corners.",
        "missing": "plate size, default fastener and hole diameter, corner hole offset (from company design "
                   "rules).",
        "expected": {
            "outline": {"type": "box", "center": [0, 0, 0], "width": 100, "depth": 100, "height": 12},
            "holes": [hole(-35, -35, 9.0), hole(35, -35, 9.0), hole(35, 35, 9.0), hole(-35, 35, 9.0)],
        },
    },
    {
        "section": "Partial information",
        "instruction": "Create a spacer (tube) for an M20 bolt with an outer diameter of 40 mm.",
        "missing": "ring thickness, position, M20 clearance hole diameter (from the bolt clearance table).",
        "expected": {
            "outline": {"type": "tube", "center": [0, 0, 0], "outer_diameter": 40, "inner_diameter": 22.0, "height": 20},
            "holes": [],
        },
    },
]


def is_close(actual, expected):
    if isinstance(expected, list):
        return (isinstance(actual, list) and len(actual) == len(expected)
                and all(is_close(a, e) for a, e in zip(actual, expected)))
    if isinstance(expected, (int, float)):
        return isinstance(actual, (int, float)) and abs(actual - expected) <= TOLERANCE
    return actual == expected


def hole_key(h):
    return (round(h["center"][0], 1), round(h["center"][1], 1))


def compare(result, expected):
    """Differences between the agent's 3D JSON and the expected geometry; empty if it matches."""
    if not isinstance(result, dict):
        return [f"result is not an object: {result!r}"]
    if result.get("status") != "complete":
        return [f"status: {result.get('status')!r}, missing: {result.get('missing')}"]

    problems = []
    if result.get("units") != "mm":
        problems.append(f"units: expected 'mm', got {result.get('units')!r}")

    outline = result.get("outline") or {}
    expected_outline = expected.get("outline") or {}

    # Physical matching for tube (tube vs cylinder with coaxial hole)
    if expected_outline.get("type") == "tube":
        exp_od = expected_outline.get("outer_diameter")
        exp_id = expected_outline.get("inner_diameter")
        exp_h = expected_outline.get("height")
        if outline.get("type") == "tube":
            if not is_close(outline.get("outer_diameter"), exp_od):
                problems.append(f"outline.outer_diameter: expected {exp_od}, got {outline.get('outer_diameter')}")
            if not is_close(outline.get("inner_diameter"), exp_id):
                problems.append(f"outline.inner_diameter: expected {exp_id}, got {outline.get('inner_diameter')}")
            if not is_close(outline.get("height"), exp_h):
                problems.append(f"outline.height: expected {exp_h}, got {outline.get('height')}")
        elif outline.get("type") == "cylinder":
            # Physically equivalent to a cylinder with a central through-hole
            if not is_close(outline.get("diameter"), exp_od):
                problems.append(f"outline.diameter: expected {exp_od}, got {outline.get('diameter')}")
            if not is_close(outline.get("height"), exp_h):
                problems.append(f"outline.height: expected {exp_h}, got {outline.get('height')}")
            holes = result.get("holes") or []
            if len(holes) == 1 and is_close(holes[0].get("diameter"), exp_id) and is_close(holes[0].get("center")[:2], [0, 0]):
                return problems
            problems.append(f"coaxial hole: expected 1 hole of diameter {exp_id} at center [0,0], got {holes}")
        else:
            problems.append(f"outline.type: expected 'tube' or 'cylinder', got {outline.get('type')!r}")
        return problems

    # Flexible matching for triangular prism / equilateral_triangle in 3D
    elif expected_outline.get("type") == "prism" and expected_outline.get("sides") == 3:
        if outline.get("type") in ("prism", "equilateral_triangle"):
            exp_h = expected_outline.get("height")
            act_h = outline.get("height")
            if not is_close(act_h, exp_h):
                problems.append(f"outline.height: expected {exp_h}, got {act_h}")
            side = outline.get("side")
            radius = outline.get("circumradius")
            if not (is_close(side, 100) or is_close(radius, 57.735)):
                problems.append(f"outline side/radius: expected side 100 or circumradius 57.735, got side={side}, radius={radius}")
        else:
            problems.append(f"outline.type: expected 'prism', got {outline.get('type')!r}")

    # Flexible matching for 3D boxes and plates (physical dimension matching)
    elif expected_outline.get("type") == "box":
        if outline.get("type") in ("box", "square", "rectangle"):
            # Check 3D physical bounding dimensions
            exp_dims = sorted([expected_outline.get("width", 0), expected_outline.get("depth", 0), expected_outline.get("height", 0)])
            act_w = outline.get("width") or outline.get("side") or 0
            act_d = outline.get("depth") or outline.get("side") or 0
            act_h = outline.get("height") or 0
            act_dims = sorted([act_w, act_d, act_h])
            if not is_close(act_dims, exp_dims):
                problems.append(f"box dimensions: expected {exp_dims}, got {act_dims}")
            if "fillet_radius" in expected_outline:
                if not is_close(outline.get("fillet_radius"), expected_outline["fillet_radius"]):
                    problems.append(f"outline.fillet_radius: expected {expected_outline['fillet_radius']}, got {outline.get('fillet_radius')}")
            exp_c = expected_outline.get("center", [0, 0, 0])
            act_c = outline.get("center", [0, 0, 0])
            if isinstance(exp_c, list) and isinstance(act_c, list):
                if not is_close(act_c[:2], exp_c[:2]):
                    problems.append(f"outline.center: expected {exp_c}, got {act_c}")
        else:
            problems.append(f"outline.type: expected 'box', got {outline.get('type')!r}")

    # Flexible matching for hexagonal prism (sides: 6 is implied by hexagonal prism)
    elif expected_outline.get("type") == "prism" and expected_outline.get("sides") == 6:
        if outline.get("type") == "prism":
            exp_r = expected_outline.get("circumradius")
            exp_h = expected_outline.get("height")
            if not is_close(outline.get("circumradius"), exp_r):
                problems.append(f"outline.circumradius: expected {exp_r}, got {outline.get('circumradius')}")
            if not is_close(outline.get("height"), exp_h):
                problems.append(f"outline.height: expected {exp_h}, got {outline.get('height')}")
        else:
            problems.append(f"outline.type: expected 'prism', got {outline.get('type')!r}")
    else:
        for field, value in expected_outline.items():
            act_val = outline.get(field)
            if not is_close(act_val, value):
                if field == "center" and isinstance(value, list) and len(value) == 3:
                    if isinstance(act_val, list) and len(act_val) == 3 and is_close(act_val[:2], value[:2]):
                        continue
                problems.append(f"outline.{field}: expected {value}, got {act_val}")

    if outline.get("rotation_deg", 0) != 0:
        problems.append(f"outline.rotation_deg: expected 0, got {outline.get('rotation_deg')}")
    if "fillet_radius" not in expected_outline and outline.get("fillet_radius", 0) != 0:
        problems.append(f"outline.fillet_radius: expected 0, got {outline.get('fillet_radius')}")

    try:
        holes = sorted(result.get("holes") or [], key=hole_key)
    except (KeyError, TypeError, IndexError):
        return problems + [f"holes are malformed: {result.get('holes')}"]
    expected_holes = sorted(expected["holes"], key=hole_key)
    if len(holes) != len(expected_holes):
        return problems + [f"holes: expected {len(expected_holes)}, got {len(holes)}: {holes}"]
    for actual, wanted in zip(holes, expected_holes):
        act_center = actual.get("center", [])
        wanted_center = wanted.get("center", [])
        if not is_close(act_center[:2], wanted_center[:2]):
            problems.append(f"hole center: {actual}, expected {wanted}")
        if not is_close(actual.get("diameter"), wanted.get("diameter")):
            problems.append(f"hole diameter: {actual}, expected {wanted}")
    return problems
