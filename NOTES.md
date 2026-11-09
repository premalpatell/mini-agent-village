# Dev log

## 31 Oct 2026
- Installed Ollama 0.40.13; qwen2.5:3b (1.8 GB) runs 100% on GTX 1050 Ti
- Built first agent: model + calculator tool + think → tool → answer loop
- Findings: claimed to be made by Anthropic (hallucination); thinks it's 2023;
  used ^ for powers and repeated the mistake after the error
- Fix: clearer tool description + error message → power question 1/3 → 10/10

## 1 Nov 2026
- Added a 2nd tool (get_today) + `functions` dict so the loop can call any tool by name
- Bug found in testing: model passed a made-up argument → whole script crashed.
  Fix: try/except turns tool errors into text for the model. 10 runs: 0 crashes, 9/10 correct
- Model sometimes calls get_today 3–6 times for one question (wasteful but harmless)
- Same loop on a hosted model through OpenRouter: only the client and model name change
- Trained nanoGPT from scratch on Tiny Shakespeare (Colab T4, 10.6M parameters).
  Best val loss 1.46 at step 1750; after that train loss kept falling but val loss rose
  (overfitting), so the best checkpoint is the one to keep (early stopping)
- Started DESIGN.md: 12 decisions to make before writing village code

## 3 Nov 2026
- Design Q1–Q5 decided: owned sections with cross-checking, 3 agents, group chat, rotating turns
- Hidden-bias audit of my own design found 15 confounds. The big ones:
  - "mixed vs same model" could secretly mean "big vs small" → all models in one size class
  - models might know the library topic from training → a topic from after their training cutoff
  - a token budget is unfair because models count tokens differently → work units
- Added a pilot and pre-registration so results can't be tuned after seeing them

## 5 Nov 2026
- Design Q6–Q11 decided: code-checked "done", end reasons, budget caps + kill switch,
  logging, safety (allowlist + argument validation), a 10-test checklist
- What-could-go-wrong review: 20 failure scenarios, fixes written into the design
  (one of them: real news in a public repo means publishing false facts about real
  events, so the library became a fictional topic with an answer key)
- My first token cap (50k per agent) would have ended every run as `budget`;
  estimate is ~300k, and the real caps get set from the pilot
- Swapped the planned chat-off condition for a mediator: GovSim already showed
  talking matters, so chat-off would only replicate it; a mediator extends CoopEval
- Wrote my predictions down before any run

## 7 Nov 2026
- Design Q12: architecture diagram as SVG, exported to PNG with a headless browser
- Tidy pass on DESIGN.md: clean v1 for readers; the full decision log stays in git
- Publish prep: secrets scan, private study notes removed from the git history,
  commits moved to GitHub's no-reply email, README + MIT licence + references

## 9 Nov 2026
- Replaced `eval` in the calculator. The character allowlist already blocked injected
  code, but `9**9**9**9` would hang it. New version walks the parsed expression
  (`ast`), runs only + - * / ** on numbers, and caps powers. 14 test inputs pass
