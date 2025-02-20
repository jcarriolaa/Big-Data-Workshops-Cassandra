### Workshop: Implementación de un Clúster de Apache Cassandra y Monitoreo con Prometheus y Grafana

#### **Objetivo del Workshop:**
1. Crear y administrar un clúster distribuido de Apache Cassandra.
2. Aprender a expandir un clúster añadiendo nuevos nodos y centros de datos.
3. Configurar y utilizar Prometheus y Grafana para monitorear el clúster en tiempo real.
4. Crear una tabla para registrar clicks en una página web.
5. Implementar una tabla con un campo acumulador que sume automáticamente.

---

### **Parte 1: Configuración Inicial del Primer Nodo**

1. **Instalación de Cassandra (Primer Nodo)**  
   Usaremos **Docker** para simplificar el proceso:
   ```bash
   docker network create cassandra_net
   docker run --name cassandra1 --network cassandra_net -d \
     -e CASSANDRA_CLUSTER_NAME="WorkshopCluster" \
     -e CASSANDRA_SEEDS="" \
     -p 9042:9042 \
     cassandra:4.0
   ```
   **Verifica que el nodo esté funcionando:**
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

### **Parte 5: Crear una Tabla para Simular Clicks en una Página Web**

1. **Conectar a Cassandra**
   ```bash
   docker exec -it cassandra1 cqlsh
   ```

2. **Crear la Keyspace y la Tabla event_clicks**
   ```sql
   CREATE KEYSPACE workshop WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};
   USE workshop;

   CREATE TABLE event_clicks (
     user_id UUID,
     page TEXT,
     click_time TIMESTAMP,
     PRIMARY KEY (user_id, click_time)
   );
   ```

3. **Insertar Datos en event_clicks**
   ```sql
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'homepage', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'about', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'contact', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'services', toTimestamp(now()));
   INSERT INTO event_clicks (user_id, page, click_time) VALUES (uuid(), 'blog', toTimestamp(now()));
   ```

---

### **Parte 6: Crear una Tabla con Acumulador**

1. **Crear la Tabla con un Contador**
   ```sql
   CREATE TABLE page_clicks_counter (
     page TEXT PRIMARY KEY,
     click_count COUNTER
   );
   ```

2. **Insertar Datos en la Tabla de Contador**
   ```sql
   UPDATE page_clicks_counter SET click_count = click_count + 1 WHERE page = 'homepage';
   UPDATE page_clicks_counter SET click_count = click_count + 1 WHERE page = 'about';
   ```

---

### **Parte 7: Configuración de Prometheus y Grafana**

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
   - Accede a `http://localhost:3000`
   - Crea un nuevo dashboard e integra Prometheus como fuente de datos.

---

### **Notas Finales:**
- Asegúrate de que cada paso funcione antes de pasar al siguiente.
- Prometheus y Grafana te permiten visualizar en tiempo real el estado de tu clúster.
- Cassandra soporta contadores para almacenar y actualizar valores de forma eficiente.

---

### **Próximos pasos:**
- Experimentar con diferentes configuraciones de Cassandra.
- Implementar estrategias de replicación y consistencia.
- Optimizar el monitoreo y las alertas según las necesidades del clúster.

