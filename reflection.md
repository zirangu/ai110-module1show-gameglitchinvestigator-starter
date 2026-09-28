# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error | Suspected **Code Location** | Fixed? |
|-------|-------------------|-----------------|------------------------|-------|-------|
| Number guessed < Secret or > Secret | Hint should say go higher/lower. | It is reversed. When Number guessed <Secret hint says go lower, and when Number guessed > Secret hint says go higher. | None | check_guess | Yes |
| Keep guessing when there is 2 attempts left | there will be 1 attempt left and the system should allow you to keep guessing if the 2nd last guess is not correct | "Out of attempts!" | None | line 138-141 | Yes |
| click "New Game" button after finishing a game | The game gets refreshed | The text still says "Game over. Start a new game to try again", even though the Secret is getting refreshed | None | Line 101-130 | Yes |
| Change difficulty setting, and then click on new game | Change difficulty between Easy/Normal/Hard, the secret should fall in the specified range | The secret can fall outside of the range when difficulty = easy or normal. | None | Line 95 | Yes |
| when your guess attempt is even, guess a higher number | score  - 5 | score +5 | None | Line 66 | Yes |



---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.



**Answer to 1:** Claude, Claude Code

**Answer to 2:** AI discovered the inconsistency of score deduction for higher guess when the attempt count is even, which I omitted in the beginning. I then identified the issue and resolved it.

**Answer to 3:** Claude suggested the wrong syntax for *test_guess_too_high*, *test_guess_too_low* and *test_winning_guess* in the pytest script, so I hard-coded the output to align with the expectation. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?



**Answer to 1:** if it is possible to write a pytest to test it, do it and make sure it passes. Otherwise, open Streamlit to test whether the bug is fixed.

**Answer to 2:** I was trying to test the attempt counting behavior by keep guessing the wrong number until the game ends. It appears that the game ends prematurely when there is still one attempt left. So I investigate the code and discovered that "if "attempts" not in st.session_state:
    st.session_state.attempts = 1" in app.py should have the value set to be 0 instead of 1. This along does not change the behavior, as I also discover that the guess input/buttons render before the game checks if it's already over, so I need to change the order in which the status != playing check is run. 

**Answer to 3:** AI helps a lot in identifying the root causes and pointing me to the right piece of code where the problem occurs. 

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

**Answer:** Streamlit reruns, it wipes out all the variables and states of the site and starts afresh. On the good side the UI is always in sync with the data. The drawback is that it is very inefficient, making it difficult to scale the site. 

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.



**Answer to 1:** keep a running record of discovered bug, and pay attention to bugs that emerged out of a previous bug's resolution. 

**Answer to 2: ** I would prefer using Claude Code, since it is up-to-date in terms of context as you make the edits. In Claude chat it will gradually lose focus if you just upload the static files to Claude chat.

**Answer to 3:** I personally think that AI generated codes can be very helpful at debugging, but we cannot 100% trust them. We still need to make sure proper test cases are written for all testable functionalities. 

