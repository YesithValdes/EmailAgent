"""Run the email agent using the example dataset instead of real Gmail emails.

This script converts the email_dataset format (author/to/subject/email_thread)
to the Gmail format (from/to/subject/body/id) that the agent expects,
and feeds each email through the agent pipeline.

Usage:
    python run_dataset.py
    python run_dataset.py --email 1        # run only email_input_1
    python run_dataset.py --email 4 7 10   # run specific emails
    python run_dataset.py --list           # list available emails
"""

import argparse
import sys
import uuid
from unittest.mock import patch
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

load_dotenv(".env")


# ── Import the canonical dataset ───────────────────────────────────────────
from gmail_agent.eval.email_dataset import (
    examples_triage,
    email_names,
    triage_outputs_list,
)

# Build the runtime list: add a numeric `id` and `expected` field so
# run_email() can reference them without knowing the dataset internals.
email_inputs_dataset = [
    {
        "id": i + 1,
        "expected": ex["outputs"]["classification"],
        **ex["inputs"]["email_input"],          # author, to, subject, email_thread
    }
    for i, ex in enumerate(examples_triage)
]



def dataset_to_gmail_format(email: dict) -> dict:
    """Convert dataset email format to the Gmail format expected by the agent.
    
    Dataset format:  author, to, subject, email_thread, (id as int)
    Gmail format:    from, to, subject, body, id (as string)
    """
    return {
        "from": email["author"],
        "to": email["to"],
        "subject": email["subject"],
        "body": email["email_thread"],
        # Use a fake Gmail-style ID so mark_as_read_node doesn't crash
        "id": f"DATASET_{email['id']:04d}_{uuid.uuid4().hex[:8]}",
    }



def run_email(email_dict: dict, email_number: int, store):
    """Run a single email through the agent.
    
    Recompiles the graph with a fresh MemorySaver checkpointer so that
    invoke() returns state (not None) even when an interrupt is hit.
    Mocks `interrupt` so every HITL node auto-responds with 'ignore',
    allowing the full pipeline to complete synchronously.
    """
    import gmail_agent.email_agent as agent_module

    # Fresh checkpointer per email to avoid state bleed between runs
    checkpointer = MemorySaver()

    # Recompile the graph with a real checkpointer so invoke() returns state
    email_assistant = agent_module.overall_workflow.compile(
        checkpointer=checkpointer,
        store=store,
    )

    gmail_input = dataset_to_gmail_format(email_dict)

    print(f"\n{'='*60}")
    print(f"[EMAIL #{email_number}] {email_dict['subject']}")
    print(f"    From   : {email_dict['author']}")
    print(f"    Expected: {email_dict['expected'].upper()}")
    print(f"{'='*60}")

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # auto_interrupt replaces the real interrupt() in the agent:
    # - triage_interrupt_handler: interrupt([request]) → [{"type": "ignore"}] → END
    # - interrupt_handler:        interrupt([request]) → [{"type": "ignore"}] → END
    # The classification_decision was already saved in state by triage_router,
    # so we can read it from the checkpointer after the graph ends.
    def auto_interrupt(values):
        return [{"type": "ignore"}]

    with patch("gmail_agent.email_agent.mark_as_read"), \
         patch("gmail_agent.email_agent.interrupt", side_effect=auto_interrupt):
        try:
            result = email_assistant.invoke(
                {"email_input": gmail_input},
                config=config,
            )

            # If invoke() still returns None (shouldn't happen now), fall back
            # to reading state directly from the checkpointer
            if result is None:
                snapshot = email_assistant.get_state(config)
                result = snapshot.values if snapshot else {}

            decision = (result or {}).get("classification_decision", "unknown")
            correct = decision.lower() == email_dict["expected"].lower()
            status = "[OK]" if correct else "[WRONG]"
            print(f"\n    Decision: {decision.upper()}  {status}")
            return correct

        except Exception as e:
            # Last resort: try to read partial state from checkpointer
            try:
                snapshot = email_assistant.get_state(config)
                decision = snapshot.values.get("classification_decision", "unknown")
                correct = decision.lower() == email_dict["expected"].lower()
                status = "[OK]" if correct else "[WRONG]"
                print(f"\n    Decision (from state): {decision.upper()}  {status}")
                return correct
            except Exception:
                print(f"\n    ERROR: {e}")
                return False


def main():
    parser = argparse.ArgumentParser(description="Run email agent with dataset emails")
    parser.add_argument(
        "--email",
        nargs="*",
        type=int,
        help="Email number(s) to run (1-based). If omitted, runs all.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available emails and exit.",
    )
    args = parser.parse_args()

    if args.list:
        print("\nAvailable emails in dataset:\n")
        for e in email_inputs_dataset:
            print(f"  #{e['id']:2d}  [{e['expected'].upper():8s}]  {e['subject']}")
        print()
        sys.exit(0)

    # Filter by requested email numbers
    if args.email:
        selected = [e for e in email_inputs_dataset if e["id"] in args.email]
        not_found = set(args.email) - {e["id"] for e in selected}
        if not_found:
            print(f"WARNING: Email numbers not found: {sorted(not_found)}")
    else:
        selected = email_inputs_dataset

    if not selected:
        print("No emails to process.")
        sys.exit(1)

    # Shared store for memory across all emails (checkpointer is per-email inside run_email)
    store = InMemoryStore()

    print(f"\nRunning {len(selected)} email(s) through the agent...\n")

    results = []
    for email in selected:
        ok = run_email(email, email["id"], store)
        results.append(ok)


    # Summary
    total = len(results)
    correct = sum(results)
    print(f"\n{'='*60}")
    print(f"SUMMARY: {correct}/{total} correct ({100*correct//total if total else 0}%)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
