SELECT usuario_id, nombre, pais, plan FROM spotify.usuarios WHERE usuario_id = 'u116';
SELECT reproducida_en, titulo, artista FROM spotify.reproducciones_por_usuario WHERE usuario_id = 'u031' LIMIT 10;
SELECT posicion, titulo, artista FROM spotify.canciones_por_playlist WHERE playlist_id = 'p15';
SELECT count(*) AS reproducciones FROM spotify.reproducciones_por_cancion_dia WHERE cancion_id = 'c017' AND dia = '2026-09-09';
