import csv
import argparse
from tabulate import tabulate
import pytest


def read_economic_single_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            #headers = next(data)
            #print(headers)
            data = list(reader)
            return data
    except FileNotFoundError:
        return []


def read_economic_multiple_files(paths):
    all_data = []

    for path in paths:
        data = read_economic_single_file(path)

        if data:
            all_data.extend(data[1:])
    return all_data


def calculate_avg(data, column_index):
    total = 0
    amount = 0

    for i in range(len(data[0])):
        for row in data[0][i]:
            try:
                value = float(row[column_index])
                total += value
                amount += 1
            except (ValueError, IndexError):
                continue
    return round(total / amount, 2) if amount > 0 else 0


def setup_parser():
    parser = argparse.ArgumentParser(
        prog='AnalysisMacroeconomicData',
        description='Программа для анализа макроэкономических данных',
        epilog='Для получения сведений об определенной команде наберите help <имя команды>'
    )
    parser.add_argument('--files', type=str, nargs='+', required=True, help='Входные файлы для анализа')
    parser.add_argument('--report', type=str, choices=['average-gdp'], required=True, help='Тип создаваемого отчета')

    args = parser.parse_args()
    data = read_economic_multiple_files(args.files)

    if args.report == 'average-gdp':
        result = calculate_avg(data, 4)

        print(result)


setup_parser()

'''if __name__ == '__main__':
    setup_parser()'''

'''table = read_economic_files('economic1.csv', 'economic2.csv')

print(tabulate(table, headers="firstrow"))'''
