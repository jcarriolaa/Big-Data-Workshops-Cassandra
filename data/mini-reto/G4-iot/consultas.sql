-- C1. Ficha de un sensor.
SELECT sensor_id, sitio_id, tipo, instalado_en
FROM sensores
WHERE sensor_id = 'se005';

-- C2. La lectura más reciente de un sensor.
SELECT leida_en, valor
FROM lecturas
WHERE sensor_id = 'se042'
ORDER BY leida_en DESC
LIMIT 1;

-- C3. Las 10 alertas más recientes de un sitio, con el tipo de sensor.
SELECT a.generada_en, a.sensor_id, s.tipo, a.nivel, a.mensaje
FROM alertas a JOIN sensores s ON s.sensor_id = a.sensor_id
WHERE s.sitio_id = 'si08'
ORDER BY a.generada_en DESC
LIMIT 10;

-- C4. Cuántas lecturas tuvo un sensor entre las 08:00 y las 11:59 de un día, y el valor máximo.
SELECT COUNT(*) AS lecturas, MAX(valor) AS maximo
FROM lecturas
WHERE sensor_id = 'se042'
  AND leida_en >= '2026-09-25 08:00:00' AND leida_en < '2026-09-25 12:00:00';
