# ClaudeCode Windows Task Scheduler Guide

## Overview
This repository packages the PowerShell launchers and Windows Task Scheduler exports used to run ClaudeCode CLI automations against an MCP server throughout the workday. The XML files under `TaskSchedulers/` are the exported task definitions and the scripts under `Scripts/` contain the actual Claude CLI invocations. The examples below show how to import `ClaudeCode_ConnectToMCPServers_3` so that it reconnects to your MCP servers several times per day, and how to adjust the other exported tasks.

## Repository layout
- `Scripts/Agent1` - Tasks that operate inside the Agent 1 Claude workspace. Each script currently changes directory before calling `claude` with a specific prompt.
- `Scripts/Agent2` - Companion scripts for Agent 2 workload automation.
- `TaskSchedulers` - XML exports that can be imported into Windows Task Scheduler (`Task Scheduler > Import Task...`).

## Prerequisites
- Windows 10/11 with Task Scheduler and PowerShell 5.1 or later.
- The Claude CLI (`claude`) installed and available on your `PATH`.
- Valid MCP server credentials configured for the CLI commands in the scripts.
- The repository cloned at `C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler` (update paths in the examples if your clone lives elsewhere).

## 1. Point the scripts at their new location
Each PowerShell script in `Scripts/` still contains the old `D:\GDrive\...` working-directory reference. Update the `cd` line in each file so the scripts launch from inside this repository. The table below lists the expected replacements when the repo lives at `C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler`.

| Script | Replace the first line with | Claude command |
| --- | --- | --- |
| `Scripts/Agent1/run_claude_connect_mcp.ps1` | `cd "C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent1"` | `claude --dangerously-skip-permissions "/mcp"` |
| `Scripts/Agent1/run_claude.ps1` | `cd "C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent1"` | `claude --dangerously-skip-permissions "Work on the task 'Investment Strategy Insights'..."` |
| `Scripts/Agent1/run_claude_2.ps1` | `cd "C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent1"` | `claude --dangerously-skip-permissions "Work on the task 'Earnings & Corporate Events'..."` |
| `Scripts/Agent2/run_claude_connect_mcp.ps1` | `cd "C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent2"` | `claude --dangerously-skip-permissions "/mcp"` |
| `Scripts/Agent2/run_claude.ps1` | `cd "C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent2"` | `claude --dangerously-skip-permissions "Work on the task 'Stock exchange Analysis'..."` |
| `Scripts/Agent2/run_claude_2.ps1` | `cd "C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent2"` | `claude --dangerously-skip-permissions "Work on the task 'Global Market Developments'..."` |
| `Scripts/Agent2/run_claude_3.ps1` | `cd "C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent2"` | `claude --dangerously-skip-permissions "Work on the task 'Market Sentiment Score'..."` |

> Tip: instead of hard-coding the path you can replace the `cd` line with `Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)` so the script always runs from its own folder, no matter where the repository is cloned.

## 2. Import the MCP connection tasks
1. Open **Task Scheduler** and choose **Action > Import Task...**.
2. Select `TaskSchedulers/ClaudeCode_ConnectToMCPServers_3.xml`.
3. After the task loads, go to the **Actions** tab, select the single action and click **Edit...**.
   - Set **Program/script** to `powershell.exe` (already populated).
   - Set **Add arguments** to `-ExecutionPolicy Bypass -File "C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent2\run_claude_connect_mcp.ps1"`.
   - Set **Start in (optional)** to `C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent2` so the script starts in the directory that contains any agent assets.
4. Review the **Triggers** tab. The exported task starts daily at 10:55 AM. Change the schedule or add additional triggers if you need the connection refreshed more frequently.
5. Save the task. Use **Run** once to verify that a Claude CLI window opens and connects to your MCP server without prompting for input.

Repeat the same process for the other XML exports if you want the connection refreshed multiple times per day. The default start times are staggered hourly so that the CLI reconnects from 6:55 AM through 10:55 AM.

### Daily MCP connection rotation
| Task XML | Default local time | Updated script path |
| --- | --- | --- |
| `ClaudeCode_ConnectToMCPServers.xml` | 06:55 | `C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent2\run_claude_connect_mcp.ps1` |
| `ClaudeCode_ConnectToMCPServers_Agent1.xml` | 07:55 | `C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent1\run_claude_connect_mcp.ps1` |
| `ClaudeCode_ConnectToMCPServers_2.xml` | 08:55 | `C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent2\run_claude_connect_mcp.ps1` |
| `ClaudeCode_ConnectToMCPServers_Agent1_2.xml` | 09:55 | `C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent1\run_claude_connect_mcp.ps1` |
| `ClaudeCode_ConnectToMCPServers_3.xml` | 10:55 | `C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent2\run_claude_connect_mcp.ps1` |

Importing all five tasks delivers a rolling set of reconnections that keep the MCP sessions warm throughout the morning. Adjust the triggers or consolidate tasks if you prefer a different cadence.

## 3. Financial advisor workloads (optional)
The remaining XML exports run specific Claude prompts aimed at financial-advisor workflows. Update their action paths the same way: point them to the scripts inside this repository, and then import them if you want the daily research tasks scheduled automatically.

| Task XML | Default local time | Script to target |
| --- | --- | --- |
| `ClaudeCode_FinancialAdvisors_StockMarketAnalysis.xml` | 07:00 | `Scripts\Agent2\run_claude.ps1` |
| `ClaudeCode_FinancialAdvisors_InvestmentStrategyInsights.xml` | 08:00 | `Scripts\Agent1\run_claude.ps1` |
| `ClaudeCode_FinancialAdvisors_GlobalMarketDevelopments.xml` | 09:00 | `Scripts\Agent2\run_claude_2.ps1` |
| `ClaudeCode_FinancialAdvisors_Earnings&CorporateEvents.xml` | 10:00 | `Scripts\Agent1\run_claude_2.ps1` |
| `ClaudeCode_FinancialAdvisors_MarketSentimentScore.xml` | 11:00 | `Scripts\Agent2\run_claude_3.ps1` |

After importing a task, edit the **Actions** entry so the full path reads, for example:
```
-ExecutionPolicy Bypass -File "C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler\Scripts\Agent2\run_claude_3.ps1"
```
and set **Start in** to the script directory. This ensures Claude runs with the correct working directory and prompt context.

## 4. Test and monitor
- Use **Task Scheduler > Run** on each imported task to confirm it launches without errors. Watch for any PowerShell console output and resolve missing-module or authentication prompts before leaving the task unattended.
- Check **Task Scheduler > History** (enable it if necessary) for success/failure events. Failures with code `0x1` typically mean the script path is wrong.
- When updating prompts or MCP targets, edit only the quoted Claude command inside the `.ps1` script—no changes to the Task XML are required.

## 5. Keeping the repo under version control
Initialize a Git repository in this folder (if you have not already) so that updates to the schedules or scripts remain traceable:
```
cd C:\Users\mikes\OneDrive\Documents\Projects\Paxai\Repo\WinTaskScheduler
git init
git add README.md Scripts TaskSchedulers
git commit -m "Document ClaudeCode Task Scheduler setup"
```
Push to your remote of choice once you are satisfied with the configuration. Future updates to the Task Scheduler XML or PowerShell scripts can then be reviewed and versioned alongside this guide.

With the scripts pointing at their new home and the XML tasks imported, ClaudeCode will reconnect to your MCP server on the schedule you define, keeping your agents responsive throughout the day.
