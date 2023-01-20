import subprocess


def test_arguments():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/constructor_scripts/arguments.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"init\n1\n2\n"

def test_call_init_early_return():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/constructor_scripts/call_init_early_return.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"init\ninit\nFoo instance\n"

def test_call_init_explicitly():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/constructor_scripts/call_init_explicitly.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"Foo.init(one)\nFoo.init(two)\nFoo instance\ninit\n"

def test_default():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/constructor_scripts/default.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"Foo instance\n"

def test_default_arguments():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/constructor_scripts/default_arguments.lox",
        ],
        capture_output=True,
    )
    assert b"RuntimeError('Expected 0 arguments but got 3.')" in res.stderr

def test_early_return():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/constructor_scripts/early_return.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"init\nFoo instance\n"

def test_extra_arguments():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/constructor_scripts/extra_arguments.lox",
        ],
        capture_output=True,
    )
    assert b"RuntimeError('Expected 2 arguments but got 4.')" in res.stderr

def test_init_not_method():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/constructor_scripts/init_not_method.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"not initializer\n"

def test_missing_arguments():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/constructor_scripts/missing_arguments.lox",
        ],
        capture_output=True,
    )
    assert b"RuntimeError('Expected 2 arguments but got 1.')" in res.stderr

def test_return_in_nested_function():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/constructor_scripts/return_in_nested_function.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"bar\nFoo instance\n"

def test_return_value():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/constructor_scripts/return_value.lox",
        ],
        capture_output=True,
    )
    assert b"Error at 'return': Can't return a value from an initializer." in res.stderr