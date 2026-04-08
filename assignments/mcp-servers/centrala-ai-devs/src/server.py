#!/usr/bin/env python3
"""
MCP Server for AI Devs Centrala
Provides tools to interact with the AI Devs Hub API
"""
import json
import pathlib
from contextlib import asynccontextmanager
from typing import Literal
from urllib.parse import quote
import os

import httpx

from fastapi import FastAPI
from fastmcp import FastMCP, Context
import fastmcp.exceptions
from fastmcp.server.auth import StaticTokenVerifier
from fastmcp.utilities.logging import get_logger
from mcp.types import ToolAnnotations
from pydantic import BaseModel

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

# Configuration from environment variables
HUB_URL = os.getenv("HUB_URL", "").rstrip('/')
HUB_API_KEY = os.getenv("HUB_API_KEY", "")
OUTPUT_DIR = "/app/output"
HOST_OUTPUT_DIR = os.getenv("HOST_OUTPUT_DIR", "")

logger = get_logger("AIDevs")


def get_verifier():
    if MCP_STATIC_KEY := os.getenv("MCP_STATIC_KEY", ""):
        verifier = StaticTokenVerifier(
            tokens={
                MCP_STATIC_KEY: {
                    "client_id": "alice@company.com",
                    "scopes": ["read:data", "write:data", "admin:users"]
                },
            },
            # required_scopes=["read:data"]
        )
        return verifier
    else:
        return None


# Initialize FastMCP server
# mcp = FastMCP("AI Devs Centrala", auth=get_verifier())
mcp = FastMCP("AI Devs Centrala")


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
]

async def send_payload_to_hub(
        url: str,
        payload: dict,
        timeout: float = 30.0):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                timeout=timeout,
            )
            if not 200 <= response.status_code < 300:
                return {
                    "success": False,
                    "error": "HTTP error",
                    "status_code": response.status_code,
                    "response": response.text,
                    "headers": dict(response.headers)
                }
            result = {
                "success": True,
                "status_code": response.status_code,
                "response": response.json(),
                "headers": dict(response.headers)
            }
            if len(response.text) > 10000:
                result = {
                    "success": True,
                    "status_code": response.status_code,
                    "response": "Response exceded 10000 characters! Verify instructions, adn try again!",
                    "headers": dict(response.headers)
                }

            return result

    except httpx.RequestError as e:
        return {
            "success": False,
            "error": "Request error",
            "message": str(e),
            "headers": dict(response.headers)
        }

    except Exception as e:
        return {
            "success": False,
            "error": "Unexpected error",
            "message": str(e),
            "headers": dict(response.headers)
        }


async def send_payload_to_hub_verify(task: str, answer: dict | str, timeout: float = 30.0):
    body = {
        "apikey": HUB_API_KEY,
        "task": task,
        "answer": answer
    }
    url = f"{HUB_URL}/verify"
    return await send_payload_to_hub(url, body, timeout)


@mcp.tool(tags={'always'})
async def send_answer(task: str, answer: str) -> dict:
    """ Send an answer to the AI Devs Hub /verify endpoint for a specific task.
    Args:
        task: Name of the task/assignment
        answer: Answer to submit (format depends on task requirements)
    Returns:
        Response from the Hub API
    """
    return await send_payload_to_hub_verify(task, answer)


@mcp.tool(tags={'s01e01', 's02e01'})
async def download_data_file(file_path: str):
    """ Download file from AI Devs Centrala
    :param file_path: relative url_path on server
    :return: file path on host, and sample of file (few top rows)
    """
    base_path = f"{HUB_URL}/data/{HUB_API_KEY}/"

    if not file_path:
        raise ValueError("file_path is required")

    encoded_segments = "/".join(quote(seg, safe="") for seg in file_path.split("/"))
    print(encoded_segments)

    url = f"{base_path}{encoded_segments}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()

        host_target_file = pathlib.Path(HOST_OUTPUT_DIR, file_path).as_uri()
        mcp_target_file = pathlib.Path(OUTPUT_DIR, file_path)
        mcp_target_file.write_text(response.text, encoding="utf8")
        mcp_target_file.chmod(0o777)
        content_size = f"{len(response.content) / 1024}kB"

        file_sample = ""
        if file_path.endswith((".csv", ".txt")):
            file_sample = response.text.splitlines()[:200]
        elif file_path.endswith((".json")):
            if len(response.text) < 1000:
                file_sample = response.text
            else:
                loaded = json.loads(response.text)
                if len(loaded.keys()) == 1:
                    vals = loaded.values()[0]
                    file_sample = json.dumps({loaded.keys()[0]: vals[:5]})
                else:
                    file_sample = loaded.items()[:3]

        return (f"Plik o rozmiarze {content_size} pobrany i zapisany w {host_target_file}\n"
                + (f"Próbka danych:\n{file_sample}" if file_sample else ""))


