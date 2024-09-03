from util.imports import * 
from front import MODELS, get_fasttext_embedding, get_laser_embedding, get_nearests_solutions, load_model

# Chargement du fichier Excel
excel_file = "Exemple de prompts.xlsx"
df = pd.read_excel(excel_file)

# Initialiser un dictionnaire pour stocker les classements des modèles
model_ranks = defaultdict(list)

# Parcourir les lignes du DataFrame
for index, row in df.iterrows():
    prompt = row["Prompt"]
    code_k = row.get("Code K", ) 
    
    if pd.isna(code_k):
        continue 
    
    # Pour chaque modèle
    for model_choice in MODELS:
        if model_choice == "Croissant":
            continue
        print(model_choice)
        # Charger le modèle et tokenizer approprié
        tokenizer, model, csv_path = load_model(model_choice)

        # Obtenir l'embedding approprié selon le modèle choisi
        if model_choice == "Fasttext":
            embedding = get_fasttext_embedding(prompt, model)
        elif model_choice == "LASER":
            embedding = get_laser_embedding(prompt, model)
        elif model_choice == "Croissant":
            embedding = model.encode([prompt])
            embedding = [embedding[0][i] for i in range(len(embedding[0]))]
        else:
            inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=512)
            with torch.no_grad():
                outputs = model(**inputs)

            embedding = outputs.last_hidden_state[0, 0, :].tolist()
        # Calculer les solutions les plus proches
        nearest_solutions = get_nearests_solutions(model_choice=model_choice, csv_file=22, K=1200, csv_path=csv_path, target_embedding=embedding)

        # Récupérer le rang du prompt en fonction de son score de similarité
        rank = next((i+1 for i, solution in enumerate(nearest_solutions) if solution[0] == code_k), None)
        model_ranks[model_choice].append(rank)

# Calculer les moyennes des rangs pour chaque modèle
mean_ranks = {model_choice: np.mean(ranks) for model_choice, ranks in model_ranks.items()}

# Trier les moyennes des rangs
sorted_mean_ranks = dict(sorted(mean_ranks.items(), key=lambda item: item[1]))

# Extraire les noms de modèle et les moyennes des rangs triés
model_names = list(sorted_mean_ranks.keys())
mean_ranks_values = list(sorted_mean_ranks.values())

# Créer le graphique avec Plotly
fig = go.Figure(data=[go.Bar(x=model_names, y=mean_ranks_values)])
fig.update_layout(title='Évaluation des modèles',
                  xaxis_title='Modèle',
                  yaxis_title='Moyenne des rangs')
fig.show()
