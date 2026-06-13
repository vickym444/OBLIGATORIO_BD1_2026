from repositories.disciplina_repository import DisciplinaRepository


class DisciplinaService:
    def __init__(self, repository=None):
        self.repository = repository or DisciplinaRepository()

    def listar_disciplinas(self):
        return self.repository.get_all_disciplinas()

    def obtener_disciplina(self, id_disciplina):
        return self.repository.get_disciplina_by_id(id_disciplina)

    def crear_disciplina(self, nombre, descripcion=None):
        return self.repository.create_disciplina(nombre=nombre, descripcion=descripcion)

    def actualizar_disciplina(self, id_disciplina, nombre, descripcion, activo):
        return self.repository.update_disciplina(
            id_disciplina=id_disciplina,
            nombre=nombre,
            descripcion=descripcion,
            activo=activo,
        )

    def eliminar_disciplina(self, id_disciplina):
        return self.repository.delete_disciplina(id_disciplina)


disciplina_service = DisciplinaService()