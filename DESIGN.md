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

**Your answer (decided 3 Nov; revised 3 Nov after the bias audit):**
> **3 agents.** Two is only a pair; three is the smallest real group (someone can be outvoted, a free-rider can hide), and it fits the A→B→C→A checking loop while keeping costs low.
>
> **Models:** three models in the **same size class (~7–9B)** from **three different companies**: 1 **self-hosted** on a rented GPU (vLLM, Week 3; Ollama qwen2.5:3b as the free fallback) + 2 **hosted** (OpenRouter). Self-hosting is the independent setup Prof. Jin asks for. Same size class, so "mixed vs same" can't secretly mean "big vs small".
>
> **Group types:** a same-model group for **each** model (AAA, BBB, CCC) plus the mixed group (ABC). The **diversity effect** = ABC compared with the average of AAA, BBB and CCC. These contain exactly the same models, so strength is matched by design. *(Revised: before, the only same-model group was the self-hosted one, so a difference could have come from model strength.)* Small hosted models cost about a cent per run, so the hosted same-model groups are affordable.
>
> **Exact models:** chosen in Week 5. Each must pass a **pre-flight test** (20 tool calls, at least 18 correct) and be pinned to one provider on OpenRouter.
>
> **Demo vs experiment:** the public demo may use stronger hosted models. **Results come only from the matched set**, and the README says so.
>
> **Same settings for all:** the same system prompt, temperature and max output length, logged with every call.
>
> **Names:** neutral (Agent A, B, C), so the model is the only difference between agents (the control).

## 3. What tools does each agent get?
**Decide:** the tool list, and what each one is allowed to do.
**Options:** Python runner (inside Docker) · web search · notes file (memory) · send a message to the group chat · read the chat.
**Jarvis suggests:** text-only tools: `run_python`, `web_search`, `read_notes` / `write_notes`, `post_message`. No clicking a screen, because GUI use was AI Village's main failure point. Which search service to use can wait until Week 4.

