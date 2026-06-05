SELECT * FROM `bd1_2026`.`facultad`;
SELECT * FROM `bd1_2026`.`actividad`;
SELECT * FROM `bd1_2026`.`practica`;
SELECT * FROM `bd1_2026`.`inscripcion`;

-- Ver estudiantes con su actividad e inscripcion
SELECT e.nombre, e.apellido, a.nombre as actividad, a.dia, p.fecha, i.estado
FROM inscripcion i
         JOIN estudiante e ON e.id_estudiante = i.id_estudiante
         JOIN practica p ON p.id_practica = i.id_practica
         JOIN actividad a ON a.id_actividad = p.id_actividad;