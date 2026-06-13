from repositories.facultad_repository import FacultadRepository


class FacultadService:
    def __init__(self, repository=None):
        self.repository = repository or FacultadRepository()

    def listar_facultades(self):
        return self.repository.get_all_facultades()

    def obtener_facultad(self, id_facultad):
        return self.repository.get_facultad_by_id(id_facultad)

    def crear_facultad(self, nombre):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la facultad es obligatorio")
        facultad_inactiva = self.repository.get_facultad_by_nombre_inactiva(nombre)
        if facultad_inactiva:
            self.repository.reactivate_facultad(facultad_inactiva["id_facultad"])
            return facultad_inactiva["id_facultad"]
        return self.repository.create_facultad(nombre=nombre)

    def actualizar_facultad(self, id_facultad, nombre):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la facultad es obligatorio")

        return self.repository.update_facultad(id_facultad=id_facultad, nombre=nombre)

    def eliminar_facultad(self, id_facultad):
        return self.repository.delete_facultad(id_facultad)


facultad_service = FacultadService()