import parsing_elan as pe
import os

# directory = os.listdir('/Users/andrejpihtin/учеба/Науканский/file_ed/elans/ready_eaf')
directory = os.listdir('/Users/andrejpihtin/учеба/Науканский/file_ed/jsons/ready_jsons')

# elans = []
# for name in directory:
#     if '.eaf' in name:
#         elans.append(name)

jsons = []
for name in directory:
    if 'json' in name:
        jsons.append(name)

# for name in elans:
#     PATH = f'elans/ready_eaf/{name}'
#     res = pe.matched_read_elan(PATH)
#     pe.df_to_json(res, name)
#     #  pe.df_to_xlsx(res, name)

for name in jsons:
    PATH = f'jsons/ready_jsons/{name}'
    pe.json_to_tsa_json(PATH, name)


# res = pe.matched_read_elan('/Users/andrejpihtin/учеба/Науканский/file_ed/elans/VAA_juggling_050822_fixed.eaf')
# pe.df_to_xlsx(res, 'DEA_raven and fox_240623')
# pe.df_to_xlsx(res, 'VAA_juggling_050822_fixed.xlsx')

