# SDK & CLI Reference

> This file contains both SDK methods (auto-generated) and CLI commands (curated).
> For SDK updates, run: `python scripts/generate_sdk_cli_reference.py`

---

## Part 1: SDK Methods

The following methods are available via `clarifai.client.*` classes.

```python
from clarifai.client import User, App, Model, Dataset, Inputs, Workflow, Pipeline, Search
```

### User

| Method | Description | Required | Optional |
|--------|-------------|----------|----------|
| `app` | Returns an App object for the specified app ID. | app_id | - |
| `compute_cluster` | Returns an Compute Cluster object for the specified compute cluster ID. | compute_cluster_id | - |
| `convert_string_to_timestamp` | Converts a string to a Timestamp object. | date_str | - |
| `create_app` | Creates an app for the user. | app_id | base_workflow |
| `create_compute_cluster` | Creates a compute cluster for the user. | - | config_filepath, compute_cluster_id, compute_cluster_config... |
| `create_secrets` | Creates secrets for the user. | secrets | - |
| `delete_app` | Deletes an app for the user. | app_id | - |
| `delete_compute_clusters` | Deletes a list of compute clusters for the user. | compute_cluster_ids | - |
| `delete_runner` | Deletes all spectified runner ids | runner_id | - |
| `delete_secrets` | Deletes a list of secrets for the user. | secret_ids | - |
| `get_secret` | Returns a secret object if exists. | secret_id | - |
| `get_user_info` | Returns the user information for the specified user ID. | - | user_id |
| `list_apps` | Lists all the apps for the user. | - | filter_by, page_no, per_page... |
| `list_compute_clusters` | List all compute clusters for the user | - | page_no, per_page |
| `list_models` |  | - | user_id, app_id, show... |
| `list_pages_generator` | Lists pages of a resource. | endpoint, proto_message, request_data | page_no, per_page |
| `list_pipeline_steps` | List all pipeline steps for the user across all apps | - | page_no, per_page |
| `list_pipelines` | List all pipelines for the user across all apps | - | page_no, per_page |
| `list_runners` | List all runners for the user | - | filter_by, page_no, per_page... |
| `list_secrets` | List all secrets for the user | - | page_no, per_page |
| `patch_app` | Patch an app for the user. | app_id | action |
| `patch_secrets` | Patches secrets for the user. | secrets | action |
| `process_response_keys` | Converts keys in a response dictionary to resource proto format. | old_dict | listing_resource |
| `runner` | Returns a Runner object if exists. | runner_id | - |
| `get_secret` | Returns a secret object by ID. | secret_id | - |
| `list_secrets` | List all secrets for the user. | - | page_no, per_page |
| `create_secrets` | Creates secrets for the user. | secrets | - |
| `patch_secrets` | Updates secrets for the user. | secrets | action |
| `delete_secrets` | Deletes a list of secrets. | secret_ids | - |
| `list_cloud_providers` | List available cloud providers. | - | - |
| `list_cloud_regions` | List regions for a cloud provider. | cloud_provider_id | - |
| `list_instance_types` | List instance types for a region. | cloud_provider_id, region_id | - |

### App

| Method | Description | Required | Optional |
|--------|-------------|----------|----------|
| `convert_string_to_timestamp` | Converts a string to a Timestamp object. | date_str | - |
| `create_concept_relations` | Creates concept relations between concepts of the app. | subject_concept_id, object_concept_ids, predicates | - |
| `create_concepts` | Add concepts to the app. | concept_ids | concepts |
| `create_dataset` | Creates a dataset for the app. | dataset_id | - |
| `create_model` | Creates a model for the app. | model_id | - |
| `create_module` | Creates a module for the app. | module_id, description | - |
| `create_workflow` | Creates a workflow for the app. | config_filepath | generate_new_id, display |
| `dataset` | Returns a Dataset object for the existing dataset ID. | dataset_id | dataset_version_id |
| `delete_concept_relations` | Delete concept relations of a concept of the app. | concept_id | concept_relation_ids |
| `delete_dataset` | Deletes an dataset for the user. | dataset_id | - |
| `delete_model` | Deletes an model for the user. | model_id | - |
| `delete_module` | Deletes an module for the user. | module_id | - |
| `delete_workflow` | Deletes an workflow for the user. | workflow_id | - |
| `get_input_count` | Get count of all the inputs in the app. | - | - |
| `inputs` | Returns an Input object. | - | - |
| `list_concepts` | Lists all the concepts for the app. | - | page_no, per_page |
| `list_datasets` | Lists all the datasets for the app. | - | page_no, per_page |
| `list_installed_module_versions` | Lists all installed module versions in the app. | - | filter_by, page_no, per_page... |
| `list_models` | Lists all the available models for the user. | - | filter_by, only_in_app, page_no... |
| `list_modules` | Lists all the available modules for the user. | - | filter_by, only_in_app, page_no... |
| `list_pages_generator` | Lists pages of a resource. | endpoint, proto_message, request_data | page_no, per_page |
| `list_pipeline_steps` | Lists all the pipeline steps for the user. | - | pipeline_id, filter_by, only_in_app... |
| `list_pipelines` | Lists all the pipelines for the user. | - | filter_by, only_in_app, page_no... |
| `list_trainable_model_types` | Lists all the trainable model types. | - | - |
| `list_workflows` | Lists all the available workflows for the user. | - | filter_by, only_in_app, page_no... |
| `model` | Returns a Model object for the existing model ID. | model_id | model_version |
| `module` | Returns a Module object for the existing module ID. | module_id | - |
| `patch_dataset` | Patches a dataset for the app. | dataset_id | action |
| `patch_model` | Patches a model of the app. | model_id | action |
| `patch_workflow` | Patches a workflow of the app. | workflow_id | action, config_filepath |
| `process_response_keys` | Converts keys in a response dictionary to resource proto format. | old_dict | listing_resource |
| `search` | Returns a Search object for the user and app ID. | - | - |
| `search_concept_relations` | List all the concept relations of the app. | - | concept_id, predicate, page_no... |
| `workflow` | Returns a workflow object for the existing workflow ID. | workflow_id | - |

