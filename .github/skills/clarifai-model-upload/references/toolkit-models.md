# Toolkit-Based Model Creation

## Supported Toolkits

| Toolkit | Command | Use Case |
|---------|---------|----------|
| vLLM | `--toolkit vllm` | High-performance LLM serving with PagedAttention |
| SGLang | `--toolkit sglang` | Structured generation, function calling |
| HuggingFace | `--toolkit huggingface` | Direct transformers integration |
| Ollama | `--toolkit ollama` | Wrap existing Ollama models |
| LM Studio | `--toolkit lmstudio` | LM Studio model integration |
| Python | `--toolkit python` | Custom Python implementation |

## CLI Commands

**Load the `clarifai-cli` skill** for all toolkit initialization commands, including:
- Complete `clarifai model init` reference with all options
- Examples for each toolkit (vLLM, SGLang, HuggingFace, Ollama, LM Studio, Python)
- Use case routing table mapping user requests to commands

See `clarifai-cli` → "clarifai model init" section for:
- `--toolkit` options and model name formats
- `--toolkit mcp` for MCP servers and `--toolkit openai` for OpenAI wrappers
- `--model-name` for specifying HuggingFace repo IDs or Ollama tags

## Toolkit Selection Guide

| Toolkit | Best For | Key Features |
|---------|----------|--------------|
| vLLM | Production LLM serving, high throughput | PagedAttention, continuous batching, tensor parallelism |
| SGLang | Structured generation, function calling | RadixAttention, constrained decoding, grammar-based |
| HuggingFace | Direct transformers access, research | Full API access, custom tokenization, flexible preprocessing |
| Ollama | Local development, existing Ollama models | Wrap existing setups, requires local Ollama installation |
| Python | Fully custom implementations | Basic ModelClass template for custom logic |
