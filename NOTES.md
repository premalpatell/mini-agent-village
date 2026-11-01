# Dev log

## 31 Oct 2026
- Installed Ollama 0.40.13; qwen2.5:3b (1.8 GB) runs 100% on GTX 1050 Ti
- Built first agent: model + calculator tool + think → tool → answer loop
- Findings: claimed to be made by Anthropic (hallucination); thinks it's 2023;
  used ^ for powers and repeated the mistake after the error
- Fix: clearer tool description + error message → power question 1/3 → 10/10
- Time: ~X hours

## 1 Nov 2026
- Added a 2nd tool (get_today) + `functions` dict so the loop can call any tool by name
- Bug found in testing: model passed a made-up argument → whole script crashed.
  Fix: try/except turns tool errors into text for the model. 10 runs: 0 crashes, 9/10 correct
- Model sometimes calls get_today 3–6 times for one question (wasteful but harmless)

