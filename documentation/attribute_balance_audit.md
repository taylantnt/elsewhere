# Attribute Balance Audit — Elsewhere

Scope: all active `reward_attributes_once` calls in `game/script.rpy`, `game/chef.rpy`, `game/sim.rpy`, `game/aya.rpy`, `game/hana.rpy`, and `game/orson.rpy`, through the end of Day 6 (`monday_lecture`). Excluded: `game/quiz.rpy` L23 (commented out), `attribute_test_rank_up` (L592, dev shortcut), and the archived board in `dream_archive.rpy` L430.

Reward sizes: tiny = 0.1, micro = 0.2, micro_loss = -0.2, nudge = 0.3, small = 0.5, medium = 1.0. Rank thresholds (cumulative): 0 / 2 / 5 / 9.5 / 15.

## Complete reward-call table

### `game/script.rpy`

| Line | Flag | Reward |
|---:|---|---|
| **Airport (Day 1)** | | |
| 2070 | `answer_security_bow` | Grace tiny (0.1) |
| 2077 | `answer_security_press` | Nerve tiny (0.1) |
| 2130 | `answer_timid_listen` | Insight micro (0.2) |
| 2161 | `answer_woman_smile` | Grace micro (0.2) |
| 2168 | `answer_woman_echo` | Grace micro (0.2) |
| 2229 | `answer_assistant_patient` | Insight micro (0.2) |
| 2279 | `veteran_advice_decline` | Insight micro (0.2) |
| 2301 | `information_seeker` | Grace tiny (0.1) |
| 2311 | `plant_determination` | Nerve tiny (0.1) |
| **Travel (Day 1)** | | |
| 2362 | `travel_route_attribute` | Insight small (0.5) |
| 2377 | `travel_route_attribute` | Nerve medium (1.0) |
| 2381 | `travel_route_attribute` | Insight small (0.5) |
| 2437 | `answer_taxi_fare` | Nerve small (0.5) |
| 2540 | `answer_train_gate` | Nerve nudge (0.3) |
| 2601 | `answer_ticket_ask` | Grace micro (0.2) |
| 2637 | `answer_train_express` | Insight micro (0.2) |
| **Home arrival / boxes (Day 1 night)** | | |
| 2804 | `answer_boxes_reassure` | Grace nudge (0.3) |
| 2813 | `answer_boxes_postpone` | Grace micro_loss (-0.2) |
| **Day 2 morning / university** | | |
| 3124 | `answer_breakfast_questions` | Nerve micro_loss (-0.2) |
| 3134 | `answer_breakfast_emails` | Grace small (0.5) |
| 3404 | `answer_courtyard_buildings` | Insight micro (0.2) |
| 3466 | `answer_wall_cat` | Insight micro (0.2) |
| 3551 | `answer_circles_back` | Grace micro (0.2) |
| 3654 | `answer_clock_ask` | Grace micro_loss (-0.2) |
| 3693 | `answer_hikari_warning` | Nerve small (0.5), Grace micro_loss (-0.2) |
| **Day 2 afternoon: walk_alone** | | |
| 3840 | `answer_ramen_recommendation` | Nerve small (0.5) |
| 3862 | `answer_ramen_broth` | Insight nudge (0.3) |
| 3888 | `chef_first_umai` | Grace small (0.5) |
| 3892 | `chef_first_umai` | Grace small (0.5) |
| 3949 | `walk_first_found` | Insight small (0.5) |
| **Day 2 afternoon: walk_hikari (run)** | | |
| 4017 | `answer_run_thanks` | Grace nudge (0.3) |
| 4021 | `answer_run_history` | Insight nudge (0.3) |
| 4039 | `answer_run_join` | Nerve micro (0.2) |
| 4103 | `answer_river_quiet` | Grace small (0.5) |
| 4136 | `run_first_river` | Nerve small (0.5) |
| **Day 2 afternoon: photo_club** | | |
| 4246 | `answer_circle_join` | Nerve small (0.5) |
| 4276 | `sim_circle_first` | Insight small (0.5) |
| 4308 | `answer_circle_help` | Grace small (0.5) |
| 4353 | `photo_first_session` | Grace small (0.5) |
| **Day 2 dinner / night** | | |
| 4942 | `first_dinner_declined` | Grace micro_loss (-0.2) |
| 4948 | `first_dinner_covered` | Grace small (0.5) |
| 4965 | `first_dinner_natto` | Nerve micro (0.2) |
| 4976 | `first_dinner_neighborhood` | Insight micro (0.2) |
| 4986 | `first_dinner_apology` | Grace micro (0.2) |
| 5062 | `first_night_hikari_thanks` | Grace micro (0.2) |
| 5069 | `first_night_hikari_observation` | Insight micro (0.2) |
| 5074 | `first_night_hikari_promise` | Nerve micro (0.2) |
| 5118 | `first_night_memory_pairs` | Insight nudge (0.3) |
| **Day 3: second school day** | | |
| 5256 | `answer_left` | Insight nudge (0.3) |
| 5307 | `haiku_lesson_notes` | Insight nudge (0.3) |
| 5311 | `haiku_lesson_listen` | Insight nudge (0.3) |
| 5315 | `haiku_lesson_research` | Nerve nudge (0.3) |
| 5369 | `cellular_plan_modest` | Insight micro (0.2) |
| 5373 | `cellular_plan_usage` | Nerve micro (0.2) |
| 5377 | `cellular_plan_student_rate` | Grace micro (0.2) |
| 5394 | `cellular_plan_total` | Insight micro (0.2) |
| 5398 | `cellular_plan_basic` | Grace micro (0.2) |
| 5402 | `cellular_plan_decline_extras` | Nerve micro (0.2) |
| 5458 | `akihabara_explore_arcades` | Nerve micro (0.2) |
| 5462 | `akihabara_explore_cameras` | Insight micro (0.2) |
| 5466 | `akihabara_explore_crowd` | Grace micro (0.2) |
| 5483 | `akihabara_maid_cafe_cautious` | Grace micro (0.2) |
| 5487 | `akihabara_maid_cafe_curiosity` | Nerve micro (0.2) |
| 5491 | `akihabara_maid_cafe_questions` | Insight micro (0.2) |
| 5525 | `maid_cafe_understand_options` | Insight micro (0.2) |
| 5530 | `maid_cafe_admit_nerves` | Nerve micro (0.2) |
| 5535 | `maid_cafe_thank_aya` | Grace micro (0.2) |
| 5544 | `maid_cafe_first_recommendation` | Grace micro (0.2) |
| 5549 | `maid_cafe_first_independent_order` | Nerve micro (0.2) |
| 5555 | `maid_cafe_first_popular_order` | Insight micro (0.2) |
| 5574 | `maid_cafe_join_spell` | Nerve micro (0.2) |
| 5582 | `maid_cafe_watch_spell` | Grace micro (0.2) |
| 5728 | `night_table_total` | Insight micro (0.2) |
| 5733 | `night_table_plain` | Grace micro (0.2) |
| 5742 | `night_table_boundary` | Nerve micro (0.2) |
| 5754 | `night_table_nerve` | Nerve micro (0.2) |
| 5830 | `night_weekend_study` | Insight micro (0.2) |
| 5867 | `night_room_library_promise` | Insight micro (0.2) |
| 5874 | `night_room_study_plan` | Grace micro (0.2) |
| 5882 | `night_room_tease` | Grace micro (0.2) |
| **Day 4: Saturday library / Hana / Orson** | | |
| 6068 | `library_errand_docs` | Insight micro (0.2) |
| 6110 | `reading_club_first` | Grace micro (0.2) |
| 6182 | `lupins_den_thanks` | Grace micro (0.2) |
| 6204 | `lupins_den_first` | Nerve micro (0.2) |
| **Day 5: Sunday quiz** | | |
| 6320 | `sunday_quiz_q1` | Insight micro (0.2) |
| 6336 | `sunday_quiz_q2` | Insight micro (0.2) |
| 6354 | `sunday_quiz_q3` | Insight micro (0.2) |
| **Day 6: Monday quiz** | | |
| 6519 | `monday_quiz_q1` | Insight micro (0.2) |
| 6535 | `monday_quiz_q2` | Insight micro (0.2) |
| 6550 | `monday_quiz_q3` | Insight micro (0.2) |

