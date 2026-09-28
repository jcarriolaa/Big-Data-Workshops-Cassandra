CREATE TABLE pasajeros (
  pasajero_id  VARCHAR(10) PRIMARY KEY,
  nombre       VARCHAR(60) NOT NULL,
  ciudad       VARCHAR(30) NOT NULL,
  calificacion DECIMAL(3,2) NOT NULL
);
CREATE TABLE conductores (
  conductor_id VARCHAR(10) PRIMARY KEY,
  nombre       VARCHAR(60) NOT NULL,
  ciudad       VARCHAR(30) NOT NULL,
  vehiculo     VARCHAR(40) NOT NULL,
  placa        VARCHAR(10) NOT NULL
);
CREATE TABLE viajes (
  viaje_id     INTEGER PRIMARY KEY,
  pasajero_id  VARCHAR(10) NOT NULL REFERENCES pasajeros(pasajero_id),
  conductor_id VARCHAR(10) NOT NULL REFERENCES conductores(conductor_id),
  ciudad       VARCHAR(30) NOT NULL,
  inicio       TIMESTAMP NOT NULL,
  fin          TIMESTAMP NOT NULL,
  distancia_km DECIMAL(5,1) NOT NULL,
  tarifa       DECIMAL(8,2) NOT NULL
);
CREATE TABLE pagos (
  pago_id   INTEGER PRIMARY KEY,
  viaje_id  INTEGER NOT NULL REFERENCES viajes(viaje_id),
  metodo    VARCHAR(10) NOT NULL,
  monto     DECIMAL(8,2) NOT NULL,
  pagado_en TIMESTAMP NOT NULL
);