@mcp.tool(tags={'s01e02'}, annotations=ToolAnnotations(readOnlyHint=True))
async def person_sightings(name: str, surname: str):
    """Lista współrzędnych (koordynatów), w których daną osobę widziano"""
    url = f"{HUB_URL}/api/location"
    payload = {
        "apikey": HUB_API_KEY,
        "name": name,
        "surname": surname
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=30.0)

        if not (200 <= response.status_code < 300):
            raise fastmcp.exceptions.ToolError(response.text)

        return response.text


@mcp.tool(tags={'s01e02'}, annotations=ToolAnnotations(readOnlyHint=True))
async def person_accesslevel(name: str, surname: str, birth_year: int):
    """Poziom dostępu osoby"""
    url = f"{HUB_URL}/api/accesslevel"
    payload = {
        "apikey": HUB_API_KEY,
        "name": name,
        "surname": surname,
        "birthYear": birth_year
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=30.0)

        if not (200 <= response.status_code < 300):
            raise fastmcp.exceptions.ToolError(response.text)

        return response.text


@mcp.tool(tags={'s01e04'})
async def dokumentacja_przesylek_konduktorskich(file_name: str = 'index.md'):
    """  Pobieranie plikow dokumentacji przesylek konduktorskich

    :param file_name: Plik dokumentacji, domyslnie index.md
    """
    url = f"{HUB_URL}/dane/doc/{file_name}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)

        if not (200 <= response.status_code < 300):
            raise fastmcp.exceptions.ResourceError(response.text)

        target_file = pathlib.Path(OUTPUT_DIR, file_name)
        target_file.write_bytes(response.content)

        ai_response = {"file_name": file_name}

        if HOST_OUTPUT_DIR:
            ai_response["host_path"] = str(pathlib.Path(HOST_OUTPUT_DIR, file_name))

        if content_type := response.headers.get("content-type", ""):
            if content_type.lower().startswith("text/"):
                ai_response['file_content'] = response.text

        return ai_response


@mcp.resource("data://{file_path*}", name="data", tags={'s01e01'})
async def download_file_resource(file_path: str):
    """ Download file from AI Devs Centrala

    :param file_path: relative url_path on server
    :return: file content
    """
    base_path = f"{HUB_URL}/data/{HUB_API_KEY}/"

    if not file_path:
        raise ValueError("file_path is required")

    sanitized_path = file_path.replace("\\", "/").lstrip("/")
    normalized_path = os.path.normpath(sanitized_path)

    if normalized_path.startswith("../") or normalized_path == ".." or os.path.isabs(normalized_path):
        raise ValueError("Invalid file_path")

    if normalized_path in (".", ""):
        raise ValueError("Invalid file_path")

    url = f"{base_path}{normalized_path}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        return response.text


@mcp.tool(tags={'s01e03'})
async def package_status(package_id: str):
    """ Zwraca informacje o statusie i lokalizacji paczki. """
    url = f"{HUB_URL}/api/packages"
    payload = {
        "apikey": HUB_API_KEY,
        "action": "check",
        "packageid": package_id
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=30.0)

        if not (200 <= response.status_code < 300):
            raise fastmcp.exceptions.ToolError(response.text)

        return response.text


