-- =============================================================================
-- Mini-Reto: Consultas CQL (Grupo G4 - IoT)
-- Estudiante: Jonatan Aguilar (Carné: 20240565)
-- Ninguna consulta utiliza ALLOW FILTERING.
-- =============================================================================

-- C1. Ficha de un sensor.
SELECT sensor_id, sitio_id, tipo, instalado_en
FROM iot_20240565.sensores_por_id
WHERE sensor_id = 'se005';

-- C2. La lectura mas reciente de un sensor.
SELECT leida_en, valor
FROM iot_20240565.lectura_reciente_por_sensor
WHERE sensor_id = 'se042'
ORDER BY leida_en DESC
LIMIT 1;

-- C3. Las 10 alertas mas recientes de un sitio, con el tipo de sensor.
SELECT generada_en, sensor_id, tipo, nivel, mensaje
FROM iot_20240565.alertas_por_sitio
WHERE sitio_id = 'si08'
LIMIT 10;

-- C4. Cuantas lecturas tuvo un sensor entre las 08:00 y las 11:59 de un dia, y el valor maximo.
SELECT count(*) AS lecturas, max(valor) AS maximo
FROM iot_20240565.lecturas_por_sensor_rango
WHERE sensor_id = 'se042'
  AND leida_en >= '2026-09-25 08:00:00+0000' AND leida_en < '2026-09-25 12:00:00+0000';
