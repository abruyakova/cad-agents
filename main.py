

MODEL = 'qwen3:4b-instruct'
# Limits so one run cannot take over the machine.
CHAT_OPTIONS = {
    "temperature": 0,
    "num_ctx": 8192,
    "num_predict": 1024,
    "keep_alive": "1m",
}


if __name__ == "__main__":
    print("Hello World")