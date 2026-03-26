---
name: clarifai-model-upload
description: Upload and deploy custom models to Clarifai platform. Use when the user wants to (1) deploy LLMs using toolkits (vLLM, SGLang, Ollama, HuggingFace), (2) convert existing Python models to Clarifai format, (3) create custom model implementations with ModelClass, or (4) configure compute resources. Covers toolkit templates, ModelClass implementation, config.yaml, checkpoints, GPU configuration, and local testing.
---

# Model Upload & Deployment

> **IMPORTANT:** For SDK methods and CLI commands and code generation, first scan [../clarifai-cli/references/sdk-cli-reference.md](../clarifai-cli/references/sdk-cli-reference.md)

Deploy custom models to Clarifai platform using toolkits or custom ModelClass implementations.

## Workflow: How to Help Users Deploy Models

**CRITICAL:** Execute these steps IN ORDER. Complete each step before moving to the next.

### Step 1: Check CLI Init First (ALWAYS TRY THIS FIRST)

**FIRST**, check if a CLI init command can directly generate a working deployment:

| User Request | CLI Command |
|--------------|-------------|
| Deploy HuggingFace model with vLLM | `clarifai model init --toolkit vllm --model-name "<hf-model-id>"` |
| Deploy with SGLang | `clarifai model init --toolkit sglang --model-name "<hf-model-id>"` |
| Deploy HuggingFace transformers | `clarifai model init --toolkit huggingface --model-name "<hf-model-id>"` |
| Deploy Ollama model | `clarifai model init --toolkit ollama --model-name "<model>"` |
| Create MCP server | `clarifai model init --toolkit mcp` |
| OpenAI-compatible wrapper | `clarifai model init --toolkit openai` |
| Custom Python model | `clarifai model init --toolkit python` |

**Reference:** See `clarifai-cli` skill → "clarifai model init" section for complete command reference.

This generates base template files: `config.yaml`, `1/model.py`, `requirements.txt`.

### Steps 2-4: Customize (ONLY if toolkit template isn't enough)

**For most toolkit deployments (vLLM, SGLang, HuggingFace, Ollama, MCP, OpenAI), skip to Step 5.** The CLI-generated template works out of the box.

**Only do these steps for custom Python models (`--toolkit python`) or when you need to modify the generated template:**

1. Check [examples-index.md](examples/examples-index.md) for matching patterns
2. Browse https://github.com/Clarifai/runners-examples for additional examples
3. Adapt `config.yaml`, `1/model.py`, `requirements.txt` as needed

### Step 5: Final Summary (IMPORTANT)

**ALWAYS** provide a summary with TWO options:

**Option 1: CLI Init + Deploy (Recommended)**
```bash
# Quick start - use CLI to generate working template
clarifai model init ./my-model --toolkit <toolkit> --model-name "<model-id>"

# Test locally before deploying
clarifai model serve ./my-model

# Deploy to cloud in one step (auto-creates infrastructure)
clarifai model deploy ./my-model

# Or deploy with a specific GPU
clarifai model deploy ./my-model --instance gpu-nvidia-a10g

# Monitor (deploy prints the deployment ID to use here)
clarifai model status --deployment <deployment-id>
clarifai model logs --deployment <deployment-id>

# Clean up when done
clarifai model undeploy --deployment <deployment-id>
```

**CRITICAL: Waiting for Deploy completion**
Both `clarifai model upload` and `clarifai model deploy` stream build logs to your terminal and exit with a proper status code (0 for success, non-zero for failure). Do not interrupt until the command returns.

**Option 2: Custom Scripts (Generated above)**
"If you need more customization, I've also generated the complete scripts above that you can use directly. Copy them to your model directory and test with the same commands."

**CRITICAL:** Always suggest Option 1 (CLI init + deploy) first when a suitable toolkit exists. The CLI-generated templates are the most reliable starting point.

---

## Model Creation Decision Tree

