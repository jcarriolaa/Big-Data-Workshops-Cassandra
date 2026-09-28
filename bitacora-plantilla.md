# Bitácora del taller de Cassandra

> Copia este archivo a tu carpeta de entrega como `bitacora.md` y llénalo. Borra las líneas que
> empiezan con `>`. No borres los enunciados en negrita.

- **Nombre:**
- **Carné:**
- **Grupo:**
- **Tu nodo en el clúster del grupo:**

---

## 1. Evidencias

> Debajo de cada captura, una o dos frases diciendo qué se ve. Formato en `ENTREGA.md`, sección 1.1.

### E1. Tres nodos en tu clúster y tu datacenter

![E1](capturas/E1-cluster.png)

### E2. Las copias de la partición de Quetzaltenango

![E2](capturas/E2-copias.png)

### E3. Upsert, TTL e IF NOT EXISTS

![E3](capturas/E3-cql.png)

### E4. Un nodo caído: QUORUM frente a ALL

![E4](capturas/E4-un-nodo-caido.png)

### E5. Dos nodos caídos: ONE frente a QUORUM

![E5](capturas/E5-dos-nodos-caidos.png)

### E6a. El hint guardado para el nodo caído

![E6a](capturas/E6a-hint.png)

### E6b. La entrega del hint

![E6b](capturas/E6b-handoff.png)

### Tabla del Paso 8

> ✅ si la lectura respondió, ❌ si se rechazó.

| Nodos caídos | `ONE` | `QUORUM` | `ALL` |
|---|---|---|---|
| 0 | | | |
| 1 | | | |
| 2 | | | |

---

## 2. Preguntas

**1. ¿Qué línea de la traza muestra que la consulta por ciudad leyó una sola partición, y cuál que la de producto recorrió toda la tabla? ¿Por qué Cassandra rechaza la segunda sin ALLOW FILTERING?**



**2. ¿Qué lecturas se comportaron como CP y cuáles como AP? ¿Qué nivel usarías para el saldo de una cuenta y cuál para un contador de reproducciones, y por qué?**



**3. ¿Cómo se enteró el nodo apagado de tu venta? ¿Qué pasaría si el nodo estuviera apagado más tiempo que max_hint_window?**



---

## 3. Mini-reto

> Los archivos van en `mini-reto/`: `modelo.cql`, `consultas.cql`, `resultados.txt` y `carga.*`.

### Tablas

> Una fila por tabla.

| Tabla | Consulta que responde | Partition key | Clustering key |
|---|---|---|---|
| | C1 | | |
| | C2 | | |
| | C3 | | |
| | C4 | | |

### Justificación

**Por qué esas llaves:**



**Qué datos quedaron duplicados entre tablas:**



**Qué hace la aplicación si cambia un dato duplicado:**



---

## 4. Problemas encontrados (opcional)

> Qué falló, qué intentaste y cómo lo resolviste.
