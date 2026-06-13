from pydantic import BaseModel, EmailStr
    
class EstudianteCreate(BaseModel):
    documento: str
    nombre: str
    apellido: str
    email: EmailStr
    id_carrera: int
    
class EstudianteUpdate(BaseModel):
    documento: str
    nombre: str
    apellido: str
    email: EmailStr
    id_carrera: int
    activo: int
    
class EstudianteResponse(BaseModel):
    id_estudiante: int
    documento: str
    nombre: str
    apellido: str
    email: str
    id_carrera: int
    activo: int    