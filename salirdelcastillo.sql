-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         5.5.60 - MySQL Community Server (GPL)
-- SO del servidor:              Win64
-- HeidiSQL Versión:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para juego
CREATE DATABASE IF NOT EXISTS `juego` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_spanish_ci */;
USE `juego`;

-- Volcando estructura para tabla juego.frases
CREATE TABLE IF NOT EXISTS `frases` (
  `idfrase` int(11) NOT NULL AUTO_INCREMENT,
  `idsala` int(11) NOT NULL DEFAULT '0',
  `texto` varchar(500) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`idfrase`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.frases: ~20 rows (aproximadamente)
/*!40000 ALTER TABLE `frases` DISABLE KEYS */;
REPLACE INTO `frases` (`idfrase`, `idsala`, `texto`) VALUES
	(1, 1, 'mirar mesa'),
	(2, 1, 'mirar candelabro'),
	(3, 1, 'coger candelabro'),
	(4, 2, 'mirar cofre'),
	(5, 2, 'mirar cuadro'),
	(6, 2, 'mirar llave'),
	(7, 2, 'coger llave'),
	(8, 2, 'abrir cofre con llave'),
	(9, 2, 'usar llave con cofre'),
	(10, 3, 'mirar cuchillo'),
	(11, 3, 'coger cuchillo'),
	(12, 3, 'hablar con guerrero'),
	(13, 3, 'empujar guerrero con cuchillo'),
	(14, 3, 'usar cuchillo con guerrero'),
	(15, 4, 'hablar con tendero'),
	(16, 4, 'comprar palanca'),
	(17, 4, 'vender candelabro'),
	(18, 5, 'mirar puerta'),
	(19, 5, 'abrir puerta con palanca'),
	(20, 5, 'usar palanca con puerta');
/*!40000 ALTER TABLE `frases` ENABLE KEYS */;

-- Volcando estructura para tabla juego.objeto
CREATE TABLE IF NOT EXISTS `objeto` (
  `idobjeto` int(11) NOT NULL AUTO_INCREMENT,
  `idsala` int(11) NOT NULL DEFAULT '0',
  `nombre` varchar(50) COLLATE latin1_spanish_ci NOT NULL,
  `descripcion` varchar(500) COLLATE latin1_spanish_ci NOT NULL,
  PRIMARY KEY (`idobjeto`),
  KEY `idobjeto` (`idobjeto`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.objeto: ~10 rows (aproximadamente)
/*!40000 ALTER TABLE `objeto` DISABLE KEYS */;
REPLACE INTO `objeto` (`idobjeto`, `idsala`, `nombre`, `descripcion`) VALUES
	(1, 2, 'llave', 'Una vieja llave oxidada. Parece estar cubierte de una sustancia pegajosa.'),
	(2, 2, 'cofre', 'Un cofre ornamentado con motivos dorados. Podría contener algo valioso.'),
	(3, 1, 'candelabro', 'Un pesado candelabro adornado con motivos florales. Parece ser bastante valioso.'),
	(4, 3, 'cuchillo', 'Cuchillo de carnicero aún manchado de sangre. Tiene un olor repulsivo.'),
	(5, 4, 'monedas', 'Monedas de oro talladas. Tiene imágenes que recuerda a una época antigua.'),
	(6, 3, 'escudo', 'Escudo de madera de lo más rústico. Algo dentro de ti te dice que tiene poderes mágicos.'),
	(7, 1, 'mesa', 'Mesa de roble muy desgastada. Parece haber albergado ostentosos banquetes en el pasado.'),
	(8, 4, 'palanca', 'Palanca de madera. Parece poder usarse para abrir algún tipo de puerta.'),
	(9, 2, 'cuadro', 'Un cuadro con marcos dorados. En él se observa una especie de alacena repleta de cuerpos despedazados colgando del techo. El simple hecho de mirar el cuadro te produce náuseas.'),
	(10, 5, 'puerta', 'Inmenso portón de dos hojas. No tiene ningún tipo de pomo o ranura para llave. Tal vez se abra con algún mecanismo.');
/*!40000 ALTER TABLE `objeto` ENABLE KEYS */;

-- Volcando estructura para tabla juego.partida
CREATE TABLE IF NOT EXISTS `partida` (
  `idpartida` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  `sala` int(11) NOT NULL DEFAULT '0',
  `puntuacion` int(11) NOT NULL DEFAULT '0',
  `monedas` int(11) NOT NULL DEFAULT '0',
  `visibles` varchar(500) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  `usados` varchar(500) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  `visitadas` varchar(500) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  `inventario` varchar(500) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`idpartida`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.partida: ~2 rows (aproximadamente)
/*!40000 ALTER TABLE `partida` DISABLE KEYS */;
REPLACE INTO `partida` (`idpartida`, `nombre`, `sala`, `puntuacion`, `monedas`, `visibles`, `usados`, `visitadas`, `inventario`) VALUES
	(1, 'Javi', 2, 400, 0, 'mesa cofre cuadro puerta', 'cuchillo', '1 3 2', 'llave'),
	(2, 'Javi', 5, 675, 10, 'mesa cofre cuadro puerta', 'cuchillo llave palanca', '1 3 2 4 5', '');
/*!40000 ALTER TABLE `partida` ENABLE KEYS */;

-- Volcando estructura para tabla juego.personaje
CREATE TABLE IF NOT EXISTS `personaje` (
  `idpersonaje` int(11) NOT NULL,
  `idsala` int(11) DEFAULT NULL,
  `nombre` varchar(50) COLLATE latin1_spanish_ci NOT NULL,
  `frase1` varchar(500) COLLATE latin1_spanish_ci NOT NULL,
  `frase2` varchar(500) COLLATE latin1_spanish_ci NOT NULL,
  PRIMARY KEY (`idpersonaje`),
  KEY `idpersonaje` (`idpersonaje`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.personaje: ~2 rows (aproximadamente)
/*!40000 ALTER TABLE `personaje` DISABLE KEYS */;
REPLACE INTO `personaje` (`idpersonaje`, `idsala`, `nombre`, `frase1`, `frase2`) VALUES
	(1, 3, 'guerrero', 'Guerrero: ¿Qué haces aquí, gusano? Este no es lugar para debiluchos como tú... ¡Fuera de mi vista!', 'Guerrero: ¡Vale, vale, tú ganas! Puedes llevarte lo que quieras pero perdóname la vida por favor...'),
	(2, 4, 'tendero', 'Tendero: ¡Oh, un cliente! ¡Pasa por favor! Ahora mismo solo te puedo ofrecer esta palanca por 90 monedas de oro...', 'Tendero: No me queda nada más que ofrecerte a menos que quieras venderme algo...');
/*!40000 ALTER TABLE `personaje` ENABLE KEYS */;

-- Volcando estructura para tabla juego.pista
CREATE TABLE IF NOT EXISTS `pista` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `texto` varchar(500) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.pista: ~5 rows (aproximadamente)
/*!40000 ALTER TABLE `pista` DISABLE KEYS */;
REPLACE INTO `pista` (`id`, `texto`) VALUES
	(1, 'Debería buscar en todo el castillo la forma de salir de aquí...'),
	(2, 'Tal vez el guerrero tenga algo útil que ofrecerme...'),
	(3, 'La palanca del tendero podría resultarme útil...'),
	(4, 'Debería buscar como conseguir algo de oro. Quizás en el salón...'),
	(5, '¡Tengo que intentar salir por las puertas del fondo!');
/*!40000 ALTER TABLE `pista` ENABLE KEYS */;

-- Volcando estructura para tabla juego.puntuaciones
CREATE TABLE IF NOT EXISTS `puntuaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE latin1_spanish_ci NOT NULL,
  `puntuacion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.puntuaciones: ~9 rows (aproximadamente)
/*!40000 ALTER TABLE `puntuaciones` DISABLE KEYS */;
REPLACE INTO `puntuaciones` (`id`, `nombre`, `puntuacion`) VALUES
	(1, 'Javi', 675);
/*!40000 ALTER TABLE `puntuaciones` ENABLE KEYS */;

-- Volcando estructura para tabla juego.record
CREATE TABLE IF NOT EXISTS `record` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) COLLATE latin1_spanish_ci NOT NULL,
  `puntuacion` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.record: ~1 rows (aproximadamente)
/*!40000 ALTER TABLE `record` DISABLE KEYS */;
REPLACE INTO `record` (`id`, `nombre`, `puntuacion`) VALUES
	(1, 'Javi', 675);
/*!40000 ALTER TABLE `record` ENABLE KEYS */;

-- Volcando estructura para tabla juego.sala
CREATE TABLE IF NOT EXISTS `sala` (
  `idsala` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(1000) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  PRIMARY KEY (`idsala`),
  KEY `id` (`idsala`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.sala: ~5 rows (aproximadamente)
/*!40000 ALTER TABLE `sala` DISABLE KEYS */;
REPLACE INTO `sala` (`idsala`, `descripcion`) VALUES
	(1, 'Te encuentras en una enorme sala llena de columnas , no hay apenas luz. El olor es desagradable, algo anda cerca.'),
	(2, 'Has entrado en el salón de esta enorme fortaleza. Es amplio y muy luminoso. A lo lejos se aprecian unas puertas.'),
	(3, 'Estás en una mazmorra llena de esqueletos de antiguos inquilinos. El suelo es tierra y parece estar mojado.'),
	(4, 'Bienvenido a la tienda de esta fortaleza. El tendero estará encantado de hacer tratos contigo.'),
	(5, 'Has llegado a una gran escalinata. Quizás sea el fin de todo o el comiezo de algo nuevo. Se ve una puerta al final, pero parece cerrada.');
/*!40000 ALTER TABLE `sala` ENABLE KEYS */;

-- Volcando estructura para tabla juego.salida
CREATE TABLE IF NOT EXISTS `salida` (
  `idsalida` int(11) NOT NULL AUTO_INCREMENT,
  `idsala` int(11) NOT NULL DEFAULT '0',
  `salida` varchar(10) COLLATE latin1_spanish_ci NOT NULL DEFAULT '0',
  `idsalasalida` int(11) DEFAULT NULL,
  PRIMARY KEY (`idsalida`),
  KEY `idsalida` (`idsalida`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

-- Volcando datos para la tabla juego.salida: ~9 rows (aproximadamente)
/*!40000 ALTER TABLE `salida` DISABLE KEYS */;
REPLACE INTO `salida` (`idsalida`, `idsala`, `salida`, `idsalasalida`) VALUES
	(1, 1, 'sur', 3),
	(2, 1, 'este', 2),
	(3, 2, 'este', 5),
	(4, 2, 'oeste', 1),
	(5, 2, 'sur', 4),
	(6, 3, 'norte', 1),
	(7, 4, 'norte', 2),
	(8, 5, 'este', 0),
	(9, 5, 'oeste', 2);
/*!40000 ALTER TABLE `salida` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
