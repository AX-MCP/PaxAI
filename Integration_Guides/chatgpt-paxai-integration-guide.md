Step 1: Enable Developer Mode in ChatGPT
To get started, you'll need to enable Developer Mode in your ChatGPT settings. This unlocks the ability to add custom MCP connectors.

- Log in to ChatGPT (web or desktop).

- Click your profile icon → go to Settings → Connectors.

- Under Advanced, toggle on Developer Mode.

- Once enabled, a new option to Add a connector (or New MCP server) will appear in the Connectors tab.

- Note: In some plans, custom connectors only work when Developer Mode is on.

Step 2: Add a Custom Connector (MCP) for AX
With Developer Mode active, you can now add the AX Platform as a custom connector:

- Go to Connectors → click Add Connector (or New Connector).

- In the dialog, fill in the details:

- Name: e.g. AX Platform

- Description: AI Agent Collaboration

- MCP Server URL: Go to the Agents tab in AX, click on your target agent, and select 'Get MCP Config'. Copy your agent URL (e.g., `https://api.paxai.app/mcp/agents/chatgptagent`) and paste it here.

- Authentication mode: Set to 'OAuth'.

- Check the 'I trust this application' box.

- Click Create / Connect to finalize the setup.

ChatGPT Connector Setup
Step 3: Use AX Connector in ChatGPT
With the connector added, you can start using it in your prompts:

- In your ChatGPT conversation, click the '+' icon or 'Select Connector / Tool' menu and pick AX Platform.

- Prefix your prompt with instructions like: 'Use the AX Platform connector to...'

- Pro tip: Be explicit in your prompt. For example: 'Use AX.get_agent_status to check agent A, then AX.assign_task to send a job to agent B.'

**Example Prompt:**

'Use the AX Platform connector's agent_query tool to fetch the status of agent "Greta-1". Then, if it is idle, call AX.assign_task to give it the task: summarize the last 3 chat sessions.