### Model

| Method | Description | Required | Optional |
|--------|-------------|----------|----------|
| `async_generate` | Calls the model's async generate() method with the given arguments. | - | - |
| `async_predict` | Calls the model's async predict() method with the given arguments. | - | - |
| `async_stream` | Calls the model's async stream() method with the given arguments. | - | - |
| `convert_string_to_timestamp` | Converts a string to a Timestamp object. | date_str | - |
| `create_version` | Creates a model version for the Model. | - | - |
| `create_version_by_file` | Create model version by uploading local file | file_path, input_field_maps, output_field_maps | inference_parameter_configs, model_version, part_id... |
| `create_version_by_url` | Upload a new version of an existing model in the Clarifai platform using direct  | url, input_field_maps, output_field_maps | inference_parameter_configs, description |
| `delete_version` | Deletes a model version for the Model. | version_id | - |
| `evaluate` | Run evaluation | - | dataset, dataset_id, dataset_app_id... |
| `export` | Export the model, stores the exported model as model.tar file | - | export_dir |
| `generate` | Calls the model's generate() method with the given arguments. | - | - |
| `generate_by_bytes` | Generate the stream output on model based on the given bytes. | input_bytes | input_type, inference_params, output_config... |
| `generate_by_filepath` | Generate the stream output on model based on the given filepath. | filepath | input_type, inference_params, output_config... |
| `generate_by_url` | Generate the stream output on model based on the given URL. | url | input_type, inference_params, output_config... |
| `get_eval_by_dataset` | Get all eval data of dataset | dataset | - |
| `get_eval_by_id` | Get detail eval_metrics by eval_id with extra metric fields | eval_id | label_counts, test_set, binary_metrics... |
| `get_latest_eval` | Run `get_eval_by_id` method with latest `eval_id` | - | label_counts, test_set, binary_metrics... |
| `get_param_info` | Returns the parameter info for the specified parameter. | param | - |
| `get_params` | Returns the model params for the model type and saves them to a yaml file. | - | template, save_to |
| `get_raw_eval` | Get ground truths, predictions and input information. Do not pass dataset and ev | - | dataset, eval_id, return_format... |
| `list_evaluations` | List all eval_metrics of current model version | - | - |
| `list_pages_generator` | Lists pages of a resource. | endpoint, proto_message, request_data | page_no, per_page |
| `list_training_templates` | Lists all the training templates for the model type. | - | - |
| `list_versions` | Lists all the versions for the model. | - | page_no, per_page |
| `load_input_types` | Loads the input types for the model. | - | - |
| `patch_version` | Patch the model version with the given version ID. | version_id | - |
| `predict` | Calls the model's predict() method with the given arguments. | - | - |
| `predict_by_bytes` | Predicts the model based on the given bytes. | input_bytes | input_type, inference_params, output_config... |
| `predict_by_filepath` | Predicts the model based on the given filepath. | filepath | input_type, inference_params, output_config... |
| `predict_by_url` | Predicts the model based on the given URL. | url | input_type, inference_params, output_config... |
| `process_response_keys` | Converts keys in a response dictionary to resource proto format. | old_dict | listing_resource |
| `stream` | Calls the model's stream() method with the given arguments. | - | - |
| `stream_by_bytes` | Stream the model output based on the given bytes. | input_bytes_iterator | input_type, inference_params, output_config... |
| `stream_by_filepath` | Stream the model output based on the given filepath. | filepath | input_type, inference_params, output_config... |
| `stream_by_url` | Stream the model output based on the given URL. | url_iterator | input_type, inference_params, output_config... |
| `train` | Trains the model based on the given yaml file or model params. | - | yaml_file |
| `training_status` | Get the training status for the model version. Also stores training logs | - | version_id, training_logs |
| `update_params` | Updates the model params for the model. | - | - |

### Dataset

