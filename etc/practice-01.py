#!/usr/bin/env python


from mcp.server.fastmcp import FastMCP
import rdr

# Create an MCP server
mcp = FastMCP("Demo", json_response=True, stateless_http=True)


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# catalog
@mcp.tool()
def catalog() -> list:
    """Get a list of the available study carrels"""
    return( rdr.catalog().splitlines() )

# bibliography
@mcp.tool()
def bibliography( carrel: str ) -> str:
    """Get the bibliographics of the given carrel"""
    return( rdr.bibliography( carrel, format='json' ) )


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")