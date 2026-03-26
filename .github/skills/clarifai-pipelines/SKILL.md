---
name: clarifai-pipelines
description: Create and run Clarifai pipelines for batch processing and multi-step workflows. Use when the user wants to create custom pipelines with containerized steps, transfer data between steps using Artifacts API, or orchestrate long-running workflows. NOT for training - use clarifai-training-pipelines for model training.
---

# Clarifai Pipelines

> **IMPORTANT:** For SDK methods and CLI commands and code generation, first scan [../clarifai-cli/references/sdk-cli-reference.md](../clarifai-cli/references/sdk-cli-reference.md)

Build containerized multi-step workflows for batch processing and data pipelines.

## When to Use This Skill

| Use This Skill | Use clarifai-training-pipelines |
|----------------|--------------------------------|
| Custom batch processing, ETL | ResNet-50 image classifier |
| Custom training (LLM, segmentation) | YOLOF object detector |
| Any training NOT ResNet-50/YOLOF | |

**clarifai-training-pipelines has ONLY 2 templates.** For anything else, use THIS skill.

## CLI Commands

**See `clarifai-cli` skill** for all pipeline and artifact CLI commands:
- `clarifai pipeline init/upload/run/list`
- `clarifai pipelinerun monitor/pause/resume/cancel`
- `clarifai artifact cp/list/get/delete` (for data transfer between steps)

## Pipeline Directory Structure

Wrap your vanilla Python scripts in this structure:

```
my-pipeline/
├── config.yaml              # Main pipeline config
├── stepA/
│   ├── config.yaml         # Step config
│   ├── requirements.txt
│   └── 1/
│       └── pipeline_step.py         # Vanilla Python script
├── stepB/
│   ├── config.yaml
│   ├── requirements.txt
│   └── 1/
│       └── pipeline_step.py
```

## Main config.yaml

```yaml
pipeline:
  id: "my-pipeline"
  user_id: "YOUR_USER_ID"
  app_id: "YOUR_APP_ID"

  pipeline_steps:
    - id: "stepA"
      model_dir: "./stepA"
    - id: "stepB"
      model_dir: "./stepB"
      depends_on: ["stepA"]

  orchestration_spec:
    entrypoint: main
    templates:
      - name: main
        dag:
          tasks:
            - name: stepA
              template: stepA-template
            - name: stepB
              template: stepB-template
              depends: stepA
```

## Step Implementation (Vanilla Python)

```python
#!/usr/bin/env python3
"""Pipeline step - vanilla Python script."""
import os
from clarifai.client.artifact_version import ArtifactVersion

def main():
    user_id = os.environ.get("CLARIFAI_USER_ID")
    app_id = os.environ.get("CLARIFAI_APP_ID")

    # Your processing logic here
    process_data()

    # Upload output as artifact
    version = ArtifactVersion().upload(
        file_path="/tmp/output.pt",
        artifact_id="step-output",
        user_id=user_id,
        app_id=app_id
    )
    print(f"Uploaded: {version.id}")

def process_data():
    pass

if __name__ == "__main__":
    main()
```

## Step config.yaml (CPU)

```yaml
pipeline_step:
  id: "my-step"
  user_id: "YOUR_USER_ID"
  app_id: "YOUR_APP_ID"
  model_type_id: "any-to-any"

build_info:
  python_version: "3.12"

inference_compute_info:
  cpu_limit: "2"
  cpu_memory: "8Gi"
  num_accelerators: 0
```

## Step config.yaml (GPU)

```yaml
pipeline_step:
  id: "training-step"
  user_id: "YOUR_USER_ID"
  app_id: "YOUR_APP_ID"
  model_type_id: "any-to-any"

build_info:
  python_version: "3.12"

inference_compute_info:
  cpu_limit: "4"
  cpu_memory: "32Gi"
  num_accelerators: 1
  accelerator_type: ["NVIDIA-A10G", "NVIDIA-A100"]
  accelerator_memory: "40Gi"
```

## Artifacts SDK (Data Transfer)

```python
from clarifai.client.artifact import Artifact
from clarifai.client.artifact_version import ArtifactVersion

# Upload
version = ArtifactVersion().upload(
    file_path="./model.pt",
    artifact_id="my-model",
    user_id="user123",
    app_id="app456"
)

# Download
version = ArtifactVersion(
    artifact_id="my-model",
    version_id="v123",
    user_id="user123",
    app_id="app456"
)
version.download(output_path="./downloaded.pt")
```

## Extended Search

- **Pipeline examples**: https://github.com/Clarifai/pipeline-examples
- **Documentation**: https://docs.clarifai.com/compute/pipelines/

## References

- Pipeline structure: [references/pipeline-structure.md](references/pipeline-structure.md)