| Method | Description | Required | Optional |
|--------|-------------|----------|----------|
| `archive_zip` | Exports the dataset to a zip file URL. | - | wait |
| `convert_string_to_timestamp` | Converts a string to a Timestamp object. | date_str | - |
| `create_version` | Creates a dataset version for the Dataset. | - | - |
| `delete_version` | Deletes a dataset version for the Dataset. | version_id | - |
| `export` | Exports the Clarifai protobuf dataset to a local archive. | save_path | archive_url, local_archive_path, split... |
| `get_upload_status` | Creates a new dataset version and displays the upload status of the dataset. | - | dataloader, delete_version, timeout... |
| `list_inputs` | Lists all the inputs for the dataset. | - | page_no, per_page, input_type... |
| `list_pages_generator` | Lists pages of a resource. | endpoint, proto_message, request_data | page_no, per_page |
| `list_versions` | Lists all the versions for the dataset. | - | page_no, per_page |
| `merge_dataset` | Merges the another dataset into current dataset. | merge_dataset_id | - |
| `process_response_keys` | Converts keys in a response dictionary to resource proto format. | old_dict | listing_resource |
| `retry_upload_from_logs` | Retries failed uploads from the log file. | log_file_path, dataloader | retry_duplicates, log_warnings |
| `upload_dataset` | Uploads a dataset to the app. | dataloader | batch_size, get_upload_status, log_warnings... |
| `upload_from_csv` | Uploads dataset from a csv file. | csv_path | input_type, csv_type, labels... |
| `upload_from_folder` | Upload dataset from folder. | folder_path, input_type | labels, batch_size |

### Inputs

| Method | Description | Required | Optional |
|--------|-------------|----------|----------|
| `convert_string_to_timestamp` | Converts a string to a Timestamp object. | date_str | - |
| `delete_annotations` | Delete list of annotations of input objects from the app. | input_ids | annotation_ids |
| `delete_inputs` | Delete list of input objects from the app. | inputs | - |
| `download_inputs` | Download list of input objects from the app. | inputs | - |
| `get_bbox_proto` | Create an annotation proto for each bounding box, label input pair. | input_id, label, bbox | label_id, annot_id |
| `get_image_inputs_from_folder` | Create input protos for image data type from folder. | folder_path | dataset_id, labels |
| `get_input` | Get Input object of input with input_id provided from the app. | input_id | - |
| `get_input_from_bytes` | Create input proto from bytes. | input_id | image_bytes, video_bytes, audio_bytes... |
| `get_input_from_file` | Create input proto from files. | input_id | image_file, video_file, audio_file... |
| `get_input_from_url` | Create input proto from url. | input_id | image_url, video_url, audio_url... |
| `get_inputs_from_csv` | Create input protos from csv. | csv_path | input_type, csv_type, dataset_id... |
| `get_mask_proto` | Create an annotation proto for each polygon box, label input pair. | input_id, label, polygons | label_id, annot_id |
| `get_multimodal_input` | Create input proto for text and image from bytes or url. | input_id | raw_text, text_bytes, image_url... |
| `get_text_input` | Create input proto for text data type from raw text. | input_id, raw_text | dataset_id |
| `get_text_inputs_from_folder` | Create input protos for text data type from folder. | folder_path | dataset_id, labels |
| `list_annotations` | Lists all the annotations for the app. | - | batch_input, page_no, per_page... |
| `list_inputs` | Lists all the inputs for the app. | - | dataset_id, page_no, per_page... |
| `list_pages_generator` | Lists pages of a resource. | endpoint, proto_message, request_data | page_no, per_page |
| `patch_annotations` | Patch image annotations to app. | batch_annot | action |
| `patch_concepts` | Patch concepts to app. | concept_ids | labels, values, action... |
| `patch_inputs` | Patch list of input objects to the app. | inputs | action |
| `process_response_keys` | Converts keys in a response dictionary to resource proto format. | old_dict | listing_resource |
| `upload_annotations` | Upload image annotations to app. | batch_annot | show_log |
| `upload_from_bytes` | Upload input from bytes. | input_id | image_bytes, video_bytes, audio_bytes... |
| `upload_from_file` | Upload input from file. | input_id | image_file, video_file, audio_file... |
| `upload_from_url` | Upload input from url. | input_id | image_url, video_url, audio_url... |
| `upload_inputs` | Upload list of input objects to the app. | inputs | show_log |
| `upload_text` | Upload text from raw text. | input_id, raw_text | dataset_id |

### Workflow

| Method | Description | Required | Optional |
|--------|-------------|----------|----------|
| `convert_string_to_timestamp` | Converts a string to a Timestamp object. | date_str | - |
| `export` | Exports the workflow to a yaml file. | out_path | - |
| `list_pages_generator` | Lists pages of a resource. | endpoint, proto_message, request_data | page_no, per_page |
| `list_versions` | Lists all the versions of the workflow. | - | page_no, per_page |
| `predict` | Predicts the workflow based on the given inputs. | inputs | workflow_state_id |
| `predict_by_bytes` | Predicts the workflow based on the given bytes. | input_bytes | input_type |
| `predict_by_filepath` | Predicts the workflow based on the given filepath. | filepath | input_type |
| `predict_by_url` | Predicts the workflow based on the given URL. | url | input_type |
| `process_response_keys` | Converts keys in a response dictionary to resource proto format. | old_dict | listing_resource |

### Pipeline

