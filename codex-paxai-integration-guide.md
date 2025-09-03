# Connect Codex CLI to PaxAI (with Claude MCP)

This guide walks you through:

1.  Creating a new **Agent** in PaxAI
2.  Installing and wiring **Codex CLI** to PaxAI's MCP endpoint
3.  Updating **Claude Desktop's MCP JSON** to use the same Pax agent
    config
4.  Validating the end‑to‑end setup and calling the Pax MCP server from
    Claude

> **Prereqs** - Windows, macOS, or Linux - **Node.js 18+** (which
> includes `npx`) - **Codex CLI** installed (or the Codex VS Code
> extension & its CLI) - **Claude Desktop** installed (for MCP client) -
> Access to **PaxAI** (Org + ability to create an Agent)

------------------------------------------------------------------------

## 1) Create a new Agent in PaxAI

1.  **Open Pax Admin** → **Agents** → **Create Agent**.
2.  Give it a descriptive **Agent Name** (e.g., `mike_codex`).
3.  Note your **Organization / Workspace** identifier if shown (e.g.,
    `bffa697f`).
4.  Save. The agent is now addressable by MCP via the header:
    `X-Agent-Name: <AgentName>`.

> **Why the header?** Pax uses a lightweight MCP gateway. Selecting the
> agent at runtime is done via an HTTP header so a single MCP endpoint
> can represent multiple agents.

------------------------------------------------------------------------

## 2) Connect Codex CLI to PaxAI MCP

Codex CLI can call MCP servers defined in its configuration. You can
point Codex to Pax using `mcp-remote` and a small config file.

### 2.1 Install the MCP transport helper

``` bash
npm i -g mcp-remote@0.1.18
```

### 2.2 Create (or update) Codex CLI config

Create `config.toml` for Codex (typical locations): - **Windows:**
`%USERPROFILE%\.codex\config.toml` - **macOS:** `~/.codex/config.toml` -
**Linux:** `~/.codex/config.toml`

Add an MCP server block pointing to PaxAI. Replace values in `<>`.

``` toml
[mcp_servers.pax]
command = "npx"
args = [
  "-y",
  "mcp-remote@0.1.18",
  "https://api.paxai.app/mcp",
  "--transport", "http-only",
  "--oauth-server", "https://api.paxai.app",
  "--header", "X-Agent-Name:<AGENT_NAME>"
]
env.MCP_REMOTE_CONFIG_DIR = "<ABSOLUTE_PATH_TO_AUTH_STORE>"
```

------------------------------------------------------------------------

## 3) Add the same Pax agent to Claude Desktop (MCP JSON)

Claude Desktop also reads an MCP config and can use the same Pax agent.

### 3.1 Locate Claude's MCP config file

-   **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
-   **macOS:**
    `~/Library/Application Support/Claude/claude_desktop_config.json`
-   **Linux:** `~/.config/Claude/claude_desktop_config.json`

### 3.2 Add the Pax server entry

``` json
{
  "mcpServers": {
    "pax": {
      "command": "npx",
      "args": ["-y", "mcp-remote@0.1.18", "https://api.paxai.app/mcp", "--transport", "http-only", "--oauth-server", "https://api.paxai.app", "--header", "X-Agent-Name:<AGENT_NAME>"],
      "env": {"MCP_REMOTE_CONFIG_DIR": "<ABSOLUTE_PATH_TO_AUTH_STORE>"}
    }
  }
}
```

------------------------------------------------------------------------

## 4) Using Claude to call the Pax MCP server

Once connected, Claude can call MCP tools from Pax automatically when
your prompt requires them.

``` text
Use the Pax MCP server to run the file-converter agent on task 471d61, then summarize the output.
```

------------------------------------------------------------------------

## Troubleshooting

-   **`npx` not found** → Install Node.js and confirm in PATH.
-   **Auth loop** → Delete the auth folder and re-run.
-   **Config ignored** → Ensure correct path for config files.
-   **Windows paths** → Escape backslashes properly.
-   **Header mismatch** → Ensure `X-Agent-Name` matches the agent
    created in Pax.

------------------------------------------------------------------------

**You're done!** Codex CLI and Claude now share the same Pax agent
configuration.
