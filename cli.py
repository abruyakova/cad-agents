import time

from langchain_core.callbacks import get_usage_metadata_callback

from main import MODEL
from metrics import record_metrics, start_metrics_server


def run_dialog(agent):

    start_metrics_server(model=MODEL)
    print("Enter a drawing instruction (empty line or 'exit' to quit).")
    messages = []
    while True:
        try:
            user_content = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_content or user_content.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_content})

        with get_usage_metadata_callback() as cb:
            started = time.perf_counter()
            result = agent.invoke({"messages": messages})
            seconds = time.perf_counter() - started

            for model_name, usage in cb.usage_metadata.items():
                print(f"Model: {model_name}")
                print(f"Total Tokens: {usage['total_tokens']}")
                print(f"Prompt Tokens: {usage['input_tokens']}")
                print(f"Completion Tokens: {usage['output_tokens']}")

        messages = result["messages"]
        final_message = messages[-1]
        print(final_message.content)

        is_question = final_message.text.lstrip().startswith("QUESTION:")
        record_metrics(final_message, cb.usage_metadata, seconds,
                       "question" if is_question else "json")

        # Keep the conversation while the agent is asking questions;
        # start a new one once it returns the final JSON.
        if not is_question:
            messages = []