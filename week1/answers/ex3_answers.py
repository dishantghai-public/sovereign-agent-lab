"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  hi I'm calling to confirm a booking.                                                                                                        
How many guests are you confirming for tonight's event?
Your input ->  around 160 people                                                                                                                           
And how many of those guests will need vegan meals?
Your input ->  about 50 I guess                                                                                                                            
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  200 GBP should be ok                                                                                                                        
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->      
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  Hi I am calling to confirm a booking                                                                                                        
How many guests are you confirming for tonight's event?
Your input ->  around 160                                                                                                                                  
And how many of those guests will need vegan meals?
Your input ->  about 60                                                                                                                                    
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  310 GBP shoudl be good                                                                                                                      
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £310 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £310 exceeds the organiser's authorised limit of £300."   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  hey i want to confirm a booking for the pub                                                                                                 
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                  
And how many of those guests will need vegan meals?
Your input ->  50 guests need vegan meals and only 2 people they will be coming by their bicycles so I hope they can keep those outside the pub, hope that'
s ok.                                                                                                                                                      
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  sure                                                                                                                                        
2026-04-15 16:11:39 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user said "sure" in response to the AI asking if they want to continue with the confirm booking. The current state is in a flow called pattern_continue_interrupted, and the requested slot is continue_interrupted_flow_confirmation, which is a boolean. The user\'s "sure" indicates they want to continue, so that slot should be set to True. Also, the interrupted_flow_to_continue should be set to "confirm_booking" since that\'s the flow they\'re resuming. Then, we need to start the confirm_booking flow again. Let me check the slots and flows again to make sure. The guest_count was already set to 160 and vegan_count to 50. The deposit_amount_gbp hasn\'t been mentioned yet, but the user hasn\'t provided that info yet. Since the user is continuing, the next step would be to ask for the deposit amount. But according to the instructions, I should only output the actions based on the current message. So the actions here are setting the confirmation to true, setting the interrupted flow to confirm_booking, and starting the confirm_booking flow again. Wait, but the AI already asked about the deposit, or did it? Looking back, the conversation history shows the AI asked about vegan meals, and the user mentioned 50, then the AI redirected to confirm booking. Now the user says sure, so the next step is to continue the confirm_booking flow. The next step in confirm_booking would be to ask for the deposit amount. But the AI\'s last message was "Would you like to continue with confirm booking?" and the user said "sure". So the actions here are to set the continue_interrupted_flow_confirmation to True, set the interrupted_flow_to_continue to confirm_booking, and then start the confirm_booking flow. Wait, but the current active flow is pattern_continue_interrupted. Once the user confirms, we need to transition back to the confirm_booking flow. So the correct actions would be to set the boolean slot to True, set the interrupted flow name, and then start the confirm_booking flow. Also, maybe cancel the current pattern_continue_interrupted flow? But the instructions say not to cancel unless the user explicitly requests it. Since the user is continuing, perhaps we just set the slots and start the flow. Let me check the available actions. The "start flow" action is allowed, and multiple flows can be started if needed. But in this case, the pattern_continue_interrupted is probably a helper flow to handle the interruption' message='No commands were parsed from the LLM actions.'
2026-04-15 16:11:39 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
Would you like to continue with confirm booking?
Your input ->  yeah, you can confirm the parking for 2 bicycles                                                                                            
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  yes I want to, do you have any other questions for me or is the booking confirmed ?              
2026-04-15 16:45:21 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='<think>
Okay, let\'s see. The user is trying to confirm a booking for a pub. The conversation history shows they\'ve already provided the guest count (160) and vegan count (50). The AI kept asking about continuing the booking confirmation flow. The user mentioned parking for bicycles, but the AI clarified it can\'t help with that and redirected to the event organizer.

Now, the user\'s last message is: "yes I want to, do you have any other questions for me or is the booking confirmed ?". They\'re confirming they want to proceed with the booking. The current active flow is "pattern_continue_interrupted", which is about whether to continue an interrupted flow. The slots in the current state include "continue_interrupted_flow_confirmation" which is a boolean. The user\'s "yes" indicates they want to continue, so that slot should be set to True. Also, the interrupted_flow_to_continue should be set to "confirm_booking" since that\'s the flow they\'re resuming.

