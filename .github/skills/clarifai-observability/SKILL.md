---
name: clarifai-observability
description: Debug and monitor Clarifai resources (Runners and Pipelines). Use when a resource is stuck, crashing, or failing to build. Covers the CLI logs command, interpreting builder logs, runtime stdout/stderr, and infrastructure events to resolve scheduling and execution issues.
---

# Clarifai Observability & Debugging

Monitoring and debugging Clarifai resources happens across distinct log streams: Build, Infrastructure, and Runtime.

## CLI Log Commands (Recommended)

The fastest way to debug deployments is via the CLI:

```bash
# Stream model runtime logs (stdout/stderr) — follows by default
clarifai model logs --deployment <deployment-id>

# View K8s scheduling events (for startup/infrastructure issues)
clarifai model logs --deployment <deployment-id> --log-type events

# Print recent logs and exit (no follow)
clarifai model logs --deployment <deployment-id> --no-follow

# Check deployment status
clarifai model status --deployment <deployment-id>
```

> Use `--deployment <id>` when you have the deployment ID (from `clarifai model deploy` output).
> Use `--model-url <url>` when you don't know the deployment ID and need to discover it.

### Log Type Options

| CLI Flag | Log Type | Purpose |
|----------|----------|---------|
| `--log-type model` (default) | Runtime | Model stdout/stderr - Python tracebacks, OOM errors |
| `--log-type events` | Infrastructure | K8s events - scheduling delays, image pull, node taints |

## Log Stream Types

| Log Type | Scope | Purpose |
|----------|-------|---------|
| `builder` | Runner, Pipeline | Image build process. Check for `pip` failures or OS library conflicts. |
| `runner.events` | Runner | Infrastructure/K8s events. Check for scheduling delays, node taints, or image pull timeouts. |
| `runner` | Runner | Model runtime logic. Check for Python Tracebacks or OOM (Out of Memory). |
| `pipeline` | Pipeline | Pipeline execution logic. Check for step failures, artifact issues, or script errors. |

## Debugging Workflow

### 1. Check Deployment Status
```bash
clarifai model status --deployment <deployment-id>
```
Shows: enabled/disabled state, replicas (running/desired), instance type, GPU info, timing.

### 2. Check Infrastructure Events (Runners)
```bash
clarifai model logs --deployment <deployment-id> --log-type events
```
*   **"Successfully assigned"**: Pod has found a node.
*   **"Pulling image"**: Container is downloading.
*   **"FailedScheduling"**: Check if the nodepool has compatible instances (GPU type, memory).

### 3. Check Builder Logs (Pre-run)
If a resource fails to start, the build might have failed.
*   Look for `Done building image!!!`.
*   Search for `ERROR` in the builder logs for dependency conflicts.

### 4. Check Runtime Logs (Runtime)
```bash
clarifai model logs --deployment <deployment-id>
```
*   **TypeError/ValueError**: Usually an issue in the code or signature mapping.
*   **ModuleNotFoundError**: Dependency missing in `requirements.txt`.
*   **Killed**: Usually indicates OOM (Out of Memory). Increase compute resources in configuration.

## Python Snippet for Log Access

For programmatic access, use the `Deployment` object:

```python
from clarifai.client.deployment import Deployment

deployment = Deployment(deployment_id="my-deployment", user_id="user_id")

# Stream real-time "runner" logs (stdout/stderr)
for entry in deployment.logs(stream=True):
    print(entry.message, end="")

# Fetch build/infrastructure logs
for lt in ["builder", "runner.events"]:
    print(f"\n--- {lt} logs ---")
    for entry in deployment.logs(log_type=lt, stream=False, per_page=20):
        print(entry.message)
```

## Common Resolutions

*   **Infrastructure Delay**: If `runner.events` shows no nodes fit, check if the nodepool is scaled to 0 and needs a few minutes to spin up an instance. Use `clarifai list-instances` to verify available instance types.
*   **Code Change Persistence**: If you patch `model.py`, you **must** upload a new model version and update your deployment to use the new `version_id`. Use `clarifai model deploy` to re-deploy.
*   **Weights/Checkpoints**: Ensure your `load_model` logic uses paths relative to the checkpoint download directory (usually `1/checkpoints`).
