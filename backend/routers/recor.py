from fastapi import APIRouter, File, UploadFile, HTTPException, Form ,FastAPI
import pandas as pd
import shutil
import os
from pydantic import BaseModel
import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import threading

router = APIRouter()
app = FastAPI()

UPLOAD_DIRECTORY = "../frontend/uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
class ErrorResponse(BaseModel):
    detail: str

@router.post("/uploadfiles/")
async def upload_files(file1: UploadFile = File(...), file2: UploadFile = File(...), file3: UploadFile = File(...)):
    files = [file1, file2, file3]
    for file in files:
        file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    return {"message": "Files uploaded successfully"}

@router.get("/user/{matricule}")
def get_user(matricule: int):
    try:
        # Log to check if the files exist
        print(f"Reading files from {UPLOAD_DIRECTORY}")
        df1_path = os.path.join(UPLOAD_DIRECTORY, 'fichier1.xlsx')
        df2_path = os.path.join(UPLOAD_DIRECTORY, 'fichier2.xlsx')
        df3_path = os.path.join(UPLOAD_DIRECTORY, 'fichier3.xlsx')
        
        if not os.path.exists(df1_path):
            raise HTTPException(status_code=404, detail="fichier1.xlsx not found")
        if not os.path.exists(df2_path):
            raise HTTPException(status_code=404, detail="fichier2.xlsx not found")
        if not os.path.exists(df3_path):
            raise HTTPException(status_code=404, detail="fichier3.xlsx not found")

        df1 = pd.read_excel(df1_path)
        df2 = pd.read_excel(df2_path)
        df3 = pd.read_excel(df3_path)
        
        print(f"df1 head: {df1.head()}")
        print(f"df2 head: {df2.head()}")
        print(f"df3 head: {df3.head()}")
        print(f"df1 columns: {df1.columns}")
        print(f"df2 columns: {df2.columns}")
        print(f"df3 columns: {df3.columns}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading files: {str(e)}")

    try:
        print(f"Searching for matricule {matricule}")
        user_info1 = df1[df1['matricule'] == matricule]
        if user_info1.empty:
            print("User not found in fichier1.xlsx")
            raise HTTPException(status_code=404, detail="User not found in fichier1.xlsx")
        else:
            print(f"User info found in fichier1.xlsx: {user_info1}")

        numero_affiliation = user_info1['numero_affiliation'].values[0]
        date_cotisation = user_info1['date_cotisation'].values[0]

        user_info2 = df2[df2['matricule'] == matricule]
        nombre_mois = user_info2.shape[0]

        user_info3 = df3[df3['matricule'] == matricule]
        if user_info3.empty:
            a_avance = "Non"
        else:
            a_avance = user_info3['a_avance'].values[0]

        return {
            "matricule": matricule,
            "numero_affiliation": numero_affiliation,
            "date_cotisation": date_cotisation,
            "nombre_mois": nombre_mois,
            "a_avance": a_avance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing user data: {str(e)}")

@app.put("/update_telephone/")
def update_telephone(matricule1: int, telephone: int = Form(...)):
    try:
        df1_path = os.path.join(UPLOAD_DIRECTORY, 'fichier1.xlsx')
        if not os.path.exists(df1_path):
            raise HTTPException(status_code=404, detail="fichier1.xlsx not found")

        df1 = pd.read_excel(df1_path)
        print("File loaded successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading files: {str(e)}")

    try:
        print(f"Checking for user with matricule: {matricule1}")
        
        # Convertir la colonne 'matricule' en int si nécessaire
        df1['matricule'] = df1['matricule1'].astype(int)
        
        # Afficher les valeurs pour vérifier
        print(df1['matricule'].head())
        
        user_index = df1.index[df1['matricule'] == matricule1].tolist()
        
        # Si la liste est vide, cela signifie que le matricule n'a pas été trouvé
        if not user_index:
            raise HTTPException(status_code=404, detail="User not found in fichier1.xlsx")

        print(f"User found at index: {user_index[0]}")
        df1.at[user_index[0], 'telephone'] = telephone
        df1.to_excel(df1_path, index=False)
        print("Telephone number updated successfully.")

        return {"message": "Telephone number updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user data: {str(e)}")




@app.get("/start-dashboard/")
async def start_dashboard():
    try:
        print("Démarrage du tableau de bord via FastAPI...")
        await run_dash()
        return {"message": "Tableau de bord démarré", "url": "http://127.0.0.1:8050"}
    except Exception as e:
        import traceback
        print(f"Erreur lors du démarrage du tableau de bord : {traceback.format_exc()}")
        return {"message": "Erreur lors du démarrage du tableau de bord"}

async def run_dash():
    try:
        print("Lecture du fichier Excel...")
        df = pd.read_excel("exemple_avance_agents.xlsx")
        print("Fichier Excel lu avec succès.")
        
        # Vérification des données
        print("Transformation des données...")
        df['A pris une avance'] = df['A pris une avance'].apply(lambda x: 1 if x == 'Oui' else 0)
        taux_avance = df['A pris une avance'].mean() * 100
        df_grouped = df.groupby('Département')['A pris une avance'].mean().reset_index()
        print("Données transformées avec succès.")
        
        # Initialisation de l'application Dash
        print("Initialisation de l'application Dash...")
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
        print("Application Dash initialisée.")
        
        # Démarrage du serveur Dash
        print("Démarrage du serveur Dash...")
        await dash_app.run_server(debug=True, use_reloader=False, port=8051)
        dash_app.run_server(debug=True, use_reloader=False, port=8051)

        print("Serveur Dash démarré.")
        
    except Exception as e:
        import traceback
        print(f"Erreur lors de l'exécution du tableau de bord : {traceback.format_exc()}")

if __name__ == "__main__":
    import uvicorn
    print("Démarrage du serveur FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=8000)