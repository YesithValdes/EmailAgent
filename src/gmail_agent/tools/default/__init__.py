"""Default tools for email assistant."""

from gmail_agent.tools.default.email_tools import write_email, triage_email, Done
from gmail_agent.tools.default.calendar_tools import schedule_meeting, check_calendar_availability
from gmail_agent.tools.default.prompt_templates import (
    STANDARD_TOOLS_PROMPT,
    AGENT_TOOLS_PROMPT,
    HITL_TOOLS_PROMPT,
    HITL_MEMORY_TOOLS_PROMPT
)

__all__ = [
    "write_email",
    "triage_email",
    "Done",
    "schedule_meeting", 
    "check_calendar_availability",
    "STANDARD_TOOLS_PROMPT",
    "AGENT_TOOLS_PROMPT",
    "HITL_TOOLS_PROMPT",
    "HITL_MEMORY_TOOLS_PROMPT"
]
