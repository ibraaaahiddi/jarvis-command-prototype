# JARVIS Command Prototype

A deliberately small, command-driven prototype inspired by JARVIS: **one instruction in, one simple local task out**.

**Portfolio:** [PORTFOLIO.md](PORTFOLIO.md) — AI quality, data annotation, automation, virtual assistance, and content QA.

This is **not** the full JARVIS assistant. It is a proof-of-concept for demonstrating command parsing, safe local workspace actions, and a simple computer task without exposing credentials, email, business data, or personal information.

## What it does

```text
python jarvis.py mkdir "demo folder"
python jarvis.py list
python jarvis.py note remember the milk
python jarvis.py open https://example.com
python jarvis.py time
```

Optional screenshot (requires `pyautogui`):

```text
pip install pyautogui
python jarvis.py screenshot
```

## Safety boundaries

- All file operations are confined to a local `workspace/` folder.
- Folder names are validated; path traversal is rejected.
- The `open` command accepts only `http(s)` URLs.
- No email, no calls, no publishing, no credentials, no network API keys.
- The optional screenshot command is local-only and saves inside `workspace/`.
- This prototype is not a production automation system and has no approval workflow. Do not use it for sensitive actions.

## Workspace

The default workspace is `./workspace/`. Override it for tests or experimentation:

```text
JARVIS_PROTOTYPE_WORKSPACE=/tmp/jarvis-demo python jarvis.py list
```

## Tests

```text
python -m unittest discover -s tests -v
```

## Why this exists

It is a small, shareable proof of the core idea: a command can be parsed and turned into a simple, bounded computer action. It is intentionally separate from any private assistant, business pipeline, or personal data.

## License

MIT. See `LICENSE`.
