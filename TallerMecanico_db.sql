DROP DATABASE IF EXISTS `TallerMecanico`;
CREATE DATABASE `TallerMecanico`;
USE `TallerMecanico`;

CREATE TABLE `Persona` (
  `dni` varchar(10) PRIMARY KEY NOT NULL,
  `nombre` varchar(10) NOT NULL,
  `apellido` varchar(10) NOT NULL,
  `tel` varchar(10),
  `dir` varchar(25)
);

CREATE TABLE `Cliente` (
  `cod_cliente` varchar(10) PRIMARY KEY NOT NULL,
  `dni_cliente` varchar(10)  NOT NULL
);

CREATE TABLE `Empleado` (
  `legajo` INT PRIMARY KEY NOT NULL,
  `dni_empleado` varchar(10) NOT NULL
);

CREATE TABLE `Provedor` (
  `cod_Provedor` varchar(10) PRIMARY KEY NOT NULL,
  `dni_Provedor` varchar(10)  NOT NULL
);


alter table Cliente
add index Fk_dni_cliente (`dni_cliente`);

alter table Cliente
add constraint Fk_dni_cliente
foreign key (`dni_cliente`)
    references Persona (`dni`)
    on delete no action
    on update cascade;

alter table Empleado
add index Fk_dni_empleado (`dni_empleado`);

alter table Empleado
add constraint Fk_dni_empleado
foreign key (`dni_empleado`)
    references Persona (`dni`)
    on delete no action
    on update cascade;

CREATE TABLE `Vehiculo` (
  `matricula` varchar(10) PRIMARY KEY,
  `color` varchar(10),
  `modelo` varchar(10),
  `dni_cliente` varchar(10) ,
   FOREIGN KEY (dni_cliente) REFERENCES Persona(dni)
);

#DROP TABLE IF EXISTS `Reparaciones`;


CREATE TABLE `Repuesto` (
  `nombre` varchar(25) PRIMARY KEY,
  `precio_x_unidad` float,
  `cantidad` int
);

CREATE TABLE `Reparaciones` (
  `id` int auto_increment PRIMARY KEY,
  `fecha_entrada` date,
  `matricula_vehiculo` varchar(25),
  FOREIGN KEY (`matricula_vehiculo`) REFERENCES `Vehiculo` (`matricula`)
);

CREATE TABLE `Mecanico_Reparacion` (
  `id` int auto_increment PRIMARY KEY,
  `legajo` INT,
  `reparacion_id` int,
  FOREIGN KEY (`legajo`) REFERENCES `Empleado` (`legajo`),
  FOREIGN KEY (`reparacion_id`) REFERENCES `Reparaciones` (`id`)
);

CREATE TABLE `Repuesto_Reparacion` (
  `id_RR` int auto_increment primary Key,
  `repuesto` varchar(25),
  `reparacion_id` int,
  `cantidad` int,
  `Precio` float,
  FOREIGN KEY (`repuesto`) REFERENCES `Repuesto` (`nombre`),
  FOREIGN KEY (`reparacion_id`) REFERENCES `Reparaciones` (`id`)
);

CREATE TABLE IF NOT EXISTS Usuarios (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL
);

CREATE TABLE `Ficha_Tecnica` (
  `id_FT` int auto_increment primary Key,
  `Vehiculo_Matricula` varchar(10),
  `nroEmpleados` int,
  `subtotal`float,
  `mano_de_obra`float,
  `total`float,
  FOREIGN KEY (`Vehiculo_Matricula`) REFERENCES `Vehiculo` (`matricula`)
);

INSERT INTO Persona (dni,nombre,apellido,tel,dir) VALUES
('0001','Juan','Pérez','111111111','Calle 1'),
('0002','Ana','Gómez','222222222','Calle 2'),
('0003','Luis','López','333333333','Calle 3'),
('0004','María','Sánchez','444444444','Calle 4'),
('0005','Pedro','Torres','555555555','Calle 5'),
('0006','Sofía','Romero','666666666','Calle 6'),
('0007','Diego','Ruiz','777777777','Calle 7'),
('0008','Lucía','Díaz','888888888','Calle 8'),
('0009','Carlos','Fernández','999999999','Calle 9'),
('0010','Clara','Vega','101010101','Calle 10'),
('0011','Matías','Navarro','121212121','Calle 11'),
('0012','Camila','Méndez','131313131','Calle 12'),
('0013','Federico','Cruz','141414141','Calle 13'),
('0014','Valentina','Mora','151515151','Calle 14'),
('0015','Ignacio','Rojas','161616161','Calle 15'),
('0016','Mariana','Silva','171717171','Calle 16'),
('0017','Gonzalo','Flores','181818181','Calle 17'),
('0018','Florencia','Pérez','191919191','Calle 18'),
('0019','Bruno','Herrera','202020202','Calle 19'),
('0020','Sabrina','Gómez','212121212','Calle 20');

