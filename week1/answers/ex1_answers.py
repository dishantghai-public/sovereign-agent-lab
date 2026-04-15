"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True   # True or False
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """
All three conditions produced correct answers, but the model's choice of which
correct pub to name differed by format. The PLAIN condition returned "The Haymarket
Vaults" (180 tokens), while XML and SANDWICH both returned "The Albanach" (251 and
289 tokens respectively). This suggests that structured formatting — XML tags and
sandwich-style context repetition — shifted the model's attention toward a different
valid answer within the context, even though the large model (Llama-3.3-70B) was
robust enough to extract a correct answer in every case. The token count increase
from PLAIN → XML → SANDWICH is expected: XML wrappers and repeated instructions
literally add more tokens to the prompt, which the model then processes.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_B_XML_ANSWER      = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
Neither distractor caused an error with the large model, but The Holyrood Arms
(capacity=160, vegan=yes, status=full) is the harder of the two. It satisfies
two of the three constraints — capacity ≥ 160 AND vegan=yes — and only fails
on status=full. The other distractor, The New Town Vault (capacity=162, vegan=no,
status=available), fails on the vegan requirement which is a simple binary field.
The Holyrood Arms requires the model to evaluate all three constraints and
specifically check availability last, after two conditions already match, making
it far more likely to produce a false positive in a weaker model. 

But in our case, the pattern "PLAIN → Haymarket Vaults" was identical between Part A and Part B, confirming the
distractors had zero influence on Llama-3.3-70B model's output.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True   # True or False

PART_C_PLAIN_ANSWER    = "Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C ran the same three conditions on the small model (google/gemma-2-2b-it, ~2B
parameters). Surprisingly, all three conditions were still marked correct. However,
there are subtle differences worth noting. The PLAIN answer was "Haymarket Vaults"
(without the article "The"), while XML and SANDWICH both returned the fully-formed
"The Haymarket Vaults". This indicates that even a 2B model can locate the right
answer when it is directly present in context, but PLAIN formatting produced a
slightly less precise extraction — dropping the article — which is a small sign
of weaker instruction-following. The token counts for the small model were very
close to Part B's counts (214 vs 213, 316 vs 302, 357 vs 340), confirming the
prompts were nearly identical. The result that the small model still succeeded
across all formats suggests this particular retrieval task may not have been
difficult enough to expose formatting sensitivity; a longer context, more
distractors, or a more complex multi-hop question would likely reveal clearer
degradation under PLAIN formatting for the small model.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """
Context formatting matters most when the model is small or the context is long and
noisy. A large model like Llama-3.3-70B extracted the correct answer regardless of
whether the context was plain prose, XML-tagged, or sandwich-wrapped — demonstrating
intrinsic robustness to format variation. The small model (Gemma-2-2B) also succeeded
here, but showed a tell: PLAIN formatting produced a slightly degraded extraction
("Haymarket Vaults" without the article 'The' ), hinting that structured formatting provides
extra scaffolding that smaller models rely on more heavily. In production, where
context windows are packed with multiple documents, distractors, and interleaved
instructions, XML tags and sandwich-style repetition can act as explicit attention anchors,
helping weaker models locate the relevant passage and follow the instruction precisely.
We will definitely expend more tokens, but the benefits should scale with model weakness and task
complexity.
"""
