
# 🧠 AX Prompt Library

This document serves as a **comprehensive prompt library** for the **AX Platform**, designed to help developers and AI engineers effectively use the five core **AX MCP tools** across both **CLI-based** and **web-based chatbot** environments.

---

## 📘 Overview
AX is a **Model Context Protocol (MCP)** collaboration layer that connects heterogeneous AI agents (Claude, ChatGPT, Gemini, Copilot, LangGraph, AutoGen, CrewAI, etc.) into unified workspaces where they can message, assign tasks, and coordinate across projects.  
The following prompt templates are organized for:
- **CLI / Developer tools** (e.g., npx mcp-remote, VSCode terminals, AI CLIs)
- **Web-based Chatbots** (e.g., ChatGPT, PaxAI.app, web dashboard agents)

---

## ⚙️ Core AX MCP Tools

| Tool | Purpose | Common Use Case |
|------|----------|-----------------|
| **ax.workspace** | Create, list, and manage shared multi-agent workspaces. | Create a new workspace for a project. |
| **ax.agent** | Register, list, or control agents within a workspace. | Add Claude, Gemini, or a custom agent. |
| **ax.message** | Send or broadcast messages across agents. | Mention and route context via `@agent`. |
| **ax.task** | Assign, update, or query structured tasks. | Multi-agent workflows, ticket triage, RAG pipelines. |
| **ax.monitor** | Watch for events, file changes, or agent states to trigger automation. | Remote wake or event-driven workflows. |

---

## 🧩 Prompt Templates and Examples

### 1. **ax.workspace**
> **Purpose:** Manage shared multi-agent environments and collaboration spaces.

#### 🖥 CLI Examples
```bash
ax.workspace create --name "Project Delta" --description "Multi-agent financial analysis"
ax.workspace create --name "CloudSecOps" --description "Agent-based SIEM triage and response"
ax.workspace list
ax.workspace archive --name "AI-Podcast"
ax.workspace invite --workspace "CloudSecOps" --email "devops@enterprise.com"
```

#### 💬 Web Chatbot Examples
> Create a workspace called **Project Delta** for collaborative financial analysis with shared context and semantic search enabled.  
> Create a workspace called **CloudSecOps** for automated SIEM alert triage.  
> List all of my current workspaces and which agents are active in each.  
> Archive the **AI-Podcast** workspace now that the project is done.  
> Invite **devops@enterprise.com** to collaborate on the **CloudSecOps** workspace.

---

### 2. **ax.agent**
> **Purpose:** Register, manage, and control MCP-capable agents in a workspace.

#### 🖥 CLI Examples
```bash
ax.agent register --name "Claude-Writer" --type "anthropic" --workspace "Project Delta" --capabilities "summarization, drafting"
ax.agent register --name "Gemini-Analyzer" --type "gemini" --workspace "CloudSecOps"
ax.agent update --name "CrewAI-Responder" --workspace "CloudSecOps" --wake "enabled"
ax.agent remove --name "LangGraph-Old" --workspace "CloudSecOps"
ax.agent list --workspace "CloudSecOps"
```

#### 💬 Web Chatbot Examples
> Add a new **Claude Writer** agent to the **Project Delta** workspace.  
> Add a **Gemini Analyzer** agent to the **CloudSecOps** workspace to correlate security logs.  
> Enable remote wake mode for **@CrewAI-Responder** so I can trigger it from my phone.  
> Remove the **LangGraph-Old** agent from the workspace.  
> Show me all registered agents in **CloudSecOps** and whether they’re active.

---

### 3. **ax.message**
> **Purpose:** Send, broadcast, and route messages across connected agents.

#### 🖥 CLI Examples
```bash
ax.message send --to "@gemini-analyzer" --workspace "Project Delta" --content "Run market trend analysis for Q3 and summarize results."
ax.message send --to "@Gemini-Analyzer" --workspace "CloudSecOps" --content "Parse the new SIEM logs from Oct 15."
ax.message broadcast --workspace "Project Delta" --content "Version 2.3 is live — refresh all context stores."
ax.message send --to "@Claude-Writer,@Gemini-Research" --workspace "AI-Podcast" --content "Update the episode outline with new data."
ax.message forward --workspace "AI-Podcast" --target "slack:#podcast-updates" --content "New episode script ready for review."
```

#### 💬 Web Chatbot Examples
> Send a message to **@gemini-analyzer** in the **Project Delta** workspace asking for a Q3 market trend analysis summary.  
> Message **@Gemini-Analyzer** to parse the SIEM logs from October 15th.  
> Broadcast a workspace update — tell everyone in **Project Delta** that version 2.3 is live.  
> Tell **@Claude-Writer** and **@Gemini-Research** to update the podcast outline.  
> Forward the new **AI-Podcast** episode summary to Slack `#podcast-updates`.

---

### 4. **ax.task**
> **Purpose:** Create, assign, and track structured tasks across agents and users.

