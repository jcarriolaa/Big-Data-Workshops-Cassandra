CREATE TABLE sitios (
  sitio_id VARCHAR(10) PRIMARY KEY,
  nombre   VARCHAR(60) NOT NULL,
  ciudad   VARCHAR(30) NOT NULL
);
CREATE TABLE sensores (
  sensor_id    VARCHAR(10) PRIMARY KEY,
  sitio_id     VARCHAR(10) NOT NULL REFERENCES sitios(sitio_id),
  tipo         VARCHAR(20) NOT NULL,
  instalado_en TIMESTAMP NOT NULL
);
CREATE TABLE lecturas (
  lectura_id INTEGER PRIMARY KEY,
  sensor_id  VARCHAR(10) NOT NULL REFERENCES sensores(sensor_id),
  leida_en   TIMESTAMP NOT NULL,
  valor      DECIMAL(8,2) NOT NULL
);
CREATE TABLE alertas (
  alerta_id   INTEGER PRIMARY KEY,
  sensor_id   VARCHAR(10) NOT NULL REFERENCES sensores(sensor_id),
  generada_en TIMESTAMP NOT NULL,
  nivel       VARCHAR(10) NOT NULL,
  mensaje     VARCHAR(100) NOT NULL
);
