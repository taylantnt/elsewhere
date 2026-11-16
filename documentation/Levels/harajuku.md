# Harajuku: Takeshita Street

**Status:** built as a city row and as the second Message Hikari tour.

- **Solo label** — `city_row_harajuku` (`game/city_rows.rpy`).
- **Tour label** — `hikari_tour_harajuku` (`game/confidant_visits/hikari_tour.rpy`).
- **Hub name** — `Harajuku: Takeshita Street`.
- **Art** — `bg_harajuku` (the street), `bg_harajuku_clothes` (the kawaii shop),
  `bg_harajuku_candy` (the cotton candy shop). All three are real art on disk;
  the two shop backgrounds are sized explicitly in `script.rpy`.

## Tour

The second Message Hikari outing. She opens with the fashion rather than a
place: have you heard of kawaii style? He has not. She explains enough in the
texts to make him curious, then turns it into a walk because the street is the
point. Beats:

1. Text hook: 可愛い is not just "cute" — it is a way of dressing and a way of
   deciding what deserves attention. The weather is nice; meet at the station.
2. Takeshita Street: a quiet lane behind the station until the boutiques came.
   Hikari's rules — look with your eyes, say 可愛い when something deserves it,
   never laugh, buy nothing before the third shop.
3. The food street: crepes, タピオカ, and cotton candy in every colour.
4. A kawaii clothing shop: layers, socks over boots, one colour that should not
   work. She admits she dressed that way for a year. The assistant then pulls
   her into the fitting room; she comes out in the full outfit (the
   `sister_kawaii.png` portrait, selected by the `hikari_kawaii` flag), and he is
   speechless. She keeps the dress, ribbon, and socks on for the rest of the day.
5. A cotton candy shop (綿菓子 / wataame): pink flowers and blue hearts. He eats
   his; she eats hers before he can photograph it.
6. Home by train. At the door the ribbon is gone and she is in her own clothes
   again; she never mentions the dress afterward. The tour unlocks the solo hub
   row; Hikari does not come on later visits.

Six menus with one-time attribute rewards cover the street, the food, the
clothes, the fitting room, the candy, and the reason she brought him. Finishing
pays a final Insight tick. `test_hikari_tour_harajuku` in the console plays the
full tour.

## Solo scene

He walks the street alone with Hikari's rules still in his head. The clothes
shop is the one she told him to wait for; the assistant explains an outfit the
way she would explain a sentence. He buys socks with cats on them. At the candy
shop he gets the pink flower because Hikari would have taken the blue heart.

Four choices on the street (Nerve / Insight / Grace / Nerve), then two in the
clothes shop (Insight / Grace). No Hikari: the rules are his to keep or break.
The Fortune Teller's second card also names Harajuku as a hook for her later
appearance; the row does not stage her.