-- INSERT: 10 CLIENTES
INSERT INTO Cliente (cod_cliente,dni_cliente) VALUES
('CLI01','0001'),('CLI02','0002'),('CLI03','0003'),
('CLI04','0004'),('CLI05','0005'),('CLI06','0006'),
('CLI07','0007'),('CLI08','0008'),('CLI09','0009'),
('CLI10','0010');

-- INSERT: 10 EMPLEADOS
INSERT INTO Empleado (legajo,dni_empleado) VALUES
(101,'0011'),(102,'0012'),(103,'0013'),(104,'0014'),(105,'0015'),
(106,'0016'),(107,'0017'),(108,'0018'),(109,'0019'),(110,'0020');

-- INSERT: 10 VEHICULOS
INSERT INTO Vehiculo (matricula,color,modelo,dni_cliente) VALUES
('A101','Rojo','Fiesta','0001'),
('B202','Azul','Focus','0002'),
('C303','Verde','Eco','0003'),
('D404','Negro','Golf','0004'),
('E505','Blanco','Clio','0005'),
('F606','Gris','Corsa','0006'),
('G707','Azul','Polo','0007'),
('H808','Rojo','Uno','0008'),
('I909','Verde','Mobi','0009'),
('J010','Negro','Sandero','0010');

-- INSERT: 10 REPUESTOS
INSERT INTO Repuesto (nombre,precio_x_unidad,cantidad) VALUES
('FiltroAceite',1500,10),
('FiltroAire',1200,12),
('PastillasFreno',5000,8),
('AceiteMotor',3000,15),
('Bujias',2000,20),
('Correa',7000,5),
('Bateria',15000,3),
('Amortiguador',6000,4),
('Radiador',10000,2),
('Embrague',12000,1);

-- INSERT: 10 REPARACIONES
INSERT INTO Reparaciones (fecha_entrada,matricula_vehiculo) VALUES
('2025-06-01','A101'),('2025-06-02','B202'),
('2025-06-03','C303'),('2025-06-04','D404'),
('2025-06-05','E505'),('2025-06-06','F606'),
('2025-06-07','G707'),('2025-06-08','H808'),
('2025-06-09','I909'),('2025-06-10','J010');

-- INSERT: 10 MECANICO_REPARACION
INSERT INTO Mecanico_Reparacion (legajo,reparacion_id) VALUES
(101,1),(102,2),(103,3),(104,4),(105,5),
(106,6),(107,7),(108,8),(109,9),(110,10);

-- INSERT: 10 REPUESTO_REPARACION
INSERT INTO Repuesto_Reparacion (repuesto,reparacion_id,cantidad,Precio) VALUES
('FiltroAceite',1,1,1500),
('FiltroAire',2,2,2400),
('PastillasFreno',3,1,5000),
('AceiteMotor',4,3,9000),
('Bujias',5,2,4000),
('Correa',6,1,7000),
('Bateria',7,1,15000),
('Amortiguador',8,2,12000),
('Radiador',9,1,10000),
('Embrague',10,1,12000);

-- INSERT: 10 FICHA_TECNICA
INSERT INTO Ficha_Tecnica (Vehiculo_Matricula,nroEmpleados,subtotal,mano_de_obra,total) VALUES
('A101',1,1500,3000,4500),
('B202',1,2400,3000,5400),
('C303',1,5000,3000,8000),
('D404',1,9000,3000,12000),
('E505',1,4000,3000,7000),
('F606',1,7000,3000,10000),
('G707',1,15000,3000,18000),
('H808',1,12000,3000,15000),
('I909',1,10000,3000,13000),
('J010',1,12000,3000,15000);