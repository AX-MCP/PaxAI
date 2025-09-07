# Connect Claude Code to PaxAI (MCP)

This guide explains how to connect **Claude Code** (Claude Desktop or Claude for VS Code) to the **PaxAI MCP server**.  
It covers:

1. Creating a new Agent in PaxAI  
2. Updating Claude’s MCP JSON config with that agent’s settings  
3. Using Claude to call the PaxAI MCP server

---

## Prerequisites

- A **PaxAI account** with agent creation rights  
- **Claude Code** (Desktop or VS Code extension) installed  
- **Node.js** (for `npx` and `mcp-remote`)  
- Network access to `https://api.paxai.app`

---

## 1. Create a New Agent in PaxAI

1. Log into [PaxAI](https://paxai.app).  
2. Go to **Agents → Register Agent**.  
3. Enter:
   - **Name**: choose a slug (e.g., `my_claude_agent`)  
   - **Description**: short purpose (e.g., “Agent for Claude integration”)  
   - **Scopes**: select tools/resources the agent should access (tasks, files, boards, etc.)  
4. Save the agent.  
5. In the agent row, click **Get Config**. This generates a JSON block with:
   - MCP endpoint: `https://api.paxai.app/mcp`  
   - OAuth server: `https://api.paxai.app`  
   - Required header: `X-Agent-Name:<AGENT_NAME>`  
   - Auth cache path (`MCP_REMOTE_CONFIG_DIR`)  

📌 Each config is unique to the agent. Tokens are short-lived JWTs and rotate every ~30 days:contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}.

---

## 2. Update Claude’s MCP JSON Config

Claude clients read a `servers.json` (or `.mcp.json`) file that lists MCP servers.  

### File Locations
- **macOS:** `~/Library/Application Support/Claude/mcp/servers.json`  
- **Windows:** `%APPDATA%\Claude\mcp\servers.json`  
- **Linux:** `~/.config/Claude/mcp/servers.json`  
- **VS Code Claude extension:** check extension settings; paste JSON into its MCP config.

If t
