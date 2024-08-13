from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import recor
from fastapi import  Form, HTTPException
import threading


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recor.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RECOR API"}
@app.put("/update_telephone/")
def update_telephone(matricule: int = Form(...), telephone: int = Form(...)):
    # Ton code ici
    return {"message": "Telephone number updated successfully"}
@app.get("/start-dashboard/")
def start_dashboard():
    return {"message": "Tableau de bord updated successfully"}
    