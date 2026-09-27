# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error | Suspected **Code Location** | Fixed? |
|-------|-------------------|-----------------|------------------------|------------------------|------------------------|
| Number guessed < Secret or > Secret | Hint should say go higher/lower. | It is reversed. When Number guessed <Secret hint says go lower, and when Number guessed > Secret hint says go higher. | None | check_guess | Yes |
| Keep guessing when there is 2 attempts left | there will be 1 attempt left and the system should allow you to keep guessing if the 2nd last guess is not correct | "Out of attempts!" | None | line 182-187 |  |
| click "New Game" button after finishing a game | The text still says "Game over. Start a new game to try again", even though the Secret is getting refreshed | The text still says "Game over. Start a new game to try again", even though the Secret is getting refreshed | None |  |  |
| Change difficulty setting, and then click on new game | Change difficulty between Easy/Normal/Hard, the secret should fall in the specified range | The secret can fall outside of the range when difficulty = easy or normal. | None |  |  |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
