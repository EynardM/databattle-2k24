FLAGS = ['include_description', 'include_technos', 'include_last_techno_description',
             'include_synthese_economique', 'include_technique']

INDEX_TO_FLAGS = {0: ['include_description'], 1: ['include_technos'], 2: ['include_last_techno_description'],
                  3: ['include_synthese_economique'], 4: ['include_technique'], 5: ['include_description', 'include_technos'],
                  6: ['include_description', 'include_last_techno_description'], 7: ['include_description', 'include_synthese_economique'],
                  8: ['include_description', 'include_technique'], 9: ['include_technos', 'include_synthese_economique'],
                  10: ['include_technos', 'include_technique'], 11: ['include_last_techno_description', 'include_synthese_economique'],
                  12: ['include_last_techno_description', 'include_technique'], 13: ['include_synthese_economique', 'include_technique'],
                  14: ['include_description', 'include_technos', 'include_synthese_economique'],
                  15: ['include_description', 'include_technos', 'include_technique'],
                  16: ['include_description', 'include_last_techno_description', 'include_synthese_economique'],
                  17: ['include_description', 'include_last_techno_description', 'include_technique'],
                  18: ['include_description', 'include_synthese_economique', 'include_technique'],
                  19: ['include_technos', 'include_synthese_economique', 'include_technique'],
                  20: ['include_last_techno_description', 'include_synthese_economique', 'include_technique'],
                  21: ['include_description', 'include_technos', 'include_synthese_economique', 'include_technique'],
                  22: ['include_description', 'include_last_techno_description', 'include_synthese_economique', 'include_technique']}

CO2_TO_KWH = 2.32