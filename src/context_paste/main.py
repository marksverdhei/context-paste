import argparse
import os
from typing import List

import pyperclip

WORD_TO_TOKEN_RATE = 1.6

MAX_TOKENS = 3900


def get_prompts_from_files(pattern) -> List[str]:
    if os.path.isdir(pattern):
        prompts = []
        for dirpath, _, filenames in os.walk(pattern):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                prompts.append(get_file_prompt(filepath))

        return prompts
    elif os.path.isfile(pattern):
        return [get_file_prompt(pattern)]
    else:
        raise TypeError(f"Invalid pattern: {pattern}")


def get_file_prompt(filename):
    with open(filename, "r") as f:
        content = f.read()

    template = """
`{filename}`
```{language}
{content}
```
"""
    _, ext = os.path.splitext(filename)
    language = ext.lstrip(".")
    return template.format(filename=filename, language=language, content=content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", help="Directory or file path pattern to process")
    args = parser.parse_args()
    prompts = get_prompts_from_files(args.pattern)
    full_string = "\n".join(prompts)
    if len(full_string.split()) * WORD_TO_TOKEN_RATE >= MAX_TOKENS:
        print("warning, text too long. Try one file at a time")
    pyperclip.copy(full_string)
    print("Copied file templates to clipboard!")


if __name__ == "__main__":
    main()