| Method | Description | Required | Optional |
|--------|-------------|----------|----------|
| `convert_string_to_timestamp` | Converts a string to a Timestamp object. | date_str | - |
| `list_pages_generator` | Lists pages of a resource. | endpoint, proto_message, request_data | page_no, per_page |
| `monitor_only` | Monitor an existing pipeline run without starting a new one. | - | timeout, monitor_interval |
| `patch_pipeline_version_run` | Patch a pipeline version run's orchestration status. | pipeline_version_run_id, orchestration_status_code | - |
| `process_response_keys` | Converts keys in a response dictionary to resource proto format. | old_dict | listing_resource |
| `run` | Run the pipeline and monitor its progress. | - | inputs, timeout, monitor_interval... |

### Search

| Method | Description | Required | Optional |
|--------|-------------|----------|----------|
| `convert_string_to_timestamp` | Converts a string to a Timestamp object. | date_str | - |
| `list_pages_generator` | Lists pages of a resource. | endpoint, proto_message, request_data | page_no, per_page |
| `process_response_keys` | Converts keys in a response dictionary to resource proto format. | old_dict | listing_resource |
| `query` | Perform a query with rank and filters. | - | ranks, filters, page_no... |

---

## Part 2: CLI Commands

### Quick Command Reference

| Task | Command |
|------|---------|
| Login | `clarifai login` |
| Initialize model | `clarifai model init` |
| Init from toolkit | `clarifai model init --toolkit vllm` |
| Init MCP server | `clarifai model init --toolkit mcp` |
| Upload model | `clarifai model upload ./model` |
| Serve locally | `clarifai model serve ./model` |
| Serve as gRPC | `clarifai model serve ./model --grpc --port 8000` |
| Deploy to cloud | `clarifai model deploy ./model` |
| Deploy with GPU | `clarifai model deploy ./model --instance gpu-nvidia-a10g` |
| Check status | `clarifai model status --deployment <id>` |
| Stream logs | `clarifai model logs --deployment <id>` |
| Undeploy | `clarifai model undeploy --deployment <id>` |
| Predict | `clarifai model predict <model_ref> "Hello!"` |
| List models | `clarifai model list` |
| List GPU instances | `clarifai list-instances` |
| Init pipeline | `clarifai pipeline init` |
| Init from template | `clarifai pipeline init --template classifier-pipeline-resnet` |
| Upload pipeline | `clarifai pipeline upload` |
| Run pipeline | `clarifai pipeline run --compute_cluster_id <id> --nodepool_id <id>` |
| List pipelines | `clarifai pipeline list` |
| List templates | `clarifai pipelinetemplate list` |

### Use Case Routing

| User Request | Primary Command | Follow-up |
|--------------|-----------------|-----------|
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
| "Deploy to cloud" | `clarifai model deploy ./model` | Auto-creates infra |
| "Check deployment" | `clarifai model status --deployment <id>` | Use `--model-url` to discover |
| "View logs" | `clarifai model logs --deployment <id>` | Follows by default |
| "Remove deployment" | `clarifai model undeploy --deployment <id>` | |
| "Browse GPUs" | `clarifai list-instances` | |

---

## Model Commands

### clarifai model init

Initialize a new model directory structure.

**Usage:**
```bash
clarifai model init [MODEL_PATH] [OPTIONS]
```

**Arguments:**
- `MODEL_PATH` - Path where to create the model directory. Default: current directory

**Options:**
| Option | Values | Description |
|--------|--------|-------------|
| `--toolkit` | `vllm`, `sglang`, `huggingface`, `ollama`, `lmstudio`, `mcp`, `openai`, `python` | Initialize from toolkit template |
| `--model-name` | string | Model checkpoint (HF repo_id or ollama tag). Auto-creates directory from name |
| `--streaming-video` | flag | Enable streaming video consumer (adds ffmpeg/av to Dockerfile) |

**Examples:**
```bash
# Initialize basic model (blank Python template)
clarifai model init ./my-model

# Initialize vLLM model with specific HuggingFace model
clarifai model init ./my-vllm-model --toolkit vllm --model-name "Qwen/Qwen3-4B-Instruct-2507"

# Initialize SGLang model
clarifai model init ./my-sglang-model --toolkit sglang --model-name "unsloth/Llama-3.2-1B-Instruct"

# Initialize HuggingFace transformers model
clarifai model init ./my-hf-model --toolkit huggingface --model-name "meta-llama/Llama-3.2-1B-Instruct"

# Initialize Ollama model
clarifai model init ./my-ollama-model --toolkit ollama --model-name "llama3.1"

# Initialize MCP server
clarifai model init ./my-mcp-server --toolkit mcp

# Initialize OpenAI-compatible wrapper
clarifai model init ./my-openai-wrapper --toolkit openai

# Initialize custom Python model
clarifai model init ./my-custom-model --toolkit python
```

**Created Structure:**
```
model/
├── 1/
│   └── model.py          # ModelClass implementation
├── requirements.txt      # Python dependencies
└── config.yaml          # Clarifai configuration
```

### clarifai model upload

Upload a model to Clarifai platform (build only, no deployment).

