import configparser
import pathlib
import qrcode
import csv

fini = 'sberqr.ini'
oini = configparser.ConfigParser()
oini.read('sberqr.ini', encoding='utf-8') # cp1251
sQR1 = 'ST00012|Name='+oini.get('Acc','Name') + '|PersonalAcc=' + oini.get('Acc','PersonalAcc') + '|BankName=' + oini.get('Acc','BankName') + '|BIC=' + oini.get('Acc','BIC') + '|CorrespAcc=' + oini.get('Acc','CorrespAcc') + '|KPP=' + oini.get('Acc','KPP') + '|PayeeINN=' + oini.get('Acc','PayeeINN')
sQR2 = '|CBC=' + oini.get('Acc','CBC') + '|OKTMO=' + oini.get('Acc','OKTMO')
incsv = oini.get('Path','incsv')
outqr = oini.get('Path','outqr')


import PySimpleGUI as sg

layout = [[sg.Text('Назначение платежа: ')],
                [sg.InputText(key='-NPAY-')],
                [sg.Text('Сумма (в копейках, целое число): ')],
                [sg.InputText(key='-SMPAY-')],
                [sg.Text('Имя QR файла: ')],
                [sg.InputText(key='-NFQR-')],
                [sg.Button('Создать QR', enable_events=True, key='-GENQR-')]]

window = sg.Window('МБУ "ЦДС ГПТ"', layout, icon='ep_logo.ico')

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exin'):
        break
    if event == '-GENQR-':
        text_npay = values['-NPAY-']
        text_nsum = values['-SMPAY-']
        text_nfqr = values['-NFQR-'] 
        sQR = sQR1 + '|Purpose=' + text_npay + sQR2 + '|Sum=' + text_nsum
        fqr = text_nfqr + '.png'
        img = qrcode.make(sQR)
        img.save(outqr + fqr)
        sg.popup('Сгенерирован QR код в файл: ', outqr + text_nfqr + '.png', icon='ep_logo.ico')

window.close()

# в ехе
# pyinstaller --onefile --noconsole SberQR.py
