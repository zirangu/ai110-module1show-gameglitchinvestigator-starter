from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"

def test_guess_one_above_secret():
    # Boundary just above the secret should still read "Too High"
    outcome, message = check_guess(51, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"

def test_guess_one_below_secret():
    # Boundary just below the secret should still read "Too Low"
    outcome, message = check_guess(49, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"

def test_guess_with_negative_numbers():
    # Negative guess/secret pairs should resolve the same as positive ones
    outcome, message = check_guess(-10, -5)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"

def test_range_easy():
    # Easy difficulty should give a 1-20 range
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_range_normal():
    # Normal difficulty should give a 1-100 range
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_range_hard():
    # Hard difficulty should give a 1-50 range
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_range_unknown_difficulty_defaults_to_normal():
    # Unrecognized difficulty should fall back to the Normal range
    assert get_range_for_difficulty("Nightmare") == (1, 100)

def test_parse_guess_valid_integer():
    # A plain integer string should parse successfully with no error
    ok, guess_int, err = parse_guess("42")
    assert ok is True
    assert guess_int == 42
    assert err is None

def test_parse_guess_valid_float_string_truncates():
    # "42.7" should parse via int(float(...)) and truncate to 42
    ok, guess_int, err = parse_guess("42.7")
    assert ok is True
    assert guess_int == 42
    assert err is None

def test_parse_guess_negative_number():
    # Negative number strings should parse successfully
    ok, guess_int, err = parse_guess("-5")
    assert ok is True
    assert guess_int == -5
    assert err is None

def test_parse_guess_empty_string():
    # Empty input should fail with an "Enter a guess." error
    ok, guess_int, err = parse_guess("")
    assert ok is False
    assert guess_int is None
    assert err == "Enter a guess."

def test_parse_guess_none_input():
    # None input should fail with an "Enter a guess." error
    ok, guess_int, err = parse_guess(None)
    assert ok is False
    assert guess_int is None
    assert err == "Enter a guess."

def test_parse_guess_non_numeric_string():
    # Non-numeric input should fail with a "That is not a number." error
    ok, guess_int, err = parse_guess("abc")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."

def test_update_score_win_on_first_attempt():
    # attempt_number=1 -> points = 100 - 10*(1+1) = 80
    assert update_score(current_score=0, outcome="Win", attempt_number=1) == 80

def test_update_score_win_floors_at_ten_points():
    # attempt_number=9 -> points = 100 - 10*(9+1) = 0, floored to 10
    assert update_score(current_score=0, outcome="Win", attempt_number=9) == 10

def test_update_score_too_high_even_attempt():
    # "Too High" on an even attempt number should add 5 points
    assert update_score(current_score=0, outcome="Too High", attempt_number=2) == 5

def test_update_score_too_high_odd_attempt():
    # "Too High" on an odd attempt number should subtract 5 points
    assert update_score(current_score=0, outcome="Too High", attempt_number=3) == -5

def test_update_score_too_low_always_penalized():
    # "Too Low" should always subtract 5 points, regardless of attempt number
    assert update_score(current_score=0, outcome="Too Low", attempt_number=1) == -5
    assert update_score(current_score=0, outcome="Too Low", attempt_number=2) == -5

def test_update_score_unrecognized_outcome_leaves_score_unchanged():
    # An outcome that isn't Win/Too High/Too Low should leave the score untouched
    assert update_score(current_score=42, outcome="Whatever", attempt_number=1) == 42


