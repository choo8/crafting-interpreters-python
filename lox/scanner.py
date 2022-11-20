from token_type import TokenType
from token import Token
from error_reporter import error_reporter

from typing import List, Optional


class Scanner:
    def __init__(self, src: str):
        self.src = src
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            # We are at the beginning of the next lexme
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.src)

    def advance(self) -> str:
        self.current += 1
        return self.src[self.current - 1]

    def add_token(self, type: TokenType, literal: Optional[object] = None) -> None:
        text = self.src[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def scan_token(self) -> None:
        c = self.advance()

        if c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "!":
            self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
        elif c == "=":
            self.add_token(
                TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
            )
        elif c == "<":
            self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif c == ">":
            self.add_token(
                TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
            )
        elif c == "/":
            if self.match("/"):
                # A comment goes until the end of the line
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c in [" ", "\r", "\t"]:
            pass
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if self.is_digit(c):
                self.number()
            elif self.is_alpha(c):
                self.identifier()
            else:
                error_reporter.error(self.line, "Unexpected character.")

    def identifier(self) -> None:
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.src[self.start : self.current]
        if text not in self.keywords:
            self.add_token(TokenType.IDENTIFIER)
        else:
            self.add_token(self.keywords[text])

    def number(self) -> None:
        while self.is_digit(self.peek()):
            self.advance()

        # Look for a fractional part
        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.peek().isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.src[self.start : self.current]))

    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            # Supports multi-line strings
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            error_reporter.error(self.line, "Unterminated string.")
            return

        # The closing "
        self.advance()

        # Trim the surrounding quotes
        value = self.src[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False

        if self.src[self.current] != expected:
            return False

        # Only consume current character if it is what we
        # are looking for
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.src[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.src):
            return "\0"
        return self.src[self.current + 1]

    def is_alpha(self, c: str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    def is_alpha_numeric(self, c: str) -> bool:
        return self.is_alpha(c) or self.is_digit(c)

    def is_digit(self, c: str) -> bool:
        return c >= "0" and c <= "9"
