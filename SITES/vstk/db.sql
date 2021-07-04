-- MySQL dump 10.13  Distrib 5.7.31, for osx10.12 (x86_64)
--
-- Host: localhost    Database: vstk
-- ------------------------------------------------------
-- Server version	5.7.31-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'АР, ПЗУ, ОДИ'),(4,'ВК'),(6,'ГИП'),(2,'КР, КЖ'),(3,'ОВ'),(5,'ЭМ');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,6,5),(2,6,6),(3,6,7),(4,6,8),(5,6,9),(6,6,10),(7,6,11),(8,6,12),(9,6,21),(10,6,22),(11,6,23),(12,6,24),(13,6,25),(14,6,26),(15,6,27),(16,6,28),(17,6,33),(18,6,34),(19,6,35),(20,6,36),(21,6,37),(22,6,38),(23,6,39),(24,6,40),(25,6,41),(26,6,42),(27,6,43),(28,6,44),(29,6,45),(30,6,46),(31,6,47),(32,6,48),(33,6,49),(34,6,50),(35,6,51),(36,6,52),(37,6,53),(38,6,54),(39,6,55),(40,6,56),(41,6,57),(42,6,58),(43,6,59),(44,6,60),(45,6,61),(46,6,62),(47,6,63),(48,6,64),(49,6,65),(50,6,66),(51,6,67),(52,6,68),(53,6,69),(54,6,70),(55,6,71),(56,6,72),(57,6,73),(58,6,74),(59,6,75),(60,6,76),(61,6,77),(62,6,78),(63,6,79),(64,6,80),(65,6,81);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add user',3,'add_user'),(10,'Can change user',3,'change_user'),(11,'Can delete user',3,'delete_user'),(12,'Can view user',3,'view_user'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Админка - Настройка',6,'add_config'),(22,'Can change Админка - Настройка',6,'change_config'),(23,'Can delete Админка - Настройка',6,'delete_config'),(24,'Can view Админка - Настройка',6,'view_config'),(25,'Can add Админка - Задача',7,'add_tasks'),(26,'Can change Админка - Задача',7,'change_tasks'),(27,'Can delete Админка - Задача',7,'delete_tasks'),(28,'Can view Админка - Задача',7,'view_tasks'),(29,'Can add custom user',11,'add_customuser'),(30,'Can change custom user',11,'change_customuser'),(31,'Can delete custom user',11,'delete_customuser'),(32,'Can view custom user',11,'view_customuser'),(33,'Can add Стат.контет - Файл',12,'add_files'),(34,'Can change Стат.контет - Файл',12,'change_files'),(35,'Can delete Стат.контет - Файл',12,'delete_files'),(36,'Can view Стат.контет - Файл',12,'view_files'),(37,'Can add Стат.контент - Блоки',13,'add_blocks'),(38,'Can change Стат.контент - Блоки',13,'change_blocks'),(39,'Can delete Стат.контент - Блоки',13,'delete_blocks'),(40,'Can view Стат.контент - Блоки',13,'view_blocks'),(41,'Заполнение сео-полей меню',13,'seo_fields'),(42,'Can add Стат.контент - Контейнеры',14,'add_containers'),(43,'Can change Стат.контент - Контейнеры',14,'change_containers'),(44,'Can delete Стат.контент - Контейнеры',14,'delete_containers'),(45,'Can view Стат.контент - Контейнеры',14,'view_containers'),(46,'Can add Стат.контент - Линковка меню к контейнерам',15,'add_linkcontainer'),(47,'Can change Стат.контент - Линковка меню к контейнерам',15,'change_linkcontainer'),(48,'Can delete Стат.контент - Линковка меню к контейнерам',15,'delete_linkcontainer'),(49,'Can view Стат.контент - Линковка меню к контейнерам',15,'view_linkcontainer'),(50,'Can add Объекты - объект',16,'add_structobject'),(51,'Can change Объекты - объект',16,'change_structobject'),(52,'Can delete Объекты - объект',16,'delete_structobject'),(53,'Can view Объекты - объект',16,'view_structobject'),(54,'Can add Объекты - тех. задание',17,'add_techtask'),(55,'Can change Объекты - тех. задание',17,'change_techtask'),(56,'Can delete Объекты - тех. задание',17,'delete_techtask'),(57,'Can view Объекты - тех. задание',17,'view_techtask'),(58,'Can add Объекты - исходные данные',18,'add_sourcedata'),(59,'Can change Объекты - исходные данные',18,'change_sourcedata'),(60,'Can delete Объекты - исходные данные',18,'delete_sourcedata'),(61,'Can view Объекты - исходные данные',18,'view_sourcedata'),(62,'Can add Объекты - пред. планировочное решение',19,'add_preplandesicions'),(63,'Can change Объекты - пред. планировочное решение',19,'change_preplandesicions'),(64,'Can delete Объекты - пред. планировочное решение',19,'delete_preplandesicions'),(65,'Can view Объекты - пред. планировочное решение',19,'view_preplandesicions'),(66,'Can add Объекты - планировочное решение',20,'add_plandesicions'),(67,'Can change Объекты - планировочное решение',20,'change_plandesicions'),(68,'Can delete Объекты - планировочное решение',20,'delete_plandesicions'),(69,'Can view Объекты - планировочное решение',20,'view_plandesicions'),(70,'Can add Объекты - задание на отверстие',21,'add_holetasks'),(71,'Can change Объекты - задание на отверстие',21,'change_holetasks'),(72,'Can delete Объекты - задание на отверстие',21,'delete_holetasks'),(73,'Can view Объекты - задание на отверстие',21,'view_holetasks'),(74,'Can add Объекты - описательная часть',22,'add_descriptions'),(75,'Can change Объекты - описательная часть',22,'change_descriptions'),(76,'Can delete Объекты - описательная часть',22,'delete_descriptions'),(77,'Can view Объекты - описательная часть',22,'view_descriptions'),(78,'Can add Объекты - задание на изменение',23,'add_changetasks'),(79,'Can change Объекты - задание на изменение',23,'change_changetasks'),(80,'Can delete Объекты - задание на изменение',23,'delete_changetasks'),(81,'Can view Объекты - задание на изменение',23,'view_changetasks');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$Vj0WXe3DoI5a$EwhQMWDAChlqmVEDUX1hyBFiW05/nGo221duNff5Z18=','2021-07-01 09:42:54.491005',1,'jocker','','','dkramorov@mail.ru',1,1,'2021-06-21 17:30:19.984965'),(2,'pbkdf2_sha256$150000$4qSYXnnWxDEd$2wR4FciIjgCYig8uPnZEq3+xO1IjG4syqFs5gYS9VBw=',NULL,0,'mullayarov','С.В.','Муллаяров','',1,1,'2021-06-21 17:43:16.000716'),(3,'pbkdf2_sha256$150000$jjyrb5RXcuYZ$E/c4ovSG5el42znBgBakIU9POcjhHieX7BlI/gaDqY0=',NULL,0,'otrubenko','С.Д.','Отрубенко','',1,1,'2021-06-21 17:43:48.428917'),(4,'pbkdf2_sha256$150000$3bPZ6Jb2Pg9l$vvgcfkcJMNzpjCK+ixpe8WypJ7XtHT5zVDGPwAMnUx4=',NULL,0,'barhatova','','Бархатова','',1,1,'2021-06-21 17:44:19.097637'),(5,'pbkdf2_sha256$150000$s05u3RoTRRyV$5gacY6wI480TKxCLjdrP+/DaYXOUbxyUcvm9vTq+Znw=',NULL,0,'grudinina','С.А.','Грудинина','',1,1,'2021-06-21 17:44:42.188165'),(6,'pbkdf2_sha256$150000$Wnu8jU1dJ3Jn$Xx8p73NfzIpCCEHs+dEbBGaw1WPIOgJqBUXQQXS9mqE=',NULL,0,'esikov','И.А','Есиков','',1,1,'2021-06-21 17:45:09.371072'),(7,'pbkdf2_sha256$150000$bO0qFc0yjMTj$Iw72/kjD8tuNZYQYkTBvzvo5JW1ZKbqU6y/NU6wppdw=',NULL,0,'kostyanik','С.Н.','Костяник','',1,1,'2021-06-21 17:45:39.246237'),(8,'pbkdf2_sha256$150000$dL55WoE809Y0$IxnuxIrDI3A/Ny5FU3ET197bQ4KaxEpHM1cWA65DHWE=',NULL,0,'rodionova','М.Г.','Родионова','',0,1,'2021-06-21 17:46:03.791438'),(9,'pbkdf2_sha256$150000$sGHKAts40Jkf$fE/HRLZg0631+ROoI0VthWevZWpSVyTrtt6bC27KK6w=',NULL,0,'vetul','А.А.','Ветюл','',1,1,'2021-06-21 17:46:29.051847'),(10,'pbkdf2_sha256$150000$UL7NKOxn7kXu$Ale5q2oYhSZx/GP5Qj8kcBEsLEM5sdvMW76u4yaostc=',NULL,0,'muratova','А.','Муратова','',0,1,'2021-06-21 17:46:55.590562'),(11,'pbkdf2_sha256$150000$vMGHmW1Ljntr$VCqDz5gtS7Z1TK98uHU1dvHAOY1ioq0VZ9/3Xv90RgY=',NULL,0,'kozlov','В.В','Козлов','',1,1,'2021-06-21 17:47:51.299337'),(12,'pbkdf2_sha256$150000$6OQgxdysqV0I$g01x5Fo8NHICN26SLW/8vwMUENZ3f4GVkY5Vl7/LiOw=',NULL,0,'anykeev','С.И.','Аникеев','',1,1,'2021-06-21 17:48:16.149685'),(13,'pbkdf2_sha256$150000$trT5Z2Xfosx1$BKghtywZwWVYh2yz8KHVoFMKFgDHXroNHd/OZ+vkqp4=',NULL,0,'richkov','А.С.','Рычков','',1,1,'2021-06-21 17:48:46.404480'),(14,'pbkdf2_sha256$150000$PKhzxY2YyMPn$YDHV882V0os+9oosD49ZPsjQXGRHI3QwrIJ5qBwCtSs=','2021-07-01 09:42:59.904401',0,'gip','','','',1,1,'2021-06-22 11:47:45.642443');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,2,1),(2,3,1),(3,4,1),(4,5,1),(11,6,2),(12,7,2),(10,8,2),(15,9,3),(16,10,3),(13,11,4),(14,12,4),(17,13,5),(18,14,6);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (66,14,5),(67,14,6),(68,14,7),(69,14,8),(70,14,9),(71,14,10),(72,14,11),(73,14,12),(74,14,21),(75,14,22),(76,14,23),(77,14,24),(78,14,25),(79,14,26),(80,14,27),(81,14,28),(82,14,33),(83,14,34),(84,14,35),(85,14,36),(86,14,37),(87,14,38),(88,14,39),(89,14,40),(90,14,41),(91,14,42),(92,14,43),(93,14,44),(94,14,45),(95,14,46),(96,14,47),(97,14,48),(98,14,49),(99,14,50),(100,14,51),(101,14,52),(102,14,53),(103,14,54),(104,14,55),(105,14,56),(106,14,57),(107,14,58),(108,14,59),(109,14,60),(110,14,61),(111,14,62),(112,14,63),(113,14,64),(114,14,65),(115,14,66),(116,14,67),(117,14,68),(118,14,69),(119,14,70),(120,14,71),(121,14,72),(122,14,73),(123,14,74),(124,14,75),(125,14,76),(126,14,77),(127,14,78),(128,14,79),(129,14,80),(130,14,81);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(12,'files','files'),(13,'flatcontent','blocks'),(14,'flatcontent','containers'),(15,'flatcontent','linkcontainer'),(11,'login','customuser'),(8,'login','extrafields'),(10,'login','extrainfo'),(9,'login','extravalues'),(6,'main_functions','config'),(7,'main_functions','tasks'),(5,'sessions','session'),(23,'struct','changetasks'),(22,'struct','descriptions'),(21,'struct','holetasks'),(20,'struct','plandesicions'),(19,'struct','preplandesicions'),(18,'struct','sourcedata'),(16,'struct','structobject'),(17,'struct','techtask');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-06-21 17:30:18.332185'),(2,'contenttypes','0002_remove_content_type_name','2021-06-21 17:30:18.396362'),(3,'auth','0001_initial','2021-06-21 17:30:18.630939'),(4,'auth','0002_alter_permission_name_max_length','2021-06-21 17:30:18.766151'),(5,'auth','0003_alter_user_email_max_length','2021-06-21 17:30:18.786239'),(6,'auth','0004_alter_user_username_opts','2021-06-21 17:30:18.793668'),(7,'auth','0005_alter_user_last_login_null','2021-06-21 17:30:18.809891'),(8,'auth','0006_require_contenttypes_0002','2021-06-21 17:30:18.811628'),(9,'auth','0007_alter_validators_add_error_messages','2021-06-21 17:30:18.818477'),(10,'auth','0008_alter_user_username_max_length','2021-06-21 17:30:18.838631'),(11,'auth','0009_alter_user_last_name_max_length','2021-06-21 17:30:18.858912'),(12,'auth','0010_alter_group_name_max_length','2021-06-21 17:30:18.880137'),(13,'auth','0011_update_proxy_permissions','2021-06-21 17:30:18.887257'),(14,'files','0001_initial','2021-06-21 17:30:18.911931'),(15,'files','0002_auto_20191203_2054','2021-06-21 17:30:18.967459'),(16,'files','0003_auto_20200112_1717','2021-06-21 17:30:18.975793'),(17,'files','0004_auto_20200402_2127','2021-06-21 17:30:18.994612'),(18,'files','0005_auto_20200809_1025','2021-06-21 17:30:18.999301'),(19,'files','0006_auto_20210516_1530','2021-06-21 17:30:19.026693'),(20,'flatcontent','0001_initial','2021-06-21 17:30:19.194246'),(21,'flatcontent','0002_auto_20190825_1730','2021-06-21 17:30:19.515587'),(22,'flatcontent','0003_auto_20191203_2054','2021-06-21 17:30:19.552926'),(23,'flatcontent','0004_blocks_html','2021-06-21 17:30:19.576550'),(24,'flatcontent','0005_auto_20200112_1717','2021-06-21 17:30:19.607923'),(25,'flatcontent','0006_auto_20200314_1638','2021-06-21 17:30:19.613217'),(26,'flatcontent','0007_auto_20200402_2127','2021-06-21 17:30:19.701975'),(27,'flatcontent','0008_containers_class_name','2021-06-21 17:30:19.722498'),(28,'flatcontent','0009_blocks_class_name','2021-06-21 17:30:19.751979'),(29,'flatcontent','0010_auto_20210430_1708','2021-06-21 17:30:19.765620'),(30,'flatcontent','0011_auto_20210526_2033','2021-06-21 17:30:19.773413'),(31,'login','0001_initial','2021-06-21 17:30:20.191345'),(32,'login','0002_auto_20200925_1007','2021-06-21 17:30:20.499771'),(33,'main_functions','0001_initial','2021-06-21 17:30:20.575261'),(34,'main_functions','0002_auto_20191203_2052','2021-06-21 17:30:20.595798'),(35,'main_functions','0003_auto_20200407_1845','2021-06-21 17:30:20.822052'),(36,'main_functions','0004_config_user','2021-06-21 17:30:20.930377'),(37,'main_functions','0005_auto_20210321_1210','2021-06-21 17:30:20.955509'),(38,'sessions','0001_initial','2021-06-21 17:30:20.989163'),(39,'struct','0001_initial','2021-06-21 18:01:21.369862'),(40,'struct','0002_auto_20210622_1146','2021-06-22 11:46:45.141333');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('iherjvwlgazip6fz94zx8h2sks55glir','ODYzYWZhZTBjNWVlMDAzZTAzM2YzYzQzNjU2Mzc2ZmRhNzg2M2E0Zjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjliYmI4ZGRkMDllYzExNDVkNWFkYWYyNTZlMjBhNjE2MmY5MzhlMGYifQ==','2021-07-05 17:34:37.841273'),('v2wl6n8dkg3h6za95i0kcbsltt4v81tf','ZmViMDA5NTI2MzljMDEyNWQyNmViM2UzOTNhZmFlNWEwOGNhN2IxMDp7Il9hdXRoX3VzZXJfaWQiOiIxNCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFwcHMubG9naW4uYmFja2VuZC5NeUJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjMmQyZDM1ZGEyMzAzMDRjNmMyMmQzNzlhYjY4YzM3M2E4MTU2ZGYxIn0=','2021-07-15 09:42:59.908287');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `files_files`
--