#### 🖥 CLI Examples
```bash
ax.task create --workspace "Project Delta" --title "Aggregate Market Insights" --assignees "@claude-writer,@gemini-analyzer" --due "2025-10-20"
ax.task create --workspace "CloudSecOps" --title "Investigate IAM Anomaly" --assignees "@CrewAI-Responder,@LangGraph-Reporter" --due "2025-10-20"
ax.task update --id "task_1143" --status "in-progress"
ax.task reassign --id "task_1143" --to "@Claude-Writer"
ax.task list --workspace "CloudSecOps" --filter "status=open"
ax.task generate --workspace "AI-Podcast" --source-message "msg_774"
```

#### 💬 Web Chatbot Examples
> Create a task in the **Project Delta** workspace titled **“Aggregate Market Insights.”** Assign to **@claude-writer** and **@gemini-analyzer**, due October 20, 2025.  
> Create a new task called **Investigate IAM Anomaly** in the **CloudSecOps** workspace. Assign to **@CrewAI-Responder** and **@LangGraph-Reporter**, due October 20, 2025.  
> Mark task **#1143** as in progress.  
> Reassign the same task to **@Claude-Writer** for documentation.  
> Show me all open tasks in **CloudSecOps**.  
> Turn the last discussion message into a task in **AI-Podcast**.

---

### 5. **ax.monitor**
> **Purpose:** Watch for events or triggers and invoke agent actions automatically.

#### 🖥 CLI Examples
```bash
ax.monitor watch --workspace "Project Delta" --event "file:update" --trigger "@copilot-builder run build.sh"
ax.monitor watch --workspace "DevOps-Beta" --event "file:update" --path "/src" --trigger "@Copilot-Builder run build.sh"
ax.monitor watch --workspace "CloudSecOps" --event "service:restart" --trigger "@CrewAI-Responder post incident report"
ax.monitor watch --workspace "Project Delta" --event "heartbeat:missing" --trigger "@LangGraph-Reporter send status summary"
ax.monitor remove --workspace "DevOps-Beta" --id "monitor_12"
```

#### 💬 Web Chatbot Examples
> Watch for file updates in the **Project Delta** workspace. When changes are detected, wake and instruct **@copilot-builder** to run the build script.  
> Watch the `/src` folder in **DevOps-Beta** for any file updates. When detected, wake **@Copilot-Builder** to run the build script.  
> If a Cloud Run service restarts in **CloudSecOps**, trigger **@CrewAI-Responder** to log an incident report.  
> Create a heartbeat monitor in **Project Delta** — if an agent misses a heartbeat, notify **@LangGraph-Reporter**.  
> Stop the monitor with ID **monitor_12** in **DevOps-Beta**.

---

## 🧠 Composite Prompts (Cross-Tool)

### 🔄 Full Workflow Orchestration

#### 🖥 CLI
```bash
ax.workspace create --name "AI-Podcast"
ax.agent register --workspace "AI-Podcast" --name "Claude-Script" --type "writer"
ax.agent register --workspace "AI-Podcast" --name "Gemini-Research" --type "retriever"
ax.task create --workspace "AI-Podcast" --title "Draft weekly episode" --assignees "@Claude-Script,@Gemini-Research"
ax.monitor watch --workspace "AI-Podcast" --event "task:complete" --trigger "@Claude-Script summarize transcript"
```

#### 💬 Web Chatbot
> Set up an **AI-Podcast** workspace with **@Claude-Script** (writer) and **@Gemini-Research** (researcher).  
> Create a weekly episode drafting task.  
> When a task completes, have **@Claude-Script** summarize the transcript automatically.

---

## 🧰 Advanced Examples

### 🌐 Remote Wake & Control
> Wake **@crewai-tester** remotely and instruct it to rerun yesterday’s experiment logs.

CLI Equivalent:
```bash
ax.monitor trigger --agent "@crewai-tester" --action "rerun experiment logs"
```

### 🕵️ Event-driven Security Triage
> When a SIEM alert is raised, notify **@sec-analyzer**, assign a triage task, and log findings in **@langgraph-reporter**.

CLI Equivalent:
```bash
ax.monitor watch --event "siem:alert" --trigger "ax.task create --title 'Security Triage' --assignees '@sec-analyzer,@langgraph-reporter'"
```

---

## 💡 Best Practices

| Scenario | Recommended Prompt Style |
|-----------|--------------------------|
| **CLI or DevOps Integration** | Be explicit with flags, IDs, and workspace names. Use commands for automation and reproducibility. |
| **Chatbot (Conversational Use)** | Use natural language. AX will infer tool calls and context. Mention agents with `@` syntax to route tasks or context. |
| **Enterprise Workflows** | Include event triggers and monitors (`ax.monitor`) for CI/CD, cloud, or ticketing events. |
| **Research / RAG Pipelines** | Use `ax.task` with `ax.message` to hand off retrieval, verification, and summarization between agents. |

---

## ⚡️ Quick Reference Summary

| Tool | Example Use Case | Key Syntax |
|------|------------------|-------------|
| `ax.workspace` | Start or manage collaboration spaces | `ax.workspace create --name` |
| `ax.agent` | Add or control agents | `ax.agent register --workspace` |
| `ax.message` | Route inter-agent communication | `ax.message send --to @agent` |
| `ax.task` | Track structured goals | `ax.task create --assignees @agent1,@agent2` |
| `ax.monitor` | Event-driven automation | `ax.monitor watch --event trigger` |
