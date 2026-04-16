"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "It seems there are no currently available venues in Edinburgh that can accommodate 300 people with vegan options. Would you like to:\n1. Try reducing the minimum capacity requirement?\n2. Check for venues without vegan-specific requirements?\n3. Search for smaller venues and consider booking multiple spaces?\n\nLet me know how you'd like to proceed!"

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
After making the "The Albanach" venue's capacity to be full in mcp_venue_server.py, 
The 'search_venues' tool now does not return that venue ("The Albanach") in its filtered search results.
There was no change required on the Client/Agent side of code, as the tool is now dynamically discovered and executed, 
and pick up the updated data that could have been provided by the external server.
This change demonstrates the power of the MCP pattern: the tool's behavior is now driven by the external server's logic, not hardcoded in the agent. 
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 117   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 0   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP is providing runtime tool discovery, process isolation, and framework-neutral access beyond just separating tools into a file. 
MCP is acting as a Single Source of Truth for two very different Agent Architectures - 
LangGraph: the Autonomous Loop and RASA: the Structured Agent can connect to the same MCP 
server simultaneously, discovering and calling identical tools without code duplication. 

When venue data changes in the server, both agents automatically get updated behavior without modifying any agent code. 
The tools are language-agnostic, discoverable at runtime rather than import time, and can be versioned/deployed independently of the agents that consume them.

This MCP Shared Tools Layer will act as future PyNanoClaw's nervous system - 
it lets the autonomous LangGraph half and structured Rasa half share the same tools (venues, bookings, email) 
without duplicating code or tightly coupling. Both agents discover tools at runtime from the MCP server,
enabling seamless handoffs between exploration and confirmation while maintaining a single source of truth for all capabilities.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- Planner: The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
  Qwen3-Next-Thinking) that takes the raw task and produces an ordered
  list of subgoals. It lives upstream of the ReAct loop in the
  autonomous-loop half of PyNanoClaw, so the Executor never sees an
  ambiguous task.

- Executor: The Executor is a ReAct loop powered by LangGraph that executes the subgoals produced by the Planner. 
  It lives in the autonomous-loop half of PyNanoClaw. The Current sovereign_agent/agents/research_agent.py 
  will become a part of the Executor. The Executor will use the MCP tools to execute the subgoals.

- RASA Structured Agent: The RASA Structured Agent is a Rasa-based agent that handles the conversational flow and business logic. 
  It lives in the structured agent half of PyNanoClaw. The Current exercise3_rasa/actions/actions.py will become a part of the RASA Structured Agent.
  But the RASA actions become a thin wrapper that calls the MCP tools for any Business Logic.

- Tools: All the Tools like sovereign_agent/tools/venue_tools.py will become MCP tools that the Executor can use via the MCP server.
  It lives in the shared layer (MCP Server) between the autonomous loop and the structured agent.

- Memory store: A persistent storage for the agent's memories. It lives in the MCP Server that becomes the shared layer between the autonomous loop and the structured agent as all the tools will be running on the same component - the MCP server.
  This will also enable the structured agent to access the memories of the autonomous loop via the MCP server's exposed Memory tools. There will 
  
- Handoff bridge: A component that enables the structured agent to hand off control to the autonomous loop. It lives in the shared layer (MCP Server) between the autonomous loop and the structured agent.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
LangGraph should handle the research phase, while Rasa CALM should handle the confirmation call. 
In my runs, LangGraph autonomously chained tools (checked both venues, calculated costs, checked 
weather, generated flyer) without being told the exact order - it figured out dependencies like 
"need venue confirmed before calculating catering." When faced with impossible constraints (300 
guests), it systematically checked all venues and correctly reported none could accommodate. 
However, for out-of-scope requests (train times), it hallucinated some suggestions from its 
training data instead of staying within bounds, which needs to be fixed with Guardrails and overall System Design. 

Rasa CALM, conversely, followed a rigid flow - 
it asked for guest count, vegan count, and deposit in that exact order every time. It correctly 
rejected out-of-scope requests but then got stuck in a loop trying to resume the conversation.
Which Means all the Paths of the deterministic high-stakes flows should be meticulously designed 
and incorporated into the System (data/flows.yml) and tested for coverage. 
Swapping these roles feels wrong because research requires flexibility to explore unknown paths 
(what if there are 10 venues to check?), while confirmation calls need predictable guardrails 
to prevent costly mistakes with real money and commitments.
"""