### `game/chef.rpy`

| Line | Flag | Reward |
|---:|---|---|
| **Chef visit 2** | | |
| 68 | `chef_visit_02_ask` | Insight micro (0.2) |
| 77 | `chef_visit_02_watch` | Grace micro (0.2) |
| 84 | `chef_visit_02_thank` | Nerve micro (0.2) |
| 113 | `chef_visit_02_close` | Grace micro (0.2) |
| **Chef visit 3** | | |
| 145 | `chef_visit_03_help` | Grace small (0.5) |
| 149 | `chef_visit_03_watch` | Insight micro (0.2) |
| 156 | `chef_visit_03_recommend` | Nerve micro (0.2) |
| 175 | `chef_visit_03_humble` | Grace micro (0.2) |
| 182 | `chef_visit_03_share` | Insight micro (0.2) |
| 189 | `chef_visit_03_understand` | Insight small (0.5) |
| 204 | `chef_visit_03_close` | Grace small (0.5) |
| **Chef visit 4** | | |
| 237 | `chef_visit_04_change` | Insight micro (0.2) |
| 244 | `chef_visit_04_improve` | Insight small (0.5) |
| 251 | `chef_visit_04_time` | Grace small (0.5) |
| 269 | `chef_visit_04_texture` | Insight micro (0.2) |
| 276 | `chef_visit_04_temp` | Insight micro (0.2) |
| 283 | `chef_visit_04_perfect` | Grace small (0.5) |
| 301 | `chef_visit_04_close` | Grace small (0.5) |
| **Chef visit 5** | | |
| 336 | `chef_visit_05_introduce` | Grace small (0.5) |
| 340 | `chef_visit_05_discover` | Insight micro (0.2) |
| 347 | `chef_visit_05_tell` | Nerve micro (0.2) |
| 368 | `chef_visit_05_help` | Grace micro (0.2) |
| 375 | `chef_visit_05_hard` | Insight micro (0.2) |
| 382 | `chef_visit_05_retire` | Insight small (0.5) |
| 397 | `chef_visit_05_close` | Grace small (0.5) |
| **Chef visit 6** | | |
| 429 | `chef_visit_06_learn` | Insight micro (0.2) |
| 435 | `chef_visit_06_work` | Insight micro (0.2) |
| 441 | `chef_visit_06_time` | Grace small (0.5) |
| 458 | `chef_visit_06_forget` | Insight small (0.5) |
| 462 | `chef_visit_06_watch` | Grace micro (0.2) |
| 469 | `chef_visit_06_explain` | Insight small (0.5) |
| 499 | `chef_visit_06_close` | Grace small (0.5) |
| **Chef visit 7** | | |
| 536 | `chef_visit_07_good` | Grace small (0.5) |
| 543 | `chef_visit_07_time` | Insight micro (0.2) |
| 550 | `chef_visit_07_honest` | Grace small (0.5) |
| 574 | `chef_visit_07_refuse` | Grace small (0.5) |
| 581 | `chef_visit_07_promise` | Grace small (0.5) |
| 588 | `chef_visit_07_meaning` | Insight small (0.5) |
| 617 | `chef_visit_07_why` | Insight small (0.5) |
| 624 | `chef_visit_07_kenta` | Grace micro (0.2) |
| 631 | `chef_visit_07_stay` | Nerve micro (0.2) |
| 651 | `chef_visit_07_close` | Grace small (0.5) |
| **Chef closed** | | |
| 674 | `chef_visit_closed_leave` | Grace micro (0.2) |
| 677 | `chef_visit_closed_message` | Nerve micro (0.2) |
| 680 | `chef_visit_closed_sit` | Insight micro (0.2) |
| 690 | `chef_visit_closed_close` | Grace small (0.5) |

