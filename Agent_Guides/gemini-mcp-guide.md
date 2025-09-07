# Technical Guide: Connecting Gemini CLI to an MCP Server

[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#)

## Overview

The Gemini Command Line Interface (CLI) is a powerful, open-source AI agent that operates directly in your terminal. Its functionality can be extended by connecting to custom or third-party Model Context Protocol (MCP) servers, which provide new tools and capabilities. 

This guide will walk you through:
- Installing the Gemini CLI agent
- Configuring it to connect to an MCP server
- Customizing its core behavior with specialized personas

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Custom Agent Personas](#custom-agent-personas)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have:

- **Node.js** (version 18 or higher) - The Gemini CLI is built on Node.js
- **Terminal/Command Line access**
- **Text editor** for configuration files

## Installation

### Step 1: Install the Gemini CLI Agent

The Gemini CLI is the AI agent itself. There is no separate "create agent" command; by installing the CLI, you are setting up your own local AI agent.

```bash
npm install -g @google/gemini-cli
```

> **Note:** This command installs the CLI globally, making the `gemini` command available from any directory.

## Configuration

### Step 2: Locate the Gemini CLI Settings File

The configuration for connecting to MCP servers is managed in a settings JSON file. The location depends on your operating system:

| OS | Path |
|---|---|
| **Linux** | `~/.gemini/settings.json` |
| **macOS** | `~/.gemini/settings.json` |
| **Windows** | `%APPDATA%\Gemini\settings.json` |

Open this file in your preferred text editor. If the file or the `.gemini` directory does not exist, you will need to create them.

### Step 3: Add the MCP Server Configuration

Within the `settings.json` file, you will add a `mcpServers` object. Each key represents a name for your server, and the value is a configuration object containing the server's details.

#### Basic Configuration

```json
{
  "mcpServers": {
    "my-server-name": {
      "url": "http://your-mcp-server-url:port/endpoint"
    }
  }
}
```

#### Configuration with Authentication

If the MCP server requires authentication (e.g., an API key or token):

```json
{
  "mcpServers": {
    "my-auth-server": {
      "url": "http://your-auth-server-url",
      "params": {
        "api_key": "your-api-key-here"
      }
    }
  }
}
```

> **⚠️ Security Note:** Replace placeholder values with actual server URLs and credentials. Keep your API keys secure and never commit them to version control.

## Custom Agent Personas

### Step 4: Define a Custom Agent Persona

While MCP servers add external tools, you can also define the core persona or function of your Gemini CLI agent by creating a custom system prompt.

#### 4.1 Create a Markdown File

In your project directory, create a new file (e.g., `financial_analyst.md` or `ai_researcher.md`).

#### 4.2 Write the Persona Prompt

Inside this markdown file, write detailed instructions for the agent's behavior. The more specific you are, the better the results.

**Example: Financial Analyst**

```markdown
# System Prompt for a Financial Analyst

You are a senior financial analyst with over 20 years of experience. Your primary function is to analyze market trends, interpret earnings reports, and provide investment insights. 

## Guidelines:
- Your responses should be formal, data-driven, and cite credible sources
- When analyzing a company, look for the latest quarterly report
- Summarize key performance indicators, revenue growth, and future outlook
- **Important:** You must not provide financial advice
```

**Example: AI Researcher**

```markdown
# System Prompt for an AI Researcher

You are a leading AI researcher specializing in large language models and multi-modal systems. Your role is to stay up-to-date with the latest academic papers and research from institutions like Google DeepMind, OpenAI, and universities.

## Guidelines:
- Responses should be technical, referencing specific research papers
- Reference frameworks like ReAct, Chain-of-Thought
- Explain concepts in a way accessible to other AI practitioners
```

#### 4.3 Set the Environment Variable

Before running the Gemini CLI, tell it to use your custom system prompt by setting the `GEMINI_SYSTEM_MD` environment variable.

**Linux/macOS:**
```bash
export GEMINI_SYSTEM_MD="/path/to/your/financial_analyst.md"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_SYSTEM_MD="C:\path\to\your\financial_analyst.md"
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_SYSTEM_MD = "C:\path\to\your\financial_analyst.md"
```

### Step 5: Reload the Gemini CLI

After saving your `settings.json` file with the new MCP server configuration:

1. **IDE Users (VS Code, IntelliJ):** Reload the window
2. **Terminal Users:** Close and re-open the Gemini CLI session

## Usage

### Step 6: Verify the Connection

Once the CLI has reloaded, use the built-in `/mcp` command to verify that your server is connected:

```bash
/mcp
```

This command will list:
- All configured MCP servers
- Their connection status  
- Available tools

✅ If the status shows "connected," you're ready to use the tools provided by your MCP server.

### Example Usage

Use your newly connected tools within the Gemini CLI using the `@` symbol followed by the server name and tool command:

```bash
> @my-server-name list-available-tools
```

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Command not found | Ensure Node.js 18+ is installed and CLI is globally installed |
| Server not connecting | Check URL format and network connectivity |
| Environment variable not working | Restart terminal after setting the variable |
| Settings file not found | Create the `.gemini` directory and `settings.json` manually |

### Getting Help

- Check the [Gemini CLI documentation](https://github.com/google/gemini-cli)
- Review MCP server-specific documentation for configuration details
- Verify JSON syntax in your `settings.json` file

## Contributing

This guide covers the core steps for extending your Gemini CLI's capabilities. Remember that specific configuration details for each MCP server may vary, so always refer to the server's own documentation for precise instructions.

---

> **💡 Pro Tip:** Start with a simple configuration and gradually add complexity as you become more familiar with the system.