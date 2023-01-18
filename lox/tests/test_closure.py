import subprocess


def test_assign_to_closure():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/assign_to_closure.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"local\nafter f\nafter f\nafter g\n"

def test_assign_to_shadowed_later():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/assign_to_shadowed_later.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"inner\nassigned\n"

def test_close_over_function_parameter():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/close_over_function_parameter.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"param\n"

def test_close_over_later_variable():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/close_over_later_variable.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"b\na\n"

def test_close_over_method_parameter():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/close_over_method_parameter.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"param\n"

def test_closed_closure_in_function():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/closed_closure_in_function.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"local\n"

def test_nested_closure():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/nested_closure.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"a\nb\nc\n"

def test_open_closure_in_function():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/open_closure_in_function.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"local\n"

def test_reference_closure_multiple_times():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/reference_closure_multiple_times.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"a\na\n"

def test_reuse_closure_slot():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/reuse_closure_slot.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"a\n"

def test_shadow_closure_with_local():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/shadow_closure_with_local.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"closure\nshadow\nclosure\n"

def test_unused_closure():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/unused_closure.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"ok\n"

def test_unused_later_closure():
    res = subprocess.run(
        [
            "python",
            "lox/lox.py",
            "-s",
            "lox/tests/closure_scripts/unused_later_closure.lox",
        ],
        capture_output=True,
    )
    assert res.stdout == b"a\n"