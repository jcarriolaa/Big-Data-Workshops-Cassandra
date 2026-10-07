-- =============================================================================
--  Mini-reto G2 (Uber): del modelo relacional a Cassandra.
--  Una tabla por consulta. Los datos que en SQL se traen con JOIN quedan
--  copiados (desnormalizados) dentro de cada tabla.
-- =============================================================================

CREATE KEYSPACE IF NOT EXISTS uber_20240126
  WITH replication = {'class': 'NetworkTopologyStrategy', 'dc-g2': 3};

-- C1. Perfil de un pasajero: se busca por pasajero_id, una fila por partición.
CREATE TABLE IF NOT EXISTS uber_20240126.pasajeros_por_id (
  pasajero_id  text,
  nombre       text,
  ciudad       text,
  calificacion decimal,
  PRIMARY KEY ((pasajero_id))
);

-- C2. Los 10 viajes más recientes de un pasajero, con su conductor y su pago.
-- Partición: el pasajero. Orden: inicio DESC, así LIMIT 10 da los más recientes.
-- viaje_id desempata dos viajes que empiecen en el mismo segundo.
CREATE TABLE IF NOT EXISTS uber_20240126.viajes_por_pasajero (
  pasajero_id  text,
  inicio       timestamp,
  viaje_id     int,
  conductor_id text,
  conductor    text,      -- nombre del conductor (copiado de conductores)
  distancia_km decimal,
  monto        decimal,   -- copiado de pagos
  metodo       text,      -- copiado de pagos
  PRIMARY KEY ((pasajero_id), inicio, viaje_id)
) WITH CLUSTERING ORDER BY (inicio DESC, viaje_id ASC);

-- C3. Los viajes de un conductor en un día, con el nombre del pasajero.
-- Partición: conductor + día (UTC), así cada partición es un día de trabajo
-- y no crece sin límite. Orden: inicio ASC.
CREATE TABLE IF NOT EXISTS uber_20240126.viajes_por_conductor_dia (
  conductor_id text,
  dia          date,
  inicio       timestamp,
  viaje_id     int,
  pasajero_id  text,
  pasajero     text,      -- nombre del pasajero (copiado de pasajeros)
  distancia_km decimal,
  tarifa       decimal,
  PRIMARY KEY ((conductor_id, dia), inicio, viaje_id)
) WITH CLUSTERING ORDER BY (inicio ASC, viaje_id ASC);

-- C4. Cuántos viajes empezaron en una ciudad en una franja de horas de un día.
-- Partición: ciudad + día (UTC). inicio como clustering permite el rango de horas.
CREATE TABLE IF NOT EXISTS uber_20240126.viajes_por_ciudad_dia (
  ciudad   text,
  dia      date,
  inicio   timestamp,
  viaje_id int,
  PRIMARY KEY ((ciudad, dia), inicio, viaje_id)
) WITH CLUSTERING ORDER BY (inicio ASC, viaje_id ASC);
