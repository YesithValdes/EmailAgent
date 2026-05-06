# Skill: LangGraph Router-Worker Pattern

## Overview
The Router-Worker pattern is a foundational architecture for building reliable agents. It separates the **decision logic** (Router) from the **action logic** (Worker), allowing for better control, specialized prompting, and reduced token usage.

## Implementation Details

### 1. The Router Node
The Router uses structured output to classify the incoming task. This ensures the output is predictable and easy to handle in code.

```python
from typing import Literal
from pydantic import BaseModel, Field

class Router(BaseModel):
    classification: Literal["respond", "ignore", "notify"] = Field(
        description="Decision on how to handle the input"
    )

# Node implementation
def triage_router(state: State) -> Command:
    # LLM call with structured output
    result = llm_router.invoke(...)
    
    if result.classification == "respond":
        return Command(goto="worker_agent", update={"status": "processing"})
    ...
```

### 2. The Worker (Hierarchical Graph)
Workers can be sub-graphs themselves, encapsulating complex tool-calling logic away from the main orchestration graph.

```python
# Compile a sub-graph for specific tasks
worker_builder = StateGraph(WorkerState)
worker_builder.add_node("action", action_node)
...
worker_agent = worker_builder.compile()

# Add sub-graph as a node in the main graph
main_graph.add_node("worker_agent", worker_agent)
```

## Best Practices
- **Specialized Prompts**: Use distinct system prompts for the Router (focused on classification criteria) and the Worker (focused on tool execution).
- **Structured Routing**: Always use `with_structured_output` for routing decisions to avoid parsing errors.
- **State Isolation**: Sub-graphs (Workers) can have their own state definitions, keeping the main state clean.

## Examples in EmailAgent
- `triage_router`: Classifies emails into `respond`, `ignore`, or `notify`.
- `response_agent`: A specialized worker graph that handles email drafting and calendar tool calls.
