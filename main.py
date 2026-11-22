from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# La conexión se lee de variables de entorno (MONGO_URI y MONGO_DB),
# tanto en local como en Render, para no dejar la contraseña en el código.
client = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB"]]


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}


# Punto 3: GET comentarios de un bar
@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(db["comentarios_bares"].find(
        {"bar_id": bar_id},
        {"_id": 0}
    ))
    return comentarios


# Punto 4: POST comentario de un bar
@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha'] = datetime.now().isoformat()
    db["comentarios_bares"].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}


# Punto 5: GET eventos de un bar
@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    eventos = list(db["eventos"].find(
        {"bar_id": bar_id},
        {"_id": 0}
    ))
    return eventos


# Punto 6: POST evento de un bar
@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db["eventos"].insert_one(datos)
    return {'mensaje': 'Evento registrado'}
