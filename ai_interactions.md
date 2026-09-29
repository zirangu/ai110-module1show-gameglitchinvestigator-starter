# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

"I want to add a new feature. This feature will display a 'Guess History' sidebar that visualizes how close your previous guesses were. It only displays after the game is over (you win or run out of attempts), use a visual graph option that makes the most sense. do not disturb any other mechanics in the site" — followed by three rounds of bug reports/refinements as I tested the result: a runtime crash after the feature was added, a delayed-display bug on winning, and a redundant chart legend.

**What did the agent do?**

1. Read `app.py` and `requirements.txt` to see what charting libraries were already available (found `altair<5` pinned), then added a sidebar bar chart inside the existing game-over gate showing `guess - secret` per attempt, color-coded by outcome, using `alt.Chart` + nested `alt.condition()` for coloring.
2. When I reported `TypeError: dict() got multiple values for keyword argument 'condition'` on run, the agent diagnosed that nested `alt.condition()` isn't valid in this Altair API version, and reproduced the deeper issue by testing standalone: pinned `altair<5` (4.2.2) is incompatible with the installed pandas 3.x's string dtype handling. Rather than patch around the broken library, it dropped the direct `altair` import entirely and rebuilt the chart using Streamlit's native `st.bar_chart(..., color="Category")`, which supports categorical coloring without needing Altair at all. It verified the fix with Streamlit's `AppTest` harness (simulating a finished game) before calling it done.
3. When I reported the chart only appeared after clicking a second time post-win, the agent traced this to the game-over gate (where the chart lived) only being reached on the *next* script rerun — a win sets `status` mid-script, after the gate has already been passed for that run. Its first instinct was to add `st.rerun()` right after the win/loss messages, but it caught on its own that this would immediately wipe out the win message (secret + score reveal) since the rerun would re-render the generic "You already won" gate text instead. It corrected course: factored the chart into a `render_guess_history()` function and called it both from the gate and directly inside the `if submit:` block at the moment a win/loss is detected, so it renders on the same click with no rerun needed.
4. When I pointed out the caption line ("🟦 Too low · 🟥 Too high · 🟩 Correct") duplicated the legend `st.bar_chart(..., color="Category")` already renders automatically, the agent removed the caption line.

**What did you have to verify or fix manually?**

- I was the one who caught all three issues by actually running the app (the agent's own testing — `AppTest` simulations and `pytest` — didn't surface the Altair/pandas crash, the delayed-chart timing bug, or the redundant legend, since none of those are exercised by an automated test suite). This is a good reminder that agent-run tests aren't a substitute for manually clicking through the actual UI.
- I didn't have to touch the code myself; each fix was applied by the agent after I described the symptom, and it re-ran `pytest` (22 passed) after every change to confirm no regressions to the core game logic.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Boundary guesses (secret ± 1) and negative numbers in `check_guess` | "can you think of some more test cases to add in the test_game_logic.py" | `test_guess_one_above_secret`, `test_guess_one_below_secret`, `test_guess_with_negative_numbers` | Yes | The original tests only checked one arbitrary guess/secret pair per outcome; boundary values (right next to the secret) and negative numbers are where off-by-one or sign-handling bugs like the earlier Higher/Lower swap would most likely resurface. |
| Untested `get_range_for_difficulty` branches, including the unknown-difficulty fallback | Same prompt as above | `test_range_easy`, `test_range_normal`, `test_range_hard`, `test_range_unknown_difficulty_defaults_to_normal` | Yes | This function had zero coverage before; the fallback branch (any string not "Easy"/"Normal"/"Hard" silently defaults to the Normal range) is an implicit behavior that's easy to break without a dedicated test. |
| `parse_guess` invalid/edge inputs: empty string, `None`, non-numeric text, float-like strings, negative numbers | Same prompt as above | `test_parse_guess_valid_integer`, `test_parse_guess_valid_float_string_truncates`, `test_parse_guess_negative_number`, `test_parse_guess_empty_string`, `test_parse_guess_none_input`, `test_parse_guess_non_numeric_string` | Yes | `parse_guess` is the app's only input boundary from raw user text; each failure path (`""`, `None`, `"abc"`) returns a different error message, and the `"42.7"` case exercises the `int(float(...))` truncation branch that's easy to overlook. |
| `update_score` win floor, and outcome branches (Too High / Too Low / unrecognized) | Same prompt as above, then "not all test cases are commented. add comment to explain what is to be tested" and "also, please update your test cases" (after fixing the Too High parity bug) | `test_update_score_win_on_first_attempt`, `test_update_score_win_floors_at_ten_points`, `test_update_score_too_high_even_attempt`, `test_update_score_too_high_odd_attempt`, `test_update_score_too_low_always_penalized`, `test_update_score_unrecognized_outcome_leaves_score_unchanged` | Yes (after updating the Too High tests) | `update_score` had no coverage at all; the win-floor case (`points < 10 -> 10`) is a hidden clamp, and the two `Too High` tests originally caught (then, after the fix, re-confirmed the removal of) a real bug where the penalty flipped to a +5 reward on even attempt numbers, inconsistent with `Too Low`'s constant -5. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
