# Inference Examples Reference

## Two Modes: OpenAI vs Native

| Mode | When to Use | Input Format |
|------|-------------|--------------|
| **OpenAI Mode** | LLMs with `openai_transport` method | Same as `client.chat.completions.create()` |
| **Native Mode** | Standard models with `predict` | Use param names from method signature |

## OpenAI Mode Examples

Models with `openai_transport` accept standard OpenAI chat completion format.

### Text Only

```python
from clarifai.client import Model
import json

model = Model(url="https://clarifai.com/anthropic/completion/models/claude-sonnet-4")

# Using openai_transport directly
response = model.openai_transport(msg=json.dumps({
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is AI?"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
}))
print(response)
```

### With Image (Multimodal)

```python
response = model.openai_transport(msg=json.dumps({
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "What is in this image?"},
            {"type": "image_url", "image_url": {"url": "https://samples.clarifai.com/metro-north.jpg"}}
        ]
    }]
}))
```

### Streaming

```python
# For streaming, use openai_stream_transport
for chunk in model.openai_stream_transport(msg=json.dumps({
    "messages": [{"role": "user", "content": "Write a short poem"}]
})):
    print(chunk, end="")
```

## Native Mode Examples

Models with `predict`/`generate` use parameter names from method signature.

### Text Model

```python
from clarifai.client import Model

model = Model(url="https://clarifai.com/anthropic/completion/models/claude-sonnet-4")

# Check signature first
sig = model.method_signature("predict")
print(sig)  # Shows: def predict(prompt: str, ...) -> str

# Call with signature params
result = model.predict(prompt="Hello, how are you?")
print(result)
```

### Vision Model with Image URL

```python
from clarifai.client import Model
from clarifai.runners.utils.data_types import Image

model = Model(url="https://clarifai.com/openai/chat-completion/models/gpt-4-vision")
result = model.predict(
    prompt="Describe this image in detail",
    image=Image(url="https://samples.clarifai.com/metro-north.jpg")
)
print(result)
```

### Vision Model with Local Image

```python
from clarifai.client import Model
from clarifai.runners.utils.data_types import Image

model = Model(url="https://clarifai.com/clarifai/main/models/general-image-recognition")

# Load image from file
with open("/path/to/image.jpg", "rb") as f:
    image_bytes = f.read()

result = model.predict(image=Image(bytes=image_bytes))
print(result)
```

### Embedding Model

```python
from clarifai.client import Model

model = Model(url="https://clarifai.com/openai/embed/models/text-embedding-3-large")
embedding = model.predict(text="Hello world")
print(f"Embedding dimension: {len(embedding)}")
```

### Audio Model

```python
from clarifai.client import Model
from clarifai.runners.utils.data_types import Audio

model = Model(url="https://clarifai.com/openai/generate/models/whisper-large-v3")
result = model.predict(audio=Audio(url="https://example.com/audio.mp3"))
print(result)
```

## OpenAI-Compatible API

Use standard OpenAI client with Clarifai as backend.

### Setup

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.clarifai.com/v2/ext/openai/v1",
    api_key=os.environ["CLARIFAI_PAT"],
)
```

### Basic Chat

```python
response = client.chat.completions.create(
    model="https://clarifai.com/anthropic/completion/models/claude-sonnet-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
    temperature=0.7,
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

### Vision with OpenAI Client

```python
response = client.chat.completions.create(
    model="https://clarifai.com/openai/chat-completion/models/gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {"type": "image_url", "image_url": {"url": "https://samples.clarifai.com/metro-north.jpg"}}
        ]
    }],
)
print(response.choices[0].message.content)
```

## Complete Inference Workflow

```python
import os
import json
from clarifai.client import Model
from clarifai.runners.utils.data_types import Image, Audio, Video, Text
from clarifai_grpc.grpc.api import resources_pb2

def select_method(methods, user_method=None, streaming=False):
    """Select best method based on priority."""
    s = set(methods)
    if user_method:
        return (user_method, "user") if user_method in s else (None, f"'{user_method}' not found")
    if streaming:
        if "openai_stream_transport" in s: return "openai_stream_transport", "streaming"
        if "generate" in s: return "generate", "streaming"
        return None, "no streaming method"
    if "openai_transport" in s: return "openai_transport", "openai"
    if "predict" in s: return "predict", "default"
    return (methods[0], "fallback") if methods else (None, "no methods")

def convert_media(value, media_class):
    """Convert URL or path to media object."""
    if value.startswith(("http://", "https://")):
        return media_class(url=value)
    elif os.path.isfile(value):
        with open(value, "rb") as f:
            return media_class(bytes=f.read())
    return media_class(url=value)

def prepare_inputs(inputs, signature):
    """Convert inputs based on signature types."""
    if not signature:
        return inputs
    type_map = {f.name: f.type for f in signature.input_fields}
    result = {}
    for k, v in inputs.items():
        t = type_map.get(k)
        if not isinstance(v, str):
            result[k] = v
        elif t == resources_pb2.ModelTypeField.DataType.IMAGE:
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

def run_inference(model_url, inputs, method_name=None, streaming=False):
    """Execute inference with automatic method selection."""
    model = Model(url=model_url)
    model.client.fetch()
    sigs = model.client._method_signatures
    methods = list(sigs.keys())

    selected, reason = select_method(methods, method_name, streaming)
    if not selected:
        raise ValueError(f"{reason}. Available: {methods}")

    func = getattr(model, selected)

    if selected in ("openai_transport", "openai_stream_transport"):
        resp = func(msg=json.dumps(inputs))
    else:
        sig = sigs.get(selected)
        processed = prepare_inputs(inputs, sig)
        resp = func(**processed)

    # Handle streaming
    sig = sigs.get(selected)
    if sig and sig.method_type in (
        resources_pb2.RunnerMethodType.UNARY_STREAMING,
        resources_pb2.RunnerMethodType.STREAMING_STREAMING,
    ):
        resp = "".join(str(c) for c in resp)

    return resp

# Examples
# --------

# LLM with OpenAI format
result = run_inference(
    "https://clarifai.com/anthropic/completion/models/claude-sonnet-4",
    {"messages": [{"role": "user", "content": "Hello!"}]}
)

# Vision model with native predict
result = run_inference(
    "https://clarifai.com/clarifai/main/models/general-image-recognition",
    {"image": "https://samples.clarifai.com/metro-north.jpg"},
    method_name="predict"
)

# Streaming
result = run_inference(
    "https://clarifai.com/anthropic/completion/models/claude-sonnet-4",
    {"messages": [{"role": "user", "content": "Write a poem"}]},
    streaming=True
)
```
