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

**Your answer (decided 3 Nov):**
> **3 agents.** Two is only a pair; three is the smallest real group (someone can be outvoted, a free-rider can hide), and it fits the A→B→C→A checking loop while keeping costs low.
>
> **Models:** 2 hosted models from **different companies** + 1 **self-hosted** model on a rented GPU (vLLM, Week 3; Ollama qwen2.5:3b as the free fallback). Self-hosting is the independent setup Prof. Jin asks for.
>
> **Second condition:** a **same-model village** (3 copies of one model) to compare against the mixed village in experiment A. I'll run it on my self-hosted model, so the copies cost only GPU time, not per-token fees.
>
> **Exact hosted models:** chosen in Week 5 after checking current OpenRouter prices (free models get rate-limited). Budget ~$5 of credit.
>
> **Names:** neutral (Agent A, B, C), with the **same instructions** for all, so the model is the only difference between agents (the control).

## 3. What tools does each agent get?
**Decide:** the tool list, and what each one is allowed to do.
**Options:** Python runner (inside Docker) · web search · notes file (memory) · send a message to the group chat · read the chat.
**Jarvis suggests:** text-only tools: `run_python`, `web_search`, `read_notes` / `write_notes`, `post_message`. No clicking a screen, because GUI use was AI Village's main failure point. Which search service to use can wait until Week 4.

**Your answer (decided 3 Nov):**
> Text-only tools; my code runs every one, and it decides whether each call is allowed.
>
> | Tool | What it does | Why |
> |---|---|---|
> | `run_python` | Runs code in a **Docker container**: no internet, 10-second limit, memory limit, thrown away after the run | Bad or harmful code only affects the box |
> | `search_library` | Searches a **fixed library** of ~30 saved pages on the topic | Every run sees the same pages (**reproducible**), it's free, and I can **plant the false fact** in one page. Live web search is used only for the demo |
> | `read_notes` / `write_notes` | The agent's **private** memory file | Models forget between calls; the chat is already the shared space |
> | `post_message` | Says something in the group chat | Reading isn't a tool: the last 20 messages are shown at the start of each turn (fewer tools = fewer mistakes) |
> | `add_claim(text, source)` / `check_claim(claim, verdict, reason)` | Adds a claim marked *unchecked*; **only a different agent** can mark it correct / wrong / unsure. Only *correct* claims go in the briefing | Every check is saved as **data**, so "checked by" tags and catch rates come out automatically, and the code enforces "no checking yourself" |
> | `claim_tokens(amount)` *(B only, Week 7)* | Claims tokens from the shared pool each round | The real-commons game |

## 4. How does the group chat work?
**Decide:** where messages are stored, and what each agent sees.
**Options:** every agent sees every message · each agent sees only the last N messages · a summary of older messages.
**Jarvis suggests:** store every message in an append-only file (one JSON line per message). Each agent sees the **last 20 messages + its own notes file**. Showing everything eventually overflows the model's context, and models lose track of the middle of long inputs (paper 1, *Lost in the Middle*).

**Your answer (decided 3 Nov):**
> - **Storage:** `chat.jsonl`, one JSON line per message, **append-only** (added to the end, never edited). The dashboard and the analysis both read the same file.
> - **Each message:** `time, round, sender, text`. Without who and when, nothing can be analysed (e.g. "C promised 10 in round 3, then took 25").
> - **What each agent sees:** the **last 20 messages + its own notes**. The full chat would overflow the context, get slower and costlier, and models lose the middle of long inputs (*Lost in the Middle*).
> - **Public only:** no private messages, so the dashboard and analysis see everything. Secret deals are a future idea.
> - **Length cap:** ~300 words per message, so no agent floods the chat, and it saves tokens (which matters in B).
> - **On/off switch:** the experiments compare **chat vs no chat**.
> - **No human messages during a run:** I only have the kill switch, so runs stay comparable.

## 5. Who speaks when? (the turn scheduler)
**Decide:** the order agents take turns in, and how much each can do per turn.
**Options:** round-robin (A → B → C → A …) · random order each round · all at once.
**Jarvis suggests:** **round-robin**. In one turn an agent may make up to **5 tool calls** (your `range(5)` from Week 1), then must post a message or pass. Simple, fair and easy to debug.

**Your answer (decided 3 Nov):**
> - **Order:** rotating round-robin (round 1 A-B-C, round 2 B-C-A, round 3 C-A-B…), so no agent always goes first (**first-mover bias**).
> - **Games (fish + B):** choices are made **at the same time**: each agent chooses secretly, all choices are revealed together, then they chat. Like GovSim, so the results can be compared.
> - **Per turn:** up to **5 tool calls**, then the agent must post a message or **pass** (passing is allowed and logged).
> - **Length:** briefing up to **20 rounds**; fish game: the **same number of rounds as GovSim** (set when I read the paper).
> - **When an API fails:** two kinds of failure are kept apart. **Agent failures** (bad tool call, broken JSON, poor decisions) are behaviour and count in the results. **Infrastructure failures** (API down, 429, timeout) are plumbing and must not distort the results:
>   1. Retry up to **3 times** (wait 5 s, 15 s, 45 s).
>   2. **Briefing:** if it still fails, skip that turn and log it. **Games:** the round **pauses** (nobody moves); if still down after **5 minutes**, the run stops and is marked *infrastructure failure*.
>   3. **Rule fixed in advance:** infrastructure-failure runs are kept in the logs, left out of the results, re-run, and **reported** (e.g. "2 of 27 runs re-run due to API outages"). Deciding this before seeing results prevents **cherry-picking**.

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
