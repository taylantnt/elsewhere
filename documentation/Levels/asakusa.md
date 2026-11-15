# Asakusa

**Status:** built.

- **Day 12** — `sunday_practice` (`game/days/day_12_sunday.rpy`): the temple
  visit with Murakami. Kaminarimon, Nakamise, the incense, the omikuji, and the
  low stone wall where she asks the question the week has been building to.
- **Day 13** — `monday_asakusa` (`game/days/day_13_monday.rpy`): the same old
  city with Hikari. Kaminarimon and its two guardians (Raijin's drums, Fūjin's
  bag), Nakamise, ningyo-yaki, the smoke, the omikuji rack, and the Fortune
  Teller's folding table.
- **Hub row** — `confidant_visit_fortune` (`game/city_rows.rpy`): the return
  visit that turns the Fortune Teller's second and third cards and closes her
  three-card arc.

## Scene spine

1. The gate is a threshold, not a photo. Raijin and Fūjin guard the approach,
   not the temple.
2. Nakamise is a funnel: the sacred and the snack stand in the same street.
3. The incense burner is a crowd agreeing to do the same small thing.
4. The omikuji is read against the protagonist's attributes. Grace > Nerve is a
   good slip, Nerve > Grace is a bad one, a tie is mixed.
5. The Fortune Teller turns the gate, the white corridor, and the figure on the
   table. The corridor card triggers the Day 9 genkan flashback and Hikari's
   admission that she saw it too.

## Cast

- **Hikari** — the guide who makes the old city fun instead of solemn.
- **Murakami** — the guide who makes it mean something.
- **The Fortune Teller** — the oracle at the edge of the crowd.

## Art

- Real: `bg_asakusa_kaminarimon.png`, `bg_asakusa_inside.png`,
  `bg_asakusa_kuji.png`, `bg_asakusa_smoke.png`.
- Placeholder: `bg_fortune_stall` (`ASAKUSA / FORTUNE STALL`).

## State written

`fortune_teller_met`, `fortune_arc_started`, `fortune_result`, and
`confidant_visits["fortune"]` (1 after Day 13, 3 after the hub return).
