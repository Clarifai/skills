---
name: clarifai-inference
description: Discover model capabilities and generate inference code. Use when the user wants to list available models, inspect model methods and signatures, generate working inference code, or use Clarifai's OpenAI-compatible API. Covers model discovery, code generation, featured model URLs, method selection, and media input handling.
---

# Model Discovery & Inference

> **IMPORTANT:** For SDK methods and CLI commands and code generation, first scan [../clarifai-cli/references/sdk-cli-reference.md](../clarifai-cli/references/sdk-cli-reference.md)

Discover model capabilities and generate working inference code automatically. Clarifai supports both standard API calls and a high-level "Pythonic" interface for custom model methods.

## Pythonic Inference (Custom Methods)

Models implemented using `ModelClass` (from `clarifai-model-upload`) expose their methods directly on the `Model` object. This provides a natural Python experience with IDE autocompletion and type checking.

### Calling Custom Methods

If a model defines a method in its `runner/model.py`, you can call it directly:

```python
from clarifai.client import Model
from clarifai.runners.utils.data_types import Audio

model = Model(url="https://clarifai.com/resemble-ai/completion/models/chatterbox-turbo")

# Call a custom method 'generate' with keyword arguments
# Inputs like URLs are automatically converted to high-level types
result = model.generate(
    text="Hello, how can I help you today?",
    voice_prompt="https://samples.com/voice.wav"
)

# Multi-modal outputs (like Audio) are returned as high-level objects
print(f"Generated audio URL: {result.url}")
```

### Streaming Custom Methods

If a method is a generator in the runner, it returns an iterator on the client:

```python
# Stream results (e.g., for TTS or LLMs)
for chunk in model.generate(text="A long story about..."):
    # chunk is an Audio object or similar
    chunk.play()  # If it supports playback
```

## Key SDK Discovery Methods

```python
from clarifai.client import Model

# Initialize model
model = Model(url="https://clarifai.com/anthropic/completion/models/claude-sonnet-4_5")

# 1. List available methods
methods = model.available_methods()
# Returns: ['predict', 'generate', 'openai_transport'] (example)

# 2. Get method signature
signature = model.method_signature(method_name="predict")
# Returns: "def predict(prompt: str, ...) -> str:"

# 3. Generate complete working code
client_script = model.generate_client_script()
# Returns: Complete Python script with imports and examples
print(client_script)
```

## Method Selection Priority

When a model has multiple methods, use this priority to select the best one:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    METHOD SELECTION PRIORITY                         │
├─────────────────────────────────────────────────────────────────────┤
│ 1. User specifies method_name → use that method                      │
│                                                                      │
│ 2. User requests streaming:                                          │
│    - openai_stream_transport (if available)                          │
│    - generate (if available)                                         │
│    - Error if no streaming method                                    │
│                                                                      │
│ 3. Model has openai_transport → use it (default for LLMs)            │
│                                                                      │
│ 4. Model has predict → use it (default for standard models)          │
│                                                                      │
│ 5. Fallback to first available method                                │
└─────────────────────────────────────────────────────────────────────┘
```

### Method Selection Utility

```python
def select_method(methods: list, user_method: str = None, streaming: bool = False) -> tuple:
    """
    Select best method based on priority.
    Returns: (method_name, reason) or (None, error_message)
    """
    s = set(methods)
    if user_method:
        return (user_method, "user specified") if user_method in s else (None, f"'{user_method}' not found")
    if streaming:
        if "openai_stream_transport" in s:
            return "openai_stream_transport", "streaming"
        if "generate" in s:
            return "generate", "streaming"
        return None, "no streaming method"
    if "openai_transport" in s:
        return "openai_transport", "openai"
    if "predict" in s:
        return "predict", "default"
    return (methods[0], "fallback") if methods else (None, "no methods")
```

## Media Input Handling

Clarifai models accept various input types. Use these utilities to convert URLs/paths to proper types.

### Input Type Conversion Table

| Input Type | What You Provide | Auto-Conversion |
|------------|-----------------|-----------------|
| Text | `"prompt": "Hello"` | Passed directly |
| Image URL | `"image": "https://..."` | → `Image(url=...)` |
| Image path | `"image": "/path/to/file.jpg"` | → `Image(bytes=...)` |
| Audio URL | `"audio": "https://..."` | → `Audio(url=...)` |
| Audio path | `"audio": "/path/to/file.mp3"` | → `Audio(bytes=...)` |
| Video URL | `"video": "https://..."` | → `Video(url=...)` |
| Video path | `"video": "/path/to/file.mp4"` | → `Video(bytes=...)` |

### Media Conversion Utilities

```python
import os
from clarifai.runners.utils.data_types import Image, Audio, Video, Text
from clarifai_grpc.grpc.api import resources_pb2

