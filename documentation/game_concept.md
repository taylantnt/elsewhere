# Game Concept: The Simulation of Harmony (Working Title)

## Overview
A psychological thriller visual novel with mini-games, disguised as a slice-of-life experience of a foreign student in Japan.

## Core Premise
The player takes on the role of a foreign student arriving in Tokyo. The initial experience focuses on the struggles of living in a foreign country: language barriers, social navigation, and everyday survival. However, the game gradually reveals a darker truth: the player is actually in a government-funded simulation designed to test if foreigners can successfully assimilate into a future Japanese society facing a population crisis.

## Key Themes
- **Assimilation vs. Identity**: The struggle to fit into a society that values harmony over individuality.
- **Reality vs. Simulation**: The psychological toll of living in a manufactured world.
- **Isolation and Connection**: Building relationships in a space where communication is a hurdle.

## Core Mechanics
- **Visual Novel Dialogues**: Choice-based progression. Conversations are two-way: the player answers, and the answers are what develop the character. Once he has answered someone, that answer is what comes back the next time he talks to them — a conversation is not a menu that re-rolls.
- **Character Attributes (Insight / Grace / Nerve)**: Three Pillars of progression, each with its own colour (blue, green, red). Points are **scarce**: most answers pay nothing, and only a genuine turning point awards anything. What does accrue collects into ranks that unlock or close dialogue. Fully specified in `character_attributes.md`.
- **Character Memory**: Important characters remember what he said to them, marked on screen with a short `(Hikari will remember that)` notice. It is kept separately from the attribute system: an answer can cost nothing and still matter later.
- **Language Progression System**: Japanese text starts as plain, unreadable text and gradually "translates" into coloured English as the player's fluency increases.
- **Social Links (Confidants)**: Planned, not yet built. When they arrive they should *feed* the attribute system rather than run beside it. See `game_structure.md` §7.
- **Money & Inventory**: A thin wallet and a Bag. Everyday survival is a resource puzzle.
- **Mini-Games**: Small puzzles integrated into daily tasks (e.g., navigating the train system, reconstructing the day in the dream).
- **Dream Sequences**: Horror-themed interludes that foreshadow the reality of the simulation, and the memory-reconstruction mini-game that lives inside them.

## The Big Twist
The player is a test subject in a medicine-induced coma within a facility. The "Host Sister" is actually a programmer of the simulation who is trying to help the player escape or realize the truth.

## Multiple Endings
1. **The Escape**: Realize the truth and escape the facility with the sister's help.
2. **The Blue Pill**: Reject the truth and choose to live in the comfortable simulation.
3. **Failure**: The simulation ends prematurely; the subject is deemed unfit for assimilation and wakes up to a harsh reality.
