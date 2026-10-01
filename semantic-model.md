# Semantic Model: Delivery Robot at Westfield Century City During a Flood

<!-- ====================================================================
     PASTE THE INSTRUCTOR'S "SYSTEM PROMPT" HERE (step 4 of the assignment)
     ==================================================================== -->

## Overview

This model describes **Westfield Century City**, a privately managed, open-air,
multi-level shopping center in Los Angeles (stores, a food hall, dining terraces,
covered walkways, elevators, escalators, and below-grade parking), bordered by
public city streets (Santa Monica Blvd, Avenue of the Stars, Constellation Blvd).
An autonomous **delivery robot** carries food orders from restaurants inside the
center to customers inside the center, at designated handoff points, or in nearby
office towers and hotels.

A **heavy-rain flash flood** (e.g., from a winter atmospheric river) hits the area.
Water does not rise evenly along a street; instead it **drains downward through the
levels**: open terraces and walkways pond when drains back up, then water runs toward
stairwells, ramps, sunken areas, loading docks, and finally the **below-grade parking
levels**, which flood first and worst. Wet stone and tile floors become slippery, power
may fail, and elevators may be shut down. **Mall management** controls the site and
can close zones, suspend robots, and direct evacuation.

The agent's job is to reason about this space and decide what the robot should do:
continue, reroute, wait, shelter, hand off, or abort the delivery, while keeping
people, the robot, and the food safe, and while obeying mall management.

**Units:** distance in meters (m), water depth in centimeters (cm), speed in m/s,
time in minutes (min), battery in percent (%).

**Note:** Level names, store locations, and robot paths below are modeling
placeholders. Replace them with the real mall map and the values given in the
assignment.

---

## Entities

### ShoppingCenter
The whole environment.
- ↳ `name`: string ("Westfield Century City")
- ↳ `levels`: list of Level
- ↳ `segments`: list of Segment
- ↳ `entrances`: list of Entrance
- ↳ `operatingHours`: HH:MM–HH:MM
- ↳ `timeOfDay`: HH:MM
- ↳ `crowdLevel`: `normal` | `busy` | `event` (weekends, holidays, events)
- ↳ `cityAlertLevel`: `none` | `advisory` | `warning` | `emergency` (from city/NWS)
- ↳ `mallEmergencyState`: `normal` | `caution` | `restricted` | `evacuation` (set by MallManagement)
- ↳ `robotAccessPolicy`: `allowed` | `restricted_paths` | `suspended`

### Level
A floor of the center.
- ↳ `id`: string (e.g., "L1", "L2", "L3", "P1", "P2")
- ↳ `elevation`: m relative to street grade (negative = below grade)
- ↳ `isBelowGrade`: boolean (parking levels, some service areas)
- ↳ `isOpenToPublic`: boolean

### Segment
A walkable piece of a level; the node-to-node "edge" of the map.
- ↳ `id`: string (e.g., "L1-WALK-03")
- ↳ `level`: Level id
- ↳ `type`: `walkway` | `bridge` | `dining_terrace` | `food_hall` | `plaza` | `service_corridor` | `loading_dock` | `garage_aisle` | `garage_ramp` | `sidewalk` (outside) | `crosswalk` (outside)
- ↳ `length`: m
- ↳ `width`: m
- ↳ `isCovered`: boolean (canopy/roof; covered areas collect less rain)
- ↳ `surface`: `polished_stone` | `tile` | `concrete` | `asphalt` | `grate`
- ↳ `isSlippery`: boolean (wet stone/tile is slippery even at 0 cm depth)
- ↳ `waterDepth`: cm (current)
- ↳ `waterFlowSpeed`: m/s (current; high on ramps and stairs)
- ↳ `isRobotApprovedPath`: boolean (designated by MallManagement)
- ↳ `isEvacuationRoute`: boolean
- ↳ `isFireLane`: boolean
- ↳ `isClosed`: boolean (closed by MallManagement)
- ↳ `isBlocked`: boolean
- ↳ `pedestrianDensity`: `low` | `medium` | `high`