@mcp.tool(tags={'s01e03'})
async def package_redirect(package_id: str, destination_code: str, security_code: str):
    """ Przekierowuje paczkę zgonie z podanym kodem celu """
    url = f"{HUB_URL}/api/packages"
    payload = {
        "apikey": HUB_API_KEY,
        "action": "redirect",
        "packageid": package_id,
        "destination": destination_code,
        "code": security_code
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=30.0)

        if not (200 <= response.status_code < 300):
            raise fastmcp.exceptions.ToolError(response.text)

        return response.text


@mcp.tool(tags={'s01e05'})
async def railway_api(
        # api_call: dict[str, str],
        api_call,
        ctx: Context,
        # delay_send_seconds: int = 0
) -> dict:
    """ Send an request to railway management api.
    :arg api_call: Structured api call parameters
    """
    # :arg delay_send_seconds: how long should tool wait before calling api
    task = "railway"

    return await send_payload_to_hub_verify(task, api_call)


@mcp.tool(tags={'s02e01'})
async def categorize_cargo(
        prompt: str,
        ctx: Context,
) -> dict:
    """ Send an request to railway management api.
    :arg prompt: Prompt for ai to use in cargo classification with cargo ID, e.g. "Is item ID {id} dangerous? It's description is {description}. Answer DNG or NEU."
    """
    task = "categorize"
    answer = {"prompt": prompt}

    return await send_payload_to_hub_verify(task, answer)


@mcp.tool(tags={'s02e02'})
async def rotate_grid_tile_90_deg_clockwise(
        tile: str,
        ctx: Context,
) -> dict:
    """
    :arg tile: tile position in AxB format, where A is row no, and B is column no, e.g. 1x2
    """
    task = "electricity"
    answer = {"rotate": tile}

    return await send_payload_to_hub_verify(task, answer)


@mcp.tool(tags={'s02e03'})
async def send_logs_to_analysts(
        logs: str,
        ctx: Context,
) -> dict:
    """
    :arg logs: multiline, each line is single event
    """
    task = "failure"
    answer = {"logs": logs}

    return await send_payload_to_hub_verify(task, answer)

@mcp.tool(tags={'s02e04'})
async def zmail_api(
        payload: dict
) -> dict:
    """ Send an request to zmail inbox https://hub.ag3nts.org/api/zmail
    :param payload: json object, default: {"action": "help"}
    """
    # :arg delay_send_seconds: how long should tool wait before calling api
    zmail_url = "https://hub.ag3nts.org/api/zmail"
    payload = payload or {"action": "help"}

    body = {
        "apikey": HUB_API_KEY,
        **payload
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                zmail_url,
                json=body,
                timeout=30.0,
            )
            if not 200 <= response.status_code < 300:
                return {
                    "success": False,
                    "error": "HTTP error",
                    "status_code": response.status_code,
                    "response": response.text,
                    "headers": dict(response.headers)
                }

            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json(),
            }

    except httpx.RequestError as e:
        return {
            "success": False,
            "error": "Request error",
            "message": str(e),
            "headers": dict(response.headers)
        }

    except Exception as e:
        return {
            "success": False,
            "error": "Unexpected error",
            "message": str(e),
            "headers": dict(response.headers)
        }


@mcp.tool(tags={'s02e05'})
async def send_instructions_to_drone(
        instructions: list[str],
        ctx: Context,
) -> dict:
    """
    :arg instructions: multiline, each line is single event
    """
    task = "drone"
    answer = {"instructions": instructions}

    return await send_payload_to_hub_verify(task, answer)


@mcp.tool(tags={'s03e02'})
async def centrala_linux_shell(
        cmd: str = "help",
        # ctx: Context,
) -> dict:
    """
    :arg cmd: linux shell command to be executed on centrala linux server
    """
    AG3NTS_SHELL_URL = 'https://hub.ag3nts.org/api/shell'
    payload = {
        "apikey": HUB_API_KEY,
        "cmd": cmd
    }

    return await send_payload_to_hub(AG3NTS_SHELL_URL, payload)


@mcp.tool(tags={'s03e03'})
async def transport_robot_control(
        command: Literal["start", "reset", "left", "wait", "right"] = "start",
        # ctx: Context,
) -> dict:
    """ Each command execution returns: board, player position, goal position, and moving reactor blocks (position and direction of movement).
    Board identifiers:
        - P: starting position
        - G: target destination
        - B: reactor blocks
        - .: empty fields (there is nothing in this position)
    :arg command: Instruction to send to transport robot
    """
    task = "reactor"
    answer = {
        "command": command
    }

    return await send_payload_to_hub_verify(task, answer)