**Usage:**
```bash
clarifai model upload [MODEL_PATH] [OPTIONS]
```

**Options:**
| Option | Values | Description |
|--------|--------|-------------|
| `--platform` | string | Target Docker platform (e.g., "linux/amd64") |
| `--verbose` | flag | Show detailed build and upload logs |

**Examples:**
```bash
# Upload model from current directory
clarifai model upload

# Upload model from specific path
clarifai model upload ./my-model

# Upload for specific platform with verbose logs
clarifai model upload ./my-model --platform "linux/amd64" --verbose
```

### clarifai model serve

Run model locally for development and testing. This is the **recommended** command for local testing, replacing the legacy `local-runner`, `local-grpc`, and `local-test` commands.

**Usage:**
```bash
clarifai model serve [MODEL_PATH] [OPTIONS]
```

**Options:**
| Option | Values | Description |
|--------|--------|-------------|
| `--mode` | `none`, `env`, `container` | Execution environment (default: none) |
| `--grpc` | flag | Run as standalone gRPC server (no login required) |
| `--port` | number | Server port when using `--grpc` (default: 8000) |
| `--concurrency` | number | Maximum concurrent requests (default: 32) |
| `--keep-image` | flag | Keep Docker image after exit (container mode) |
| `--keep` | flag | Keep API resources (version, runner, deployment) across restarts |
| `--verbose` | flag | Show detailed SDK and server logs |

**Modes:**
- `none` (default): Use current Python environment (fastest, deps must be pre-installed)
- `env`: Auto-create virtualenv and install deps from requirements.txt
- `container`: Build Docker image with all deps (production-like)

**Examples:**
```bash
# Fastest local test (use current Python env)
clarifai model serve ./my-model

# Run in isolated virtualenv
clarifai model serve ./my-model --mode env

# Run in Docker container (production-like)
clarifai model serve ./my-model --mode container

# Standalone gRPC server (no Clarifai login needed)
clarifai model serve ./my-model --grpc --port 8000

# Keep resources for faster restarts during development
clarifai model serve ./my-model --keep
```

### clarifai model deploy

Upload, build, and deploy a model in one step with zero interactive prompts. Automatically creates compute infrastructure (cluster + nodepool) if needed.

**Usage:**
```bash
clarifai model deploy [MODEL_PATH] [OPTIONS]
```

**Arguments:**
- `MODEL_PATH` - Local model directory to upload. Omit if using `--model-url`

**Options:**
| Option | Values | Description |
|--------|--------|-------------|
| `--instance` | string | Hardware instance type. Accepts: GPU shorthand (`A10G`, `L40S`), nodepool-style (`gpu-nvidia-a10g`), or cloud instance IDs (`g5.xlarge`). Use `clarifai list-instances` to browse |
| `--model-url` | URL | Deploy an already-uploaded model by URL |
| `--model-version-id` | string | Specific model version to deploy |
| `--min-replicas` | int | Minimum running replicas (default: 1) |
| `--max-replicas` | int | Maximum replicas for autoscaling (default: 5) |
| `--cloud` | `aws`, `gcp`, `vultr`, `azure` | Cloud provider (auto-detected from instance) |
| `--region` | string | Cloud region (auto-detected from instance) |
| `--compute-cluster-id` | string | Use existing compute cluster (advanced) |
| `--nodepool-id` | string | Use existing nodepool (advanced) |
| `--verbose` | flag | Show detailed logs |

**Examples:**
```bash
# Deploy from local directory (auto-selects GPU from config.yaml)
clarifai model deploy ./my-model

# Deploy with specific GPU instance
clarifai model deploy ./my-model --instance gpu-nvidia-a10g

# Deploy an already-uploaded model
clarifai model deploy --model-url "https://clarifai.com/user/app/models/my-model"

# Deploy with specific version and scaling
clarifai model deploy --model-url <url> --model-version-id abc123 \
  --min-replicas 2 --max-replicas 10

# Deploy to specific cloud/region
clarifai model deploy ./my-model --instance gpu-nvidia-a10g --cloud aws --region us-east-1
```

### clarifai model status

Show deployment status for a model.

**Usage:**
```bash
clarifai model status [MODEL_REF] [OPTIONS]
```

**Arguments:**
- `MODEL_REF` - Model reference as `user_id/app_id/models/model_id` (optional)

**Options:**
| Option | Description |
|--------|-------------|
| `--model-url` | Full model URL (alternative to positional arg) |
| `--deployment` | Specific deployment ID |

**When to use which flag:**
- `--deployment <id>` — When you have the deployment ID (printed by `clarifai model deploy`). Direct lookup.
- `--model-url <url>` — When you don't know the deployment ID. Lists all deployments for that model.

**Examples:**
```bash
# Check by deployment ID (fastest — direct lookup)
clarifai model status --deployment my-deployment

# Check by model URL (discovers all deployments for this model)
clarifai model status --model-url "https://clarifai.com/user/app/models/my-model"

# Check by model reference
clarifai model status user/app/models/my-model
```

**Output includes:** enabled/disabled state, replicas (running/desired), instance type, GPU info, nodepool, cluster, timing.

