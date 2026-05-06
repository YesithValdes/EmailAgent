# Skill: Persistent Memory with LangGraph Store

## Overview
Standard agent memory (thread state) is lost after a conversation ends. Using `BaseStore`, agents can maintain a persistent "user profile" or "set of preferences" that evolves across multiple threads.

## Implementation Details

### 1. Retrieving Memory
Use the `store.get()` method within a node to fetch existing preferences.

```python
def get_memory(store, namespace, default_content=None):
    user_preferences = store.get(namespace, "user_preferences")
    if user_preferences:
        return user_preferences.value
    return default_content
```

### 2. Updating Memory via Reflection
Instead of just saving logs, use a "Reflection LLM" to analyze recent interactions and update the structured profile.

```python
def update_memory(store, namespace, messages):
    current_profile = store.get(namespace, "user_preferences").value
    
    # LLM analyzes messages and creates a NEW profile
    result = llm_memory.invoke([
        {"role": "system", "content": f"Update the profile: {current_profile}"},
        *messages
    ])
    
    # Save back to store
    store.put(namespace, "user_preferences", result.updated_profile)
```

### 3. Namespace Design
Use hierarchical namespaces to separate different types of memory:
- `("user_id", "triage_preferences")`
- `("user_id", "writing_style")`
- `("user_id", "calendar_rules")`

## Best Practices
- **Structured Profiles**: Store memory as structured data (Pydantic objects) rather than raw text to make it easier for the agent to use in prompts.
- **Reinforcement Prompts**: Use instructions that encourage the LLM to *add* to existing knowledge rather than completely overwriting it.
- **Privacy**: Be mindful of what is stored in long-term memory.

## Examples in EmailAgent
- `get_memory` & `update_memory`: Utility functions used to manage triage and response preferences.
- `MEMORY_UPDATE_INSTRUCTIONS`: System prompt used to guide the memory refinement process.
