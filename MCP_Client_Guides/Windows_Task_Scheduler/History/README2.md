# ClaudeCode Automation Scheduler Guide

## Overview
Use this repository as a template for running ClaudeCode agents on a schedule. The PowerShell launchers under `Scripts/` and the Windows Task Scheduler templates under `TaskSchedulers/` demonstrate how to reconnect to the AX platform MCP server and execute pre-scripted prompts throughout the day. Adapt the instructions below for any number of agents and for whichever scheduler you prefer (Windows Task Scheduler, cron, systemd timers, third-party tools, and so on).

## Repository contents
- `Scripts/` - Sample PowerShell entrypoints that call the Claude CLI with predefined prompts. Use these as references when creating scripts for your own agents.
- `TaskSchedulers/` - Exported Windows Task Scheduler templates that you can import and customize. Each XML file aligns with one automation scenario (daily MCP reconnect, portfolio research prompts, etc.).
- `guides/claudecode-paxai-integration-guide.md` - Detailed walkthrough for connecting ClaudeCode to the AX platform MCP server. Follow this guide whenever you define or update an agent configuration.

## 1. Create per-agent project folders
For every ClaudeCode agent you want to run on a schedule, create a dedicated project directory. A typical layout is:
```
Agents/
  AgentName/
    MCP.json
    instructions.md
    Scripts/
      run_claude.ps1
      run_claude_connect_mcp.ps1
```

Guidelines:
- Keep each agent self-contained. Store the MCP configuration (`MCP.json`), prompt instructions, and launch scripts together.
- Name the folder to match the agent identifier you configured in AX (for example, `FinancialResearch`, `OperationsBot`, or `Agent1`).
- When writing the PowerShell scripts, change the working directory dynamically rather than hard-coding a path:
  ```powershell
  Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)
  claude --dangerously-skip-permissions "Your prompt or slash command"
  ```
  This guarantees the script runs correctly no matter where the repository is cloned.

## 2. Configure MCP access for each agent
Every agent needs an MCP configuration that points to the AX platform server. Use the sampling and credential setup described in `guides/claudecode-paxai-integration-guide.md` to create a tailored `MCP.json` for each agent.

Checklist per agent:
- Confirm the `server` entry targets the AX MCP endpoint supplied by PaxAI.
- Add any required authentication tokens or certificates.
- Store companion files (private keys, environment variables) alongside the agent folder or in a secure secrets manager.
- Document the agent-specific instructions in `instructions.md` (or another file of your choice) so future edits stay synchronized with the MCP configuration.

## 3. Prepare scheduler scripts
Repurpose the sample launchers under `Scripts/Agent1` and `Scripts/Agent2` by copying them into each agent folder and editing the prompt text. Keep the command format consistent:
```
claude --dangerously-skip-permissions "Prompt text referencing your MCP workspace"
```

Create two categories of scripts when needed:
1. **MCP reconnect scripts** (for example, `run_claude_connect_mcp.ps1`) that issue the `/mcp` command to refresh the connection.
2. **Workload scripts** (for example, `run_claude.ps1`, `run_claude_market.ps1`) that run the specific instructions for that agent.

Store all scripts inside the agent folder (for example, `Agents/FinancialResearch/Scripts`). This keeps the scheduler configuration simple and avoids path confusion when cloning to new machines.

## 4. Import and customize scheduler templates
The XML files under `TaskSchedulers/` are ready-made exports from Windows Task Scheduler. Follow these steps to adapt them to your project:

1. Open **Task Scheduler** and select **Action > Import Task...**.
2. Choose the XML template that matches the automation you want. For example, `TaskSchedulers/ClaudeCode_ConnectToMCPServers_3.xml` reconnects to the MCP server mid-morning.
3. After importing, edit the single action on the **Actions** tab:
   - **Program/script**: `powershell.exe`
   - **Add arguments**: `-ExecutionPolicy Bypass -File "C:\Path\To\Agents\FinancialResearch\Scripts\run_claude_connect_mcp.ps1"`
   - **Start in**: `C:\Path\To\Agents\FinancialResearch\Scripts`
4. Adjust the **Triggers** tab to match the cadence you want (daily, weekly, multiple times per day, etc.).
5. Repeat for each agent and script you want scheduled. Use different template files or duplicate an imported task to build the schedule you need.

### Using the templates as blueprints
Even if you use another scheduler (for example, cron on Linux, Windows Task Scheduler deployed through Group Policy, or a third-party automation platform), the templates show the command-line invocation pattern. Adapt the command to your environment:
```
powershell.exe -ExecutionPolicy Bypass -File "<path-to-agent-script>.ps1"
```
Replace the path with the absolute location of the script inside the corresponding agent folder.

## 5. Example mapping between templates and scripts
Update the template names to match the scripts you created. The table below illustrates one possible mapping and the placeholders you should customize:

| Template | Purpose | Replace `<agent-path>` with |
| --- | --- | --- |
| `ClaudeCode_ConnectToMCPServers.xml` | Early-morning MCP reconnect | `C:\Path\To\Agents\Agent1\Scripts\run_claude_connect_mcp.ps1` |
| `ClaudeCode_ConnectToMCPServers_Agent1.xml` | Agent-specific MCP reconnect | `C:\Path\To\Agents\Agent1\Scripts\run_claude_connect_mcp.ps1` |
| `ClaudeCode_ConnectToMCPServers_2.xml` | Mid-morning reconnect | `C:\Path\To\Agents\Agent2\Scripts\run_claude_connect_mcp.ps1` |
| `ClaudeCode_FinancialAdvisors_InvestmentStrategyInsights.xml` | Example workload script | `C:\Path\To\Agents\InvestmentInsights\Scripts\run_claude.ps1` |
| `ClaudeCode_FinancialAdvisors_MarketSentimentScore.xml` | Example workload script | `C:\Path\To\Agents\Sentiment\Scripts\run_claude_market.ps1` |

Feel free to duplicate a template and rename it for additional agents or tasks; just remember to update the `URI` and `Description` fields inside the XML if you want a cleaner name in Task Scheduler.

## 6. Test, monitor, and iterate
- Use **Run** in Task Scheduler (or the equivalent in your automation platform) to confirm each task launches the right agent script without prompts.
- Monitor task history or log output for error codes such as `0x1`, which typically point to incorrect file paths.
- When editing prompts or MCP configuration, adjust only the script contents; the scheduler configuration can stay the same as long as the script filename and location do not change.

## 7. Version control
Track the entire setup in Git so that script revisions and scheduler exports remain traceable:
```
cd <path-to-your-clone>
git init
git add README.md Scripts TaskSchedulers Agents
git commit -m "Document ClaudeCode automation setup"
```
Push the repository to your preferred remote once satisfied. Commit updated XML exports or scripts whenever you change schedules, prompts, or MCP settings.

With agent folders organized, MCP configurations aligned to the AX platform, and scheduler templates customized to your environment, ClaudeCode can operate hands-free across multiple projects and time slots.
