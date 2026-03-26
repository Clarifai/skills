---
name: clarifai-mcp
description: Create MCP (Model Context Protocol) servers on Clarifai. Use when the user wants to create tool-calling servers, implement custom tools for agentic AI workflows, bridge external stdio MCP servers (GitHub, filesystem), or deploy MCP servers for agentic models. Covers MCPModelClass, StdioMCPModelClass, FastMCP, tool definitions, and integration with agentic models.
---

# MCP Server Implementation

> **IMPORTANT:** For SDK methods and CLI commands and code generation, first scan [../clarifai-cli/references/sdk-cli-reference.md](../clarifai-cli/references/sdk-cli-reference.md)

Create MCP (Model Context Protocol) servers for tool-calling capabilities on Clarifai platform.

## Quick Start

### Step 1: Initialize MCP Server

```bash
clarifai model init ./my-mcp-server --toolkit mcp
```

### Step 2: Implement Tools

Edit `1/model.py` to add your tools.

### Step 3: Test Locally

```bash
clarifai model serve ./my-mcp-server
```

### Step 4: Deploy

```bash
# Upload and deploy in one step
clarifai model deploy ./my-mcp-server

# Or upload only (deploy separately later)
clarifai model upload ./my-mcp-server
```

## MCPModelClass Pattern

Tools are defined at **module level** using a `FastMCP` instance, then the class returns it via `get_server()`:

```python
from fastmcp import FastMCP
from clarifai.runners.models.mcp_class import MCPModelClass

# Define tools at module level
server = FastMCP("my-server", instructions="My MCP server.", stateless_http=True)

@server.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@server.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

class MyMCPServer(MCPModelClass):
    """MCP server with custom tools."""

    def get_server(self) -> FastMCP:
        """Return the FastMCP server instance."""
        return server
```

**CRITICAL:** Do NOT put tool registration in `load_model()`. Define tools at module level, then return the server from `get_server()`.

## Tool Definition Patterns

All tools are defined at **module level** on the `server` instance:

### Simple Tool

```python
@server.tool()
def greet(name: str) -> str:
    """Greet a user by name."""
    return f"Hello, {name}!"
```

### Tool with Multiple Parameters

```python
from pydantic import Field

@server.tool("calculate", description="Perform a calculation")
def calculate(
    operation: str = Field(description="One of: add, subtract, multiply, divide"),
    a: float = Field(description="First number"),
    b: float = Field(description="Second number"),
) -> float:
    """Perform a calculation."""
    ops = {"add": a + b, "subtract": a - b, "multiply": a * b, "divide": a / b if b != 0 else float('inf')}
    return ops.get(operation, 0)
```

### Async Tool

```python
import httpx

@server.tool()
async def fetch_weather(city: str) -> str:
    """Fetch weather for a city."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weather.com/{city}")
        return response.json()
```

### Resource (Read-Only Data)

```python
@server.resource("config://version")
def get_version():
    """Return the server version."""
    return "1.0.0"
```

## Complete MCP Server Example

```python
import math
from fastmcp import FastMCP
from clarifai.runners.models.mcp_class import MCPModelClass

server = FastMCP("math-server", instructions="A math operations server.", stateless_http=True)

@server.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@server.tool()
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

@server.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@server.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@server.tool()
def sqrt(x: float) -> float:
    """Calculate square root of x."""
    if x < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(x)

@server.tool()
def power(base: float, exponent: float) -> float:
    """Calculate base raised to exponent."""
    return math.pow(base, exponent)


class MathMCPServer(MCPModelClass):
    """MCP server with math tools."""

    def get_server(self) -> FastMCP:
        return server
```

## config.yaml for MCP Server

```yaml
model:
  id: "my-mcp-server"
  model_type_id: "mcp"

compute:
  instance: t3a.2xlarge  # CPU-only instance
```

Or with verbose format (if you need explicit resource control):

```yaml
model:
  id: "my-mcp-server"
  user_id: "YOUR_USER_ID"
  app_id: "YOUR_APP_ID"
  model_type_id: "mcp"

build_info:
  python_version: "3.12"

inference_compute_info:
  cpu_limit: "1"
  cpu_memory: "2Gi"
  num_accelerators: 0
```

