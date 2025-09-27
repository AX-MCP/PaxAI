Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Template (SECONDARY task): update the placeholders below before scheduling.
$taskName = "<SECONDARY_TASK_NAME>"
$mcpServer = "<SECONDARY_MCP_SERVER>"
$taskInstructions = "<SECONDARY_TASK_INSTRUCTIONS>"

$prompt = "Work on the task '$taskName' in your current workspace using the $mcpServer MCP server. $taskInstructions"
claude --dangerously-skip-permissions $prompt

# Secondary workload slot; duplicate or rename as needed for extra runs.