### clarifai model logs

Stream logs from a deployed model's runner.

**Usage:**
```bash
clarifai model logs [OPTIONS]
```

**Options:**
| Option | Values | Description |
|--------|--------|-------------|
| `--model-url` | URL | Model URL |
| `--model-id` | string | Model ID |
| `--deployment` | string | Deployment ID |
| `--model-version-id` | string | Model version ID |
| `--follow/--no-follow` | flag | Follow logs in real-time (default: enabled). Use `--no-follow` to print and exit |
| `--duration` | int | Stop after N seconds (default: unlimited, Ctrl+C to stop) |
| `--log-type` | `model`, `events` | Log type (default: model) |
| `--compute-cluster-id` | string | Compute cluster ID |
| `--nodepool-id` | string | Nodepool ID |

**Examples:**
```bash
# Stream logs by deployment ID (from deploy output)
clarifai model logs --deployment my-deployment

# Stream logs by model URL (discovers deployment automatically)
clarifai model logs --model-url <url>

# View K8s scheduling events (for debugging startup issues)
clarifai model logs --deployment my-deployment --log-type events

# Print recent logs and exit (no follow)
clarifai model logs --deployment my-deployment --no-follow

# Stop after 60 seconds
clarifai model logs --deployment my-deployment --duration 60
```

### clarifai model undeploy

Remove a deployment (stop serving the model). The model version and infrastructure remain intact.

**Usage:**
```bash
clarifai model undeploy [MODEL_REF] [OPTIONS]
```

**Arguments:**
- `MODEL_REF` - Model reference as `user_id/app_id/models/model_id` (optional)

**Options:**
| Option | Description |
|--------|-------------|
| `--model-url` | Full model URL (alternative to positional arg) |
| `--deployment` | Specific deployment ID |

**Examples:**
```bash
# Undeploy by deployment ID
clarifai model undeploy --deployment my-deployment

# Undeploy by model URL (if you don't know the deployment ID)
clarifai model undeploy --model-url "https://clarifai.com/user/app/models/my-model"
```

### clarifai model predict

Run predictions against a Clarifai model. Supports positional args, named inputs, JSON, files, URLs, and OpenAI chat format.

**Usage:**
```bash
clarifai model predict [MODEL_REF] [TEXT_INPUT] [OPTIONS]
```

**Arguments:**
- `MODEL_REF` - Model reference: `user_id/app_id/models/model_id` or full URL (optional if `--model-url` used)
- `TEXT_INPUT` - Text input for text models (optional)

**Options:**
| Option | Description |
|--------|-------------|
| `--model-url` | Full model URL (alternative to positional MODEL_REF) |
| `-i`, `--input` | Named parameter as `key=value` (repeatable) |
| `--inputs` | All parameters as JSON string |
| `--file` | Input file (image, audio, video) |
| `--url` | Input URL (image, audio, video) |
| `--chat` | OpenAI chat message (auto-uses OpenAI client) |
| `--method` | Method to call (overrides auto-selection) |
| `--info` | Show available methods and signatures, then exit |
| `-o`, `--output` | Output format: `text` (default) or `json` |
| `--deployment` | Route to specific deployment |

**Examples:**
```bash
# Simple text prediction (positional args)
clarifai model predict anthropic/completion/models/claude-sonnet-4 "Hello!"

# Named parameters
clarifai model predict --model-url <url> -i prompt="Hello" -i max_tokens=100

# JSON inputs
clarifai model predict --model-url <url> --inputs '{"prompt": "Hello"}'

# Image file input
clarifai model predict --model-url <url> --file ./image.jpg

# OpenAI chat format
clarifai model predict --model-url <url> --chat "What is AI?"

# Show model info (methods + signatures)
clarifai model predict --model-url <url> --info

# Pipe from stdin
echo "Hello" | clarifai model predict --model-url <url>

# With specific deployment
clarifai model predict --model-url <url> --deployment my-deployment -i prompt="Hello"
```

### clarifai model list

List models.

**Usage:**
```bash
clarifai model list [USER_ID] [OPTIONS]
```

**Arguments:**
- `USER_ID` - User ID (default: current user, use "all" for all public models)

**Options:**
| Option | Description |
|--------|-------------|
| `--app_id`, `-a` | Filter by app ID |

**Examples:**
```bash
# List your models
clarifai model list

# List models in specific app
clarifai model list --app_id myapp

# List all public models
clarifai model list all
```

### clarifai model download-checkpoints

Download model checkpoints from external sources.

**Usage:**
```bash
clarifai model download-checkpoints [MODEL_PATH] [OPTIONS]
```

**Options:**
| Option | Values | Description |
|--------|--------|-------------|
| `--out_path` | path | Output path for checkpoints |
| `--stage` | `runtime`, `build`, `upload` | Download stage (default: build) |

**Examples:**
```bash
# Download checkpoints for build
clarifai model download-checkpoints ./my-model --stage build

# Download to specific path
clarifai model download-checkpoints ./my-model --out_path ./checkpoints
```

### clarifai model signatures

Generate model method signatures.

**Usage:**
```bash
clarifai model signatures [MODEL_PATH] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--out_path` | Output file path (default: stdout) |