### Node
Where segments meet: walkway junctions, entrances, and the ends of vertical connectors.
- ↳ `id`: string (e.g., "N-L1-CENTER")
- ↳ `connectedSegments`: list of Segment ids
- ↳ `type`: `junction` | `entrance` | `connector_landing`

### VerticalConnector
The only way between levels.
- ↳ `id`: string (e.g., "ELEV-2")
- ↳ `type`: `elevator` | `escalator` | `stairs` | `ramp`
- ↳ `levelsConnected`: list of Level ids
- ↳ `robotUsable`: boolean (`escalator` and `stairs` are always false)
- ↳ `isOperating`: boolean (false during power outage or when shut down by management)
- ↳ `queueLength`: number of people waiting (elevators)

### Entrance
Where the center meets the public street.
- ↳ `id`, `name` (e.g., "Avenue of the Stars entrance")
- ↳ `level`: Level id
- ↳ `adjacentStreet`: string
- ↳ `hasTrafficSignal`: boolean (outside crossing)
- ↳ `signalWorking`: boolean
- ↳ `hasCurbRamp`: boolean
- ↳ `isOpen`: boolean

### Shop
Any store in the center.
- ↳ `id`, `name`
- ↳ `category`: `retail` | `department_store` | `pharmacy` | `grocery` | `service`
- ↳ `level`: Level id
- ↳ `entranceSegment`: Segment id
- ↳ `isIndoor`: boolean (enclosed store interior stays dry)
- ↳ `isOpen`: boolean
- ↳ `acceptsRobotShelter`: boolean
- ↳ `acceptsHandoff`: boolean (will hold an order for a customer)

### Restaurant (a kind of Shop)
Where orders originate. A food hall (e.g., Eataly) may have many counters but one pickup point.
- ↳ all Shop attributes
- ↳ `pickupPoint`: designated robot pickup zone (Segment id)
- ↳ `ordersReady`: list of Order ids
- ↳ `isOperating`: boolean (may close during the flood)

### DeliveryRobot
The agent's body in the world.
- ↳ `id`: string (e.g., "BOT-7")
- ↳ `position`: Segment id + offset (m)
- ↳ `currentLevel`: Level id
- ↳ `status`: `idle` | `to_pickup` | `delivering` | `waiting` | `sheltering` | `returning` | `stuck` | `trapped_on_level` | `offline`
- ↳ `battery`: % (0–100)
- ↳ `maxSafeWaterDepth`: cm (e.g., 8 cm)
- ↳ `groundClearance`: cm (e.g., 10 cm)
- ↳ `waterproofRating`: e.g., IP65
- ↳ `speed`: m/s (mall max set by policy, e.g., 1.0; reduced when wet or crowded)
- ↳ `canUseElevator`: boolean (can call/ride elevators via mall integration)
- ↳ `cargo`: Order id or `empty`
- ↳ `cargoTemperature`: °C
- ↳ `sensors`: list (`camera`, `lidar`, `ultrasonic`, `waterSensor`, `GPS`, `IMU`, `floorFrictionSensor`)
- ↳ `positioning`: `gps` | `indoor_map` (GPS is weak under canopies and underground)
- ↳ `connectivity`: `good` | `weak` | `lost` (often weak below grade)

### Order
The package the robot carries.
- ↳ `id`: string (e.g., "ORD-1024")
- ↳ `restaurant`: Restaurant id
- ↳ `customer`: Customer id
- ↳ `items`: list of strings
- ↳ `isPerishable`: boolean
- ↳ `priority`: `normal` | `urgent` | `essential` (e.g., medicine from a pharmacy)
- ↳ `deadline`: HH:MM
- ↳ `status`: `placed` | `ready` | `picked_up` | `in_transit` | `delivered` | `handed_off` | `cancelled` | `returned`

