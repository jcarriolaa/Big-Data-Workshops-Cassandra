import csv
import subprocess
from pathlib import Path


BASE = Path("data/mini-reto/G2-uber")
KEYSPACE = "uber_20240554"
NODE = "cassandra3"


def esc(value):
    if value is None:
        return "NULL"

    value = str(value).replace("'", "''")
    return f"'{value}'"


def read_csv(filename):
    with open(BASE / filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    pasajeros = read_csv("pasajeros.csv")
    conductores = read_csv("conductores.csv")
    viajes = read_csv("viajes.csv")
    pagos = read_csv("pagos.csv")

    pasajeros_by_id = {
        row["pasajero_id"]: row
        for row in pasajeros
    }

    conductores_by_id = {
        row["conductor_id"]: row
        for row in conductores
    }

    pagos_by_viaje = {
        row["viaje_id"]: row
        for row in pagos
    }

    cql = [f"USE {KEYSPACE};"]

    # C1: perfil de pasajeros
    for p in pasajeros:
        cql.append(
            f"""
INSERT INTO pasajero_perfil
(pasajero_id, nombre, ciudad, calificacion)
VALUES (
    {esc(p["pasajero_id"])},
    {esc(p["nombre"])},
    {esc(p["ciudad"])},
    {p["calificacion"]}
);
"""
        )

    # C2: viajes por pasajero
    # Reemplaza los JOIN con conductores y pagos.
    for v in viajes:
        conductor = conductores_by_id[v["conductor_id"]]
        pago = pagos_by_viaje[v["viaje_id"]]

        cql.append(
            f"""
INSERT INTO viajes_por_pasajero
(pasajero_id, inicio, viaje_id, conductor, distancia_km, monto, metodo)
VALUES (
    {esc(v["pasajero_id"])},
    {esc(v["inicio"])},
    {v["viaje_id"]},
    {esc(conductor["nombre"])},
    {v["distancia_km"]},
    {pago["monto"]},
    {esc(pago["metodo"])}
);
"""
        )

    # C3: viajes por conductor y día
    # Reemplaza el JOIN con pasajeros.
    for v in viajes:
        pasajero = pasajeros_by_id[v["pasajero_id"]]
        fecha = v["inicio"][:10]

        cql.append(
            f"""
INSERT INTO viajes_por_conductor_dia
(conductor_id, fecha, inicio, viaje_id, pasajero, distancia_km, tarifa)
VALUES (
    {esc(v["conductor_id"])},
    {esc(fecha)},
    {esc(v["inicio"])},
    {v["viaje_id"]},
    {esc(pasajero["nombre"])},
    {v["distancia_km"]},
    {v["tarifa"]}
);
"""
        )

    # C4: viajes por ciudad y día
    for v in viajes:
        fecha = v["inicio"][:10]

        cql.append(
            f"""
INSERT INTO viajes_por_ciudad_dia
(ciudad, fecha, inicio, viaje_id)
VALUES (
    {esc(v["ciudad"])},
    {esc(fecha)},
    {esc(v["inicio"])},
    {v["viaje_id"]}
);
"""
        )

    cql_text = "\n".join(cql)

    output = Path(__file__).parent / "carga_generada.cql"
    output.write_text(cql_text, encoding="utf-8")

    print(f"INSERTs generados: {len(cql) - 1}")
    print(f"Archivo generado: {output}")

    subprocess.run(
        ["docker", "exec", "-i", NODE, "cqlsh"],
        input=cql_text.encode(),
        check=True
    )

    print("Carga completada correctamente.")


if __name__ == "__main__":
    main()