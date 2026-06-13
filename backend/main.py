import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database.connection import test_connection
from routes.actividad_routes import router as actividad_router
from routes.estudiante_routes import router as estudiante_router
from routes.facultad_routes import router as facultad_router
from routes.carrera_routes import router as carrera_router
from routes.disciplina_routes import router as disciplina_router
from routes.espacio_routes import router as espacio_router
from routes.practica_routes import router as practica_router


app = FastAPI()

origins = [
    'http://localhost:5173',
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(actividad_router)
app.include_router(estudiante_router)
app.include_router(facultad_router)
app.include_router(carrera_router)
app.include_router(disciplina_router)
app.include_router(espacio_router)
app.include_router(practica_router)



@app.get("/")
def root():
    return {"message": "Backend running"}


@app.get("/health/db")
def health_db():
    try:
        return test_connection()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "8000")))