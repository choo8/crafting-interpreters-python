import subprocess


def test_bool():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/call_scripts/bool.lox",
        ],
        capture_output=True,
    )
    assert b"RuntimeError('Can only call functions and classes.')" in res.stderr

def test_nil():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/call_scripts/nil.lox",
        ],
        capture_output=True,
    )
    assert b"RuntimeError('Can only call functions and classes.')" in res.stderr

def test_num():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/call_scripts/num.lox",
        ],
        capture_output=True,
    )
    assert b"RuntimeError('Can only call functions and classes.')" in res.stderr

def test_object():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/call_scripts/object.lox",
        ],
        capture_output=True,
    )
    assert b"RuntimeError('Can only call functions and classes.')" in res.stderr

def test_string():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/call_scripts/string.lox",
        ],
        capture_output=True,
    )
    assert b"RuntimeError('Can only call functions and classes.')" in res.stderr