def convert_media(value: str, media_class):
    """Convert URL or file path to media object (Image, Audio, Video)."""
    if value.startswith(("http://", "https://")):
        return media_class(url=value)
    elif os.path.isfile(value):
        with open(value, "rb") as f:
            return media_class(bytes=f.read())
    return media_class(url=value)  # Fallback: treat as URL

def prepare_inputs(inputs: dict, signature) -> dict:
    """Convert string values to proper types based on method signature."""
    if not signature:
        return inputs

    type_map = {f.name: f.type for f in signature.input_fields}
    result = {}

    for k, v in inputs.items():
        t = type_map.get(k)
        if not isinstance(v, str):
            result[k] = v
            continue

        # Convert based on signature type
        if t == resources_pb2.ModelTypeField.DataType.IMAGE:
            result[k] = convert_media(v, Image)
        elif t == resources_pb2.ModelTypeField.DataType.AUDIO:
            result[k] = convert_media(v, Audio)
        elif t == resources_pb2.ModelTypeField.DataType.VIDEO:
            result[k] = convert_media(v, Video)
        elif t == resources_pb2.ModelTypeField.DataType.TEXT:
            result[k] = Text(v)
        else:
            result[k] = v
    return result
```

## Model Discovery Workflow

### Step 1: List Featured Models

```python
import os
from clarifai.client import Model
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

API_KEY = os.getenv("CLARIFAI_PAT")

def list_featured_models(max_models=10):
    """List featured models with method info and OpenAI compatibility."""
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (("authorization", f"Key {API_KEY}"),)

    request = service_pb2.ListModelsRequest(
        per_page=max_models,
        featured_only=True
    )
    response = stub.ListModels(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        raise Exception(f"Error: {response.status.description}")

    results = []
    for m in response.models:
        model_url = f"https://clarifai.com/{m.user_id}/{m.app_id}/models/{m.id}"
        try:
            model = Model(url=model_url)
            methods = list(model.available_methods())
            has_openai = "openai_transport" in methods
            # Filter out transport methods for display
            display_methods = [x for x in methods if "transport" not in x]
        except:
            methods = []
            has_openai = False
            display_methods = ["(unavailable)"]

        results.append({
            "id": m.id,
            "url": model_url,
            "methods": display_methods,
            "openai_compatible": has_openai,
        })
    return results

# Usage
models = list_featured_models()
for m in models:
    openai_tag = " [OpenAI]" if m["openai_compatible"] else ""
    print(f"{m['id']}: {m['url']}")
    print(f"  Methods: {', '.join(m['methods'])}{openai_tag}")
```

### Step 2: Inspect Model Capabilities

```python
from clarifai.client import Model

def discover_model(model_url):
    """Discover available methods and signatures."""
    model = Model(url=model_url)

    # Get available methods
    methods = model.available_methods()
    print(f"Available methods: {list(methods)}")

    # Get each method's signature
    for method_name in methods:
        signature = model.method_signature(method_name=method_name)
        print(f"\n{method_name}:\n  {signature}")

# Usage
discover_model("https://clarifai.com/anthropic/completion/models/claude-sonnet-4_5")
```

### Step 3: Generate Inference Code

```python
def generate_inference_code(model_url):
    """Generate complete working code."""
    model = Model(url=model_url)
    client_script = model.generate_client_script()

    print("Generated code:")
    print("=" * 80)
    print(client_script)
    print("=" * 80)

    return client_script

# Usage
code = generate_inference_code("https://clarifai.com/anthropic/completion/models/claude-sonnet-4_5")
```

## Verified Model URLs

### LLMs

| Model | URL |
|-------|-----|
| Claude Sonnet 4 | `https://clarifai.com/anthropic/completion/models/claude-sonnet-4` |
| Claude Opus 4 | `https://clarifai.com/anthropic/completion/models/claude-opus-4` |
| GPT-4o | `https://clarifai.com/openai/chat-completion/models/gpt-4o` |
| GPT-4o Mini | `https://clarifai.com/openai/chat-completion/models/gpt-4o-mini` |
| Llama 3.1 70B | `https://clarifai.com/meta/Llama-3/models/llama-3_1-70b-instruct` |
| Llama 3.1 8B | `https://clarifai.com/meta/Llama-3/models/llama-3_1-8b-instruct` |

### Vision Models

| Model | URL |
|-------|-----|
| GPT-4 Vision | `https://clarifai.com/openai/chat-completion/models/gpt-4-vision` |
| Claude Vision | `https://clarifai.com/anthropic/completion/models/claude-sonnet-4` |
| LLaVA | `https://clarifai.com/liuhaotian/llava/models/llava-1_5-7b-hf` |

### Embedding Models

| Model | URL |
|-------|-----|
| text-embedding-3-large | `https://clarifai.com/openai/embed/models/text-embedding-3-large` |
| text-embedding-ada-002 | `https://clarifai.com/openai/embed/models/text-embedding-ada-002` |

## OpenAI-Compatible API

### Basic Usage

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.clarifai.com/v2/ext/openai/v1",
    api_key=os.environ['CLARIFAI_PAT'],
)