**Your answer (decided 3 Nov; revised 3 Nov after the bias audit):**
> Text-only tools; my code runs every one, and it decides whether each call is allowed.
>
> | Tool | What it does | Why |
> |---|---|---|
> | `run_python` | Runs code in a **Docker container**: no internet, 10-second limit, memory limit, thrown away after the run | Bad or harmful code only affects the box |
> | `search_library` | Searches a **fixed, read-only library** of ~30 saved pages on a topic from **after the models' training cutoff** (e.g. a 2026 event) | Every run sees the same pages (**reproducible**), it's free, and the models can only know the topic **from the library, not from memory**. Live web search is for the demo only |
> | `read_notes` / `write_notes` | The agent's **private** memory file, **capped at 500 words** | Models forget between calls. The cap keeps every prompt a similar size, so no agent silently runs out of context |
> | `post_message` | Says something in the group chat. **Free in B** | Reading isn't a tool: the last 20 messages are shown each turn. Free, so "chat on" never costs pool units |
> | `add_claim(text, source)` / `check_claim(claim, verdict, reason)` | Adds a claim marked *unchecked*; **only a different agent** can mark it correct / wrong / unsure. Only *correct* claims go in the briefing | Every check is saved as **data**, so catch rates come out automatically, and the code enforces "no checking yourself" |
> | `claim_units(amount)` *(B only, Week 7)* | Claims **work units** from the shared pool each round | The real-commons game (see below) |
>
> **Planted false facts (experiment A):** a pool of **9 false facts**. Each one is **contradicted by at least one other library page**, so catching it takes checking, not memory. **3 per run**, each on a page central to its section (so it's likely to be used). Which facts go in which sections follows a **fixed rotation schedule**, so every fact and section is used equally across conditions. I measure three things:
> 1. **exposure:** did the fact become a claim at all?
> 2. **catch rate:** of the exposed facts, how many were marked wrong?
> 3. **false alarms:** true claims marked wrong.
>
> **B's pool in work units, not tokens:** one price list for every model (search = 2, read a page = 1, write 100 words = 1, add or check a claim = 1; chat and notes are free). Tokens differ between models and reading the chat would drain them, so tokens would make the comparison unfair. Real tokens and cost are still logged alongside.
>
> **Fresh start every run:** each run gets its own folder `runs/<run_id>/` (chat, notes, sandbox, logs). Nothing carries over between runs, and parallel runs can't mix.

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
> - **Status block (added 3 Nov):** every turn, each agent also sees a **status block** written by my code: round number, lake or pool size, everyone's past choices, the agent's own score. It's shown in **both** chat on and chat off, so "chat off" removes talking only, not information.
> - **Too long = rejected, never cut (added 3 Nov):** a message over 300 words comes back as an error the agent can read ("Too long: 412 words, max 300. Shorten and resend."), and the rejection is logged. Silently cutting it would make an agent look like a poor communicator because of my code.

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

**Your answer (decided 5 Nov):**
> - **"Done" is checked by my code, not claimed by an agent:** the briefing is complete when all 3 sections are submitted (new small tool: `submit_section`) and every claim in them has been checked. The code checks **completeness**, not quality; quality is measured in the analysis.
> - **Every way a run can end is recorded as its end reason:**
>
> | End reason | When |
> |---|---|
> | `completed` | The code confirms the briefing is done |
> | `collapsed` | The fish lake drops below 5, or B's token pool hits 0 |
> | `max_rounds` | 20 rounds (briefing) or GovSim's round count (game) |
> | `stalled` | 3 rounds in a row with nothing new (everyone passes, no new claims) |
> | `budget` | The money cap is hit (§7) |
> | `killed` | I pressed the kill switch (§7) |
> | `infra_failure` | The API was down for over 5 minutes (§5) |
>
> - **However it ends, the run always saves its logs and writes `summary.json`** (end reason, rounds, total cost, time taken), even after a crash, so dozens of runs can be counted instantly.

## 7. Budget caps and the kill switch
**Decide:** hard limits, and how you stop a run instantly.
**Options:** a dollar cap per run · a token cap per agent · a time limit · a kill switch (Ctrl+C handled cleanly, or a `STOP` file the loop checks).
**Jarvis suggests:** **$0.50 per run** and a token cap per agent, enforced **in your code** and also by the OpenRouter credit limit (two locks). A `STOP` file the loop checks each turn, plus a clean Ctrl+C.

**Your answer (decided 5 Nov):**
> - **How the cap works:** every model reply reports its tokens; cost = tokens × that model's price, added to a running total after each call. Hitting a cap ends the run with reason `budget`.
> - **Per run:** **$0.50**.
> - **Per agent:** ~**50,000 tokens** per run, so one looping agent can't eat the whole budget. (In experiment B, the shared token pool is part of the *game*; this cap is a separate guard rail above it and never changes between conditions.)
> - **Per day:** **$2** across all runs, tracked in `costs.jsonl`. The village refuses to start a new run once today's limit is spent.
> - **Outside lock:** the OpenRouter key's own credit limit ($1 now; ~$5 for the village weeks). If my code's caps fail, OpenRouter still refuses to spend more.
> - **Rented GPU** (billed per hour, so the risk is forgetting to switch it off): a max-hours rule per session, a shutdown checklist in `SETUP.md`, and a phone alarm.
> - **Kill switch:** Ctrl+C **and** a `STOP` file checked before every turn (works for background runs; later a dashboard Stop button creates it). Both end cleanly: logs + summary saved, end reason `killed`.
> - **Develop for $0:** build and test on local Ollama; paid models only for real runs.
> - **Where the self-hosted model runs:** practise vLLM on **Colab free** (no cost), then run the real village on a **rented GPU**. Colab disconnects, has no guaranteed GPU, and isn't built to be a server, so it's not reliable for dozens of 30-minute runs. A rented server is also the stronger "server I set up" evidence.

## 8. What gets logged?
**Decide:** the fields in each log line.
**Jarvis suggests:** one JSON line per step: `time, run_id, round, agent, model, prompt_tokens, output_tokens, cost, tool_name, tool_args, tool_result, message`. If it isn't in the log, it can't be in your results.
**Also log (3 Nov audit):** the **provider** that served each call, `temperature`, the **raw model output** (so plumbing errors can be told apart from agent errors), a flag when a prompt hit the context limit, and, in `summary.json`, the **git commit** and condition.

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
**Jarvis's proposed experiment plan after the bias audit (3 Nov).** You decide; write your version below.

| Experiment | Group types | Runs | Main measures |
|---|---|---|---|
| **A: truth** (must-have) | AAA, BBB, CCC, ABC | 10 each = 40 | Exposure, catch rate, false alarms |
| **Fish: sanity check against GovSim** (must-have) | AAA, BBB, CCC, ABC, using GovSim's exact settings | 10 each = 40 | Survived yes/no **plus** rounds survived, catch ÷ safe catch, total harvest, fairness |
| **B: real commons** (upgrade, cut first) | ABC, work-unit pool | 10 (compared with ABC fish) | The same game measures |
| Chat off (optional, cut second) | ABC fish, chat off | 10 | The same game measures |
| ~~Village vs solo~~ | Dropped for now (future idea; would need an equal budget) | | |

How the runs are done:
1. **Pilot first (Week 7):** 3 runs per group type, **not counted in the results**. Check for a **floor or ceiling**, e.g. every group collapses in round 1, or every lie is caught. If one appears, only the adjustments written down in advance are allowed (e.g. the reasoning hint GovSim itself tested; check paper 12).
2. **Pre-register,** then **freeze** the code (`git tag experiment-v1`).
3. **Rotate:** which agent writes which section, and the direction of the checking loop (A→B→C or A→C→B), follow a fixed schedule.
4. **Run:** shuffle the run order across conditions; pin the providers; run 3–4 runs in parallel (each in its own folder). Q5's infrastructure-failure rule applies.
5. **Report:** rates with 95% ranges, called **exploratory**. Judge quality (if at all) with a model **outside** the village. **Hide condition labels** when sorting failures.

Rough size: ~90–100 runs. A runs take ~15 min, fish runs ~5 min, 3–4 at a time → **~8–10 h of running** over 2–3 GPU sessions.

**Your answer:**
> _write here_

## 12. Architecture diagram
Draw boxes and arrows: agents, the models behind them, tools, the group chat, the scheduler, logs and the dashboard. Use [Excalidraw](https://excalidraw.com) (free, in the browser), export a PNG to `docs/architecture.png`, and link it here. The rough version in `PROJECT-MASTER.md` §1 is a starting point.

> _diagram link here_
