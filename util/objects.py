from util.imports import *

class UseCase:
    def __str__(self):
        return "UseCase"

class Techno:
    def __init__(self, id, description):
        self.id = id
        self.description = description

    def __str__(self):
        return f"Techno: ID={self.id}, Description={self.description}"

class SyntheseEconomique:
    def __init__(self, regle, difficultes, gain, effets_positifs):
        self.regle = regle
        self.difficultes = difficultes
        self.gain = gain
        self.effets_positifs = effets_positifs

    def __str__(self):
        return f"SyntheseEconomique: Regle={self.regle}, Difficultes={self.difficultes}, Gain={self.gain}, EffetsPositifs={self.effets_positifs}"

class Technique:
    def __init__(self, definition, application, bilan_energetique):
        self.definition = definition
        self.application = application
        self.bilan_energetique = bilan_energetique

    def __str__(self):
        return f"Technique: Definition={self.definition}, Application={self.application}, BilanEnergetique={self.bilan_energetique}"

class Solution:
    def __init__(self, id, description, technos: List[Techno], synthese_economique: SyntheseEconomique,
                technique: Technique, use_case: UseCase):
        self.id = id
        self.description = description
        self.technos = technos
        self.synthese_economique = synthese_economique
        self.technique = technique
        self.use_case = use_case
  
    def concat_text(self, include_description=True, include_technos=True, include_last_techno_description=False,
                    include_synthese_economique=True, include_technique=True):
        concatenated_parts = []

        if include_description:
            concatenated_parts.append(self.description)

        if include_technos:
            technos_description = ", ".join([techno.description for techno in self.technos])
            concatenated_parts.append(technos_description)

        if include_last_techno_description and self.technos:
            last_techno_description = self.technos[0].description
            concatenated_parts.append(last_techno_description)

        if include_synthese_economique:
            synthese_text = ", ".join(filter(None, [self.synthese_economique.regle, self.synthese_economique.difficultes,
                                                    self.synthese_economique.gain, self.synthese_economique.effets_positifs]))
            concatenated_parts.append(synthese_text)

        if include_technique:
            technique_text = ", ".join(filter(None, [self.technique.definition, self.technique.application, self.technique.bilan_energetique]))
            concatenated_parts.append(technique_text)

        return ", ".join(concatenated_parts)

    def __str__(self):
        return f"Solution: ID={self.id}, Description={self.description}\n, Technos={self.technos}, SyntheseEconomique={self.synthese_economique}, Technique={self.technique}, UseCase={self.use_case}"