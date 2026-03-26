# Model Upload Examples Index

## Local Examples

| Example | Description | Location |
|---------|-------------|----------|
| hf-llama-3_2-1b-instruct | HuggingFace LLaMA 3.2 1B model using HF toolkit | examples/hf-llama-3_2-1b-instruct/ |

## GitHub Examples

For additional examples, browse: https://github.com/Clarifai/runners-examples

### LLM Examples
| Example | Description | Link |
|---------|-------------|------|
| vLLM models | High-performance LLM serving | /llm/vllm-* |
| SGLang models | Structured generation | /llm/Sglang-* |
| HuggingFace models | Direct transformers | /llm/hf-* |
| Ollama models | Ollama wrapper | /llm/ollama-* |

### Vision Examples
| Example | Description | Link |
|---------|-------------|------|
| image-classifier | ResNet image classification | /image-classifier |
| image-detector | Object detection | /image-detector |
| ocr | Optical character recognition | /ocr |

### Other Examples
| Example | Description | Link |
|---------|-------------|------|
| text-embedder | Text embedding model | /text-embedder |
| text-to-image | Image generation | /text-to-image |
| multimodal-models | Vision-language models | /multimodal-models |

## How to Use GitHub Examples

```bash
# Browse and download examples
git clone https://github.com/Clarifai/runners-examples
cp -r runners-examples/llm/hf-llama-3_2-1b-instruct ./my-model

# Or init from toolkit and customize
clarifai model init ./my-model --toolkit vllm --model-name "meta-llama/Llama-3.2-1B-Instruct"
```
