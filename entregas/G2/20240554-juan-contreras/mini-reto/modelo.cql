CREATE KEYSPACE IF NOT EXISTS uber_20240554
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'dc-g2': 3
}
AND durable_writes = true;


-- C1. Perfil de un pasajero
CREATE TABLE IF NOT EXISTS uber_20240554.pasajero_perfil (
  pasajero_id text PRIMARY KEY,
  nombre text,
  ciudad text,
  calificacion decimal
);


-- C2. Los 10 viajes más recientes de un pasajero,
-- con nombre del conductor y datos del pago.
CREATE TABLE IF NOT EXISTS uber_20240554.viajes_por_pasajero (
  pasajero_id text,
  inicio timestamp,
  viaje_id int,
  conductor text,
  distancia_km decimal,
  monto decimal,
  metodo text,
  PRIMARY KEY ((pasajero_id), inicio, viaje_id)
) WITH CLUSTERING ORDER BY (
  inicio DESC,
  viaje_id ASC
);


-- C3. Viajes de un conductor en un día,
-- con nombre del pasajero.
CREATE TABLE IF NOT EXISTS uber_20240554.viajes_por_conductor_dia (
  conductor_id text,
  fecha date,
  inicio timestamp,
  viaje_id int,
  pasajero text,
  distancia_km decimal,
  tarifa decimal,
  PRIMARY KEY ((conductor_id, fecha), inicio, viaje_id)
) WITH CLUSTERING ORDER BY (
  inicio ASC,
  viaje_id ASC
);


-- C4. Viajes por ciudad y día.
CREATE TABLE IF NOT EXISTS uber_20240554.viajes_por_ciudad_dia (
  ciudad text,
  fecha date,
  inicio timestamp,
  viaje_id int,
  PRIMARY KEY ((ciudad, fecha), inicio, viaje_id)
) WITH CLUSTERING ORDER BY (
  inicio ASC,
  viaje_id ASC
);