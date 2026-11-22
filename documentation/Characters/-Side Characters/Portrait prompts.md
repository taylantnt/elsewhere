# Portrait prompts

The art direction for **every** Elsewhere character is the permanent master template in
[`master_character_art_prompt.md`](../../master_character_art_prompt.md). Sections 1–8 of that
file are kept **identical** for every character. Only the two character-specific fields are
replaced:

- `[INSERT CHARACTER DESCRIPTION HERE]` — section 2, Character Identity
- `[INSERT POSE AND EXPRESSION HERE]` — section 5, Pose and Expression

So a complete image prompt is: master sections 1–8, verbatim, with the two fields below
substituted. The full text of those two fields is recorded here so a portrait can be
regenerated exactly, without re-deriving the character from dialogue.

All portraits are generated as isolated characters on a **genuinely transparent** background
(PNG, RGBA, 1024×1536, exact 2:3). Always verify the exported PNG's mode and alpha channel
after generation — do not trust a checkerboard preview or a prompt that merely claims
transparency.

---

## Generated and wired

These eight were generated earlier and are now wired as side images in `game/script.rpy`.
Their original prompts were not saved at the time; the file → tag → `Character()` mapping is
recorded below instead.

| File | Tag | `Character()` definition | Character |
| :--- | :--- | :--- | :--- |
| `riku.png` | `riku` | `confidant_visits/sim.rpy` | Riku — quiet Circle member, designs the exhibition labels |
| `rika.png` | `rika` | `confidant_visits/sim.rpy` | Rika — the theatrical Circle model |
| `womansuit.png` | `woman` | `confidant_visits/chef.rpy` | The woman in a suit during the ramen-shop lunch rush |
| `wei.png` | `wei` | `confidant_visits/murakami.rpy` | Wei — China. Reads kanji, cannot read kana. Certain he understands. |
| `priya.png` | `priya` | `confidant_visits/murakami.rpy` | Priya — India. Asks the questions nobody else thinks to ask. |
| `oliver.png` | `oliver` | `confidant_visits/murakami.rpy` | Oliver — England. Treats every custom like a puzzle with a punchline. |
| `prakash.png` | `prakash` | `confidant_visits/murakami.rpy` | Prakash — Nepal. Quiet until he is not. Then devastating. |
| `saman.png` | `saman` | `confidant_visits/murakami.rpy` | Saman — Sri Lanka. Studies anime Japanese. Speaks like a documentary. |

`Prakash.png` was renamed to lowercase `prakash.png` for case-sensitive (Linux) builds.

---

## Pending generation — Kenta

Target file `game/images/characters/kenta.png`, tag `kenta`, `Character()` definition in
`confidant_visits/chef.rpy`. Based on the apprentice introduced in chef visits 6–7.

**Section 2 — Character Identity:**

> Kenta (健太) is a young Japanese man in his early twenties, the nervous new apprentice at a
> narrow neighbourhood ramen shop in modern Japan. He has been learning for only three weeks
> and watches his middle-aged chef mentor with terrified reverence. He bows too deeply and too
> quickly, carries a small notebook everywhere in a handwriting that is shaky and unsure, and
> is currently learning to chop green onions with the correct rhythm. He is eager, earnest and
> anxious, desperate to get everything right but constantly afraid he is getting it wrong. He
> follows the chef around with the notebook ready, trying to write down instinct. He is clearly
> distinct from his gruff middle-aged mentor: younger, softly boyish but clearly adult, anxious
> rather than stern. He has a slim build, short slightly messy dark brown hair that falls a
> little over his forehead, warm brown eyes, and an open, nervous face.
>
> He wears a clean but slightly oversized dark navy apprentice apron over a simple off-white
> t-shirt and dark trousers, sleeves rolled up, with a thin white cloth tied around his head and
> a pen tucked into the apron pocket.

**Section 5 — Pose and Expression:**