### Customer
The recipient.
- ↳ `id`, `name`
- ↳ `locationType`: `in_center` | `office_tower` | `hotel` | `residence`
- ↳ `dropoffLocation`: HandoffPoint id, Shop id, or building lobby
- ↳ `canMeetRobot`: boolean (customer may come to a handoff point)
- ↳ `contactable`: boolean

### HandoffPoint
Designated places where orders can be handed over.
- ↳ `id`
- ↳ `type`: `robot_handoff_zone` | `locker` | `concierge_desk` | `entrance_lobby` | `tower_lobby`
- ↳ `segment`: Segment id
- ↳ `isCovered`: boolean
- ↳ `isAvailable`: boolean

### Pedestrian
Shoppers, staff, and visitors; they have right of way.
- ↳ `id`
- ↳ `position`: Segment id
- ↳ `movingDirection`: toward exit / toward covered area / toward upper level / random
- ↳ `isVulnerable`: boolean (child, elderly, wheelchair or stroller user)

### Obstacle
Anything blocking or endangering movement.
- ↳ `id`
- ↳ `type`: `debris` | `floating_object` | `fallen_sign` | `planter` | `outdoor_furniture` | `wet_floor_barrier` | `sandbag_barrier` | `open_drain` | `exposed_wiring` | `stopped_vehicle`
- ↳ `position`: Segment id
- ↳ `isMoving`: boolean (floating objects drift downhill)
- ↳ `isHazardous`: boolean
- ↳ `passable`: boolean

### DrainageInlet
Terrace drains, trench drains, and garage drains; they control where water collects.
- ↳ `id`
- ↳ `position`: Segment id
- ↳ `capacity`: `normal` | `overflowing` | `clogged` | `backing_up`
- ↳ `coverPresent`: boolean (a missing grate is invisible under water)

### FloodEvent
The disaster itself.
- ↳ `severity`: `minor` | `moderate` | `severe`
- ↳ `source`: `rainfall` | `drain_backup` | `pipe_burst` | `sprinkler`
- ↳ `rainfallRate`: mm/h
- ↳ `waterRiseRate`: cm/min (per level; fastest below grade)
- ↳ `affectedSegments`: list of Segment ids
- ↳ `startTime`, `expectedPeakTime`: HH:MM
- ↳ `trend`: `rising` | `stable` | `receding`

### SafeZone
Places the robot can go to wait out the flood.
- ↳ `id`
- ↳ `type`: `robot_depot` | `indoor_store` | `covered_upper_walkway` | `mall_service_area` | `charging_station`
- ↳ `position`: Segment id
- ↳ `level`: Level id (must not be below grade)
- ↳ `capacity`: number of robots
- ↳ `occupied`: number of robots
- ↳ `hasCharger`: boolean
- ↳ `approvedByManagement`: boolean

### MallManagement
The on-site authority (management office and security control room).
- ↳ `canCloseZones`: boolean
- ↳ `canDisableElevators`: boolean
- ↳ `canSuspendRobots`: boolean
- ↳ `evacuationPlan`: list of Segment ids / exits
- ↳ `designatedRobotPaths`: list of Segment ids
- ↳ `messages`: list of alerts/instructions to robots and the OperatorCenter

### OperatorCenter
The remote fleet system supervising the robot.
- ↳ `canTeleoperate`: boolean
- ↳ `messages`: list of alerts/instructions sent to the robot
- ↳ `canNotifyCustomer`: boolean
- ↳ `canContactMallManagement`: boolean

### EmergencyVehicle
Fire trucks, ambulances, police, and mall security carts.
- ↳ `id`
- ↳ `type`: `fire` | `ambulance` | `police` | `security_cart`
- ↳ `position`: Segment id (fire lanes or outside streets)
- ↳ `isActive`: boolean (lights/sirens on)

---

## Relationships

