#!/usr/bin/env python3
"""JARVIS Command Prototype.

One instruction in, one simple local task out. This is a deliberately small
educational prototype, not the full JARVIS assistant. It uses only the Python
standard library unless you opt in to the optional screenshot command.

Safety:
- all file operations stay inside a local `workspace/` folder;
- folder names are validated;
- only http(s) URLs are accepted for the `open` command;
- no credentials, no email, no network calls, no personal data.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
import webbrowser
from pathlib import Path
from urllib.parse import urlsplit


SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _.-]{0,60}$")


def workspace() -> Path:
    root = Path(os.environ.get("JARVIS_PROTOTYPE_WORKSPACE") or (Path.cwd() / "workspace"))
    root.mkdir(parents=True, exist_ok=True)
    return root.resolve()


def _inside_workspace(path: Path) -> bool:
    root = workspace()
    return path == root or root in path.parents


def cmd_mkdir(name: str) -> str:
    if not SAFE_NAME.match(name):
        raise ValueError("folder names may use letters, numbers, spaces, dots, dashes and underscores")
    target = (workspace() / name).resolve()
    if not _inside_workspace(target):
        raise ValueError("that path leaves the prototype workspace")
    target.mkdir(exist_ok=True)
    return f"created folder: {target.name}"


def cmd_list() -> str:
    items = sorted(
        item.name + ("/" if item.is_dir() else "")
        for item in workspace().iterdir()
    )
    return "\n".join(items) if items else "(workspace is empty)"


def cmd_note(text: str) -> str:
    text = " ".join(text.split())
    if not text:
        raise ValueError("the note is empty")
    path = workspace() / "notes.txt"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")
    return f"note saved to {path.name}"


def cmd_open(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("only http(s) URLs are allowed")
    webbrowser.open(url)
    return f"opened: {url}"


def cmd_screenshot(name: str = "screenshot.jpg") -> str:
    try:
        import pyautogui  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError("the optional screenshot command needs: pip install pyautogui") from exc
    target = (workspace() / name).resolve()
    if not _inside_workspace(target):
        raise ValueError("that path leaves the prototype workspace")
    image = pyautogui.screenshot()
    image.save(target)
    return f"screenshot saved: {target.name} ({image.size[0]}x{image.size[1]})"


def cmd_time() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S %Z")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jarvis",
        description="A tiny command-driven prototype: one instruction, one simple local task.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    mkdir = sub.add_parser("mkdir", help="create a folder inside the workspace")
    mkdir.add_argument("name")

    sub.add_parser("list", help="list the workspace")

    note = sub.add_parser("note", help="append a timestamped note to the workspace")
    note.add_argument("text", nargs="+")

    open_cmd = sub.add_parser("open", help="open an http(s) URL in the default browser")
    open_cmd.add_argument("url")

    shot = sub.add_parser("screenshot", help="save a screenshot inside the workspace (optional dependency)")
    shot.add_argument("name", nargs="?", default="screenshot.jpg")

    sub.add_parser("time", help="print the local date and time")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "mkdir":
            print(cmd_mkdir(args.name))
        elif args.command == "list":
            print(cmd_list())
        elif args.command == "note":
            print(cmd_note(" ".join(args.text)))
        elif args.command == "open":
            print(cmd_open(args.url))
        elif args.command == "screenshot":
            print(cmd_screenshot(args.name))
        elif args.command == "time":
            print(cmd_time())
        else:  # pragma: no cover - argparse prevents this
            raise ValueError("unknown command")
    except Exception as exc:  # noqa: BLE001 - report a clean CLI error
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
