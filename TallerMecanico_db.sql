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
  `cod_cliente` int PRIMARY KEY auto_increment,
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

CREATE TABLE Usuarios (
  email VARCHAR(150) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  contraseña  VARCHAR(150) NOT NULL,
  legajo INT NOT NULL,
  FOREIGN KEY (`legajo`) REFERENCES `Empleado` (`legajo`)
  
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
insert into Persona values(1,"Name","LastName","12","12");
insert into Empleado values (1,1);
insert into Usuarios values ("Robert@gmail.com","Name","1234",1), ("Fran@gmail.com","Name","1234",1), ("Jos@gmail.com","Name","1234",1),("1","Name","1",1);