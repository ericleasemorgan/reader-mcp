#!/usr/bin/env python

# mcp_cli.py

import argparse
import asyncio
import json
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async def main():
    parser = argparse.ArgumentParser(description="MCP Command Line Client")
    parser.add_argument("--server", required=True, help="Server command")
    parser.add_argument("--args", nargs="*", help="Server arguments")
    parser.add_argument("--list-tools", action="store_true", help="List available tools")
    parser.add_argument("--call", help="Tool to call")
    parser.add_argument("--params", help="Tool parameters as JSON")
    
    args = parser.parse_args()
    
    async with stdio_client(args.server, args.args or []) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            if args.list_tools:
                tools = await session.list_tools()
                print("Available tools:")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                    
            elif args.call:
                params = json.loads(args.params) if args.params else {}
                result = await session.call_tool(args.call, params)
                print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
