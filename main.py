import csv
import argparse
from tabulate import tabulate
import pytest


def read_economic_files(paths):
    data = []
    for path in paths:
        with open(path, 'r', encoding='utf-8') as file:
            data.append([row for row in csv.reader(file)])
    return data


def calculate_avg():


def setup_parser():
    parser = argparse.ArgumentParser(
        prog='AnalysisMacroeconomicData',
        description='Программа для анализа макроэкономических данных',
        epilog='Для получения сведений об определенной команде наберите help <имя команды>'
    )
    parser.add_argument('--files', type=str, nargs='+', required=True, help='Входные файлы для анализа')
    parser.add_argument('--report', type=str, choices=['average-gdp'], required=True, help='Тип создаваемого отчета')

    args = parser.parse_args()
    print(args.files)
    print(read_economic_files(args.files))


setup_parser()

'''if __name__ == '__main__':
    setup_parser()'''

'''table = read_economic_files('economic1.csv', 'economic2.csv')

print(tabulate(table, headers="firstrow"))'''
