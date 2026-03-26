---
name: clarifai-training-pipelines
description: Train models using Clarifai pipeline templates. Use when the user wants to train image classifiers (ResNet-50), object detectors (YOLOF), or create custom training pipelines. Covers built-in templates (classifier-pipeline-resnet, detector-pipeline-yolof), custom training implementation, hyperparameter configuration, and training monitoring.
---

# Model Training with Pipelines

> **IMPORTANT:** For SDK methods and CLI commands and code generation, first scan [../clarifai-cli/references/sdk-cli-reference.md](../clarifai-cli/references/sdk-cli-reference.md)

Train image classifiers and object detectors using Clarifai's pipeline system.

## CRITICAL: Only 2 Built-in Templates

| Template | Model | Task |
|----------|-------|------|
| `classifier-pipeline-resnet` | ResNet-50 | Image classification |
| `detector-pipeline-yolof` | YOLOF | Object detection |

**DO NOT suggest any other templates.** These are the ONLY two.

## Decision Tree

```
What to train?
├── ResNet-50 classifier? → Use template (this skill)
├── YOLOF detector? → Use template (this skill)
└── Anything else? → Use clarifai-pipelines skill (custom pipeline)
```

## CLI Commands

**See `clarifai-cli` skill** for all pipeline CLI commands:
- `clarifai pipeline init --template <template>`
- `clarifai pipeline upload`
- `clarifai pipeline run --compute_cluster_id <id> --nodepool_id <id>`
- `clarifai pipelinerun monitor/pause/resume/cancel`

## Quick Start: ResNet-50 Classifier

### 1. Initialize
```bash
clarifai pipeline init ./classifier --template classifier-pipeline-resnet
```

### 2. Configure (config.yaml)
```yaml
pipeline:
  id: "my-classifier"
  user_id: "YOUR_USER_ID"
  app_id: "YOUR_APP_ID"

  parameters:
    dataset_id: "YOUR_DATASET_ID"
    epochs: 10
    batch_size: 32
    learning_rate: 0.001
```

### 3. Upload & Run
```bash
clarifai pipeline upload ./classifier
clarifai pipeline run --compute_cluster_id <id> --nodepool_id <id>
```

## Quick Start: YOLOF Detector

### 1. Initialize
```bash
clarifai pipeline init ./detector --template detector-pipeline-yolof
```

### 2. Configure (config.yaml)
```yaml
pipeline:
  id: "my-detector"
  user_id: "YOUR_USER_ID"
  app_id: "YOUR_APP_ID"

  parameters:
    dataset_id: "YOUR_DETECTION_DATASET_ID"
    epochs: 20
    batch_size: 16
    learning_rate: 0.0001
```

### 3. Upload & Run
```bash
clarifai pipeline upload ./detector
clarifai pipeline run --compute_cluster_id <id> --nodepool_id <id>
```

## Training Parameters

### ResNet Classifier
| Parameter | Default | Description |
|-----------|---------|-------------|
| `dataset_id` | required | Clarifai dataset ID |
| `epochs` | 10 | Training epochs |
| `batch_size` | 32 | Batch size |
| `learning_rate` | 0.001 | Learning rate |

### YOLOF Detector
| Parameter | Default | Description |
|-----------|---------|-------------|
| `dataset_id` | required | Dataset with bounding boxes |
| `epochs` | 20 | Training epochs |
| `batch_size` | 16 | Batch size |
| `learning_rate` | 0.0001 | Learning rate |

## Dataset Requirements

**Classification:** Images with class labels. See `clarifai-datasets` skill.

**Detection:** Images with bounding box annotations (COCO/VOC/YOLO format). See `clarifai-datasets` skill.

## Custom Training (NOT ResNet-50/YOLOF)

**→ Use `clarifai-pipelines` skill** for:
- LLM fine-tuning
- Segmentation models
- Custom architectures
- Any other training

The `clarifai-pipelines` skill shows how to wrap vanilla Python training scripts in pipeline structure.

## Extended Search

- **Training pipelines**: https://github.com/Clarifai/pipeline-examples
- **Documentation**: https://docs.clarifai.com/compute/pipelines/training/

## References

See [examples/examples-index.md](examples/examples-index.md) for training pipeline templates.
