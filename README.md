# Clarifai Skills

Agent skills for the [Clarifai](https://clarifai.com) AI platform. These skills give AI coding assistants (Claude Code, Cursor, Codex, and others) deep knowledge of Clarifai's model deployment, inference, MCP, pipeline, and data management capabilities.

Built on the open [Agent Skills](https://agentskills.io) standard — works across 30+ agent platforms.

## Quick Start

### Option A: Clarifai CLI (recommended)

```bash
pip install clarifai
clarifai skills install
```

That's it. Auto-detects your agents (Claude, Cursor, Codex) and installs all 11 skills globally.

### Option B: Claude Code Plugin

```bash
claude plugin marketplace add Clarifai/skills
claude plugin install clarifai-skills
```

### Option C: Manual

```bash
git clone https://github.com/Clarifai/skills.git
clarifai skills install --source ./skills
```

## What's Included

| Skill | What it does |
|-------|-------------|
| [clarifai-cli](.github/skills/clarifai-cli) | Full CLI reference: `init`, `serve`, `deploy`, `status`, `logs`, `undeploy`, `predict`, `list-instances` |
| [clarifai-model-upload](.github/skills/clarifai-model-upload) | Deploy models with vLLM, SGLang, HuggingFace, Ollama. `ModelClass`, `config.yaml`, GPU config |
| [clarifai-inference](.github/skills/clarifai-inference) | Model discovery, method signatures, code generation, OpenAI-compatible API, agentic models |
| [clarifai-mcp](.github/skills/clarifai-mcp) | Build MCP servers with `MCPModelClass`, `StdioMCPModelClass`, FastMCP tools |
| [clarifai-deployment-lifecycle](.github/skills/clarifai-deployment-lifecycle) | Deploy/status/logs/undeploy lifecycle, version patching, state monitoring |
| [clarifai-observability](.github/skills/clarifai-observability) | Debug stuck deployments: CLI logs, K8s events, common resolutions |
| [clarifai-agentic-flows](.github/skills/clarifai-agentic-flows) | Multi-step orchestration: "train THEN deploy", client scripts, server orchestrators |
| [clarifai-datasets](.github/skills/clarifai-datasets) | Upload datasets with annotations (classification, detection, segmentation), format conversion |
| [clarifai-pipelines](.github/skills/clarifai-pipelines) | Batch processing pipelines with containerized steps and Artifacts API |
| [clarifai-training-pipelines](.github/skills/clarifai-training-pipelines) | Train classifiers (ResNet-50) and detectors (YOLOF) using built-in templates |
| [clarifai-grpc](.github/skills/clarifai-grpc) | Low-level gRPC API with protobufs for advanced platform operations |

## CLI Commands

```bash
clarifai skills install                          # install all skills (auto-detect agents)
clarifai skills install --claude                 # install for Claude only
clarifai skills install clarifai-cli --claude    # install one skill
clarifai skills list --installed                 # see installed skills
clarifai skills update                           # update to latest
clarifai skills remove clarifai-grpc --claude    # remove one skill
clarifai skills remove --all                     # remove all
```

**Flags:**
- `--claude`, `--codex`, `--cursor`, `--all-agents` — target specific agents (default: auto-detect)
- `--global` / `--local` — user-wide or project-level (default: global)
- `--source /path` — install from local clone instead of GitHub

## How It Works

Skills follow the [Agent Skills standard](https://agentskills.io):

```
clarifai-cli/
  SKILL.md              # Instructions (YAML frontmatter + markdown)
  references/           # Detailed reference docs
  examples/             # Working code examples
```

Each `SKILL.md` has a `name` and `description` in YAML frontmatter. Agents load these at startup for routing, then read the full content on-demand when a matching task is detected.

**Install layout:**

```
~/.agents/skills/           # Central (one copy)
  clarifai-cli/
  clarifai-model-upload/
  ...
~/.claude/skills/           # Symlinks per agent
  clarifai-cli -> ~/.agents/skills/clarifai-cli
  ...
```

## Example: Deploy a Model in 3 Commands

With skills installed, just tell your agent:

> "Deploy Qwen3-0.6B with vLLM"

The agent reads the `clarifai-cli` and `clarifai-model-upload` skills and runs:

```bash
clarifai model init ./qwen --toolkit vllm --model-name "Qwen/Qwen3-0.6B"
clarifai model serve ./qwen          # test locally
clarifai model deploy ./qwen         # deploy to cloud
```

## Repository Structure

```
.
  AGENTS.md                              # Master index (loaded by agents)
  marketplace.json                       # Skills registry for CLI
  .claude-plugin/marketplace.json        # Claude Code plugin manifest
  .github/skills/                        # All 11 skills
    clarifai-cli/
      SKILL.md
      references/
      examples/
    clarifai-model-upload/
      SKILL.md
      references/
      examples/
    ...
  scripts/
    generate_marketplace.py              # Regenerate marketplace.json
```

## Contributing

1. Edit or create a skill in `.github/skills/your-skill/SKILL.md`
2. Follow the [SKILL.md format](https://agentskills.io): YAML frontmatter (`name`, `description`) + markdown body
3. Keep SKILL.md under 500 lines; move detailed docs to `references/`
4. Run `python scripts/generate_marketplace.py` to update the registry
5. Test with `clarifai skills install --source . --claude --force`

## Links

- [Clarifai Platform](https://clarifai.com)
- [Clarifai Python SDK](https://github.com/Clarifai/clarifai-python)
- [Runner Examples](https://github.com/Clarifai/runners-examples)
- [Agent Skills Standard](https://agentskills.io)
- [Clarifai Docs](https://docs.clarifai.com)
