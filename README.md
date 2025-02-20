### Workshop: Implementación de un Clúster de Apache Cassandra y Monitoreo con Prometheus y Grafana

#### **Objetivo del Workshop:**
1. Crear y administrar un clúster distribuido de Apache Cassandra.
2. Aprender a expandir un clúster añadiendo nuevos nodos y centros de datos.
3. Configurar y utilizar Prometheus y Grafana para monitorear el clúster en tiempo real.
4. Crear una tabla para registrar clicks en una página web.
5. Implementar una tabla con un campo acumulador que sume automáticamente.

---

### **Anexo: Comandos Básicos de cqlsh y nodetool**

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

6. **Consultar los primeros 10 registros de una tabla**
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

2. **Ver las propiedades de un nodo dentro del clúster**
   ```bash
   nodetool info
   ```

3. **Ver la distribución de datos en el clúster**
   ```bash
   nodetool ring
   ```

4. **Reparar inconsistencias de datos en un nodo**
   ```bash
   nodetool repair
   ```

5. **Forzar la compactación de datos en un nodo**
   ```bash
   nodetool compact
   ```

6. **Limpiar los datos de nodos removidos**
   ```bash
   nodetool cleanup
   ```

7. **Ver las métricas de uso de memoria y carga del nodo**
   ```bash
   nodetool gcstats
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

