-- C1. Perfil de un usuario.
SELECT usuario_id, nombre, pais, plan
FROM usuarios
WHERE usuario_id = 'u116';

-- C2. Las 10 canciones que el usuario escuchó más recientemente.
SELECT r.reproducida_en, c.titulo, c.artista
FROM reproducciones r JOIN canciones c ON c.cancion_id = r.cancion_id
WHERE r.usuario_id = 'u031'
ORDER BY r.reproducida_en DESC
LIMIT 10;

-- C3. Las canciones de una playlist, en su orden.
SELECT pc.posicion, c.titulo, c.artista
FROM playlist_canciones pc JOIN canciones c ON c.cancion_id = pc.cancion_id
WHERE pc.playlist_id = 'p15'
ORDER BY pc.posicion;

-- C4. Cuántas veces se reprodujo una canción en un día.
SELECT COUNT(*) AS reproducciones
FROM reproducciones
WHERE cancion_id = 'c017'
  AND reproducida_en >= '2026-09-09 00:00:00' AND reproducida_en < '2026-09-10 00:00:00';
