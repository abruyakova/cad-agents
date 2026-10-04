from prometheus_client import Counter, Histogram, start_http_server

METRICS_PORT = 8082

REQUESTS = Counter("cad_agent_requests", "Agent replies by result", ["result"])
TOKENS = Counter("cad_agent_tokens", "Tokens used by the agent", ["model", "kind"])
REQUEST_SECONDS = Histogram(
    "cad_agent_request_seconds", "Wall time of one agent.invoke", ["model"],
    buckets=(1, 2, 5, 10, 20, 30, 60, 120, 300),
)
LOAD_SECONDS = Histogram(
    "ollama_load_seconds", "Ollama model load time", ["model"],
    buckets=(0.01, 0.1, 0.5, 1, 2, 5, 10, 30),
)
PROMPT_EVAL_SECONDS = Histogram(
    "ollama_prompt_eval_seconds", "Ollama prompt processing time", ["model"],
    buckets=(0.1, 0.5, 1, 2, 5, 10, 20, 60),
)
EVAL_SECONDS = Histogram(
    "ollama_eval_seconds", "Ollama answer generation time", ["model"],
    buckets=(0.5, 1, 2, 5, 10, 20, 30, 60, 120),
)
TOKENS_PER_SECOND = Histogram(
    "ollama_tokens_per_second", "Ollama generation speed", ["model"],
    buckets=(5, 10, 20, 30, 40, 50, 75, 100, 150),
)


def start_metrics_server(model, port=METRICS_PORT):
    # Create every series at 0 up front; otherwise Prometheus misses the
    # first reply, because a counter's first value is never seen as an increase.
    for result in ("question", "json"):
        REQUESTS.labels(result=result)
    for kind in ("input", "output"):
        TOKENS.labels(model=model, kind=kind)
    for histogram in (REQUEST_SECONDS, LOAD_SECONDS, PROMPT_EVAL_SECONDS,
                      EVAL_SECONDS, TOKENS_PER_SECOND):
        histogram.labels(model=model)

    start_http_server(port)
    print(f"Metrics on http://localhost:{port}/metrics")


def record_metrics(final_message, usage_metadata, seconds, result):
    REQUESTS.labels(result=result).inc()
    for model_name, usage in usage_metadata.items():
        TOKENS.labels(model=model_name, kind="input").inc(usage["input_tokens"])
        TOKENS.labels(model=model_name, kind="output").inc(usage["output_tokens"])

    # Ollama reports its own timings (in nanoseconds) with every reply.
    meta = final_message.response_metadata
    model_name = meta.get("model", "unknown")
    REQUEST_SECONDS.labels(model=model_name).observe(seconds)
    if meta.get("load_duration") is not None:
        LOAD_SECONDS.labels(model=model_name).observe(meta["load_duration"] / 1e9)
    if meta.get("prompt_eval_duration") is not None:
        PROMPT_EVAL_SECONDS.labels(model=model_name).observe(meta["prompt_eval_duration"] / 1e9)
    if meta.get("eval_duration"):
        EVAL_SECONDS.labels(model=model_name).observe(meta["eval_duration"] / 1e9)
        if meta.get("eval_count"):
            TOKENS_PER_SECOND.labels(model=model_name).observe(
                meta["eval_count"] / (meta["eval_duration"] / 1e9)
            )
