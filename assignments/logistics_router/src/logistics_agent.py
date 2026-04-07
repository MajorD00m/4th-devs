from __future__ import annotations

import os
import pathlib
from typing import Iterable

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.message import Message
from agno.models.openai import OpenAIResponses

from agno.tools.mcp import MCPTools
from pydantic import BaseModel, Field

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")
centrala_mcp_server = MCPTools(
    url=MCP_SERVER_URL,
    transport="streamable-http"
)
agno_assist = Agent(
    name="Agno Assist",
    model=OpenAIResponses(
        id=os.getenv("OPENAI_MODEL"),
        service_tier="flex" if os.getenv("OPENAI_FLEX", "") == "true" else None,
    ),
    system_message=pathlib.Path("system_prompt.md").read_text("utf-8"),
    db=SqliteDb(db_file="agno.db"),                     # session storage
    tools=[centrala_mcp_server],  # Agno docs via MCP
    add_datetime_to_context=True,
    add_history_to_context=True,                         # include past runs
    num_history_runs=3,                                  # last 3 conversations
    markdown=True,
    telemetry=False,
)

agno_assist.initialize_agent()

class OperatorRequest(BaseModel):
    sessionID: str = Field(..., min_length=1)
    msg: str = Field(..., min_length=1)


class OperatorResponse(BaseModel):
    msg: str


def messages_to_dict(messages: Iterable[Message]) -> list[dict]:
    result: list[dict[str, str]] = []
    for message in messages:
        msg = {
            "role": message.role,
            "content": message.content,
            "tool_calls": message.tool_calls,
            "tool_args": message.tool_args,
            "tool_name": message.tool_name,
            "tool_call_error": message.tool_call_error
        }
        result.append({k:v for k,v in msg.items() if v})
    return result
