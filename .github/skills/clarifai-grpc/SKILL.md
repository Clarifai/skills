````skill
---
name: clarifai-grpc
description: Direct API interaction using Clarifai's gRPC client and protobufs. Use when high-level SDK methods are ambiguous, when handling complex multi-modal inputs, or for specific platform operations like log retrieval. Standardizes on using ClarifaiAuthHelper, resources_pb2, and service_pb2.
---

# Clarifai gRPC API Integration

Interact directly with the Clarifai platform using the low-level gRPC interface. This approach is preferred for complex multi-modal requests or whenever the SDK's high-level wrappers obscure required field mappings.

## Core Imports & Setup

Always use `ClarifaiAuthHelper` to manage authentication metadata.

```python
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, status_code_pb2
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel

# Initialize authentication and channel
auth = ClarifaiAuthHelper.from_env() # Uses CLARIFAI_PAT
metadata = auth.metadata
stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
```

## API Definition Files

All information for the entire Clarifai API is contained in these three core protobuf files. When in doubt about request fields, response structures, or status codes, refer directly to these files:

*   **`service_pb2`**: Contains all **Service Requests and Responses** (e.g., `PostModelOutputsRequest`, `ListLogEntriesResponse`). This defines the actions you can take.
*   **`resources_pb2`**: Contains all **Data Resources** (e.g., `Input`, `Data`, `Audio`, `Model`, `UserAppIDSet`). This defines the objects the API works with.
*   **`status_code_pb2`**: Contains all **Status Codes** for error handling (e.g., `SUCCESS`, `MODEL_DEPLOYMENT_FAILED`).

## Example Platform Operations

### 1. Model Inference (PostModelOutputs)

Used for executing predictions on models.

```python
request = service_pb2.PostModelOutputsRequest(
    user_app_id=auth.user_app_id,  # Helper provides user_id/app_id
    model_id="model-id",
    version_id="version-id",       # Optional but recommended
    inputs=[input_proto]
)

response = stub.PostModelOutputs(request, metadata=metadata)

if response.status.code != status_code_pb2.SUCCESS:
    raise Exception(f"Request failed: {response.status.description}")

# Accessing output audio/text/image
output_bytes = response.outputs[0].data.audio.base64
```

### 2. Fetching Logs (ListLogEntries)

Essential for debugging Runners and Builders.

```python
request = service_pb2.ListLogEntriesRequest(
    user_app_id=auth.user_app_id,
    model_id="model-id",
    version_id="version-id",
    log_type="runner", # Options: runner, builder, runner.events
    per_page=50
)

response = stub.ListLogEntries(request, metadata=metadata)
for entry in response.log_entries:
    print(f"[{entry.log_type}] {entry.message}")
```

## Data Type Reference

| Type | Resource Field | Value Field |
|------|----------------|-------------|
| Text | `text` | `raw` (string) |
| Image | `image` | `url` or `base64` (bytes) |
| Audio | `audio` | `url` or `base64` (bytes) |
| Video | `video` | `url` or `base64` (bytes) |
| Metadata | `metadata` | `struct` (google.protobuf.Struct) |

## Best Practices

1.  **Check Status Codes**: Always verify `response.status.code == status_code_pb2.SUCCESS` before processing data.
2. **Print full response**: Always print out the full response when debugging to understand the structure and available fields and debugging information.
3.  **Use UserAppIDSet**: Use `auth.user_app_id` to automatically fill in the `user_id` and `app_id` fields required in almost every request.
4.  **Metadata vs Raw Bytes**: When sending files, prefer `url` for platform-hosted assets and `base64` (passing raw bytes) for local files.
5.  **Version Specificity**: When calling `PostModelOutputs`, always provide a `version_id` to ensure consistency if the model is updated.
````