### `game/sim.rpy`

| Line | Flag | Reward |
|---:|---|---|
| **Sim visit 2** | | |
| 60 | `sim_visit_02_manual` | Insight micro (0.2) |
| 64 | `sim_visit_02_time` | Nerve micro (0.2) |
| 98 | `sim_visit_02_close` | Grace micro (0.2) |
| **Sim visit 3** | | |
| 132 | `sim_visit_03_decide` | Nerve micro (0.2) |
| 136 | `sim_visit_03_wait` | Grace micro (0.2) |
| 140 | `sim_visit_03_frame` | Insight micro (0.2) |
| 186 | `sim_visit_03_close` | Grace small (0.5) |
| **Sim visit 4** | | |
| 218 | `sim_visit_04_collective` | Grace small (0.5) |
| 222 | `sim_visit_04_choice` | Insight micro (0.2) |
| 253 | `sim_visit_04_commit` | Nerve small (0.5) |
| 257 | `sim_visit_04_fear` | Grace micro (0.2) |
| 275 | `sim_visit_04_close` | Grace small (0.5) |
| **Sim visit 5** | | |
| 311 | `sim_visit_05_honest` | Insight micro (0.2) |
| 315 | `sim_visit_05_real` | Grace small (0.5) |
| 344 | `sim_visit_05_close` | Grace small (0.5) |
| **Sim visit 6** | | |
| 374 | `sim_visit_06_validate` | Grace small (0.5) |
| 379 | `sim_visit_06_future` | Insight micro (0.2) |
| 383 | `sim_visit_06_fear` | Nerve micro (0.2) |
| 403 | `sim_visit_06_room` | Grace small (0.5) |
| 407 | `sim_visit_06_time` | Nerve micro (0.2) |
| 425 | `sim_visit_06_close` | Grace small (0.5) |
| **Sim visit 7** | | |
| 465 | `sim_visit_07_accept` | Grace small (0.5) |
| 469 | `sim_visit_07_stay` | Grace micro_loss (-0.2) |
| 473 | `sim_visit_07_carry` | Insight small (0.5) |
| 501 | `sim_visit_07_promise` | Grace small (0.5) |
| 505 | `sim_visit_07_meaning` | Grace small (0.5) |
| 509 | `sim_visit_07_future` | Nerve micro (0.2) |
| 523 | `sim_visit_07_close` | Grace small (0.5) |

### `game/aya.rpy`

