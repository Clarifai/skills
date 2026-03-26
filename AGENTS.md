# Clarifai Platform for Agents

Clarifai is a comprehensive end-to-end AI platform designed to manage the entire machine learning lifecycle, from data ingestion and labeling to model training, deployment, and inference. For an AI agent, Clarifai provides a robust set of tools and APIs to orchestrate complex AI workflows across Computer Vision, Natural Language Processing, and Audio domains.

## Platform Overview

### Core Entities
- **User**: The primary account holder.
- **App**: The foundational container for resources. All models, workflows, and datasets exist within an App.
- **Model**: An individual AI processing unit. Models can be built-in (Clarifai-provided), imported from Hugging Face, or custom-built.
- **Workflow**: A directed acyclic graph (DAG) of models. Workflows allow you to chain multiple models together (e.g., Crop -> Classify -> Translate).
- **Dataset**: A collection of inputs (images, text, video, audio) and annotations used for training or evaluation.
- **Pipeline**: A containerized multi-step batch workflow for training, ETL, and data processing jobs.
- **Runner**: A compute resource that executes a model or a pipeline step.
- **Deployment**: The association of a worker (model/workflow) with specific compute resources. Created automatically by `clarifai model deploy`.

### Resource Hierarchy

```
User
└── App (Application)
    ├── Inputs (data: images, text, video, audio)
    ├── Datasets (organized collections of inputs)
    ├── Concepts (labels/tags)
    ├── Models (AI models)
    ├── Workflows (model pipelines)
    ├── Pipelines (batch processing workflows)
    └── Modules
└── ComputeCluster
    └── Nodepool
        └── Runner
└── Deployment
```

### Interfaces
- **Python SDK**: High-level, developer-friendly interface for automation.
- **CLI**: Powerful command-line tool for model init, serve, deploy, status, logs, and undeploy.
- **gRPC API**: Low-level, high-performance API that powers the platform.
- **MCP (Model Context Protocol)**: Specialized servers that allow agents to use Clarifai capabilities as "tools." Supports both `MCPModelClass` (FastMCP) and `StdioMCPModelClass` (bridge external stdio MCP servers like GitHub, filesystem).
- **Agentic Models**: LLM + MCP tool-calling via `AgenticModelClass` with persistent connection pools and automatic tool discovery.

---

## Agentic Skills

These skills provide specialized instructions for specific segments of the Clarifai platform. Agents should refer to these when tasked with related objectives.

### 1. [Agentic Flows](.github/skills/clarifai-agentic-flows/SKILL.md)
Orchestrate multi-step operations. Use this when you need to combine actions, such as "upload a model AND then deploy it" or "train a model followed by evaluation."

### 2. [CLI Operations](.github/skills/clarifai-cli/SKILL.md)
Guides on using the `clarifai` CLI for the full model lifecycle: `init`, `serve`, `deploy`, `status`, `logs`, `undeploy`, plus compute discovery (`list-instances`), authentication, and app management.

### 3. [Datasets & Data Management](.github/skills/clarifai-datasets/SKILL.md)
Instructions for uploading data, managing annotations, and converting between common formats like COCO, VOC, and YOLO.

### 4. [Deployment Lifecycle](.github/skills/clarifai-deployment-lifecycle/SKILL.md)
Manage deployments via CLI (`deploy`, `status`, `logs`, `undeploy`). Also covers version patching, state transition monitoring, and the programmatic Delete-then-Post re-deployment pattern.

### 5. [gRPC API](.github/skills/clarifai-grpc/SKILL.md)
Low-level operations when high performance or specialized platform features (not yet in the SDK) are required.

### 6. [Inference & Model Discovery](.github/skills/clarifai-inference/SKILL.md)
Discovering available models and generating optimized code for predictions. Includes using Clarifai's OpenAI-compatible API.

### 7. [MCP Servers](.github/skills/clarifai-mcp/SKILL.md)
Building and deploying MCP servers using `MCPModelClass` (FastMCP) or `StdioMCPModelClass` (bridge external stdio servers like GitHub, filesystem) to provide custom tools to AI agents.

### 8. [Model Upload & Deployment](.github/skills/clarifai-model-upload/SKILL.md)
The authoritative guide for deploying custom models. Covers `ModelClass` implementation, `config.yaml` resource rules (the 80% rule), toolkit integration (vLLM, Ollama), and the zero-prompt `clarifai model deploy` workflow with auto-infrastructure creation.

### 9. [Observability & Logging](.github/skills/clarifai-observability/SKILL.md)
**Use this first when a deployment is stuck, crashing, or failing.** Covers `clarifai model logs`, `clarifai model status`, K8s event interpretation, and common resolution patterns.

### 10. [Pipelines](.github/skills/clarifai-pipelines/SKILL.md)
Creating containerized multi-step pipelines and using the Artifacts API for data transfer between steps.

### 11. [Training Pipelines](.github/skills/clarifai-training-pipelines/SKILL.md)
Implementing training jobs for classifiers and detectors using Clarifai's built-in templates.
