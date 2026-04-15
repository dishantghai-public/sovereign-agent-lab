"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = ["check_pub_availability","calculate_catering_cost","get_edinburgh_weather","generate_event_flyer"]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = False

# Optional — anything unexpected.
# If you used a non-default model via RESEARCH_MODEL env var, note it here.
# Example: "Used nvidia/nemotron-3-super-120b-a12b for the agent loop."
TASK_A_NOTES = """
    I ran two different runs, and in the first run, the agent ran the check_pub_availability tool twice 
    once for The Albanach and once for The Haymarket Vaults.
    That result is now overridden by the latest run in outputs/ex2_results.json.
    In the Latest run, he agent checked both The Albanach and The Haymarket Vaultts even though 
    The Albanach alone already satisfied the constraints. This reflects the non-deterministic nature of the agent run trajectory.
    """
    
# ── Task B ─────────────────────────────────────────────────────────────────
#
# The scaffold ships with a working generate_event_flyer that has two paths:
#
#   - Live mode: if FLYER_IMAGE_MODEL is set in .env, the tool calls that
#     model and returns a real image URL.
#   - Placeholder mode: otherwise (the default) the tool returns a
#     deterministic placehold.co URL with mode="placeholder".
#
# Both paths return success=True. Both count as "implemented" for grading.
# This is not the original Task B — the original asked you to write a direct
# FLUX image call, but Nebius removed FLUX on 2026-04-13. See CHANGELOG.md
# §Changed for why we pivoted the task.

# Did your run of the flyer tool produce a success=True result?
# (This will be True for both live and placeholder mode — both are valid.)
TASK_B_IMPLEMENTED = True   # True or False

# Which path did your run take? "live" or "placeholder"
# Look for the "mode" field in the TOOL_RESULT output of Task B.
# If you didn't set FLYER_IMAGE_MODEL in .env, you will get "placeholder".
TASK_B_MODE = "placeholder"

# The image URL returned by the tool. Copy exactly from your terminal output.
# In placeholder mode this will be a placehold.co URL.
# In live mode it will be a provider CDN URL.
TASK_B_IMAGE_URL = "https://placehold.co/1200x628/1a1a2e/eaeaea?text=The+Haymarket+Vaults+%7C+160+guests&id=2ef939fbbaf6"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "The Haymarket Vaults is confirmed for 160 guests tonight. Generate a promotional flyer with the theme 'Edinburgh AI Meetup, tech professionals, modern venue'."

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
TASK_B_WHY_AGENT_SURVIVED = """
The agent interacts only with the tool's stable interface or the output contract (name, inputs, outputs),
,not with the underlying image provider, so when FLUX was removed the tool silently
fell back to placeholder mode and still returned success=True — the agent's
decision-making loop saw an identical response shape  and continued without
any modification to its own code or prompts.
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
The first tool response showed that The Bow Bar's capacity is 80, which is too small. 
So then I checked The Albanach next. The response for The Albanach says it has a capacity of 180 and meets all constraints, including vegan options.
That's perfect because the user needs space for 160 people. Since The Albanach is available and meets the requirements,
I should confirm that this is the venue they can use.
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False       # True or False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
None of the known Edinburgh venues can accommodate 300 people with vegan options. 
The maximum capacity among the checked venues is 200 (The Guilford Arms), but it lacks vegan options. 
The largest venue with vegan options (The Albanach) only holds 180 people. You may need to consider alternative venues outside this list or adjust your requirements.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False   # True or False

SCENARIO_3_RESPONSE = """
I don't have access to real-time train schedules or transportation data. 
For the most accurate information about the last train from Edinburgh Waverley to London, I recommend checking:
\n1. The National Rail website (https://www.nationalrail.co.uk)
\n2. Train service apps like Citymapper or Trainline
\n3. The specific train operator's website (e.g., LNER)
\n\nWould you like help with anything related to Edinburgh pubs, weather, or event planning instead?
"""

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
Event though the agent didn't call a tool, as it doesn't have access to real-time train schedules, 
it still provided a response that it thought would be helpful to the user's request and offered helpful alternatives on its own from its model internal unreliable knowledge base.
This is NOT ACCEPTABLE for a real booking assistant as it is not supposed to answer questions that are out of scope. This may lead to many problems like
Firstly, it is wasting Model Tokens on something unrelated to the booking assistant's purpose. 
Secondly, who is responsible for any out-of-the-scope, incorrect information provided by the agent?
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        agent(agent)
        tools(tools)
        __end__([<p>__end__</p>]):::last
        __start__ --> agent;
        agent -.-> __end__;
        agent -.-> tools;
        tools --> agent;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
The LangGraph graph is a dynamic, two-node cycle (agent ↔ tools) where the
agent decides at runtime whether to call another tool or terminate — the graph
has no knowledge of which tools will be called or in what order.
Rasa's flows.yml, by contrast, is a static, declarative flow definition: each
step, branch, and tool call is enumerated explicitly in YAML before runtime,
making the control flow deterministic and auditable at design time.
LangGraph trades predictability for flexibility (the agent can chain arbitrary
tool sequences), while Rasa trades flexibility for transparency and reliability
(every possible path is visible in the flow file, simplifying testing and
compliance review).
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
At first glance, the response that the agent gave for SCENARIO 3 was unexpected, as it provided a made-up,  
out-of-scope suggestion for where to look for train-related details. instead of just saying something like "I can't help with that."
But on reflection, this is the default behaviour of an LLM - 
In the absence of clear System Prompt instructions / Guardrails, it will try to answer any question from its Model's internal knowledge base from its parameters, when it doesn't have the right tools to help with the user's request.
Which indeed is the main cause of this failure in our case.
"""