| Line | Flag | Reward |
|---:|---|---|
| **Aya visit 2** | | |
| 63 | `aya_visit_02_same` | Grace micro (0.2) |
| 67 | `aya_visit_02_surprise` | Nerve micro (0.2) |
| 72 | `aya_visit_02_recommend` | Grace micro (0.2) |
| 86 | `aya_visit_02_lonely` | Insight micro (0.2) |
| 91 | `aya_visit_02_travel` | Nerve micro (0.2) |
| 95 | `aya_visit_02_picked` | Grace micro (0.2) |
| 105 | `aya_visit_02_art_surprise` | Nerve micro (0.2) |
| 109 | `aya_visit_02_art_same` | Grace micro (0.2) |
| 139 | `aya_visit_02_silly` | Grace micro (0.2) |
| 143 | `aya_visit_02_smile` | Grace micro (0.2) |
| 147 | `aya_visit_02_time` | Insight micro (0.2) |
| 159 | `aya_visit_02_close` | Grace small (0.5) |
| **Aya visit 3** | | |
| 189 | `aya_visit_03_how` | Grace micro (0.2) |
| 193 | `aya_visit_03_self` | Insight micro (0.2) |
| 197 | `aya_visit_03_exhausting` | Nerve micro (0.2) |
| 209 | `aya_visit_03_tried` | Insight micro (0.2) |
| 213 | `aya_visit_03_alive` | Grace micro (0.2) |
| 218 | `aya_visit_03_try` | Nerve micro (0.2) |
| 239 | `aya_visit_03_close` | Grace small (0.5) |
| **Aya visit 4** | | |
| 270 | `aya_visit_04_school` | Insight micro (0.2) |
| 275 | `aya_visit_04_change` | Nerve micro (0.2) |
| 279 | `aya_visit_04_figuring` | Grace micro (0.2) |
| 291 | `aya_visit_04_back` | Insight small (0.5) |
| 296 | `aya_visit_04_see` | Grace small (0.5) |
| 300 | `aya_visit_04_masks` | Nerve micro (0.2) |
| 314 | `aya_visit_04_wanted` | Grace micro (0.2) |
| 318 | `aya_visit_04_worth` | Nerve micro (0.2) |
| 331 | `aya_visit_04_close` | Grace small (0.5) |
| **Aya visit 5** | | |
| 362 | `aya_visit_05_instead` | Insight micro (0.2) |
| 367 | `aya_visit_05_parents` | Grace micro (0.2) |
| 371 | `aya_visit_05_carrying` | Nerve micro (0.2) |
| 381 | `aya_visit_05_doing` | Grace micro (0.2) |
| 386 | `aya_visit_05_brave` | Nerve micro (0.2) |
| 391 | `aya_visit_05_stay` | Grace micro (0.2) |
| 407 | `aya_visit_05_close` | Grace small (0.5) |
| **Aya visit 6** | | |
| 426 | `aya_visit_06_audition` | Nerve micro (0.2) |
| 430 | `aya_visit_06_kind` | Insight micro (0.2) |
| 434 | `aya_visit_06_different` | Grace micro (0.2) |
| 446 | `aya_visit_06_felt` | Grace micro (0.2) |
| 451 | `aya_visit_06_again` | Nerve micro (0.2) |
| 457 | `aya_visit_06_proud` | Grace micro (0.2) |
| 470 | `aya_visit_06_see` | Insight micro (0.2) |
| 475 | `aya_visit_06_show` | Nerve micro (0.2) |
| 479 | `aya_visit_06_good` | Grace micro (0.2) |
| 491 | `aya_visit_06_both` | Grace small (0.5) |
| 495 | `aya_visit_06_brave` | Nerve micro (0.2) |
| 507 | `aya_visit_06_close` | Grace small (0.5) |
| **Aya visit 7** | | |
| 530 | `aya_visit_07_leaving` | Insight micro (0.2) |
| 535 | `aya_visit_07_happened` | Nerve micro (0.2) |
| 539 | `aya_visit_07_sorry` | Grace micro (0.2) |
| 551 | `aya_visit_07_proud` | Grace small (0.5) |
| 556 | `aya_visit_07_braver` | Nerve micro (0.2) |
| 560 | `aya_visit_07_miss` | Grace micro (0.2) |
| 571 | `aya_visit_07_treasure` | Grace micro (0.2) |
| 575 | `aya_visit_07_perfect` | Nerve micro (0.2) |
| 597 | `aya_visit_07_close` | Grace small (0.5) |

### `game/hana.rpy`

| Line | Flag | Reward |
|---:|---|---|
| **Hana visit 2** | | |
| 64 | `hana_visit_02_thanks` | Grace micro (0.2) |
| 68 | `hana_visit_02_quiet` | Insight micro (0.2) |
| 90 | `hana_visit_02_close` | Grace small (0.5) |
| **Hana visit 3** | | |
| 118 | `hana_visit_03_whisper` | Grace micro (0.2) |
| 122 | `hana_visit_03_wait` | Insight micro (0.2) |
| 149 | `hana_visit_03_close` | Grace small (0.5) |
| **Hana visit 4** | | |
| 186 | `hana_visit_04_match` | Nerve micro (0.2) |
| 189 | `hana_visit_04_stay` | Grace micro (0.2) |
| 202 | `hana_visit_04_close` | Grace small (0.5) |
| **Hana visit 5** | | |
| 226 | `hana_visit_05_quiet` | Grace micro (0.2) |
| 229 | `hana_visit_05_pretend` | Insight micro (0.2) |
| 258 | `hana_visit_05_close` | Grace small (0.5) |
| **Hana visit 6** | | |
| 279 | `hana_visit_06_time` | Grace micro (0.2) |
| 282 | `hana_visit_06_listen` | Insight micro (0.2) |
| 313 | `hana_visit_06_tell` | Nerve micro (0.2) |
| 317 | `hana_visit_06_incredible` | Grace small (0.5) |
| 332 | `hana_visit_06_close` | Grace small (0.5) |
| **Hana visit 7** | | |
| 356 | `hana_visit_07_told` | Insight micro (0.2) |
| 359 | `hana_visit_07_parents` | Grace micro (0.2) |
| 379 | `hana_visit_07_now` | Insight micro (0.2) |
| 383 | `hana_visit_07_win` | Grace micro (0.2) |
| 397 | `hana_visit_07_forget` | Grace micro (0.2) |
| 400 | `hana_visit_07_means` | Grace small (0.5) |
| 419 | `hana_visit_07_close` | Grace small (0.5) |
| **Hana closed** | | |
| 445 | `hana_visit_closed_quiet` | Grace micro (0.2) |
| 448 | `hana_visit_closed_message` | Nerve micro (0.2) |
| 457 | `hana_visit_closed_close` | Grace small (0.5) |

### `game/orson.rpy`

