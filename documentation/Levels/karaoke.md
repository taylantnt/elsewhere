# Karaoke: Kuru Fuku Neko

**Status:** built as a city row and as the third Message Hikari tour.

- **Solo label** — `city_row_karaoke` (`game/city_rows.rpy`).
- **Tour label** — `hikari_tour_karaoke` (`game/confidant_visits/hikari_tour.rpy`).
- **Hub name** — `Karaoke Box`.
- **Art** — `bg_karaoke_outside` (the neon sign and cat over the door),
  `bg_karaoke_drink` (the drink bar), `bg_karaoke_room` (the box). All three are
  real art on disk, sized explicitly in `script.rpy`.

## Tour

The third Message Hikari outing. She has to stay after seminar to finish
something and gives him a reason to accept before he can refuse: she needs to
let something out tonight. She frames it as stress relief and as something to do
*with him*, not as a performance. Beats:

1. Text hook: "I hope you like singing. Or, better, that you like letting things
   out. I need to let something out tonight." He is shy; she says that is why she
   asked him and not somebody else: "You can be shy in a room with me."
2. Outside Kuru Fuku Neko (来る福猫 — "the cat that brings luck when it comes"):
   karaoke is a private room rented by the hour, not a stage. Cost by the hour
   plus drinks, or 飲み放題 / nomihōdai for a fixed-price flow. Costumes (cat
   ears, plastic glasses), 応援 / cheering sticks and maracas, soft drinks and
   free soft-serve, with water brought once the staff decide it is time.
3. The corridor: songs leaking from other rooms. She identifies a drama theme
   everybody knows, and a room where somebody is practising the same two lines —
   "the bravest room in this building." You can read a room from its song.
4. The drink bar: "Singing is exercise and nobody tells you that." Water first.
5. The room: the tablet, English support, the queue, the score. He selects
   English songs; she adds ones that matter to her (her mother's song, a summer
   she wanted to leave town, one she likes because it is stupid). He recognizes
   them from shops and train ads — "a city teaches you its songs."
6. The first song is his and he is terrible. She hits the cheering stick once,
   yells something in Japanese, and keeps singing when he laughs and loses the
   words. They get closer through the song.
7. Choosing a group song is an art: read the room, pick something everybody can
   join, lift the energy instead of spending it. He does not understand yet;
   she says he will notice the day he does it without thinking.
8. Home by train. The tour unlocks the solo hub row; Hikari does not come on
   later visits.

Five menus with one-time attribute rewards cover the street corner, the drink
bar, the tablet, her songs, and the group-song lesson. Finishing pays a final
Insight tick. `test_hikari_tour_karaoke` in the console plays the full tour.

## Solo scene

He comes back alone. Water first — that part he learned. He switches the
tablet between English and Japanese, then leaves it in Japanese, and uses the
ローマ字 / rōmaji setting so the lyrics come up in roman letters.

He is terrible, but he finishes the song. The second attempt is better and the
third is almost a song. On the way back he reads a room from the corridor for
ten seconds and realizes he can now tell what it is doing. Before he leaves he
queues one of the songs she sang with him — not for himself, but for the next
time somebody is in the room with him.

Three choices on the first pass (Nerve / Nerve / Insight), then three more
(Nerve / Insight / Grace).
