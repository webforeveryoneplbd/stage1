import pandas as pd
import os

UPLOAD_DIRECTORY = "/frontend/uploads"

# Fonction pour obtenir les informations de l'utilisateur
def get_user_info(matricule: int):
    df1 = pd.read_excel(os.path.join(UPLOAD_DIRECTORY, 'fichier1.xlsx'))
    df2 = pd.read_excel(os.path.join(UPLOAD_DIRECTORY, 'fichier2.xlsx'))
    df3 = pd.read_excel(os.path.join(UPLOAD_DIRECTORY, 'fichier3.xlsx'))

    # Chercher les informations dans fichier 1
    user_info1 = df1[df1['matricule'] == matricule]
    if user_info1.empty:
        return None  # L'utilisateur n'existe pas dans fichier 1

    numero_affiliation = user_info1['numero_affiliation'].values[0]
    date_cotisation = user_info1['date_cotisation'].values[0]

    # Chercher les informations dans fichier 2
    user_info2 = df2[df2['matricule'] == matricule]
    nombre_mois = user_info2.shape[0]  # Nombre total de mois de cotisation

    # Chercher les informations dans fichier 3
    user_info3 = df3[df3['matricule'] == matricule]
    if user_info3.empty:
        a_avance = "Non"
    else:
        a_avance = user_info3['a_avance'].values[0]

    return {
        "numero_affiliation": numero_affiliation,
        "date_cotisation": date_cotisation,
        "nombre_mois": nombre_mois,
        "a_avance": a_avance
    }
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

def run_dash():
    try:
        df = pd.read_excel("exemple_avance_agents.xlsx")  # Assure-toi que ce chemin est correct
        df['A pris une avance'] = df['A pris une avance'].apply(lambda x: 1 if x == 'Oui' else 0)
        taux_avance = df['A pris une avance'].mean() * 100
        df_grouped = df.groupby('Département')['A pris une avance'].mean().reset_index()

        dash_app = Dash(__name__)
        dash_app.layout = html.Div([
            html.H1(children='Tableau de Bord des Avances des Agents'),
            html.Div(f"Taux global des agents ayant pris une avance : {taux_avance:.2f}%"),
            dcc.Graph(
                id='graph1',
                figure=px.bar(df_grouped, x='Département', y='A pris une avance', 
                              title="Taux d'Agents ayant pris une Avance par Département",
                              labels={'A pris une avance': 'Taux (%)'})
            )
        ])

        dash_app.run_server(debug=True, use_reloader=False, port=8050)
    except Exception as e:
        import traceback
        print(f"Erreur lors de l'exécution du tableau de bord : {traceback.format_exc()}")

# Exécuter directement pour tester
if __name__ == "__main__":
    run_dash()