| Line | Flag | Reward |
|---:|---|---|
| **Orson visit 2** | | |
| 49 | `orson_visit_02_origin` | Nerve micro (0.2) |
| 53 | `orson_visit_02_everywhere` | Grace micro (0.2) |
| 63 | `orson_visit_02_surprise` | Nerve micro (0.2) |
| 67 | `orson_visit_02_light` | Grace micro (0.2) |
| 98 | `orson_visit_02_teach` | Grace small (0.5) |
| 102 | `orson_visit_02_nexttime` | Nerve micro (0.2) |
| 113 | `orson_visit_02_close` | Grace small (0.5) |
| **Orson visit 3** | | |
| 135 | `orson_visit_03_story` | Grace micro (0.2) |
| 150 | `orson_visit_03_notebook` | Grace micro (0.2) |
| 154 | `orson_visit_03_live` | Nerve micro (0.2) |
| 165 | `orson_visit_03_close` | Grace small (0.5) |
| **Orson visit 4** | | |
| 197 | `orson_visit_04_fake` | Nerve micro (0.2) |
| 201 | `orson_visit_04_anchors` | Grace micro (0.2) |
| 222 | `orson_visit_04_close` | Grace small (0.5) |
| **Orson visit 5** | | |
| 262 | `orson_visit_05_helps` | Grace micro (0.2) |
| 266 | `orson_visit_05_hard` | Nerve micro (0.2) |
| 275 | `orson_visit_05_close` | Grace small (0.5) |
| **Orson visit 6** | | |
| 320 | `orson_visit_06_showup` | Nerve micro (0.2) |
| 324 | `orson_visit_06_scared` | Grace micro (0.2) |
| 336 | `orson_visit_06_close` | Grace small (0.5) |
| **Orson visit 7** | | |
| 379 | `orson_visit_07_miss` | Grace micro (0.2) |
| 383 | `orson_visit_07_carry` | Nerve micro (0.2) |
| 405 | `orson_visit_07_close` | Grace small (0.5) |


## Findings

### 1. Unbalanced menus

Balance criterion: each option should reward the behavior it expresses, usually one attribute, and the option set should not make one attribute strictly dominant or one choice strictly worse.

**Severely unbalanced / one-sided**
- `talk_veteran_assistant` (L2268): only "I have what I need. Thank you." pays (`veteran_advice_decline`, Insight 0.2, L2279). Both information-seeking options pay nothing. The menu rewards refusing information.
- `first_class` (L3641): only the Nerve-gated option pays, and it pays Grace **-0.2** (`answer_clock_ask`, L3654). The two ungated options pay nothing. Spending a Nerve gate to lose Grace is a trap.
- `after_school` warning menu (L3691): "Next time, warn me before you go." pays Nerve +0.5 and Grace -0.2 (`answer_hikari_warning`, L3693); the other two options pay nothing.
- `first_evening_dinner` first menu (L4955, walk_alone only): covered pays Grace +0.5 (L4948), declined pays Grace -0.2 (L4942). No neutral option.
- `night_table` (L5724): total Insight 0.2 (L5728), plain Grace 0.2 (L5733), boundary Nerve 0.2 (L5742), gated Nerve 0.2 (L5754). Two Nerve options; the 1.2 Nerve gate buys no extra reward over the ungated boundary option.
- `lupins_den` (L6177): thanks pays Grace 0.2 (L6182); silence pays nothing.

**Mono-attribute menus (no real attribute choice)**
- `talk_cheerful_woman` (L2150): both rewarded options are Grace 0.2 (`answer_woman_smile` L2161, `answer_woman_echo` L2168).
- `haiku_lesson` (L5303): notes and listen are both Insight 0.3 (L5307, L5311); research is Nerve 0.3 (L5315). Two of three options are mechanically identical, so the real choice is Insight vs Nerve.
- `night_room_visit` (L5862): library promise Insight 0.2 (L5867), study plan Grace 0.2 (L5874), tease Grace 0.2 (L5882). Two Grace options, no Nerve.
- `sunday_quiz` (L6314/L6329/L6346) and `monday_quiz` (L6513/L6529/L6544): every correct answer pays Insight 0.2; wrong answers pay nothing. This is knowledge-gated, not personality, but it makes the quiz sections Insight-only.

**Well-balanced menus (one option per attribute, same size)**
- `first_dinner` second menu (L4960): natto Nerve 0.2 (L4965), neighborhood Insight 0.2 (L4976), apology Grace 0.2 (L4986).
- `first_night_hikari` (L5057): thanks Grace 0.2 (L5062), observation Insight 0.2 (L5069), promise Nerve 0.2 (L5074).
- `cellular_plan` first menu (L5367) and second menu (L5390): one Insight/Grace/Nerve option each, all 0.2.
- `akihabara_explore` (L5456), maid-cafe entrance (L5481), options (L5523), order (L5542): one Insight/Grace/Nerve option each, all 0.2.
- `maid_cafe` spell (L5572): join Nerve 0.2 (L5574) vs watch Grace 0.2 (L5582).

**Hub-grind asymmetry**
- `check_boards` (L2293) pays Grace 0.1 (`information_seeker`, L2301) only after reading every notice; `look_plants` (L2305) pays Nerve 0.1 (`plant_determination`, L2311) only after ten plants. These are hidden, repeat-visit rewards, unlike the one-visit airport conversations. They are also absent from the checklist.

### 2. Behavior/reward mismatches

