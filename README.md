### Workshop: Implementación de un Clúster de Apache Cassandra y Monitoreo con Prometheus y Grafana

#### **Objetivo del Workshop:**
1. Crear y administrar un clúster distribuido de Apache Cassandra.
2. Aprender a expandir un clúster añadiendo nuevos nodos y centros de datos.
3. Configurar y utilizar Prometheus y Grafana para monitorear el clúster en tiempo real.
4. Crear una tabla para registrar clics en una página web.
5. Implementar una tabla con un campo acumulador que sume automáticamente.

---

### **Parte 1: Configuración Inicial del Primer Nodo**

1. **Instalar Cassandra utilizando Docker**  
   ```bash
   docker network create cassandra_net
   docker run --name cassandra1 --network cassandra_net -d \
     -e CASSANDRA_CLUSTER_NAME="WorkshopCluster" \
     -e CASSANDRA_SEEDS="" \
     -p 9042:9042 \
     cassandra:4.0
   ```

2. **Verificar el estado del nodo**
   ```bash
   docker exec -it cassandra1 nodetool status
   ```

---

### **Parte 2: Agregar el Segundo Nodo al Clúster**

1. **Levantar el segundo nodo y conectarlo al clúster:**
   ```bash
   docker run --name cassandra2 --network cassandra_net -d \
     -e CASSANDRA_CLUSTER_NAME="WorkshopCluster" \
     -e CASSANDRA_SEEDS="cassandra1" \
     -p 9043:9042 \
     cassandra:4.0
   ```

2. **Verificar que el segundo nodo se haya unido:**
   ```bash
   docker exec -it cassandra1 nodetool status
   ```

---

### **Parte 3: Agregar el Tercer Nodo**

1. **Levantar el tercer nodo:**
   ```bash
   docker run --name cassandra3 --network cassandra_net -d \
     -e CASSANDRA_CLUSTER_NAME="WorkshopCluster" \
     -e CASSANDRA_SEEDS="cassandra1" \
     -p 9044:9042 \
     cassandra:4.0
   ```

2. **Verificar que el tercer nodo se haya unido al clúster:**
   ```bash
   docker exec -it cassandra1 nodetool status
   ```

---

### **Parte 4: Crear un Segundo Data Center (2 nodos)**

1. **Levantar el cuarto y quinto nodo en un nuevo Data Center:**
   ```bash
   docker run --name cassandra4 --network cassandra_net -d \
     -e CASSANDRA_DC="datacenter2" \
     -e CASSANDRA_CLUSTER_NAME="WorkshopCluster" \
     -e CASSANDRA_SEEDS="cassandra1" \
     -p 9045:9042 \
     cassandra:4.0

   docker run --name cassandra5 --network cassandra_net -d \
     -e CASSANDRA_DC="datacenter2" \
     -e CASSANDRA_CLUSTER_NAME="WorkshopCluster" \
     -e CASSANDRA_SEEDS="cassandra1" \
     -p 9046:9042 \
     cassandra:4.0
   ```

---

### **Parte 5: Configuración de Monitoreo con Prometheus y Grafana**

1. **Levantar Prometheus:**
   ```bash
   docker run --name prometheus -d -p 9090:9090 \
     -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
     prom/prometheus
   ```

2. **Levantar Grafana:**
   ```bash
   docker run --name grafana -d -p 3000:3000 grafana/grafana
   ```

3. **Configurar un Dashboard en Grafana:**
   - Acceder a `http://localhost:3000`.
   - Configurar Prometheus como fuente de datos.

---

### **Parte 6: Creación de Keyspace y Tablas**

1. **Crear un keyspace con replicación de factor 2:**
   ```sql
   CREATE KEYSPACE workshop WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};
   ```

2. **Usar el keyspace recién creado:**
   ```sql
   USE workshop;
   ```

3. **Crear una tabla para simular clics en una página web:**
   ```sql
   CREATE TABLE event_clicks (
     user_id UUID,
     page TEXT,
     click_time TIMESTAMP,
     PRIMARY KEY (user_id, click_time)
   );
   ```

4. **Insertar 10 registros en event_clicks:**
   ```sql
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'homepage', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'about', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'contact', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'services', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'blog', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'products', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'support', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'faq', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'testimonials', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'pricing', toTimestamp(now()));
   ```

