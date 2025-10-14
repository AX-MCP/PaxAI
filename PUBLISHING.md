# Publishing PaxAI to MCP Registry

This document describes how to publish PaxAI to the official Model Context Protocol (MCP) Registry.

## Overview

PaxAI is published to the MCP Registry as a **remote deployment** server. Users don't install a package; instead, they configure their MCP clients to connect to the PaxAI API at `https://api.paxai.app/mcp`.

## Server Configuration

The `server.json` file contains all metadata about the PaxAI MCP server:
- **Name**: `io.github.michaelschecht/paxai`
- **Type**: Remote deployment (SSE transport)
- **Endpoint**: `https://api.paxai.app/mcp`
- **Authentication**: OAuth via GitHub

## Automated Publishing via GitHub Actions

The repository includes an automated GitHub Actions workflow that publishes to the MCP Registry.

### Trigger Publication

There are two ways to trigger publication:

#### 1. Tag-based Publication (Recommended)
Create and push a version tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

#### 2. Manual Workflow Dispatch
Go to GitHub Actions → "Publish to MCP Registry" → "Run workflow"

### What the Workflow Does

1. **Validates** `server.json` against the official MCP schema
2. **Installs** the MCP Publisher CLI
3. **Authenticates** using GitHub OIDC (no secrets needed!)
4. **Publishes** the server configuration to the registry
5. **Verifies** the publication

## Manual Publishing (Optional)

If you need to publish manually:

### Prerequisites
- Install the [MCP Publisher CLI](https://github.com/modelcontextprotocol/publisher)
- Have push access to this repository

### Steps

1. **Validate server.json**:
   ```bash
   python validate_server.py
   ```

2. **Install MCP Publisher CLI**:
   ```bash
   # macOS
   brew install modelcontextprotocol/tap/mcp-publisher

   # Linux/WSL
   curl -L https://github.com/modelcontextprotocol/publisher/releases/latest/download/mcp-publisher-linux-amd64 -o mcp-publisher
   chmod +x mcp-publisher
   sudo mv mcp-publisher /usr/local/bin/

   # Windows
   # Download from: https://github.com/modelcontextprotocol/publisher/releases
   ```

3. **Login via GitHub**:
   ```bash
   mcp-publisher login github
   ```
   Follow the OAuth flow to authenticate.

4. **Publish**:
   ```bash
   mcp-publisher publish
   ```

5. **Verify**:
   ```bash
   curl "https://registry.modelcontextprotocol.io/v0/servers?search=paxai"
   ```

## Namespace Information

- **Namespace**: `io.github.ax-mcp/*`
- **Authentication**: GitHub OAuth (automatic via OIDC in Actions)
- **Repository**: https://github.com/AX-MCP/PaxAI

This namespace is tied to the GitHub organization `AX-MCP` and requires GitHub authentication to publish.

## Updating the Registry Entry

To update the published server information:

1. Update `server.json` with your changes
2. Validate: `python validate_server.py`
3. Commit and push changes
4. Create a new version tag (e.g., `v1.1.0`)
5. Push the tag to trigger publication

## Troubleshooting

### Validation Fails
Run `python validate_server.py` locally to see detailed error messages.

### Authentication Fails
- For GitHub Actions: Ensure `id-token: write` permission is set
- For manual: Run `mcp-publisher login github` again

### Publication Timeout
The registry may take a few minutes to index new servers. Check again after 5-10 minutes.

### Server Not Appearing in Search
- Verify publication succeeded in GitHub Actions logs
- Check the server name matches: `io.github.michaelschecht/paxai`
- Search using: `curl "https://registry.modelcontextprotocol.io/v0/servers?search=paxai"`

## Resources

- [MCP Registry Documentation](https://modelcontextprotocol.io/registry)
- [Publishing Guide](https://github.com/modelcontextprotocol/registry/blob/main/docs/guides/publishing/publish-server.md)
- [GitHub Actions Publishing](https://github.com/modelcontextprotocol/registry/blob/main/docs/guides/publishing/github-actions.md)
- [PaxAI Platform](https://paxai.app)
