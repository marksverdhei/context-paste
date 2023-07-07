import os
import sys
from unittest import mock

import pytest

from context_paste import main


# Mock pyperclip.copy function to not interact with the clipboard during tests
@pytest.fixture
def mock_pyperclip(monkeypatch):
    def mock_copy(*args, **kwargs):
        pass  # Do nothing

    monkeypatch.setattr(main.pyperclip, "copy", mock_copy)


def test_get_file_prompt():
    expected_prompt = """
`tests/data/foo.json`
```json
{
    "a": [],
    "b": {
        "c": "d"
    }
}
```
"""

    prompt = main.get_file_prompt("tests/data/foo.json")
    assert prompt == expected_prompt


def test_get_prompts_from_files_with_file():
    prompts = main.get_prompts_from_files("tests/data/foo.json")
    assert len(prompts) == 1
    assert prompts[0].startswith("\n`tests/data/foo.json`")


def test_get_prompts_from_files_with_dir():
    prompts = main.get_prompts_from_files("tests/data/")
    assert len(prompts) == 1
    assert prompts[0].startswith("\n`tests/data/foo.json`")


def test_get_prompts_from_files_with_invalid_pattern():
    with pytest.raises(TypeError):
        main.get_prompts_from_files("invalid")


def test_main_with_pattern_argument(mock_pyperclip):
    test_args = ["main.py", "tests/data/foo.json"]
    with mock.patch.object(sys, "argv", test_args):
        main.main()  # Assert no exceptions


def test_main_with_too_long_text(mock_pyperclip):
    long_text_file = "tests/data/long_text_file.txt"
    with open(long_text_file, "w") as f:
        f.write("a" * main.MAX_TOKENS * 10)

    test_args = ["main.py", long_text_file]
    with mock.patch.object(sys, "argv", test_args):
        main.main()  # Assert no exceptions

    os.remove(long_text_file)
