# Skill: Agent Evaluation with Synthetic Datasets

## Overview
Building agents requires reliable evaluation. A synthetic dataset of "ground-truth" scenarios allows you to measure an agent's accuracy in routing and tool-calling without relying on live production data.

## Implementation Details

### 1. Defining a Dataset
Create a list of scenarios that include:
- **Input**: The raw data (e.g., email subject and body).
- **Expected Decision**: The classification the router *should* make.
- **Expected Tool**: The tool that *should* be called.

```python
eval_dataset = [
    {
        "id": "1",
        "input": "Subject: Invoice #123... Body: Payment is due...",
        "expected_classification": "respond",
        "expected_tool": "send_email_tool"
    },
    ...
]
```

### 2. Execution Script
Write a script that iterates through the dataset and runs the agent in "headless" mode.

```python
for item in eval_dataset:
    # Run agent
    config = {"configurable": {"thread_id": f"eval_{item['id']}"}}
    result = agent.invoke({"email_input": item["input"]}, config)
    
    # Compare result with expectation
    actual = result["classification_decision"]
    is_correct = actual == item["expected_classification"]
    ...
```

### 3. Measuring Performance
Track metrics such as:
- **Classification Accuracy**: Percentage of correct triage decisions.
- **Hallucination Rate**: How often the agent calls a tool when it shouldn't.
- **Tool-Call Precision**: Correctness of the arguments passed to tools.

## Best Practices
- **Edge Cases**: Include tricky examples (e.g., an email that looks like spam but is important).
- **Automated CI/CD**: Run evaluations automatically whenever the agent's prompts or logic change.
- **Detailed Logging**: Store the full agent trace for failed cases to debug prompt issues.

## Examples in EmailAgent
- `run_dataset.py`: A script that runs a 16-email dataset to validate the triage and worker logic.
- `src/gmail_agent/eval`: (Placeholder for potential evaluation schemas).