response = client.chat.completions.create(
    model="https://clarifai.com/anthropic/completion/models/claude-sonnet-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
    temperature=1.0,
)
print(response.choices[0].message.content)
```

### Streaming

```python
response = client.chat.completions.create(
    model="https://clarifai.com/anthropic/completion/models/claude-sonnet-4",
    messages=[{"role": "user", "content": "Tell me a story."}],
    stream=True,
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### With MCP Servers

```python
response = client.chat.completions.create(
    model="https://clarifai.com/anthropic/completion/models/claude-sonnet-4",
    messages=[{"role": "user", "content": "What is 25 * 17?"}],
    extra_body={
        "mcp_servers": [
            "https://clarifai.com/user/app/models/math-server"
        ]
    },
    stream=True,  # REQUIRED for MCP
)
```

### With Deployment

```python
from clarifai.client import Model

model = Model(
    url="https://clarifai.com/user/app/models/my-model",
    deployment_id="my-deployment"
)
result = model.predict(prompt="Hello")
```

## Direct SDK Inference

### Two Modes: OpenAI vs Native

Models on Clarifai support two inference modes:

| Mode | When to Use | Input Format |
|------|-------------|--------------|
| **OpenAI Mode** | LLMs with `openai_transport` | Same as `chat.completions.create()` |
| **Native Mode** | Standard models with `predict` | Use param names from signature |

### Complete Inference Example

```python
import json
from clarifai.client import Model
from clarifai.runners.utils.data_types import Image, Audio, Video, Text
from clarifai_grpc.grpc.api import resources_pb2

def run_inference(model_url: str, inputs: dict, method_name: str = None, streaming: bool = False):
    """
    Execute inference with automatic method selection and type conversion.

    Args:
        model_url: Clarifai model URL
        inputs: Dict with param names as keys
        method_name: Override automatic method selection
        streaming: Use streaming method if available
    """
    model = Model(url=model_url)
    model.client.fetch()
    sigs = model.client._method_signatures
    methods = list(sigs.keys())

    # Select best method
    selected, reason = select_method(methods, method_name, streaming)
    if not selected:
        raise ValueError(f"{reason}. Available: {methods}")

    func = getattr(model, selected)

    # OpenAI transport: pass inputs as JSON string
    if selected in ("openai_transport", "openai_stream_transport"):
        resp = func(msg=json.dumps(inputs))
    else:
        # Native methods: convert types and pass as kwargs
        sig = sigs.get(selected)
        processed = prepare_inputs(inputs, sig)
        resp = func(**processed)

    # Handle streaming response
    sig = sigs.get(selected)
    if sig and sig.method_type in (
        resources_pb2.RunnerMethodType.UNARY_STREAMING,
        resources_pb2.RunnerMethodType.STREAMING_STREAMING,
    ):
        resp = "".join(str(c) for c in resp)

    return resp

# Usage Examples
# --------------

# 1. Text LLM (auto-selects openai_transport)
result = run_inference(
    model_url="https://clarifai.com/anthropic/completion/models/claude-sonnet-4",
    inputs={"messages": [{"role": "user", "content": "What is AI?"}]}
)

# 2. Text LLM with streaming
result = run_inference(
    model_url="https://clarifai.com/anthropic/completion/models/claude-sonnet-4",
    inputs={"messages": [{"role": "user", "content": "Write a poem"}]},
    streaming=True
)

# 3. Vision model (multimodal via OpenAI format)
result = run_inference(
    model_url="https://clarifai.com/openai/chat-completion/models/gpt-4o",
    inputs={
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this image?"},
                {"type": "image_url", "image_url": {"url": "https://samples.clarifai.com/metro-north.jpg"}}
            ]
        }]
    }
)

# 4. Native predict method (override auto-selection)
result = run_inference(
    model_url="https://clarifai.com/clarifai/main/models/general-image-recognition",
    inputs={"image": "https://samples.clarifai.com/metro-north.jpg"},
    method_name="predict"
)
```

### Text Model (Simple)

```python
from clarifai.client import Model

model = Model(url="https://clarifai.com/anthropic/completion/models/claude-sonnet-4")
result = model.predict(prompt="Hello, how are you?")
print(result)
```

### Vision Model (Simple)

```python
from clarifai.client import Model
from clarifai.runners.utils.data_types import Image

model = Model(url="https://clarifai.com/openai/chat-completion/models/gpt-4-vision")
result = model.predict(
    prompt="What's in this image?",
    image=Image(url="https://samples.clarifai.com/metro-north.jpg")
)
print(result)
```

### Embedding Model

```python
from clarifai.client import Model

model = Model(url="https://clarifai.com/openai/embed/models/text-embedding-3-large")
embedding = model.predict(text="Hello world")
print(f"Embedding dimension: {len(embedding)}")
```

## CLI for Inference

```bash
# Simple text prediction (positional args)
clarifai model predict anthropic/completion/models/claude-sonnet-4 "Hello!"

# Named parameters
clarifai model predict --model-url <url> -i prompt="Hello" -i max_tokens=100

# OpenAI chat format
clarifai model predict --model-url <url> --chat "What is AI?"

# Image file input
clarifai model predict --model-url <url> --file ./image.jpg

# Show model info (methods + signatures)
clarifai model predict --model-url <url> --info

# JSON inputs (legacy format, still supported)
clarifai model predict --model-url <url> --inputs '{"prompt": "Hello!"}'

# With specific deployment
clarifai model predict --model-url <url> --deployment my-deployment -i prompt="Hello"

# Pipe from stdin
echo "Explain quantum computing" | clarifai model predict --model-url <url>
```

## Agentic Models (LLM + MCP Tool Calling)

Clarifai supports agentic models that combine LLMs with MCP tool-calling via the `AgenticModelClass`. These models automatically discover and call tools from MCP servers during inference.

### Using Agentic Models via OpenAI API

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://api.clarifai.com/v2/ext/openai/v1",
    api_key=os.environ['CLARIFAI_PAT'],
)

