Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Template (PRIMARY task): update the placeholders below before scheduling.
$taskName = "<PRIMARY_TASK_NAME>"
$mcpServer = "<PRIMARY_MCP_SERVER>"
$taskInstructions = "<PRIMARY_TASK_INSTRUCTIONS>"

$prompt = "Work on the task '$taskName' in your current workspace using the $mcpServer MCP server. $taskInstructions"
claude --dangerously-skip-permissions $prompt

# Core recurring workload for this agent.
