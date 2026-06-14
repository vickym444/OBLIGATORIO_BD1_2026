SELECT id_estudiante, nombre, apellido FROM estudiante LIMIT 5;


SELECT * FROM usuario;

INSERT INTO usuario (username, password_hash, id_estudiante, activo)
VALUES ('admin', '$2b$12$WBm2aEBrmxXQs0j2hfw1DOGFWiwsjf9iFv8ykRyrwPcGOU.pdbL.W', 1, 1);

UPDATE usuario
SET rol = 'admin', id_estudiante = NULL
WHERE username = 'admin';