```
Do you want to deploy an LLM?
├── YES → Which framework?
│   ├── vLLM (high performance) → --toolkit vllm
│   ├── SGLang (structured gen) → --toolkit sglang
│   ├── HuggingFace (direct) → --toolkit huggingface
│   ├── Ollama (local) → --toolkit ollama
│   └── LM Studio → --toolkit lmstudio
├── MCP server (tools)? → --toolkit mcp
├── OpenAI-compatible wrapper? → --toolkit openai
└── Custom Python model? → --toolkit python
```

**→ For exact CLI commands:** See `clarifai-cli` skill → "Use Case Routing" table for command mapping.

## Quick Start: Toolkit-Based Deployment

### Step 1: Initialize from Toolkit

Use `clarifai model init` with the appropriate toolkit. **Load the `clarifai-cli` skill** for complete command reference, all init options, and examples.

### Step 2: Test and Upload

**Load the `clarifai-cli` skill** for local testing commands (`clarifai model serve`) and upload/deploy commands (`clarifai model upload`, `clarifai model deploy`).

**IMPORTANT:** When running `clarifai model upload`, you must wait for the command to exit. It streams real-time build logs from the Clarifai platform and will indicate if the build succeeded or failed upon completion.

## Directory Structure

All Clarifai models follow this structure:

```
my-model/
├── 1/                    # Version directory (REQUIRED)
│   └── model.py          # ModelClass implementation
├── requirements.txt      # Python dependencies
└── config.yaml          # Clarifai configuration
```

## ModelClass Implementation

### Basic Template

```python
from clarifai.runners.models.model_class import ModelClass
from clarifai.runners.utils.data_utils import Param

class MyModel(ModelClass):
    """Custom model implementation."""

    def load_model(self):
        """Load model resources during startup (runs once)."""
        # Load your model, tokenizer, etc.
        self.model = load_your_model()
        self.tokenizer = load_your_tokenizer()

    @ModelClass.method
    def predict(
        self,
        prompt: str = "",
        max_tokens: int = Param(default=512, description="Max tokens to generate")
    ) -> str:
        """Inference method (called for each request)."""
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

### Exposing Methods to Clients (Pythonic API)

Any method decorated with `@ModelClass.method` is automatically available to users of the `Model` client. 

1. **Keyword Arguments**: Input parameters become keyword arguments in the client.
2. **Type Mapping**: Arguments typed as `str` (URLs/paths), `Image`, `Audio`, etc., are automatically handled.
3. **Return Values**: The return value of the method is returned directly to the client (converted to high-level types if needed).
4. **Streaming**: Methods that `yield` instead of `return` automatically become streaming endpoints on the client.

Example Client Usage:
```python
from clarifai.client import Model
model = Model("model_url")
output = model.predict(prompt="Tell me a joke", max_tokens=100)
```

### Streaming Template

```python
from typing import Iterator

@ModelClass.method
def generate(
    self,
    prompt: str = "",
    max_tokens: int = Param(default=512, description="Max tokens")
) -> Iterator[str]:
    """Streaming inference method."""
    for chunk in self.model.stream(prompt):
        yield chunk
```

### Multimodal Template

```python
from clarifai.runners.utils.data_types import Image, Video
from typing import List

@ModelClass.method
def predict(
    self,
    prompt: str = "",
    image: Image = None,
    video: Video = None,
    chat_history: List[dict] = None,
    max_tokens: int = Param(default=512, description="Max tokens")
) -> str:
    """Vision-language inference."""
    if image is None:
        return "Please provide an image."

    # Process image and generate response
    pil_image = PILImage.open(image.to_file())
    # ... your processing logic
    return response
```

## config.yaml Reference

> **IMPORTANT: Compute Reservations & Overhead**
> Do not request the full capacity of an instance type in `config.yaml`. Every deployment has infrastructure overhead (system processes, drivers, agents).
> **Rule of Thumb:** Request **80% or less** of the instance's total CPU, CPU Memory, and GPU Memory. For example, if an instance has 16Gi of memory, set `cpu_memory` to `12Gi` or `13Gi`.

### Simplified Configuration (Recommended)

The minimal config.yaml generated by `clarifai model init`. Uses `compute.instance` shorthand:

```yaml
model:
  id: "my-model-id"
  model_type_id: "any-to-any"