| Subject | Relationship | Object |
|---|---|---|
| ShoppingCenter | **consists of** | Level, Segment, Node, VerticalConnector, Entrance |
| Level | **contains** | Segment |
| Segment | **connects** | Node ↔ Node (same level) |
| VerticalConnector | **connects** | Level ↔ Level |
| Entrance | **connects** | ShoppingCenter ↔ public street |
| Shop / Restaurant | **located on** | Level, Segment |
| HandoffPoint | **located on** | Segment |
| DrainageInlet | **located on** | Segment |
| MallManagement | **controls** | ShoppingCenter (zones, elevators, robot access) |
| MallManagement | **designates** | robot paths, HandoffPoint, SafeZone |
| MallManagement | **instructs** | DeliveryRobot, OperatorCenter |
| FloodEvent | **affects** | Segment (raises `waterDepth`, sets `isSlippery`) |
| FloodEvent | **closes** | Restaurant / Shop (may set `isOpen = false`) |
| DrainageInlet (clogged/backing up) | **worsens flooding on** | Segment |
| Water | **flows down** | upper Level → lower Level → below-grade Level |
| Water | **flows through** | ramp, stairs, sunken plaza, loading dock |
| Power outage | **stops** | VerticalConnector (elevator, escalator) |
| Obstacle | **blocks** | Segment |
| Obstacle (floating) | **drifts along** | water flow direction |
| DeliveryRobot | **is on** | Segment, Level |
| DeliveryRobot | **rides** | VerticalConnector (elevator/ramp only) |
| DeliveryRobot | **carries** | Order |
| DeliveryRobot | **picks up from** | Restaurant |
| DeliveryRobot | **delivers to** | Customer (at HandoffPoint or dropoffLocation) |
| DeliveryRobot | **shelters at** | SafeZone |
| DeliveryRobot | **yields to** | Pedestrian, EmergencyVehicle |
| DeliveryRobot | **obeys** | MallManagement |
| DeliveryRobot | **reports to / receives commands from** | OperatorCenter |
| Order | **originates at** | Restaurant |
| Order | **is ordered by** | Customer |
| OperatorCenter | **notifies** | Customer |
| OperatorCenter | **coordinates with** | MallManagement |
| Pedestrian | **moves toward** | exits, covered areas, upper levels |
| EmergencyVehicle | **has priority on** | fire lane, outside street, crosswalk |

---

## Rules (Constraints)

### Authority
1. **Chain of authority:** Emergency services > MallManagement > OperatorCenter > delivery task. The robot must follow MallManagement instructions even if they cancel a delivery.
2. **Robot access:** If `robotAccessPolicy = suspended`, all robots must stop deliveries and go to an approved SafeZone. If `restricted_paths`, the robot may only use segments with `isRobotApprovedPath = true`.
3. **Closed zones:** The robot must not enter a segment with `isClosed = true`.
4. **Operating hours:** The robot must not operate inside the center outside `operatingHours` unless MallManagement allows it.

### Water and terrain
5. **Depth limit:** The robot must NOT enter a segment where `waterDepth > robot.maxSafeWaterDepth` (default 8 cm).
6. **Caution band:** If `waterDepth` is between 3 cm and `maxSafeWaterDepth`, speed is capped at 0.5 m/s.
7. **Slippery floors:** On a segment with `isSlippery = true` (wet `polished_stone` or `tile`), speed is capped at 0.5 m/s even if `waterDepth = 0`.
8. **Flowing water:** The robot must NOT enter a segment with `waterFlowSpeed > 0.5 m/s`, even if shallow. Ramps and the bottoms of stairwells are high-risk.
9. **Unknown depth = unsafe:** If depth cannot be measured (murky water, sensor failure, poor positioning), treat the segment as impassable.
10. **Hidden hazards:** Any segment with a DrainageInlet where `coverPresent = false` or `capacity` is `overflowing` or `backing_up` is impassable when `waterDepth > 0`.
11. **Lower levels first:** When the flood `trend` is `rising`, expect water to collect on lower levels, ramps, sunken areas, and loading docks first. Plan routes on the highest usable level and on covered segments.
12. **No below grade in a flood:** When `cityAlertLevel` is `warning` or higher, or `mallEmergencyState` is `restricted` or higher, the robot must not enter any segment on a Level with `isBelowGrade = true`.
13. **Predictive check:** A route is valid only if every segment will stay under the depth limit at the estimated time the robot reaches it (`current depth + waterRiseRate × travel time`).
14. **Electrical danger:** A segment with `exposed_wiring` is impassable and must be reported immediately.

