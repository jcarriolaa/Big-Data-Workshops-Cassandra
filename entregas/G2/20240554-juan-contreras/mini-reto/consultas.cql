USE uber_20240554;


-- C1. Perfil de un pasajero.
SELECT pasajero_id, nombre, ciudad, calificacion
FROM pasajero_perfil
WHERE pasajero_id = 'pa038';


-- C2. Los 10 viajes más recientes de un pasajero,
-- con su conductor y lo que pagó.
SELECT inicio, conductor, distancia_km, monto, metodo
FROM viajes_por_pasajero
WHERE pasajero_id = 'pa133'
LIMIT 10;


-- C3. Los viajes de un conductor en un día,
-- con el nombre del pasajero.
SELECT inicio, pasajero, distancia_km, tarifa
FROM viajes_por_conductor_dia
WHERE conductor_id = 'co73'
  AND fecha = '2026-09-07'
  AND inicio >= '2026-09-07 00:00:00'
  AND inicio < '2026-09-08 00:00:00';


-- C4. Cuántos viajes empezaron en una ciudad
-- entre las 17:00 y las 19:59 de un día.
SELECT count(*) AS viajes
FROM viajes_por_ciudad_dia
WHERE ciudad = 'San José'
  AND fecha = '2026-09-01'
  AND inicio >= '2026-09-01 17:00:00'
  AND inicio < '2026-09-01 20:00:00';