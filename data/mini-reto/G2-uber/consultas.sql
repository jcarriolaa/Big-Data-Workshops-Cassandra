-- C1. Perfil de un pasajero.
SELECT pasajero_id, nombre, ciudad, calificacion
FROM pasajeros
WHERE pasajero_id = 'pa038';

-- C2. Los 10 viajes más recientes de un pasajero, con su conductor y lo que pagó.
SELECT v.inicio, c.nombre AS conductor, v.distancia_km, pg.monto, pg.metodo
FROM viajes v
  JOIN conductores c ON c.conductor_id = v.conductor_id
  JOIN pagos pg ON pg.viaje_id = v.viaje_id
WHERE v.pasajero_id = 'pa133'
ORDER BY v.inicio DESC
LIMIT 10;

-- C3. Los viajes de un conductor en un día, con el nombre del pasajero.
SELECT v.inicio, p.nombre AS pasajero, v.distancia_km, v.tarifa
FROM viajes v JOIN pasajeros p ON p.pasajero_id = v.pasajero_id
WHERE v.conductor_id = 'co73'
  AND v.inicio >= '2026-09-07 00:00:00' AND v.inicio < '2026-09-08 00:00:00'
ORDER BY v.inicio;

-- C4. Cuántos viajes empezaron en una ciudad entre las 17:00 y las 19:59 de un día.
SELECT COUNT(*) AS viajes
FROM viajes
WHERE ciudad = 'San José'
  AND inicio >= '2026-09-01 17:00:00' AND inicio < '2026-09-01 20:00:00';