compute:
  instance: g5.xlarge  # Run 'clarifai list-instances' to see all options.
  # cloud: aws          # Cloud provider (auto-detected from instance)
  # region: us-east-1   # Cloud region (auto-detected from instance)

# Uncomment to auto-download model checkpoints:
# checkpoints:
#   repo_id: owner/model-name
```

**Key points:**
- `user_id` and `app_id` are auto-resolved from CLI context at deploy time
- `compute.instance` replaces verbose `inference_compute_info` section
- Use `clarifai list-instances` to browse available instances
- Default `model_type_id` is `any-to-any` (works for all model types)

You only need the verbose `inference_compute_info` format if you need fine-grained control over CPU/memory limits.

### Verbose Configuration (Basic)

```yaml
model:
  id: "my-model-id"
  user_id: "YOUR_USER_ID"
  app_id: "YOUR_APP_ID"
  model_type_id: "any-to-any"  # See model types below

build_info:
  python_version: "3.12"

inference_compute_info:
  cpu_limit: "2"
  cpu_memory: "8Gi"
  num_accelerators: 0  # CPU only
```

### Verbose GPU Configuration

```yaml
model:
  id: "my-gpu-model"
  user_id: "YOUR_USER_ID"
  app_id: "YOUR_APP_ID"
  model_type_id: "any-to-any"

build_info:
  python_version: "3.12"

inference_compute_info:
  cpu_limit: "2"
  cpu_memory: "12Gi"
  cpu_requests: "1"
  cpu_memory_requests: "8Gi"
  num_accelerators: 1
  accelerator_type: ["NVIDIA-*"]
  accelerator_memory: "14Gi"
```

### With HuggingFace Checkpoints

```yaml
model:
  id: "my-hf-model"
  model_type_id: "any-to-any"

checkpoints:
  repo_id: "meta-llama/Llama-3.2-1B-Instruct"
  # type: "huggingface"  # Auto-detected from repo_id
  # when: "runtime"      # Default: runtime. Options: runtime, build, upload
  # hf_token: "YOUR_HF_TOKEN"  # For gated models

compute:
  instance: g5.xlarge
```

## Model Type IDs

| model_type_id | Description | When to Use |
|---------------|-------------|-------------|
| `any-to-any` | Any input, any output | **Default for most models** (LLMs, custom, multimodal) |
| `multimodal-to-text` | Image/video + text input, text output | Vision-language models (enables upload UI) |
| `visual-classifier` | Image input, classification output | Image classifiers |
| `visual-detector` | Image input, bounding boxes | Object detectors |
| `visual-segmenter` | Image input, segmentation masks | Semantic segmentation |
| `text-embedder` | Text input, embeddings output | Text embedding models |
| `text-to-text` | Text input, text output | Text-only LLMs (legacy, prefer `any-to-any`) |
| `mcp` | MCP server | Tool-calling servers |

**Notes:**
- `any-to-any` is the default and recommended type for most models (including LLMs)
- Use `multimodal-to-text` for models that accept images/videos to enable the upload UI
- Use `mcp` specifically for MCP tool-calling servers

## Local Testing Workflow

Test your model locally before deploying using `clarifai model serve`:

```bash
# Fastest: use current Python env (deps must be pre-installed)
clarifai model serve ./my-model

# Isolated: auto-create virtualenv with deps
clarifai model serve ./my-model --mode env

# Production-like: build and run in Docker container
clarifai model serve ./my-model --mode container

# Standalone gRPC server (no Clarifai login needed)
clarifai model serve ./my-model --grpc --port 8000
```

**ALWAYS try `clarifai model serve` first** - it's the fastest path to testing.

**Load the `clarifai-cli` skill** for complete options.

## Deploy in One Step

After testing locally, deploy to the cloud with a single command:

```bash
# Auto-selects GPU from config.yaml, creates infrastructure automatically
clarifai model deploy ./my-model