DROP TABLE IF EXISTS `files_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `files_files` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `desc` longtext,
  `mime` varchar(255) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `domain` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `files_files_created_18bb5ba5` (`created`),
  KEY `files_files_updated_98d0072e` (`updated`),
  KEY `files_files_position_9aa9a563` (`position`),
  KEY `files_files_is_active_368d94f0` (`is_active`),
  KEY `files_files_state_80db30e9` (`state`),
  KEY `files_files_parents_61383b35` (`parents`),
  KEY `files_files_name_2ed1b48d` (`name`),
  KEY `files_files_link_1e36fbb3` (`link`),
  KEY `files_files_mime_4444de1c` (`mime`),
  KEY `files_files_path_1ee40119` (`path`),
  KEY `files_files_img_fbfb9b0a` (`img`),
  KEY `files_files_domain_8c5d51c1` (`domain`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files_files`
--

LOCK TABLES `files_files` WRITE;
/*!40000 ALTER TABLE `files_files` DISABLE KEYS */;
/*!40000 ALTER TABLE `files_files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flatcontent_blocks`
--

DROP TABLE IF EXISTS `flatcontent_blocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flatcontent_blocks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `tag` varchar(255) DEFAULT NULL,
  `container_id` int(11) DEFAULT NULL,
  `blank` tinyint(1) NOT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `keywords` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `html` longtext,
  `class_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `flatcontent_blocks_created_ac8f728c` (`created`),
  KEY `flatcontent_blocks_updated_3b94570e` (`updated`),
  KEY `flatcontent_blocks_position_9d66f892` (`position`),
  KEY `flatcontent_blocks_is_active_013025f3` (`is_active`),
  KEY `flatcontent_blocks_state_370815a5` (`state`),
  KEY `flatcontent_blocks_parents_447361a3` (`parents`),
  KEY `flatcontent_blocks_name_f035fc87` (`name`),
  KEY `flatcontent_blocks_link_c5940f59` (`link`),
  KEY `flatcontent_blocks_tag_2d7989b3` (`tag`),
  KEY `flatcontent_blocks_container_id_5864baa1_fk_flatconte` (`container_id`),
  KEY `flatcontent_blocks_description_52726bac` (`description`),
  KEY `flatcontent_blocks_blank_b607b7e8` (`blank`),
  KEY `flatcontent_blocks_icon_22fe22b4` (`icon`),
  KEY `flatcontent_blocks_keywords_0363c2ad` (`keywords`),
  KEY `flatcontent_blocks_title_5b09011e` (`title`),
  KEY `flatcontent_blocks_img_876dc659` (`img`),
  KEY `flatcontent_blocks_class_name_b28da06f` (`class_name`),
  CONSTRAINT `flatcontent_blocks_container_id_5864baa1_fk_flatconte` FOREIGN KEY (`container_id`) REFERENCES `flatcontent_containers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
/*!40000 ALTER TABLE `flatcontent_blocks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flatcontent_containers`
--

DROP TABLE IF EXISTS `flatcontent_containers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flatcontent_containers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` longtext,
  `tag` varchar(255) DEFAULT NULL,
  `template_position` varchar(255) DEFAULT NULL,
  `class_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `flatcontent_containers_created_af28c039` (`created`),
  KEY `flatcontent_containers_updated_134be2c3` (`updated`),
  KEY `flatcontent_containers_position_a4f08a12` (`position`),
  KEY `flatcontent_containers_is_active_d4dd19c8` (`is_active`),
  KEY `flatcontent_containers_state_58277f20` (`state`),
  KEY `flatcontent_containers_parents_9809c178` (`parents`),
  KEY `flatcontent_containers_name_555024ab` (`name`),
  KEY `flatcontent_containers_tag_5f2487d0` (`tag`),
  KEY `flatcontent_containers_template_position_2e66b690` (`template_position`),
  KEY `flatcontent_containers_img_59d06f2c` (`img`),
  KEY `flatcontent_containers_class_name_dc7e7319` (`class_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
/*!40000 ALTER TABLE `flatcontent_containers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flatcontent_linkcontainer`
--

DROP TABLE IF EXISTS `flatcontent_linkcontainer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flatcontent_linkcontainer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `block_id` int(11) NOT NULL,
  `container_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `flatcontent_linkcont_block_id_95a742ab_fk_flatconte` (`block_id`),
  KEY `flatcontent_linkcont_container_id_9d707d07_fk_flatconte` (`container_id`),
  KEY `flatcontent_linkcontainer_created_817be879` (`created`),
  KEY `flatcontent_linkcontainer_updated_f577aa94` (`updated`),
  KEY `flatcontent_linkcontainer_position_fabe1bde` (`position`),
  KEY `flatcontent_linkcontainer_is_active_d61b1bb9` (`is_active`),
  KEY `flatcontent_linkcontainer_state_cb4a990a` (`state`),
  KEY `flatcontent_linkcontainer_parents_36b28f6e` (`parents`),
  KEY `flatcontent_linkcontainer_img_2d8c4e0a` (`img`),
  CONSTRAINT `flatcontent_linkcont_block_id_95a742ab_fk_flatconte` FOREIGN KEY (`block_id`) REFERENCES `flatcontent_blocks` (`id`),
  CONSTRAINT `flatcontent_linkcont_container_id_9d707d07_fk_flatconte` FOREIGN KEY (`container_id`) REFERENCES `flatcontent_containers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_linkcontainer`
--

LOCK TABLES `flatcontent_linkcontainer` WRITE;
/*!40000 ALTER TABLE `flatcontent_linkcontainer` DISABLE KEYS */;
/*!40000 ALTER TABLE `flatcontent_linkcontainer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_customuser`
--

DROP TABLE IF EXISTS `login_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_customuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `function` varchar(255) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `login_customuser_img_6a17a9f3` (`img`),
  KEY `login_customuser_created_4a29e213` (`created`),
  KEY `login_customuser_updated_dc9f9081` (`updated`),
  KEY `login_customuser_position_33445dcc` (`position`),
  KEY `login_customuser_is_active_cccf2704` (`is_active`),
  KEY `login_customuser_state_f0a75add` (`state`),
  KEY `login_customuser_parents_3604d87b` (`parents`),
  KEY `login_customuser_phone_d456dd09` (`phone`),
  KEY `login_customuser_function_2ad64bbc` (`function`),
  CONSTRAINT `login_customuser_user_id_70d7d409_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_customuser`
--

LOCK TABLES `login_customuser` WRITE;
/*!40000 ALTER TABLE `login_customuser` DISABLE KEYS */;
INSERT INTO `login_customuser` VALUES (1,NULL,'2021-06-21 17:30:20.083600','2021-07-01 09:42:54.495248',1,1,NULL,NULL,NULL,NULL,1),(2,NULL,'2021-06-21 17:43:16.048898','2021-06-21 17:43:16.207614',2,1,NULL,NULL,'','',2),(3,NULL,'2021-06-21 17:43:48.431653','2021-06-21 17:43:48.543405',3,1,NULL,NULL,'','',3),(4,NULL,'2021-06-21 17:44:06.692177','2021-06-21 17:44:19.249024',4,1,NULL,NULL,'','',4),(5,NULL,'2021-06-21 17:44:42.191753','2021-06-21 17:44:42.297432',5,1,NULL,NULL,'','',5),(6,NULL,'2021-06-21 17:45:09.373923','2021-06-21 17:45:09.494644',6,1,NULL,NULL,'','',6),(7,NULL,'2021-06-21 17:45:39.248192','2021-06-21 17:45:39.391589',7,1,NULL,NULL,'','',7),(8,NULL,'2021-06-21 17:46:03.795096','2021-06-21 17:46:03.942434',8,1,NULL,NULL,'','',8),(9,NULL,'2021-06-21 17:46:29.053650','2021-06-21 17:46:29.206092',9,1,NULL,NULL,'','',9),(10,NULL,'2021-06-21 17:46:55.592797','2021-06-21 17:46:55.697708',10,1,NULL,NULL,'','',10),(11,NULL,'2021-06-21 17:47:17.102167','2021-06-21 17:47:51.409871',11,1,NULL,NULL,'','',11),(12,NULL,'2021-06-21 17:48:16.152707','2021-06-21 17:48:16.264255',12,1,NULL,NULL,'','',12),(13,NULL,'2021-06-21 17:48:46.406769','2021-06-21 17:48:46.512389',13,1,NULL,NULL,'','',13),(14,NULL,'2021-06-22 11:47:45.663136','2021-07-01 09:42:59.906761',14,1,NULL,NULL,'','Главный инженер проекта',14);
/*!40000 ALTER TABLE `login_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_extrafields`
--

DROP TABLE IF EXISTS `login_extrafields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_extrafields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `field` varchar(255) DEFAULT NULL,
  `show_in_table` tinyint(1) NOT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `login_extrafields_group_id_e7950649_fk_auth_group_id` (`group_id`),
  KEY `login_extrafields_img_6007a1e5` (`img`),
  KEY `login_extrafields_created_724dd98a` (`created`),
  KEY `login_extrafields_updated_730fb204` (`updated`),
  KEY `login_extrafields_position_213dfecb` (`position`),
  KEY `login_extrafields_is_active_829ea67a` (`is_active`),
  KEY `login_extrafields_state_66b5864d` (`state`),
  KEY `login_extrafields_parents_441198ed` (`parents`),
  KEY `login_extrafields_name_d654ec12` (`name`),
  KEY `login_extrafields_field_05c895b8` (`field`),
  KEY `login_extrafields_show_in_table_4a6daeb7` (`show_in_table`),
  CONSTRAINT `login_extrafields_group_id_e7950649_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_extrafields`
--

LOCK TABLES `login_extrafields` WRITE;
/*!40000 ALTER TABLE `login_extrafields` DISABLE KEYS */;
/*!40000 ALTER TABLE `login_extrafields` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_extrainfo`
--

DROP TABLE IF EXISTS `login_extrainfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_extrainfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) DEFAULT NULL,
  `field_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `login_extrainfo_field_id_a5fdd905_fk_login_extrafields_id` (`field_id`),
  KEY `login_extrainfo_user_id_c9445a9d_fk_auth_user_id` (`user_id`),
  KEY `login_extrainfo_value_367be965` (`value`),
  CONSTRAINT `login_extrainfo_field_id_a5fdd905_fk_login_extrafields_id` FOREIGN KEY (`field_id`) REFERENCES `login_extrafields` (`id`),
  CONSTRAINT `login_extrainfo_user_id_c9445a9d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_extrainfo`
--

LOCK TABLES `login_extrainfo` WRITE;
/*!40000 ALTER TABLE `login_extrainfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `login_extrainfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_extravalues`
--

DROP TABLE IF EXISTS `login_extravalues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_extravalues` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `field_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `login_extravalues_field_id_6aeff450_fk_login_extrafields_id` (`field_id`),
  KEY `login_extravalues_img_02f21812` (`img`),
  KEY `login_extravalues_created_edaed3b0` (`created`),
  KEY `login_extravalues_updated_320cc6a9` (`updated`),
  KEY `login_extravalues_position_0c7c6e7a` (`position`),
  KEY `login_extravalues_is_active_ae75e02d` (`is_active`),
  KEY `login_extravalues_state_a241360f` (`state`),
  KEY `login_extravalues_parents_aeb6b2c4` (`parents`),
  KEY `login_extravalues_value_c6dc278d` (`value`),
  CONSTRAINT `login_extravalues_field_id_6aeff450_fk_login_extrafields_id` FOREIGN KEY (`field_id`) REFERENCES `login_extrafields` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_extravalues`
--

LOCK TABLES `login_extravalues` WRITE;
/*!40000 ALTER TABLE `login_extravalues` DISABLE KEYS */;
/*!40000 ALTER TABLE `login_extravalues` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_functions_config`
--

DROP TABLE IF EXISTS `main_functions_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_functions_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `attr` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `img` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `position` int(11) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `updated` datetime(6) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_functions_config_name_923c9fba` (`name`),
  KEY `main_functions_config_attr_99aeb037` (`attr`),
  KEY `main_functions_config_value_463dd357` (`value`),
  KEY `main_functions_config_created_e08da0ad` (`created`),
  KEY `main_functions_config_img_1e25f97d` (`img`),
  KEY `main_functions_config_is_active_74557b50` (`is_active`),
  KEY `main_functions_config_parents_e7f90ba8` (`parents`),
  KEY `main_functions_config_position_cd5d988c` (`position`),
  KEY `main_functions_config_state_bce5179d` (`state`),
  KEY `main_functions_config_updated_b30da946` (`updated`),
  KEY `main_functions_config_user_id_c5dbfa40_fk_auth_user_id` (`user_id`),
  CONSTRAINT `main_functions_config_user_id_c5dbfa40_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_functions_config`
--

LOCK TABLES `main_functions_config` WRITE;
/*!40000 ALTER TABLE `main_functions_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_functions_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_functions_tasks`
--

DROP TABLE IF EXISTS `main_functions_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_functions_tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `command` longtext NOT NULL,
  `created` datetime(6) NOT NULL,
  `img` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `position` int(11) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_functions_tasks_created_e5645878` (`created`),
  KEY `main_functions_tasks_img_50fb49d4` (`img`),
  KEY `main_functions_tasks_is_active_59683d1a` (`is_active`),
  KEY `main_functions_tasks_name_778afd08` (`name`),
  KEY `main_functions_tasks_parents_4b60e8c2` (`parents`),
  KEY `main_functions_tasks_position_57fd722a` (`position`),
  KEY `main_functions_tasks_state_223f6135` (`state`),
  KEY `main_functions_tasks_updated_b0382311` (`updated`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_functions_tasks`
--

LOCK TABLES `main_functions_tasks` WRITE;
/*!40000 ALTER TABLE `main_functions_tasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_functions_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `struct_changetasks`
--

DROP TABLE IF EXISTS `struct_changetasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `struct_changetasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `doc_id` int(11) DEFAULT NULL,
  `obj_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `struct_changetasks_doc_id_9925f8d6_fk_files_files_id` (`doc_id`),
  KEY `struct_changetasks_obj_id_91e1f861_fk_struct_structobject_id` (`obj_id`),
  KEY `struct_changetasks_img_14b3e40b` (`img`),
  KEY `struct_changetasks_created_4883139c` (`created`),
  KEY `struct_changetasks_updated_2f6aaed2` (`updated`),
  KEY `struct_changetasks_position_e7590da3` (`position`),
  KEY `struct_changetasks_is_active_1f0d1da3` (`is_active`),
  KEY `struct_changetasks_state_29b10d3a` (`state`),
  KEY `struct_changetasks_parents_8e810def` (`parents`),
  KEY `struct_changetasks_name_86e6d005` (`name`),
  KEY `struct_changetasks_description_332bccc7` (`description`),
  CONSTRAINT `struct_changetasks_doc_id_9925f8d6_fk_files_files_id` FOREIGN KEY (`doc_id`) REFERENCES `files_files` (`id`),
  CONSTRAINT `struct_changetasks_obj_id_91e1f861_fk_struct_structobject_id` FOREIGN KEY (`obj_id`) REFERENCES `struct_structobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `struct_changetasks`
--

LOCK TABLES `struct_changetasks` WRITE;
/*!40000 ALTER TABLE `struct_changetasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `struct_changetasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `struct_descriptions`
--

DROP TABLE IF EXISTS `struct_descriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `struct_descriptions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `doc_id` int(11) DEFAULT NULL,
  `obj_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `struct_descriptions_doc_id_e532060f_fk_files_files_id` (`doc_id`),
  KEY `struct_descriptions_obj_id_282c7be6_fk_struct_structobject_id` (`obj_id`),
  KEY `struct_descriptions_img_b2db02af` (`img`),
  KEY `struct_descriptions_created_d48fa031` (`created`),
  KEY `struct_descriptions_updated_7bd3d082` (`updated`),
  KEY `struct_descriptions_position_10f58591` (`position`),
  KEY `struct_descriptions_is_active_7495985a` (`is_active`),
  KEY `struct_descriptions_state_a9440363` (`state`),
  KEY `struct_descriptions_parents_c320eb57` (`parents`),
  KEY `struct_descriptions_name_805b8924` (`name`),
  KEY `struct_descriptions_description_bc2d301a` (`description`),
  CONSTRAINT `struct_descriptions_doc_id_e532060f_fk_files_files_id` FOREIGN KEY (`doc_id`) REFERENCES `files_files` (`id`),
  CONSTRAINT `struct_descriptions_obj_id_282c7be6_fk_struct_structobject_id` FOREIGN KEY (`obj_id`) REFERENCES `struct_structobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `struct_descriptions`
--

LOCK TABLES `struct_descriptions` WRITE;
/*!40000 ALTER TABLE `struct_descriptions` DISABLE KEYS */;
/*!40000 ALTER TABLE `struct_descriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `struct_holetasks`
--

DROP TABLE IF EXISTS `struct_holetasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `struct_holetasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `doc_id` int(11) DEFAULT NULL,
  `obj_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `struct_holetasks_doc_id_0e698167_fk_files_files_id` (`doc_id`),
  KEY `struct_holetasks_obj_id_2fe532a7_fk_struct_structobject_id` (`obj_id`),
  KEY `struct_holetasks_img_34969103` (`img`),
  KEY `struct_holetasks_created_76fdd40b` (`created`),
  KEY `struct_holetasks_updated_7b51b7bf` (`updated`),
  KEY `struct_holetasks_position_1c710c05` (`position`),
  KEY `struct_holetasks_is_active_1112dbf3` (`is_active`),
  KEY `struct_holetasks_state_a293fd27` (`state`),
  KEY `struct_holetasks_parents_722d07f8` (`parents`),
  KEY `struct_holetasks_name_0800268d` (`name`),
  KEY `struct_holetasks_description_129950a7` (`description`),
  CONSTRAINT `struct_holetasks_doc_id_0e698167_fk_files_files_id` FOREIGN KEY (`doc_id`) REFERENCES `files_files` (`id`),
  CONSTRAINT `struct_holetasks_obj_id_2fe532a7_fk_struct_structobject_id` FOREIGN KEY (`obj_id`) REFERENCES `struct_structobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `struct_holetasks`
--

LOCK TABLES `struct_holetasks` WRITE;
/*!40000 ALTER TABLE `struct_holetasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `struct_holetasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `struct_plandesicions`
--

DROP TABLE IF EXISTS `struct_plandesicions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `struct_plandesicions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `doc_id` int(11) DEFAULT NULL,
  `obj_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `struct_plandesicions_doc_id_d4759873_fk_files_files_id` (`doc_id`),
  KEY `struct_plandesicions_obj_id_e2c43208_fk_struct_structobject_id` (`obj_id`),
  KEY `struct_plandesicions_img_a4862407` (`img`),
  KEY `struct_plandesicions_created_9fa8f1fe` (`created`),
  KEY `struct_plandesicions_updated_270c2b75` (`updated`),
  KEY `struct_plandesicions_position_85032396` (`position`),
  KEY `struct_plandesicions_is_active_96c281e7` (`is_active`),
  KEY `struct_plandesicions_state_b5d2aece` (`state`),
  KEY `struct_plandesicions_parents_031beac8` (`parents`),
  KEY `struct_plandesicions_name_e24a4548` (`name`),
  KEY `struct_plandesicions_description_ded55edf` (`description`),
  CONSTRAINT `struct_plandesicions_doc_id_d4759873_fk_files_files_id` FOREIGN KEY (`doc_id`) REFERENCES `files_files` (`id`),
  CONSTRAINT `struct_plandesicions_obj_id_e2c43208_fk_struct_structobject_id` FOREIGN KEY (`obj_id`) REFERENCES `struct_structobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `struct_plandesicions`
--

LOCK TABLES `struct_plandesicions` WRITE;
/*!40000 ALTER TABLE `struct_plandesicions` DISABLE KEYS */;
/*!40000 ALTER TABLE `struct_plandesicions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `struct_preplandesicions`
--

DROP TABLE IF EXISTS `struct_preplandesicions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `struct_preplandesicions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `doc_id` int(11) DEFAULT NULL,
  `obj_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `struct_preplandesicions_doc_id_9c3c4796_fk_files_files_id` (`doc_id`),
  KEY `struct_preplandesici_obj_id_81c8e883_fk_struct_st` (`obj_id`),
  KEY `struct_preplandesicions_img_67d30469` (`img`),
  KEY `struct_preplandesicions_created_72590e8d` (`created`),
  KEY `struct_preplandesicions_updated_9b888b70` (`updated`),
  KEY `struct_preplandesicions_position_ac344beb` (`position`),
  KEY `struct_preplandesicions_is_active_7e096d2b` (`is_active`),
  KEY `struct_preplandesicions_state_6a19ecbc` (`state`),
  KEY `struct_preplandesicions_parents_a1da71fd` (`parents`),
  KEY `struct_preplandesicions_name_56968a90` (`name`),
  KEY `struct_preplandesicions_description_e741162b` (`description`),
  CONSTRAINT `struct_preplandesici_obj_id_81c8e883_fk_struct_st` FOREIGN KEY (`obj_id`) REFERENCES `struct_structobject` (`id`),
  CONSTRAINT `struct_preplandesicions_doc_id_9c3c4796_fk_files_files_id` FOREIGN KEY (`doc_id`) REFERENCES `files_files` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `struct_preplandesicions`
--

LOCK TABLES `struct_preplandesicions` WRITE;
/*!40000 ALTER TABLE `struct_preplandesicions` DISABLE KEYS */;
/*!40000 ALTER TABLE `struct_preplandesicions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `struct_sourcedata`
--

DROP TABLE IF EXISTS `struct_sourcedata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `struct_sourcedata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `doc_id` int(11) DEFAULT NULL,
  `obj_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `struct_sourcedata_doc_id_645d43ae_fk_files_files_id` (`doc_id`),
  KEY `struct_sourcedata_obj_id_103913a4_fk_struct_structobject_id` (`obj_id`),
  KEY `struct_sourcedata_img_19ab167e` (`img`),
  KEY `struct_sourcedata_created_6023148b` (`created`),
  KEY `struct_sourcedata_updated_7a1f7d40` (`updated`),
  KEY `struct_sourcedata_position_ac10e113` (`position`),
  KEY `struct_sourcedata_is_active_40be2220` (`is_active`),
  KEY `struct_sourcedata_state_aeb0d363` (`state`),
  KEY `struct_sourcedata_parents_c2625ba6` (`parents`),
  KEY `struct_sourcedata_name_0a73cafa` (`name`),
  KEY `struct_sourcedata_description_32761244` (`description`),
  CONSTRAINT `struct_sourcedata_doc_id_645d43ae_fk_files_files_id` FOREIGN KEY (`doc_id`) REFERENCES `files_files` (`id`),
  CONSTRAINT `struct_sourcedata_obj_id_103913a4_fk_struct_structobject_id` FOREIGN KEY (`obj_id`) REFERENCES `struct_structobject` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `struct_sourcedata`
--

LOCK TABLES `struct_sourcedata` WRITE;
/*!40000 ALTER TABLE `struct_sourcedata` DISABLE KEYS */;
INSERT INTO `struct_sourcedata` VALUES (1,NULL,'2021-06-22 12:29:44.371249','2021-06-22 12:29:44.371274',1,1,NULL,'','123','',NULL,NULL);
/*!40000 ALTER TABLE `struct_sourcedata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `struct_structobject`
--

DROP TABLE IF EXISTS `struct_structobject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `struct_structobject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `struct_structobject_img_082f79ce` (`img`),
  KEY `struct_structobject_created_ad3c6356` (`created`),
  KEY `struct_structobject_updated_3f2ae207` (`updated`),
  KEY `struct_structobject_position_4e008683` (`position`),
  KEY `struct_structobject_is_active_3b546f0c` (`is_active`),
  KEY `struct_structobject_state_05e0e992` (`state`),
  KEY `struct_structobject_parents_e178f2e2` (`parents`),
  KEY `struct_structobject_name_62988f46` (`name`),
  KEY `struct_structobject_description_d619dfd6` (`description`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `struct_structobject`
--

LOCK TABLES `struct_structobject` WRITE;
/*!40000 ALTER TABLE `struct_structobject` DISABLE KEYS */;
INSERT INTO `struct_structobject` VALUES (1,NULL,'2021-06-21 18:03:51.077122','2021-06-21 18:03:51.077142',1,1,NULL,'','Объект - Тайшет',NULL);
/*!40000 ALTER TABLE `struct_structobject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `struct_techtask`
--

DROP TABLE IF EXISTS `struct_techtask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `struct_techtask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `doc_id` int(11) DEFAULT NULL,
  `obj_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `struct_techtask_doc_id_8879370b_fk_files_files_id` (`doc_id`),
  KEY `struct_techtask_obj_id_41772bd5_fk_struct_structobject_id` (`obj_id`),
  KEY `struct_techtask_img_938afe0f` (`img`),
  KEY `struct_techtask_created_610536c9` (`created`),
  KEY `struct_techtask_updated_d3a595ec` (`updated`),
  KEY `struct_techtask_position_09941fbe` (`position`),
  KEY `struct_techtask_is_active_dea59f6e` (`is_active`),
  KEY `struct_techtask_state_e712f486` (`state`),
  KEY `struct_techtask_parents_9901ce3b` (`parents`),
  KEY `struct_techtask_name_4c84eacd` (`name`),
  KEY `struct_techtask_description_d0aa8a69` (`description`),
  CONSTRAINT `struct_techtask_doc_id_8879370b_fk_files_files_id` FOREIGN KEY (`doc_id`) REFERENCES `files_files` (`id`),
  CONSTRAINT `struct_techtask_obj_id_41772bd5_fk_struct_structobject_id` FOREIGN KEY (`obj_id`) REFERENCES `struct_structobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `struct_techtask`
--

LOCK TABLES `struct_techtask` WRITE;
/*!40000 ALTER TABLE `struct_techtask` DISABLE KEYS */;
/*!40000 ALTER TABLE `struct_techtask` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-01  9:47:26
