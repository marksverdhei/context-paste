import os
import argparse
import pathlib
import pyperclip
from transformers import AutoTokenizer

MAX_TOKENS = 3900
tokenizer = AutoTokenizer.from_pretrained("gpt2")

templates = []

def process_files(pattern):
    if os.path.isdir(pattern):
        for dirpath, dirnames, filenames in os.walk(pattern):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                add_file_content(filepath)
    elif os.path.isfile(pattern):
        add_file_content(pattern)
    else:
        print(f"Invalid pattern: {pattern}")

def add_template(filename, content):
    template = """
`{filename}`
```{language}
{content}
```
    """
    _, ext = os.path.splitext(filename)
    language = ext.lstrip('.')
    templates.append(template.format(filename=filename, language=language, content=content))


def add_file_content(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {str(e)}")
        return

    add_template(filepath, content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", help="Directory or file path pattern to process")
    args = parser.parse_args()
    process_files(args.pattern)
    full_string = "\n".join(templates)
    if len(tokenizer.encode(full_string)) >= MAX_TOKENS:
        print("warning, text too long. Try one file at a time")
    pyperclip.copy(full_string)
    print("Copied file templates to clipboard!")

if __name__ == '__main__':
    main()