-- =============================================================================
-- Mini-Reto: Modelo de Datos para Sistema IoT en Apache Cassandra
-- Dominio: Sensores y Alertas (G4)
-- Estudiante: Jonatan Aguilar (Carné: 20240565)
-- =============================================================================

CREATE KEYSPACE IF NOT EXISTS iot_20240565
  WITH replication = {'class': 'NetworkTopologyStrategy', 'dc-g4': 3};

-- -----------------------------------------------------------------------------
-- C1. Ficha de un sensor.
-- Consulta: SELECT sensor_id, sitio_id, tipo, instalado_en WHERE sensor_id = ?
-- Partition key: sensor_id (acceso puntual a una particion por sensor).
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS iot_20240565.sensores_por_id (
    sensor_id    text,
    sitio_id     text,
    tipo         text,
    instalado_en timestamp,
    PRIMARY KEY ((sensor_id))
);

-- -----------------------------------------------------------------------------
-- C2. La lectura mas reciente de un sensor.
-- Consulta: WHERE sensor_id = ? ORDER BY leida_en DESC LIMIT 1
-- Partition key: sensor_id (todas las lecturas del sensor en el mismo nodo).
-- Clustering key: leida_en DESC (orden natural descendente en disco).
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS iot_20240565.lectura_reciente_por_sensor (
    sensor_id  text,
    leida_en   timestamp,
    lectura_id int,
    valor      decimal,
    PRIMARY KEY ((sensor_id), leida_en, lectura_id)
) WITH CLUSTERING ORDER BY (leida_en DESC, lectura_id ASC);

-- -----------------------------------------------------------------------------
-- C3. Las 10 alertas mas recientes de un sitio, con el tipo de sensor.
-- Consulta relacional con JOIN desnormalizado.
-- Partition key: sitio_id (todas las alertas de un sitio juntas).
-- Clustering key: generada_en DESC (alertas ordenadas cronologicamente).
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS iot_20240565.alertas_por_sitio (
    sitio_id    text,
    generada_en timestamp,
    alerta_id   int,
    sensor_id   text,
    tipo        text,
    nivel       text,
    mensaje     text,
    PRIMARY KEY ((sitio_id), generada_en, alerta_id)
) WITH CLUSTERING ORDER BY (generada_en DESC, alerta_id ASC);

-- -----------------------------------------------------------------------------
-- C4. Metricas de lecturas en rango horario para un sensor.
-- Consulta: WHERE sensor_id = ? AND leida_en >= ? AND leida_en < ?
-- Partition key: sensor_id.
-- Clustering key: leida_en ASC (permite cortes de rango continuos eficientes).
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS iot_20240565.lecturas_por_sensor_rango (
    sensor_id  text,
    leida_en   timestamp,
    lectura_id int,
    valor      decimal,
    PRIMARY KEY ((sensor_id), leida_en, lectura_id)
) WITH CLUSTERING ORDER BY (leida_en ASC, lectura_id ASC);
