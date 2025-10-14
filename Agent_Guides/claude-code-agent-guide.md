# Guide: Setting Up Multiple Agents and Sub-Agents in Claude Code

This guide covers how to configure and manage multiple agents and sub-agents using **Claude Code CLI** (Anthropic).

---

## Prerequisites

- Installed **Claude Code CLI**
- Anthropic API key configured (`CLAUDE_API_KEY`)
- Node.js v18+ or Python 3.10+
- Access to your Claude workspace

---

## 1. Setting Up the Claude CLI

1. **Install the CLI tool:**
   ```bash
   npm install -g @anthropic-ai/claude-cli
   ```

2. **Authenticate:**
   ```bash
   claude login
   ```

3. **Initialize your project:**
   ```bash
   claude init multi-agent-demo
   ```

---

## 2. Creating Multiple Agents

Claude allows defining multiple agents in a single workspace.

1. **Create the main agent:**
   ```bash
   claude agent create --name main-agent --model claude-3-opus
   ```

2. **Add supporting agents:**
   ```bash
   claude agent create --name assistant-agent --model claude-3-sonnet
   ```

3. **List all agents:**
   ```bash
   claude agent list
   ```

Example configuration (`agents.json`):
```json
{
  "agents": [
    {
      "name": "main-agent",
      "model": "claude-3-opus",
      "description": "Handles main orchestration"
    },
    {
      "name": "assistant-agent",
      "model": "claude-3-sonnet",
      "description": "Assists with summarization tasks"
    }
  ]
}
```

---

## 3. Setting Up Sub-Agents

Sub-agents are child entities under a parent agent.

1. **Create a sub-agent:**
   ```bash
   claude agent create --name summarizer --parent main-agent --model claude-3-haiku
   ```

2. **Define hierarchy in configuration:**
   ```json
   {
     "main-agent": {
       "subagents": ["summarizer", "retriever"]
     }
   }
   ```

3. **Invoke sub-agents programmatically:**
   ```bash
   claude agent run summarizer --input "Summarize this report"
   ```

---

## 4. Managing Multi-Agent Workflows

Claude supports workflow orchestration through the CLI:

```bash
claude workflow create --name team-orchestration
claude workflow add-agent main-agent
claude workflow add-agent assistant-agent
claude workflow run --input "Develop a launch plan for Q4."
```

---

## 5. Monitoring and Logs

To view logs for a specific agent:

```bash
claude logs --agent main-agent
```

For real-time monitoring:

```bash
claude watch --agent assistant-agent
```

---

## 6. Best Practices

- Use **distinct agent roles** to separate tasks
- Keep sub-agents lightweight (e.g., summarization, retrieval)
- Secure API keys using environment variables
- Regularly sync CLI and dependencies

---

✅ **You now have a multi-agent and sub-agent setup running with Claude Code!**

---

## 7. Connect Each Agent/Sub‑Agent to Its Own MCP Servers

Claude Code supports MCP servers at **local**, **project**, and **user** scopes via `.mcp.json`. To give each agent its own toolset, prefer **project‑scoped** `.mcp.json` kept alongside that agent’s files.

### 7.1 Scopes refresher
- **Local scope (per‑project, private):** default when you run `claude mcp add` → stored under your project user settings
- **Project scope (shared):** `.mcp.json` in the repo root (checked in) — use `--scope project`
- **User scope:** applies across all projects — use `--scope user`

### 7.2 Project A (main agent + its sub‑agents)
1) Create a project for Agent A and initialize:
```bash
mkdir -p ~/agents/agent-a && cd ~/agents/agent-a
```
2) Add MCP servers only for this project:
```bash
claude mcp add --scope project --transport http github https://api.githubcopilot.com/mcp/
claude mcp add --scope project --transport http sentry https://mcp.sentry.dev/mcp
```
This creates/updates `./.mcp.json`:
```json
{
  "mcpServers": {
    "github": { "type": "http", "url": "https://api.githubcopilot.com/mcp/" },
    "sentry": { "type": "http", "url": "https://mcp.sentry.dev/mcp" }
  }
}
```

3) Grant sub‑agents specific MCP tools
Create `.claude/agents/code-reviewer.md`:
```markdown
---
name: code-reviewer
description: Expert reviewer. Use proactively after code changes.
tools: Read, Grep, Glob, Bash, github.list_pull_requests
model: sonnet
---
Focus on review quality and security. Prefer least‑privilege MCP calls.
```
> If `tools` is omitted, the sub‑agent inherits **all** available tools (including MCP). Specify explicit tools for least‑privilege.

### 7.3 Project B (a different agent with different MCP servers)
```bash
mkdir -p ~/agents/agent-b && cd ~/agents/agent-b
claude mcp add --scope project --transport http notion https://mcp.notion.com/mcp
claude mcp add --scope project --transport sse linear https://mcp.linear.app/sse
```

### 7.4 Lock down tool visibility per server
Use allow/deny lists in `.mcp.json`:
```json
{
  "mcpServers": {
    "github": {
      "type": "http,
      "url": "https://api.githubcopilot.com/mcp/",
      "includeTools": ["list_pull_requests", "create_issue"],
      "excludeTools": ["delete_repo"],
      "trust": false
    }
  }
}
```
> Keep `trust: false` for confirmation prompts; raise only for known‑safe servers.

### 7.5 Secrets per agent
Store tokens as env vars loaded by your shell or `.env` files, and expand in `.mcp.json`:
```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp",
      "headers": { "Authorization": "Bearer ${NOTION_TOKEN}" }
    }
  }
}
```

### 7.6 Authenticate & inspect
```bash
# Authenticate servers that require OAuth
/mcp  # then pick the server → Authenticate

# See what’s installed (including plugin-provided MCP servers)
/mcp
```

### 7.7 Running multiple agents concurrently
- Start each agent from its own project root so it reads that project’s `.mcp.json` and `.claude/agents/`.
- For concurrency, launch separate shells or processes per project so each one keeps its own MCP connections.

### 7.8 Import from Claude Desktop
If you already configured MCP in Claude Desktop, you can import those servers into Claude Code via the docs’ import flow. Keep only the servers needed by each agent; remove others to maintain least‑privilege.

### 7.9 Output and resource limits
Claude warns when MCP tool output is large; tune via env (e.g., `MAX_MCP_OUTPUT_TOKENS`).
