# mini-agent-village: design doc

Status: **draft**. Started 1 Nov 2026.

How to use this file: each section is one decision. Read the options and Jarvis's suggestion, then write **your own answer and your reason** under "Your answer". Delete the guidance once you've decided, and the answers become the design doc (aim for 1–2 pages). You must be able to defend every answer in an interview, so pick what you understand, not what sounds impressive.

---

## 1. What is the village's goal?
**Decide:** what the agents work on together in a normal run (the GovSim game comes later, as a second mode).
**Options:** a research task (e.g. a fact-checked briefing on a topic) · a coding task (e.g. build and test a small program) · a puzzle or game.
**Jarvis suggests:** a research task with a checkable finish line, e.g. *"Produce a one-page briefing on X with at least 5 sources, every claim checked by a second agent."* It uses all three tools and can be scored, and it tests the AI Village failure where one agent's false claim spreads.
**Also consider:** a goal where agents must **cooperate or share something** (a shared budget, a shared resource, splitting the work). That brings Prof. Jin's research question (GovSim: cooperation) into the village from day one.

**Options ranked for Prof. Jin (1 Nov):**
- **A. Truth in the village:** fact-checked briefing; some runs plant a false fact. *Does checking between agents (especially different models) stop false claims spreading?* Fits multi-agent + misinformation. Safe and clear.
- **B. The real commons ⭐:** the briefing from A, but all agents share **one token pool** (their real compute) that refills a little each round; over-spending → collapse for everyone. *Do agents share a real resource better or worse than GovSim's simulated fish?* Directly extends GovSim. The code is just a *shared* budget cap.
- **C. Causal detectives:** agents uncover a hidden cause in a dataset. Fits causal reasoning, but needs knowledge you don't have yet: high risk in an interview. Future idea.
- **D. Sanctions:** avoid. Her lab already published **SanctSim**.
- **Jarvis suggests A + B, with the classic fish game as a GovSim baseline:** "replicate, then extend". Check the literature before calling B new. If time runs short, A + the classic fish game is still strong.

**Your answer (decided 3 Nov: A + B):**
> **Goal:** In a normal run, the agents split a topic into sections. Each agent researches and writes its own section, and a different agent checks every claim in it before it goes into the joint briefing (A's section is checked by B, B's by C, C's by A). The final output is a one-page briefing where every claim has a source and a "checked by" tag, plus a log of every check.
>
> **Why:** A connects to Prof. Jin's work on LLM democracy defence (stopping misinformation spreading) and on how agents behave together. It responds to the AI Village failure where o3 invented a 93-person contact list and the other agents believed it and used it. B (the real commons: one shared token pool) connects to her GovSim paper on cooperation over a shared resource, because it asks GovSim's question with a real resource (the agents' own compute) instead of pretend fish.
>
> **Done when:** a run counts as a success if the briefing is finished (every section written), every claim was checked by a different agent, and the run stayed under budget without me touching it. Whether a planted false fact gets caught is a result I measure, not a success test.
>
> **If time runs short:** I cut B first and keep A plus the classic fish game, because A proves the village works and the fish game connects to GovSim. B is the extension: worth having, but not essential.

## 2. Which agents, and which models?
**Decide:** how many agents, and which model each one runs.
**Options:** 2–5 agents · hosted models from OpenRouter (different companies) · your own self-hosted model (vLLM in Week 3; Ollama as the free fallback).
**Jarvis suggests:** **3 agents**: 2 hosted from **different model families** + 1 self-hosted. Give all three the **same system prompt**, so the model is the only thing that differs. That keeps the comparison fair later.

**Your answer:**
> _write here_

## 3. What tools does each agent get?
**Decide:** the tool list, and what each one is allowed to do.
**Options:** Python runner (inside Docker) · web search · notes file (memory) · send a message to the group chat · read the chat.
**Jarvis suggests:** text-only tools: `run_python`, `web_search`, `read_notes` / `write_notes`, `post_message`. No clicking a screen, because GUI use was AI Village's main failure point. Which search service to use can wait until Week 4.

**Your answer:**
> _write here_

## 4. How does the group chat work?
**Decide:** where messages are stored, and what each agent sees.
**Options:** every agent sees every message · each agent sees only the last N messages · a summary of older messages.
**Jarvis suggests:** store every message in an append-only file (one JSON line per message). Each agent sees the **last 20 messages + its own notes file**. Showing everything eventually overflows the model's context, and models lose track of the middle of long inputs (paper 1, *Lost in the Middle*).

**Your answer:**
> _write here_

## 5. Who speaks when? (the turn scheduler)
**Decide:** the order agents take turns in, and how much each can do per turn.
**Options:** round-robin (A → B → C → A …) · random order each round · all at once.
**Jarvis suggests:** **round-robin**. In one turn an agent may make up to **5 tool calls** (your `range(5)` from Week 1), then must post a message or pass. Simple, fair and easy to debug.

**Your answer:**
> _write here_

## 6. When does a run stop?
**Decide:** every way a run can end.
**Options:** max rounds · the goal is declared done · the budget runs out · you press the kill switch · an error.
**Jarvis suggests:** all of them. Max **20 rounds**. "Done" only counts if another agent confirms it, because AI Village agents declared success that wasn't real. Whatever the reason, **always save the logs** before exiting.

**Your answer:**
> _write here_

## 7. Budget caps and the kill switch
**Decide:** hard limits, and how you stop a run instantly.
**Options:** a dollar cap per run · a token cap per agent · a time limit · a kill switch (Ctrl+C handled cleanly, or a `STOP` file the loop checks).
**Jarvis suggests:** **$0.50 per run** and a token cap per agent, enforced **in your code** and also by the OpenRouter credit limit (two locks). A `STOP` file the loop checks each turn, plus a clean Ctrl+C.

**Your answer:**
> _write here_

## 8. What gets logged?
**Decide:** the fields in each log line.
**Jarvis suggests:** one JSON line per step: `time, run_id, round, agent, model, prompt_tokens, output_tokens, cost, tool_name, tool_args, tool_result, message`. If it isn't in the log, it can't be in your results.

**Your answer:**
> _write here_

## 9. Safety rules
**Decide:** what agents can never do.
**Jarvis suggests:** the Python sandbox has **no network**, a 10-second time limit and a memory limit, and it's thrown away after each run. No email, no payments, no posting online, no access to your files. Agents can only use tools from the list, and your code decides whether each call runs.

**Your answer:**
> _write here_

## 10. How will you know it works?
**Decide:** the "done when" for the village (Week 5).
**Jarvis suggests:** *"A 30-minute run finishes on the goal from §1 without me touching it, stays under budget, and the full trace is in the log."*

**Your answer:**
> _write here_

## 11. The experiment (first draft only; fixed in Week 7)
**Decide:** the research question for the GovSim-style game.
**Example:** *"Do mixed-model groups sustain a shared resource as well as same-model groups? Does open chat help?"* Another option, from AI Village: village vs a solo agent.

**Your answer:**
> _write here_

## 12. Architecture diagram
Draw boxes and arrows: agents, the models behind them, tools, the group chat, the scheduler, logs and the dashboard. Use [Excalidraw](https://excalidraw.com) (free, in the browser), export a PNG to `docs/architecture.png`, and link it here. The rough version in `PROJECT-MASTER.md` §1 is a starting point.

> _diagram link here_
