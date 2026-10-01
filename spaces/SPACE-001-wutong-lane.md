# Space Definition: Wutong Lane Commercial Street

## 1. Overview

| Attribute | Value |
|---|---|
| Space ID | `SPACE-001` |
| Name | Wutong Lane Commercial Street |
| Type | Pedestrian shopping street (outdoor) |
| Orientation | East–West |
| Total length | 200 m |
| Street width | 12 m (6 m central walkway, 3 m covered arcade on each side) |
| Coordinate system | Origin (0, 0) at the midpoint of the west entrance; x-axis points east, y-axis points north; unit: meters |
| Operating hours | 10:00 – 22:00 |

## 2. Zones

| Zone ID | Name | x range | Description |
|---|---|---|---|
| `Z-W` | West Entrance Plaza | -10 ~ 0 | Entrance arch, directory sign, bike-share parking |
| `Z-A` | Dining Zone | 0 ~ 80 | Mainly restaurants and drinks |
| `Z-C` | Central Plaza | 80 ~ 120 | Fountain, benches, pop-up market stalls |
| `Z-B` | Retail Zone | 120 ~ 200 | Clothing, books, everyday goods |
| `Z-E` | East Entrance | 200 ~ 210 | Connects to the subway station exit |

## 3. Floor Plan

```
                 North shops (y = 6 ~ 18)
   ┌───────┬───────┬───────┬────────────┬───────┬───────┬───────┐
   │ N-01  │ N-02  │ N-03  │            │ N-04  │ N-05  │ N-06  │
   │Noodles│Coffee │Bakery │            │ Books │Apparel│Flowers│
 W ├───────┴───────┴───────┤  Central   ├───────┴───────┴───────┤ E
 E │       Walkway         │   Plaza    │       Walkway         │ A
 S │                       │ ◎ Fountain │                       │ S
 T ├───────┬───────┬───────┤            ├───────┬───────┬───────┤ T
   │ S-01  │ S-02  │ S-03  │            │ S-04  │ S-05  │ S-06  │
   │BubTea │HotPot │ Conv. │            │Home   │Optical│Station│
   └───────┴───────┴───────┴────────────┴───────┴───────┴───────┘
                 South shops (y = -18 ~ -6)
  x=0                     x=80         x=120                  x=200
```

## 4. Shops

### North Side (y = 6 ~ 18)

| Shop ID | Name | Category | x range | Area | Floors | Hours | Status |
|---|---|---|---|---|---|---|---|
| `N-01` | Old Street Beef Noodles | Dining / Chinese fast food | 0 ~ 25 | 300 m² | 1F | 07:00 – 21:00 | Open |
| `N-02` | Hillside Coffee | Drinks / Coffee | 25 ~ 50 | 300 m² | 1–2F | 08:00 – 22:00 | Open |
| `N-03` | Wheatfield Bakery | Dining / Bread & desserts | 50 ~ 80 | 360 m² | 1F | 09:00 – 21:00 | Open |
| `N-04` | Page Turner Books | Retail / Books & gifts | 120 ~ 150 | 360 m² | 1–2F | 10:00 – 22:00 | Open |
| `N-05` | Plain Linen Apparel | Retail / Clothing | 150 ~ 175 | 300 m² | 1F | 10:00 – 22:00 | Open |
| `N-06` | Little Bloom Florist | Retail / Flowers | 175 ~ 200 | 300 m² | 1F | 09:00 – 20:00 | Under renovation |

### South Side (y = -18 ~ -6)

| Shop ID | Name | Category | x range | Area | Floors | Hours | Status |
|---|---|---|---|---|---|---|---|
| `S-01` | Tea Talk | Drinks / Bubble tea | 0 ~ 20 | 240 m² | 1F | 10:00 – 22:00 | Open |
| `S-02` | Sichuan Flavor Hot Pot | Dining / Hot pot | 20 ~ 55 | 420 m² | 1–2F | 11:00 – 23:00 | Open |
| `S-03` | Neighborhood Mart | Retail / Convenience store | 55 ~ 80 | 300 m² | 1F | 24 hours | Open |
| `S-04` | Daily Goods Store | Retail / Home & living | 120 ~ 145 | 300 m² | 1F | 10:00 – 21:00 | Open |
| `S-05` | Clear View Optical | Retail / Eyewear | 145 ~ 170 | 300 m² | 1F | 10:00 – 21:00 | Open |
| `S-06` | Ink Dot Stationery | Retail / Stationery | 170 ~ 200 | 360 m² | 1F | 10:00 – 21:00 | Vacant, for lease |

## 5. Public Facilities

| Facility ID | Name | Coordinates (x, y) | Notes |
|---|---|---|---|
| `F-01` | Fountain | (100, 0) | Landmark of the Central Plaza |
| `F-02` | Public restrooms | (100, -10) | South side of the Central Plaza |
| `F-03` | Directory signs | (-5, 0) / (205, 0) | One at each entrance |
| `F-04` | Benches | Around the Central Plaza | 12 sets in total |
| `F-05` | Recycling stations | (40, 0) / (160, 0) | Center of the walkway |

## 6. Rules

- No motor vehicles on the walkway. Delivery vehicles may enter only through the east entrance, 06:00 – 09:00.
- Outdoor displays and seating must stay within the covered arcade (no more than 3 m from the shopfront).
- The Central Plaza hosts a pop-up market on weekends; the operator assigns all stalls.
- Shops are adjacent when their x ranges touch. A north shop and a south shop with the same x range face each other.
