import argparse
import os
import sys
from typing import List, Callable, Dict, Any

import colorama

from galoup import logger, process, error
from galoup.error import Error

ParserAssignmentFunction = Callable[[argparse._SubParsersAction], None]
OperationFunction = Callable[[Dict[Any, Any]], None]


class Operation:
    def __init__(self, description: str, operation_func: OperationFunction):
        self.description = description
        self.operation_func = operation_func

    def run(self, current_vars: Dict[Any, Any]):
        logger.normal(self.description + "... ", end='')
        try:
            self.operation_func(current_vars)
            logger.good("Done!")
        except Error as e:
            logger.bad("Failed.")
            raise e


class Command:
    def __init__(self, name: str, help_str: str, parser_func: ParserAssignmentFunction, operations: List[Operation]):
        self.name = name
        self.help = help_str
        self.parser_func = parser_func
        self.operations = operations

    def register(self, parent_parser: argparse._SubParsersAction):
        subparser = parent_parser.add_parser(name=self.name, title=self.name, help=self.help)
        subparser.set_defaults(func=self.run)

    def run(self, opts: argparse.Namespace):
        current_vars = {}
        current_vars.update(opts.__dict__)
        for op in self.operations:
            op.run(current_vars)


class Program:
    def __init__(self, name: str, description: str, commands: List[Command]):
        self.name = name
        self.description = description
        self.commands = commands

    def run(self):
        # Get args
        parser = argparse.ArgumentParser(prog=self.name, description=self.description)
        subparsers = parser.add_subparsers(title='sub-commands')
        for command in self.commands:
            command.register(subparsers)
        # Init global fixtures
        colorama.init()
        # Do some basic validation
        try:
            _validate()
        except Error as e:
            _fail(e)
        # Get args
        parsed = parser.parse_args(sys.argv[1:])
        if not hasattr(parsed, 'func'):
            # If we get here, it means a sub-command wasn't given
            logger.normal("You must specify a sub-command.")
            parser.print_usage(sys.stderr)
            sys.exit(1)
        # Execute sub-command
        try:
            parsed.func(parsed)
        except Error as e:
            _fail(e)


def _in_project_root() -> bool:
    # Get the git root directory
    output, _ = process.run('git rev-parse --show-toplevel')
    # Get the current working directory
    cwd = os.getcwd()
    # See if they match
    return os.path.realpath(output.rstrip()) == os.path.realpath(cwd)


def _validate():
    if not _in_project_root():
        raise error.ValidationError("You must be in the project root directory to run galoup.")


def _fail(e: Error):
    logger.error(e)
    sys.exit(1)
