from util.imports import *
from util.helpers import *
from util.objects import *
from util.locations import *

def get_solutions() -> List[Solution]:
    connexion = mysql.connector.connect(
        host="localhost",
        user="user",
        password="123",
        database="db_databattle"
    )

    curseur = connexion.cursor()

    query1 = '''
    SELECT codeappelobjet,
        MAX(CASE WHEN indexdictionnaire = 1 THEN traductiondictionnaire END) AS description,
        MAX(CASE WHEN indexdictionnaire = 2 THEN traductiondictionnaire END) AS definition,
        MAX(CASE WHEN indexdictionnaire = 5 THEN traductiondictionnaire END) AS application,
        MAX(CASE WHEN indexdictionnaire = 6 THEN traductiondictionnaire END) AS bilan_energetique,
        MAX(CASE WHEN indexdictionnaire = 9 THEN traductiondictionnaire END) AS regle,
        MAX(CASE WHEN indexdictionnaire = 10 THEN traductiondictionnaire END) AS difficultes,
        MAX(CASE WHEN indexdictionnaire = 11 THEN traductiondictionnaire END) AS gain,
        MAX(CASE WHEN indexdictionnaire = 12 THEN traductiondictionnaire END) AS effets_positifs
    FROM db_databattle.tbldictionnaire
    WHERE codelangue = 2 
        AND typedictionnaire = "sol"
    GROUP BY codeappelobjet;
    '''

    query2 = '''
    SELECT s.numsolution, s.codetechno, d.traductiondictionnaire AS traduction_techno
    FROM db_databattle.tblsolution AS s
    JOIN db_databattle.tbldictionnaire AS d ON s.codetechno = d.codeappelobjet
    WHERE d.typedictionnaire = "tec" AND d.codelangue = 2;
    '''

    curseur.execute(query1)
    resultats1 = curseur.fetchall()

    curseur.execute(query2)
    resultats2 = curseur.fetchall()

    query3 = '''
    WITH RECURSIVE ParentHierarchy AS (
        SELECT numtechno, codeparenttechno
        FROM db_databattle.tbltechno
        WHERE numtechno = (
            SELECT codetechno
            FROM db_databattle.tblsolution
            WHERE numsolution = %s
        ) -- Spécifiez l'enregistrement de départ
        UNION ALL
        SELECT t.numtechno, t.codeparenttechno
        FROM db_databattle.tbltechno t
        INNER JOIN ParentHierarchy ph ON t.numtechno = ph.codeparenttechno
        WHERE t.numtechno <> 1 -- Arrêtez la récursion lorsque numtechno = 1
    )
    SELECT codeappelobjet, traductiondictionnaire
        FROM db_databattle.tbldictionnaire 
        WHERE typedictionnaire="tec" 
        AND codelangue=2 
        and indexdictionnaire = 1
        AND codeappelobjet IN (SELECT numtechno FROM ParentHierarchy);
    '''


    solutions = []
    solutions_ids = []
    for resultat1 in resultats1:
        id_solution = resultat1[0]
        description = clean_html_text(resultat1[1])
        definition = clean_html_text(resultat1[2])
        application = clean_html_text(resultat1[3])
        bilan_energetique = clean_html_text(resultat1[4])
        regle = clean_html_text(resultat1[5])
        difficultes = clean_html_text(resultat1[6])
        gain = clean_html_text(resultat1[7])
        effets_positifs = clean_html_text(resultat1[8])

        for resultat2 in resultats2:
            numsolution, codetechno, traduction_techno = resultat2
            if id_solution == numsolution:
                curseur.execute(query3, (numsolution,))
                resultats3 = curseur.fetchall()
                technos = []
                for resultat3 in resultats3: 
                    codetechno, traduction_techno = resultat3
                    techno = Techno(codetechno, traduction_techno)
                    technos.append(techno)
                synthese_economique = SyntheseEconomique(regle, difficultes, gain, effets_positifs)
                technique = Technique(definition, application, bilan_energetique)
                use_case = UseCase()
                solution = Solution(id_solution, description, technos, synthese_economique, technique, use_case)
                if id_solution not in solutions_ids:
                    solutions_ids.append(id_solution)
                    solutions.append(solution)

    curseur.close()
    connexion.close()
    return solutions

def create_csv(solutions: List[Solution]) -> None:
    output_folder = CSV_PATH
    os.makedirs(output_folder, exist_ok=True)

    for index, flags_combination in INDEX_TO_FLAGS.items():
        data = []
        for solution in solutions:
            concatenated_text_data = generate_concatenated_text(solution, flags_combination)
            if concatenated_text_data['Text']:
                data.append(concatenated_text_data)

        if data:
            df = pd.DataFrame(data)
            filename = os.path.join(output_folder, f'{index}.csv')
            df.to_csv(filename, index=False)
            print(f"Fichier '{filename}' sauvegardé avec succès.")

    flags_dict = {flag: True if flag in flags_combination else False for flag in FLAGS}
    concatenated_text = solution.concat_text(**flags_dict)
    return {'Solution_ID': solution.id, 'Text': concatenated_text}

if "__main__" == __name__:
    solutions = get_solutions()
    create_csv(solutions)