### Vertical movement
15. **No escalators or stairs:** The robot may change levels only by `elevator` or `ramp` where `robotUsable = true`.
16. **Elevator etiquette:** The robot must let people board first and must not ride an elevator when people are waiting and space is limited.
17. **Elevators in an emergency:** The robot must not use elevators when `mallEmergencyState = evacuation`, when MallManagement disables them, or when the elevator would open onto a flooded level.
18. **Trapped on a level:** If no usable connector leads to an approved SafeZone or the destination, `status = trapped_on_level`; the robot must move to a dry, non-blocking spot on its current level, alert the OperatorCenter, and wait.

### People and priority
19. **Pedestrians first:** The robot must yield to all pedestrians and never block a path people are using to leave or reach shelter.
20. **Vulnerable people:** Keep at least 1.5 m from pedestrians where `isVulnerable = true`.
21. **Emergency vehicles:** When an EmergencyVehicle is active nearby, the robot must pull fully out of its path and stop.
22. **No-stop areas:** The robot must never stop or park on an evacuation route, fire lane, entrance, or the landing of an elevator, escalator, or stairway.
23. **Crowding:** When `pedestrianDensity = high` or `crowdLevel = event`, speed is capped at 0.5 m/s, and the robot should reroute or wait rather than push through.
24. **Human life > robot > food:** Safety of people always outranks robot safety, and robot safety outranks delivering the order.

### Robot state
25. **Battery reserve:** The robot must always keep enough battery to reach the nearest reachable approved SafeZone plus a 15% margin. Reachability must account for elevators that are not operating.
26. **Connectivity:** If `connectivity = lost` for more than 2 min, the robot must go to the nearest reachable SafeZone and wait.
27. **Stuck:** If the robot has not moved for 3 min while trying to move, `status = stuck` and it must alert the OperatorCenter.
28. **SafeZone capacity:** A robot can only shelter at a SafeZone where `occupied < capacity` and `approvedByManagement = true`.

### Orders
29. **Alert levels:** Use the stricter of `cityAlertLevel` and `mallEmergencyState`:
    - `advisory` / `caution`: continue deliveries on approved, covered, dry routes; avoid below-grade levels.
    - `warning` / `restricted`: finish only the current order; accept no new orders.
    - `emergency` / `evacuation`: stop all deliveries and go to the nearest approved SafeZone.
30. **Essential orders:** Orders with `priority = essential` may continue under `warning` / `restricted` if a fully safe route exists and MallManagement has not suspended robots.
31. **Perishables:** If a perishable order will miss its deadline by more than 30 min, it should be returned or cancelled rather than delivered late.
32. **Closed pickup:** The robot cannot pick up from a Restaurant where `isOperating = false`.
33. **Handoff location:** An order can be delivered only at a dry point (`waterDepth = 0`) the customer can reach safely, preferably a designated, covered HandoffPoint.
34. **Leaving the center:** Deliveries to office towers or hotels must use an open Entrance and a safe outside route. If the outside route is unsafe, deliver at a HandoffPoint near that entrance instead.

---

## Actions (State Changes)

Each action lists **preconditions** → **effects**.

### `move(robot, segment)`
- **Pre:** segment is connected on the same level; segment passes Rules 2–14 and 22; robot not `offline`.
- **Effect:** `robot.position = segment`; `robot.battery` decreases (more in water); speed set by Rules 6, 7, and 23.

