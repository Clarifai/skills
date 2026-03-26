---
name: clarifai-deployment-lifecycle
description: Manage the end-to-end lifecycle of Clarifai deployments. Use when deploying, updating, monitoring, or removing model deployments. Covers the CLI-first deploy/status/logs/undeploy workflow, version tracking with metadata, the Delete-then-Post cycle, and state transition monitoring.
---

# Clarifai Deployment Lifecycle

Managing deployments involves the full lifecycle: deploy, monitor, update, and teardown. The CLI provides the primary interface for all these operations.

## CLI-First Deployment (Recommended)

The `clarifai model deploy` command handles the entire deployment lifecycle with zero interactive prompts:

```bash
# Deploy from local model directory (auto-creates infrastructure)
clarifai model deploy ./my-model

# Deploy with specific GPU
clarifai model deploy ./my-model --instance gpu-nvidia-a10g

# Deploy already-uploaded model
clarifai model deploy --model-url "https://clarifai.com/user/app/models/my-model"

# After deploy, use the deployment ID from the output:
clarifai model status --deployment <deployment-id>
clarifai model logs --deployment <deployment-id>
clarifai model logs --deployment <deployment-id> --log-type events
clarifai model undeploy --deployment <deployment-id>
```

> **When to use `--deployment` vs `--model-url`:**
> - Use `--deployment <id>` when you have the deployment ID (printed by `clarifai model deploy`)
> - Use `--model-url <url>` when you don't know the deployment ID and want to discover deployments for a model

### What `clarifai model deploy` Does

1. **Uploads and builds** the model (if local path provided)
2. **Discovers or creates** compute cluster and nodepool based on `--instance` or config.yaml
3. **Creates deployment** with autoscaling (default: 1-5 replicas)
4. **Monitors** until pods are running and healthy
5. **Zero prompts** - fully non-interactive, suitable for CI/CD

### Browse Available GPUs

```bash
# List all available compute instances
clarifai list-instances

# Filter by cloud and GPU
clarifai list-instances --cloud aws --gpu A10G

# Find high-memory GPUs
clarifai list-instances --min-gpu-mem 80Gi
```

## Advanced: Programmatic Deployment

## Version Patching (The Refresh Cycle)

When model code is updated in `1/model.py`, a new version must be uploaded, and the active deployment must be pointed to that new version. Since deployments are currently static, the standard pattern is **Delete-then-Post**.

### Automated Re-deployment Pattern

```python
from clarifai.client.user import User
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
import time

def refresh_deployment(app, deployment_id, model_id, version_id, nodepool_id):
    # 1. Check if exists
    list_req = service_pb2.ListDeploymentsRequest(user_app_id=app.user_app_id)
    list_resp = app.STUB.ListDeployments(list_req, metadata=app.metadata)
    
    existing = next((d for d in list_resp.deployments if d.id == deployment_id), None)
    
    # 2. Delete if pointing to old version
    if existing:
        print(f"Deleting existing deployment {deployment_id}...")
        del_req = service_pb2.DeleteDeploymentsRequest(
            user_app_id=app.user_app_id, 
            ids=[deployment_id]
        )
        app.STUB.DeleteDeployments(del_req, metadata=app.metadata)
        time.sleep(2) # Stability pause

    # 3. Post new deployment with updated version
    deployment = resources_pb2.Deployment(
        id=deployment_id,
        worker=resources_pb2.Worker(
            model=resources_pb2.Model(
                id=model_id,
                model_version=resources_pb2.ModelVersion(id=version_id)
            )
        ),
        nodepools=[resources_pb2.Nodepool(id=nodepool_id)]
    )
    
    request = service_pb2.PostDeploymentsRequest(
        user_app_id=app.user_app_id,
        deployments=[deployment]
    )
    return app.STUB.PostDeployments(request, metadata=app.metadata)
```

## Version Tracking with Metadata

Always use the `metadata` field in `ModelVersion` to track the source of the deployment. This is visible in logs and via the API, making it clear which Git commit or branch is currently running in production.

### Setting Metadata during Upload

```python
version = resources_pb2.ModelVersion(
    metadata=resources_pb2.MetaData(
        fields={
            "git_commit": resources_pb2.Value(string_value="664cf8a..."),
            "git_branch": resources_pb2.Value(string_value="main"),
            "environment": resources_pb2.Value(string_value="production")
        }
    )
)
```

## Deployment States and Status Monitoring

Understanding the progression of a deployment is critical for automated workflows. You should always verify that a deployment is `READY` before attempting inference.

### Monitoring Readiness via SDK

The `create_deployment()` method in the `Nodepool` class handles waiting and log streaming by default via the `wait=True` argument.

