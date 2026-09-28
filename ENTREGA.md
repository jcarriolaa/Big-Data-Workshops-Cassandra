# Qué entregas y cómo se califica

Taller de Cassandra · Curso *Big Data y su Relación con Generative AI*, UFM.

**Fecha de entrega: lunes 5 de octubre, 4:00 PM** (hora de Guatemala), por Pull Request. Ese mismo
día, en clase, presenta cada grupo.

La bitácora es **individual**: cada quien levanta su nodo del clúster del grupo, toma sus capturas
desde ese nodo y escribe sus respuestas. La presentación es **grupal**, salvo la pregunta a cada integrante.

En los comandos, sustituye `G1`, `20241234` y `juan-perez` por tu grupo, carné y nombre.

---

## Tu carpeta de entrega

Todo va en `entregas/G#/<carné>-<nombre>-<apellido>/`, en minúsculas y sin tildes ni ñ. Por ejemplo,
`entregas/G1/20241234-juan-perez/`:

| Archivo | Qué es |
|---|---|
| `bitacora.md` | Tu bitácora, copiada de [`bitacora-plantilla.md`](bitacora-plantilla.md) y llena |
| `capturas/E1-cluster.png` … `capturas/E6b-handoff.png` | Las capturas de la sección 1.1 |
| `compose.yml` | Tu compose, con tu nodo del clúster del grupo |
| `mini-reto/modelo.cql` | El `CREATE KEYSPACE` y los `CREATE TABLE` de tu modelo |
| `mini-reto/consultas.cql` | Las cuatro consultas en CQL |
| `mini-reto/resultados.txt` | La salida de tus cuatro consultas |
| `mini-reto/carga.*` | Cómo cargaste los datos: CQL, un script o lo que hayas usado |
| `check.txt` | La prueba de que tu clúster estuvo completo |

El `compose.yml`, `carga.*` y `check.txt` no tienen porcentaje propio: respaldan la autoría.

---

## 1. Bitácora (50 %)

En tu bitácora, borra las líneas que empiezan con `>` (son instrucciones), pero **no** los enunciados
en negrita de las preguntas: la validación los usa para encontrar tus respuestas. Las respuestas no
van en líneas que empiecen con `>`.

### 1.1 Las evidencias (15 %, 2.5 cada una)

Capturas de **tu** terminal donde se vea **el comando y su salida completa**. Debajo de cada una, en
la bitácora, una o dos frases diciendo qué se ve.

| # | Archivo | Qué debe verse | Comandos | Paso |
|---|---|---|---|---|
| E1 | `E1-cluster.png` | Tres nodos `UN` en `dc-g#` **y** el nombre `UFM-G#` | `nodetool status` y `nodetool describecluster` | 5 |
| E2 | `E2-copias.png` | Las tres direcciones de la partición de Quetzaltenango **y** el keyspace con 3 copias en `dc-g#` | `nodetool getendpoints ventas ventas_por_ciudad Quetzaltenango` y `DESCRIBE KEYSPACE ventas;` | 6 |
| E3 | `E3-cql.png` | El upsert (una sola fila), la fila con TTL antes y después de expirar, **y** `[applied] False` | los `INSERT` y `SELECT` del Paso 7 | 7 |
| E4 | `E4-un-nodo-caido.png` | El nodo apagado en `DN`, la lectura con `QUORUM` respondiendo **y** la misma lectura con `ALL` rechazada | `nodetool status` y las dos lecturas del Paso 8.1 | 8 |
| E5 | `E5-dos-nodos-caidos.png` | Dos nodos en `DN`, la lectura con `ONE` respondiendo **y** con `QUORUM` rechazada | `nodetool status` y las dos lecturas del Paso 8.2 | 8 |
| E6a | `E6a-hint.png` | El archivo `.hints` con el Host ID del nodo apagado **y** esa misma fila `DN` | `ls /var/lib/cassandra/hints` y `nodetool status` | 9 |
| E6b | `E6b-handoff.png` | `Finished hinted handoff` **y** tu venta leída desde el nodo que volvió | `docker logs <tu-nodo> 2>&1 \| grep "Finished hinted handoff"` y la lectura del Paso 9 | 9 |

E6a y E6b valen 1.25 cada una. Cada imagen en `.png` o `.jpg`, de 1 MB como máximo; los enlaces de
la bitácora apuntan a los archivos que subas. Si no cabe en
una pantalla, una evidencia se puede partir en dos (`E1a`, `E1b`). Las evidencias que piden dos
cosas ("esto **y** aquello") valen la mitad si solo se ve una. En E4 y E5, un `ReadTimeout` cuenta
como rechazo.

