import os
import os
import re
import pandas as pd
import PySimpleGUI as sg

# GUI
sg.theme('DarkTeal7')
layout = [ [sg.Text('Select the target file.')],
            [sg.Text('file name', size=(15, 1)), sg.Input(), sg.FileBrowse('Select', key='inputFilePath')],
            [sg.Button('submit', key='submit'), sg.Button('exit', key='exit')],
            [sg.Output(size=(80,20))]]
window = sg.Window('Oligonucleotide Melting Temperature Calculator', layout)

def text2list(text):
    text_list = text.split('\n')
    ids, titles, authors, affiliationses, _, *bodies = text_list
    return [ids, titles, authors, affiliationses, [*bodies]]

while True:
    event, values = window.read()

    if event in [sg.WIN_CLOSED, 'exit']:
        break

    else:
        try:
            path = values['inputFilePath']
            if not os.path.exists(path):
                print('The file doesn\'t exitst.')
                continue

            with open(path, 'r', encoding='UTF-8') as f:
                texts = f.read()
                texts_list = list(map(lambda text: text2list(text), texts.split('\n\n\n\n')))
                print(texts_list)
                article_df = pd.DataFrame(texts_list, columns=['id', 'title', 'author', 'affiliations', 'body'])

                print(article_df)
                out_path = re.sub('.txt', '_out.csv', path)
                article_df.to_csv(out_path)

                print('\nThe file is successfully saved: {out_path}')
                print('\nTo import this csv, `df.read_csv({out_path})`')

        except Exception as e:
            print(e)

window.close

