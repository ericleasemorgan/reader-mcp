# read-with-llama.sh - use llama.cpp as the LLM to the Reader's MCP server

export GGML_METAL_NO_RESIDENCY=1
export HF_HUB_CACHE=/Users/eric/.cache/huggingface/hub
export LLAMA_CACHE=/tmp/llama-empty-cache

/Users/eric/.llama-app/llama serve \
  --models-preset '/Users/eric/Library/Application Support/Llama/models.ini' \
  --ctx-size 65536 \
  --mcp-servers-json '{"mcpServers":{"echo":{"command":"/Users/eric/Documents/reader-mcp/bin/server.py"}}}'

#/Users/eric/.llama-app/llama serve \
#  --models-preset '/Users/eric/Library/Application Support/Llama/models.ini' \
#  --log-file /tmp/llama-server.log \
#  --ctx-size 16384 \
#  --models-max 1 \
#  --fit-target 1024 \
#  --sleep-idle-seconds 300 \
#  --jinja \
# --spec-default \
#  --mcp-servers-json '{"mcpServers":{"echo":{"command":"/Users/eric/Documents/reader-mcp/bin/server.py"}}}'

