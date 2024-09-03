from util.imports import *

def get_couts_fin(df_money, df_cout):
    costs = []
    for index, row in df_cout.iterrows():
        reel_cout = row['reelcoutrex']
        code_monnaie = row['codemonnaiecoutrex']
        if reel_cout is not None and not pd.isna(reel_cout):
            taux_monnaie = df_money.loc[df_money['nummonnaie'] == code_monnaie, 'valeurtauxmonnaie'].values[0]
            cout_converti = reel_cout * taux_monnaie
            costs.append(cout_converti)
    cout_moyen = sum(costs) / len(costs) if costs else None
    ecart_type_cout = pd.Series(costs).std() if costs else None
    return {'valeurs': costs, 'moyenne': cout_moyen, 'ecart_type': ecart_type_cout}

def get_gains_fin(df_money, df_gain):
    gains = [] 
    for index, row in df_gain.iterrows():
        reel_gain_financier = row['gainfinanciergainrex']
        code_monnaie = row['codemonnaiegainrex']
        if reel_gain_financier is not None and not math.isnan(reel_gain_financier):
            taux_monnaie = df_money.loc[df_money['nummonnaie'] == code_monnaie, 'valeurtauxmonnaie'].values[0]
            gain_converti = reel_gain_financier * taux_monnaie
            gains.append(gain_converti)
    gain_financier_moyen = sum(gains) / len(gains) if gains else None
    ecart_type_gain = pd.Series(gains).std() if gains else None
    return {'valeurs': gains, 'moyenne': gain_financier_moyen, 'ecart_type': ecart_type_gain}

def get_eco_energie(df_energy):
    total_economie_energie = {}
    compteur_par_unite = {}
    for index, row in df_energy.iterrows():
        economie_energie = row['energiegainrex']
        unite_energie = row['uniteenergiegainrex']
        print(unite_energie)
        
        if unite_energie in total_economie_energie:
            total_economie_energie[unite_energie] += economie_energie
            compteur_par_unite[unite_energie] += 1
        else:
            if economie_energie is not None:
                total_economie_energie[unite_energie] = economie_energie
                compteur_par_unite[unite_energie] = 1
    
    moyenne_par_unite = {}
    for unite, total in total_economie_energie.items():
        moyenne_par_unite[unite] = total / compteur_par_unite[unite]
    
    moyennes_dict = {}
    for unite, moyenne in moyenne_par_unite.items():
        moyennes_dict[unite] = moyenne

    ecart_type_energie = pd.Series(df_energy['energiegainrex']).std()
    return {'valeurs': total_economie_energie, 'moyennes': moyennes_dict, 'ecart_type': ecart_type_energie}

def get_GES(df_gain):
    GES_values = []
    for index, row in df_gain.iterrows():
        GES_gain = row['gesgainrex']
        if GES_gain is not None and not math.isnan(GES_gain):
            GES_values.append(GES_gain)
    GES_moyen = sum(GES_values) / len(GES_values) if GES_values else None
    ecart_type_GES = pd.Series(GES_values).std() if GES_values else None
    return {'valeurs': GES_values, 'moyenne': GES_moyen, 'ecart_type': ecart_type_GES}

def main(solution_id):
    host = 'localhost'
    user = 'user'
    password = '123'
    database = 'db_databattle'

    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
    results = {}

    query_gain = f"""
        SELECT 
            d.typedictionnaire, 
            c.coderex, 
            d.traductiondictionnaire, 
            c.gainfinanciergainrex, 
            c.codemonnaiegainrex, 
            c.codeperiodeeconomie, 
            c.energiegainrex, 
            c.uniteenergiegainrex, 
            c.codeperiodeenergie, 
            c.gesgainrex, 
            c.minigainrex, 
            c.maxigainrex, 
            c.moyengainrex, 
            c.reelgainrex, 
            c.trireelgainrex, 
            c.trimingainrex, 
            c.trimaxgainrex
        FROM 
            tblgainrex c
        LEFT JOIN 
            tbldictionnaire d ON d.codeappelobjet = c.numgainrex
                            AND d.typedictionnaire = "rexgain"
                            AND d.codelangue = 2
        WHERE 
            c.codesolution = {solution_id}
        ORDER BY 
            c.coderex ASC;
    """
    df_gain = pd.read_sql(query_gain, con=engine)

    query_cout = f"""
        SELECT 
            d.typedictionnaire AS typeDict, 
            c.coderex AS use_case, 
            d.traductiondictionnaire AS phrases, 
            c.minicoutrex, 
            c.maxicoutrex, 
            c.reelcoutrex,
            c.codemonnaiecoutrex
        FROM 
            tblcoutrex c
        LEFT JOIN 
            tbldictionnaire d ON d.codeappelobjet = c.numcoutrex
                            AND d.typedictionnaire = "rexcout"
                            AND d.codelangue = 2
        WHERE 
            c.codesolution = {solution_id}
        ORDER BY 
            c.coderex ASC;
    """

    df_cout = pd.read_sql(query_cout, con=engine)

    query_economy = f"""
        SELECT r.codesolution, r.coderex, r.energiegainrex, r.gesgainrex,r.uniteenergiegainrex, dic.traductiondictionnairecategories
        FROM tblgainrex r
        INNER JOIN tbldictionnairecategories dic on dic.codeappelobjet = r.uniteenergiegainrex
        WHERE codesolution={solution_id} and codelangue=2 and dic.typedictionnairecategories="uni" 
        ORDER BY coderex asc ;
    """
    df_energy = pd.read_sql(query_economy, con=engine)

    data = {
        'nummonnaie': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        'shortmonnaie': ['', 'EUR', 'USD', 'AUD', 'CAD', 'GBP', 'INR', 'SEK', 'FRF', 'JPY', 'CHF', 'MYR', 'BRL', 'LACS', 'DZD', 'KRW'],
        'valeurtauxmonnaie': [1, 1, 0.7899, 0.8029, 0.7735, 1.2389, 0.014, 0.1132, 0.1524, 0.0099, 0.8326, 0.2487, 0.3895, 14029.14, 0.0099, 0.00075]
    }

    df_money = pd.DataFrame(data)

    cout_financier = get_couts_fin(df_money, df_cout)
    gain_financier = get_gains_fin(df_money, df_gain)
    eco_energie = get_eco_energie(df_energy)
    GES = get_GES(df_gain)

    results["solution"] = solution_id
    results["cout_financier"] = cout_financier
    results["gain_financier"] = gain_financier
    results["eco_energie"] = eco_energie
    results["GES"] = GES

    engine.dispose()
    return results