# Specify GPU instance explicitly
clarifai model deploy ./my-model --instance gpu-nvidia-a10g

# Deploy already-uploaded model
clarifai model deploy --model-url "https://clarifai.com/user/app/models/my-model"

# Browse available GPUs first
clarifai list-instances --cloud aws --gpu A10G
```

The deploy command:
1. Uploads and builds the model (if local path provided)
2. Auto-creates compute cluster and nodepool (or reuses existing)
3. Creates deployment and monitors until pods are running
4. On success, prints: model URL, deployment ID, usage code snippet, and Playground URL
5. Zero interactive prompts - fully non-interactive, suitable for CI/CD

## Common Model Patterns

### Text-to-Text LLM

```python
import os
from clarifai.runners.models.model_class import ModelClass
from clarifai.runners.models.model_builder import ModelBuilder
from clarifai.runners.utils.data_utils import Param
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class TextToTextLLM(ModelClass):
    def load_model(self):
        # Download checkpoints defined in config.yaml
        model_path = os.path.dirname(os.path.dirname(__file__))
        builder = ModelBuilder(model_path, download_validation_only=True)
        checkpoint_path = builder.download_checkpoints(stage="runtime")

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            checkpoint_path,
            torch_dtype=torch.bfloat16,
            device_map=self.device
        )

    @ModelClass.method
    def predict(
        self,
        prompt: str = "",
        max_tokens: int = Param(default=512, description="Max tokens"),
        temperature: float = Param(default=0.7, description="Temperature")
    ) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### Image Classifier

```python
import os
from clarifai.runners.models.model_class import ModelClass
from clarifai.runners.models.model_builder import ModelBuilder
from clarifai.runners.utils.data_types import Image
from clarifai.runners.utils.data_utils import Param
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image as PILImage

class ImageClassifier(ModelClass):
    def load_model(self):
        # Download checkpoints defined in config.yaml
        model_path = os.path.dirname(os.path.dirname(__file__))
        builder = ModelBuilder(model_path, download_validation_only=True)
        checkpoint_path = builder.download_checkpoints(stage="runtime")

        self.processor = AutoImageProcessor.from_pretrained(checkpoint_path)
        self.model = AutoModelForImageClassification.from_pretrained(checkpoint_path)

    @ModelClass.method
    def predict(
        self,
        image: Image,
        top_k: int = Param(default=5, description="Number of top predictions")
    ) -> str:
        pil_image = PILImage.open(image.to_file())
        inputs = self.processor(pil_image, return_tensors="pt")
        outputs = self.model(**inputs)

        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        top_probs, top_indices = torch.topk(probs, top_k)

        results = []
        for prob, idx in zip(top_probs[0], top_indices[0]):
            label = self.model.config.id2label[idx.item()]
            results.append(f"{label}: {prob.item():.4f}")

        return "\n".join(results)
```

## Best Practices & Pitfalls

### Coding the ModelClass (`1/model.py`)

*   **Reliable Initialization**: Use `ModelBuilder` inside `load_model()` to download checkpoints defined in `config.yaml`. This ensures weights are fetched using platform optimizations (like `hf_transfer`) before the model starts loading.
*   **Checkpoint Download Pattern**:
    ```python
    model_path = os.path.dirname(os.path.dirname(__file__))
    builder = ModelBuilder(model_path, download_validation_only=True)
    checkpoint_path = builder.download_checkpoints(stage="runtime")
    ```
*   **Device Management**: Always capture `self.device` during `load_model` (e.g., `self.device = "cuda" if torch.cuda.is_available() else "cpu"`) and explicitly pass it to model/library constructors. Avoid using `device_map="auto"` combined with `.to(device)` calls.

### The Deployment Loop

