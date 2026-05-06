# Skill: Human-in-the-Loop (HITL) Interrupts

## Overview
HITL allows an agent to pause its execution and wait for human approval or feedback before proceeding with high-stakes actions (e.g., sending an email, making a payment, or scheduling a meeting).

## Implementation Details

### 1. Using the `interrupt` Function
In LangGraph, the `interrupt` function is used to create a "breakpoint". It yields execution and waits for a response from the UI or an external system.

```python
from langgraph.types import interrupt

def interrupt_handler(state: State):
    # Define what the user needs to review
    request = {
        "action": "send_email",
        "args": {"to": "user@example.com", "body": "..."},
        "description": "Please review this email draft."
    }
    
    # Execution pauses here
    response = interrupt([request])[0]
    
    # Process the user's response (accept, edit, ignore, etc.)
    if response["type"] == "accept":
        # Execute action
        ...
```

### 2. Handling Different Response Types
A robust HITL system should handle multiple types of user interaction:
- **Accept**: Execute the action as proposed.
- **Edit**: Modify the arguments and then execute or re-submit for review.
- **Ignore**: Cancel the action and potentially end the workflow.
- **Response/Feedback**: Incorporate feedback into the state and ask the LLM to regenerate.

### 3. Agent Inbox Integration
For a seamless experience, the interrupt data should be formatted for a UI (like "Agent Inbox") that can present the "description" and provide buttons for "accept", "edit", etc.

## Best Practices
- **Granular Control**: Only interrupt for specific "high-risk" tools. Let "low-risk" tools (like searches) run autonomously.
- **Contextual Descriptions**: Provide clear markdown descriptions of what the agent is about to do so the human can make an informed decision.
- **Memory Feedback**: When a human edits or ignores a draft, feed that decision back into the agent's memory to improve future performance.

## Examples in EmailAgent
- `interrupt_handler`: Pauses for tool calls like `send_email_tool`.
- `triage_interrupt_handler`: Pauses when an email is classified as `notify` to let the user decide if a response is needed.