Most severe first:
1. **`answer_clock_ask` L3649–3654** — a choice gated on Nerve 0.3 ("Can we discuss today's late mark?") rewards Grace **-0.2** and no Nerve. Assertively asking a professor to review a mark is the definition of the Nerve behavior the gate tests; penalizing Grace is backwards.
2. **`answer_hikari_warning` L3693** — setting a boundary ("warn me before you go") pays Nerve +0.5 but also Grace -0.2. Boundary-setting is assertive, not ungracious; the Grace penalty is unjustified.
3. **`veteran_advice_decline` L2279** — declining offered help pays Insight +0.2. Refusing information is the opposite of insight-seeking; it should be Nerve (independence) or no reward.
4. **`answer_breakfast_questions` L3124** — asking what the department knows about you pays Nerve **-0.2**. Curiosity is penalized while thanking Hikari for the emails pays Grace +0.5 (L3134). The question is awkward, not a failure of Nerve.
5. **`first_dinner_neighborhood` L4976** — asking the father about his own life pays Insight +0.2. Taking an interest in another person is Grace/relationship behavior, not Insight.
6. **`night_room_study_plan` L5874** — asking "What do I actually need to study?" pays Grace +0.2. This is planning/prioritization (Insight), not Grace.
7. **`akihabara_explore_crowd` L5466** — watching the crowd and noticing its patterns pays Grace +0.2. Pattern recognition is Insight; Grace would fit "let the crowd pass" / social ease, but the text explicitly describes analysis.
8. **`night_table_plain` L5733** — "I spent what I needed to. Nothing extra." pays Grace +0.2. Financial restraint is planning/Insight; the sibling `night_table_total` L5728 already pays Insight for checking the total.
9. **`information_seeker` L2301** — reading the entire notice board pays Grace +0.1. Reading/curiosity is Insight. The flag is also undocumented.
10. **`chef_first_umai` L3888/L3892** — "Ask what it means" (an Insight/curiosity behavior) and "Thank him properly" (Grace) share one flag and one Grace +0.5 reward. The Insight behavior is misrewarded as Grace.
11. **`answer_ramen_recommendation` L3840** — asking the chef's recommendation pays Nerve +0.5. Asking for help is closer to Grace/Insight; the two socially harder options ("Order in English", "Point at something") pay nothing.
12. **`answer_taxi_fare` L2437** — asking the fare pays Nerve +0.5. Asking a price is practical/Insight; Nerve is defensible only as asserting yourself about money.
13. **`answer_boxes_postpone` L2813** — the option text is "Which ones go upstairs?", a practical question, but it pays Grace -0.2. The penalty reads as punishing a question rather than a grace violation.
14. **`first_dinner_declined` L4942** — honesty about being full pays Grace -0.2. The behavior is honest (Nerve/Insight); the Grace penalty is harsh, especially since the game elsewhere rewards honesty.
15. **`plant_determination` L2311** — looking at ten plants pays Nerve +0.1. Persistence/determination is defensible, but the behavior is also curiosity (Insight); the flag is undocumented.

Appropriate examples worth keeping: `answer_wall_cat` L3466 (Insight for noticing the poster), `answer_circles_back` L3551 (Grace for thanking the clerk), `sim_circle_first` L4276 (Insight for noticing the light), `answer_circle_help` L4308 (Grace for helping), `night_table_nerve` L5754 (Nerve for the car-cost joke), `lupins_den_first` L6204 (Nerve for entering the bar).

### 3. Inconsistent no-reward options / missing rewards

**Menus where a clearly expressive option pays nothing while a sibling pays 0.2–0.5**
- `talk_security` L2056: "Watch him work" (Insight) pays nothing; bow pays Grace 0.1, press pays Nerve 0.1.
- `talk_timid_man` L2103: "Ask again" (Nerve) and "Step aside" pay nothing; "Leave him alone" pays Insight 0.2.
- `talk_assistant` L2212: "Ask for the address" (Nerve/Grace) and "Never mind" pay nothing; "Wait patiently" pays Insight 0.2.
- `taxi_stand` L2427: "Watch the city through the window" (Insight) pays nothing; asking the fare pays Nerve 0.5.
- `ticket_machine` L2576: using the machine (Insight) pays nothing; asking the woman pays Grace 0.2.
- `train_platform` L2634: the local sign pays nothing; the express sign pays Insight 0.2.
- `boxes` L2801: "Which ones go upstairs?" pays nothing; reassure pays Grace 0.3, postpone pays Grace -0.2.
- `breakfast` L3122: "Should I introduce myself today?" pays nothing; questions pays Nerve -0.2, emails pays Grace 0.5.
- `department_tour` L3452: film and rooms pay nothing; the gated lost cat pays Insight 0.2.
- `student_relations` L3538: the first two options pay nothing; the gated thank-you pays Grace 0.2.
- `after_school` L3691: thanks and move-on pay nothing; warn pays Nerve 0.5/Grace -0.2.
- Ramen order L3827: English and point pay nothing; recommendation pays Nerve 0.5.
- Ramen broth L3855: "Try it before asking" pays nothing; asking pays Insight 0.3.
- Umai L3878: smoky-flavour and smile options pay nothing; ask-meaning/thank pay Grace 0.5 (same flag).
- Run L4013: "Which turn is ours?" (Insight) pays nothing; thanks pays Grace 0.3, history pays Insight 0.3.
- Run L4031: "Out where?" pays nothing; "Can I come?" pays Nerve 0.2.
- River L4098: "Do you do this every day?" and "Why the river?" (Insight) pay nothing; "Let her enjoy the quiet" pays Grace 0.5.
- Circle L4239: "Is this the photography club?" and "Hikari told me" pay nothing; "Could I join today?" pays Nerve 0.5.
- Circle L4270: tilted phone and "not sure what to look for" pay nothing; window observation pays Insight 0.5.
- Circle L4288: **both** options ("How did Circle start?" and "Do you shoot outside the club too?") pay nothing — a dead menu.
- Circle L4303: watch and theme pay nothing; help pays Grace 0.5.
- `library_search` L6014: all three navigation options pay nothing (flavor/navigation, not necessarily a bug).
- `reading_club_first` L6054: both options pay nothing (dead menu).
- `lupins_den` L6177: silence pays nothing; thanks pays Grace 0.2.
- `monday_morning` L6587: no reward calls; flavor only.

