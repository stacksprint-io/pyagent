import subprocess
import time

TOOLS = [
    {
        "name": "read_file",
        "description": "Read a file and return its contents.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
    {
        "name": "run_tests",
        "description": "Run the pytest suite for the buggy module.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "edit_file",
        "description": "Replace old_text with new_text in a file. The human gets a veto window first.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "old_text": {"type": "string"},
                "new_text": {"type": "string"},
            },
            "required": ["path", "old_text", "new_text"],
        },
    },
]


def read_file(path):
    return open(path).read()


def run_tests():
    result = subprocess.run(
        ["python3", "-m", "pytest", "buggy/", "-q"],
        capture_output=True, text=True,
    )
    return result.stdout + result.stderr


def edit_file(path, old_text, new_text):
    print(f"\n  proposed edit to {path}:")
    print(f"  - {old_text}")
    print(f"  + {new_text}")
    print("  applying in 5 seconds, press ctrl+c to veto...")
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        return "The human vetoed this edit."
    source = open(path).read()
    if old_text not in source:
        return "old_text was not found in the file."
    open(path, "w").write(source.replace(old_text, new_text, 1))
    return "Edit applied."


def run_tool(name, args):
    if name == "read_file":
        return read_file(**args)
    if name == "run_tests":
        return run_tests()
    if name == "edit_file":
        return edit_file(**args)
    return f"Unknown tool: {name}"
