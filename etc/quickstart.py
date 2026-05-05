#!/usr/bin/env python

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("your-server")

@mcp.tool()
def example_tool():
    return "Hello World"

# Use streamable HTTP instead of SSE
if __name__ == "__main__":
    mcp.run(transport="streamable-http")  # Change from "sse"
