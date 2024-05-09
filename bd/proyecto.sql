CREATE DATABASE  IF NOT EXISTS `blancos_valentina` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `blancos_valentina`;
-- MySQL dump 10.13  Distrib 8.0.29, for macos12 (x86_64)
--
-- Host: localhost    Database: blancos_valentina
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `anio_apartado`
--

DROP TABLE IF EXISTS `anio_apartado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anio_apartado` (
  `ID_AA` int NOT NULL AUTO_INCREMENT,
  `Anio_Apartado` int NOT NULL,
  PRIMARY KEY (`ID_AA`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anio_apartado`
--

LOCK TABLES `anio_apartado` WRITE;
/*!40000 ALTER TABLE `anio_apartado` DISABLE KEYS */;
INSERT INTO `anio_apartado` VALUES (1,2024),(2,2025),(3,2026),(4,2027),(5,2028);
/*!40000 ALTER TABLE `anio_apartado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anio_compra`
--

DROP TABLE IF EXISTS `anio_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anio_compra` (
  `ID_AC` int NOT NULL AUTO_INCREMENT,
  `Anio_Compra` int NOT NULL,
  PRIMARY KEY (`ID_AC`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anio_compra`
--

LOCK TABLES `anio_compra` WRITE;
/*!40000 ALTER TABLE `anio_compra` DISABLE KEYS */;
INSERT INTO `anio_compra` VALUES (1,2024),(2,2025),(3,2026),(4,2027),(5,2028);
/*!40000 ALTER TABLE `anio_compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anio_envio`
--

DROP TABLE IF EXISTS `anio_envio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anio_envio` (
  `ID_AE` int NOT NULL AUTO_INCREMENT,
  `Anio_Envio` int NOT NULL,
  PRIMARY KEY (`ID_AE`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anio_envio`
--

LOCK TABLES `anio_envio` WRITE;
/*!40000 ALTER TABLE `anio_envio` DISABLE KEYS */;
INSERT INTO `anio_envio` VALUES (1,2024),(2,2025),(3,2026),(4,2027),(5,2028);
/*!40000 ALTER TABLE `anio_envio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anio_venta`
--

DROP TABLE IF EXISTS `anio_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anio_venta` (
  `ID_AV` int NOT NULL AUTO_INCREMENT,
  `Anio_Venta` int NOT NULL,
  PRIMARY KEY (`ID_AV`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anio_venta`
--

LOCK TABLES `anio_venta` WRITE;
/*!40000 ALTER TABLE `anio_venta` DISABLE KEYS */;
INSERT INTO `anio_venta` VALUES (1,2024),(2,2025),(3,2026),(4,2027),(5,2028);
/*!40000 ALTER TABLE `anio_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apartados`
--

DROP TABLE IF EXISTS `apartados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apartados` (
  `ID_Apartados` int NOT NULL AUTO_INCREMENT,
  `Cantidad_Abonada` float NOT NULL,
  `Deuda_Pendiente` float NOT NULL,
  `Dias_Restantes` int NOT NULL,
  `ID_Status` int NOT NULL,
  `ID_DA` int NOT NULL,
  `ID_MA` int NOT NULL,
  `ID_AA` int NOT NULL,
  `ID_DL` int NOT NULL,
  `ID_ML` int NOT NULL,
  `ID_AL` int NOT NULL,
  `ID_DU` int NOT NULL,
  `ID_MU` int NOT NULL,
  `ID_AU` int NOT NULL,
  PRIMARY KEY (`ID_Apartados`),
  KEY `FKID_Status` (`ID_Status`),
  KEY `KFID_DA` (`ID_DA`),
  KEY `FKID_MA` (`ID_MA`),
  KEY `FKID_AA` (`ID_AA`),
  KEY `FKID_DL` (`ID_DL`),
  KEY `FKID_ML` (`ID_ML`),
  KEY `FKID_AL` (`ID_AL`),
  KEY `FKID_DU` (`ID_DU`),
  KEY `FKID_MU` (`ID_MU`),
  KEY `FKID_AU` (`ID_AU`),
  CONSTRAINT `apartados_ibfk_1` FOREIGN KEY (`ID_Status`) REFERENCES `status` (`ID_Status`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `apartados_ibfk_10` FOREIGN KEY (`ID_MU`) REFERENCES `mes_apartado` (`ID_MA`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `apartados_ibfk_2` FOREIGN KEY (`ID_DA`) REFERENCES `dia_apartado` (`ID_DA`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `apartados_ibfk_3` FOREIGN KEY (`ID_MA`) REFERENCES `mes_apartado` (`ID_MA`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `apartados_ibfk_4` FOREIGN KEY (`ID_AA`) REFERENCES `anio_apartado` (`ID_AA`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `apartados_ibfk_5` FOREIGN KEY (`ID_AL`) REFERENCES `anio_apartado` (`ID_AA`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `apartados_ibfk_6` FOREIGN KEY (`ID_DL`) REFERENCES `dia_apartado` (`ID_DA`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `apartados_ibfk_7` FOREIGN KEY (`ID_ML`) REFERENCES `mes_apartado` (`ID_MA`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `apartados_ibfk_8` FOREIGN KEY (`ID_DU`) REFERENCES `dia_apartado` (`ID_DA`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `apartados_ibfk_9` FOREIGN KEY (`ID_AU`) REFERENCES `anio_apartado` (`ID_AA`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apartados`
--

LOCK TABLES `apartados` WRITE;
/*!40000 ALTER TABLE `apartados` DISABLE KEYS */;
INSERT INTO `apartados` VALUES (1,200,300,13,1,6,2,1,21,2,1,6,2,1);
/*!40000 ALTER TABLE `apartados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `ID_C` int NOT NULL AUTO_INCREMENT,
  `Categoria` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_C`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (1,'Ropa de Cama'),(2,'Toallas y Batas'),(3,'Cortinas y Persianas'),(4,'Decoración para el Hogar'),(5,'Textiles de Cocina');
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celulares`
--

DROP TABLE IF EXISTS `celulares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `celulares` (
  `ID_CEL` int NOT NULL AUTO_INCREMENT,
  `Celular` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_CEL`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celulares`
--

LOCK TABLES `celulares` WRITE;
/*!40000 ALTER TABLE `celulares` DISABLE KEYS */;
INSERT INTO `celulares` VALUES (1,'9994094154'),(2,'5551234567'),(3,'6669876543'),(4,'7772345678'),(5,'8888765432'),(6,'3337654321'),(7,'2228765432'),(8,'4449876543'),(9,'9992345678'),(10,'1113456789');
/*!40000 ALTER TABLE `celulares` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `ID_Cliente` int NOT NULL AUTO_INCREMENT,
  `Nombres` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `Apellido_P` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `Apellido_M` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Total_Adeudo` float DEFAULT NULL,
  `ID_CEL` int NOT NULL,
  `ID_AP` int NOT NULL,
  PRIMARY KEY (`ID_Cliente`),
  KEY `FKID_CEL` (`ID_CEL`),
  KEY `FKID_AP` (`ID_AP`),
  CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`ID_CEL`) REFERENCES `celulares` (`ID_CEL`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `clientes_ibfk_2` FOREIGN KEY (`ID_AP`) REFERENCES `t_apartado` (`ID_AP`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'Carlos Eduardo','Bojórquez','Ruiz',900,1,1),(2,'Cristian Leonardo','Kantún','Ramirez',800,2,2),(3,'Carlos Eduardo','Valencia','Hernández',700,3,2),(4,'Eduardo José','Santiago','Medina',600,4,2),(5,'Eduardo','Escalante','Pacheco',500,5,2);
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `colonia`
--

DROP TABLE IF EXISTS `colonia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonia` (
  `ID_C` int NOT NULL AUTO_INCREMENT,
  `Colonia` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_C`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colonia`
--

LOCK TABLES `colonia` WRITE;
/*!40000 ALTER TABLE `colonia` DISABLE KEYS */;
INSERT INTO `colonia` VALUES (1,'Flamboyanes'),(2,'Chuburna'),(3,'Causel');
/*!40000 ALTER TABLE `colonia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `destino`
--

DROP TABLE IF EXISTS `destino`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `destino` (
  `ID_Destino` int NOT NULL AUTO_INCREMENT,
  `Destino` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_Destino`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `destino`
--

LOCK TABLES `destino` WRITE;
/*!40000 ALTER TABLE `destino` DISABLE KEYS */;
INSERT INTO `destino` VALUES (1,'Progreso'),(2,'Mérida');
/*!40000 ALTER TABLE `destino` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dia_apartado`
--

DROP TABLE IF EXISTS `dia_apartado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dia_apartado` (
  `ID_DA` int NOT NULL AUTO_INCREMENT,
  `Dia_Apartado` int NOT NULL,
  PRIMARY KEY (`ID_DA`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dia_apartado`
--

LOCK TABLES `dia_apartado` WRITE;
/*!40000 ALTER TABLE `dia_apartado` DISABLE KEYS */;
INSERT INTO `dia_apartado` VALUES (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19,19),(20,20),(21,21),(22,22),(23,23),(24,24),(25,25),(26,26),(27,27),(28,28),(29,29),(30,30),(31,31);
/*!40000 ALTER TABLE `dia_apartado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dia_compra`
--

DROP TABLE IF EXISTS `dia_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dia_compra` (
  `ID_DC` int NOT NULL AUTO_INCREMENT,
  `Dia_Compra` int NOT NULL,
  PRIMARY KEY (`ID_DC`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dia_compra`
--

LOCK TABLES `dia_compra` WRITE;
/*!40000 ALTER TABLE `dia_compra` DISABLE KEYS */;
INSERT INTO `dia_compra` VALUES (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19,19),(20,20),(21,21),(22,22),(23,23),(24,24),(25,25),(26,26),(27,27),(28,28),(29,29),(30,30),(31,31);
/*!40000 ALTER TABLE `dia_compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dia_envio`
--

DROP TABLE IF EXISTS `dia_envio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dia_envio` (
  `ID_DE` int NOT NULL AUTO_INCREMENT,
  `Dia_Envio` int NOT NULL,
  PRIMARY KEY (`ID_DE`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dia_envio`
--

LOCK TABLES `dia_envio` WRITE;
/*!40000 ALTER TABLE `dia_envio` DISABLE KEYS */;
INSERT INTO `dia_envio` VALUES (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19,19),(20,20),(21,21),(22,22),(23,23),(24,24),(25,25),(26,26),(27,27),(28,28),(29,29),(30,30),(31,31);
/*!40000 ALTER TABLE `dia_envio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dia_venta`
--

DROP TABLE IF EXISTS `dia_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dia_venta` (
  `ID_DV` int NOT NULL AUTO_INCREMENT,
  `Dia_Venta` int NOT NULL,
  PRIMARY KEY (`ID_DV`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dia_venta`
--

LOCK TABLES `dia_venta` WRITE;
/*!40000 ALTER TABLE `dia_venta` DISABLE KEYS */;
INSERT INTO `dia_venta` VALUES (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19,19),(20,20),(21,21),(22,22),(23,23),(24,24),(25,25),(26,26),(27,27),(28,28),(29,29),(30,30),(31,31);
/*!40000 ALTER TABLE `dia_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `envios`
--

DROP TABLE IF EXISTS `envios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `envios` (
  `ID_Envios` int NOT NULL AUTO_INCREMENT,
  `Calle` int NOT NULL,
  `Cruzamiento_1` int NOT NULL,
  `Cruzamiento_2` int NOT NULL,
  `Dias_Para_El_Envio` int NOT NULL,
  `ID_DE` int NOT NULL,
  `ID_ME` int NOT NULL,
  `ID_AE` int NOT NULL,
  `ID_Destino` int NOT NULL,
  `ID_StatusE` int NOT NULL,
  `ID_C` int NOT NULL,
  PRIMARY KEY (`ID_Envios`),
  KEY `FKID_DE` (`ID_DE`),
  KEY `FKID_ME` (`ID_ME`),
  KEY `FKID_AE` (`ID_AE`),
  KEY `FKID_Destino` (`ID_Destino`),
  KEY `FKID_StatusE` (`ID_StatusE`),
  KEY `FKID_C` (`ID_C`),
  CONSTRAINT `envios_ibfk_1` FOREIGN KEY (`ID_StatusE`) REFERENCES `status_envio` (`ID_StatusE`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `envios_ibfk_2` FOREIGN KEY (`ID_C`) REFERENCES `colonia` (`ID_C`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `envios_ibfk_3` FOREIGN KEY (`ID_Destino`) REFERENCES `destino` (`ID_Destino`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `envios_ibfk_4` FOREIGN KEY (`ID_ME`) REFERENCES `mes_envio` (`ID_ME`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `envios_ibfk_5` FOREIGN KEY (`ID_DE`) REFERENCES `dia_envio` (`ID_DE`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `envios_ibfk_6` FOREIGN KEY (`ID_AE`) REFERENCES `anio_envio` (`ID_AE`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `envios`
--

LOCK TABLES `envios` WRITE;
/*!40000 ALTER TABLE `envios` DISABLE KEYS */;
INSERT INTO `envios` VALUES (1,87,102,104,7,8,3,1,1,1,1);
/*!40000 ALTER TABLE `envios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forma_pago`
--

DROP TABLE IF EXISTS `forma_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forma_pago` (
  `ID_FP` int NOT NULL AUTO_INCREMENT,
  `Forma_De_Pago` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_FP`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forma_pago`
--

LOCK TABLES `forma_pago` WRITE;
/*!40000 ALTER TABLE `forma_pago` DISABLE KEYS */;
INSERT INTO `forma_pago` VALUES (1,'Tarjeta'),(2,'Efectivo');
/*!40000 ALTER TABLE `forma_pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `ID_Login` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Contraseña` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_Login`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (1,'carlos','blancos_valentina@gmail.com','1234');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mes_apartado`
--

DROP TABLE IF EXISTS `mes_apartado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mes_apartado` (
  `ID_MA` int NOT NULL AUTO_INCREMENT,
  `Mes_Apartado` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_MA`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mes_apartado`
--

LOCK TABLES `mes_apartado` WRITE;
/*!40000 ALTER TABLE `mes_apartado` DISABLE KEYS */;
INSERT INTO `mes_apartado` VALUES (1,'Enero'),(2,'Febrero'),(3,'Marzo'),(4,'Abril'),(5,'Mayo'),(6,'Junio'),(7,'Julio'),(8,'Agosto'),(9,'Septiembre'),(10,'Octubre'),(11,'Noviembre'),(12,'Diciembre');
/*!40000 ALTER TABLE `mes_apartado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mes_compra`
--

DROP TABLE IF EXISTS `mes_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mes_compra` (
  `ID_MC` int NOT NULL AUTO_INCREMENT,
  `Mes_Compra` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_MC`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mes_compra`
--

LOCK TABLES `mes_compra` WRITE;
/*!40000 ALTER TABLE `mes_compra` DISABLE KEYS */;
INSERT INTO `mes_compra` VALUES (1,'Enero'),(2,'Febrero'),(3,'Marzo'),(4,'Abril'),(5,'Mayo'),(6,'Junio'),(7,'Julio'),(8,'Agosto'),(9,'Septiembre'),(10,'Octubre'),(11,'Noviembre'),(12,'Diciembre');
/*!40000 ALTER TABLE `mes_compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mes_envio`
--

DROP TABLE IF EXISTS `mes_envio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mes_envio` (
  `ID_ME` int NOT NULL AUTO_INCREMENT,
  `Mes_Envio` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_ME`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mes_envio`
--

LOCK TABLES `mes_envio` WRITE;
/*!40000 ALTER TABLE `mes_envio` DISABLE KEYS */;
INSERT INTO `mes_envio` VALUES (1,'Enero'),(2,'Febrero'),(3,'Marzo'),(4,'Abril'),(5,'Mayo'),(6,'Junio'),(7,'Julio'),(8,'Agosto'),(9,'Septiembre'),(10,'Octubre'),(11,'Noviembre'),(12,'Diciembre');
/*!40000 ALTER TABLE `mes_envio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mes_venta`
--

DROP TABLE IF EXISTS `mes_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mes_venta` (
  `ID_MV` int NOT NULL AUTO_INCREMENT,
  `Mes_Venta` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_MV`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mes_venta`
--

LOCK TABLES `mes_venta` WRITE;
/*!40000 ALTER TABLE `mes_venta` DISABLE KEYS */;
INSERT INTO `mes_venta` VALUES (1,'Enero'),(2,'Febrero'),(3,'Marzo'),(4,'Abril'),(5,'Mayo'),(6,'Junio'),(7,'Julio'),(8,'Agosto'),(9,'Septiembre'),(10,'Octubre'),(11,'Noviembre'),(12,'Diciembre');
/*!40000 ALTER TABLE `mes_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `ID_Producto` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `Precio_Compra` float NOT NULL,
  `Precio_Venta` float NOT NULL,
  `Ganancia_Producto` float NOT NULL,
  `Existencias` int NOT NULL,
  `Existencias_Deseadas` int DEFAULT NULL,
  `ID_Provedor` int NOT NULL,
  `ID_C` int NOT NULL,
  PRIMARY KEY (`ID_Producto`),
  KEY `FKID_C` (`ID_C`),
  KEY `FKID_P` (`ID_Provedor`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`ID_C`) REFERENCES `categoria` (`ID_C`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `producto_ibfk_2` FOREIGN KEY (`ID_Provedor`) REFERENCES `proveedor` (`ID_Proveedor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'Sábana Suave',80,200,120,25,25,1,3),(2,'Almohada de plumas',70,180,110,30,30,1,4),(3,'Toalla de playa XL',60,150,90,20,20,2,2),(4,'Juego de sábanas King',120,320,200,10,10,3,3),(5,'Toalla de mano bordada',45,125,80,35,35,4,2),(6,'Funda de almohada sedosa',30,90,60,50,50,5,4),(7,'Toalla de baño de lujo',55,150,95,18,18,6,2),(8,'Juego de sábanas doble',90,240,150,28,28,7,3),(9,'Almohada ergonómica',65,165,100,40,40,8,4),(10,'Toalla Del America',80,200,120,25,25,9,3);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto_venta`
--

DROP TABLE IF EXISTS `producto_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_venta` (
  `ID_PV` int NOT NULL AUTO_INCREMENT,
  `ID_Producto` int NOT NULL,
  `ID_Venta` int NOT NULL,
  `Cantidad_Vendida` int NOT NULL,
  `Subtotal_Vendido` float DEFAULT NULL,
  `Subtotal_Reinversión` float DEFAULT NULL,
  `Subtotal_Ganancia` float DEFAULT NULL,
  PRIMARY KEY (`ID_PV`),
  KEY `FkID_P` (`ID_Producto`),
  KEY `FkID_V` (`ID_Venta`),
  CONSTRAINT `producto_venta_ibfk_1` FOREIGN KEY (`ID_Venta`) REFERENCES `venta` (`ID_Venta`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `producto_venta_ibfk_2` FOREIGN KEY (`ID_Producto`) REFERENCES `producto` (`ID_Producto`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_venta`
--

LOCK TABLES `producto_venta` WRITE;
/*!40000 ALTER TABLE `producto_venta` DISABLE KEYS */;
INSERT INTO `producto_venta` VALUES (1,1,1,3,40.75,10,30);
/*!40000 ALTER TABLE `producto_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `ID_Proveedor` int NOT NULL AUTO_INCREMENT,
  `Empresa` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `Monto_Comprado` float NOT NULL,
  `Cantidad_Comprada` int NOT NULL,
  `Hora` int NOT NULL,
  `ID_DC` int NOT NULL,
  `ID_MC` int NOT NULL,
  `ID_AC` int NOT NULL,
  `ID_RE1` int NOT NULL,
  `ID_RE2` int DEFAULT NULL,
  PRIMARY KEY (`ID_Proveedor`),
  KEY `FKID_REP2` (`ID_RE2`),
  KEY `FKID_REP1` (`ID_RE1`),
  KEY `FKID_AC` (`ID_AC`),
  KEY `FKID_MC` (`ID_MC`),
  KEY `FKID_DC` (`ID_DC`),
  CONSTRAINT `proveedor_ibfk_1` FOREIGN KEY (`ID_AC`) REFERENCES `anio_compra` (`ID_AC`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `proveedor_ibfk_2` FOREIGN KEY (`ID_DC`) REFERENCES `dia_compra` (`ID_DC`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `proveedor_ibfk_3` FOREIGN KEY (`ID_MC`) REFERENCES `mes_compra` (`ID_MC`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `proveedor_ibfk_4` FOREIGN KEY (`ID_RE1`) REFERENCES `reparto` (`ID_REP`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `proveedor_ibfk_5` FOREIGN KEY (`ID_RE2`) REFERENCES `reparto` (`ID_REP`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
INSERT INTO `proveedor` VALUES (1,'Welspun India',150,1,10,1,1,1,1,5),(2,'Acme Corporation',200,5,11,2,1,1,3,6),(3,'TechCom Solutions',100,3,12,3,1,1,2,7),(4,'Global Electronics',300,3,13,4,1,1,5,2),(5,'ABC Manufacturing',250,2,14,5,1,1,4,1),(6,'XYZ Textiles',120,2,15,6,1,1,1,1),(7,'InnovateTech',400,7,16,7,1,1,6,1),(8,'Sunrise Foods',180,4,17,8,1,1,3,2),(9,'Oceanic Imports',500,4,18,9,1,1,7,3),(10,'Skyline Enterprises',300,6,19,10,1,1,5,4);
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relacion_c_p_a_e`
--

DROP TABLE IF EXISTS `relacion_c_p_a_e`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `relacion_c_p_a_e` (
  `ID_CPAE` int NOT NULL AUTO_INCREMENT,
  `ID_Cliente` int NOT NULL,
  `ID_Producto` int NOT NULL,
  `ID_Apartado` int DEFAULT NULL,
  `ID_Envio` int DEFAULT NULL,
  PRIMARY KEY (`ID_CPAE`),
  KEY `FKID_Apartado` (`ID_Apartado`),
  KEY `FKID_Envio` (`ID_Envio`),
  KEY `FKID_Cliente` (`ID_Cliente`),
  KEY `FKID_Producto` (`ID_Producto`),
  CONSTRAINT `relacion_c_p_a_e_ibfk_1` FOREIGN KEY (`ID_Producto`) REFERENCES `producto` (`ID_Producto`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relacion_c_p_a_e_ibfk_2` FOREIGN KEY (`ID_Apartado`) REFERENCES `apartados` (`ID_Apartados`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relacion_c_p_a_e_ibfk_3` FOREIGN KEY (`ID_Envio`) REFERENCES `envios` (`ID_Envios`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `relacion_c_p_a_e_ibfk_4` FOREIGN KEY (`ID_Cliente`) REFERENCES `clientes` (`ID_Cliente`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relacion_c_p_a_e`
--

LOCK TABLES `relacion_c_p_a_e` WRITE;
/*!40000 ALTER TABLE `relacion_c_p_a_e` DISABLE KEYS */;
INSERT INTO `relacion_c_p_a_e` VALUES (1,1,1,1,NULL);
/*!40000 ALTER TABLE `relacion_c_p_a_e` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reparto`
--

DROP TABLE IF EXISTS `reparto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reparto` (
  `ID_REP` int NOT NULL AUTO_INCREMENT,
  `Dia_Reparto` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_REP`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reparto`
--

LOCK TABLES `reparto` WRITE;
/*!40000 ALTER TABLE `reparto` DISABLE KEYS */;
INSERT INTO `reparto` VALUES (1,'Lunes'),(2,'Martes'),(3,'Miercoles'),(4,'Jueves'),(5,'Viernes'),(6,'Sabado'),(7,'Domingo');
/*!40000 ALTER TABLE `reparto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status` (
  `ID_Status` int NOT NULL AUTO_INCREMENT,
  `Status` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_Status`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES (1,'Pendiente'),(2,'Pagado'),(3,'Cancelado');
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status_envio`
--

DROP TABLE IF EXISTS `status_envio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_envio` (
  `ID_StatusE` int NOT NULL AUTO_INCREMENT,
  `Status_Envio` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_StatusE`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_envio`
--

LOCK TABLES `status_envio` WRITE;
/*!40000 ALTER TABLE `status_envio` DISABLE KEYS */;
INSERT INTO `status_envio` VALUES (1,'Enviado'),(2,'Entregado'),(3,'Espera');
/*!40000 ALTER TABLE `status_envio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_apartado`
--

DROP TABLE IF EXISTS `t_apartado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `t_apartado` (
  `ID_AP` int NOT NULL AUTO_INCREMENT,
  `Tiene_Apartados` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID_AP`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_apartado`
--

LOCK TABLES `t_apartado` WRITE;
/*!40000 ALTER TABLE `t_apartado` DISABLE KEYS */;
INSERT INTO `t_apartado` VALUES (1,'Si'),(2,'No');
/*!40000 ALTER TABLE `t_apartado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `ID_Venta` int NOT NULL AUTO_INCREMENT,
  `Ingresos_Total` float NOT NULL,
  `Ganancia_Total` float NOT NULL,
  `Reinversion_Total` float NOT NULL,
  `Cantidad_Piezas_Vendidas` int NOT NULL,
  `Hora` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ID_DV` int NOT NULL,
  `ID_MV` int NOT NULL,
  `ID_AV` int NOT NULL,
  `ID_FP` int NOT NULL,
  PRIMARY KEY (`ID_Venta`),
  KEY `FKID_FP` (`ID_FP`),
  KEY `FKID_DV` (`ID_DV`),
  KEY `FKID_MV` (`ID_MV`),
  KEY `FKID_AV` (`ID_AV`),
  CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`ID_FP`) REFERENCES `forma_pago` (`ID_FP`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `venta_ibfk_2` FOREIGN KEY (`ID_MV`) REFERENCES `mes_venta` (`ID_MV`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `venta_ibfk_3` FOREIGN KEY (`ID_DV`) REFERENCES `dia_venta` (`ID_DV`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `venta_ibfk_4` FOREIGN KEY (`ID_AV`) REFERENCES `anio_venta` (`ID_AV`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
INSERT INTO `venta` VALUES (1,234,0,0,2,'10',2,10,1,2),(2,2233,0,0,1,'12',2,10,1,2),(3,323,0,0,23,'13',2,10,1,2),(4,2345,0,0,24,'2',2,10,1,2),(5,67,0,0,24,'1',2,10,1,2),(6,6766,0,0,21,'1',2,10,1,2),(7,765,0,0,12,'12',2,10,1,2),(8,56,0,0,22,'12',2,10,1,2),(9,87,0,0,32,'11',2,10,1,2),(10,89,0,0,24,'11',2,10,1,2);
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-08 21:16:46