> Kenta stands slightly hunched forward with nervous energy, clutching a small worn notebook
> against his chest with both hands, a pen tucked into his apron pocket. His shoulders are
> lifted a little and his posture is almost a bow, eager and apologetic but still standing
> upright. His expression is anxious yet eager: wide, uncertain eyes, slightly parted lips, and
> a nervous, uncertain half-smile, as if he is hoping he has done the right thing. Not an
> exaggerated anime expression — a quiet, human nervousness.

---

## Pending generation — Student 1 (anxious exchange student, ramen shop)

Target file `game/images/characters/student1.png`, tag `student1`, `Character()` definition in
`confidant_visits/chef.rpy`. This is **not** the library regular — `quietstudent.png` belongs to
the reading-room regular in Hana's scenes. Based on chef visit 3.

**Section 2 — Character Identity:**

> An exchange student in a modern Japanese ramen shop: a young woman in her early twenties,
> foreign, and completely unable to read the Japanese menu. She is anxious and cautious,
> overwhelmed by the unfamiliar characters and the busy shop, and keeps glancing to her friend
> for reassurance. She says things like "I don't know what any of this says — just point at
> something?" and "What if I point at the wrong thing?" She has shoulder-length wavy dark
> auburn hair, hazel eyes, light tan skin, and a soft, uncertain face. She is a visitor, slightly
> out of her depth, but curious. She must look clearly distinct from her confident, easygoing
> friend who is also in the shop.
>
> She wears a casual oversized cream hooded sweatshirt over a simple t-shirt, faded blue jeans,
> and comfortable sneakers, with a small crossbody bag. The clothes are practical travel
> clothes with believable fabric folds.

**Section 5 — Pose and Expression:**

> She stands leaning slightly forward, holding a ramen shop paper menu in both hands in front
> of her, studying it with a furrowed brow. Her shoulders are raised and her posture is
> defensive and uncertain; she glances sideways toward her friend for help. Her expression is
> anxious and uncertain — raised eyebrows, a small worried frown, slightly parted lips — not a
> generic exaggerated anime emotion.

---

## Pending generation — Student 2 (confident exchange student, ramen shop)

Target file `game/images/characters/student2.png`, tag `student2`, `Character()` definition in
`confidant_visits/chef.rpy`. Based on chef visit 3.

**Section 2 — Character Identity:**

> An exchange student in a modern Japanese ramen shop: a young man in his early twenties,
> foreign, confident and relaxed. He has been here before and treats the incomprehensible
> Japanese menu as a joke — "That's what I did last time. It worked." and "Then you learn
> something about yourself." He is easygoing, a little cocky but warm, the friend who reassures
> the anxious one. He has short-cropped curly dark hair, warm brown skin, a strong jaw and a
> ready, easy grin, and a taller, more solid build than his anxious friend. He must look clearly
> distinct from that friend.
>
> He wears a casual dark olive bomber jacket over a simple graphic t-shirt, dark straight-leg
> jeans and sneakers, with a phone in one pocket. Believable fabric, stitching and construction.

**Section 5 — Pose and Expression:**

> He stands relaxed with his weight on one leg, one hand lifted in a casual "trust me" gesture
> and the other tucked into a pocket. His posture is open and confident, the opposite of his
> anxious friend. His expression is a confident, easy, slightly cheeky grin — warm and
> reassuring rather than smug, and not an exaggerated anime expression.

---

## Wiring checklist (once the three images exist)

1. Verify each new PNG is RGBA, 1024×1536, with a real alpha channel (min 0, max 255).
2. Add `image side <tag> = At(Transform(...), portrait_idle)` lines in `game/script.rpy`.
3. Add `image="<tag>"` to the matching `Character()` definitions in `confidant_visits/chef.rpy`.
4. Add `kenta`, `student1`, `student2` to the `_standing` twin loop in `game/script.rpy`.
5. Step through chef visit 3 and visits 6–7 in Ren'Py to confirm the portraits load.
