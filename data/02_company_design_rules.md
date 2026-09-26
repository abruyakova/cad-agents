# Company Design Rules for 2D Sketches

These rules apply whenever a drawing request leaves a value unspecified.
If a value is given explicitly in the request, the explicit value always wins.

## General conventions
- Units: millimeters (mm).
- Coordinate system: origin at (0, 0), X axis to the right, Y axis up.
- Angles: degrees, measured counterclockwise from the positive X axis.
- If no position is given, shapes are centered at the origin.

## Default shape sizes
- Square plate: side length **100 mm**.
- Rectangle with only width given: height = **width / 2**.
- Equilateral triangle: side length **100 mm**, one vertex pointing up (+Y).
- Circular flange: if not specified, outer diameter **160 mm**.

## Default holes
- Default fastener when no bolt size is given: **M8**.
- Default hole diameter therefore: **9.0 mm** (M8 medium clearance, see bolt clearance table).
- Minimum distance from a hole center to any plate edge: **2 × hole diameter**.
- Corner holes: centers offset **15 mm** from both adjacent edges, unless the part spec says otherwise.

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

## Fillets
- Plates have sharp corners unless a fillet radius is specified or defined in the part spec.