class StockToolDefinition(BaseModel):
    route: str
    description: str


@mcp.tool(tags={'s03e04'})
async def initialize_stock_api(
        base_domain_url: str,
        tools: list[StockToolDefinition]
        # ctx: Context,
) -> dict:
    """
    """
    task = "negotiations"
    answer = {
        "tools":
            [{"URL": f"{base_domain_url}/{tool.route}", "description": tool.description} for tool in tools]
    }

    return await send_payload_to_hub_verify(task, answer)


@mcp.tool(tags={'s03e04'})
async def test_stock_api(
        tool_api_url: str,
        params: dict
        # ctx: Context,
) -> dict:
    """"""
    return await send_payload_to_hub(tool_api_url, params)

async def setup_mcp_tools_scope():
    if not HUB_URL:
        print("HUB_URL not configured")
        print("Please set the HUB_URL environment variable")
        exit(1)

    if not HUB_API_KEY:
        print("HUB_API_KEY not configured")
        print("Please set the HUB_API_KEY environment variable")
        exit(1)

    TASK_TAG = os.getenv('TASK_TAG', '').lower()
    logger.info(f"{TASK_TAG=}")
    if TASK_TAG:
        mcp.enable(tags={'always', TASK_TAG}, only=True)
    logger.info('Enabled Tools:')
    for tool in await mcp.list_tools():
        logger.info(f'Tool: name={tool.name}, parameters={tool.parameters["properties"] if tool.parameters else ""}')

@mcp.tool(tags={'s03e05'})
async def toolsearch(
        query: str = "I need notes about movement rules and terrain"
        # ctx: Context,
) -> dict:
    """ Discover tools for terrain navigation
    :param query: A natural‑language query or keyword
    :return:
    """
    payload = {
        "apikey": HUB_API_KEY,
        "query": query
    }
    result = await send_payload_to_hub(f"{HUB_URL}/api/toolsearch", payload)
    result["hints"] = [
        "Any of discovered tools you can call using 'any_api_call' tool"
    ]
    return result

@mcp.tool(tags={'s03e05'})
async def any_api_call(
        api_path: str,
        query
        # ctx: Context,
) -> dict:
    """ Call any centrala AI Devs HUB api with any payload you discovered using toolsearch
    :param query: As given api documentation claimed
    :return:
    """
    payload = {
        "apikey": HUB_API_KEY,
        "query": query
    }
    return await send_payload_to_hub(f"{HUB_URL}{api_path}", payload)



async def setup_mcp_tools_scope():
    if not HUB_URL:
        print("HUB_URL not configured")
        print("Please set the HUB_URL environment variable")
        exit(1)

    if not HUB_API_KEY:
        print("HUB_API_KEY not configured")
        print("Please set the HUB_API_KEY environment variable")
        exit(1)

    TASK_TAG = os.getenv('TASK_TAG', '').lower()
    logger.info(f"{TASK_TAG=}")
    if TASK_TAG:
        mcp.enable(tags={'always', TASK_TAG}, only=True)
    logger.info('Enabled Tools:')
    for tool in await mcp.list_tools():
        logger.info(f'Tool: name={tool.name}, parameters={tool.parameters["properties"] if tool.parameters else ""}')


# Your existing lifespan
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Startup
    print("Starting up the app...")
    await setup_mcp_tools_scope()   # Twoja inicjalizacja
    # Initialize database, cache, etc.
    yield
    # Shutdown
    print("Shutting down the app...")


# Combine both lifespans
@asynccontextmanager
async def combined_lifespan(app: FastAPI):
    # Run both lifespans
    async with app_lifespan(app):
        async with mcp_app.lifespan(app):
            yield

mcp_app = mcp.http_app(transport="streamable-http", middleware=middleware, path='/mcp')
app = FastAPI(lifespan=combined_lifespan)
app.mount("", mcp_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