*   **Immutability**: Once a model version is uploaded, it cannot be changed. If you fix a bug in `model.py`, you **must** call `clarifai model upload` again and note the NEW version ID.
*   **Cleaning Up**: Before creating a new deployment for a fixed version, delete the old deployment and wait ~5 seconds for the platform to release the ID.
*   **Observability link**: If the model status is `TRAINED` but the deployment is hanging, run `clarifai model logs --deployment <id> --log-type events` or consult the `clarifai-observability` skill to check infrastructure scheduling errors.

### Do's
- Use `torch.no_grad()` and `.clone()` if needed
- Use `ModelBuilder` in `load_model()` to download checkpoints
- **Account for overhead**: Set compute requirements to ~80% of instance capacity
- Use `device_map="cuda"` directly (not `"auto"` with `.to()`)
- Always test locally before upload
- Use type hints for all parameters
- Use `Param()` for UI descriptions

### Don'ts
- Don't request 100% of an instance's CPU/Memory (it will fail to schedule/start)
- Don't hardcode HuggingFace repo IDs in `model.py` (use `config.yaml`)
- Don't assume checkpoints are automatically present (call `ModelBuilder().download_checkpoints()`)
- Don't use manual `snapshot_download` or `from_pretrained("repo/id")`
- Don't use `torch.inference_mode()` with image tokens
- Don't skip local testing
- Don't use `device_map="auto"` with `.to()` calls
- **Don't forget to update your version ID** in deployment scripts after a re-upload.

## Monitoring and Logs

You can access logs directly from the `Deployment` object to monitor model behavior and debug issues.

```python
from clarifai.client.deployment import Deployment

deployment = Deployment(deployment_id="my-deployment", user_id="user_id")

# Stream logs in real-time for a deployed runner
for entry in deployment.logs(log_type="runner", stream=True):
    print(entry.message, end="")

# List previous logs with pagination
for entry in deployment.logs(stream=False, page=1, per_page=50):
    print(entry.message)

# Access specific log types (default is "runner")
# Use log_type="builder" for build/upload logs
build_logs = list(deployment.logs(log_type="builder"))
```

Note: The `logs()` method automatically captures necessary IDs (model version, nodepool) from the deployment context.

For batch processing or orchestration flows, you can also access logs from the `Pipeline` object:

```python
from clarifai.client.pipeline import Pipeline

pipeline = Pipeline(pipeline_id="my-pipeline", user_id="user_id", app_id="app_id", pipeline_version_run_id="run_id")

# Stream logs for a running pipeline
for entry in pipeline.logs(stream=True):
    print(entry.message, end="")
```

Finally, you can also access logs directly from the `Model` object if it was initialized with a `deployment_id`:

```python
from clarifai.client.model import Model

model = Model(user_id="user_id", app_id="app_id", model_id="model_id", deployment_id="my-deployment")

# Stream logs for the model's runner
for entry in model.logs(stream=True):
    print(entry.message, end="")
```

## Scaling and Updates

You can update deployment scaling parameters directly using the `update()` method on the `Deployment` object.

```python
from clarifai.client.deployment import Deployment

deployment = Deployment(deployment_id="my-deployment", user_id="user_id")

# Update min and max replicas for scaling
deployment.update(min_replicas=1, max_replicas=5)

# For more granular updates, use the patch method
# IMPORTANT: The Clarifai backend requires action="overwrite" for deployment patches
deployment.patch(
    action="overwrite",
    autoscale_config={
        "min_replicas": 2,
        "max_replicas": 10,
        "scale_to_zero_delay_seconds": 300
    }
)
```

Note: The `update()` method automatically uses `action="overwrite"` internally.

## Extended Search

For more examples and edge cases:
- **Runner examples**: https://github.com/Clarifai/runners-examples
- **SDK source**: https://github.com/Clarifai/clarifai-python
- **Documentation**: https://docs.clarifai.com/compute/upload/

## References

- Toolkit models: [references/toolkit-models.md](references/toolkit-models.md)
