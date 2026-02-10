import main


def test_read_single_file():
    assert main.read_economic_single_file('asdfasf.py') == []

