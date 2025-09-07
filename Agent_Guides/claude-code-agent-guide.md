# Claude Code Agents & MCP Integration Guide

## Table of Contents
- [Overview](#overview)
- [Understanding Claude Code Architecture](#understanding-claude-code-architecture)
- [MCP (Model Context Protocol) Fundamentals](#mcp-model-context-protocol-fundamentals)
- [Setting Up Claude Code](#setting-up-claude-code)
- [Creating Individual Agents](#creating-individual-agents)
- [Connecting to MCP Servers](#connecting-to-mcp-servers)
- [Configuration Scopes](#configuration-scopes)
- [Essential MCP Servers](#essential-mcp-servers)
- [Advanced Configurations](#advanced-configurations)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

Claude Code is Anthropic's command-line tool for agentic coding that enables developers to delegate coding tasks directly from the terminal. When combined with Model Context Protocol (MCP) servers, Claude Code becomes a powerful platform that can connect to external tools, databases, APIs, and services.

This guide covers how to create individual specialized agents within Claude Code and connect them to MCP servers for enhanced functionality.

## Understanding Claude Code Architecture

Claude Code functions as both an **MCP client** and **MCP server**:

### As an MCP Client
- Connects to multiple MCP servers to access their tools
- Can use tools from GitHub, databases, APIs, web browsers, etc.
- Maintains context across multiple server connections

### As an MCP Server
- Exposes Claude's own capabilities to other applications
- Provides tools like file editing, code analysis, and more
- Can be connected to by other MCP clients (like Claude Desktop)

## MCP (Model Context Protocol) Fundamentals

### What is MCP?
MCP is an open protocol developed by Anthropic that standardizes communication between AI models and external systems. It acts as a universal adapter, enabling Claude Code to interact with tools, databases, and services through a structured interface.

### MCP Architecture Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MCP Client    │◄──►│   MCP Server    │◄──►│  External Tool  │
│  (Claude Code)  │    │   (GitHub)      │    │   (GitHub API)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

- **Host/Client**: The application (Claude Code) that initiates requests
- **Server**: Exposes specific functionalities as tools or resources
- **Transport**: Communication layer (stdio, SSE, or HTTP)

### MCP Capabilities
MCP servers can provide three main types of capabilities:

1. **Resources**: File-like data that can be read by clients (API responses, file contents)
2. **Tools**: Functions that can be called by the LLM (with user approval)
3. **Prompts**: Pre-written templates that help users accomplish tasks

## Setting Up Claude Code

### Prerequisites
- **Operating Systems**: macOS 10.15+, Ubuntu 20.04+/Debian 10+, or Windows via WSL
- **Hardware**: 4GB RAM minimum
- **Software**: Node.js 18+, git 2.23+ (optional)
- **Network**: Internet connection for authentication and AI processing

### Installation

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version

# Run initial setup and doctor check
claude
claude /doctor
```

**Important**: Do NOT use `sudo npm install -g` as this can lead to permission issues.

### Windows Setup
Claude Code requires WSL on Windows:

```bash
# If using WSL and encountering node errors
sudo apt update
sudo apt install nodejs npm

# Verify WSL is using Linux npm, not Windows npm
which npm
```

## Creating Individual Agents

Claude Code supports creating specialized agents through the `/agents` command and custom prompt templates.

### Method 1: Using the /agents Command

```bash
# Start Claude Code
claude

# Create a new specialized agent
/agents

# Follow the interactive prompts to define:
# - Agent name and description
# - Specific expertise areas
# - Context and capabilities
# - Usage examples
```

### Method 2: Custom Slash Commands

Create reusable prompt templates in the `.claude/commands` folder:

```bash
# Create commands directory
mkdir -p .claude/commands

# Create a specialized agent command
cat > .claude/commands/mcp-expert.md << 'EOF'
# MCP Protocol Expert Agent

You are an expert in Model Context Protocol (MCP) development with deep knowledge of:

- Building MCP clients and servers
- Debugging MCP applications  
- Understanding protocol specifications
- Implementing MCP solutions using Python or TypeScript SDKs
- Creating new MCP servers
- Integrating MCP clients into applications
- Troubleshooting connection issues
- Optimizing MCP implementations
- MCP architecture and best practices

When helping with MCP tasks, provide detailed technical guidance, code examples, and step-by-step implementation instructions.
EOF
```

### Method 3: Project-Specific Agents

Create agents that are shared across your team by checking them into version control:

```bash
# Create team-shared commands
mkdir -p .claude/commands
git add .claude/commands/
git commit -m "Add specialized agent commands"
```

### Agent Examples

#### Database Expert Agent
```markdown
# Database Expert Agent

You are a database specialist focused on:
- SQL query optimization
- Database schema design
- Data migration strategies
- Performance tuning
- Database security best practices

Use this agent for database-related tasks and always consider performance implications.
```

#### API Integration Agent
```markdown
# API Integration Agent

You are an API integration specialist with expertise in:
- RESTful API design
- OpenAPI/Swagger specifications
- API authentication and security
- Rate limiting and error handling
- API testing and documentation

Focus on creating robust, scalable API integrations.
```

## Connecting to MCP Servers

### Basic MCP Server Addition

```bash
# Add an MCP server (local scope - default)
claude mcp add <server-name> -- <command> [args...]

# Example: Add GitHub MCP server
claude mcp add github-server -- npx -y @modelcontextprotocol/server-github

# Add with environment variables
claude mcp add postgres-server \
  -e DATABASE_URL=postgresql://user:pass@localhost:5432/db \
  -- npx -y @modelcontextprotocol/server-postgres
```

### Server-Sent Events (SSE) Configuration

```bash
# Add an SSE-based MCP server
claude mcp add my-sse-server \
  --transport sse \
  --endpoint http://localhost:3000/sse \
  -e API_KEY=your-api-key
```

### JSON Configuration Method

```bash
# Add server from JSON configuration
claude mcp add-from-json '{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token"
  }
}'
```

## Configuration Scopes

MCP servers can be configured at three different scope levels:

### Local Scope (Default)
- **When to use**: Personal development, experimental configurations
- **Storage**: Project-specific user settings
- **Accessibility**: Only you, only in current project

```bash
claude mcp add server-name -s local -- command args
```

### Project Scope
- **When to use**: Team-shared servers, project-specific tools
- **Storage**: `.mcp.json` file (checked into version control)
- **Accessibility**: Everyone working on the project

```bash
claude mcp add server-name -s project -- command args
```

This creates a `.mcp.json` file:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "command",
      "args": ["args"],
      "env": {
        "KEY": "value"
      }
    }
  }
}
```

### User Scope  
- **When to use**: Personal tools across all projects
- **Storage**: User-specific global settings
- **Accessibility**: Only you, across all projects

```bash
claude mcp add server-name -s user -- command args
```

### Scope Precedence
1. **Local-scoped** servers (highest priority)
2. **Project-scoped** servers (`.mcp.json`)
3. **User-scoped** servers (lowest priority)

## Essential MCP Servers

### 1. GitHub Integration

```bash
# Add GitHub MCP server
claude mcp add github \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=your-token \
  -- npx -y @modelcontextprotocol/server-github

# Usage examples:
# "Add the feature described in JIRA issue ENG-4521 and create a PR on GitHub"
# "Check the latest commits on the main branch"
```

### 2. PostgreSQL Database

```bash
# Add PostgreSQL MCP server
claude mcp add postgres \
  -e DATABASE_URL=postgresql://user:pass@localhost:5432/database \
  -- npx -y @modelcontextprotocol/server-postgres

# Usage examples:
# "Find emails of users who used feature ENG-4521"
# "Show me the database schema for the users table"
```

### 3. File System Operations

```bash
# Add filesystem MCP server
claude mcp add filesystem \
  -e ALLOWED_DIRECTORIES=/path/to/project,/path/to/docs \
  -- npx -y @modelcontextprotocol/server-filesystem

# Usage examples:
# "Read all markdown files in the docs directory"
# "Create a new configuration file based on the template"
```

### 4. Web Automation (Puppeteer)

```bash
# Add Puppeteer MCP server
claude mcp add puppeteer \
  -- npx -y @modelcontextprotocol/server-puppeteer

# Usage examples:
# "Navigate to our staging site and test the login flow"
# "Take a screenshot of the homepage and analyze the layout"
```

### 5. Notion Integration

```bash
# Add Notion MCP server
claude mcp add notion \
  -e NOTION_API_KEY=your-notion-token \
  -- npx -y @modelcontextprotocol/server-notion

# Usage examples:
# "Create a project update page in Notion"
# "Search for all meeting notes that mention the API migration"
```

### 6. Context7 (Documentation Search)

```bash
# Add Context7 for live documentation access
claude mcp add context7 \
  -e CONTEXT7_API_KEY=your-api-key \
  -- npx -y context7-mcp

# Usage examples:
# "Create a React component using the latest Next.js patterns - use context7"
```

## Advanced Configurations

### Environment Variable Management

```bash
# Set multiple environment variables
claude mcp add complex-server \
  -e API_KEY=key1 \
  -e DATABASE_URL=postgres://... \
  -e DEBUG=true \
  -- npx -y complex-mcp-server

# Use environment files
export $(cat .env | xargs)
claude mcp add server-name -- command args
```

### Custom MCP Server Timeouts

```bash
# Configure server startup timeout (10 seconds)
MCP_TIMEOUT=10000 claude

# Or set globally
export MCP_TIMEOUT=15000
```

### Importing from Claude Desktop

```bash
# Import existing Claude Desktop MCP configurations
claude mcp import-from-claude-desktop

# Import to global scope
claude mcp import-from-claude-desktop -s global
```

### Using Claude Code as an MCP Server

```bash
# Start Claude Code as an MCP server
claude mcp serve

# In another terminal or application, connect to:
# stdio transport with command: claude mcp serve
```

## Best Practices

### 1. Agent Specialization
- Create focused agents for specific domains (database, API, frontend, etc.)
- Use descriptive names and clear capability descriptions
- Document agent usage in your team's README

### 2. MCP Server Management
- Use project scope for team-shared servers
- Use local scope for experimental or personal servers
- Use user scope for tools you want across all projects

### 3. Security Considerations
- **Trust verification**: Only use MCP servers from trusted sources
- **Environment variables**: Store sensitive credentials securely
- **Permissions**: Use minimal required permissions for database connections
- **Prompt injection risk**: Be cautious with servers that fetch external content

### 4. Performance Optimization
- **Scope precedence**: Understand which servers take priority
- **Resource management**: Use servers with efficient resource usage
- **Debugging**: Use `--mcp-debug` flag to troubleshoot issues

### 5. Team Collaboration
- Check `.mcp.json` into version control
- Document required environment variables in README
- Create setup scripts for new team members

### Example Team Setup Script
```bash
#!/bin/bash
# setup-mcp.sh - Team MCP server setup

echo "Setting up MCP servers for the project..."

# Check if required environment variables are set
required_vars=("GITHUB_TOKEN" "DATABASE_URL" "NOTION_API_KEY")
for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
        echo "Error: $var environment variable is not set"
        exit 1
    fi
done

# Add project-scoped servers
claude mcp add github -s project \
  -e GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_TOKEN \
  -- npx -y @modelcontextprotocol/server-github

claude mcp add postgres -s project \
  -e DATABASE_URL=$DATABASE_URL \
  -- npx -y @modelcontextprotocol/server-postgres

claude mcp add notion -s project \
  -e NOTION_API_KEY=$NOTION_API_KEY \
  -- npx -y @modelcontextprotocol/server-notion

echo "MCP servers configured successfully!"
echo "Run 'claude /mcp' to verify server status"
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Server Connection Failures

```bash
# Check server status
claude /mcp

# Debug MCP connections
claude --mcp-debug

# Check Claude logs (macOS)
tail -n 20 -f ~/Library/Logs/Claude/mcp*.log
```

#### 2. Permission Issues

```bash
# Reset project choices for security prompts
claude mcp reset-project-choices

# Verify server configuration
claude mcp list
```

#### 3. Environment Variable Problems

```bash
# Test environment variables
echo $GITHUB_PERSONAL_ACCESS_TOKEN

# Verify server configuration
claude mcp show server-name
```

#### 4. Windows/WSL Issues

```bash
# For npm execution issues on Windows
claude mcp add server-name -- cmd /c npx -y package-name

# Check WSL Node.js installation
which node
which npm
```

#### 5. Server Not Showing Up

1. **Restart Claude Code completely**
2. **Check configuration file syntax** (for project-scoped servers)
3. **Verify server installation**: `npx -y package-name --help`
4. **Check logs** for specific error messages

### Debug Mode

```bash
# Enable debug logging
export MCP_CLAUDE_DEBUG=true
claude --mcp-debug

# Check specific server logs
tail -f ~/.claude/logs/mcp-server-SERVERNAME.log
```

### Recovery Commands

```bash
# Remove problematic server
claude mcp remove server-name

# Reset all MCP configuration
claude mcp reset

# Re-add servers from scratch
claude mcp add server-name -- command args
```

## Conclusion

Claude Code with MCP servers transforms coding from individual tasks into collaborative workflows with specialized AI agents. By following this guide, you can:

- Create focused, specialized agents for different domains
- Connect to powerful external tools and services
- Share configurations with your team
- Build robust, scalable development workflows

The key to success is starting with essential servers that match your workflow, then gradually expanding your MCP ecosystem as you identify new automation opportunities.

For the latest updates and community-contributed servers, visit:
- [Official MCP Documentation](https://modelcontextprotocol.io/)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [MCP Community Hub](https://www.claudemcp.com/)