**Examples:**
```bash
# Print signatures to console
clarifai model signatures ./my-model

# Save to file
clarifai model signatures ./my-model --out_path signatures.yaml
```

---

## Pipeline Commands

### clarifai pipeline init

Initialize a new pipeline project.

**Usage:**
```bash
clarifai pipeline init [PIPELINE_PATH] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--template` | Initialize from template (e.g., classifier-pipeline-resnet, detector-pipeline-yolof) |

**Examples:**
```bash
# Interactive initialization
clarifai pipeline init ./my-pipeline

# Initialize from ResNet training template
clarifai pipeline init ./classifier --template classifier-pipeline-resnet

# Initialize from YOLOF detector template
clarifai pipeline init ./detector --template detector-pipeline-yolof
```

**Created Structure:**
```
pipeline/
├── config.yaml          # Pipeline configuration
├── stepA/               # First step
│   ├── config.yaml
│   ├── requirements.txt
│   └── 1/
│       └── pipeline_step.py
├── stepB/               # Second step
│   └── ...
└── README.md
```

### clarifai pipeline upload

Upload a pipeline to Clarifai.

**Usage:**
```bash
clarifai pipeline upload [PATH] [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--no-lockfile` | Skip creating config-lock.yaml |

**Examples:**
```bash
# Upload pipeline from current directory
clarifai pipeline upload

# Upload from specific path
clarifai pipeline upload ./my-pipeline
```

### clarifai pipeline run

Run a pipeline and monitor progress.

**Usage:**
```bash
clarifai pipeline run [OPTIONS]
```

**Required Options:**
| Option | Description |
|--------|-------------|
| `--compute_cluster_id` | Compute cluster ID (REQUIRED) |
| `--nodepool_id` | Nodepool ID (REQUIRED) |

**Pipeline Identification (one required):**
| Option | Description |
|--------|-------------|
| `--pipeline_url` | Full pipeline URL |
| `--pipeline_id` + `--user_id` + `--app_id` + `--pipeline_version_id` | Individual IDs |

**Additional Options:**
| Option | Description |
|--------|-------------|
| `--config` | Path to config file |
| `--timeout` | Max wait time in seconds (default: 3600) |
| `--monitor_interval` | Status check interval (default: 10) |
| `--log_file` | Path for log output |
| `--monitor` | Monitor existing run (requires pipeline_version_run_id) |
| `--set` | Override parameters inline (e.g., --set key=value) |
| `--overrides-file` | JSON/YAML file with parameter overrides |

**Examples:**
```bash
# Run pipeline with config-lock.yaml (auto-detected)
clarifai pipeline run --compute_cluster_id cc-123 --nodepool_id np-456

# Run with explicit pipeline URL
clarifai pipeline run \
  --pipeline_url "https://clarifai.com/user/app/pipelines/my-pipeline/versions/v1" \
  --compute_cluster_id cc-123 \
  --nodepool_id np-456

# Run with parameter overrides
clarifai pipeline run \
  --compute_cluster_id cc-123 \
  --nodepool_id np-456 \
  --set epochs=10 \
  --set batch_size=32

# Monitor existing run
clarifai pipeline run \
  --compute_cluster_id cc-123 \
  --nodepool_id np-456 \
  --pipeline_version_run_id run-789 \
  --monitor
```

### clarifai pipeline list

List pipelines.

**Usage:**
```bash
clarifai pipeline list [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--page_no` | Page number (default: 1) |
| `--per_page` | Items per page (default: 16) |
| `--app_id` | Filter by app ID |

**Examples:**
```bash
# List all pipelines
clarifai pipeline list

# List pipelines in specific app
clarifai pipeline list --app_id myapp
```

---

## Pipeline Template Commands

### clarifai pipelinetemplate list

List available pipeline templates.

**Usage:**
```bash
clarifai pipelinetemplate list
```

**Available Templates:**
| Template | Description |
|----------|-------------|
| `classifier-pipeline-resnet` | ResNet-50 image classification training |
| `detector-pipeline-yolof` | YOLOF object detection training |

### clarifai pipelinetemplate info

Get information about a specific template.

**Usage:**
```bash
clarifai pipelinetemplate info <template_name>
```

**Examples:**
```bash
clarifai pipelinetemplate info classifier-pipeline-resnet
```

---

## Pipeline Run Commands

### clarifai pipelinerun monitor

Monitor a pipeline run.

**Usage:**
```bash
clarifai pipelinerun monitor <run_id> [OPTIONS]
```

### clarifai pipelinerun pause / resume / cancel

Control pipeline execution.

**Usage:**
```bash
clarifai pipelinerun pause <run_id>
clarifai pipelinerun resume <run_id>
clarifai pipelinerun cancel <run_id>
```

---

## Pipeline Step Commands

### clarifai pipelinestep init

Initialize a new pipeline step.

**Usage:**
```bash
clarifai pipelinestep init [STEP_PATH] [OPTIONS]
```

---

## Authentication Commands

### clarifai login

Login to Clarifai CLI.

**Usage:**
```bash
clarifai login
```

