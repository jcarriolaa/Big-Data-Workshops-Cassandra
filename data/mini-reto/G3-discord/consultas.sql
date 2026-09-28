-- C1. Perfil de un usuario.
SELECT usuario_id, nombre_usuario, creado_en
FROM usuarios
WHERE usuario_id = 'du230';

-- C2. Los 20 mensajes más recientes de un canal, con el autor.
SELECT m.enviado_en, u.nombre_usuario, m.contenido
FROM mensajes m JOIN usuarios u ON u.usuario_id = m.usuario_id
WHERE m.canal_id = 'ch16'
ORDER BY m.enviado_en DESC
LIMIT 20;

-- C3. Los 10 mensajes más recientes de un usuario, con el canal y el servidor.
SELECT m.enviado_en, s.nombre AS servidor, c.nombre AS canal, m.contenido
FROM mensajes m
  JOIN canales c ON c.canal_id = m.canal_id
  JOIN servidores s ON s.servidor_id = c.servidor_id
WHERE m.usuario_id = 'du186'
ORDER BY m.enviado_en DESC
LIMIT 10;

-- C4. Cuántos mensajes tuvo un canal en un día.
SELECT COUNT(*) AS mensajes
FROM mensajes
WHERE canal_id = 'ch16'
  AND enviado_en >= '2026-09-04 00:00:00' AND enviado_en < '2026-09-05 00:00:00';
