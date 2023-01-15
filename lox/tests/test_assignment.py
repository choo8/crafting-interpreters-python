import subprocess


def test_associativity():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/assignment_scripts/associativity.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"c\nc\nc\n"


def test_global():
    res = subprocess.run(
        ["python", "lox/lox.py", "-s", "lox/tests/assignment_scripts/global.lox"],
        capture_output=True,
    )
    assert res.stdout == b"before\nafter\narg\narg\n"


def test_grouping():
    res = subprocess.run(
        ["python", "lox/lox.py", "-s", "lox/tests/assignment_scripts/grouping.lox"],
        capture_output=True,
    )
    assert b"Error at '=': Invalid assignment target." in res.stderr


def test_infix_operator():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/assignment_scripts/infix_operator.lox",
        ],
        capture_output=True,
    )
    assert b"Error at '=': Invalid assignment target." in res.stderr


def test_local():
    res = subprocess.run(
        ["python", "lox/lox.py", "-s", "lox/tests/assignment_scripts/local.lox"],
        capture_output=True,
    )
    assert res.stdout == b"before\nafter\narg\narg\n"


def test_prefix_operator():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/assignment_scripts/prefix_operator.lox",
        ],
        capture_output=True,
    )
    assert b"Error at '=': Invalid assignment target." in res.stderr


def test_syntax():
    res = subprocess.run(
        ["python", "lox/lox.py", "-s", "lox/tests/assignment_scripts/syntax.lox"],
        capture_output=True,
    )
    assert res.stdout == b"var\nvar\n"


def test_to_this():
    res = subprocess.run(
        ["python", "lox/lox.py", "-s", "lox/tests/assignment_scripts/to_this.lox"],
        capture_output=True,
    )
    assert b"Error at '=': Invalid assignment target." in res.stderr


def test_undefined():
    res = subprocess.run(
        ["python", "lox/lox.py", "-s", "lox/tests/assignment_scripts/undefined.lox"],
        capture_output=True,
    )
    assert b"RuntimeError(\"Undefined variable 'unknown'.\")" in res.stderr
