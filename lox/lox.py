import sys
import argparse

from scanner import Scanner
from error_reporter import error_reporter


class Lox:
    def __init__(self):
        self.had_error = False

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
            self.run_file(args.script[0])
        else:
            self.run_prompt()

    def run_file(self, path: str) -> None:
        with open(path, "r") as f:
            self.run(f.read())

            if error_reporter.had_error:
                sys.exit(65)

    def run_prompt(self) -> None:
        while True:
            line = input("> ")
            # Interpreter exits when user does not enter any input
            # before pressing enter, resulting in "line" being an
            # empty string
            if not line:
                break
            self.run(line)
            error_reporter.had_error = False

    def run(self, src: str) -> None:
        scanner = Scanner(src)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)


if __name__ == "__main__":
    lox = Lox()
    lox.main()
