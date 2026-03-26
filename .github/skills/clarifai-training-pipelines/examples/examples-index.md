# Training Pipeline Examples Index

## Local Examples

| Example | Description | Location |
|---------|-------------|----------|
| classifier-pipeline-resnet | ResNet-50 image classifier training | examples/classifier-pipeline-resnet/ |

## GitHub Examples

For additional training examples: https://github.com/Clarifai/pipeline-examples

### Available Templates
| Template | Model | Task |
|----------|-------|------|
| classifier-pipeline-resnet | ResNet-50 | Image classification |
| detector-pipeline-yolof | YOLOF | Object detection |

## How to Use Templates

```bash
# Initialize from template
clarifai pipeline init ./my-classifier --template classifier-pipeline-resnet
```

## Customizing Training

1. Edit `config.yaml` to set:
   - `dataset_id`: Your Clarifai dataset
   - `epochs`: Number of training epochs
   - `batch_size`: Training batch size
   - `learning_rate`: Initial learning rate

2. Upload and run:
```bash
clarifai pipeline upload ./my-classifier
clarifai pipeline run --compute_cluster_id <id> --nodepool_id <id>
```
