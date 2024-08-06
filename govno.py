import parsing_elan as pe
import pympi
import typing
import pandas as pd


def match_id(numb: str, inst: dict) -> str:
    res = ''
    keys = inst.keys()
    for key in keys:
        if inst[key][0] == numb:
            res = inst[key][1]
    return res


path_to_eaf = ('/Users/andrejpihtin/учеба/Науканский/file_ed/elans/MGI_skull tale_250722.eaf')

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
    df = pd.DataFrame(matched, columns = [
        'text',
        'gloss',
        'morpheme'])

print(eafob.tiers['Text-txt-ynk'][0])
