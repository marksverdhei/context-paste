from setuptools import setup

setup(
    name="context-paste",
    version="0.0.1",
    author="marksverdhei",
    author_email="marksverdhei@hotmail.com",
    description="A command-line utility to ",
    packages=["context_paste"],
    package_dir={"context_paste": "src/context_paste"},
    entry_points={
        "console_scripts": ["conpaste=context_paste.main:main"],
    },
    install_requires=[
        "pyperclip",
        "transformers",
    ],
)