# Agentic inference: LLM + MCP tools
response = client.chat.completions.create(
    model="https://clarifai.com/anthropic/completion/models/claude-sonnet-4",
    messages=[{"role": "user", "content": "Search GitHub for the latest Clarifai Python SDK release"}],
    extra_body={
        "mcp_servers": [
            "https://clarifai.com/user/app/models/github-mcp-server"
        ]
    },
    stream=True,  # REQUIRED for MCP tool calling
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Connection Pool Tuning

Agentic models maintain persistent MCP connections for performance. Tune via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `CLARIFAI_MCP_CONNECT_TIMEOUT` | 30s | Connection establishment timeout |
| `CLARIFAI_MCP_TOOL_CALL_TIMEOUT` | 60s | Tool execution timeout |
| `CLARIFAI_MCP_VERIFY_IDLE_THRESHOLD` | 2min | Re-verify connections after idle |
| `CLARIFAI_MCP_MAX_IDLE_TIME` | 15min | Remove stale connections |

### Building Custom Agentic Models

```python
from clarifai.runners.models.agentic_class import AgenticModelClass
from openai import OpenAI

class MyAgenticModel(AgenticModelClass):
    def load_model(self):
        self.client = OpenAI(
            base_url="http://localhost:8080/v1",
            api_key="local-key"
        )
        self.model = "my-local-llm"
```

The `AgenticModelClass` extends `OpenAIModelClass` with:
- Persistent MCP connection pool (thread-safe singleton)
- Automatic tool discovery and caching
- Iterative tool calling (LLM calls tools, gets results, calls more tools)
- Token tracking including reasoning models (o1, o3)

## Extended Search

For more model information:
- **Model catalog**: https://clarifai.com/explore/models
- **API docs**: https://docs.clarifai.com/api/
- **SDK reference**: https://github.com/Clarifai/clarifai-python

## References

- Model discovery & utilities: [references/model-discovery.md](references/model-discovery.md)
- Inference examples: [references/inference-examples.md](references/inference-examples.md)
