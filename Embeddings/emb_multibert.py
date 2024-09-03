from util.imports import *
from util.helpers import *
from util.objects import *
from util.locations import *
from util.variables import *

from transformers import BertTokenizer, BertModel
model_name = "bert-base-multilingual-cased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

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
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

            with torch.no_grad():
                outputs = model(**inputs)

            embedding = outputs.last_hidden_state[0, 0, :].tolist()

            embeddings_list.append(embedding)
            pbar.update(1)

        pbar.close()

        df['sentence-bert-multi'] = embeddings_list

        df.to_csv(filepath, index=False)
        print(f"Fichier '{filename}' mis à jour avec les embeddings de {model_name} et sauvegardé avec succès.")

co2: float = tracker.stop()
emission_kwh = co2 * CO2_TO_KWH
print(f'Emission: {emission_kwh}')