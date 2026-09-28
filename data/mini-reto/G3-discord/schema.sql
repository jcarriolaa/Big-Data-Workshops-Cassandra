CREATE TABLE servidores (
  servidor_id VARCHAR(10) PRIMARY KEY,
  nombre      VARCHAR(60) NOT NULL,
  creado_en   TIMESTAMP NOT NULL
);
CREATE TABLE canales (
  canal_id    VARCHAR(10) PRIMARY KEY,
  servidor_id VARCHAR(10) NOT NULL REFERENCES servidores(servidor_id),
  nombre      VARCHAR(30) NOT NULL
);
CREATE TABLE usuarios (
  usuario_id     VARCHAR(10) PRIMARY KEY,
  nombre_usuario VARCHAR(40) NOT NULL,
  creado_en      TIMESTAMP NOT NULL
);
CREATE TABLE mensajes (
  mensaje_id INTEGER PRIMARY KEY,
  canal_id   VARCHAR(10) NOT NULL REFERENCES canales(canal_id),
  usuario_id VARCHAR(10) NOT NULL REFERENCES usuarios(usuario_id),
  enviado_en TIMESTAMP NOT NULL,
  contenido  VARCHAR(200) NOT NULL
);