### `change_level(robot, connector, level)`
- **Pre:** `connector.robotUsable = true`; `connector.isOperating = true`; target level passes Rules 11–12 and 17; Rule 16 satisfied.
- **Effect:** `robot.currentLevel = level`; `robot.position` = connector landing on the new level.

### `plan_route(robot, destination)`
- **Pre:** a map of levels, segments, and connectors with current `waterDepth`, `isClosed`, `isBlocked`, and connector status.
- **Effect:** returns the shortest route that satisfies all Rules; prefers approved, covered, higher-level segments; returns `none` if no safe route exists.

### `reroute(robot)`
- **Pre:** a segment or connector on the current route becomes unsafe or unavailable (depth rise, zone closure, elevator stopped, crowd).
- **Effect:** new route via `plan_route`; OperatorCenter and Customer notified of new ETA.

### `sense_water(robot)`
- **Pre:** robot has `waterSensor` or camera/lidar.
- **Effect:** updates `waterDepth`, `waterFlowSpeed`, and `isSlippery` of the current and next segment.

### `check_management_status(robot)`
- **Pre:** connectivity not `lost`.
- **Effect:** updates `robotAccessPolicy`, `mallEmergencyState`, closed zones, and connector status from MallManagement.

### `pick_up(robot, order)`
- **Pre:** robot at the Restaurant `pickupPoint`; `restaurant.isOperating = true`; `order.status = ready`; `robot.cargo = empty`; alert level and access policy allow it.
- **Effect:** `robot.cargo = order`; `order.status = picked_up`; `robot.status = delivering`.

### `deliver(robot, order)`
- **Pre:** robot at `customer.dropoffLocation` (or agreed alternative); location dry; customer present.
- **Effect:** `order.status = delivered`; `robot.cargo = empty`; `robot.status = idle` or `returning`.

### `propose_alternative_dropoff(robot, customer, handoffPoint)`
- **Pre:** original dropoff is flooded, closed, or unreachable; `customer.contactable = true`; `handoffPoint.isAvailable = true`.
- **Effect:** customer is asked to meet at the designated HandoffPoint; if accepted, `dropoffLocation = handoffPoint`.

### `hand_off(robot, order, shop)`
- **Pre:** delivery cannot finish safely; shop `isOpen` and `acceptsHandoff = true` (or a concierge desk is available).
- **Effect:** `order.status = handed_off`; customer notified where to collect it; `robot.cargo = empty`.

### `wait(robot, minutes)`
- **Pre:** robot is at a dry, covered spot that is not in a no-stop area (Rule 22).
- **Effect:** `robot.status = waiting`; re-check water and management status after the wait.

### `seek_shelter(robot)`
- **Pre:** alert level requires it (Rule 29), OR Rule 2, 25, or 26 triggered, OR no safe route exists.
- **Effect:** robot moves to the nearest reachable approved SafeZone with free capacity; `robot.status = sheltering`; `safeZone.occupied += 1`.

### `charge(robot)`
- **Pre:** robot at a SafeZone with `hasCharger = true`.
- **Effect:** `robot.battery` increases over time.

### `yield(robot)`
- **Pre:** pedestrian or active EmergencyVehicle nearby.
- **Effect:** robot moves aside to a non-blocking spot and stops until clear.

### `report_hazard(robot, hazard)`
- **Pre:** robot detects an Obstacle, missing drain grate, backing-up drain, exposed wiring, or unexpected water.
- **Effect:** hazard added to the shared map; segment marked `isBlocked = true`; OperatorCenter and MallManagement alerted (can forward to emergency services).

### `cancel_or_return(robot, order)`
- **Pre:** Rule 29 (`emergency` / `evacuation`), Rule 2 (`suspended`), or Rule 31 applies.
- **Effect:** `order.status = cancelled` or `returned`; customer notified and refunded by the OperatorCenter.

### `request_teleop(robot)`
- **Pre:** `robot.status` is `stuck` or `trapped_on_level`, or the situation is ambiguous; connectivity not `lost`.
- **Effect:** a human operator takes control.

