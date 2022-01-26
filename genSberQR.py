# Библиотека для работы с ini
import configparser
# Библиотека для работы с файлами
import pathlib
# Библиотека для формирования QR
import qrcode
# Библиотка для csv
import csv

# Чтение ini файла с реквизитами
fini = 'sberqr.ini'
oini = configparser.ConfigParser()
# Читаем реквизиты банка
oini.read('sberqr.ini', encoding='utf-8') # cp1251
sQR1 = 'ST00012|Name='+oini.get('Acc','Name') + '|PersonalAcc=' + oini.get('Acc','PersonalAcc') + '|BankName=' + oini.get('Acc','BankName') + '|BIC=' + oini.get('Acc','BIC') + '|CorrespAcc=' + oini.get('Acc','CorrespAcc') + '|KPP=' + oini.get('Acc','KPP') + '|PayeeINN=' + oini.get('Acc','PayeeINN')
sQR2 = '|CBC=' + oini.get('Acc','CBC') + '|OKTMO='+oini.get('Acc','OKTMO')
# Читаем пути к файлам
incsv = oini.get('Path','incsv')
print('Путь к исходным файлам: ' + incsv)
outqr = oini.get('Path','outqr')
print('Путь к файлам c QR кодом: ' + outqr)

# Обход по исходным файлам согласно маске
csvdir = pathlib.Path(incsv)
for csvfi in csvdir.glob('transactions*.csv'):
    print(csvfi)
    # Сканируем текщий файл csv
    with open(csvfi) as csvfile:
        # Читаем содержимое csv
        reader = csv.DictReader(csvfile, delimiter=';')
        # Обходим содержимое построчно
        for row in reader:
            # данные в QR
            sQR = sQR1 + '|Purpose=Погашение поездки ' + row['Reference number'] + ' ' + row['terminal_date'].replace('T',' ') + ' ' + row['Номер карты'] + sQR2 + '|Sum=0'
            # имя конечного файла
            fqr = row['Номер карты'] + '.png'
            # генерируем qr-код
            img = qrcode.make(sQR)
            # сохраняем img в файл
            img.save(outqr + fqr)

print('ГОТОВО!')

# в ехе
# pyinstaller --onefile genSberQR.py