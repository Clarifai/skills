# MCP Server Implementation Reference

## MCPModelClass Structure

Tools are defined at **module level**, then returned from `get_server()`:

```python
from fastmcp import FastMCP
from clarifai.runners.models.mcp_class import MCPModelClass

# Define tools at module level
server = FastMCP("server-name", instructions="Server description.", stateless_http=True)

@server.tool()
def my_tool(param: str) -> str:
    """Tool description."""
    return f"Result: {param}"

class MyMCPServer(MCPModelClass):
    """MCP server implementation."""

    def get_server(self) -> FastMCP:
        """Return the FastMCP server instance."""
        return server
```

## Tool Registration

### Basic Tool

```python
@server.tool()
def tool_name(param1: str, param2: int = 10) -> str:
    """Tool description for the AI model.

    Args:
        param1: Description of param1
        param2: Description of param2 (optional)

    Returns:
        Description of return value
    """
    return result
```

### Async Tool

```python
@server.tool()
async def async_tool(query: str) -> str:
    """Async tool for I/O operations."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/{query}")
        return response.text
```

### Resource (Read-Only Data)

```python
@server.resource("config://version")
def get_version():
    """Return the server version."""
    return "1.0.0"
```

## StdioMCPModelClass (Bridge External Servers)

For wrapping existing stdio MCP servers (GitHub, filesystem, etc.):

```python
from clarifai.runners.models.stdio_mcp_class import StdioMCPModelClass

class MyStdioServer(StdioMCPModelClass):
    pass  # All config from config.yaml
```

**config.yaml** (note: section is `mcp_server`, not `mcp`):
```yaml
model:
  id: "github-mcp-server"
  model_type_id: "mcp"

mcp_server:
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-github"]
  env:
    GITHUB_PERSONAL_ACCESS_TOKEN: "your-token"

compute:
  instance: t3a.2xlarge
```

## Config.yaml (MCPModelClass)

```yaml
model:
  id: "my-mcp-server"
  model_type_id: "mcp"

compute:
  instance: t3a.2xlarge  # CPU-only instance
```

## Requirements

```
clarifai>=12.0.0
fastmcp
```

## Using with Agentic Models

**IMPORTANT:** Always use `stream=True` when calling models with MCP servers.

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://api.clarifai.com/v2/ext/openai/v1",
    api_key=os.environ['CLARIFAI_PAT'],
)

response = client.chat.completions.create(
    model="https://clarifai.com/anthropic/completion/models/claude-sonnet-4",
    messages=[{"role": "user", "content": "Use the tools to..."}],
    extra_body={
        "mcp_servers": ["https://clarifai.com/user/app/models/my-mcp"]
    },
    stream=True,  # REQUIRED
)
```
