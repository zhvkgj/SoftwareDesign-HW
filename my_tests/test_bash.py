from my_bash_lib.bash import run_bash


def test_A():
    assert run_bash() == 0


def test_B():
    assert run_bash() == 1
