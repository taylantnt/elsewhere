# Yokohama Chinatown

**Status:** built as a city row and as the first Message Hikari tour.

- **Solo label** — `city_row_yokohama` (`game/city_rows.rpy`).
- **Tour label** — `hikari_tour_yokohama` (`game/confidant_visits/hikari_tour.rpy`).
- **Hub name** — `Yokohama Chinatown`.
- **Art** — `bg_yokohama_chinatown`, `bg_yokohama_akarenga`, and two gyoza-shop
  drawings: `bg_gyoza_shop` (the room, used in both the tour and the solo visit)
  and `bg_gyoza_dishes` (the dish close-up when the food arrives). Lei Lei has three portraits
  selected by `lei_mood`: `lei_normal.png` (unimpressed), `lei_shout.png`
  (shouting), `lei_intense.png` (the room goes quiet).

## Tour

The first Message Hikari outing. Hikari is hungry, so the tour starts as a
dinner invitation and becomes a walk through the district. Beats:

1. Text hook: she is starving and offers the best gyoza in the city.
2. Chinatown gate: the 1859 port, the Chinese traders and cooks, the largest
   Chinatown in Japan, the people who still live above the shops.
3. Food street: jiaozi/gyoza, shoronpo, and Yokohama ramen (sanmamen).
4. A tiny gyoza shop run by Lei Lei, her family, and a great deal of shouting.
   Lei Lei and the family recognize Hikari from her seminar-trip visits and
   tease her about bringing a foreigner and about coming back every week.
   The family speaks Chinese; the player understands none of it and relies on
   Hikari (who understands none of the Chinese either). Lei Lei repeats the
   important lines in Japanese afterwards, so Hikari follows the second half
   and relays it to him. The kitchen banter carries a few shared Japanese words
   (電話, 蒸し器) that Hikari can pick up too.
5. Akarenga (the red brick warehouses): customs, cargo, the 1923 earthquake,
   and the version of Yokohama that faces the water.
6. Home by train. The tour unlocks the solo hub row; Hikari does not come on
   later visits.

Five choices cover the gate, the food street, ordering, the meal, and Akarenga.
Each pays a micro attribute reward once; finishing the tour pays a final
Insight tick. The dinner callback in `evening_templates.rpy` has a Yokohama
branch.

## Solo scene

Chinatown is ten minutes from the station and a hundred years from the rest of
the city. Red lanterns, gates with Chinese characters, steamed buns, lucky cats,
things made of sugar. A woman speaks to him in Chinese; he answers in Japanese;
she laughs and moves between Japanese and English.

The theme is the other foreigner: he is a foreigner in a district that is
foreign to the country it sits inside. That is a different kind of foreign.

Four choices in Chinatown:

- follow the smell of the steamed buns (Grace);
- ask a shopkeeper how long they have been here (Insight);
- get lost in the side streets (Nerve);
- go back to Lei Lei's gyoza shop — she recognizes him and 餃子 is not a
  question (Grace).

The walk then opens toward the water and Akarenga, with three more choices
(Nerve / Grace / Insight). Lei Lei's Japanese line 「また来たのか」 follows the
same rule as the tour: she says the important part in Japanese because he does
not understand Chinese.

## Simulation thread

The treatment keeps a sign that says WELCOME HOME in English. The built row
keeps the displacement without the explicit sign; the words can return in Act 3
when the leaks become structural.
