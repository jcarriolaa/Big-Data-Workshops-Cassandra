# Bitácora del taller de Cassandra


- **Nombre:**
- **Carné:** 99999999
- **Grupo:**
- **Tu nodo en el clúster del grupo:** cassandra2

---

## 1. Evidencias


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


| Nodos caídos | `ONE` | `QUORUM` | `ALL` |
|---|---|---|---|
| 0 | ✅ | ✅ | ✅ |
| 1 | ✅ | ✅ | ❌ |
| 2 | ✅ | ❌ | ❌ |

---

## 2. Preguntas

**1. ¿Qué línea de la traza muestra que la consulta por ciudad leyó una sola partición, y cuál que la de producto recorrió toda la tabla? ¿Por qué Cassandra rechaza la segunda sin ALLOW FILTERING?**

respuesta de prueba del validador con suficientes palabras para superar el mínimo de quince palabras exigido 1.



**2. ¿Qué lecturas se comportaron como CP y cuáles como AP? ¿Qué nivel usarías para el saldo de una cuenta y cuál para un contador de reproducciones, y por qué?**

respuesta de prueba del validador con suficientes palabras para superar el mínimo de quince palabras exigido 2.



**3. ¿Cómo se enteró el nodo apagado de tu venta? ¿Qué pasaría si el nodo estuviera apagado más tiempo que max_hint_window?**

respuesta de prueba del validador con suficientes palabras para superar el mínimo de quince palabras exigido 3.



---

## 3. Mini-reto


### Tablas


| Tabla | Consulta que responde | Partition key | Clustering key |
|---|---|---|---|
| tabla_c1 | C1 | x | y |
| tabla_c2 | C2 | x | y |
| tabla_c3 | C3 | x | y |
| tabla_c4 | C4 | x | y |

### Justificación

**Por qué esas llaves:**

respuesta de prueba del validador con suficientes palabras para superar el mínimo de quince palabras exigido Por qu



**Qué datos quedaron duplicados entre tablas:**

respuesta de prueba del validador con suficientes palabras para superar el mínimo de quince palabras exigido Qué da



**Qué hace la aplicación si cambia un dato duplicado:**

respuesta de prueba del validador con suficientes palabras para superar el mínimo de quince palabras exigido Qué ha



---

## 4. Problemas encontrados (opcional)
