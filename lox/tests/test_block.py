import subprocess


def test_empty():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/block_scripts/empty.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"ok\n"

def test_scope():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/block_scripts/scope.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"inner\nouter\n"