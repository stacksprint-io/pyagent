# pyagent — build your own Claude Code in pure Python

A complete, working coding agent in two small files. No LangChain, no CrewAI,
no framework of any kind. Just Python, the standard library, and one HTTPS
call to Anthropic's API.

This is the companion repo for the StackSprint tutorial video. The repo ships
with **two real bugs already in it**, so the first thing your agent does is
fix something that is genuinely broken.

```
agent.py            the loop        (~76 lines)
tools.py            three tools     (~70 lines)
buggy/invoice.py    bug #1: a one-cent rounding error
buggy/ledger.py     bug #2: the classic mutable default trap
buggy/test_*.py     the failing tests that prove them
```

## What you need

- Python 3.9 or newer (`python3 --version`)
- `pytest` (`python3 -m pip install pytest`)
- An Anthropic API key from https://console.anthropic.com/settings/keys
  (API usage is billed by Anthropic — a full agent run on these bugs costs
  a fraction of a cent, but it is real money, so keep your key private)

## Setup

```bash
git clone https://github.com/stacksprint-io/pyagent.git
cd pyagent
cp .env.example .env
# open .env and paste your key after ANTHROPIC_API_KEY=
```

The `.env` file is gitignored. Never commit it, never paste your key
anywhere else.

## See the bug fail first

```bash
python3 -m pytest buggy/ -q
```

You should see `test_discount_applies_to_the_order_not_per_line` fail:
the order total comes out `62.14` where it should be `62.15`, because the
billing code rounds each line item to cents inside the loop and the
per-line losses add up.

## Let the agent fix it

```bash
python3 agent.py "The pricing test is failing. Find the bug and fix it."
```

Watch what it does: it runs the tests first to see the failure for itself,
reads the code, proposes an exact edit, and then **pauses for five seconds
before touching anything** — press `ctrl+c` inside that window to veto the
edit. If you let it through, it reruns the tests and explains the bug back
to you in its own words.

Then try the second bug:

```bash
python3 agent.py "One test is still failing, in the ledger. Find it and fix it."
```

## How the loop works

The entire idea is one sentence: send the conversation history to the model,
the model answers with either text or a tool call, run the tool locally,
append the result to the history, and repeat until the model stops asking
for tools.

- `agent.py` holds that loop, plus one function that makes the API call
  with `urllib` from the standard library.
- `tools.py` holds three tools — `read_file`, `run_tests`, `edit_file` —
  and the JSON descriptions the model actually sees. The model never sees
  your Python, only those descriptions.

## Guardrails built in

- every `edit_file` call prints the exact change and waits five seconds,
  `ctrl+c` rejects it
- reads are always free, writes always wait
- the loop is hard-capped at ten steps, so it can never run away
- there is no memory between runs, and that is on purpose — every session
  starts from exactly what you gave it

## Things to try next

- give it a `MEMORY.md` file it reads at the start of every run
- add tools: search, `git`, your own deploy script — the loop does not change
- run several agents at once, one per bug, each in its own copy of the repo

## License

MIT — see [LICENSE](LICENSE). Have fun, and point it at your own failing
test.
