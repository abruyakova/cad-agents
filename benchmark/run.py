"""Run every case from benchmark/cases_2d.py (or cases_3d.py) through the agent, one at a time,
and save timing, token and correctness statistics.

    uv run python -m benchmark.run
    uv run python -m benchmark.run --set 3d       # 3D cases have no expected geometry yet: "unchecked"
    uv run python -m benchmark.run --cases M10,MP-200 --repeat 3
    uv run python -m benchmark.run --metrics      # also feed Prometheus / Grafana
    uv run python -m benchmark.run --agent rag_agent   # tool-calling agent (rag_agent.py) instead of rag_chain.py

Results go to benchmark/results/run_<timestamp>.csv (one row per case) and
run_<timestamp>_replies.jsonl (the final reply of every case).
"""
import argparse
import csv
import json
import statistics
import time
from datetime import datetime
from pathlib import Path

from langchain_core.callbacks import get_usage_metadata_callback

from benchmark import cases_2d, cases_3d
from main import MODEL
from metrics import record_metrics, start_metrics_server
import pure_prompt
import rag_agent
import rag_chain
from vector_store import EMBEDDING_MODEL

ROOT = Path(__file__).parent.parent
RESULTS_DIR = Path(__file__).parent / "results"
CASE_SETS = {"2d": cases_2d.CASES, "3d": cases_3d.CASES}
# rag_chain:   retrieval on every turn, context in the system prompt (rag_chain.py)
# rag_agent:   the model decides when to call the retrieve_context tool (rag_agent.py)
# pure_prompt: pure baseline prompt without RAG retrieval (pure_prompt.py)
AGENTS = {
    "rag_chain": rag_chain.build_agent,
    "rag_agent": rag_agent.rag_chain,
    "pure_prompt": pure_prompt.build_agent,
}
CANONICAL_NAMES = {
    "rag_chain": "rag_chain",
    "rag_agent": "rag_agent",
    "pure_prompt": "pure_prompt",
}

# When the agent asks questions, accept every default it offers.
# Benchmark harness specifically uses "default all" to accept all defaults.
ACCEPT_DEFAULTS = "default all"
MAX_TURNS = 4

FIELDS = [
    "run_id", "agent", "case_set", "case_no", "section", "case", "repeat", "turns", "status", "mismatches",
    "total_s", "retrieval_s", "load_s", "prompt_eval_s", "eval_s",
    "input_tokens", "output_tokens", "tokens_per_sec", "model", "embedding_model",
]

def run_case(agent, timings, instruction, use_metrics):
    """Send the instruction, accept defaults while the agent asks.

    Returns (stats, final reply text, True if the agent was still asking at the end).
    """
    stats = {"turns": 0, "total_s": 0.0, "load_s": 0.0, "prompt_eval_s": 0.0,
             "eval_s": 0.0, "input_tokens": 0, "output_tokens": 0, "eval_count": 0}
    timings["retrieval_s"] = 0.0
    messages = [{"role": "user", "content": instruction}]
    reply = ""
    for _ in range(MAX_TURNS):
        with get_usage_metadata_callback() as cb:
            started = time.perf_counter()
            sent = len(messages)
            messages = agent.invoke({"messages": messages})["messages"]
            seconds = time.perf_counter() - started

        final_message = messages[-1]
        reply = final_message.text.strip()
        is_question = reply.startswith("QUESTION:")

        stats["turns"] += 1
        stats["total_s"] += seconds
        for usage in cb.usage_metadata.values():
            stats["input_tokens"] += usage["input_tokens"]
            stats["output_tokens"] += usage["output_tokens"]
        # Ollama reports its own timings (in nanoseconds) with every reply;
        # the tool agent makes several model calls per turn, so add them all up.
        for message in messages[sent:]:
            if message.type != "ai":
                continue
            meta = message.response_metadata
            stats["load_s"] += (meta.get("load_duration") or 0) / 1e9
            stats["prompt_eval_s"] += (meta.get("prompt_eval_duration") or 0) / 1e9
            stats["eval_s"] += (meta.get("eval_duration") or 0) / 1e9
            stats["eval_count"] += meta.get("eval_count") or 0

        if use_metrics:
            record_metrics(final_message, cb.usage_metadata, seconds,
                           "question" if is_question else "json")
        if not is_question:
            return stats, reply, False
        messages.append({"role": "user", "content": ACCEPT_DEFAULTS})
    return stats, reply, True


def judge(reply, still_asking, expected, case_set="2d"):
    """(status, mismatches) for the final reply; expected is None when the case has no expected geometry."""
    if still_asking:
        return "still_asking", []
    try:
        result = json.loads(reply)
    except json.JSONDecodeError:
        return "not_json", []
    if expected is None:
        return "unchecked", []
    compare_fn = cases_3d.compare if case_set == "3d" else cases_2d.compare
    mismatches = compare_fn(result, expected)
    return ("wrong" if mismatches else "correct"), mismatches


def short(text, length=60):
    return text if len(text) <= length else text[:length - 1] + "…"