**Dead menus (no reward on any option)**: `leaving_house` L3215, `school_morning` L3344, `library_search` L6014, `reading_club_first` L6054, `monday_morning` L6587. Some are navigation/flavor, but they break the reward cadence.

**Missing documentation**: `information_seeker` (Grace 0.1, L2301) and `plant_determination` (Nerve 0.1, L2311) are absent from `documentation/attribute_rewards_checklist.md`. All 180 confidant reward calls are also absent from that checklist.

**Excluded, confirmed**: `game/quiz.rpy` L23 is commented out; `attribute_test_rank_up` L592 is a dev shortcut; `dream_archive.rpy` L430 is the archived board.

### 4. Per-route totals through end of Day 6

Method: maximum attainable points per attribute, not simultaneous. "Common" covers all mandatory/hub content outside the Day 2 afternoon branch: airport, travel, boxes, Day 2 morning, dinner/night, and Days 3–6. "Route exclusive" covers the Day 2 afternoon label, including the walk-only ramen scene and the walk-only first-dinner menu. Confidant repeat visits are excluded.

| Segment | Insight | Grace | Nerve |
|---|---:|---:|---:|
| Common — train | 6.2 | 4.2 | 3.5 |
| Common — taxi | 5.5 | 4.0 | 4.7 |
| `walk_alone` exclusive | 0.8 | 1.0 | 0.5 |
| `walk_hikari` (run) exclusive | 0.3 | 0.8 | 0.7 |
| `photo_club` exclusive | 0.5 | 1.0 | 0.5 |

| Route | Travel | Insight | Grace | Nerve |
|---|---|---:|---:|---:|
| `walk_alone` | train | **7.0** | **5.2** | 4.0 |
| `walk_alone` | taxi | 6.3 | 5.0 | **5.2** |
| `walk_hikari` | train | 6.5 | 5.0 | 4.2 |
| `walk_hikari` | taxi | 5.8 | 4.8 | **5.4** |
| `photo_club` | train | 6.7 | **5.2** | 4.0 |
| `photo_club` | taxi | 6.0 | 5.0 | **5.2** |

Interpretation:
- No route starves an attribute to zero. Every route can earn all three.
- Grace is the highest ceiling on every route (4.8–5.2). Insight is second on train (6.2–7.0) but drops on taxi (5.5–6.3). Nerve is lowest on train (4.0–4.2) and highest on taxi (5.2–5.4). This is the intended route asymmetry documented at `script.rpy` L2345–2352: train rewards Insight, taxi rewards Nerve.
- The run route has the lowest Insight ceiling (6.5 train / 5.8 taxi). `walk_alone` has the highest Insight ceiling (7.0/6.3) but the lowest train Nerve (4.0). `photo_club` is middle.
- **Rank 3 (9.5) is unreachable in any attribute by the end of Day 6 on the linear path**; the maximum is 7.0. Rank 2 (5.0) is reachable in Insight on all routes, in Grace on all routes except taxi+run (4.8, 0.2 short), and in Nerve only on taxi routes (5.2–5.4). Train Nerve (4.0–4.2) cannot reach rank 2.
- Including confidant repeat visits changes this sharply: the five confidant files pay roughly Grace 35.2 / Insight 10.9 / Nerve 8.1 (~65% Grace). Grace can reach rank 3–4 while Insight and Nerve lag. Orson pays **zero Insight** across all seven visits.

### 5. Gate reachability

| Gate | Line | Requirement | Train max before gate | Taxi max before gate | Verdict |
|---|---:|---:|---:|---:|---|
| Lost cat (Insight) | 3461 | 0.8 | 1.5 | 0.8 | Train easy; taxi exactly 0.8, requiring all four pre-gate Insight choices: timid 0.2 + assistant 0.2 + veteran 0.2 + courtyard buildings 0.2. |
| Clerk thank-you (Grace) | 3548 | 1.0 | 1.1–1.2 | 1.1–1.2 | Reachable on both. Minimum practical combo: security bow 0.1 + woman 0.2 + boxes reassure 0.3 + breakfast emails 0.5 = 1.1. Reading the whole board adds 0.1 (1.2). One bad choice (boxes postpone -0.2 or breakfast questions instead of emails) can drop below 1.0. |
| Late mark (Nerve) | 3649 | 0.3 | 0.4 | 1.6 | Train has only 0.1 margin: security press 0.1 + train gate 0.3. If the player chose bow at security, train gate alone gives exactly 0.3. Taxi is trivial (route 1.0 + fare 0.5 + press 0.1). |
| Car cost (Nerve) | 5744 | 1.2 | ≥3.1 | ≥4.3 | Comfortably reachable on all routes with ordinary Nerve choices; not a real constraint. |

