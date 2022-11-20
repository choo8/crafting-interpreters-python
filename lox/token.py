from token_type import TokenType


class Token:
    def __init__(self, type: TokenType, lexme: str, literal: object, line: int):
        self.type = type
        self.lexme = lexme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexme} {self.literal}"
