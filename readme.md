# Riverside Distance Lab

An environment simulation of a small riverside town: walls, buildings, a river with two bridges, ten named places and eight occupants who walk between them.

Open `index.html` in a browser. No build step and no dependencies.

## Distance metrics

| Metric | Formula | What it ignores |
|---|---|---|
| Straight line (Euclidean) | `√(Δx² + Δy²)` | walls and water |
| City block (Manhattan) | `|Δx| + |Δy|` | walls and water; diagonals |
| Walking path (bonus) | shortest route via Dijkstra, 8 directions, diagonal = √2, no corner cutting | nothing; it goes around obstacles |

One grid cell is 10 m.

## What the simulation shows

- **Distance between two locations or two occupants** for each metric. Pick From/To in the dropdowns or click the map. A selected occupant is tracked live as they walk.
- **Visual comparison**: all three routes are drawn on the map, a bar chart compares their lengths, and a heatmap shows the distance field from the "From" point (circles for Euclidean, diamonds for Manhattan, bent fronts around walls for walking).
- **Far by one metric, close by another**: the scatter plot puts every place and occupant at (straight-line, walking). Anything in the shaded zone is at least 2× farther on foot than in a straight line, and the panel names the worst cases. It also flags when the straight line is blocked by a wall or the river.

Good examples: Library → Café (separated by the garden wall), Boathouse → Pier (straight across the river).
