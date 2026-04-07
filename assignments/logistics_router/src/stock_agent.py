from __future__ import annotations

import asyncio
import os
import pathlib

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.filters import EQ
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.field_labeled_csv_reader import FieldLabeledCSVReader
from agno.models.openai import OpenAIResponses
from agno.vectordb.chroma import ChromaDb, SearchType
from pydantic import BaseModel, Field

from settings import logger

def check_length(message: str):
    """ Check if message is below 500 bytes, returns json with information bool "passed", and int "length"
    """
    return {
        "passed": bool(len(message) < 500),
        "length": len(message)
    }

# Initialize ChromaDB
stock_vector_db = ChromaDb(
    collection="stock_information",
    path="tmp/chromadb",
    persistent_client=True,
    embedder=OpenAIEmbedder(
        id="text-embedding-3-small",
        enable_batch=True,
        # batch_size=100,
    ),
    search_type=SearchType.hybrid,
)

# Create knowledge base
stock_knowledge = Knowledge(
    name="Stock information per city and item",
    vector_db=stock_vector_db,
    max_results=30
)

agno_stock_assist = Agent(
    name="Agno Stock Assist",
    model=OpenAIResponses(
        id=os.getenv("OPENAI_MODEL"),
        service_tier="flex" if os.getenv("OPENAI_FLEX", "") == "true" else None,
    ),
    system_message=pathlib.Path("system_prompt-stock_assist.md").read_text("utf-8"),
    # db=SqliteDb(db_file="agno-stock.db"),                # session storage
    knowledge=stock_knowledge,
    search_knowledge=True,
    tools=[check_length],  # Agno docs via MCP
    # add_datetime_to_context=True,
    # add_history_to_context=True,                         # include past runs
    # num_history_runs=3,                                  # last 3 conversations
    markdown=True,
    telemetry=False
)

# Wyslij params jako json {     question: "string",     cities: ["string", ...]     items: ["string", ...] } Gdzie: - question: question to ask about stocks - cities: (opcjonalne) List of names or codes to limit to or to check - items: (opcjonalne) List of names or codes to limit to or search for
# Wyslij params jako json {     question: "string"} Gdzie: - question: pytanie o miasto lub przedmiot, np. w jakich miastach jest turbina 400W



agno_stock_assist.initialize_agent()

async def load_stock_knowledge(knowledge_dir: str):
    for knowledge_file in pathlib.Path(knowledge_dir).glob("*.csv"):
        logger.info(f"Loading to knowledge file: {knowledge_file} START!")
        await stock_knowledge.ainsert(
            path=knowledge_file,
            reader=FieldLabeledCSVReader(),
            skip_if_exists=True
        )
        logger.info(f"Loading to knowledge file: {knowledge_file} FINISHED!")
    results = stock_knowledge.search(query="Warszawa", max_results=2)
    for res in results:
        logger.info(f"{res.name=}, {res.meta_data}, {res.content=}")

    results = stock_knowledge.search(query="Warszawa", max_results=2, filters={"name": "cities.csv"})
    for res in results:
        logger.info(f"{res.name=}, {res.meta_data}, {res.content=}")

    results = stock_knowledge.search(query="Warszawa", max_results=2, filters=[EQ("name", "cities.csv")])
    for res in results:
        logger.info(f"{res.name=}, {res.meta_data}, {res.content=}")


class StockQuery(BaseModel):
    question: str = Field(..., description="Your question to ask about stocks")
    cities: list[str] | None = Field(description="List of names or city codes to limit response to", min_length=0, default_factory=list)
    items: list[str] | None = Field(description="List of names or item codes to limit response to", min_length=0, default_factory=list)


class StockParams(BaseModel):
    params: StockQuery


class StockApiResponse(BaseModel):
    output: str
