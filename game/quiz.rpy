################################################################################
## QUIZ — reusable question screen for exams, lectures, and study scenes
################################################################################
##
## One question at a time, no timer, no fail state. `run_quiz(questions)` plays
## a set and returns a list of booleans — True where he answered correctly — so
## a scene can award Insight for a clean sheet or branch on a specific miss.
##
## Each question is a dict:
##   "q"       the prompt
##   "choices" list of answer strings
##   "answer"  index into "choices"
##   "explain" optional line shown after answering, right or wrong
##
## Example:
##   $ results = run_quiz([
##       {"q": "What is a kigo?",
##        "choices": ["A seasonal word", "A syllable count", "A poet's name"],
##        "answer": 0,
##        "explain": "The word that places the poem in a season."},
##   ])
##   if all(results):
##       $ reward_attributes_once("exam_quiz_clean", [("insight", "small")], show="auto")
##
## Design guardrails (see documentation/minigame_ideas.md): short, rules clear
## up front, never required for story progression, once-only rewards.

init python:

    def run_quiz(questions):
        """Play a quiz set. Returns a list of booleans, one per question."""
        results = []
        for q in questions:
            pick = renpy.call_screen("quiz_question", q)
            results.append(pick == q["answer"])
            renpy.call_screen("quiz_feedback", q, pick)
        return results


screen quiz_question(q):

    modal True
    zorder 180

    add Solid("#000000")

    frame:
        xalign 0.5
        yalign 0.5
        xsize gui.scale(620)
        padding (gui.scale(40), gui.scale(30))
        background Solid("#1d1a16f2")

        vbox:
            spacing gui.scale(18)

            text "QUESTION" size gui.scale(13) color "#8a8377" kerning gui.scale(3)
            text q["q"] size gui.scale(28) color "#e8e2d5" xalign 0.5

            vbox:
                spacing gui.scale(8)
                for i, choice in enumerate(q["choices"]):
                    button:
                        action Return(i)
                        background Solid("#2b2721")
                        hover_background Solid("#393126")
                        padding (gui.scale(16), gui.scale(10))
                        text choice size gui.scale(22) color "#e8e2d5" xalign 0.5


screen quiz_feedback(q, pick):

    modal True
    zorder 181

    add Solid("#000000")

    $ correct = (pick == q["answer"])

    frame:
        xalign 0.5
        yalign 0.5
        xsize gui.scale(560)
        padding (gui.scale(40), gui.scale(30))
        background Solid("#1d1a16f2")

        vbox:
            spacing gui.scale(16)
            xalign 0.5

            text ("CORRECT" if correct else "NOT QUITE") size gui.scale(13) color ("#77d98b" if correct else "#ff6b6b") kerning gui.scale(3) xalign 0.5

            text q["choices"][pick] size gui.scale(24) color "#e8e2d5" xalign 0.5

            if correct:
                text "That's the one." size gui.scale(19) color "#8a8377" xalign 0.5
            else:
                text "The answer was: [q['choices'][q['answer']]]" size gui.scale(19) color "#8a8377" xalign 0.5

            if "explain" in q:
                text q["explain"] size gui.scale(19) color "#b8b0a0" xalign 0.5

            textbutton "Continue":
                action Return(True)
                xalign 0.5
                text_size gui.scale(20)
                text_color "#e8e2d5"
                text_hover_color "#ffffff"
