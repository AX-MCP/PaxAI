# Guide: Multi‑“Agent” Setups with GitHub Copilot **CLI** (and per‑agent MCP servers)

---

## 0) What you’ll need

- **GitHub Copilot CLI** (Public Preview) installed and enabled for your plan.
- A GitHub account signed in via `copilot` → `/login`.
- Optional: `tmux` or multiple terminal windows for concurrent “agents”.

**References**
- Install & use Copilot CLI; slash commands; MCP config path.  
- Extending Copilot with MCP; where configs live and examples.  
- Coding agent + MCP limitations (tools only; OAuth caveats).

---

## 1) Install and start Copilot CLI

```bash
# Install (see official instructions for your OS)
# Then in a repo (or a new empty folder) start Copilot CLI:
copilot
# If prompted, /login and trust the folder for the session
```

- Resume a previous session: `copilot --resume`  
- Trust & directory management: `/add-dir /path/to/dir`, change cwd with `/cwd /path/to/dir`.  
- In‑session help: `?` or `copilot help`.

> 📌 The CLI is agentic and can read/modify/execute files; you must approve tools when prompted.

---

## 2) Pattern A — Per‑“Agent” via **separate working directories**

Create a folder for each “agent” and keep its config + instructions inside it.

```bash
mkdir -p ~/agents/repo-a ~/agents/repo-b
cd ~/agents/repo-a && git init
cd ~/agents/repo-b && git init
```

Start **one Copilot CLI session per folder** (separate terminals). Each session will keep its **own MCP configuration** and instruction files.

### 2.1 Per‑agent instructions
Put guidance in the repo so it’s auto‑included by the CLI:

```
./.github/copilot-instructions.md
./.github/copilot-instructions/security.instructions.md
AGENTS.md
```

Examples for two different “agents”:

**Repo A** (`AGENTS.md` excerpt)
```markdown
# Agent: Release Manager
Scope: versioning, changelog, tagging, GH releases.
Principles: least-privilege; draft PRs; never push to main.
```

**Repo B** (`AGENTS.md` excerpt)
```markdown
# Agent: Infra Maintainer
Scope: IaC changes, CI/CD updates, dependency bumps.
Principles: propose changes in branches; run tests; require approvals.
```

---

## 3) Pattern B — Per‑“Agent” via **separate config homes**

If you prefer to keep multiple “agents” in the *same* folder (or want hard separation), run each session with its own **config directory**, so each has an isolated **`mcp-config.json`** and **`config.json`**:

```bash
# Agent A
XDG_CONFIG_HOME=~/.config/agentA copilot

# Agent B
XDG_CONFIG_HOME=~/.config/agentB copilot
```

This creates/uses different config files (including MCP). Handy for switching “roles” without changing the repo.

---

## 4) Add **different MCP servers** to each “agent”

Inside each session, use the slash command to add servers. The CLI stores them in **`mcp-config.json`** under the active config home.

```text
/mcp add
# Fill in: server name, command or URL (HTTP/SSE if supported), args, env, etc.
# Press Ctrl+S to save.
```

- Default path: **`${XDG_CONFIG_HOME:-~/.config}/mcp-config.json`**.  
- List/inspect via `/mcp`; remove/update via the same UI.  
- The GitHub MCP Server is preconfigured to act on GitHub (PRs, merges) from the CLI.

### Example: Two “agents” with different toolsets

**Agent A (Release Manager)** — add GitHub + Fetch
```
/mcp add
name: github
type: builtin (preconfigured)

/mcp add
name: fetch
command: uvx
args: mcp-server-fetch
```

**Agent B (Infra Maintainer)** — add Linear + Notion (SSE/HTTP examples; adjust per server docs)
```
/mcp add
name: linear
type: sse
url: https://mcp.linear.app/sse
env: LINEAR_API_KEY=${LINEAR_API_KEY}

/mcp add
name: notion
type: http
url: https://mcp.notion.com/mcp
headers: Authorization=Bearer ${NOTION_TOKEN}
```

> Keep secrets in your shell env when you launch the session, e.g.  
> `LINEAR_API_KEY=lin_xxx NOTION_TOKEN=secret_xxx XDG_CONFIG_HOME=~/.config/agentB copilot`

### Where the config lives (CLI‑managed)
```json
// ~/.config/mcp-config.json  (or under your XDG_CONFIG_HOME override)
{
  "servers": {
    "fetch":  { "command": "uvx", "args": ["mcp-server-fetch"] },
    "linear": { "type": "sse", "url": "https://mcp.linear.app/sse" },
    "notion": { "type": "http", "url": "https://mcp.notion.com/mcp" }
  }
}
```

---

## 5) Emulating sub‑agents (task‑scoped roles)

Until sub‑agents are available in the CLI, emulate them by splitting responsibilities:
- **Shell orchestration:** run multiple terminals (or `tmux` windows), one per role.
- **Prompt files:** keep role prompts in `prompts/` and paste or reference them.
- **Task hand‑offs:** ask Agent A to produce a branch/PR; ask Agent B to review and patch.
- **Policy files:** codify rules in `.github/copilot-instructions/**/*.instructions.md` for least‑privilege workflows.

> Note: The Copilot **coding agent** currently supports **MCP tools** only (no MCP resources/prompts) and has limitations with some **OAuth** remote MCP servers. Choose token‑based or local servers when possible.

---

## 6) Security & governance tips

- **Least‑privilege MCP:** Only add the servers each role truly needs; favor local/stdio servers you control.
- **Human approvals:** Keep command approvals on; avoid blanket approval for destructive tools.
- **Org policy:** Enterprises can allow/deny MCP usage via admin policy.
- **Auditability:** Keep sessions tied to branches and PRs; avoid running as root.
- **Secrets:** Inject per‑session env vars; do not hardcode tokens in `mcp-config.json`.

---

## 7) Quick recipes

### 7.1 Two isolated agents using config homes
```bash
# Terminal 1
export XDG_CONFIG_HOME=~/.config/agentA
export RELEASE_NOTES_TOKEN=...
copilot   # add: github, fetch

# Terminal 2
export XDG_CONFIG_HOME=~/.config/agentB
export LINEAR_API_KEY=... NOTION_TOKEN=...
copilot   # add: linear, notion
```

### 7.2 Repo‑scoped roles with instructions
```
repo/
  .github/copilot-instructions.md
  .github/copilot-instructions/release.instructions.md
  .github/copilot-instructions/infra.instructions.md
  AGENTS.md
```

---

## 8) Troubleshooting

- **“Where is my MCP file?”** `${XDG_CONFIG_HOME:-~/.config}/mcp-config.json`.
- **Server won’t start?** Ensure command/URL is reachable and required env vars are set **in the same shell** before launching `copilot`.
- **OAuth server blocked?** Some remote MCP servers with OAuth aren’t supported by the coding agent—prefer tokens or local servers.
- **Org disabled MCP?** Ask an admin to enable “MCP servers in Copilot” policy.

---

## 9) Handy commands

- Start: `copilot` (resume: `--resume`)
- Add MCP server: `/mcp add`
- Usage stats: `/usage`
- Help: `?`, `copilot help`, `copilot help config`, `copilot help permissions`

---

_This guide mirrors the workflow patterns you used for Gemini CLI and Claude Code, adapted to the realities of GitHub Copilot CLI today._
