# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start a new game on **Normal** difficulty (range 1-100, 8 attempts). The secret is hidden, but the Debug Info panel shows the secret, for example, `55`.
2. Enter a guess of `40` and click **Submit Guess**. The game returns **"Too Low"** with the hint "📈 Go HIGHER!" and the score drops by 5 (Attempts: 1, Score: -5).
3. Enter a guess of `70` and click **Submit Guess**. The game returns **"Too High"** with the hint "📉 Go LOWER!"; a wrong guess always costs 5 points, regardless of attempt number (Attempts: 2, Score: -10).
4. Enter a guess of `55` and click **Submit Guess**. The game returns **"Win"**, awarding `100 - 10 * (attempt + 1)` points for the 3rd attempt (60 points), bringing the final score to 50.
5. The app shows a success banner with the revealed secret and final score, the guess input/Submit/hint controls disappear, and only a **"New Game 🔁"** button remains to start over.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================

collected 22 items                                                                                                                                                                                                                               

tests/test_game_logic.py::test_winning_guess PASSED                                                                                                                                                                                        [  4%]
tests/test_game_logic.py::test_guess_too_high PASSED                                                                                                                                                                                       [  9%]
tests/test_game_logic.py::test_guess_too_low PASSED                                                                                                                                                                                        [ 13%]
tests/test_game_logic.py::test_guess_one_above_secret PASSED                                                                                                                                                                               [ 18%]
tests/test_game_logic.py::test_guess_one_below_secret PASSED                                                                                                                                                                               [ 22%]
tests/test_game_logic.py::test_guess_with_negative_numbers PASSED                                                                                                                                                                          [ 27%]
tests/test_game_logic.py::test_range_easy PASSED                                                                                                                                                                                           [ 31%]
tests/test_game_logic.py::test_range_normal PASSED                                                                                                                                                                                         [ 36%]
tests/test_game_logic.py::test_range_hard PASSED                                                                                                                                                                                           [ 40%]
tests/test_game_logic.py::test_range_unknown_difficulty_defaults_to_normal PASSED                                                                                                                                                          [ 45%]
tests/test_game_logic.py::test_parse_guess_valid_integer PASSED                                                                                                                                                                            [ 50%]
tests/test_game_logic.py::test_parse_guess_valid_float_string_truncates PASSED                                                                                                                                                             [ 54%]
tests/test_game_logic.py::test_parse_guess_negative_number PASSED                                                                                                                                                                          [ 59%]
tests/test_game_logic.py::test_parse_guess_empty_string PASSED                                                                                                                                                                             [ 63%]
tests/test_game_logic.py::test_parse_guess_none_input PASSED                                                                                                                                                                               [ 68%]
tests/test_game_logic.py::test_parse_guess_non_numeric_string PASSED                                                                                                                                                                       [ 72%]
tests/test_game_logic.py::test_update_score_win_on_first_attempt PASSED                                                                                                                                                                    [ 77%]
tests/test_game_logic.py::test_update_score_win_floors_at_ten_points PASSED                                                                                                                                                                [ 81%]
tests/test_game_logic.py::test_update_score_too_high_even_attempt PASSED                                                                                                                                                                   [ 86%]
tests/test_game_logic.py::test_update_score_too_high_odd_attempt PASSED                                                                                                                                                                    [ 90%]
tests/test_game_logic.py::test_update_score_too_low_always_penalized PASSED                                                                                                                                                                [ 95%]
tests/test_game_logic.py::test_update_score_unrecognized_outcome_leaves_score_unchanged PASSED                                                                                                                                             [100%]

============================================================================================================== 22 passed in 0.03s ===============================================================================================================
(.venv) PS C:\Users\z_gu0\Documents\github_io\ai110-module1show-gameglitchinvestigator-starter> 
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