5. **Crear una tabla con acumulador:**
   ```sql
   CREATE TABLE page_clicks_counter (
     page TEXT PRIMARY KEY,
     click_count COUNTER
   );
   ```

6. **Insertar 10 registros acumulativos en page_clicks_counter:**
   ```sql
   UPDATE page_clicks_counter SET click_count = click_count + 1 WHERE page = 'homepage';
   UPDATE page_clicks_counter SET click_count = click_count + 1 WHERE page = 'about';
   UPDATE page_clicks_counter SET click_count = click_count + 1 WHERE page = 'contact';
   UPDATE page_clicks_counter SET click_count = click_count + 1 WHERE page = 'services';
   UPDATE page_clicks_counter SET click_count = click_count + 1 WHERE page = 'blog';
   UPDATE page_clicks_counter SET click_count = click_count + 1 WHERE page = 'products';
   UPDATE page_clicks_counter SET click_count = click_count + 1 WHERE page = 'support';
   UPDATE page_clicks_counter SET click_count = click_count + 1 WHERE page = 'faq';
   UPDATE page_clicks_counter SET click_count = click_count + 1 WHERE page = 'testimonials';
   UPDATE page_clicks_counter SET click_count = click_count + 1 WHERE page = 'pricing';
   ```

---

### **Anexo: Comandos de Administración en cqlsh y nodetool**

#### **Comandos en cqlsh**

1. **Conectar a cqlsh**
   ```bash
   docker exec -it cassandra1 cqlsh
   ```

2. **Listar keyspaces disponibles**
   ```sql
   DESCRIBE KEYSPACES;
   ```

3. **Ver detalles de un keyspace específico**
   ```sql
   DESCRIBE KEYSPACE workshop;
   ```

4. **Listar todas las tablas dentro de un keyspace**
   ```sql
   USE workshop;
   DESCRIBE TABLES;
   ```

5. **Ver la estructura de una tabla específica**
   ```sql
   DESCRIBE TABLE event_clicks;
   ```

6. **Consultar registros de una tabla**
   ```sql
   SELECT * FROM event_clicks LIMIT 10;
   ```

7. **Eliminar un registro de una tabla**
   ```sql
   DELETE FROM event_clicks WHERE user_id = <UUID> AND click_time = '<TIMESTAMP>';
   ```

8. **Eliminar todos los registros de una tabla sin eliminar la estructura**
   ```sql
   TRUNCATE event_clicks;
   ```

---

#### **Comandos de nodetool**

1. **Ver el estado de los nodos del clúster**
   ```bash
   nodetool status
   ```

2. **Ver información detallada de un nodo**
   ```bash
   nodetool info
   ```

3. **Reparar inconsistencias de datos en un nodo**
   ```bash
   nodetool repair
   ```

4. **Forzar la compactación de datos en un nodo**
   ```bash
   nodetool compact
   ```

5. **Limpiar los datos de nodos removidos**
   ```bash
   nodetool cleanup
   ```

6. **Ver la distribución de datos en el clúster**
   ```bash
   nodetool ring
   ```

---

#### **Agregar y quitar nodos en el clúster**

1. **Agregar un nuevo nodo al clúster:**
   - Editar el archivo de configuración `cassandra.yaml` en el nuevo nodo y establecer:
     ```yaml
     - seeds: "IP_DEL_NODO_EXISTENTE"
     ```
   - Iniciar el nuevo nodo con:
     ```bash
     docker run --name cassandra_new --network cassandra_net -d \
       -e CASSANDRA_CLUSTER_NAME="WorkshopCluster" \
       -e CASSANDRA_SEEDS="IP_DEL_NODO_EXISTENTE" \
       -p 9047:9042 \
       cassandra:4.0
     ```
   - Verificar que se haya agregado correctamente:
     ```bash
     nodetool status
     ```

2. **Quitar un nodo del clúster:**
   - Identificar el nodo que se quiere quitar con `nodetool status`.
   - Ejecutar el comando para deshabilitar el nodo:
     ```bash
     nodetool decommission
     ```
   - Si el nodo está fallando y no puede ser deshabilitado correctamente:
     ```bash
     nodetool removenode <ID_DEL_NODO>
     ```

3. **Reequilibrar el clúster después de quitar un nodo:**
   ```bash
   nodetool cleanup
   ```

