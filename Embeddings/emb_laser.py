from util.imports import *
from util.locations import * 
from util.variables import *
from laserembeddings import Laser

model = Laser()
model_name = "laser"
tracker = EmissionsTracker()
tracker.start()

for filename in os.listdir(CSV_PATH):
    if filename.endswith(".csv"):
        filepath = os.path.join(CSV_PATH, filename)
        df = pd.read_csv(filepath)

        pbar = tqdm(total=len(df), desc=f"Processing {filename}", unit="rows")

        embeddings_list = []
        for index, row in df.iterrows():
            text = str(row["Text"])
            embedding = model.embed_sentences([text],lang='fr')
            embeddings_list.append(embedding[0])
            pbar.update(1)

        pbar.close()

        df["fasttext-fr-vectors"] = embeddings_list

        df.to_csv(filepath, index=False)
        print(f"Fichier '{filename}' mis à jour avec les embeddings de {model_name} et sauvegardé avec succès.")

co2: float = tracker.stop()
emission_kwh = co2 * CO2_TO_KWH
print(f'Emission: {emission_kwh}')