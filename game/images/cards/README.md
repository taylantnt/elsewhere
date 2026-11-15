# Memory card faces

Commissioned tarot-style card art, cropped to one PNG per card from the two
6×3 sheets. The card back is still `../ui/memory/memory_card_back.png`.

The first-night memory board (`build_first_day_memory_deck` in
`game/script.rpy`) uses these as full card faces: each PNG already contains its
own border, numeral and title, so the screen draws it in place of the old
frame-and-caption face.

## Wired into the first-day deck

Each pair keeps its story id and picks one of its own cards at deck-build time,
so both copies of a pair always match but a replay can deal different art.

| Pair | Cards |
| :--- | :--- |
| `station` | `platform`, `train`, `gate`, `clock` |
| `student_id` | `student`, `lecture`, `notebook`, `phone` |
| `alley` (ramen route) | `alley`, `vending`, `rain`, `moon` |
| `ramen_shop` | `ramen`, `lantern` |
| `ramen_bowl` | `bowl` |
| `chef` | `chef` |
| `river` (Hikari route) | `river` |
| `running` | `run` |
| `kitchen` | `kitchen`, `table`, `tea` |
| `home_wait` | `home`, `family`, `bicycle`, `house` |
| `club` (photo route) | `circle`, `camera` |
| `sim` | `mentor` |
| `campus` | `campus` |
| `club_hall` | `print` |

## Reserved for later decks

These six belong to other confidants or the dream, so they are not part of the
first-day board yet:

`bar`, `cafe`, `dream`, `fortune`, `reader`, `sister`
