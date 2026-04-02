# Model Discovery Reference

## URL Validation

```python
import re

def validate_model_url(url: str) -> bool:
    """Validate Clarifai model URL format."""
    pattern = r"https://clarifai\.com/[^/]+/[^/]+/models/[^/]+"
    return bool(re.match(pattern, url))

# Examples
validate_model_url("https://clarifai.com/anthropic/completion/models/claude-sonnet-4")  # True
validate_model_url("https://example.com/model")  # False
```

## Model URL Format

```
https://clarifai.com/{user_id}/{app_id}/models/{model_id}
```

Examples:
- `https://clarifai.com/anthropic/completion/models/claude-sonnet-4`
- `https://clarifai.com/openai/chat-completion/models/gpt-4o`
- `https://clarifai.com/meta/Llama-3/models/llama-3_1-70b-instruct`
- `https://clarifai.com/clarifai/main/models/general-image-recognition`

## SDK Methods

### available_methods()

List all methods available on a model:

```python
from clarifai.client import Model

model = Model(url="https://clarifai.com/anthropic/completion/models/claude-sonnet-4")
methods = model.available_methods()
print(methods)  # ['predict', 'generate', 'openai_transport', 'openai_stream_transport']
```

### method_signature()

Get the signature of a specific method:

```python
signature = model.method_signature(method_name="predict")
print(signature)
# def predict(prompt: str, max_tokens: int = 4096, ...) -> str:
```

### generate_client_script()

Generate complete working code:

```python
code = model.generate_client_script()
print(code)
# Prints complete Python script with:
# - Imports
# - Model initialization
# - Example calls for each method
# - Output handling
```

## gRPC Model Listing

> **Note:** If filtering featured models to LLMs client-side, check for both `text-to-text` and `multimodal-to-text` model types. Most modern LLMs (e.g. those with vision support) use `multimodal-to-text`.

```python
import os
from clarifai.client import Model
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

PAT = os.environ["CLARIFAI_PAT"]

def list_featured_models(max_models=10):
    """List featured models with methods and OpenAI compatibility."""
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (("authorization", f"Key {PAT}"),)

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
        except:
            methods = []
            has_openai = False

        results.append({
            "id": m.id,
            "url": model_url,
            "methods": [x for x in methods if "transport" not in x],
            "openai_compatible": has_openai,
        })
    return results

# Usage
for m in list_featured_models():
    tag = " [OpenAI]" if m["openai_compatible"] else ""
    print(f"{m['id']}: {m['url']}")
    print(f"  Methods: {', '.join(m['methods'])}{tag}\n")
```

## Method Selection Logic

Priority order for automatic method selection:

1. **User specifies method** → use that method
2. **Streaming requested**:
   - `openai_stream_transport` if available
   - `generate` if available
   - Error if no streaming method
3. **`openai_transport` available** → use it (default for LLMs)
4. **`predict` available** → use it (default for standard models)
5. **Fallback** → first available method

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

## Input Type Conversion

### Type Map

| Signature Type | Input | Converted To |
|----------------|-------|--------------|
| `IMAGE` | URL string | `Image(url=...)` |
| `IMAGE` | File path | `Image(bytes=...)` |
| `AUDIO` | URL string | `Audio(url=...)` |
| `AUDIO` | File path | `Audio(bytes=...)` |
| `VIDEO` | URL string | `Video(url=...)` |
| `VIDEO` | File path | `Video(bytes=...)` |
| `TEXT` | String | `Text(...)` |

### Conversion Utility

```python
import os
from clarifai.runners.utils.data_types import Image, Audio, Video, Text
from clarifai_grpc.grpc.api import resources_pb2

def convert_media(value: str, media_class):
    """Convert URL or file path to media object."""
    if value.startswith(("http://", "https://")):
        return media_class(url=value)
    elif os.path.isfile(value):
        with open(value, "rb") as f:
            return media_class(bytes=f.read())
    return media_class(url=value)  # Fallback

def prepare_inputs(inputs: dict, signature) -> dict:
    """Convert inputs based on method signature types."""
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
```
