"""Tests for the minimal JARVIS command prototype."""
from __future__ import annotations

import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock

import jarvis


class JarvisPrototypeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["JARVIS_PROTOTYPE_WORKSPACE"] = self.tmp.name

    def tearDown(self) -> None:
        os.environ.pop("JARVIS_PROTOTYPE_WORKSPACE", None)
        self.tmp.cleanup()

    def run_cli(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = jarvis.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_mkdir_and_list(self) -> None:
        code, out, _ = self.run_cli("mkdir", "demo folder")
        self.assertEqual(code, 0)
        self.assertIn("created folder", out)
        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("demo folder/", out)

    def test_note_is_written(self) -> None:
        code, out, _ = self.run_cli("note", "remember", "the", "milk")
        self.assertEqual(code, 0)
        self.assertIn("note saved", out)
        text = (jarvis.workspace() / "notes.txt").read_text(encoding="utf-8")
        self.assertIn("remember the milk", text)

    def test_unsafe_folder_name_is_rejected(self) -> None:
        code, _, err = self.run_cli("mkdir", "../escape")
        self.assertEqual(code, 1)
        self.assertIn("folder names", err)

    def test_open_rejects_non_http_urls(self) -> None:
        code, _, err = self.run_cli("open", "file:///etc/passwd")
        self.assertEqual(code, 1)
        self.assertIn("http(s)", err)

    def test_open_accepts_http_and_calls_browser(self) -> None:
        with mock.patch("webbrowser.open") as opener:
            code, out, _ = self.run_cli("open", "https://example.com")
        self.assertEqual(code, 0)
        opener.assert_called_once_with("https://example.com")
        self.assertIn("opened", out)

    def test_time(self) -> None:
        code, out, _ = self.run_cli("time")
        self.assertEqual(code, 0)
        self.assertGreater(len(out.strip()), 10)


if __name__ == "__main__":
    unittest.main()
