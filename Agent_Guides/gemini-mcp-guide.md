# Guide: Setting Up Multiple Agents and Sub-Agents in Gemini CLI

This guide explains how to configure and manage multiple agents and sub-agents using **Gemini CLI**.

---

## Prerequisites

- Installed and configured **Gemini CLI**
- Valid API key or authentication credentials
- Node.js v18+ or Python 3.10+ (depending on setup)
- Access to the workspace or project where the agents will run

---

## 1. Setting Up the Gemini CLI

1. **Install Gemini CLI:**
   ```bash
   npm install -g @google/gemini-cli
   ```

2. **Authenticate:**
   ```bash
   gemini auth login
   ```

3. **Initialize your project:**
   ```bash
   gemini init my-multi-agent-project
   ```

---

## 2. Creating Multiple Agents

Gemini allows multiple agent definitions within one workspace.

1. **Create your first agent:**
   ```bash
   gemini agent create --name main-agent --model gemini-1.5-pro
   ```

2. **Add another agent:**
   ```bash
   gemini agent create --name assistant-agent --model gemini-1.5-flash
   ```

3. **List all agents:**
   ```bash
   gemini agent list
   ```

Each agent can have unique configuration parameters such as temperature, max tokens, and prompt templates.

Example configuration file (`agents.yaml`):
```yaml
agents:
  - name: main-agent
    model: gemini-1.5-pro
    description: Primary reasoning agent
  - name: assistant-agent
    model: gemini-1.5-flash
    description: Quick-response helper
```

---

## 3. Setting Up Sub-Agents

Sub-agents are child processes or specialized models under a parent agent.

1. **Create a sub-agent:**
   ```bash
   gemini agent create --name summarizer --parent main-agent --model gemini-1.5-mini
   ```

2. **Define sub-agent hierarchy in config:**
   ```yaml
   agents:
     - name: main-agent
       subagents:
         - summarizer
         - retriever
   ```

3. **Invoke sub-agents programmatically:**
   ```bash
   gemini agent run summarizer --input "Summarize this text..."
   ```

---

## 4. Managing Multi-Agent Workflows

You can orchestrate multiple agents using `gemini workflow` commands.

```bash
gemini workflow create --name multi-agent-demo
gemini workflow add-agent main-agent
gemini workflow add-agent assistant-agent
gemini workflow run --input "Plan a product launch with detailed steps."
```

---

## 5. Debugging and Logs

View all logs for your agents:

```bash
gemini logs --agent main-agent
```

For real-time monitoring:

```bash
gemini watch --agent assistant-agent
```

---

## 6. Best Practices

- Use **descriptive agent names**
- Keep sub-agents lightweight and single-purpose
- Manage credentials securely using environment variables
- Regularly update your CLI and API tokens

---

✅ **You now have a multi-agent setup running in Gemini CLI!**

---

## 7. Connect Each Agent to Its Own MCP Servers

Gemini CLI discovers MCP servers from **settings.json** files at different scopes. To give *each agent* its own isolated toolset, use **project-scoped** configs so each agent runs from its own project directory.

### 7.1 Scopes refresher
- **User scope:** `~/.gemini/settings.json` (applies to all projects)
- **Project scope:** `./.gemini/settings.json` (applies only when you run `gemini` from this folder; **recommended for per‑agent isolation**)

> Tools defined at the project scope override/augment user scope. Keep sensitive API keys in env vars, not in JSON.

### 7.2 Add MCP servers for *Agent A* (project A)
1) Create a project folder for the agent and init Gemini:
```bash
mkdir -p ~/agents/agent-a/.gemini && cd ~/agents/agent-a
```
2) Add MCP servers to this project only:
```bash
gemini mcp add --scope project --transport http github https://api.githubcopilot.com/mcp/
gemini mcp add --scope project --transport http sentry https://mcp.sentry.dev/mcp
```
3) Verify:
```bash
gemini mcp list
```
This writes entries under `./.gemini/settings.json` → `{"mcpServers": { ... }}`.

### 7.3 Add different MCP servers for *Agent B* (project B)
```bash
mkdir -p ~/agents/agent-b/.gemini && cd ~/agents/agent-b
# Different toolset than Agent A
gemini mcp add --scope project --transport sse notion https://mcp.notion.com/mcp
gemini mcp add --scope project --transport http linear https://mcp.linear.app/sse
```

### 7.4 Restrict tool visibility per agent (allowlist/denylist)
Within each project’s `./.gemini/settings.json`, you can scope which tools from a server are exposed via `includeTools`/`excludeTools`.
```json
{
  "mcpServers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "includeTools": ["list_pull_requests", "create_issue"],
      "excludeTools": ["delete_repo"],
      "trust": false
    }
  }
}
```
> Use `trust: false` for explicit confirmation on tool calls; set to `true` only for well‑audited servers.

### 7.5 Per‑agent secrets
Set env vars per project so only that agent can use them:
```bash
# In ~/agents/agent-a/.env
GITHUB_TOKEN=ghp_xxx
SENTRY_AUTH_TOKEN=sntr_xxx

# In ~/agents/agent-b/.env
NOTION_TOKEN=secret_xxx
LINEAR_API_KEY=lin_xxx
```
Reference them from `settings.json`:
```json
{
  "mcpServers": {
    "github": {
      "headers": { "Authorization": "Bearer ${GITHUB_TOKEN}" }
    }
  }
}
```

### 7.6 Running agents with isolated MCP toolsets
- Start each agent from its own project directory (so it picks up that project’s `./.gemini/settings.json`).
- If you orchestrate multiple agents, start each in a separate process with its project cwd.

### 7.7 Sub‑agents and MCP tools
Sub‑agents inherit the main process’ discovered tools. To constrain a sub‑agent, keep the parent project’s allowlist tight, or run sub‑agents in their own project/context if you need hard isolation.

### 7.8 OAuth‑protected servers
When adding an HTTP/SSE server that requires OAuth, Gemini will detect 401s and walk you through browser sign‑in. Ensure your machine can open a browser and receive redirects on `http://localhost:7777/oauth/callback`.

### Quick commands
```bash
# Add a local stdio server with env
gemini mcp add --scope project my-local python server.py --port 8080 -e API_KEY=$MY_KEY

# Remove a server from the current project
gemini mcp remove my-local
```
