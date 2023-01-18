import subprocess


def test_equality():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/bool_scripts/equality.lox",
        ],
        capture_output=True,
    )
    assert (
        res.stdout
        == b"True\nFalse\nFalse\nTrue\nFalse\nFalse\nFalse\nFalse\nFalse\nFalse\nTrue\nTrue\nFalse\nTrue\nTrue\nTrue\nTrue\nTrue\n"
    )


def test_not():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/bool_scripts/not.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"False\nTrue\nTrue\n"
