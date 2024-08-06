import json

import pympi
import pandas as pd
import typing
import re


def match_id(numb: str, inst: dict) -> str:
    res = ''
    keys = inst.keys()
    for key in keys:
        if inst[key][0] == numb:
            res = inst[key][1]
    return res


def get_closest(tiers: list, key: str) -> str:
    closest_str = 'huy'
    return closest_str


def find_pos(tier: list) -> int: #возвращает номер, в котором лежат глоссы или морфемы
    number = 0
    for j in range(len(tier)):
        for i in range(len(tier[j])):
            if str(tier[j][i]).isdigit():
                pass
            elif '-' in tier[j][i]:
                number = i
                break
            else:
                pass
    return number


def make_eq(tier: list, max_len: int) -> list:
    if not max_len == len(tier):
        tier.extend([''] * (max_len - len(tier)))
    return tier


def read_elan(path_to_eaf) -> pd.DataFrame:
    eafob = pympi.Elan.Eaf(path_to_eaf)
    gloss_it = eafob.get_annotation_data_for_tier('gloss')
    morpheme_it = eafob.get_annotation_data_for_tier('morpheme')
    text_it = eafob.get_annotation_data_for_tier('Text-txt-ynk')

    glosses = []
    gloss_pos = find_pos(gloss_it)
    morphemes = []
    morph_pos = find_pos(morpheme_it)
    texts = []

    for it in gloss_it:
        glosses.append(it[gloss_pos])
    for it in morpheme_it:
        morphemes.append(it[morph_pos])
    for it in text_it:
        texts.append(it[-1])

    lens = [len(glosses), len(morphemes), len(texts)]
    max_len = max(lens)

    glosses = make_eq(glosses, max_len)
    morphemes = make_eq(morphemes, max_len)
    texts = make_eq(texts, max_len)

    d = {'text': texts, 'morphemes': morphemes, 'gloss': glosses}
    df = pd.DataFrame(d)

    return df


def create_word_structure(words: list, glosses: list, morphemes: list) -> list:
    res = []
    l = len(words)
    for i in range(l - 1):
        try:
            wd = {
                'wtype': 'word',
                'wf': words[i],
                'ana': [
                    {
                        "parts": morphemes[i],
                        "gloss": glosses[i]
                    }
                ]
            }
        except IndexError:
            wd = {
                'wtype': 'word',
                'wf': words[i],
                'ana': [
                    {
                        "parts": '',
                        "gloss": ''
                    }
                ]
            }
        res.append(wd)
    return res


def json_to_tsa_json(path_to_json, name):
    """Сохраняет файл в json для TSAKORPUS"""
    with open(path_to_json, 'r') as f:
        it = json.load(f)
    sentences = []
    for index in it['text'].keys():
        iter_dict = {
            "lang": 0,
            # "words": it['text'][index].split()
            "words": create_word_structure(it['text'][index].split(), it['gloss'][index].split(), it['morpheme'][index].split()),
            "text": it['text'][index]
        }
        sentences.append(iter_dict)
    res_dict = {
        'meta': f'{name}'.rstrip('.json'),
        'sentences': sentences
    }
    with open(f'/Users/andrejpihtin/учеба/Науканский/file_ed/jsons/tsa_js/{name}', 'w') as f:
        json.dump(res_dict, f, ensure_ascii=False)


def matched_read_elan(path_to_eaf) -> pd.DataFrame:
    eafob = pympi.Elan.Eaf(path_to_eaf)
    ids = eafob.tiers['Text-txt-ynk'][0].keys()
    matched = []
    for numb in ids:
        try:
            text = eafob.tiers['Text-txt-ynk'][0][numb][2]
        except KeyError:
            text = 'NaN'
        gloss = match_id(numb, eafob.tiers['gloss'][1])
        morpheme = match_id(numb, eafob.tiers['morpheme'][1])

        matched.append([text, gloss, morpheme])
    df = pd.DataFrame(matched, columns=[
            'text',
            'gloss',
            'morpheme'])

    return df


def xlsx_to_df(path_to_xlsx):
    file = pd.read_excel(path_to_xlsx)
    return [file, path_to_xlsx.rstrip('.xlsx')]


def df_to_xlsx(df: pd.DataFrame, name: str):
    name = re.sub('.eaf', '', name)
    df.to_excel(f"/Users/andrejpihtin/учеба/Науканский/file_ed/excel/{name}.xlsx")


def df_to_json(df: pd.DataFrame, name: str):
    name = re.sub('.eaf', '', name)
    df.to_json(f"/Users/andrejpihtin/учеба/Науканский/file_ed/jsons/{name}.json", index=True, force_ascii=False)