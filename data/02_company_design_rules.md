# Company Design Rules for 2D Sketches and 3D Solids

These rules apply whenever a drawing request leaves a value unspecified.
If a value is given explicitly in the request, the explicit value always wins.

## General conventions
- Units: millimeters (mm).
- Coordinate system: origin at (0, 0) for 2D and (0, 0, 0) for 3D, X axis to the right, Y axis up, Z axis up for 3D solids.
- Angles: degrees, measured counterclockwise from the positive X axis.
- If no position is given, shapes are centered at the origin.

## Default shape sizes (2D footprint and 3D solids)
- Square plate: side length **100 mm**.
- Rectangle with only width given: depth / height = **width / 2**.
- Equilateral triangle: side length **100 mm**, one vertex pointing up (+Y).
- Circular flange: if not specified, outer diameter **160 mm**.
- Cylinder diameter (when only height is specified): **80 mm**.

## Default 3D solid thickness and dimensions
- Default solid plate thickness (along Z): **10 mm**.
- Default circular flange thickness (along Z): **15 mm**.
- Default spacer / tube length (height along Z): **20 mm**.
- Equilateral triangular solid plate: thickness (height along Z) = **8 mm** unless specified; side length 100 mm.

## Default holes
- Default fastener when no bolt size is given: **M8**.
- Default hole diameter therefore: **9.0 mm** (M8 medium clearance, see bolt clearance table).
- Minimum distance from a hole center to any plate edge: **2 × hole diameter**.
- Corner holes: centers offset **15 mm** from both adjacent edges, unless the part spec says otherwise.
- Through holes in 3D solids extend straight through the solid along Z.

## Default hole spacing
- "Default hole spacing" for holes along a centerline: **100 mm center to center**.
- Holes are placed symmetrically about the part center.
  - Two holes: at −50 mm and +50 mm from center.
  - Three holes: at −100 mm, 0 mm, and +100 mm (only if they fit within edge distance rules; otherwise reduce spacing to fit).

## Flange bolt pattern
- Bolt circle diameter (BCD) = **outer diameter − 40 mm**.
- Holes are evenly spaced on the bolt circle.
- The first hole is placed at **0°** (on the positive X axis).
- Default flange hole diameter: 9.0 mm (M8 medium clearance).
- Standard bolt count for flanges: 6 holes (unless specified otherwise, e.g. 8 holes).

## Fillets
- Plates have sharp corners unless a fillet radius is specified or defined in the part spec.
