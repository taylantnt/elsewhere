# Missing Backgrounds Reference

**Purpose:** A checklist of background PNGs that need to be created. The game
runs fine without them (colored placeholder with text label shows), but these
are the ones visually missing.

**How backgrounds work:**
- `bg_or_placeholder("bg_name", "#color", "LABEL")` — auto-loads `bg_name.png`
  if present, else shows a colored placeholder. **Safe to ship without the PNG.**
- `Transform("images/backgrounds/bg_name.png", ...)` — requires the PNG to
  exist or the game errors. **All of these already have their PNGs.**

---

## Missing PNGs (19) — currently showing placeholder

### Shimokitazawa tour (4)
| PNG needed | Placeholder label | Used in |
|---|---|---|
| `bg_shimokitazawa.png` | SHIMOKITAZAWA / SMALL THEATERS | Hikari tour |
| `bg_record_shop.png` | USED RECORDS / CRATES | Shimokitazawa |
| `bg_live_house.png` | LIVE HOUSE / THE DOOR LIKE A FRIDGE | Shimokitazawa |
| `bg_shimokiti_cafe.png` | COFFEE / SHIMOKITI | Shimokitazawa |

### Ueno tour (2)
| PNG needed | Placeholder label | Used in |
|---|---|---|
| `bg_ueno.png` | UENO PARK / APRIL | Hikari tour |
| `bg_ueno_museum.png` | TOKYO NATIONAL MUSEUM / THE STEPS | Hikari tour |

### Golden Week / Nakameguro (1)
| PNG needed | Placeholder label | Used in |
|---|---|---|
| `bg_nakameguro.png` | NAKAMEGURO / THE CANAL | Day 26 (late blossoms) |

### Shibuya (1)
| PNG needed | Placeholder label | Used in |
|---|---|---|
| `bg_shibuya.png` | SHIBUYA / SCRAMBLE CROSSING | Day 33 |

**Note:** `bg_shibuya_day.png` and `bg_shibuya_dusk.png` already exist on
disk. If you want to reuse one of those instead of making a new PNG, the
definition can be rewired to point at the existing file.

### Common days (1)
| PNG needed | Placeholder label | Used in |
|---|---|---|
| `bg_shrine.png` | A SMALL SHRINE / THE STEPS | Common days (temizu echo Day 42) |

### Days 46-50 arc (10) — the entire end-of-build trip runs on placeholder
| PNG needed | Placeholder label | Used in |
|---|---|---|
| `bg_tsukiji_dawn.png` | TSUKIJI / BEFORE DAWN | Day 46 |
| `bg_tsukiji_stalls.png` | TSUKIJI / THE LANES | Day 46 |
| `bg_kamakura_station.png` | KAMAKURA / THE STATION | Day 47 |
| `bg_kamakura_daibutsu.png` | KAMAKURA / THE GREAT BUDDHA | Day 47 |
| `bg_enoden.png` | THE ENODEN / LITTLE GREEN TRAIN | Day 47 |
| `bg_kamakura_shore.png` | KAMAKURA / THE SHORE | Day 47 |
| `bg_sento_outside.png` | THE SENTO / BLUE CURTAIN | Day 48 |
| `bg_sento_bath.png` | THE SENTO / STEAM AND TILE | Day 48 |
| `bg_ajisai_temple.png` | HYDRANGEA GARDEN / IN THE RAIN | Day 49 |
| `bg_river_fireflies.png` | THE RIVER / FIREFLIES | Day 50 |

---

## Recommended additional backgrounds (5)

These are moments where the dialogue describes a distinct visual but the
screen stays on the current background. A new background would let the beat
land harder:

1. **`bg_shibuya_hikarie_roof`** — Day 33. The free rooftop of Shibuya
   Hikarie where Hikari takes MC to see the city from above. Currently uses
   `bg_shibuya_day` / `bg_shibuya_dusk`. The rooftop view (looking down at
   the scramble crossing) is the emotional beat of that day.

2. **`bg_daibutsu_face`** — Day 47 Kamakura. The Daibutsu up close. If MC
   sees the face, that deserves its own frame rather than staying on the
   station/shore background.

3. **`bg_sento_mural`** — Day 48. The tiled mural above the sento bath
   (often Mt. Fuji). `bg_sento_bath` covers the room, but the mural is the
   detail that would elevate it.

4. **`bg_mikoshi`** — Day 18 matsuri. The portable shrine carried by men in
   happi coats is the visual climax of the festival.

5. **`bg_kitchen_rain`** — Act 3 (tsuyu). The kitchen window in rain is the
   recurring domestic image of Act 3. A rain version of the kitchen (or a
   rain-on-window overlay) would anchor the season change.

---

## File location

All background PNGs go in:
```
game/images/backgrounds/
```

The naming convention is `bg_<name>.png` (lowercase, underscores). The
`bg_or_placeholder` call looks for exactly `bg_<name>.png` in that folder.