## requirements.txt for MCP Server

```
clarifai>=12.0.0
fastmcp
```

Add `httpx` only if your tools make HTTP requests.

## Using MCP with Agentic Models

### CRITICAL: Streaming Required

When using MCP servers with agentic models, you **MUST** use `stream=True`:

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://api.clarifai.com/v2/ext/openai/v1",
    api_key=os.environ['CLARIFAI_PAT'],
)

response = client.chat.completions.create(
    model="https://clarifai.com/anthropic/completion/models/claude-sonnet-4",
    messages=[
        {"role": "user", "content": "What is 25 * 17?"},
    ],
    extra_body={
        "mcp_servers": [
            "https://clarifai.com/YOUR_USER/YOUR_APP/models/my-mcp-server"
        ]
    },
    stream=True,  # REQUIRED for MCP
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Multiple MCP Servers

```python
response = client.chat.completions.create(
    model="https://clarifai.com/anthropic/completion/models/claude-sonnet-4",
    messages=[...],
    extra_body={
        "mcp_servers": [
            "https://clarifai.com/user/app/models/math-server",
            "https://clarifai.com/user/app/models/web-search-server",
            "https://clarifai.com/user/app/models/file-server",
        ]
    },
    stream=True,
)
```

## Common MCP Server Types

| Server Type | Tools | Use Case |
|-------------|-------|----------|
| Math | add, subtract, multiply, divide, sqrt | Calculations |
| Web Search | search, fetch_url | Information retrieval |
| File System | read_file, write_file, list_dir | File operations |
| Database | query, insert, update | Data operations |
| API Wrapper | Custom API calls | External service integration |
| Code Execution | run_python, run_bash | Code execution |

## StdioMCPModelClass: Bridge External MCP Servers

Use `StdioMCPModelClass` to wrap existing stdio-based MCP servers (like GitHub, filesystem, or any npx-based server) as Clarifai models. No custom Python code needed - just configure via `config.yaml`.

### How It Works

1. Launches the stdio MCP server as a subprocess
2. Auto-discovers all tools from the server
3. Registers tools with FastMCP for Clarifai compatibility
4. Maintains a single long-lived session per request

### config.yaml for StdioMCPModelClass

**CRITICAL:** The config section must be `mcp_server:` (not `mcp:`).

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
  instance: t3a.2xlarge  # CPU-only instance
```

### Implementation (1/model.py)

```python
from clarifai.runners.models.stdio_mcp_class import StdioMCPModelClass

class MyStdioMCPServer(StdioMCPModelClass):
    """Bridge an external stdio MCP server to Clarifai."""
    pass  # Config is read from config.yaml automatically
```

### Common Stdio MCP Servers

| Server | Command | Args |
|--------|---------|------|
| GitHub | `npx` | `["-y", "@modelcontextprotocol/server-github"]` |
| Filesystem | `npx` | `["-y", "@modelcontextprotocol/server-filesystem", "/path"]` |
| Brave Search | `npx` | `["-y", "@modelcontextprotocol/server-brave-search"]` |
| Google Maps | `npx` | `["-y", "@modelcontextprotocol/server-google-maps"]` |

### Environment Variables as Secrets

For production, use Clarifai secrets instead of hardcoding tokens:

```yaml
mcp_server:
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-github"]
  env:
    GITHUB_PERSONAL_ACCESS_TOKEN: "$SECRET_GITHUB_TOKEN"
```

Then create the secret via CLI or SDK:
```bash
# Via Python SDK
from clarifai.client import User
user = User()
user.create_secrets([{"id": "SECRET_GITHUB_TOKEN", "value": "ghp_..."}])
```

## Testing MCP Servers

### Local Test

```bash
clarifai model serve ./my-mcp-server
```

### With gRPC Server

```bash
clarifai model serve ./my-mcp-server --grpc --port 8000
```

Then test with the OpenAI client pointing to your local model.

## Extended Search

For more MCP examples:
- **MCP examples**: https://github.com/Clarifai/runners-examples/tree/main/mcp
- **FastMCP docs**: https://modelcontextprotocol.io/

## References

- MCP implementation: [references/mcp-implementation.md](references/mcp-implementation.md)
