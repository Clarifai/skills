# Pipeline Structure Reference

## Directory Layout

```
my-pipeline/
├── config.yaml              # Main pipeline configuration
├── stepA/                   # First step
│   ├── config.yaml         # Step configuration
│   ├── requirements.txt    # Step dependencies
│   └── 1/
│       └── pipeline_step.py  # Step implementation
├── stepB/                   # Second step (depends on stepA)
│   ├── config.yaml
│   ├── requirements.txt
│   └── 1/
│       └── pipeline_step.py
└── README.md
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
      depends_on:
        - "stepA"

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

## Step config.yaml

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

## Orchestration Spec (Argo)

The `orchestration_spec` uses Argo Workflow syntax:

```yaml
orchestration_spec:
  entrypoint: main
  templates:
    - name: main
      dag:
        tasks:
          - name: step1
            template: step1-template
          - name: step2
            template: step2-template
            depends: step1
          - name: step3
            template: step3-template
            depends: "step1 && step2"  # Depends on both
```
