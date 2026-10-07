# /// script
# dependencies = [
#     "cassandra-driver",
# ]
# ///
"""Script de carga de datos para el Mini-Reto de Cassandra (Grupo G4 - IoT).

Estudiante: Jonatan Aguilar (Carné: 20240565)
Dominio: Sensores y Alertas (sitios, sensores, lecturas, alertas)

Uso:
    uv run carga.py
    o:
    python3 carga.py
"""
import csv
import sys
from datetime import datetime
from decimal import Decimal
from pathlib import Path

try:
    from cassandra.cluster import Cluster
    from cassandra.concurrent import execute_concurrent_with_args
except ImportError:
    print("Error: falta la libreria 'cassandra-driver'. Ejecuta: uv run carga.py")
    sys.exit(1)


def main():
    base_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
    data_dir = base_dir / "data" / "mini-reto" / "G4-iot"

    if not data_dir.exists():
        print(f"Error: no se encuentra el directorio de datos en {data_dir}")
        sys.exit(1)

    print("Conectando a Cassandra en localhost:9042...")
    cluster = Cluster(["127.0.0.1"], port=9042)
    session = cluster.connect("iot_20240565")

    # 1. Cargar sensores (en memoria para denormalizar alertas y en tabla sensores_por_id)
    print("Cargando sensores...")
    sensores_map = {}
    sensores_rows = []
    with open(data_dir / "sensores.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["sensor_id"]
            sitio = row["sitio_id"]
            tipo = row["tipo"]
            inst = datetime.fromisoformat(row["instalado_en"])
            sensores_map[sid] = (sitio, tipo)
            sensores_rows.append((sid, sitio, tipo, inst))

    ps_sensor = session.prepare(
        "INSERT INTO sensores_por_id (sensor_id, sitio_id, tipo, instalado_en) VALUES (?, ?, ?, ?)"
    )
    execute_concurrent_with_args(session, ps_sensor, sensores_rows, concurrency=20)
    print(f"  Insertados {len(sensores_rows)} sensores en sensores_por_id.")

    # 2. Cargar alertas desnormalizadas con datos de sensor en alertas_por_sitio
    print("Cargando alertas desnormalizadas...")
    alertas_rows = []
    with open(data_dir / "alertas.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            aid = int(row["alerta_id"])
            sid = row["sensor_id"]
            gen = datetime.fromisoformat(row["generada_en"])
            nivel = row["nivel"]
            msg = row["mensaje"]
            sitio, tipo = sensores_map.get(sid, ("desconocido", "desconocido"))
            alertas_rows.append((sitio, gen, aid, sid, tipo, nivel, msg))

    ps_alerta = session.prepare(
        "INSERT INTO alertas_por_sitio (sitio_id, generada_en, alerta_id, sensor_id, tipo, nivel, mensaje) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)"
    )
    execute_concurrent_with_args(session, ps_alerta, alertas_rows, concurrency=20)
    print(f"  Insertadas {len(alertas_rows)} alertas en alertas_por_sitio.")

    # 3. Cargar lecturas en lectura_reciente_por_sensor y lecturas_por_sensor_rango
    print("Cargando 40,000 lecturas en lectura_reciente_por_sensor y lecturas_por_sensor_rango...")
    lecturas_c2 = []
    lecturas_c4 = []
    with open(data_dir / "lecturas.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lid = int(row["lectura_id"])
            sid = row["sensor_id"]
            leida = datetime.fromisoformat(row["leida_en"])
            val = Decimal(row["valor"])
            lecturas_c2.append((sid, leida, lid, val))
            lecturas_c4.append((sid, leida, lid, val))

    ps_c2 = session.prepare(
        "INSERT INTO lectura_reciente_por_sensor (sensor_id, leida_en, lectura_id, valor) VALUES (?, ?, ?, ?)"
    )
    execute_concurrent_with_args(session, ps_c2, lecturas_c2, concurrency=50)

    ps_c4 = session.prepare(
        "INSERT INTO lecturas_por_sensor_rango (sensor_id, leida_en, lectura_id, valor) VALUES (?, ?, ?, ?)"
    )
    execute_concurrent_with_args(session, ps_c4, lecturas_c4, concurrency=50)
    print(f"  Insertadas {len(lecturas_c2)} lecturas en ambas tablas.")

    cluster.shutdown()
    print("Carga finalizada con exito.")


if __name__ == "__main__":
    main()