Gate issues:
- The Insight gate is route-asymmetric by design, but the taxi path has **zero margin**: 0.8 exactly. Missing any one of the four Insight options closes it permanently for that run.
- The Grace gate is the tightest early gate in practice. It is front-loaded into the airport and the boxes/breakfast scenes, so it is route-independent, but a player who prioritizes Nerve or Insight at those menus can miss it.
- The Nerve 0.3 gate on the train route is brittle (0.1 margin) and, once opened, the reward is Grace -0.2. Passing the gate is actively punished.
- The 1.2 Nerve gate is decorative: by Day 3 the player has far more than 1.2 Nerve available, and the gated option pays the same 0.2 as the ungated boundary option.

### 6. Duplicate / reused / non-unique flags

Verified by scanning every `reward_attributes_once` flag across all six files. Only two flags repeat:

| Flag | Lines | Attributes | Assessment |
|---|---|---|---|
| `chef_first_umai` | `script.rpy` L3888, L3892 | Grace small (0.5) both | Two different options ("Ask what it means" and "Thank him properly") share one flag. `reward_attributes_once` means only the first call pays; the second is a no-op. Intentional anti-farming, but the two behaviors are not independently tracked, and the Insight-flavored option is paid as Grace. |
| `travel_route_attribute` | `script.rpy` L2362, L2377, L2381 | Insight small (L2362, L2381), Nerve medium (L2377) | Same flag across three mutually exclusive travel branches. Only one can fire per run, so no double-pay, but the flag does not encode branch or attribute. Train and taxi→train both pay Insight 0.5 and are indistinguishable in the save/analytics. |

Non-unique semantics without duplicate flags:
- `answer_woman_smile` L2161 and `answer_woman_echo` L2168: separate flags, identical Grace 0.2, mutually exclusive.
- `haiku_lesson_notes` L5307 and `haiku_lesson_listen` L5311: separate flags, identical Insight 0.3, mutually exclusive.
- `night_table_boundary` L5742 and `night_table_nerve` L5754: separate flags, identical Nerve 0.2, mutually exclusive; the 1.2 gate adds no reward.
- `first_dinner_declined` L4942 and `first_dinner_covered` L4948: mutually exclusive, +0.5 vs -0.2.
- `chef_first_umai` L3888/L3892 as above.

No cross-file flag collisions were found. `information_seeker` L2301 and `plant_determination` L2311 are unique but undocumented and semantically questionable (Grace for reading, Nerve for persistence).

### Bottom line

The reward system is coherent in its size vocabulary and its one-time-flag discipline, but it is **Grace-heavy and Nerve-punishing** in the main story, and overwhelmingly Grace-heavy in the confidant chains. The three changes with the highest balance payoff are:
1. Fix `answer_clock_ask` L3654: a Nerve-gated choice must not pay Grace -0.2 and zero Nerve.
2. Remove or reassign the Grace penalties on `answer_hikari_warning` L3693, `answer_boxes_postpone` L2813, and `first_dinner_declined` L4942; they punish honest/boundary behavior.
3. Reassign the mislabeled rewards: `veteran_advice_decline` (Insight→Nerve/none), `first_dinner_neighborhood` and `night_room_study_plan` (→Insight), `akihabara_explore_crowd` and `night_table_plain` (→Insight), and split `chef_first_umai` so the Insight option pays Insight.

No game files were modified. The report is at `documentation/attribute_balance_audit.md`.

---

## Follow-up — 2026-11-09 (balance pass applied)

The findings above were applied later the same day, in the same session that
built Day 7. The pass rewrote reward calls in `game/script.rpy` and the five
confidant files; the audit's final line ("No game files were modified") records
the state that produced it, not the state after this pass.

Applied fixes:

1. `answer_clock_ask` (late mark) now pays **Nerve micro**; the ungated
   attendance options pay Insight and Grace micro respectively, so the menu is
   no longer one-sided and the gate tests what it rewards.
2. The Grace penalties were removed from `answer_hikari_warning`,
   `answer_boxes_postpone`, and `first_dinner_declined`; boundary honesty now
   pays Nerve (small / micro).
3. The mislabeled rewards were reassigned: `veteran_advice_decline` → Nerve;
   `first_dinner_neighborhood` → Grace; `night_room_study_plan` → Insight;
   `akihabara_explore_crowd` → Insight; `night_table_plain` kept as Grace
   (responsibility); `chef_first_umai` was split into
   `chef_first_umai_meaning` (Insight) and `chef_first_umai_thanks` (Grace).
4. One-sided and dead menus were filled so each answered choice pays one
   attribute at micro size (veteran advice, taxi fare, ramen order, run
   logistics, river questions, circle menus, Lupin's Den silence, Monday forks,
   and the new hub walks).
5. Close rewards (`*_close`) were rotated across Insight, Grace and Nerve at
   micro size, so no confidant pays Grace on nearly every visit.

The new Day 7 content (breakfast, lecture, night study, hub walks) follows the
same one-attribute-per-choice-at-micro pattern, and the checklist now carries
M55–M60 plus the confidant visit reward tables. See
`documentation/character_attributes.md` §12.2 for the new final balance verdict.
