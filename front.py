from util.imports import *
from util.locations import *
import calculate_bilan as calc
from datamodule import get_solutions

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://i.pinimg.com/564x/e3/50/1d/e3501d3aa8ac3cd6e405bdfd93cd5529.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}
</style>
"""

MODELS = [
    "Camembert",
    "Multilang_Bert",
    "Fasttext",
    "LASER",
    "Croissant"
]

def load_camembert():
    tokenizer = CamembertTokenizer.from_pretrained(CAMEMBERT_TOKENIZER)
    model = CamembertModel.from_pretrained(CAMEMBERT_MODEL)
    return tokenizer, model

def load_multilang_bert():
    tokenizer = BertTokenizer.from_pretrained(MULTILANG_BERT_TOKENIZER)
    model = BertModel.from_pretrained(MULTILANG_BERT_MODEL)
    return tokenizer, model

def load_fasttext():
    model = fasttext.load_model(FASTTEXT_MODEL)
    return model

def load_laser():
    model = Laser()
    return model

def load_croissant():
    model = SentenceTransformer(CROISSANT_MODEL_TOKENIZER)
    return model

def get_fasttext_embedding(text, model):
    return model.get_sentence_vector(text)

def get_laser_embedding(text, model):
    return model.embed_sentences([text], lang='fr')

def get_nearests_solutions(model_choice, csv_file=22, K=10, csv_path=None, target_embedding=None):
    nearest_solutions = []

    if csv_path is None or not os.path.exists(csv_path):
        st.error(f"Le chemin du fichier CSV est invalide : {csv_path}")
        return nearest_solutions

    filepath = os.path.join(csv_path, f"{csv_file}.csv")

    if not os.path.exists(filepath):
        st.error(f"Le fichier CSV {csv_file}.csv n'existe pas dans le dossier {csv_path}")
        return nearest_solutions

    df = pd.read_csv(filepath)

    embeddings = []
    for index, row in df.iterrows():
        text_embedding = row["Embedding"]
        # Clean up the string representation of the embedding
        if model_choice == "Fasttext":
            text_embedding = text_embedding.strip('][')
        else:  # For BERT, Camembert, or LASER
            text_embedding = text_embedding.strip('][').replace(',', '')  # Remove commas
            text_embedding = text_embedding.replace('...', '')  # Remove ellipses
        embedding_values = [float(value) for value in text_embedding.split() if value != '']  # Remove empty values
        try:
            embeddings.append(embedding_values)
        except ValueError:
            print("Unable to convert embedding values to float:", text_embedding)  # Debugging
            continue

    embeddings = np.array(embeddings)
    target_embedding = np.array(target_embedding).reshape(1, -1)

    similarities = cosine_similarity(target_embedding, embeddings)
    top_indices = np.argsort(similarities[0])[-K:][::-1]  # Les indices des K plus grandes similarités

    unique_solutions = set()
    count = 0
    for index in top_indices:
        id_solution = df.at[index, "Solution_ID"]
        text = df.at[index, "Text"]
        similarity_score = similarities[0][index]
        if id_solution not in unique_solutions:
            nearest_solutions.append((id_solution, text, similarity_score))
            unique_solutions.add(id_solution)
            count += 1
        if count == K:
            break
    nearest_solutions = sorted(nearest_solutions, key=lambda x: x[2], reverse=True)
    return nearest_solutions

def load_model(model_choice):
    if model_choice == "Camembert":
        tokenizer, model = load_camembert()
        csv_path = CAMEMBERT_CSV 

    elif model_choice == "Multilang_Bert":
        tokenizer, model = load_multilang_bert()
        csv_path = MULTILANG_BERT_CSV

    elif model_choice == "Fasttext":
        model = load_fasttext()
        tokenizer = None
        csv_path = FASTTEXT_CSV

    elif model_choice == "LASER":
        model = load_laser()
        tokenizer = None
        csv_path = LASER_CSV

    elif model_choice == "Croissant":
        model = load_croissant()
        tokenizer = None
        csv_path = CROISSANT_CSV
    return tokenizer, model, csv_path

def afficher_resultats_streamlit(results):
    print(results)
    solution_id = results["solution"]
    cout_financier = results["cout_financier"]
    gain_financier = results["gain_financier"]
    eco_energie = results["eco_energie"]
    GES = results["GES"]

    st.header(f"Résultats pour la solution {solution_id}:")
    
    if cout_financier and any(cout_financier.values()):
        st.subheader("Coût financier:")
        if cout_financier["moyenne"] is not None:
            st.write("Moyenne:", cout_financier["moyenne"])
        else:
            st.write("Moyenne:", "None")
        if not pd.isnull(cout_financier["ecart_type"]):
            st.write("Écart-type:", cout_financier["ecart_type"])
        else:
            st.write("Écart-type:", "nan")

    if gain_financier and any(gain_financier.values()):
        st.subheader("Gain financier:")
        if gain_financier["moyenne"] is not None:
            st.write("Moyenne:", gain_financier["moyenne"])
        else:
            st.write("Moyenne:", "None")
        if not pd.isnull(gain_financier["ecart_type"]):
            st.write("Écart-type:", gain_financier["ecart_type"])
        else:
            st.write("Écart-type:", "nan")

    if eco_energie and any(eco_energie.values()):
        st.subheader("Économie d'énergie:")
        if eco_energie["moyennes"]:
            st.write("Moyennes par unité:", eco_energie["moyennes"])
        else:
            st.write("Moyennes par unité:", "None")
        if not pd.isnull(eco_energie["ecart_type"]):
            st.write("Écart-type:", eco_energie["ecart_type"])
        else:
            st.write("Écart-type:", "nan")

    if GES and any(GES.values()):
        st.subheader("GES:")
        if GES["moyenne"] is not None:
            st.write("Moyenne:", GES["moyenne"])
        else:
            st.write("Moyenne:", "None")
        if not pd.isnull(GES["ecart_type"]):
            st.write("Écart-type:", GES["ecart_type"])
        else:
            st.write("Écart-type:", "nan")



def click_button():
    st.session_state.clicked = True

def main():
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False
    st.markdown(background_image, unsafe_allow_html=True)
    html = '''
    <h1 style="color:white">CY-MBALES - DATACHALLENGE 2024</h1>
    '''
    st.markdown(html, unsafe_allow_html=True)
    # Chemin vers le fichier GIF
    gif_path = "kerdos.gif"

    # Affichage du GIF
    st.image(gif_path, use_column_width=True)
    model_choice = st.selectbox("Choix du modèle :", MODELS)
    
    # Afficher le bouton avec les styles CSS personnalisés
    if st.button("Charger le modèle", key="custom_button"):
        tokenizer, model, csv_path = load_model(model_choice)
        st.session_state.model_choice = model_choice
        st.session_state.tokenizer = tokenizer
        st.session_state.model = model
        st.session_state.csv_path = csv_path
    
    if "model_choice" not in st.session_state:
        st.warning("Veuillez d'abord charger un modèle.")
    else:
        model_choice = st.session_state.model_choice
        tokenizer = st.session_state.tokenizer
        model = st.session_state.model
        csv_path = st.session_state.csv_path
        
        if "query_input" not in st.session_state:
            st.session_state.query_input = ""

        csv_number = st.number_input("Choisir le numéro du fichier CSV :", min_value=0, max_value=22, value=22, step=1, key="csv_number")
        requete = st.text_area("Saisir une requête :", value=st.session_state.query_input, key="query_input", height=50)
        k = st.slider("Nombre de solutions les plus proches (K) :", min_value=1, max_value=50, value=10, step=1)

        solutions = []
        solutions = st.session_state.get("solutions", [])
        st.button("Rechercher",on_click=click_button)
        if st.session_state.clicked:
            if requete:
                if model_choice == "Fasttext":
                    embedding = get_fasttext_embedding(requete, model)
                    nearest_solutions = get_nearests_solutions(model_choice="Fasttext", csv_file=csv_number, K=k, csv_path=csv_path, target_embedding=embedding)
                elif model_choice == "LASER":
                    embedding = get_laser_embedding(requete, model)
                    nearest_solutions = get_nearests_solutions(model_choice="LASER", csv_file=csv_number, K=k, csv_path=csv_path, target_embedding=embedding)
                else:
                    inputs = tokenizer(requete, return_tensors="pt", padding=True, truncation=True, max_length=512)

                    with torch.no_grad():
                        outputs = model(**inputs)

                    embedding = outputs.last_hidden_state[0, 0, :].tolist()
                    nearest_solutions = get_nearests_solutions(model_choice=model_choice, csv_file=csv_number, K=k, csv_path=csv_path, target_embedding=embedding)
                
        
                st.write("""
                    <div style="text-align: center;margin:20px 0px 20px 0px;">
                        <h3>SOLUTIONS LES PLUS PROCHES</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                solutions = []
                solution_list = get_solutions()
                for solution in nearest_solutions:
                    if len(solutions)<len(nearest_solutions):
                            solutions.append(int(solution[0]))
                    solution_id = solution[0]
                    similarity_score = solution[2]
                    for sol_obj in solution_list:
                        if sol_obj.id == solution_id:
                            synthese_eco_obj = sol_obj.synthese_economique
                            technique_obj = sol_obj.technique
                            techno_obj = sol_obj.technos
                            
                            # Affichage de la description et de l'id
                            st.markdown("<div style='margin-top: 50px></div>", unsafe_allow_html=True)
                            sol_container = st.container(border=True)
                            sol_container.write("""
                            <div style="background-color:#17f617 ;display:flex;flex-direction:flex-start; text-align: center;margin:20px 20px 20px 20px;border-radius:8px;">            
                                <h3 style="color:#1f0856">K {id} : {description}</h3>
                            </div>
                            """.format(id=sol_obj.id, description=sol_obj.description), unsafe_allow_html=True)
                            

                            # Affichage des Technologie

                            if None in techno_obj:
                                sol_container.write("""
                                        <div style="display:flex; flex-direction:column; text-align: center;">
                                            <h4>Technologie : {techno1} ({id1}) </h4>
                                            <p>{techno} ({id})</p>
                                        </div>
                                        """.format(id=techno_obj[-1].id, techno=techno_obj[-1].description,
                                                techno1=techno_obj[0].description,id1=techno_obj[0].id),unsafe_allow_html=True)

                            elif all(element is not None for element in techno_obj):
                                sol_container.write("""
                                        <div style="display:flex; flex-direction:column; text-align: center;">
                                            <h4>Technologie : {techno1} ({id1}) </h4>
                                            <p>{techno} ({id}) - {techno2} ({id2})</p>
                                        </div>
                                        """.format(id=techno_obj[-1].id, techno=techno_obj[-1].description,
                                                techno1=techno_obj[0].description,id1=techno_obj[0].id, techno2=techno_obj[1].description,
                                                id2=techno_obj[1].id), unsafe_allow_html=True)
                                
                            # Affichage de la synthèse économique si elle existe
                            
                            if synthese_eco_obj.regle !=None or synthese_eco_obj.difficultes!=None or synthese_eco_obj.gain!=None or synthese_eco_obj.effets_positifs!=None:
                                
                                container_synth_eco = sol_container.container(border=True)
                                container_synth_eco.write("""
                                        <div style="display:flex; flex-direction:flex-start; text-align: center;justify-content:center";>
                                            <h4 sytle="justify-content:center;align-items;display:flex">Synthèse économique</h4>
                                        </div>
                                        """, unsafe_allow_html=True)
                                
                                col1, col2 = container_synth_eco.columns(2)
                                container_cout=col1.container(border=True)
                                container_gain=col2.container(border=True)
                                
                                # Les coûts
                            
                                with col1:
                                    container_cout.write("""
                                                        <div style="background-color:#e60000;margin:20px 10px 20px 10px;padding-top:10px; text-align: center;border-radius:8px;align-items:center;justify-content:center">
                                                            <h5>Coûts</h5>
                                                        </div>
                                                        """,unsafe_allow_html=True)
                                    if synthese_eco_obj.regle != None: 
                                        container_cout.write(f"Règle du pouce :\n{synthese_eco_obj.regle}")
                                    if synthese_eco_obj.difficultes != None:
                                        container_cout.write(f"Difficultés :\n{synthese_eco_obj.difficultes}")

                                # Les gains
                                with col2:
                                    container_gain.write("""
                                                        <div style="background-color:#52ce12;margin:20px 10px 20px 10px;padding-top:10px; text-align: center;border-radius:8px;align-items:center;justify-content:center">
                                                            <h5>Gains</h5>
                                                        </div>
                                                        """, unsafe_allow_html=True)
                                    if synthese_eco_obj.gain != None:
                                        container_gain.write(f"Gain :\n{synthese_eco_obj.gain}")
                                    if synthese_eco_obj.effets_positifs != None:
                                        container_gain.write(f"Effets positifs :\n{synthese_eco_obj.effets_positifs}")

                            # Affichage de l'onglet technique

                            if technique_obj.definition!=None or technique_obj.bilan_energetique!=None or technique_obj.application!=None:
                                container_technique = sol_container.container(border=True)
                                container_technique.write("""
                                        <div style="display:flex; flex-direction:flex-start; text-align: center;justify-content:center">
                                            <h4>Technique</h4>
                                        </div>
                                        """, unsafe_allow_html=True)
                                
                                # Pour la défintion dans Technique
                                if technique_obj.definition != None: 
                                    container_def = container_technique.container(border=True)
                                    container_def.write("""
                                                        <div style="background-color:#5d5dff;margin:20px 10px 20px 10px;display:flex;padding-top:10px;flex-direction:flex-start; text-align: center;border-radius:8px">
                                                            <h5>Définition</h5>
                                                        </div>
                                                        """,unsafe_allow_html=True)
    
                                    container_def.write(f"{technique_obj.definition}")
                                
                                # Pour l'application dans Technique 
                                if technique_obj.application != None: 
                                    container_appli = container_technique.container(border=True)
                                    container_appli.write("""
                                                        <div style="background-color:#7070ff;margin:20px 10px 20px 10px;display:flex;padding-top:10px;flex-direction:flex-start; text-align: center;border-radius:8px">
                                                            <h5>Application</h5>
                                                        </div>
                                                        """,unsafe_allow_html=True)
    
                                    container_appli.write(f"{technique_obj.application}")
                                
                                # Pour le bilan d'énergie dans Technique
                                if technique_obj.bilan_energetique != None: 
                                    container_bilan = container_technique.container(border=True)
                                    container_bilan.write("""
                                                        <div style="background-color:#0073e6;margin:20px 10px 20px 10px;display:flex; padding-top:10px;flex-direction:flex-start; text-align: center;border-radius:8px">
                                                            <h5>Bilan Énergétique</h5>
                                                        </div>
                                                        """,unsafe_allow_html=True)
    
                                    container_bilan.write(f"{technique_obj.bilan_energetique}")
                                sol_container.write("""
                                        <div>
                                        <p> Score de similarité : {score} </p>                
                                        </div>
                                    """.format(score=solution[2]), unsafe_allow_html=True)
                
                                results = calc.main(str(solution[0]))
                                afficher_resultats_streamlit(results)
                    


if __name__ == "__main__":
    main()
