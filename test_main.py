import importlib
import sys
import types
import pytest


def import_main_for_test(monkeypatch):
    """Безопасный импорт main.py внутри теста."""
    monkeypatch.setitem(sys.modules, 'tabulate', types.SimpleNamespace(tabulate=lambda *args, **kwargs: 'table'))
    monkeypatch.setattr(sys, 'argv', ['main.py', '--files', 'economic1.csv', '--report', 'average-gdp'])
    sys.modules.pop('main', None)
    return importlib.import_module('main')


def test_read_economic_single_file(monkeypatch, tmp_path):
    main = import_main_for_test(monkeypatch)
    file_path = tmp_path / 'single.csv'
    file_path.write_text('country,year,gdp\nA,2023,100\n', encoding='utf-8')

    assert main.read_economic_single_file(str(file_path)) == [
        ['country', 'year', 'gdp'],
        ['A', '2023', '100'],
    ]
    assert main.read_economic_single_file(str(tmp_path / 'missing.csv')) == []


def test_read_economic_multiple_files(monkeypatch, tmp_path):
    main = import_main_for_test(monkeypatch)
    f1 = tmp_path / 'f1.csv'
    f2 = tmp_path / 'f2.csv'
    f1.write_text('country,year,gdp\nA,2023,100\n', encoding='utf-8')
    f2.write_text('country,year,gdp\nB,2023,200\n', encoding='utf-8')

    data = main.read_economic_multiple_files([str(f1), str(f2), str(tmp_path / 'none.csv')])
    assert data == [['A', '2023', '100'], ['B', '2023', '200']]


def test_calculate_avg(monkeypatch):
    main = import_main_for_test(monkeypatch)
    rows = [
        ['A', '2023', '100'],
        ['A', '2022', '200'],
        ['B', '2023', '50'],
        ['B', '2022', '100'],
    ]

    assert main.calculate_avg(rows, 2) == [
        [1, 'A', '150.00'],
        [2, 'B', '75.00'],
    ]


def test_setup_parser_unknown_report_raises_error(monkeypatch, tmp_path):
    main = import_main_for_test(monkeypatch)

    class FakeArgs:
        files = [str(tmp_path / 'data.csv')]
        report = 'unknown'

    monkeypatch.setattr(main.argparse.ArgumentParser, 'parse_args', lambda _self: FakeArgs())

    with pytest.raises(ValueError, match='Неизвестный тип отчета'):
        main.setup_parser()


def test_setup_parser_average_gdp_success(monkeypatch, tmp_path):
    main = import_main_for_test(monkeypatch)
    data_file = tmp_path / 'ok.csv'
    data_file.write_text('country,year,gdp\nA,2023,100\nA,2022,200\n', encoding='utf-8')

    class FakeArgs:
        files = [str(data_file)]
        report = 'average-gdp'

    monkeypatch.setattr(main.argparse.ArgumentParser, 'parse_args', lambda _self: FakeArgs())

    result = main.setup_parser()
    assert result == [[1, 'A', '150.00']]
