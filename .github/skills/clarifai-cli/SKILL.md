---
name: clarifai-cli
description: Execute Clarifai operations using the `clarifai` CLI. Use when the user needs to authenticate, check identity, manage apps, compute clusters, nodepools, deployments, pipelines, pipeline runs, artifacts, or initialize models. Covers model init (toolkits, MCP, GitHub templates), pipeline templates, compute orchestration CLI, and all model/pipeline operations.
---

# Clarifai CLI

> **IMPORTANT:** For SDK methods and CLI commands and code generation, first scan [references/sdk-cli-reference.md](references/sdk-cli-reference.md)

The `clarifai` CLI provides terminal access to all Clarifai platform operations including model initialization, upload, local testing, pipeline management, and compute orchestration.

## Quick Command Reference

| Task | Command |
|------|---------|
| Login | `clarifai login` |
| Logout | `clarifai logout` |
| Whoami | `clarifai whoami` |
| Config profiles | `clarifai config` |
| Initialize model | `clarifai model init` |
| Init from toolkit | `clarifai model init --toolkit vllm` |
| Init MCP server | `clarifai model init --toolkit mcp` |
| Upload model | `clarifai model upload ./model` |
| Serve locally | `clarifai model serve ./model` |
| Serve as gRPC | `clarifai model serve ./model --grpc --port 8000` |
| Deploy to cloud | `clarifai model deploy ./model` |
| Deploy with GPU | `clarifai model deploy ./model --instance gpu-nvidia-a10g` |
| Deploy existing model | `clarifai model deploy --model-url <url>` |
| Check status (by deployment) | `clarifai model status --deployment <id>` |
| Check status (by model) | `clarifai model status --model-url <url>` |
| Stream logs | `clarifai model logs --deployment <id>` |
| Undeploy | `clarifai model undeploy --deployment <id>` |
| Predict | `clarifai model predict <model_ref> "Hello!"` |
| Predict with inputs | `clarifai model predict --model-url <url> -i prompt="Hi" -i max_tokens=100` |
| List models | `clarifai model list` |
| List GPU instances | `clarifai list-instances` |
| Filter instances | `clarifai list-instances --cloud aws --gpu A10G` |
| Init pipeline | `clarifai pipeline init` |
| Init from template | `clarifai pipeline init --template classifier-pipeline-resnet` |
| Upload pipeline | `clarifai pipeline upload` |
| Run pipeline | `clarifai pipeline run --compute_cluster_id <id> --nodepool_id <id>` |
| List pipelines | `clarifai pipeline list` |
| List pipeline templates | `clarifai pipelinetemplate list` |
| Discover templates | `clarifai pipelinetemplate discover` |
| Manage pipeline runs | `clarifai pipelinerun` |
| List deployments | `clarifai deployment list --compute_cluster_id <id>` |
| Create deployment | `clarifai deployment create <deployment_id> --compute_cluster_id <id> --nodepool_id <id>` |
| Delete deployment | `clarifai deployment delete <deployment_id>` |
| List nodepools | `clarifai nodepool list --compute_cluster_id <id>` |
| Create nodepool | `clarifai nodepool create <nodepool_id> --compute_cluster_id <id>` |
| Delete nodepool | `clarifai nodepool delete <nodepool_id>` |
| List apps | `clarifai app list [--user_id <user_id>]` |
| Create app | `clarifai app create <app_id>` |
| Delete app | `clarifai app delete <app_id>` |
| List compute clusters | `clarifai computecluster list` |
| Create compute cluster | `clarifai computecluster create <cluster_id> --config <config_file>` |
| Delete compute cluster | `clarifai computecluster delete <cluster_id>` |
| Manage artifacts | `clarifai artifact` |
| Run script with context | `clarifai run <script.py>` |
| Shell completion | `clarifai shell-completion` |

## Use Case Routing

| User Request | Primary Command | Follow-up |
|--------------|-----------------|-----------|
| "Check who I'm logged in as" | `clarifai whoami` | |
| "Log out" | `clarifai logout` | |
| "Manage config profiles" | `clarifai config` | |
| "List my apps" | `clarifai app list` | |
| "List apps for another user" | `clarifai app list --user_id <user_id>` | |
| "Create a new app" | `clarifai app create <app_id>` | |
| "Delete an app" | `clarifai app delete <app_id>` | |
| "List compute clusters" | `clarifai computecluster list` | |
| "Create compute cluster" | `clarifai computecluster create <id> --config <file>` | |
| "Delete compute cluster" | `clarifai computecluster delete <id>` | |
| "List nodepools" | `clarifai nodepool list --compute_cluster_id <id>` | |
| "Create nodepool" | `clarifai nodepool create <id> --compute_cluster_id <id>` | |
| "Delete nodepool" | `clarifai nodepool delete <id>` | |
| "List deployments" | `clarifai deployment list --compute_cluster_id <id>` | |
| "Create deployment" | `clarifai deployment create <id> --compute_cluster_id <id> --nodepool_id <id>` | |
| "Delete deployment" | `clarifai deployment delete <id>` | |
| "List pipeline runs" | `clarifai pipelinerun list` | |
| "Pause pipeline run" | `clarifai pipelinerun pause <run_id>` | |
| "Resume pipeline run" | `clarifai pipelinerun resume <run_id>` | |
| "Cancel pipeline run" | `clarifai pipelinerun cancel <run_id>` | |
| "Discover pipeline templates" | `clarifai pipelinetemplate discover` | |
| "List pipeline templates" | `clarifai pipelinetemplate list` | |
| "Manage artifacts" | `clarifai artifact` | |
| "Deploy vLLM model" | `clarifai model init --toolkit vllm` | `clarifai model deploy` |
| "Deploy SGLang model" | `clarifai model init --toolkit sglang` | `clarifai model deploy` |
| "Deploy HuggingFace model" | `clarifai model init --toolkit huggingface` | `clarifai model deploy` |
| "Deploy Ollama model" | `clarifai model init --toolkit ollama` | `clarifai model serve` |
| "Create MCP server" | `clarifai model init --toolkit mcp` | `clarifai model deploy` |
| "Create OpenAI-compatible model" | `clarifai model init --toolkit openai` | `clarifai model deploy` |
| "Train image classifier" | `clarifai pipeline init --template classifier-pipeline-resnet` | `clarifai pipeline run` |
| "Train object detector" | `clarifai pipeline init --template detector-pipeline-yolof` | `clarifai pipeline run` |
| "Test model locally" | `clarifai model serve ./model` | **Always try first** |
| "Test as gRPC server" | `clarifai model serve ./model --grpc --port 8000` | |
| "Test in container" | `clarifai model serve ./model --mode container` | |
| "Deploy model to cloud" | `clarifai model deploy ./model` | Auto-creates infra |
| "Deploy with specific GPU" | `clarifai model deploy ./model --instance gpu-nvidia-a10g` | |
| "Deploy already-uploaded model" | `clarifai model deploy --model-url <url>` | |
| "Check deployment status" | `clarifai model status --deployment <id>` | Use `--model-url` to discover deployments |
| "View deployment logs" | `clarifai model logs --deployment <id>` | Follows by default |
| "View K8s events" | `clarifai model logs --deployment <id> --log-type events` | For debugging startup |
| "Remove deployment" | `clarifai model undeploy --deployment <id>` | |
| "Browse available GPUs" | `clarifai list-instances` | Filter: `--cloud`, `--gpu` |

## References

- **Complete SDK + CLI reference**: [references/sdk-cli-reference.md](references/sdk-cli-reference.md)
