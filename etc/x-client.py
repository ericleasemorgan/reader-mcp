# list tools
curl -s -X POST "http://localhost:8000/mcp" \
  -H "Content-Type: application/json"    \
  -H "Accept: application/json"          \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/list"
  }' | jq


# catalog
curl -s -X POST "http://localhost:8000/mcp" \
    -H "Content-Type: application/json"       \
    -H "Accept: application/json"             \
    -d '{
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/call",
        "params": {
            "name": "catalog",
            "arguments": {}
    }
  }' | jq -r '.result|.content[].text' | tr '\n' '\t'


# bibliography
curl -X POST "http://localhost:8000/mcp" \
    -H "Content-Type: application/json"     \
    -H "Accept: application/json"           \
    -d '{
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/call",
        "params": { "name": "bibliography", "arguments": { "carrel": "homer" } }
    }' | jq '.result|.content[]|.text' | jq fromjson
  

curl -X POST "http://localhost:8000/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "add",
      "arguments": {
        "a": "2",
        "b": "4"
      }
    }
  }'

