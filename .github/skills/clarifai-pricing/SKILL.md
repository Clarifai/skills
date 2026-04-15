---
name: clarifai-pricing
description: Fetch and display Clarifai pricing information. Use when the user wants to check model pricing (per-token, per-operation), compute instance pricing (GPU/CPU hourly rates), or compare prices across providers and regions. Covers model inference pricing, compute pricing, and price conversion utilities.
---

# Clarifai Pricing

Fetch live pricing information from the Clarifai API for model inference and compute instances.

## Price Units

Clarifai stores prices in **millicents** (1/100,000 of a dollar):
- `$1.00 = 100,000 millicents`
- Model token prices: millicents per token → convert to $/1M tokens
- Compute instance prices: millicents per second → convert to $/hour

### Conversion Formulas

```python
# Millicents per token → dollars per 1M tokens
dollars_per_million = millicents_per_token / 100_000 * 1_000_000

# Millicents per second → dollars per hour
dollars_per_hour = millicents_per_second / 100_000 * 3600
```

## Model Pricing (Per-Token / Per-Operation)

### API Endpoint

```
POST https://api.clarifai.com/v2/resource_prices/searches
```

### Python Example

```python
import requests

PAT = "your_pat_here"
headers = {"Authorization": f"Key {PAT}", "Content-Type": "application/json"}

# Fetch pricing for specific models
body = {
    "models": [
        {"id": "model_id", "user_id": "owner_user_id", "app_id": "owner_app_id"}
    ]
}

response = requests.post(
    "https://api.clarifai.com/v2/resource_prices/searches",
    headers=headers,
    json=body
)

for mp in response.json().get("model_prices", []):
    billing_type = mp.get("billing_type")  # 1 = token-based, 2 = ops-based

    if billing_type == 1:
        # Token-based model (LLMs, multimodal)
        input_price = mp["price_per_prompt_token"] / 100_000 * 1_000_000
        output_price = mp["price_per_completion_token"] / 100_000 * 1_000_000
        print(f"Input: ${input_price:.3f}/1M tokens, Output: ${output_price:.3f}/1M tokens")

    elif billing_type == 2:
        # Operation-based model (CV, embeddings)
        op_price = mp["price_per_op"] / 100_000
        print(f"${op_price:.5f}/operation")
```

### Using the SDK

```python
from clarifai.client import Model

model = Model(url="https://clarifai.com/clarifai/llm/models/gpt-oss-120b")
# Pricing is available via the API endpoint above; the SDK does not expose pricing directly
```

Always pull live pricing from the API rather than using hardcoded values.

## Compute Instance Pricing (GPU/CPU Hourly Rates)

### API Endpoints

```
# List cloud providers
GET https://api.clarifai.com/v2/cloud_providers

# List regions for a provider
GET https://api.clarifai.com/v2/cloud_providers/{cloud_provider_id}/regions

# List instance types with pricing for a region
GET https://api.clarifai.com/v2/cloud_providers/{cloud_provider_id}/regions/{region_id}/instance_types
```

### Python Example

```python
import requests

PAT = "your_pat_here"
headers = {"Authorization": f"Key {PAT}"}
base = "https://api.clarifai.com/v2"

# Get all providers
providers = requests.get(f"{base}/cloud_providers", headers=headers).json()["cloud_providers"]

for provider in providers:
    pid = provider["id"]

    # Get regions
    regions = requests.get(f"{base}/cloud_providers/{pid}/regions", headers=headers).json()["regions"]

    for region in regions:
        rid = region if isinstance(region, str) else region["id"]

        # Get instance types with pricing
        instances = requests.get(
            f"{base}/cloud_providers/{pid}/regions/{rid}/instance_types?per_page=100",
            headers=headers
        ).json().get("instance_types", [])

        for inst in instances:
            price_millicents_per_sec = float(inst.get("price", "0"))
            price_per_hour = price_millicents_per_sec / 100_000 * 3600

            compute = inst.get("compute_info", {})
            acc_type = compute.get("accelerator_type", "")
            num_acc = compute.get("num_accelerators", 0)

            if price_per_hour > 0:
                gpu = f"{num_acc}x {acc_type}" if acc_type else "CPU"
                print(f"{pid}/{rid}: {inst.get('cfid')} | {gpu} | ${price_per_hour:.2f}/hr")
```

### Instance Type Response Fields

```json
{
    "id": "instance_type_id",
    "cfid": "g6e.xlarge",
    "description": "",
    "price": "65000",           // millicents per second
    "compute_info": {
        "cpu_limit": "4",
        "cpu_memory": "29033Mi",
        "accelerator_type": "['NVIDIA-L40S']",
        "num_accelerators": 1,
        "accelerator_memory": "48000Mi"
    }
}
```

### Available Cloud Providers

| Provider | Regions | GPU Types Available |
|---|---|---|
| AWS | us-east-1, us-west-2 | T4, A10G, L4, L40S, RTX PRO 6000, H100 |
| GCP | us-east4, us-central1 | L4, A100, H100, RTX PRO 6000, TPU v5/v6/v7 |
| Vultr | new-york, atlanta, chicago, seattle | A16, A100, L40S, GH200, B200, MI300X |
| DigitalOcean | nyc1, nyc2, sfo3, atl1 | H100, MI300X, MI350X |
| Azure | eastus | T4, A100, H100, MI300X, V620 |
| Lambda | us-east-1, us-south-3 | B200 |
| Oracle | us-chicago-1 | A10G, MI300X |

Always pull live pricing from the API rather than using cached values.

## Pricing Notes

- All compute instances support **autoscale to zero** — no cost when idle
- **Spot pricing** is available on select instances at reduced rates
- Enterprise customers on **dedicated nodepools** pay committed capacity rates
- **Third-party model pass-through** (Claude, GPT, Gemini, etc.) is priced at provider rates
- Token-based pricing applies to LLMs and multimodal models; operation-based pricing applies to CV, embeddings, and custom models
