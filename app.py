import random
import pandas as pd
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    # Fix: was initialized to 1, causing an off-by-one that ended the game
    # one guess early and undercounted "Attempts left" from the first render.
    st.session_state.attempts = 0



if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []



# Feature: Hot/Cold proximity label, purely cosmetic on top of check_guess's
# existing outcome/message — doesn't change scoring or win/loss logic.
def get_hot_cold_label(guess: int, secret: int, low: int, high: int) -> str:
    span = max(high - low, 1)
    closeness = abs(guess - secret) / span
    if guess == secret:
        return "🎯 Bullseye!"
    if closeness <= 0.02:
        return "🔥🔥 Blazing Hot"
    if closeness <= 0.10:
        return "🔥 Hot"
    if closeness <= 0.25:
        return "🌤️ Warm"
    return "🧊 Cold"


# Feature: Guess History sidebar chart + session summary table, shown only
# once the game has ended (won or lost). Factored into a function so it can
# be called both from the game-over gate below and immediately at the moment
# a win/loss is detected in the `if submit:` block, without needing an extra
# rerun/click.
def render_guess_history():
    numeric_guesses = [g for g in st.session_state.history if isinstance(g, int)]
    if not numeric_guesses:
        return
    distances = [g - st.session_state.secret for g in numeric_guesses]
    categories = [
        "Correct" if d == 0 else "Too High" if d > 0 else "Too Low"
        for d in distances
    ]
    hot_cold = [
        get_hot_cold_label(g, st.session_state.secret, low, high)
        for g in numeric_guesses
    ]

    st.sidebar.subheader("📊 Guess History")
    chart_df = pd.DataFrame({
        "Attempt": range(1, len(numeric_guesses) + 1),
        "Distance": distances,
        "Category": categories,
    })
    st.sidebar.bar_chart(
        chart_df,
        x="Attempt",
        y="Distance",
        color="Category",
    )

    st.subheader("📋 Session Summary")
    summary_df = pd.DataFrame({
        "Attempt": range(1, len(numeric_guesses) + 1),
        "Guess": numeric_guesses,
        "Result": categories,
        "Hot/Cold": hot_cold,
    })
    st.table(summary_df.set_index("Attempt"))


if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")

    render_guess_history()

    # Fix: New Game control lives inside the gate (before st.stop()) so the
    # player isn't stranded with no way to restart once the game ends. Also
    # resets status and history, which the original handler never cleared.
    if st.button("New Game 🔁"):
        st.session_state.attempts = 0
        st.session_state.secret = random.randint(low, high)
        st.session_state.status = "playing"
        st.session_state.history = []
        st.success("New game started.")
        st.rerun()

    st.stop()

st.subheader("Make a guess")

# Fix: "Attempts left" banner moved to after the `if submit:` block (see
# bottom of file) so it reflects the post-increment count instead of
# showing a stale pre-increment value on the loss-triggering render.

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    # Fix: was hardcoded to random.randint(1, 100), which ignored the
    # selected difficulty's range for every mid-session New Game click.
    st.session_state.secret = random.randint(low, high)
    st.success("New game started.")
    st.rerun()



if submit:
    
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # Fix: removed the old int/str alternation hack (secret's type used
        # to flip every other guess), which caused
        # "TypeError: '>' not supported between instances of 'int' and 'str'"
        # once check_guess's silent string-fallback branch was dropped.
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            # Feature: color-code the hint by direction instead of always
            # using a plain warning, and append a Hot/Cold proximity badge.
            # Purely presentational — outcome/message still come from the
            # unmodified check_guess() in logic_utils.py.
            hot_cold = get_hot_cold_label(guess_int, st.session_state.secret, low, high)
            hint_text = f"{message} {hot_cold}"
            if outcome == "Too High":
                st.error(hint_text)
            elif outcome == "Too Low":
                st.info(hint_text)
            else:
                st.warning(hint_text)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
            # Fix: show the Guess History chart right away on the winning
            # click, instead of waiting for the next rerun to hit the
            # game-over gate above (which only runs on the *next* script run).
            render_guess_history()
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
                render_guess_history()

# Fix: Debug Info expander moved to after the `if submit:` block so
# "History" reflects the current click's append instead of lagging one
# render behind (most visible as an empty [] on the very first submit).
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# Fix: moved here (after `if submit:`) so it shows the post-increment
# attempts count instead of a stale value from before the submit.
st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)
st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
