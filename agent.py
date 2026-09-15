import json
import os
import sys
import urllib.request

from tools import TOOLS, run_tool


def load_env(path=".env"):
    for line in open(path):
        if "=" in line and not line.startswith("#"):
            key, value = line.strip().split("=", 1)
            os.environ.setdefault(key, value)


load_env()
API_KEY = os.environ["ANTHROPIC_API_KEY"]
MODEL = "claude-fable-5-1"

SYSTEM = (
    "You are a tiny coding agent working in this repo. "
    "Use the tools to find and fix the problem with a small, focused edit, "
    "then rerun the tests to prove it."
)


def call_model(messages):
    body = json.dumps({
        "model": MODEL,
        "max_tokens": 1500,
        "system": SYSTEM,
        "messages": messages,
        "tools": TOOLS,
    }).encode()
    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def main():
    task = sys.argv[1]
    messages = [{"role": "user", "content": task}]
    for step in range(1, 11):
        reply = call_model(messages)
        messages.append({"role": "assistant", "content": reply["content"]})
        for block in reply["content"]:
            if block["type"] == "text" and block["text"].strip():
                print(f"\n[claude] {block['text'].strip()}")
        if reply["stop_reason"] != "tool_use":
            print(f"\n[done] finished after {step} steps")
            return
        results = []
        for block in reply["content"]:
            if block["type"] != "tool_use":
                continue
            print(f"\n[tool] {block['name']} {json.dumps(block['input'])[:90]}")
            output = run_tool(block["name"], block["input"])
            print(output if len(output) < 500 else output[:500] + " ...")
            results.append({
                "type": "tool_result",
                "tool_use_id": block["id"],
                "content": output,
            })
        messages.append({"role": "user", "content": results})
    print("\n[stopped] hit the step limit")


main()
