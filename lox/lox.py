import sys
import argparse

from scanner import Scanner
from parser import Parser
from error_reporter import error_reporter
from interpreter import Interpreter


class Lox:
    def __init__(self):
        self._interpreter = Interpreter()

    def main(self) -> None:
        parser = argparse.ArgumentParser(description="Interprets Lox scripts")
        parser.add_argument(
            "-s",
            "--script",
            required=False,
            metavar="[script]",
            type=str,
            nargs=1,
            help="Lox script to be interpreted",
        )

        args = parser.parse_args()

        if args.script:
            self._run_file(args.script[0])
        else:
            self._run_prompt()

    def _run_file(self, path: str) -> None:
        with open(path, "r") as f:
            self._run(f.read())

            if error_reporter.had_error:
                sys.exit(65)
            if error_reporter.had_runtime_error:
                sys.exit(70)

    def _run_prompt(self) -> None:
        while True:
            line = input("> ")
            # Interpreter exits when user does not enter any input
            # before pressing enter, resulting in "line" being an
            # empty string
            if not line:
                break
            self._run(line)
            error_reporter.had_error = False

    def _run(self, src: str) -> None:
        scanner = Scanner(src)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        statements = parser.parse()

        if error_reporter.had_error:
            return

        self._interpreter.interpret(statements)


if __name__ == "__main__":
    lox = Lox()
    lox.main()
