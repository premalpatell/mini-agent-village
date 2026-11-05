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
> **Added 5 Nov (review):** **temperature 0.7** for every agent (at 0, the three copies in AAA would act almost identically every run). Agents are **never told which models are in their group**, in any condition, because knowing "we're mixed" would be a second difference. The prompt **never mentions the experiment** ("we're testing whether you catch lies" would change behaviour). The exact prompt text is fixed before the experiment and published.
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
> | `run_python` | Runs code in a **Docker container**: no internet, 10-second limit, memory limit, thrown away after the run | Bad or harmful code only affects the box. **Revised 5 Nov:** used in the Week 4 single-agent milestone and the demo, **not in the experiment tool set**. The experiments don't need it, every extra tool makes small models less reliable, and it takes Docker off the experiment's critical path |
> | `search_library` | Searches a **fixed, read-only library** of ~30 pages. **Revised 5 Nov:** the topic is **fictional but realistic** (e.g. a made-up town's 2026 flood-defence project), drafted by a model **outside** the village and checked by hand | No model can know it from memory (stronger than "after the cutoff"), every run sees the same pages (**reproducible**), it's free, it can be **published** without copyright problems, and planted false facts are **never about real people or events**. Live web search is for the demo only |
> | `read_page(page_id)` *(added 5 Nov)* | Returns the full text of one library page | Search returns short snippets; checking a claim properly needs the whole page. It was already in B's price list (read a page = 1) but missing from this table |
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
>
> **Added 5 Nov (review):**
> - **Ground truth is fixed in advance:** every true fact appears on **at least 2 pages**, one of them an "official" page (e.g. the council report). Each planted false fact appears on **exactly 1 page**. An answer key (`library/answer_key.json`) lists every true and false fact; agents never see it.
> - **How verdicts on a planted fact are scored:** `wrong` = **caught**, `unsure` = **flagged** (reported separately), `correct` = **missed**. Claims marked `unsure` don't enter the briefing.
> - **Rubber-stamping is measured:** a checker who marks claims "correct" without looking. `check_claim` also takes `evidence_page`; the code logs whether the checker actually searched or read that page earlier in the run. **% of checks with no evidence looked at** is a measure.
> - **No hiding from the test:** each section needs **at least 5 claims marked correct** to be submittable, so an agent can't avoid mistakes by making no claims.
> - **The library file carries a warning:** "contains deliberately false statements for research", so nobody mistakes it for real information.

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
> - **On/off switch:** kept as a setting. **Changed 5 Nov:** the chat-off condition was replaced by the mediator (§11), so chat-off is now a future idea.
> - **No human messages during a run:** I only have the kill switch, so runs stay comparable.
> - **Status block (added 3 Nov):** every turn, each agent also sees a **status block** written by my code: round number, lake or pool size, everyone's past choices, the agent's own score. It's shown in **both** chat on and chat off, so "chat off" removes talking only, not information. **Added 5 Nov:** in the briefing, the status block also shows each agent's **to-do list** (e.g. "your section: 3 of 5 claims checked; 2 of Agent B's claims are waiting for your check; submit by round 15"), the same in every condition, so a run doesn't stall just because an agent lost track of the steps.
> - **Too long = rejected, never cut (added 3 Nov):** a message over 300 words comes back as an error the agent can read ("Too long: 412 words, max 300. Shorten and resend."), and the rejection is logged. Silently cutting it would make an agent look like a poor communicator because of my code.

## 5. Who speaks when? (the turn scheduler)
**Decide:** the order agents take turns in, and how much each can do per turn.
**Options:** round-robin (A → B → C → A …) · random order each round · all at once.
**Jarvis suggests:** **round-robin**. In one turn an agent may make up to **5 tool calls** (your `range(5)` from Week 1), then must post a message or pass. Simple, fair and easy to debug.

**Your answer (decided 3 Nov):**
> - **Order:** rotating round-robin (round 1 A-B-C, round 2 B-C-A, round 3 C-A-B…), so no agent always goes first (**first-mover bias**).
> - **Games (fish + B):** choices are made **at the same time**: each agent chooses secretly, all choices are revealed together, then they chat. Like GovSim, so the results can be compared. **Added 5 Nov:** the choice is made through a tool, `choose_catch(amount)` (or `claim_units(amount)` in B), and the code checks it's a whole number between 0 and what's available. An invalid choice comes back as a readable error, with up to **3 attempts**. After that, the catch is 0 and the turn is flagged as an **agent failure** (it's behaviour, so it counts, and its rate is reported). The pilot checks that this is rare.
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
> - **"Done" is checked by my code, not claimed by an agent:** the briefing is complete when all 3 sections are submitted (new small tool: `submit_section`), every claim in them has been checked, and each has **at least 5 claims marked correct** (added 5 Nov). **Sections must be submitted by round 15**, which leaves 5 rounds for the last checks, so a claim added in round 19 can't make a run fail on timing alone. The code checks **completeness**, not quality; quality is measured in the analysis.
> - **Every way a run can end is recorded as its end reason:**
>
> | End reason | When |
> |---|---|
> | `completed` | The code confirms the briefing is done |
> | `collapsed` | The fish lake drops below 5, or B's work-unit pool hits 0 |
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
> - **Per agent:** a token cap per run, so one looping agent can't eat the whole budget. **Revised 5 Nov:** the cap is **set from the pilot at ~3× typical use**. My rough maths: each call sends ~5,000 tokens (instructions + status + 20 messages + notes + tool results), ~3 calls a turn, 20 rounds = **~300,000 tokens per agent per A run**. The first guess of 50,000 would have stopped *every* run as `budget`, a floor effect created by my own cap. The **$0.50/run** and **daily** caps are also re-set from the pilot (small models cost roughly 1–5 cents a run, so the daily cap is likely ~$5 in experiment week, and ~$10 of OpenRouter credit in total). Free OpenRouter models have small daily request limits, so the experiments use cheap **paid** models. (In experiment B, the shared work-unit pool is part of the *game*; this token cap is a separate guard rail above it and never changes between conditions.)
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

**Your answer (decided 5 Nov):**
> - **Format:** JSON lines, one event per line, so analysis code can read every event as data.
> - **Fields:** `time, run_id, round, agent, model, provider, temperature, event, prompt_tokens, output_tokens, cost, work_units, tool_name, tool_args, tool_result, message, context_limit_hit`. `event` = `model_call | tool_call | message | claim | check | game_choice | error`. `work_units` is what the action cost in B's pool (real tokens and cost are logged alongside).
> - **Full prompts and raw replies** go in a separate file (`prompts.jsonl`), for failure analysis (the exact text each agent saw and wrote) and to tell plumbing errors apart from agent errors.
> - **`config.json` per run:** models + providers, group type (AAA/BBB/CCC/ABC), chat on/off, caps, topic, random seed, and the **git commit ID**, so every result can be traced to the exact code and settings (**reproducibility**). `summary.json` repeats the commit and condition.
> - **Seed:** my code's own random choices use a recorded seed. A model's randomness via an API can't be fully fixed, and the report will say so.
> - **One folder per run:** `runs/<YYYY-MM-DD_HHMM_condition>/` with `config.json`, `events.jsonl`, `chat.jsonl`, `prompts.jsonl`, `summary.json`.
> - **Never logged:** API keys, request headers, `.env` values. The logs will be public.
> - **Where:** committed to git while small; over ~50 MB, zipped onto a GitHub release. Raw logs are never deleted, failed runs included.
> - **Times:** UTC (`2026-12-21T14:30:05Z`).

## 9. Safety rules
**Decide:** what agents can never do.
**Jarvis suggests:** the Python sandbox has **no network**, a 10-second time limit and a memory limit, and it's thrown away after each run. No email, no payments, no posting online, no access to your files. Agents can only use tools from the list, and your code decides whether each call runs.

**Your answer (decided 5 Nov, from the options):**
> - **Allowlist, not blocklist:** agents get **only** the tools in §3. There is no email, payment, posting or file-access tool, so those actions are impossible, not just forbidden.
> - **Every tool call is validated by my code before it runs:** the tool must be on the list · no checking your own claim · a verdict must be `correct`, `wrong` or `unsure` · page IDs (`read_page`, `source`, `evidence_page`) must be real library pages · `choose_catch` / `claim_units` must be a whole number between 0 and what's available · messages ≤ 300 words · notes ≤ 500 words · at most 5 tool calls per turn (§5). A rejected call goes back as a readable error, is logged as an `error` event (§8), **uses up one of the 5 calls** (so an agent can't loop forever), and counts as an **agent error** in the results. Game choices keep §5's rule: 3 attempts, then 0 and an agent failure.
> - **Notes tools take text only, never a file name,** and always use that agent's own file. This blocks **path traversal** (e.g. asking for `../../.env`).
> - **Python sandbox** (Week 4 agent + demo only, §3): Docker, **no network**, 10-second limit, memory + CPU limits, **non-root** user, no access to my files, thrown away after each run.
> - **Prompt injection** (text in a page that tries to give orders): tool results are wrapped and marked as **data**; the real defence is that agents have **no dangerous tools**. My library is drafted by a model outside the village and **checked by me by hand** (§3), including for instruction-like text; live web search is used only in the demo.
> - **vLLM server locked with an API key** (`--api-key`), so strangers who find its address can't use my paid GPU.
> - **Before every push:** scan for **every value in `.env`** (this catches the vLLM key, which doesn't start with `sk-`) plus `sk-`, and for personal information; confirm `.env` isn't tracked by git. Keys are never logged (§8).
> - **The library carries a warning label:** "contains deliberately false statements for research".

## 10. How will you know it works?
**Decide:** the "done when" for the village (Week 5).
**Jarvis suggests:** *"A 30-minute run finishes on the goal from §1 without me touching it, stays under budget, and the full trace is in the log."*

**Your answer (decided 5 Nov):**
> Not one good run: a **checklist**, including tests where I break things on purpose (**fault injection**), because the safety parts only run when something goes wrong.
>
> | # | Test | Passes when |
> |---|---|---|
> | 1 | Fish run on the real models | Completes end to end without me touching it |
> | 2 | Briefing run (A) | Ends `completed` within budget |
> | 3 | Run files | Every run writes `config.json`, `events.jsonl`, `chat.jsonl`, `prompts.jsonl`, `summary.json` (§8) |
> | 4 | Caps | A tiny cap ($0.01) stops the run with end reason `budget` |
> | 5 | Kill switch | A STOP file mid-run gives `killed`, with all logs saved |
> | 6 | Outages | A wrong API key gives retry → pause → `infra_failure` (§5) |
> | 7 | Parallel runs | 3 at once; each folder holds only its own run |
> | 8 | Pre-flight | Each model gets ≥ 18 of 20 tool calls right (§2) |
> | 9 | Reproducibility | The same config + seed puts the false facts in the same places |
> | 10 | Validation (§9) | Bad calls (own claim, fake page ID, catch of 999) are rejected and logged as `error` |
>
> **When:** the full checklist runs **before the pilot**, and again **after any code change** before the counted runs.

## 11. The experiment (first draft only; fixed in Week 7)
**Decide:** the research question for the GovSim-style game.
**Example:** *"Do mixed-model groups sustain a shared resource as well as same-model groups? Does open chat help?"* Another option, from AI Village: village vs a solo agent.
**Jarvis's proposed experiment plan after the bias audit (3 Nov).** You decide; write your version below.

| Experiment | Group types | Runs | Main measures |
|---|---|---|---|
| **A: truth** (must-have) | AAA, BBB, CCC, ABC | 9 each = 36 | **Primary:** catch rate of exposed facts, ABC vs the average of AAA/BBB/CCC. Secondary: exposure, false alarms, rubber-stamp rate |
| **Fish: sanity check against GovSim** (must-have) | AAA, BBB, CCC, ABC, using GovSim's exact settings | 9 each = 36 | **Primary:** rounds survived. Secondary: survived yes/no, catch ÷ safe catch, total harvest, fairness |
| **B: real commons** (upgrade, cut first) | ABC, work-unit pool | 9 (compared with ABC fish) | Primary: rounds survived |
| ~~Chat off~~ → **Mediator** (optional, cut second; changed 5 Nov) | ABC fish + a neutral mediator agent that can't fish | 9 (compared with ABC fish) | Primary: rounds survived |
| ~~Village vs solo~~ | Dropped for now (future idea; would need an equal budget) | | |

How the runs are done:
1. **Pilot first (Week 7):** 3 runs per group type, **not counted in the results**. Check for a **floor or ceiling**, e.g. every group collapses in round 1, or every lie is caught. If one appears, only the adjustments written down in advance are allowed (e.g. the reasoning hint GovSim itself tested; check paper 12).
2. **Pre-register,** then **freeze** the code (`git tag experiment-v1`).
3. **Rotate:** which agent writes which section follows a fixed schedule. The checking direction is **fixed** (A→B→C→A; see my answer below).
4. **Run:** shuffle the run order across conditions; pin the providers; run 3–4 runs in parallel (each in its own folder). Q5's infrastructure-failure rule applies.
5. **Report:** rates with 95% ranges, called **exploratory**. Judge quality (if at all) with a model **outside** the village. **Hide condition labels** when sorting failures.

Rough size: ~90 runs. A runs take ~15 min, fish runs ~5 min, 3–4 at a time → **~8–10 h of running** over 2–3 GPU sessions.

**Added 5 Nov (review):**
- **Why 9 runs, not 10:** 9 false facts form **3 sets of 3**, and there are **3 ways** to assign sections. 3 × 3 = 9 runs uses every fact set with every section assignment exactly once (**balanced**). With 10 runs, one set would be used more than the others. The checking direction stays fixed (see my answer below).
- **One primary measure per experiment, fixed in advance.** With many measures × many groups, something will look different **by luck** (the **multiple-comparisons** problem). The primary measure is the headline; everything else is reported as secondary.
- **Runs, not facts, are the unit.** The 3 facts in one run share the same agents, so they aren't independent. Ranges are worked out by **resampling whole runs** (a **bootstrap over runs**), not by treating 27 facts as 27 separate trials.
- **Build order: fish game first.** It needs no library, no claims and no sandbox, only the core village (scheduler, status block, simultaneous choices, chat, logs, caps). So it's the fastest way to a working village with a real result. Then A, then B. (A is still the must-have *experiment*; this is only the order of *building*.)
- **Where the experiment runs:** the village program runs **on the rented server**, next to vLLM, not on the laptop. A laptop that sleeps, restarts for Windows Update, or loses power or internet would kill runs. A run that dies isn't resumed: it's marked `infra_failure` and re-run (Q5 rule).
- **Gate dates:** **13 Dec**: the fish game runs end to end on the real models, or B and the mediator condition are cut at once. **20 Dec** (end of the pilot): A works, or A shrinks to ABC + the strongest same-model group, and the report says so.
- **If a hosted model or provider disappears mid-experiment:** stop, swap, and re-run **every** condition containing that model. Running all experiment runs inside a **3-day window** makes this unlikely.

**Your answer (decided 5 Nov):**
> **I accept the plan above,** with two changes decided 5 Nov:
> 1. **Mediator replaces chat-off.** GovSim already showed that talking matters, so chat-off would only replicate it. Prof. Jin's 2026 CoopEval paper found that a **neutral mediator** is one of the best ways to keep agents cooperating, so testing it in a live village **extends** her newest work. Setup: ABC fish + a 4th agent, the **mediator**, which sees the same status block, posts **one message per round before the choices** (e.g. a suggested fair catch), and **cannot fish**. It runs on one fixed model for all 9 runs (chosen at the pilot). It's compared with the 9 plain ABC fish runs. Same slot: optional, **cut second** (after B).
> 2. **Checking direction is fixed** (A→B→C→A) for all runs. Two directions can't be split evenly over 9 runs, and the fact-set balance matters more. It only affects ABC (in AAA/BBB/CCC every checker is the same model), and it's **reported as a limitation**.
>
> **Research questions:**
> - **A:** Do mixed-model groups catch planted false facts more often than same-model groups?
> - **Fish:** Do our groups sustain the lake about as well as GovSim's results suggest, and does group type matter?
> - **B:** Do agents sustain a real resource (their own work budget) better or worse than pretend fish?
> - **Mediator:** Does a neutral mediator help a mixed group keep the lake alive?
>
> **My predictions (chosen 5 Nov, before any run):**
> - **A:** mixed groups catch **more** false facts. Models from different companies are trained on different data, so their blind spots differ; three copies of one model share the same ones.
> - **Fish:** **most groups collapse.** In GovSim most models, especially smaller ones, over-fished; mine are ~7–9B.
> - **B:** the real resource is sustained **worse** than the fish. A lake running out is a vivid, familiar story; a pool of work units is abstract, so agents notice the danger less and take more to finish their own task.
> - **Mediator:** it **helps.** Prof. Jin's 2026 CoopEval paper found a neutral mediator was one of the best ways to keep agents cooperating.

## 12. Architecture diagram
Draw boxes and arrows: agents, the models behind them, tools, the group chat, the scheduler, logs and the dashboard. Use [Excalidraw](https://excalidraw.com) (free, in the browser), export a PNG to `docs/architecture.png`, and link it here. The rough version in `PROJECT-MASTER.md` §1 is a starting point.

> _diagram link here_
