import subprocess


def test_line_at_eof():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/comments_scripts/line_at_eof.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"ok\n"

def test_only_line_comment():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/comments_scripts/only_line_comment.lox",
        ],
        capture_output=True,
    )
    assert len(res.stderr) == 0

def test_only_line_comment_and_line():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/comments_scripts/only_line_comment_and_line.lox",
        ],
        capture_output=True,
    )
    assert len(res.stderr) == 0

def test_unicode():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/comments_scripts/unicode.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"ok\n"