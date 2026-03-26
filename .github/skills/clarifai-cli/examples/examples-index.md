# Clarifai CLI Examples Index

## Command Examples

The SKILL.md contains comprehensive examples for each command. Here are quick references:

### Model Initialization Examples

```bash
# vLLM model
clarifai model init ./vllm-model --toolkit vllm --model-name "Qwen/Qwen3-4B-Instruct-2507"

# SGLang model
clarifai model init ./sglang-model --toolkit sglang --model-name "unsloth/Llama-3.2-1B-Instruct"

# HuggingFace model
clarifai model init ./hf-model --toolkit huggingface --model-name "meta-llama/Llama-3.2-1B-Instruct"

# MCP server
clarifai model init ./mcp-server --toolkit mcp
```

### Pipeline Training Examples

```bash
# Image classifier training
clarifai pipeline init ./classifier --template classifier-pipeline-resnet
clarifai pipeline upload ./classifier
clarifai pipeline run --compute_cluster_id cc-123 --nodepool_id np-456

# Object detector training
clarifai pipeline init ./detector --template detector-pipeline-yolof
clarifai pipeline upload ./detector
clarifai pipeline run --compute_cluster_id cc-123 --nodepool_id np-456
```

### Local Testing & Deployment Examples

```bash
# Serve locally (fastest)
clarifai model serve ./my-model

# Serve in container (production-like)
clarifai model serve ./my-model --mode container

# Serve as standalone gRPC server
clarifai model serve ./my-model --grpc --port 8000

# Deploy to cloud (auto-creates infrastructure)
clarifai model deploy ./my-model

# Deploy with specific GPU
clarifai model deploy ./my-model --instance gpu-nvidia-a10g

# Check status / stream logs / undeploy (use deployment ID from deploy output)
clarifai model status --deployment <deployment-id>
clarifai model logs --deployment <deployment-id>
clarifai model undeploy --deployment <deployment-id>

# Browse available GPU instances
clarifai list-instances --cloud aws --gpu A10G
```

## GitHub Examples

For more complex examples, see:

- **Model examples**: https://github.com/Clarifai/runners-examples
- **Pipeline examples**: https://github.com/Clarifai/pipeline-examples
- **General examples**: https://github.com/Clarifai/examples
