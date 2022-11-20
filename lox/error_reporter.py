import sys


class ErrorReporter:
    def __init__(self):
        self.had_error = False

    def error(self, line: int, msg: str) -> None:
        self.report(line, "", msg)

    def report(self, line: int, where: str, msg: str) -> None:
        print(f"[line {line}] Error{where}: {msg}", file=sys.stderr)
        self.had_error = True


error_reporter = ErrorReporter()