### 1.2 Las 3 preguntas (10 %)

De tres a seis líneas, **con tus palabras y con tus datos**.

| Nivel | Cómo es la respuesta |
|---|---|
| Completa | Correcta, con tus palabras, citando algo de tu pantalla: tus líneas de traza, tu tabla, tu Host ID |
| Tres cuartos | Correcta y con tus palabras, pero sin ningún dato tuyo |
| Mitad | Parcialmente correcta, incompleta o con conceptos mezclados |
| Cero | Copiada de internet, texto de la guía sin salida propia, o en blanco |

1. **(3 %)** Con la traza (`TRACING ON`) de las dos consultas del Paso 4 de la Parte 1: ¿qué línea
   muestra que la consulta por ciudad leyó una sola partición, y cuál que la de producto recorrió
   toda la tabla? ¿Por qué Cassandra rechaza la segunda sin `ALLOW FILTERING`?
2. **(4 %)** Con tu tabla del Paso 8: ¿qué lecturas se comportaron como **CP** (prefieren fallar
   antes que dar un dato posiblemente viejo) y cuáles como **AP** (responden aunque falten copias)?
   ¿Qué nivel usarías para leer el saldo de una cuenta bancaria y cuál para un contador de
   reproducciones, y por qué?
3. **(3 %)** ¿Cómo se enteró el nodo apagado de tu venta, escrita mientras estaba apagado? Cita su
   Host ID y la línea del registro que lo prueba. ¿Qué pasaría si el nodo estuviera apagado más
   tiempo que `max_hint_window`?

### 1.3 Mini-reto: del modelo relacional a Cassandra (25 %)

Cada grupo recibe, en `data/mini-reto/`, un sistema real modelado **como en SQL**:

| Grupo | Carpeta | Dominio |
|---|---|---|
| **G1** | `data/mini-reto/G1-spotify/` | Música: usuarios, canciones, playlists y reproducciones |
| **G2** | `data/mini-reto/G2-uber/` | Transporte: pasajeros, conductores, viajes y pagos |
| **G3** | `data/mini-reto/G3-discord/` | Mensajería: servidores, canales, usuarios y mensajes |
| **G4** | `data/mini-reto/G4-iot/` | Sensores: sitios, sensores, lecturas y alertas |

En cada carpeta:

- `schema.sql`: el modelo relacional, con llaves foráneas.
- Un CSV por tabla, con los datos.
- `consultas.sql`: las **cuatro consultas** que la aplicación necesita, con sus JOIN y sus
  parámetros fijos.

Cassandra no tiene JOIN. Tu trabajo:

1. **Modelo** (`modelo.cql`): un keyspace con el nombre del dominio (`spotify`, `uber`, `discord` o
   `iot`) seguido de tu carné, `spotify_20241234`, porque el clúster es compartido; 3 copias en tu
   datacenter, y **una tabla por consulta**: cuatro tablas.
2. **Carga**: los datos de los CSV en tus tablas. El método es libre; se entrega en `carga.*`.
3. **Consultas** (`consultas.cql`): las cuatro, en CQL, **sin `ALLOW FILTERING`**, con los mismos
   parámetros de `consultas.sql`. Su salida va en `resultados.txt`:

   ```bash
   docker exec -i <tu-nodo> cqlsh < entregas/G1/20241234-juan-perez/mini-reto/consultas.cql \
     > entregas/G1/20241234-juan-perez/mini-reto/resultados.txt
   ```

   Las horas de los CSV están en UTC; `cqlsh` las muestra con el sufijo `.000000+0000`.

4. **Justificación**, en la bitácora: para cada tabla, por qué esa partition key y esa clustering
   key; qué datos quedaron duplicados entre tablas; y qué tendría que hacer la aplicación si cambia
   uno de esos datos duplicados.

| Criterio | % |
|---|---|
| Modelo: una tabla por consulta, con partition key y clustering key que la respondan | 8 |
| Consultas: corren sin `ALLOW FILTERING` y devuelven lo mismo que `consultas.sql` sobre los CSV (2.5 cada una) | 10 |
| Justificación | 7 |

El resultado de las consultas es el mismo dentro de un grupo. El modelo, la carga y la
justificación son individuales.

