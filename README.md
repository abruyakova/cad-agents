# CAD Geometry Agent

This repository contains a CAD geometry agent that converts short natural-language drawing instructions into strict JSON geometry descriptions for 2D and 3D parts. The project includes a pure prompt agent, a retrieval-augmented chain agent, and a tool-using RAG agent, along with benchmark scripts to compare their behavior.

## What it does

The agent turns instructions such as:

- "Create a square plate centered at the origin with a central hole for an M10 bolt"
- "Create a cylinder with a diameter of 80 mm and a height of 120 mm"
- "Create a circular flange with six bolt holes evenly spaced on a 120 mm bolt circle"

into validated geometry JSON used directly by downstream CAD tooling.

## Project structure

- `main.py` — core model configuration and runtime settings
- `cli.py` — interactive dialog loop for chatting with an agent
- `pure_prompt.py` — baseline agent without retrieval
- `rag_chain.py` — agent that injects retrieved context on every turn
- `rag_agent.py` — agent that calls a retrieval tool when needed
- `prompts.py` — prompt construction and system prompt loading
- `vector_store.py` — vector store and retrieval logic
- `benchmark/` — benchmark cases, runner, and result export
- `data/system_promt.txt` — company rules, defaults, and instruction constraints
- `tests/` — lightweight validation tests

## Requirements

- Python 3.14+
- `uv`
- Ollama with a model available to the project configuration
- Optional local observability stack for metrics/grafana if using dashboard tooling

## Setup

From the repository root:

```bash
uv sync
```

Make sure Ollama is running and that the configured model is available, as defined in `main.py`.

## Running the agents

Interactive runs:

```bash
uv run python pure_prompt.py
uv run python rag_chain.py
uv run python rag_agent.py
```

Each agent starts the interactive prompt loop from `cli.py`.

## Benchmarking

Use the benchmark runner to evaluate the agents against the bundled 2D and 3D cases:

```bash
uv run python -m benchmark.run
uv run python -m benchmark.run --set 2d
uv run python -m benchmark.run --set 3d
uv run python -m benchmark.run --agent rag_agent
uv run python -m benchmark.run --cases M10,MP-200 --repeat 3
```

The runner writes CSV summaries and reply logs into `benchmark/results/`.

## Benchmark output

The benchmark pipeline records:

- per-case status (`correct`, `wrong`, `not_json`, etc.)
- timing data
- token usage
- generation speed
- JSON reply logs for each run

These outputs can be used to compare prompt-only, retrieval-chain, and tool-based agent behavior.

## Notes

- The project is designed to prefer explicit instructions over defaults, but company defaults are used when allowed by the system rules.
- Missing required values trigger clarification questions rather than silent JSON output.
- The benchmark expects exact geometry comparisons for the 2D and 3D case sets under `benchmark/cases_2d.py` and `benchmark/cases_3d.py`.

## License

This project does not currently declare a repository license in the root tree.
