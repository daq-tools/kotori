# Needed for typed args.
# https://github.com/pyinvoke/invoke/issues/357#issuecomment-688596802
import os
from typing import Any, Callable, TypeVar

import invoke

F = TypeVar("F", bound=Callable[..., Any])


def task(f: F) -> F:
    f.__annotations__ = {}
    return invoke.task(f)


def run_commands(commands):
    if isinstance(commands, str):
        commands = [commands]
    for command in commands:
        command = command.strip()
        print(command)
        exitcode = os.system(command)
        if exitcode != 0:
            raise SystemExit("Command failed")


def print_header(label, char="-"):
    length = max(len(label), 42)
    print(char * length)
    print(label.center(length))
    print(char * length)