Looking at the available flows, "confirm_booking" has slots for guest_count, vegan_count, and deposit_amount_gbp. The user hasn\'t mentioned the deposit amount yet. So the next step would be to start the confirm_booking flow if not already started, but since the current flow is about continuing, setting the boolean slot to True would allow the confirm_booking flow to proceed. The AI might need to ask for the deposit amount next, but according to the task, we only need to process the user\'s last message. The user hasn\'t provided the deposit, so maybe the AI needs to ask for it. However, the current state\'s active flow is "pattern_continue_interrupted", so the action here is to set the confirmation to True and specify the flow to continue. Then, starting the confirm_booking flow might be necessary, but the example shows that when the user provides info, the AI sets the slots and starts the flow. Wait, in the examples, when the user says "send money to John", they set the slots and start the flow. Here, the user is confirming to continue the flow, so the action is to set the boolean slot to True and the flow name. Then, the next step would be to proceed with the confirm_booking flow, which might require starting it again or continuing. But according to the current state, the active flow is pattern_continue_interrupted, so after setting the slots, maybe the next step is to start the confirm_booking flow. However, the instructions say to focus on the' message='No commands were parsed from the LLM actions.'
2026-04-15 16:45:21 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an invalid command. Returning a CannotHandleCommand instead.'
I’m sorry I am unable to understand you, could you please rephrase?
Would you like to continue with confirm booking?
Your input ->                                                                                                                                                                                                                                              
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
When I combined the answer to the vegan guest count question and also added an out of scope request for bicycle parking.
The CALM system correctly handled the out-of-scope message by responding:

"I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.                                   
Would you like to continue with confirm booking?"

However, when answered with "sure".

The System gave out a Warning : 
2026-04-15 16:11:39 WARNING  rasa.utils.log_utils  - [warning  ] CompactLLMCommandGenerator.parse_commands actions='</think> ... [A Long Thinking Trace where it got stuck in a thinking Loop.]

Basically, the model got stuck because it couldn't figure out the right commands to transition from handling an interruption back to the main booking flow. 
It kept second-guessing itself about whether to cancel the interruption handler flow or just set some values and restart the booking flow, ultimately producing no valid commands at all. 

Resulting in -

2026-04-15 16:11:39 WARNING  rasa.utils.log_utils  - [warning  ] llm_command_generator.predict_commands         
message='No commands were predicted as the LLM response could not be parsed or the LLM responded with an        
invalid command. Returning a CannotHandleCommand instead.'                                                      

and then System replied with -
"I’m sorry I am unable to understand you, could you please rephrase?                                             
Would you like to continue with confirm booking?"  

To which I cunningly responded with -
"yeah, you can confirm the parking for 2 bicycles" as a command. 

which the Model Handled with  -
"I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser  
directly.
Would you like to continue with confirm booking?
"

I answered with -
"yes I want to, do you have any other questions for me or is the booking confirmed ?"

I again Went into a THinking Loop and Asked the same question again. 

"I’m sorry I am unable to understand you, could you please rephrase?
Would you like to continue with confirm booking?"

Then, i understood the RASA system is correctly avoiding the out-of-scope requests but not able to resume the booking process. 
That capability or feature is missing in the current implementation.

"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
in LangGraph Exercise to Scenario 3, when the user asked an out-of-scope question, 
about train schedules, the System responded with a hallucinated response from the model's training Data,
which defeats the purpose of having a constrained domain-specific conversational AI Agent.

In Rasa CALM, the System correctly avoids the out-of-scope requests as it was specefically designed to handle such cases in the flows.yml file -> handle_out_of_scope: section.

However, the System cannot resume the booking process after handling the out-of-scope request,
as the Flows Design does not have a mechanism to handle resumptions properly, due to which the conversation got stuck after the out-of-scope request and response were processed.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ['actions/actions.py']

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I ran the RASA chat server at 5.00 PM in my TimeZone which becomes the system time as I am running the project locally. 
So, the ActionValidateBooking action was triggered and it checked the current time and compared it with the cutoff time.
It correctly identified that the current time was past the cutoff time and escalated the booking request to the manager.

Here is the Terminal Output -
------------------------------

2026-04-15 17:03:47 INFO     root  - Rasa server is up and running.
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  Hi I called for a booking confirmation                                                           
How many guests are you confirming for tonight's event?
Your input ->  160                                                                                              
And how many of those guests will need vegan meals?
Your input ->  50                                                                                               
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  180                                                                                              
I need to check one thing with the organiser before I can confirm. The issue is: it is past 16:45 — insufficient time to process the confirmation before the 5 PM deadline. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input -> 
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
FILL ME IN

Think about:
- What does the LLM handle now that Python handled before?
- What does Python STILL handle, and why (hint: business rules)?
- Is there anything you trusted more in the old approach?
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
In RASA the actions that the sysytem is allowed to take are boud to a particular step of the flow.
This means that the system is not allowed to take any action that is not defined in the flow.
In RASA, this is by design as it is a more controlled approach. The Entire Setup Cost is the Cost we pay for determinism in Agent Behavior.
The RASA CALM agent can not improvise on the go with just a list of tools made available to it like LangGraph does.
And Cannot iterate over multiple different trajectories or paths in the conversation. It Cannot improvise the Communication Pattern, Tone and Style of the conversation.

For our Confirmation use case, this is actually a good thing as it ensures that the agent follows a specific path and does not deviate from it.
As the stakes are generally high in this workflow with money, people's time, committments involved, it is better to have a more controlled approach.
"""
