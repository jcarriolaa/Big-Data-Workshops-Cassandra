# Parte 1 — Guiada: un nodo, una tabla y las ventas

Sesión guiada de 40 minutos a una hora, en clase o por cuenta propia. Todo el código se proporciona. No se califica; la Parte 2
empieza desde cero con un clúster nuevo.

Cada paso tiene la misma estructura: objetivo, código, **✅ Checkpoint** con la salida esperada y
**❌ Si falla**.

En los comandos, `G1` es el grupo (`G1` a `G4`): sustitúyelo por el tuyo. Las salidas de ejemplo son
del grupo G1; con otro grupo cambian los números, no la forma.

---

## Paso 0: La imagen de Cassandra

```bash
docker pull cassandra:5.0.8
```

### ✅ Checkpoint

```bash
bash scripts/check.sh prereq
```

```
✅ docker compose v2 disponible
✅ Docker esta corriendo
✅ Docker tiene 14.6 GB de RAM
✅ imagen cassandra:5.0.8 descargada

Todo en orden.
```

---

## Paso 1: Levanta un nodo

`compose.yml` define un solo servicio, `cassandra1`, con cada línea comentada. La carpeta `data/` del
repo queda dentro del contenedor en `/data`.

```bash
docker compose up -d
```

Cassandra tarda alrededor de un minuto en quedar lista. `nodetool` es la herramienta de
administración de Cassandra; `status` muestra los nodos del clúster:

```bash
docker exec cassandra1 nodetool status
```

### ✅ Checkpoint

```
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address     Load        Tokens  Owns (effective)  Host ID                               Rack 
UN  172.18.0.2  144.31 KiB  16      100.0%            e1e9575f-2baa-4323-9da2-7c609296b871  rack1
```

`UN` significa **U**p (encendido) y **N**ormal (listo para atender). `Datacenter: datacenter1` y el
nombre del clúster, `Test Cluster`, son los valores por defecto de la imagen.

### ❌ Si falla

| Síntoma | Arreglo |
|---|---|
| `no configuration file provided` | No estás en la carpeta del repo. Con `ls` tienes que ver `compose.yml`. |
| `Failed to connect to '127.0.0.1:7199'` | El nodo todavía está arrancando. Espera 30 segundos y repite. |
| `port is already allocated` | Otro proceso usa el puerto 9042: `docker ps` muestra cuál. |
| El contenedor se detiene solo | `docker compose logs cassandra1`: la última línea con `ERROR` indica la causa. |

---

## Paso 2: Keyspace y tabla

Un **keyspace** es el equivalente a una base de datos y define cuántas copias hay de cada dato (el
*replication factor*). Con un solo nodo, una copia.

Entra a `cqlsh`, la consola de CQL:

```bash
docker exec -it cassandra1 cqlsh
```

```sql
CREATE KEYSPACE ventas
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE ventas.ventas_por_ciudad (
  ciudad          text,
  fecha           date,
  id_venta        int,
  pais            text,
  categoria       text,
  producto        text,
  cantidad        int,
  precio_unitario decimal,
  canal           text,
  PRIMARY KEY ((ciudad), fecha, id_venta)
) WITH CLUSTERING ORDER BY (fecha DESC, id_venta ASC);
```

La **llave primaria** tiene dos partes, y es la decisión más importante en Cassandra:

- **Partition key**, `(ciudad)`: decide **en qué nodo** vive cada fila. Todas las ventas de una
  ciudad quedan juntas, en una misma **partición**.
- **Clustering key**, `fecha, id_venta`: decide **el orden** de las filas dentro de la partición.
  Aquí, de la fecha más reciente a la más antigua. `id_venta` hace que cada fila sea única: dos
  ventas de la misma ciudad y el mismo día no se pisan.

```
ventas_por_ciudad

 partition key: ciudad            clustering key: fecha (más reciente primero), id_venta
┌─ partición "Quetzaltenango" ──────────────────────────────┐
│ 2024-12-31 │  7171 │ Miel      │ 1 │   69.69 │ tienda     │
│ 2024-12-31 │ 22469 │ Lampara   │ 4 │  207.31 │ tienda     │
│ ...                                                       │
│ 2024-08-01 │  8143 │ Miel      │ 1 │   68.54 │ web        │
│ ...                                                       │
└───────────────────────────────────────────────────────────┘
┌─ partición "Tegucigalpa" ─────────────────────────────────┐
│ ...                                                       │
└───────────────────────────────────────────────────────────┘
```

Una consulta por ciudad lee **una** partición, ya ordenada. Una consulta por producto tendría que
abrirlas todas.

El nombre `ventas_por_ciudad` no es casual: la tabla existe para responder una consulta, "las ventas
de una ciudad".

### ✅ Checkpoint

```sql
USE ventas;
DESCRIBE TABLES;
```

```
ventas_por_ciudad
```

Sal de `cqlsh` con `exit`.

### ❌ Si falla

| Síntoma | Arreglo |
|---|---|
| `Keyspace 'ventas' does not exist` | El `CREATE KEYSPACE` no se ejecutó; córrelo antes de la tabla. |
| `already exists` | Ya estaba creado; continúa. |

---

## Paso 3: Carga las ventas de tu grupo