Documentación: <https://cassandra.apache.org/doc/5.0/cassandra/developing/data-modeling/index.html>

---

## 2. Presentación del lunes 5 de octubre (50 %)

Diez minutos por grupo: ocho de presentación y dos para el cambio. El orden se decide en clase. El
clúster del grupo se levanta **antes** de la clase, en las tres laptops.

| Bloque | Tiempo | Qué se muestra | % |
|---|---|---|---|
| Modelo | 3 min | Del modelo relacional a Cassandra: las tablas con sus llaves, qué se duplicó y por qué, y qué pasa si cambia un dato duplicado | 20 (grupal) |
| Demo en vivo | 3 min | Tres nodos `UN`, en las tres laptops → se apaga uno → una lectura con `QUORUM` responde → la misma lectura con `ALL` se rechaza | 20 (grupal) |
| Preguntas | 2 min | Una pregunta del catedrático a cada integrante | 10 (individual) |

Cada criterio se califica completo o no se califica. Si la demo falla en vivo, se pierden sus 20 %.
Diapositivas opcionales, tres como máximo.

---

## 3. Cómo se entrega

**Orden de cierre** (todo requiere el clúster activo):

1. Las capturas (durante la Parte 2).
2. El mini-reto.
3. El `check.txt` (abajo).
4. Tu carpeta, la validación y el PR (abajo).
5. La presentación del lunes 5-oct.
6. Limpieza (Paso 10 de la [Parte 2](parte-2-tarea.md)).

Desde el clon de tu fork:

**1. Conecta el repo del curso y crea tu rama** (una sola vez):

```bash
git remote add upstream https://github.com/jcarriolaa/Big-Data-Workshops-Cassandra.git
git checkout main
git pull upstream main
git checkout -b entrega-20241234-juan-perez
```

`git pull upstream main` trae las correcciones publicadas en el repo del curso.

**2. Arma tu carpeta:**

```bash
mkdir -p entregas/G1/20241234-juan-perez/capturas entregas/G1/20241234-juan-perez/mini-reto
cp bitacora-plantilla.md entregas/G1/20241234-juan-perez/bitacora.md
cp compose.yml entregas/G1/20241234-juan-perez/

# Con los tres nodos del clúster del grupo arriba:
bash scripts/check.sh cluster > entregas/G1/20241234-juan-perez/check.txt
```

Después se agregan las capturas y los archivos del mini-reto, y se completa la bitácora.

**3. Valida en tu máquina:**

```bash
python3 scripts/validar_entrega.py entregas/G1/20241234-juan-perez
```

Resultado esperado: **0 ❌**. Cada ❌ indica qué falta.

**4. Sube y abre el Pull Request:**

```bash
git add entregas/G1/20241234-juan-perez
git commit -m "Entrega taller Cassandra - Juan Perez"
git push -u origin entrega-20241234-juan-perez
```

Sube **solo tu carpeta** (`git add` de tu carpeta, no `git add -A`). En GitHub, haz clic en
**Compare & pull request**, con destino `jcarriolaa/Big-Data-Workshops-Cassandra`, rama `main`, y
título `Entrega G1 - Juan Perez`. **No hagas merge**: el PR es solo el medio de entrega.

La validación automática se publica en el PR y se repite en cada push. No asigna la nota: un ❌ no
es un cero, pero lo que falte no suma.

**5. Registra la URL del PR en MIU** (<https://miu.ufm.edu/>). La entrega es el PR; el registro en
MIU es informativo.

### ❌ Si falla

| Síntoma | Arreglo |
|---|---|
| `remote: Permission denied` | El push va al repo del curso. `git remote -v`: `origin` debe ser **tu** fork. |
| El PR muestra archivos que no tocaste | `git fetch upstream && git merge upstream/main && git push` |

---

## Reglas

- **Hora.** Abrir el PR, hacer un commit o hacer un push a partir de las 4:00 PM del lunes 5 de
  octubre vuelve tardía la entrega completa: se califica y se multiplica por 0.5. Hasta el viernes 9
  de octubre a las 4:00 PM se acepta tarde; después, no se recibe. La presentación no se repite.
- **Trabajo propio.** Entregas con la misma captura, el mismo modelo o la misma justificación se
  revisan caso por caso. Resultados iguales dentro de un grupo son esperados.
- **Problemas no resueltos** se documentan en la sección 4 de la bitácora. No sustituyen lo que
  falte.