def print_summary(rows):
    if not rows:
        print("No cases were run.")
        return
    print(f"\n{'#':>2}  {'status':<12} {'turns':>5} {'time s':>7} {'tok in':>7} {'tok out':>7} {'tok/s':>6}  case")
    for r in rows:
        print(f"{r['case_no']:>2}  {r['status']:<12} {r['turns']:>5} {r['total_s']:>7.1f} "
              f"{r['input_tokens']:>7} {r['output_tokens']:>7} {r['tokens_per_sec']:>6.1f}  {short(r['case'], 50)}")

    def accuracy(subset):
        checked = [r for r in subset if r["status"] != "unchecked"]
        return f"{sum(r['status'] == 'correct' for r in checked)}/{len(checked)}"

    times = [r["total_s"] for r in rows]
    speeds = [r["tokens_per_sec"] for r in rows if r["tokens_per_sec"]]
    print(f"\nAccuracy: {accuracy(rows)}", end="")
    for section in sorted({r["section"] for r in rows}):
        print(f"  |  {section}: {accuracy([r for r in rows if r['section'] == section])}", end="")
    print(f"\nTime per case: mean {statistics.mean(times):.1f}s, median {statistics.median(times):.1f}s, "
          f"total {sum(times):.1f}s")
    print(f"Tokens: input {sum(r['input_tokens'] for r in rows)}, "
          f"output {sum(r['output_tokens'] for r in rows)}")
    if speeds:
        print(f"Generation speed: mean {statistics.mean(speeds):.1f} tokens/s")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--set", choices=CASE_SETS, default="2d", help="which cases to run (default: 2d)")
    parser.add_argument("--agent", choices=list(AGENTS.keys()), default="rag_chain",
                        help="rag_chain: rag_chain.py, context injected every turn (default); "
                             "rag_agent: rag_agent.py, model calls retrieve_context; "
                             "pure_prompt: pure_prompt.py, direct execution without RAG; "
                             "prompt/tool: aliases for rag_chain/rag_agent")
    parser.add_argument("--cases", help="comma-separated substrings; run only instructions containing one of them")
    parser.add_argument("--repeat", type=int, default=1, help="run every case N times")
    parser.add_argument("--pause", type=float, default=0, help="seconds to sleep between cases")
    parser.add_argument("--metrics", action="store_true", help="serve Prometheus metrics while running")
    args = parser.parse_args()

    cases = list(enumerate(CASE_SETS[args.set], start=1))
    if args.cases:
        wanted = [w.strip() for w in args.cases.split(",") if w.strip()]
        cases = [(no, case) for no, case in cases if any(w in case["instruction"] for w in wanted)]
    if not cases:
        parser.error("no instruction matches --cases")

    if args.metrics:
        start_metrics_server(model=MODEL)

    agent_name = CANONICAL_NAMES.get(args.agent, args.agent)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    RESULTS_DIR.mkdir(exist_ok=True)
    csv_path = RESULTS_DIR / f"run_{run_id}_{agent_name}.csv"
    replies_path = RESULTS_DIR / f"run_{run_id}_{agent_name}_replies.jsonl"

    timings = {"retrieval_s": 0.0}

    def add_retrieval(seconds):
        timings["retrieval_s"] += seconds

    agent = AGENTS[args.agent](on_retrieval=add_retrieval)
    rows = []
    total = len(cases) * args.repeat

    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file, \
            open(replies_path, "w", encoding="utf-8") as replies_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
        writer.writeheader()

        for repeat in range(1, args.repeat + 1):
            for case_no, case in cases:
                instruction = case["instruction"]
                print(f"[{len(rows) + 1}/{total}] #{case_no} {short(instruction)}", flush=True)
                try:
                    stats, reply, still_asking = run_case(agent, timings, instruction, args.metrics)
                    status, mismatches = judge(reply, still_asking, case.get("expected"), case_set=args.set)
                except Exception as error:  # keep going; one broken case should not stop the run
                    stats, reply = None, f"{type(error).__name__}: {error}"
                    status, mismatches = "error", [reply]

                stats = stats or {}
                eval_s = stats.get("eval_s", 0.0)
                row = {
                    "run_id": run_id,
                    "agent": agent_name,
                    "case_set": args.set,
                    "case_no": case_no,
                    "section": case["section"],
                    "case": instruction,
                    "repeat": repeat,
                    "turns": stats.get("turns", 0),
                    "status": status,
                    "mismatches": "; ".join(mismatches),
                    "total_s": round(stats.get("total_s", 0.0), 3),
                    "retrieval_s": round(timings["retrieval_s"], 3),
                    "load_s": round(stats.get("load_s", 0.0), 3),
                    "prompt_eval_s": round(stats.get("prompt_eval_s", 0.0), 3),
                    "eval_s": round(eval_s, 3),
                    "input_tokens": stats.get("input_tokens", 0),
                    "output_tokens": stats.get("output_tokens", 0),
                    "tokens_per_sec": round(stats.get("eval_count", 0) / eval_s, 2) if eval_s else 0.0,
                    "model": MODEL,
                    "embedding_model": EMBEDDING_MODEL,
                }
                rows.append(row)
                writer.writerow(row)
                csv_file.flush()
                replies_file.write(json.dumps({"case_no": case_no, "repeat": repeat, "status": status,
                                               "reply": reply}, ensure_ascii=False) + "\n")
                replies_file.flush()
                print(f"    {status}, {row['turns']} turn(s), {row['total_s']:.1f}s", flush=True)

                if args.pause and len(rows) < total:
                    time.sleep(args.pause)

    print(f"\nAgent: {agent_name}")
    print_summary(rows)
    print(f"\nSaved {csv_path.relative_to(ROOT)} and {replies_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
