"""2D benchmark cases: the instruction sent to the agent and the geometry it should return."""
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
        "instruction": "Create a square with side length 100 mm centered at the origin. "
                       "Place a circle with a radius of 20 mm at the center of the square.",
        "expected": {
            "outline": {"type": "square", "center": [0, 0], "side": 100},
            "holes": [hole(0, 0, 40)],
        },
    },
    {
        "section": "Full information",
        "instruction": "Draw a circle with a radius of 50 mm centered at (0, 0). "
                       "Inside it, add a concentric circle with a radius of 25 mm.",
        "expected": {
            "outline": {"type": "circle", "center": [0, 0], "diameter": 100},
            "holes": [hole(0, 0, 50)],
        },
    },
    {
        "section": "Full information",
        "instruction": "Create a rectangle 150 mm wide and 80 mm tall with its bottom-left corner at (0, 0). "
                       "Add a circle with a diameter of 30 mm at the center of the rectangle.",
        "expected": {
            "outline": {"type": "rectangle", "center": [75, 40], "width": 150, "height": 80},
            "holes": [hole(75, 40, 30)],
        },
    },
    {
        "section": "Full information",
        "instruction": "Draw a regular hexagon with a circumradius of 60 mm centered at the origin. "
                       "Place a circle with radius 30 mm at its center.",
        "expected": {
            "outline": {"type": "regular_polygon", "center": [0, 0], "sides": 6, "circumradius": 60},
            "holes": [hole(0, 0, 60)],
        },
    },
    # Partial information (filled from the knowledge base)
    {
        "section": "Partial information",
        "instruction": "Create a square plate centered at the origin with a central hole for an M10 bolt.",
        "missing": "plate size, hole diameter for M10 clearance (e.g. from a bolt standard table).",
        "expected": {
            "outline": {"type": "square", "center": [0, 0], "side": 100},
            "holes": [hole(0, 0, 11.0)],
        },
    },
    {
        "section": "Partial information",
        "instruction": 'Make a standard mounting plate, type "MP-200", with four corner holes.',
        "missing": "plate dimensions, hole diameter, hole offset from corners (from an internal product spec).",
        "expected": {
            "outline": {"type": "square", "center": [0, 0], "side": 200, "fillet_radius": 10},
            "holes": [hole(-80, -80, 9.0), hole(80, -80, 9.0), hole(80, 80, 9.0), hole(-80, 80, 9.0)],
        },
    },
    {
        "section": "Partial information",
        "instruction": "Draw a circular flange with 6 bolt holes evenly spaced on the bolt circle, "
                       "outer diameter 160 mm.",
        "missing": "bolt circle diameter, hole diameter.",
        "expected": {
            "outline": {"type": "circle", "center": [0, 0], "diameter": 160},
            "holes": flange_holes(6, bolt_circle_diameter=120, diameter=9.0),
        },
    },
    {
        "section": "Partial information",
        "instruction": "Create a rectangle 200 mm wide centered at the origin, with two holes along the "
                       "horizontal centerline using our default hole spacing.",
        "missing": 'rectangle height, hole diameter, "default hole spacing" (from company design rules).',
        "expected": {
            "outline": {"type": "rectangle", "center": [0, 0], "width": 200, "height": 100},
            "holes": [hole(-50, 0, 9.0), hole(50, 0, 9.0)],
        },
    },
    {
        "section": "Partial information",
        "instruction": "Draw an equilateral triangle, centered at the origin with one vertex pointing up, "
                       "and place a circle at its centroid with the standard clearance hole for M6.",
        "missing": "triangle side length, M6 clearance hole diameter.",
        "expected": {
            "outline": {"type": "equilateral_triangle", "center": [0, 0], "side": 100},
            "holes": [hole(0, 0, 6.6)],
        },
    },
    {
        "section": "Partial information",
        "instruction": 'Create a rectangular bracket for part "BR-45" with three holes in a row; '
                       "the middle hole is larger than the outer two.",
        "missing": "all dimensions, hole sizes, spacing (from a part catalog).",
        "expected": {
            "outline": {"type": "rectangle", "center": [0, 0], "width": 120, "height": 45},
            "holes": [hole(-40, 0, 9.0), hole(0, 0, 13.5), hole(40, 0, 9.0)],
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
    """Differences between the agent's JSON and the expected geometry; empty if it matches."""
    if not isinstance(result, dict):
        return [f"result is not an object: {result!r}"]
    if result.get("status") != "complete":
        return [f"status: {result.get('status')!r}, missing: {result.get('missing')}"]

    problems = []
    if result.get("units") != "mm":
        problems.append(f"units: expected 'mm', got {result.get('units')!r}")

    outline = result.get("outline") or {}
    for field, value in expected["outline"].items():
        if not is_close(outline.get(field), value):
            problems.append(f"outline.{field}: expected {value}, got {outline.get(field)}")
    if outline.get("rotation_deg", 0) != 0:
        problems.append(f"outline.rotation_deg: expected 0, got {outline.get('rotation_deg')}")
    if "fillet_radius" not in expected["outline"] and outline.get("fillet_radius", 0) != 0:
        problems.append(f"outline.fillet_radius: expected 0, got {outline.get('fillet_radius')}")

    try:
        holes = sorted(result.get("holes") or [], key=hole_key)
    except (KeyError, TypeError, IndexError):
        return problems + [f"holes are malformed: {result.get('holes')}"]
    expected_holes = sorted(expected["holes"], key=hole_key)
    if len(holes) != len(expected_holes):
        return problems + [f"holes: expected {len(expected_holes)}, got {len(holes)}: {holes}"]
    for actual, wanted in zip(holes, expected_holes):
        if not is_close(actual.get("center"), wanted["center"]):
            problems.append(f"hole center: {actual}, expected {wanted}")
        if not is_close(actual.get("diameter"), wanted["diameter"]):
            problems.append(f"hole diameter: {actual}, expected {wanted}")
    return problems
