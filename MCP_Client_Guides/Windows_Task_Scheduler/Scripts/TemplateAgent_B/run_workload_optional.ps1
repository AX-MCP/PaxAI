Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Template (OPTIONAL task): update the placeholders below before scheduling.
$taskName = "<OPTIONAL_TASK_NAME>"
$mcpServer = "<OPTIONAL_MCP_SERVER>"
$taskInstructions = "<OPTIONAL_TASK_INSTRUCTIONS>"

$prompt = "Work on the task '$taskName' in your current workspace using the $mcpServer MCP server. $taskInstructions"
claude --dangerously-skip-permissions $prompt

# Optional or ad-hoc workload. Remove if not required.
