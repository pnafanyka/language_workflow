import pandas as pd
import typing
import parsing_elan as pe
import os


path_to_elans = '/Users/andrejpihtin/учеба/Науканский/file_ed/elans'
path_to_xlsx = '/Users/andrejpihtin/учеба/Науканский/file_ed/xlsx'

story_list = ['DEA_raven and fox_240623.xlsx',
              'MGI_skull tale_250722.xlsx',
              'VAA_dog bublik_170822.xlsx']


# reading all xlsx into one file
# for i in story_list:
#     read = pe.xlsx_to_df(f'{ABS_PATH}/{i}')  # возвращает список, 0 - сначала файл 1 - имя файля без расширения
#     pe.df_to_xlsx('one', read[0])


# iterating over elan files making xlsx: добавляем новые эксель таблицы, если раньше их не существовало
for file in os.listdir(path_to_elans):
    if file != '.DS_Store':  # автоматический файл от mac os :/
        if f"{file.rstrip('.eaf')}.xlsx" not in os.listdir(path_to_xlsx):
            path_to_eaf = path_to_elans + '/' + file  # прописали путь до елана
            obj = pe.read_file(path_to_eaf)  # прочитали в датафрейм елан
            pe.df_to_xlsx('one', obj)
            print('new file' + ' ' + obj[1])
