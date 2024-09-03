import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from front import get_fasttext_embedding, get_laser_embedding, get_nearests_solutions, load_model

# Chargement du fichier Excel
excel_file = "Exemple de prompts.xlsx"
df = pd.read_excel(excel_file)

# Initialiser un dictionnaire pour stocker les classements des modèles
model_ranks = defaultdict(list)

# Parcourir les lignes du DataFrame
for index, row in df.iterrows():
    prompt = row["Prompt"]
    code_k = row.get("Code K", None)  # Si le Code K est manquant, il sera None

    # Pour chaque modèle
    for model_choice in ["Fasttext", "LASER"]:
        # Charger le modèle et tokenizer approprié
        tokenizer, model, csv_path = load_model(model_choice)

        # Obtenir l'embedding approprié selon le modèle choisi
        if model_choice == "Fasttext":
            embedding = get_fasttext_embedding(prompt, model)
        elif model_choice == "LASER":
            embedding = get_laser_embedding(prompt, model)

        # Calculer les solutions les plus proches
        nearest_solutions = get_nearests_solutions(model_choice=model_choice, csv_file=22, K=10, csv_path=csv_path, target_embedding=embedding)

        # Récupérer le rang du prompt en fonction de son score de similarité
        rank = next((i+1 for i, solution in enumerate(nearest_solutions) if solution[0] == code_k), None)
        model_ranks[model_choice].append(rank)

# Calculer les moyennes des rangs pour chaque modèle
mean_ranks = {model_choice: np.mean(ranks) for model_choice, ranks in model_ranks.items()}

# Trier les moyennes des rangs
sorted_mean_ranks = dict(sorted(mean_ranks.items(), key=lambda item: item[1]))

# Afficher les résultats
print("Moyennes des rangs pour chaque modèle:")
for model_choice, mean_rank in sorted_mean_ranks.items():
    print(f"{model_choice}: {mean_rank}")

# Plot des résultats
plt.bar(sorted_mean_ranks.keys(), sorted_mean_ranks.values())
plt.xlabel('Modèle')
plt.ylabel('Moyenne des rangs')
plt.title('Évaluation des modèles')
plt.show()
