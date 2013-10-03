# coding=utf-8
import csv
import math

FIRST_REGION_COL = 9  # Номер первой колонки с данными
listOfCorrelations = []  # Сюда собираем результаты
fileToRead = "stats.csv"  # Отсюда берем статистику
fileToSave = "correlation_results.csv"  # Файл для записи результатов
k, i = 0, 0  # счетчики чтения строк


def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)


def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff

    return diffprod / math.sqrt(xdiff2 * ydiff2)

f = open(fileToRead, "rb")
spamReader1 = list(csv.reader(f, dialect='excel', delimiter=','))[1:]
spamReader2 = spamReader1

for row1 in spamReader1:
    for row2 in spamReader2:
        if row1 == row2:
            continue  # Не считаем корреляцию в одинаковых строках
        # читаем данные из первой и второй строки, приводим к float
        data1 = [float(s.replace(',', '.').replace(' ', '')) for s in row1[(FIRST_REGION_COL - 1):]]
        data2 = [float(s.replace(',', '.').replace(' ', '')) for s in row2[(FIRST_REGION_COL - 1):]]
        # читаем названия показателей (short_name)
        name1 = row1[1]
        name2 = row2[1]
        correlation = pearson_def(data1, data2)
        listOfCorrelations.append([correlation, name1, name2])

f.close()

# сортируем по абсолютному значению корреляции
listOfCorrelations = sorted(listOfCorrelations, key=lambda correlations: abs(correlations[0]), reverse=True)


with open(fileToSave, "wb") as f:
    spamWriter = csv.writer(f)
    spamWriter.writerows(listOfCorrelations)