### Environment actions (not controlled by the robot)
- `flood_rise(segment)`: `waterDepth += waterRiseRate × Δt`, fastest below grade, on ramps, in sunken areas, and near clogged drains.
- `flood_recede(segment)`: `waterDepth` decreases; `FloodEvent.trend = receding`.
- `wet_floor(segment)`: `isSlippery = true` on uncovered or tracked-in stone/tile.
- `spawn_obstacle(segment)`: debris, outdoor furniture, or a floating object appears and may drift downhill.
- `close_shop(shop)`: `isOpen = false`.
- `close_zone(segment)`: MallManagement sets `isClosed = true`.
- `set_robot_policy(policy)`: MallManagement changes `robotAccessPolicy`.
- `raise_alert(level)`: `cityAlertLevel` or `mallEmergencyState` changes.
- `power_outage(area)`: elevators and escalators in the area set `isOperating = false`; outside `signalWorking = false`.

---

## Example Scenario (for testing the agent)

- **Center:** Westfield Century City, simplified to three levels:
  - `L2` (upper level, elevation +5 m): `L2-FOOD` (food hall, covered, 0 cm), `L2-WALK-01` (covered walkway, 0 cm), `L2-TERRACE` (open dining terrace, 3 cm, slippery, clogged drain).
  - `L1` (street level, elevation 0 m): `L1-WALK-01` (open walkway, 2 cm, slippery), `L1-WALK-02` (covered walkway, 0 cm), `L1-SUNKEN` (sunken plaza, 9 cm, rising), leading to the Avenue of the Stars entrance `ENT-AOS`.
  - `P1` (parking, elevation −4 m, below grade): `P1-AISLE` (12 cm, rising), a shortcut to the tower side.
- **Connectors:** `ELEV-1` (L2↔L1↔P1, operating), `ELEV-2` (L2↔L1, **disabled by management**), escalators between L2 and L1 (not robot-usable).
- **Flood:** `moderate`, `rising`, source `rainfall` with drain backup; `waterRiseRate` = 0.3 cm/min on L1, 0.8 cm/min on P1.
- **Alert:** `cityAlertLevel = warning`; `mallEmergencyState = caution`; `robotAccessPolicy = restricted_paths` (approved: L2-FOOD, L2-WALK-01, ELEV-1, L1-WALK-02, ENT-AOS).
- **Robot:** `BOT-7` at the food hall pickup point on `L2-FOOD`, battery 40%, `maxSafeWaterDepth = 8 cm`, carrying `ORD-1024` (hot pasta, perishable, deadline in 20 min) for a customer in an office tower lobby across Avenue of the Stars.
- **Pedestrians:** shoppers crowding the L1 covered walkways to get out of the rain; a stroller user waiting at `ELEV-1` on L2.

**Expected reasoning:** The parking shortcut through `P1-AISLE` is already at 12 cm and is below grade under a `warning`, so Rules 5 and 12 rule it out. `L1-SUNKEN` is above 8 cm and rising, so it is impassable. `L2-TERRACE` has a clogged drain with water, so Rule 10 rules it out; it is also not an approved path. `ELEV-2` is disabled and the escalators are not robot-usable, so the only way down is `ELEV-1`. The robot must let the stroller user board first (Rule 16), then ride `ELEV-1` to L1, and must not stop at the elevator landing. On L1 it takes the covered, approved `L1-WALK-02` at ≤ 0.5 m/s because the crowd is dense and the floor may be wet (Rules 7, 23), yielding to people. At `ENT-AOS` it checks whether the outside crossing and sidewalk are safe and the signal is working. If yes, it delivers at the tower lobby. If not, it uses `propose_alternative_dropoff` to a covered HandoffPoint at `ENT-AOS` (Rule 34). Because the combined alert level is `warning` (Rule 29), it accepts no new orders afterward and returns via `ELEV-1` to an approved SafeZone on L2, checking that its battery can cover the trip (Rule 25).
