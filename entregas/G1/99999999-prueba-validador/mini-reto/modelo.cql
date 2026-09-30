CREATE KEYSPACE IF NOT EXISTS spotify
  WITH replication = {'class': 'NetworkTopologyStrategy', 'dc-g1': 3};

-- C1: perfil por usuario_id
CREATE TABLE IF NOT EXISTS spotify.usuarios (
  usuario_id text PRIMARY KEY, nombre text, pais text, plan text);

-- C2: reproducciones de un usuario, lo más reciente primero (canción desnormalizada)
CREATE TABLE IF NOT EXISTS spotify.reproducciones_por_usuario (
  usuario_id text, reproducida_en timestamp, reproduccion_id int,
  cancion_id text, titulo text, artista text,
  PRIMARY KEY ((usuario_id), reproducida_en, reproduccion_id)
) WITH CLUSTERING ORDER BY (reproducida_en DESC, reproduccion_id DESC);

-- C3: canciones de una playlist en su orden
CREATE TABLE IF NOT EXISTS spotify.canciones_por_playlist (
  playlist_id text, posicion int, cancion_id text, titulo text, artista text,
  PRIMARY KEY ((playlist_id), posicion)
) WITH CLUSTERING ORDER BY (posicion ASC);

-- C4: reproducciones de una canción por día (bucket = día)
CREATE TABLE IF NOT EXISTS spotify.reproducciones_por_cancion_dia (
  cancion_id text, dia date, reproducida_en timestamp, reproduccion_id int, usuario_id text,
  PRIMARY KEY ((cancion_id, dia), reproducida_en, reproduccion_id));