```python
deployment = nodepool.create_deployment(config_filepath="config.yaml", wait=True)
# This will stream logs and only return once pods_running >= min_replicas 
# AND at least one log entry is received.
```

If you prefer to handle waiting manually (e.g., in a non-interactive script), set `wait=False` and use `runner_metrics()`:

```python
deployment = nodepool.deployment("my-deployment")

# Wait for readiness
while True:
    metrics = deployment.runner_metrics()
    if metrics["pods_running"] > 0:
        break
    print(f"Waiting for deployment... Total pods: {metrics['pods_total']}, Running: {metrics['pods_running']}")
    time.sleep(10)
```

### Manual Status Check (Runner Metrics)

If using the gRPC API directly, you must list the `Runners` for the specific `nodepool` and check their `runner_metrics` field. A deployment is considered ready when `pods_running >= 1`.

| State | Condition | Description |
| :--- | :--- | :--- |
| **READY** | `pods_running >= 1` | At least one pod is healthy and accepting traffic. |
| **INITIALIZING** | `pods_total >= 1` and `pods_running == 0` | Resources are assigned but pods are still starting up or pulling images. |
| **QUEUED** | `pods_total == 0` | No resources have been assigned by the scheduler yet. |

## Best Practices

*   **Atomic Updates**: Always name your deployments descriptively (e.g., `chatterbox-prod-v1`) to allow for blue-green deployments where you spin up a new version before deleting the old one.
*   **Wait for Stability**: After a `DeleteDeployments` call, wait at least 5 seconds before attempting to POST a deployment with the same ID to allow the platform to clear existing state.
*   **Scale Limits**: Use `AutoscaleConfig` to strictly control costs during development.
    ```python
    autoscale_config=resources_pb2.AutoscaleConfig(min_replicas=1, max_replicas=1)
    ```

## CLI Deployment Management

You can manage deployments directly via the CLI:
```bash
# List all deployments in a user account
clarifai deployment list

# List deployments for a specific nodepool
clarifai deployment list --nodepool_id <nodepool_id>

# List deployments for a specific compute cluster
clarifai deployment list --compute_cluster_id <compute_cluster_id>

# Delete a deployment
clarifai deployment delete <deployment_id>
```

### Creating a Deployment (`clarifai deployment create`)

To create a deployment via CLI, you must provide a `config.yaml` file that defines the deployment configuration.

```bash
clarifai deployment create --config deployment_config.yaml
```

**Wait and Log Behavior:**
When `min_replicas > 0`, the CLI will automatically:
1. Stream `runner` and `runner.events` logs to your terminal to provide visibility into the initialization or potential errors.
2. Wait and poll the deployment status until the number of running replicas reaches `min_replicas` **AND** at least one log entry has been received from the infrastructure.
3. Return only after a successful deployment is confirmed and initialized.

If `min_replicas` is 0, the CLI displays a warning and returns immediately, as actual infrastructure replicas will only be provisioned upon the first prediction request (Cold Start pattern).

#### Deployment Config Structure (`deployment_config.yaml`)

The configuration file follows a structured YAML format matching the `PostDeployments` request:

```yaml
deployment:
  id: "my-deployment-id" # Optional if provided as CLI argument
  user_id: "your-user-id" # Optional, defaults to current user
  worker:
    model: # Provide model OR workflow
      id: "model-id"
      model_version:
        id: "version-id"
      user_id: "model-owner-id"
      app_id: "app-id"
    # workflow:
    #   id: "workflow-id"
    #   app_id: "app-id"
    #   user_id: "user-id"
  nodepools:
    - id: "nodepool-id"
      compute_cluster:
        id: "cluster-id"
        user_id: "cluster-owner-id"
  autoscale_config: # Optional
    min_replicas: 1
    max_replicas: 5
    scale_to_zero_delay_seconds: 3600
  deploy_latest_version: true
```

## Automated Deployment Strategy

**Preferred approach:** Use `clarifai model deploy` which handles everything automatically:

```bash
# Simplest: auto-detects GPU from config.yaml
clarifai model deploy ./my-model

# Explicit GPU selection
clarifai model deploy ./my-model --instance gpu-nvidia-a10g
```

The deploy command automatically:
1. Searches for existing compute clusters and nodepools in the user's account
2. Creates deterministic cluster/nodepool IDs based on cloud/region/instance
3. Reuses existing infrastructure if it matches, creates new if not

**Manual fallback** (when `clarifai model deploy` isn't suitable):

1. **Browse instances**: `clarifai list-instances --cloud aws --gpu A10G`
2. **Resource Discovery**: List available `ComputeClusters` and `Nodepools` via SDK
3. **Heuristic Matching**: Compare model's `inference_compute_info` against available instance types
4. **Agent-Led Provisioning**: If no match, ask user before creating infrastructure
