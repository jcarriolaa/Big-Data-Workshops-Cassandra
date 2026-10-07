"""
Mini-reto G2 (Uber): carga de los CSV relacionales en las tablas de Cassandra.

Cassandra no hace JOIN, así que el JOIN se hace aquí, una sola vez, al cargar:
1. Lee los cuatro CSV de data/mini-reto/G2-uber/.
2. Arma un CSV por tabla de Cassandra, con los nombres y el pago ya copiados.
3. Los copia al contenedor y los carga con COPY ... FROM.
4. Repara el keyspace para que las 3 copias queden iguales.

Uso (desde la raíz del repo, con el clúster arriba y modelo.cql ya aplicado):
    python entregas/G2/20240126-fabiola-deras/mini-reto/carga.py
"""
import csv
import subprocess
import tempfile
from pathlib import Path

NODO = "cassandra2"
KS = "uber_20240126"
ORIGEN = Path(__file__).resolve().parents[4] / "data" / "mini-reto" / "G2-uber"


def leer(nombre):
    with open(ORIGEN / f"{nombre}.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def ts(valor):
    # Las horas de los CSV están en UTC: se marca la zona para que no se reinterpreten.
    return valor + "+0000"


pasajeros = {p["pasajero_id"]: p for p in leer("pasajeros")}
conductores = {c["conductor_id"]: c for c in leer("conductores")}
pagos = {p["viaje_id"]: p for p in leer("pagos")}
viajes = leer("viajes")

tablas = {
    "pasajeros_por_id": (
        ["pasajero_id", "nombre", "ciudad", "calificacion"],
        [[p["pasajero_id"], p["nombre"], p["ciudad"], p["calificacion"]] for p in pasajeros.values()],
    ),
    "viajes_por_pasajero": (
        ["pasajero_id", "inicio", "viaje_id", "conductor_id", "conductor", "distancia_km", "monto", "metodo"],
        [[v["pasajero_id"], ts(v["inicio"]), v["viaje_id"], v["conductor_id"],
          conductores[v["conductor_id"]]["nombre"], v["distancia_km"],
          pagos[v["viaje_id"]]["monto"], pagos[v["viaje_id"]]["metodo"]] for v in viajes],
    ),
    "viajes_por_conductor_dia": (
        ["conductor_id", "dia", "inicio", "viaje_id", "pasajero_id", "pasajero", "distancia_km", "tarifa"],
        [[v["conductor_id"], v["inicio"][:10], ts(v["inicio"]), v["viaje_id"], v["pasajero_id"],
          pasajeros[v["pasajero_id"]]["nombre"], v["distancia_km"], v["tarifa"]] for v in viajes],
    ),
    "viajes_por_ciudad_dia": (
        ["ciudad", "dia", "inicio", "viaje_id"],
        [[v["ciudad"], v["inicio"][:10], ts(v["inicio"]), v["viaje_id"]] for v in viajes],
    ),
}

with tempfile.TemporaryDirectory() as tmp:
    for tabla, (columnas, filas) in tablas.items():
        archivo = Path(tmp) / f"{tabla}.csv"
        with open(archivo, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(columnas)
            w.writerows(filas)
        subprocess.run(["docker", "cp", str(archivo), f"{NODO}:/tmp/{tabla}.csv"], check=True)
        # CONSISTENCY QUORUM: cada fila queda confirmada en 2 de las 3 copias.
        # Con el ONE por defecto, la VPN lenta hizo que se descartaran escrituras
        # y las copias quedaron desiguales; ALL falla si un enlace entre nodos se cae.
        copy = (f"CONSISTENCY QUORUM; COPY {KS}.{tabla} ({', '.join(columnas)}) "
                f"FROM '/tmp/{tabla}.csv' WITH HEADER = true;")
        print(f"--> {tabla}: {len(filas)} filas")
        # Sin check: cqlsh sale con código 2 si tuvo que reintentar algún lote,
        # aunque al final los importe todos. El repair de abajo completa las copias.
        subprocess.run(["docker", "exec", NODO, "cqlsh", "-e", copy])

# La copia que faltó en el QUORUM se completa con repair. El enlace directo entre
# cassandra1 y cassandra3 falla en la VPN, así que se repara por pares a través
# de cassandra2: 2<->1, 2<->3 y otra vez 2<->1 para que cassandra1 reciba lo de cassandra3.
YO, C1, C3 = "100.113.11.13", "100.126.2.38", "100.100.99.24"
for otro in (C1, C3, C1):
    print(f"--> repair {YO} <-> {otro}")
    subprocess.run(["docker", "exec", NODO, "nodetool", "repair", "-full",
                    "-hosts", f"{YO},{otro}", KS], check=True, stdout=subprocess.DEVNULL)
