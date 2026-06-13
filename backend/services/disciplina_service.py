from repositories.disciplina_repository import DisciplinaRepository

repo = DisciplinaRepository()

def listar_disciplinas():
    return repo.get_all_disciplinas()

def obtener_disciplina(id_disciplina: int):
    return repo.get_disciplina_by_id(id_disciplina)

def crear_disciplina(nombre, descripcion):
    return repo.create_disciplina(nombre, descripcion)

def actualizar_disciplina(id_disciplina, nombre, descripcion, activo):
    return repo.update_disciplina(id_disciplina, nombre, descripcion, activo)

def eliminar_disciplina(id_disciplina: int):
    return repo.delete_disciplina(id_disciplina)