This creates or updates your CLI context with your PAT (Personal Access Token).

### clarifai config

Manage CLI configuration contexts.

**Usage:**
```bash
clarifai config ls                     # List all contexts (aliases: list-contexts, get-contexts)
clarifai config current                # Show current context
clarifai config use <context_name>     # Switch active context
clarifai config create <context_name>  # Create new context
clarifai config delete <context_name>  # Delete a context
clarifai config show                   # Display current config
clarifai config env                    # Print env vars for active context
```

---

## Compute Discovery Commands

### clarifai list-instances

List available compute instance types across all cloud providers. Alias: `clarifai li`.

**Usage:**
```bash
clarifai list-instances [OPTIONS]
```

**Options:**
| Option | Values | Description |
|--------|--------|-------------|
| `--cloud` | `aws`, `gcp`, `vultr`, `azure` | Filter by cloud provider |
| `--region` | string | Filter by region (e.g., `us-east-1`, `us-central1`) |
| `--gpu` | string | Filter by GPU name (e.g., `A10G`, `H100`, `L40S`) |
| `--min-gpus` | int | Minimum GPU count |
| `--min-gpu-mem` | string | Minimum GPU memory (e.g., `80Gi`, `48Gi`) |

**Examples:**
```bash
# List all available instances
clarifai list-instances

# Filter by cloud provider
clarifai list-instances --cloud aws

# Find specific GPU across all clouds
clarifai list-instances --gpu A10G

# Find instances with at least 80Gi GPU memory
clarifai list-instances --min-gpu-mem 80Gi

# Combine filters
clarifai list-instances --cloud gcp --min-gpus 2 --min-gpu-mem 48Gi
```

---

## Compute Orchestration Commands

### clarifai computecluster

Manage compute clusters.

**Usage:**
```bash
clarifai computecluster list
clarifai computecluster create <cluster_id>
clarifai computecluster delete <cluster_id>
```

**Example (cleanup for local-runner):**
```bash
clarifai computecluster delete local-runner-compute-cluster
```

### clarifai nodepool

Manage nodepools within compute clusters.

**Usage:**
```bash
clarifai nodepool list --compute_cluster_id <id>
clarifai nodepool create <nodepool_id> --compute_cluster_id <id>
clarifai nodepool delete <nodepool_id> --compute_cluster_id <id>
```

### clarifai deployment

Manage model deployments.

**Usage:**
```bash
clarifai deployment list [--nodepool_id <id>] [--compute_cluster_id <id>]
clarifai deployment create
clarifai deployment delete <deployment_id>
```

---

## Artifact Commands

Manage pipeline artifacts for storing checkpoints, logs, models, and other files between pipeline steps.

### clarifai artifact list

List artifacts in an app or versions of an artifact.

```bash
# List all artifacts in an app
clarifai artifact list users/<user_id>/apps/<app_id>
clarifai af ls users/<user_id>/apps/<app_id>

# List versions of a specific artifact
clarifai artifact list users/<user_id>/apps/<app_id>/artifacts/<artifact_id> --versions
```

### clarifai artifact cp (upload/download)

Upload or download artifact files.

**Upload:**
```bash
# Basic upload
clarifai artifact cp ./model.pt users/<user_id>/apps/<app_id>/artifacts/<artifact_id>
clarifai af cp ./weights.safetensors users/u/apps/a/artifacts/model

# Upload with options
clarifai artifact cp ./model.pt users/u/apps/a/artifacts/model \
  --description="Production model v2.0" \
  --visibility=public
```

**Download:**
```bash
# Download latest version
clarifai artifact cp users/<user_id>/apps/<app_id>/artifacts/<artifact_id> ./downloads/

# Download specific version
clarifai artifact cp users/u/apps/a/artifacts/model/versions/v123 ./model.pt
```

### clarifai artifact get

Get artifact or version details.

```bash
clarifai artifact get users/<user_id>/apps/<app_id>/artifacts/<artifact_id>
clarifai af get users/u/apps/a/artifacts/model/versions/v123
```

### clarifai artifact delete

Delete artifacts or versions.

```bash
# Delete artifact
clarifai artifact delete users/<user_id>/apps/<app_id>/artifacts/<artifact_id>

# Delete specific version
clarifai artifact delete users/u/apps/a/artifacts/model/versions/v123

# Force delete (no confirmation)
clarifai af delete users/u/apps/a/artifacts/model --force
```

### Artifact CLI Options

| Option | Description |
|--------|-------------|
| `--visibility` | `private` (default), `public`, `org` |
| `--description` | Version description |
| `--expires-at` | RFC3339 expiration: `2024-12-31T23:59:59.999Z` |
| `--force`, `-f` | Skip confirmations/overwrite files |
| `--versions` | List artifact versions |

---

## Extended Search

For edge cases not covered here, search:
- **SDK source**: https://github.com/Clarifai/clarifai-python/tree/main/clarifai/client
- **CLI source**: https://github.com/Clarifai/clarifai-python/tree/main/clarifai/cli
- **Official documentation**: https://docs.clarifai.com/resources/api-overview/cli
- **Examples repository**: https://github.com/Clarifai/examples
