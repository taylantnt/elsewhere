# Night Run — Hikari Progression Summary

Hikari's arc is not one of the five confidant chains. It is the recurring river
run: seven after-school beats that run parallel to the confidant arcs and are
tracked by `hikari_visits` and `sister_affection`. The run is the one place she
is not the host sister, not the translator, not the person who knows where
everything is. It is the one place she is allowed to be tired.

The first run is written in `after_school_run` (`game/script.rpy`); visits 2–7
live in `game/hikari.rpy`. The hub's **Walk home with Hikari** row
(`walk_hikari`) routes through `confidant_visit_hikari`, which plays the next
run or falls back to the ordinary walk home (`afternoon_walk_hikari`) when the
first run was skipped or the chain is finished.

## The Seven Beats

1. **The first run** — `after_school_run` — he cannot keep up, and she invites
   him anyway. The run is her daily thing, and she lets him see it.
2. **The route** — `hikari_visit_02` — she knows every vending machine, every
   crack in the path. She runs it the way the chef makes ramen: from memory,
   without thinking. She admits she needs it, not just likes it.
3. **The evening he keeps up** — `hikari_visit_03` — he matches her pace for ten
   minutes, and she is surprised enough to say so. What it costs her is that he
   sees her face when she is not performing.
4. **The night neither of them says anything** — `hikari_visit_04` — they run,
   they stop, they drink from the vending machine, and they walk home in
   silence. She admits she does not know where the performance ends.
5. **The rain** — `hikari_visit_05` — the bridge in the rain, the amado, and the
   first true thing she says about the house. She asks whether the street looks
   right to him. The answer can confirm the unease or try to smooth it over;
   either way she has said it out loud.
6. **The part of the river she keeps** — `hikari_visit_06` — she takes him to a
   place he has never seen, where a vending machine with no cable still hums.
   She says she comes here when the house feels too small. She says it is not
   the house; it is the thing she is running from.
7. **The last run** — `hikari_visit_07` — she is faster than she has ever been,
   and he cannot keep up. At the second bridge she asks: *don't you ever feel
   like we've done this before?* She asks him to remember a promise: if she ever
   asks him to run somewhere that isn't home, say yes. The scene ends on the
   question, not the answer. The reveal belongs to Act 3/4.

## Emotional Shape

The run moves from **being allowed to watch** (1–2) to **being allowed to stay**
(3–4) to **being told the truth** (5–6) to **being asked to choose** (7). Hikari
does not get warmer or colder; she gets more specific. The horror comes from the
reader recognizing the seams, never from Hikari being sinister. She never says
the word "simulation." She says the amado sounds wrong, the street looks wrong,
and she has done this before.

The final run is deliberately the shortest-feeling and the fastest. She runs
ahead; he loses sight of her; she is waiting at the bridge. The last line she
says is not a confession. It is an instruction: *Race you back.* The promise is
left where he can find it.

## State And Routing

| State | Written by | Read by |
| :--- | :--- | :--- |
| `hikari_visits` | `after_school_run` (1), `hikari_visit_02`–`07` | `confidant_visit_hikari`, WIRE progress |
| `sister_affection` | every run (`add_affection("sister", …)`) | affection helpers and later scenes |
| `hikari_run_finished` | `hikari_visit_07` | Act 3/4 threshold, future scenes |
| `last_afternoon_was_run` | each run (set), `free_afternoon` and `afternoon_walk_hikari` (cleared) | the Day 7 dinner branch |

`confidant_visit_hikari` dispatches on `hikari_visits`: `0` falls back to the
ordinary walk, `1`–`6` play visits 2–7, and `7` falls back to the ordinary walk.
The run does not touch `confidant_visits`, so it does not affect the confidant
caps or the "all confidants met" gate.

## Rewards

Each run has two 3-option menus, one option per attribute at micro (0.2). The
close rewards rotate Grace (v2), Insight (v3), Nerve (v4), Grace (v5), Insight
(v6), and Insight small (0.5, v7). The final small close marks the recognition
beat as the last run. The twelve menus are M61–M66 in
`attribute_rewards_checklist.md`.

## Current Build

Only visit 2 is reachable now: the first run is the Day 2 afternoon fork, and
the Day 7 hub is the first hub day. Visits 3–7 are written and wired, waiting
for later hub days. The ordinary walk home remains available after visit 7, so
the Hikari row never runs out of something to do.
