Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Template: reconnect the agent to its configured MCP server.
claude --dangerously-skip-permissions "/mcp"
