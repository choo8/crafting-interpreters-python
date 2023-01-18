import subprocess


def test_empty():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/class_scripts/empty.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"Foo\n"

def test_inherit_self():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/class_scripts/inherit_self.lox",
        ],
        capture_output=True,
    )
    assert b"Error at 'Foo': A class can't inherit from itself." in res.stderr

def test_inherited_method():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/class_scripts/inherited_method.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"in foo\nin bar\nin baz\n"

def test_local_inherit_other():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/class_scripts/local_inherit_other.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"B\n"

def test_local_inherit_self():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/class_scripts/local_inherit_self.lox",
        ],
        capture_output=True,
    )
    assert b"Error at 'Foo': A class can't inherit from itself." in res.stderr

def test_local_reference_self():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/class_scripts/local_reference_self.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"Foo\n"

def test_reference_self():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/class_scripts/reference_self.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"Foo\n"