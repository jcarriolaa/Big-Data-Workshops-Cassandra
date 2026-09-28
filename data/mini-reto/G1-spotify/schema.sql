CREATE TABLE usuarios (
  usuario_id  VARCHAR(10) PRIMARY KEY,
  nombre      VARCHAR(60) NOT NULL,
  pais        VARCHAR(30) NOT NULL,
  plan        VARCHAR(10) NOT NULL
);
CREATE TABLE canciones (
  cancion_id   VARCHAR(10) PRIMARY KEY,
  titulo       VARCHAR(80) NOT NULL,
  artista      VARCHAR(60) NOT NULL,
  genero       VARCHAR(20) NOT NULL,
  duracion_seg INTEGER NOT NULL
);
CREATE TABLE playlists (
  playlist_id VARCHAR(10) PRIMARY KEY,
  usuario_id  VARCHAR(10) NOT NULL REFERENCES usuarios(usuario_id),
  nombre      VARCHAR(60) NOT NULL,
  creada_en   TIMESTAMP NOT NULL
);
CREATE TABLE playlist_canciones (
  playlist_id VARCHAR(10) NOT NULL REFERENCES playlists(playlist_id),
  cancion_id  VARCHAR(10) NOT NULL REFERENCES canciones(cancion_id),
  posicion    INTEGER NOT NULL,
  agregada_en TIMESTAMP NOT NULL,
  PRIMARY KEY (playlist_id, cancion_id)
);
CREATE TABLE reproducciones (
  reproduccion_id     INTEGER PRIMARY KEY,
  usuario_id          VARCHAR(10) NOT NULL REFERENCES usuarios(usuario_id),
  cancion_id          VARCHAR(10) NOT NULL REFERENCES canciones(cancion_id),
  reproducida_en      TIMESTAMP NOT NULL,
  segundos_escuchados INTEGER NOT NULL
);
