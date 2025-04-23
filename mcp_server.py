# server.py
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount, Route
from starlette.applications import Starlette
import clickhouse_connect
import asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize MCP server
mcp = FastMCP("ClickHouse MCP Server")

# Configure ClickHouse client
config = {
    "clickhouse_host": os.getenv("CLICKHOUSE_HOST"),
    "clickhouse_port": os.getenv("CLICKHOUSE_PORT"),
    "clickhouse_user": os.getenv("CLICKHOUSE_USER"),
    "clickhouse_password": os.getenv("CLICKHOUSE_PASSWORD"),
    "clickhouse_database": os.getenv("CLICKHOUSE_DATABASE")
}

# Initialize ClickHouse client
clickhouse_client = clickhouse_connect.get_client(
    host=config["clickhouse_host"],
    port=config["clickhouse_port"],
    username=config["clickhouse_user"],
    password=config["clickhouse_password"],
    database=config["clickhouse_database"]
)

# Define an MCP tool to execute ClickHouse queries
@mcp.tool()
def run_query(query: str):
    """Execute a ClickHouse SQL query and return the results."""
    result = clickhouse_client.query(query)
    return result.result_rows

# Create SSE transport
transport = SseServerTransport("/messages/")

# Define SSE handler
async def handle_sse(request):
    async with transport.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await mcp._mcp_server.run(
            streams[0], streams[1], mcp._mcp_server.create_initialization_options()
        )

# Create Starlette routes
routes = [
    Route("/sse", endpoint=handle_sse),
    Mount("/messages", app=transport.handle_post_message),
]

# Create Starlette app
sse_app = Starlette(routes=routes)

# Mount the SSE app to the main FastAPI app
app.mount("/", sse_app)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mcp_server:app", host="0.0.0.0", port=8000, reload=True)
