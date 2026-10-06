"""L2 footfall analysis for thermal-comfort prioritisation.

Reads the weekday entrance footfall export (工作日各出入口) and ranks the
L2 entrances / connections by footfall, so thermal-comfort effort can be
weighted towards the busiest points.

Usage:
    python analysis/l2_footfall/l2_footfall.py [path/to/export.xlsx]

Outputs (next to this script, in out/):
    l2_entrances.csv   one row per L2 counter, ranked, with shares and tier
    l2_by_zone.csv     L2 footfall per zone (A/B/C/D)
    floors.csv         building-wide footfall per floor, for context
"""
import csv
import re
import sys
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE / "data" / "weekday_entrance_footfall.xlsx"
OUT = HERE / "out"

# Counter types, inferred from the entrance name.
# connection: link passage / bridge to a neighbouring building or plaza (envelope boundary)
# vertical:   escalator / lift lobby arriving from another floor (internal, stack-effect zone)
VERTICAL = ("扶梯", "电梯")


def load(path):
    ws = openpyxl.load_workbook(path, data_only=True).active
    rows = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r or r[1] is None:
            continue
        rows.append({
            "name": r[1],
            "floor_src": r[2],
            "trips": int(r[3]),    # 客流(人次)
            "people": int(r[4]),   # 客流(人数)
            # "-" marks zone totals and counters excluded from the mall total
            "in_total": r[5] != "-",
        })
    return rows


def floor_of(row):
    # Several C区 counters are named "L2" but tagged L1 in the export; trust the name.
    return "L2" if "L2" in row["name"] else row["floor_src"]


def tier(share):
    if share >= 0.10:
        return 1
    if share >= 0.02:
        return 2
    return 3


def main(path):
    rows = [r for r in load(path) if r["in_total"]]
    for r in rows:
        r["floor"] = floor_of(r)
        r["zone"] = r["name"][0]

    mall_trips = sum(r["trips"] for r in rows)
    l2 = sorted((r for r in rows if r["floor"] == "L2"), key=lambda r: -r["trips"])
    l2_trips = sum(r["trips"] for r in l2)

    OUT.mkdir(exist_ok=True)
    cum = 0
    with open(OUT / "l2_entrances.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["rank", "name", "zone", "type", "floor_in_export", "trips", "people",
                    "trips_per_person", "share_of_L2", "cumulative_share", "share_of_mall", "tier"])
        for i, r in enumerate(l2, 1):
            share = r["trips"] / l2_trips
            cum += share
            kind = "vertical" if any(k in r["name"] for k in VERTICAL) else "connection"
            ratio = r["trips"] / r["people"] if r["people"] else 0
            w.writerow([i, r["name"], r["zone"], kind, r["floor_src"], r["trips"], r["people"],
                        f"{ratio:.2f}", f"{share:.4f}", f"{cum:.4f}",
                        f"{r['trips'] / mall_trips:.4f}", tier(share)])
            print(f"{i:>2} {r['name']:<24} {r['trips']:>6} {share:6.1%} cum {cum:6.1%}  T{tier(share)}  {kind}")

    zones = {}
    for r in l2:
        zones[r["zone"]] = zones.get(r["zone"], 0) + r["trips"]
    with open(OUT / "l2_by_zone.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["zone", "trips", "share_of_L2"])
        for z in sorted(zones):
            w.writerow([z, zones[z], f"{zones[z] / l2_trips:.4f}"])

    floors = {}
    for r in rows:
        floors[r["floor"]] = floors.get(r["floor"], 0) + r["trips"]
    with open(OUT / "floors.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["floor", "trips", "share_of_mall"])
        for fl, t in sorted(floors.items(), key=lambda kv: -kv[1]):
            w.writerow([fl, t, f"{t / mall_trips:.4f}"])

    print(f"\nL2 total {l2_trips} trips = {l2_trips / mall_trips:.1%} of mall ({mall_trips})")
    print("By zone:", {z: f"{t} ({t / l2_trips:.1%})" for z, t in sorted(zones.items())})


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT)