Son las mismas 75 000 ventas del taller de Hadoop. `COPY FROM` es un comando de `cqlsh` que carga un
CSV; lee el archivo **dentro del contenedor**, por eso la ruta empieza con `/data`.

```bash
docker exec cassandra1 cqlsh -e "COPY ventas.ventas_por_ciudad (id_venta, fecha, pais, ciudad, categoria, producto, cantidad, precio_unitario, canal) FROM '/data/ventas/ventas_G1.csv' WITH HEADER = true;"
```

La última línea de la salida:

```
75000 rows imported from 1 files in 0 day, 0 hour, 0 minute, and 1.365 seconds (0 skipped).
```

### ✅ Checkpoint

```bash
bash scripts/check.sh nodo
```

```
✅ Contenedor cassandra1 corriendo
✅ cassandra1 en estado UN
✅ ventas.ventas_por_ciudad tiene 75000 filas

Todo en orden.
```

### ❌ Si falla

| Síntoma | Arreglo |
|---|---|
| `0 rows imported from 0 files` | El archivo no existe: los nombres son `ventas_G1.csv` a `ventas_G4.csv`, con `G` mayúscula. |

---

## Paso 4: Consultas por partición, y la que Cassandra rechaza

Entra de nuevo a `cqlsh`:

```bash
docker exec -it cassandra1 cqlsh
```

Las ventas de una ciudad en un día. Filtra por la partition key y por la clustering key:

```sql
SELECT fecha, id_venta, producto, cantidad, precio_unitario, canal
FROM ventas.ventas_por_ciudad
WHERE ciudad = 'Quetzaltenango' AND fecha = '2024-08-01';
```

```
 fecha      | id_venta | producto  | cantidad | precio_unitario | canal
------------+----------+-----------+----------+-----------------+--------
 2024-08-01 |     8143 |      Miel |        1 |           68.54 |    web
 2024-08-01 |    22266 |  Telefono |        3 |         4645.17 |    app
 2024-08-01 |    23868 | Chocolate |        1 |           43.89 |    app
 2024-08-01 |    27595 |      Miel |        3 |           68.17 |    app
 2024-08-01 |    28125 | Bicicleta |        2 |         3889.96 | tienda
 2024-08-01 |    29779 |   Zapatos |        2 |          543.90 | tienda
 2024-08-01 |    32213 |  Cafetera |        1 |          636.74 | tienda
 2024-08-01 |    41045 |  Telefono |        3 |         4738.00 | tienda
 2024-08-01 |    46621 |   Zapatos |        3 |          587.94 | tienda
 2024-08-01 |    50685 |      Cafe |        3 |           86.81 | tienda
 2024-08-01 |    64412 |  Cafetera |        1 |          716.47 | tienda

(11 rows)
```

Ahora, las ventas de un producto:

```sql
SELECT fecha, id_venta, ciudad, cantidad
FROM ventas.ventas_por_ciudad
WHERE producto = 'Miel';
```

```
InvalidRequest: Error from server: code=2200 [Invalid query] message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"
```

Cassandra se niega. `producto` no es parte de la llave, así que para responder tendría que leer
**todas** las particiones de **todos** los nodos. `ALLOW FILTERING` obliga a hacerlo; `TRACING ON`
muestra qué hizo Cassandra en cada consulta:

```sql
TRACING ON;
SELECT count(*) FROM ventas.ventas_por_ciudad WHERE ciudad = 'Quetzaltenango' AND fecha = '2024-08-01';
SELECT count(*) FROM ventas.ventas_por_ciudad WHERE producto = 'Miel' ALLOW FILTERING;
TRACING OFF;
```

Cada consulta imprime su **traza**: la lista de lo que hizo Cassandra. En la de la primera aparece:

```
Executing single-partition query on ventas_por_ciudad [ReadStage-17]
Read 11 live rows and 0 tombstone cells [ReadStage-17]
```

En la de la segunda aparecen otras líneas, repetidas una vez por cada rango de la tabla, hasta
recorrer las 75 000 filas:

```
Submitting range requests on 17 ranges with a concurrency of 1 (152618.4 rows per range expected) [Native-Transport-Requests-5]
Executing seq scan across 3 sstables for (min(-9223372036854775808), min(-9223372036854775808)] [ReadStage-16]
Read 1432 live rows and 0 tombstone cells [ReadStage-16]
```

En Cassandra **la tabla se diseña a partir de la consulta**: si la aplicación necesita las ventas de
un producto, se crea otra tabla cuya partition key sea el producto. Esa es la base de la Parte 2 y
del mini-reto.

### ✅ Checkpoint

La primera consulta devuelve las ventas de un solo día y la segunda termina en
`InvalidRequest ... ALLOW FILTERING`.

### ❌ Si falla

| Síntoma | Arreglo |
|---|---|
| `(0 rows)` en la primera consulta | La ciudad o la fecha están mal escritas: `Quetzaltenango`, `'2024-08-01'`. |
| `SyntaxException: ... no viable alternative at input '-08'` | La fecha va entre comillas simples: `'2024-08-01'`. |

---

## Estado al terminar

Un nodo con una tabla de 75 000 ventas, diseñada para una sola consulta. Sin copias: si
`cassandra1` falla, no hay datos.

Siguiente: **[Parte 2](parte-2-tarea.md)**.
