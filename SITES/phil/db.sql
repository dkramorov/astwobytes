-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: localhost    Database: phil
-- ------------------------------------------------------
-- Server version	8.0.22-0ubuntu0.20.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add user',3,'add_user'),(10,'Can change user',3,'change_user'),(11,'Can delete user',3,'delete_user'),(12,'Can view user',3,'view_user'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Админка - Настрока',6,'add_config'),(22,'Can change Админка - Настрока',6,'change_config'),(23,'Can delete Админка - Настрока',6,'delete_config'),(24,'Can view Админка - Настрока',6,'view_config'),(25,'Can add Админка - Задача',7,'add_tasks'),(26,'Can change Админка - Задача',7,'change_tasks'),(27,'Can delete Админка - Задача',7,'delete_tasks'),(28,'Can view Админка - Задача',7,'view_tasks'),(29,'Can add custom user',11,'add_customuser'),(30,'Can change custom user',11,'change_customuser'),(31,'Can delete custom user',11,'delete_customuser'),(32,'Can view custom user',11,'view_customuser'),(33,'Can add Стат.контет - Файл',12,'add_files'),(34,'Can change Стат.контет - Файл',12,'change_files'),(35,'Can delete Стат.контет - Файл',12,'delete_files'),(36,'Can view Стат.контет - Файл',12,'view_files'),(37,'Can add Стат.контент - Блоки',13,'add_blocks'),(38,'Can change Стат.контент - Блоки',13,'change_blocks'),(39,'Can delete Стат.контент - Блоки',13,'delete_blocks'),(40,'Can view Стат.контент - Блоки',13,'view_blocks'),(41,'Can add Стат.контент - Контейнеры',14,'add_containers'),(42,'Can change Стат.контент - Контейнеры',14,'change_containers'),(43,'Can delete Стат.контент - Контейнеры',14,'delete_containers'),(44,'Can view Стат.контент - Контейнеры',14,'view_containers'),(45,'Can add Стат.контент - Линковка меню к контейнерам',15,'add_linkcontainer'),(46,'Can change Стат.контент - Линковка меню к контейнерам',15,'change_linkcontainer'),(47,'Can delete Стат.контент - Линковка меню к контейнерам',15,'delete_linkcontainer'),(48,'Can view Стат.контент - Линковка меню к контейнерам',15,'view_linkcontainer'),(49,'Can add Перевод',16,'add_translate'),(50,'Can change Перевод',16,'change_translate'),(51,'Can delete Перевод',16,'delete_translate'),(52,'Can view Перевод',16,'view_translate');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$EzJikwfaVajH$mqjgGHWdZlXzEOOhWOXWJR/JYzuy2nfwvezQHen4niY=','2020-12-21 14:23:27.221290',1,'jocker','','','dkramorov@mail.ru',1,1,'2020-12-06 15:05:34.448453'),(2,'pbkdf2_sha256$150000$iCkn9bMJpnMk$YUXtB1gS8aKTM5xkl7RDhNPHmVhXEzff5sarwcIud7U=','2020-12-23 11:31:23.715067',1,'phil','Ромка','Обухов','',1,1,'2020-12-07 01:22:55.516369');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(12,'files','files'),(13,'flatcontent','blocks'),(14,'flatcontent','containers'),(15,'flatcontent','linkcontainer'),(16,'languages','translate'),(11,'login','customuser'),(8,'login','extrafields'),(10,'login','extrainfo'),(9,'login','extravalues'),(6,'main_functions','config'),(7,'main_functions','tasks'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-12-06 15:05:32.885854'),(2,'contenttypes','0002_remove_content_type_name','2020-12-06 15:05:32.963163'),(3,'auth','0001_initial','2020-12-06 15:05:33.123532'),(4,'auth','0002_alter_permission_name_max_length','2020-12-06 15:05:33.420493'),(5,'auth','0003_alter_user_email_max_length','2020-12-06 15:05:33.441130'),(6,'auth','0004_alter_user_username_opts','2020-12-06 15:05:33.449642'),(7,'auth','0005_alter_user_last_login_null','2020-12-06 15:05:33.475722'),(8,'auth','0006_require_contenttypes_0002','2020-12-06 15:05:33.477043'),(9,'auth','0007_alter_validators_add_error_messages','2020-12-06 15:05:33.483810'),(10,'auth','0008_alter_user_username_max_length','2020-12-06 15:05:33.505740'),(11,'auth','0009_alter_user_last_name_max_length','2020-12-06 15:05:33.529434'),(12,'auth','0010_alter_group_name_max_length','2020-12-06 15:05:33.549321'),(13,'auth','0011_update_proxy_permissions','2020-12-06 15:05:33.555954'),(14,'files','0001_initial','2020-12-06 15:05:33.592665'),(15,'files','0002_auto_20191203_2054','2020-12-06 15:05:33.651802'),(16,'files','0003_auto_20200112_1717','2020-12-06 15:05:33.661676'),(17,'files','0004_auto_20200402_2127','2020-12-06 15:05:33.684500'),(18,'files','0005_auto_20200809_1025','2020-12-06 15:05:33.689742'),(19,'flatcontent','0001_initial','2020-12-06 15:05:33.789666'),(20,'flatcontent','0002_auto_20190825_1730','2020-12-06 15:05:34.064986'),(21,'flatcontent','0003_auto_20191203_2054','2020-12-06 15:05:34.098845'),(22,'flatcontent','0004_blocks_html','2020-12-06 15:05:34.119900'),(23,'flatcontent','0005_auto_20200112_1717','2020-12-06 15:05:34.152250'),(24,'flatcontent','0006_auto_20200314_1638','2020-12-06 15:05:34.157468'),(25,'flatcontent','0007_auto_20200402_2127','2020-12-06 15:05:34.291772'),(26,'flatcontent','0008_containers_class_name','2020-12-06 15:05:34.322991'),(27,'login','0001_initial','2020-12-06 15:05:34.560287'),(28,'login','0002_auto_20200925_1007','2020-12-06 15:05:34.812187'),(29,'main_functions','0001_initial','2020-12-06 15:05:34.849209'),(30,'main_functions','0002_auto_20191203_2052','2020-12-06 15:05:34.869351'),(31,'main_functions','0003_auto_20200407_1845','2020-12-06 15:05:35.150781'),(32,'sessions','0001_initial','2020-12-06 15:05:35.249068'),(33,'flatcontent','0009_blocks_class_name','2020-12-08 12:14:37.554523'),(34,'languages','0001_initial','2020-12-21 13:53:48.080872');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
INSERT INTO `django_session` VALUES ('08nuz9dc2x9hakjix3zllrv57nzvoufl','OGYxYzFhMTk5OWU3YmQ5ZmE3YTIxOGQyYzY2MzkxN2RiMzRlYzllZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjJiOTViMzRiNDJhOWM5NjdhNDNlMmZiMzViMTI4OTM2N2Q0Y2IxZDUifQ==','2020-12-20 15:29:33.456916'),('0deo768c0rv4fzam25sg1txqa7htp0vk','ODA4MzA2YjNhYjY5OWI1NmUwYzVjZTAyODY1NjYwNDE0ZDZkNjhiYTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjJiOTViMzRiNDJhOWM5NjdhNDNlMmZiMzViMTI4OTM2N2Q0Y2IxZDUiLCJsYW5nIjoicnVzIn0=','2021-01-04 14:27:56.558665'),('j7irld6581nyark250s1s7wm5h5due0t','OGYxYzFhMTk5OWU3YmQ5ZmE3YTIxOGQyYzY2MzkxN2RiMzRlYzllZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjJiOTViMzRiNDJhOWM5NjdhNDNlMmZiMzViMTI4OTM2N2Q0Y2IxZDUifQ==','2020-12-22 15:59:31.936723'),('mrp1d5xvbeokknjw6aciwtohatemjlzr','OGYxYzFhMTk5OWU3YmQ5ZmE3YTIxOGQyYzY2MzkxN2RiMzRlYzllZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjJiOTViMzRiNDJhOWM5NjdhNDNlMmZiMzViMTI4OTM2N2Q0Y2IxZDUifQ==','2020-12-21 10:13:31.571322'),('o3chtyqaxrz1r12vfmyq7q1kgzj8re5q','OGYxYzFhMTk5OWU3YmQ5ZmE3YTIxOGQyYzY2MzkxN2RiMzRlYzllZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjJiOTViMzRiNDJhOWM5NjdhNDNlMmZiMzViMTI4OTM2N2Q0Y2IxZDUifQ==','2020-12-24 18:30:35.231827'),('sm4p2g8429myxh3h59t2wxmp7c80m7qj','OGYxYzFhMTk5OWU3YmQ5ZmE3YTIxOGQyYzY2MzkxN2RiMzRlYzllZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjJiOTViMzRiNDJhOWM5NjdhNDNlMmZiMzViMTI4OTM2N2Q0Y2IxZDUifQ==','2020-12-30 17:37:31.630617'),('ur4udhe5mt52ke2mz4a7wmcioco76p3g','NTc3OTk0MTc3ZjIxNDM2M2E0YjE2Y2E0YjIyNDNhNTc3NzQ0NmJkODp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImZkYzM4NWNiOWRlMzNmYWM3MDQzOGM3NTY0NTk4ZDY4YjM0YzhiNjQiLCJsYW5nIjoiY2hpIn0=','2021-01-06 14:40:22.183722');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `files_files`
--

DROP TABLE IF EXISTS `files_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `files_files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `desc` longtext,
  `mime` varchar(255) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
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
  KEY `files_files_img_fbfb9b0a` (`img`)
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flatcontent_blocks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `tag` varchar(255) DEFAULT NULL,
  `container_id` int DEFAULT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=198 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
INSERT INTO `flatcontent_blocks` VALUES (1,'1.png','2020-12-06 15:28:44.652426','2020-12-08 12:44:39.442372',1,1,1,'','Логотип','design and endless ideas','/','logo',1,0,'','','','Infinity Ink - a Universe of endless ideas. We are a design studio with an unusual view on ordinary things. From here we set out to explore the mysteries of design. Design that helps you to really stand out.<br>',''),(2,NULL,'2020-12-06 15:28:44.656728','2020-12-07 17:54:33.528348',2,1,1,'','Телефон','','tel:73952123321','phone',1,0,'','','','<div>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p><span>+86 134 29 020002</span></p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n		</div>',NULL),(3,NULL,'2020-12-06 15:28:44.660991','2020-12-23 13:59:27.096273',3,1,1,'','CHINA','Our address','','address',1,0,'','','','<div>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>#225, Krspace, No.328 Huashan Road,\r\nJingan District, Shanghai. <br>Post code: 200040\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n		</div>',''),(4,NULL,'2020-12-06 15:28:44.663594','2020-12-23 14:15:52.682382',4,1,1,'','Email china','Online Support','','email',1,0,'','','','<div>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>info@infinityink.cn</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n		</div>',''),(5,NULL,'2020-12-06 15:28:44.666013','2020-12-06 15:28:44.666030',5,1,3,'','Режим работы',NULL,NULL,'worktime',1,0,NULL,NULL,NULL,'пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 17:00',NULL),(6,NULL,'2020-12-06 15:28:44.668630','2020-12-07 18:03:51.326700',6,1,1,'','Copyright','','','copyright',1,0,'','','','<p>\r\n\r\n	\r\n		\r\n		\r\n	\r\n	\r\n		<div>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>© 2021 Infinity Ink\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n		</div>\r\n	\r\n</p>',NULL),(7,NULL,'2020-12-06 15:28:44.671258','2020-12-06 15:28:44.671276',7,1,3,'','Сообщества',NULL,NULL,'social',1,0,NULL,NULL,NULL,NULL,NULL),(8,NULL,'2020-12-06 15:28:44.673801','2020-12-06 15:28:44.673817',8,1,3,'_7','instagram',NULL,NULL,'instagram',1,1,'instagram',NULL,NULL,NULL,NULL),(9,NULL,'2020-12-06 15:28:44.676489','2020-12-06 15:28:44.676511',9,1,3,'_7','vk',NULL,NULL,'vk',1,1,'vk',NULL,NULL,NULL,NULL),(10,NULL,'2020-12-06 15:28:44.679271','2020-12-06 15:28:44.679291',10,1,3,'_7','facebook',NULL,NULL,'facebook',1,1,'facebook',NULL,NULL,NULL,NULL),(11,NULL,'2020-12-06 15:28:44.681897','2020-12-06 15:28:44.681917',11,1,3,'_7','twitter',NULL,NULL,'twitter',1,1,'twitter',NULL,NULL,NULL,NULL),(12,NULL,'2020-12-06 15:28:44.689053','2020-12-23 11:34:37.573997',1,1,4,'','Home','','/','_mainmenu_mainpage',2,0,'','','','',''),(13,NULL,'2020-12-06 15:28:44.692091','2020-12-23 12:02:38.024658',3,1,4,'','Portfolio','Look at out works','#portfolio','_mainmenu_catpage',2,0,'','','','If you have a questions, please, let us know about it<br>',''),(14,NULL,'2020-12-06 15:28:44.695615','2020-12-23 14:39:13.539213',14,1,4,'_13','Identity','','/portfolio/banners/','',2,0,'','','','',''),(15,NULL,'2020-12-06 15:28:44.698908','2020-12-23 14:39:25.701522',15,1,4,'_13','Illustrations','','/portfolio/videos/','',2,0,'','','','',''),(16,NULL,'2020-12-06 15:28:44.702483','2020-12-23 14:39:38.035480',16,1,4,'_13','Toys','','/portfolio/logos/','',2,0,'','','','',''),(17,NULL,'2020-12-06 15:28:44.706091','2020-12-23 14:39:47.740004',17,1,4,'_13','Industrial','','/portfolio/other/','',2,0,'','','','',''),(18,NULL,'2020-12-06 15:28:44.708740','2020-12-23 11:56:58.087771',4,1,4,'','Services','','#simple_services','_mainmenu_aboutpage',2,0,'','','','',''),(19,NULL,'2020-12-06 15:28:44.711479','2020-12-23 11:57:12.219468',5,1,4,'','Design Application','','#','_mainmenu_servicespage',2,0,'','','','','custom-open-aside'),(20,NULL,'2020-12-06 15:28:44.714025','2020-12-23 11:57:26.523774',6,1,4,'','Contacts','','#simple_contacts','_mainmenu_feedbackpage',2,0,'','','','',''),(21,NULL,'2020-12-06 15:28:44.716584','2020-12-06 15:28:44.716606',21,1,4,'','Каталог',NULL,'/cat/','_bottommenu_catpage',3,0,NULL,NULL,NULL,NULL,NULL),(22,NULL,'2020-12-06 15:28:44.719947','2020-12-06 15:28:44.719968',22,1,4,'_21','Популярные товары',NULL,'/cat/populyarnye-tovary/','_bottommenu_catpage_popular',3,0,NULL,NULL,NULL,NULL,NULL),(23,NULL,'2020-12-06 15:28:44.723227','2020-12-06 15:28:44.723246',23,1,4,'_21','Новые товары',NULL,'/cat/novye-tovary/','_bottommenu_catpage_new',3,0,NULL,NULL,NULL,NULL,NULL),(24,NULL,'2020-12-06 15:28:44.726606','2020-12-06 15:28:44.726629',24,1,4,'_21','Товары со скидкой',NULL,'/cat/tovary-so-skidkoy/','_bottommenu_catpage_discount',3,0,NULL,NULL,NULL,NULL,NULL),(25,NULL,'2020-12-06 15:28:44.729982','2020-12-06 15:28:44.730003',25,1,4,'_21','Распродажа',NULL,'/cat/rasprodaja/','_bottommenu_catpage_sale',3,0,NULL,NULL,NULL,NULL,NULL),(26,NULL,'2020-12-06 15:28:44.732518','2020-12-06 15:28:44.732537',26,1,4,'','О нас',NULL,'/about/','_bottommenu_aboutpage',3,0,NULL,NULL,NULL,NULL,NULL),(27,NULL,'2020-12-06 15:28:44.735080','2020-12-06 15:28:44.735099',27,1,4,'','Услуги',NULL,'/services/','_bottommenu_servicespage',3,0,NULL,NULL,NULL,NULL,NULL),(28,NULL,'2020-12-06 15:28:44.737871','2020-12-06 15:28:44.737894',28,1,4,'','Контакты',NULL,'/feedback/','_bottommenu_feedbackpage',3,0,NULL,NULL,NULL,NULL,NULL),(29,NULL,'2020-12-06 17:18:27.178880','2020-12-23 11:41:43.823754',2,1,4,'','Our Team','','#team','',2,0,'','','','',''),(30,NULL,'2020-12-06 18:37:49.085895','2020-12-06 18:38:46.065752',29,1,1,'','Инфа с контактами','Get in touch','','get_in_touch',1,0,'','','','You can call us or send email, we will be happy answer on your questions<br>',NULL),(31,'31.png','2020-12-07 00:31:29.938958','2020-12-07 00:31:35.327916',30,1,1,'','About Infinity Ink','','','',4,0,'','','','Infinity Ink - a Universe of endless ideas.<br>We are a design studio with an unusual<br>view on ordinary things. From here we set<br>out to explore the mysteries of design.<br>Design that helps you to really stand out.<br><br>Since 2015, Infinity Ink has been successfully<br>solving various customer problems with the<br>help of design.<br><i>No nonsense. Just effective results.</i>',NULL),(32,'31.png','2020-12-07 00:49:00.010188','2020-12-23 13:53:15.086877',30,1,1,'','About Infinity Ink','','','',5,0,'','','','Infinity Ink - a Universe of endless ideas.<br>We are a design studio with an unusual<br>view on ordinary things. From here we set<br>out to explore the mysteries of design.<br>Design that helps you to really stand out.<br><br>Since 2015, Infinity Ink has been successfully<br>solving various customer problems with the<br>help of design.<br><i>No nonsense. Just effective results.</i>',''),(33,NULL,'2020-12-07 01:05:21.871968','2020-12-07 01:06:14.849853',31,1,1,'','Identity','24','','',6,0,'','','','',NULL),(34,NULL,'2020-12-07 01:05:42.416007','2020-12-07 01:06:33.369159',32,1,1,'','Illustration','15','','',6,0,'','','','',NULL),(35,NULL,'2020-12-07 01:05:45.901077','2020-12-07 01:07:14.138879',33,1,1,'','Toys','20','','',6,0,'','','','',NULL),(36,NULL,'2020-12-07 01:05:51.976889','2020-12-07 01:10:12.807317',34,1,1,'','Industrial','09','','',6,0,'','','','',NULL),(37,NULL,'2020-12-07 01:05:56.862369','2020-12-07 01:10:17.851124',35,1,1,'','Packaging','06','','',6,0,'','','','',NULL),(38,NULL,'2020-12-07 01:06:01.134484','2020-12-07 01:10:21.743372',36,1,1,'','Web','05','','',6,0,'','','','',NULL),(41,'41.jpg','2020-12-07 01:10:44.384111','2020-12-07 01:40:57.868995',39,1,1,'_33','RusCASA - real estate agency','','','',6,0,'','','','',NULL),(42,'42.jpg','2020-12-07 01:41:17.607376','2020-12-07 01:41:17.607396',40,1,1,'_33','Empy - pet accessories',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(43,'43.jpg','2020-12-07 01:41:32.624090','2020-12-07 01:41:32.624108',41,1,1,'_33','SnimiSnami - video studio',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(44,NULL,'2020-12-07 01:41:51.324117','2020-12-07 01:41:51.324137',42,1,1,'_33','Obro toys - wooden toys brand',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(45,NULL,'2020-12-07 01:42:06.105733','2020-12-07 01:42:06.105755',43,1,1,'_33','Rugo doors - door manufacturer',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(46,NULL,'2020-12-07 01:42:22.046177','2020-12-07 01:42:22.046198',44,1,1,'_33','Ural locomotives on Innoprom 2018',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(47,NULL,'2020-12-07 01:42:36.670545','2020-12-07 01:42:36.670564',45,1,1,'_33','Marketing Agency - Market Entry Atelier',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(48,NULL,'2020-12-07 01:42:49.686445','2020-12-07 01:42:49.686464',46,1,1,'_33','Instant noodles - \"Moodle\"',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(49,NULL,'2020-12-07 01:43:03.551404','2020-12-07 01:43:03.551424',47,1,1,'_33','Novae - decoration manufacturer',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(50,NULL,'2020-12-07 01:43:20.525886','2020-12-07 01:43:20.525907',48,1,1,'_33','Video Marketing',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(51,NULL,'2020-12-07 01:43:34.698531','2020-12-07 01:43:34.698551',49,1,1,'_33','Baby shop - Ballet Bear',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(52,NULL,'2020-12-07 01:43:47.142525','2020-12-07 01:43:47.142548',50,1,1,'_33','Bai advertising',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(53,NULL,'2020-12-07 01:44:07.360384','2020-12-07 01:44:07.360413',51,1,1,'_33','\"Street Childhood\" - shop',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(54,NULL,'2020-12-07 01:44:34.598643','2020-12-07 01:44:34.598664',52,1,1,'_33','FC \"Urumqi\" - concept',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(55,NULL,'2020-12-07 01:45:02.014265','2020-12-07 01:45:02.014305',53,1,1,'_33','\"City-ride\" - shop logo',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(56,NULL,'2020-12-07 01:45:13.227068','2020-12-07 01:45:13.227088',54,1,1,'_33','Bistro \"Hunan\"',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(57,NULL,'2020-12-07 01:45:23.768755','2020-12-07 01:45:23.768776',55,1,1,'_33','Fashion boutique - Brand Collector',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(58,NULL,'2020-12-07 01:45:37.628617','2020-12-07 01:45:37.628646',56,1,1,'_33','Contention agency',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(59,NULL,'2020-12-07 01:45:50.175367','2020-12-07 01:45:50.175386',57,1,1,'_33','Fasteners and tools \"Yalida\"',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(60,NULL,'2020-12-07 01:46:00.072373','2020-12-07 01:46:00.072392',58,1,1,'_33','Urban Developement',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(61,NULL,'2020-12-07 01:46:09.996207','2020-12-07 01:46:09.996229',59,1,1,'_33','Trade company \"Caravel\"',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(62,NULL,'2020-12-07 01:46:21.881723','2020-12-07 01:46:21.881743',60,1,1,'_33','Barbershop - Hair Piece',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(63,NULL,'2020-12-07 01:46:33.766484','2020-12-07 01:46:33.766510',61,1,1,'_33','Corporate pavilion for Intime',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(64,NULL,'2020-12-07 01:46:44.922672','2020-12-07 01:46:44.922692',62,1,1,'_33','Fishing gear - Da he Lian',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(65,'65.jpg','2020-12-07 10:06:31.079720','2020-12-07 10:06:31.079746',63,1,1,'_33_41','1',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(66,'66.jpg','2020-12-07 10:06:35.510927','2020-12-07 10:06:35.510950',64,1,1,'_33_41','2',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(67,'67.png','2020-12-07 10:07:21.606214','2020-12-07 10:07:21.606233',65,1,1,'_33_42','1',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(68,'68.jpg','2020-12-07 10:07:23.827385','2020-12-07 10:07:23.827406',66,1,1,'_33_42','2',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(69,'69.jpg','2020-12-07 10:07:26.314752','2020-12-07 10:07:26.314773',67,1,1,'_33_42','3',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(105,NULL,'2020-12-07 14:03:29.417444','2020-12-23 13:57:06.167765',31,1,1,'','Identity','24','','',9,0,'','','','',''),(106,'41.jpg','2020-12-07 14:03:29.422128','2020-12-07 14:03:29.422323',39,1,1,'_105','RusCASA - real estate agency','','','',9,0,'','','','',NULL),(107,'65.jpg','2020-12-07 14:03:29.429275','2020-12-07 14:03:29.429302',63,1,1,'_105_106','1',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(108,'66.jpg','2020-12-07 14:03:29.461932','2020-12-07 14:03:29.461954',64,1,1,'_105_106','2',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(109,'42.jpg','2020-12-07 14:03:29.471606','2020-12-07 14:03:29.471717',40,1,1,'_105','Empy - pet accessories',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(110,'67.png','2020-12-07 14:03:29.490579','2020-12-07 14:03:29.490600',65,1,1,'_105_109','1',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(111,'68.jpg','2020-12-07 14:03:29.500769','2020-12-07 14:03:29.500799',66,1,1,'_105_109','2',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(112,'69.jpg','2020-12-07 14:03:29.531551','2020-12-07 14:03:29.531584',67,1,1,'_105_109','3',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(113,'43.jpg','2020-12-07 14:03:29.573659','2020-12-07 14:03:29.573694',41,1,1,'_105','SnimiSnami - video studio',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(114,NULL,'2020-12-07 14:03:29.591988','2020-12-07 14:03:29.592010',42,1,1,'_105','Obro toys - wooden toys brand',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(115,NULL,'2020-12-07 14:03:29.621332','2020-12-07 14:03:29.621354',43,1,1,'_105','Rugo doors - door manufacturer',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(116,NULL,'2020-12-07 14:03:29.623486','2020-12-07 14:03:29.623507',44,1,1,'_105','Ural locomotives on Innoprom 2018',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(117,NULL,'2020-12-07 14:03:29.625214','2020-12-07 14:03:29.625236',45,1,1,'_105','Marketing Agency - Market Entry Atelier',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(118,NULL,'2020-12-07 14:03:29.626529','2020-12-07 14:03:29.626548',46,1,1,'_105','Instant noodles - \"Moodle\"',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(119,NULL,'2020-12-07 14:03:29.629937','2020-12-07 14:03:29.629959',47,1,1,'_105','Novae - decoration manufacturer',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(120,NULL,'2020-12-07 14:03:29.630778','2020-12-07 14:03:29.630799',48,1,1,'_105','Video Marketing',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(121,NULL,'2020-12-07 14:03:29.631606','2020-12-07 14:03:29.631623',49,1,1,'_105','Baby shop - Ballet Bear',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(122,NULL,'2020-12-07 14:03:29.633630','2020-12-07 14:03:29.633646',50,1,1,'_105','Bai advertising',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(123,NULL,'2020-12-07 14:03:29.634356','2020-12-07 14:03:29.634373',51,1,1,'_105','\"Street Childhood\" - shop',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(124,NULL,'2020-12-07 14:03:29.635078','2020-12-07 14:03:29.635095',52,1,1,'_105','FC \"Urumqi\" - concept',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(125,NULL,'2020-12-07 14:03:29.635824','2020-12-07 14:03:29.635840',53,1,1,'_105','\"City-ride\" - shop logo',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(126,NULL,'2020-12-07 14:03:29.636634','2020-12-07 14:03:29.636650',54,1,1,'_105','Bistro \"Hunan\"',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(127,NULL,'2020-12-07 14:03:29.637391','2020-12-07 14:03:29.637408',55,1,1,'_105','Fashion boutique - Brand Collector',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(128,NULL,'2020-12-07 14:03:29.638249','2020-12-07 14:03:29.638268',56,1,1,'_105','Contention agency',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(129,NULL,'2020-12-07 14:03:29.639119','2020-12-07 14:03:29.639140',57,1,1,'_105','Fasteners and tools \"Yalida\"',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(130,NULL,'2020-12-07 14:03:29.640050','2020-12-07 14:03:29.640079',58,1,1,'_105','Urban Developement',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(131,NULL,'2020-12-07 14:03:29.642211','2020-12-07 14:03:29.642231',59,1,1,'_105','Trade company \"Caravel\"',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(132,NULL,'2020-12-07 14:03:29.644425','2020-12-07 14:03:29.644441',60,1,1,'_105','Barbershop - Hair Piece',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(133,NULL,'2020-12-07 14:03:29.645186','2020-12-07 14:03:29.645204',61,1,1,'_105','Corporate pavilion for Intime',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(134,NULL,'2020-12-07 14:03:29.645949','2020-12-07 14:03:29.645966',62,1,1,'_105','Fishing gear - Da he Lian',NULL,NULL,NULL,9,0,NULL,NULL,NULL,NULL,NULL),(135,NULL,'2020-12-07 14:03:29.646718','2020-12-23 13:40:47.780492',32,1,1,'','Illustration','15','','',9,0,'','','','',''),(136,NULL,'2020-12-07 14:03:29.647541','2020-12-23 13:57:12.252698',33,1,1,'','Toys','20','','',9,0,'','','','',''),(137,NULL,'2020-12-07 14:03:29.649777','2020-12-23 13:57:16.981216',34,1,1,'','Industrial','09','','',9,0,'','','','',''),(138,NULL,'2020-12-07 14:03:29.650552','2020-12-23 13:57:23.532250',35,1,1,'','Packaging','06','','',9,0,'','','','',''),(139,NULL,'2020-12-07 14:03:29.651317','2020-12-23 13:57:28.633515',36,1,1,'','Web','05','','',9,0,'','','','',''),(140,NULL,'2020-12-07 14:19:40.022292','2020-12-07 14:23:00.987938',68,1,1,'','Identity','Identity projects','/','',10,0,'','','','Developing an identity is a complex task, the correct approach to which allows you to form the \"face\" of a brand or company.<br>Corporate identity is the interaction of all visual elements used for communication with the target audience.<br><br>We take into account how corporate colors, fonts and graphics will look in different conditions and on different media - indoors and outdoors, in bright and low light, on a poster and on a small business card.<br>',NULL),(141,NULL,'2020-12-07 14:19:42.058842','2020-12-07 14:25:45.714692',69,1,1,'','Toys','Toys projects','/','',10,0,'','','','Toy design main goal is to contribute to growth and development of children, encourage their imagination and use of various skills, and, of course, to provide them with high-quality, safe and fun experience.<br><br>We believe that toys should provide high educational and developmental value for children, be comprehensive and engaging to play.<br>',NULL),(142,NULL,'2020-12-07 14:19:50.012361','2020-12-07 14:27:41.577599',70,1,1,'','Illustration','Illustration projects','/','',10,0,'','','','Revives \"boring\" multi-page commercial offers and reports. Fills ads with bright, memorable images. Decorates things.<br><br>When picking up a book, package, or toy, the vast majority of people first look at the illustrations. Vivid visual images can evoke a strong emotional response in people.<br>',NULL),(143,NULL,'2020-12-07 14:19:50.942347','2020-12-07 14:29:58.534592',71,1,1,'','Industrial','Industrial projects','/','',10,0,'','','','The product must be competitive and attractive. How to produce a product that meets these conditions? Industrial design becomes an integral part of product design, improvement, and commercial success.<br><br>Without a harmonious and functional design, it is impossible to complete in the modern market. We develop up-to-date design of consumer goods and electronic devices.<br>',NULL),(144,NULL,'2020-12-07 14:19:51.886355','2020-12-07 14:32:05.848785',72,1,1,'','Packaging','Packaging projects','/','',10,0,'','','','A characteristic feature of the modern market is a high level of competition. In such conditions, it is not enough just to release a quality product. It is equally important to present it correctly to potential consumers.<br><br>The original memorable packaging design helps in solving this problem. Effective product packaging design attracts attention, effective - makes people buy.<br>',NULL),(145,NULL,'2020-12-07 14:19:53.223351','2020-12-07 14:34:29.166189',73,1,1,'','Web','Web projects','/','',10,0,'','','','Online branding is the most important business engine in the modern world. Structured content allows you to work correctly to attract new customers and work with existing ones.<br><br>Our task is to design web user interfaces, websites or web applications. Unique design for each specific client, to provide high consumer properties and aesthetic qualities.<br>',NULL),(146,NULL,'2020-12-07 15:13:04.146812','2020-12-23 13:41:56.834722',68,1,1,'','Identity','Identity projects','/','',11,0,'','','','Developing an identity is a complex task, the correct approach to which allows you to form the \"face\" of a brand or company.<br>Corporate identity is the interaction of all visual elements used for communication with the target audience.<br><br>We take into account how corporate colors, fonts and graphics will look in different conditions and on different media - indoors and outdoors, in bright and low light, on a poster and on a small business card.<br>',''),(147,NULL,'2020-12-07 15:13:04.147885','2020-12-23 14:19:15.678967',69,1,1,'','Toys','Toys projects','/','',11,0,'','','','Toy design main goal is to contribute to growth and development of children, encourage their imagination and use of various skills, and, of course, to provide them with high-quality, safe and fun experience.<br><br>We believe that toys should provide high educational and developmental value for children, be comprehensive and engaging to play.&nbsp;Our team consists of people who devote themselves completely to creating toys, people who, despite their age, remain children in their souls. Each of us tries to feel the gameplay and bring something new, useful in our own way.<br>',''),(148,NULL,'2020-12-07 15:13:04.148855','2020-12-23 14:19:20.336866',70,1,1,'','Illustration','Illustration projects','/','',11,0,'','','','Revives \"boring\" multi-page commercial offers and reports. Fills ads with bright, memorable images. Decorates things.<br><br>When picking up a book, package, or toy, the vast majority of people first look at the illustrations. Vivid visual images can evoke a strong emotional response in people.<br>',''),(149,NULL,'2020-12-07 15:13:04.151161','2020-12-23 14:19:24.668869',71,1,1,'','Industrial','Industrial projects','/','',11,0,'','','','The product must be competitive and attractive. How to produce a product that meets these conditions? Industrial design becomes an integral part of product design, improvement, and commercial success.<br><br>Without a harmonious and functional design, it is impossible to complete in the modern market. We develop up-to-date design of consumer goods and electronic devices.<br>',''),(150,NULL,'2020-12-07 15:13:04.152054','2020-12-23 14:19:28.634978',72,1,1,'','Packaging','Packaging projects','/','',11,0,'','','','A characteristic feature of the modern market is a high level of competition. In such conditions, it is not enough just to release a quality product. It is equally important to present it correctly to potential consumers.<br><br>The original memorable packaging design helps in solving this problem. Effective product packaging design attracts attention, effective - makes people buy.<br>',''),(151,NULL,'2020-12-07 15:13:04.165191','2020-12-23 14:19:32.834624',73,1,1,'','Web','Web projects','/','',11,0,'','','','Online branding is the most important business engine in the modern world. Structured content allows you to work correctly to attract new customers and work with existing ones.<br><br>Our task is to design web user interfaces, websites or web applications. Unique design for each specific client, to provide high consumer properties and aesthetic qualities.<br>',''),(152,'152.png','2020-12-07 15:19:14.225550','2020-12-07 16:51:46.454965',74,1,1,'','IVAN','designer | creative director','/','',12,0,'','','','More than 9 years of experience in design and international art projects in Russia, China and Spain.<br><br>I love any form of design and prefer to combine original ideas with great passion and dedication. I get one simple method to achieve the big desired results - eclecticism, original ideas and a great love to my work.<br>',NULL),(153,'153.png','2020-12-07 15:19:28.215787','2020-12-07 15:23:19.696134',75,1,1,'','CLEMENCE','industrial designer | engineer','','',12,0,'','','','My experiences led me to work on both industrial products (robots, connected objects, toys...) and digital (websites, mobile applications).<br><br>I enjoy all types of missions, be it the complete design of your project or a punctual accompaniment on a precise phase of you development.<br>',NULL),(154,'154.png','2020-12-07 15:19:31.880538','2020-12-07 15:24:48.233698',76,1,1,'','ROMAN','design director | project director','','',12,0,'','','','Managing foreign design projects for over 7 years. Perfect knowledge of the Chinese language helps me to provide best service to our clients.<br><br>I have extensive experience in the organization of mass production, working with typography, as well as branding for Chinese market. My goal is to bring our projects to the real life.<br>',NULL),(155,'152.png','2020-12-07 16:54:06.391059','2020-12-23 13:46:57.461892',74,1,1,'','IVAN','designer | creative director','/','',13,0,'','','','More than 9 years of experience in design and international art projects in Russia, China and Spain.<br><br>I love any form of design and prefer to combine original ideas with great passion and dedication. I get one simple method to achieve the big desired results - eclecticism, original ideas and a great love to my work.<br>',''),(156,'153.png','2020-12-07 16:54:06.399790','2020-12-23 12:18:09.647335',75,1,1,'','CLEMENCE','industrial designer | engineer','','',13,0,'','','','My experiences led me to work on both industrial products (robots, connected objects, toys...) and digital (websites, mobile applications).<br><br>I enjoy all types of missions, be it the complete design of your project or a punctual accompaniment on a precise phase of you development.<br>',''),(157,'154.png','2020-12-07 16:54:06.413457','2020-12-23 13:49:41.853914',76,1,1,'','ROMAN','design director | project director','','',13,0,'','','','Managing foreign design projects for over 7 years. Perfect knowledge of the Chinese language helps me to provide best service to our clients.<br><br>I have extensive experience in the organization of mass production, toys design, working with typography, as well as branding for Chinese market. My goal is to bring our projects to the real life.<br>',''),(158,'158.png','2020-12-07 17:31:19.505059','2020-12-07 17:32:30.221483',77,1,1,'','1','','','',14,0,'','','','',NULL),(159,'159.png','2020-12-07 17:31:20.977085','2020-12-07 17:32:32.819997',78,1,1,'','2','','','',14,0,'','','','',NULL),(160,'160.png','2020-12-07 17:31:22.003850','2020-12-07 17:32:35.221784',79,1,1,'','3','','','',14,0,'','','','',NULL),(161,'161.png','2020-12-07 17:31:22.900422','2020-12-07 17:32:26.872875',80,1,1,'','4','','','',14,0,'','','','',NULL),(162,'162.png','2020-12-07 17:31:23.784153','2020-12-10 19:08:27.862359',81,1,1,'','5','','','',14,0,'','','','',''),(163,'163.png','2020-12-07 17:31:24.691283','2020-12-07 17:32:47.736540',82,1,1,'','6','','','',14,0,'','','','',NULL),(164,'164.png','2020-12-07 17:31:25.519585','2020-12-07 17:32:54.104143',83,1,1,'','7','','','',14,0,'','','','',NULL),(165,'165.png','2020-12-07 17:31:26.287030','2020-12-07 17:32:58.174878',84,1,1,'','8','','','',14,0,'','','','',NULL),(166,'166.png','2020-12-07 17:31:27.356459','2020-12-10 19:06:46.132919',85,1,1,'','9','','','',14,0,'','','','',''),(167,'167.png','2020-12-07 17:31:28.352229','2020-12-07 17:33:05.329838',86,1,1,'','10','','','',14,0,'','','','',NULL),(168,'168.png','2020-12-07 17:33:08.502798','2020-12-07 17:33:08.502822',87,1,1,'','11',NULL,NULL,NULL,14,0,NULL,NULL,NULL,NULL,NULL),(180,'158.png','2020-12-07 17:41:52.764591','2020-12-07 17:41:52.764613',77,1,1,'','1','','','',16,0,'','','','',NULL),(181,'159.png','2020-12-07 17:41:52.767233','2020-12-07 17:41:52.767252',78,1,1,'','2','','','',16,0,'','','','',NULL),(182,'160.png','2020-12-07 17:41:52.774565','2020-12-07 17:41:52.774595',79,1,1,'','3','','','',16,0,'','','','',NULL),(183,'161.png','2020-12-07 17:41:52.781547','2020-12-07 17:41:52.781574',80,1,1,'','4','','','',16,0,'','','','',NULL),(184,'162.png','2020-12-07 17:41:52.789212','2020-12-07 17:41:52.789246',81,1,1,'','5','','','',16,0,'','','','',NULL),(185,'163.png','2020-12-07 17:41:52.808149','2020-12-07 17:41:52.808177',82,1,1,'','6','','','',16,0,'','','','',NULL),(186,'164.png','2020-12-07 17:41:52.815784','2020-12-07 17:41:52.815810',83,1,1,'','7','','','',16,0,'','','','',NULL),(187,'165.png','2020-12-07 17:41:52.823615','2020-12-07 17:41:52.823642',84,1,1,'','8','','','',16,0,'','','','',NULL),(188,'166.png','2020-12-07 17:41:52.830946','2020-12-07 17:41:52.830975',85,1,1,'','9','','','',16,0,'','','','',NULL),(189,'167.png','2020-12-07 17:41:52.838318','2020-12-07 17:41:52.838352',86,1,1,'','10','','','',16,0,'','','','',NULL),(190,'168.png','2020-12-07 17:41:52.845806','2020-12-07 17:41:52.845827',87,1,1,'','11',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(191,NULL,'2020-12-07 17:50:32.190586','2020-12-23 14:13:27.767866',88,1,1,'','RUSSIA','','','address2',1,0,'','','','<div>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p><span>Yekaterinburg city, st. Metallurgov 32, #42\r\nPost code: 620131<br></span></p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n		</div>',''),(192,NULL,'2020-12-07 17:54:06.170846','2020-12-07 17:54:16.113014',89,1,1,'','Телефон','','','phone2',1,0,'','','','<div>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p><span>+7 922 132 4999</span></p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n		</div>',NULL),(193,NULL,'2020-12-07 17:55:11.520576','2020-12-23 14:16:44.194591',90,1,1,'','Email Russia','','','email2',1,0,'','','','<div>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>info@infinityink.eu</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n		</div>',''),(194,NULL,'2020-12-16 18:02:48.146052','2020-12-23 15:05:11.132719',91,1,1,'','Design Application','','','right_panel',1,0,'','','','Do you want to order a design?<br>Write briefly about the project and <br>we will call you back for further details.<br>',''),(196,NULL,'2020-12-23 11:52:01.658032','2020-12-23 14:39:52.887080',92,1,4,'_13','Packaging','','#portfoliobez-nazvaniya/','',2,0,'','','','',''),(197,NULL,'2020-12-23 11:55:29.961796','2020-12-23 14:39:58.997176',93,1,4,'_13','Web','','#portfolioweb-design/','',2,0,'','','','','');
/*!40000 ALTER TABLE `flatcontent_blocks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flatcontent_containers`
--

DROP TABLE IF EXISTS `flatcontent_containers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flatcontent_containers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int DEFAULT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
INSERT INTO `flatcontent_containers` VALUES (1,NULL,'2020-12-06 15:28:44.635919','2020-12-06 15:28:44.635952',1,1,2,NULL,'Контент для всех страничек','Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики','main',NULL,NULL),(2,NULL,'2020-12-06 15:28:44.684205','2020-12-06 15:28:44.684224',2,1,1,NULL,'Главное меню','Создано автоматически, выводит главное меню','mainmenu',NULL,NULL),(3,NULL,'2020-12-06 15:28:44.686457','2020-12-06 15:28:44.686476',3,1,1,NULL,'Нижнее меню','Создано автоматически, выводит нижнее меню','bottommenu',NULL,NULL),(4,NULL,'2020-12-07 00:28:45.999144','2020-12-07 00:28:45.999167',4,1,99,'','Простая статья','','simple_article','',''),(5,NULL,'2020-12-07 00:48:59.999904','2020-12-23 13:35:23.944181',5,1,3,'','О нас','','simple_article','',''),(6,NULL,'2020-12-07 01:00:27.198337','2020-12-07 12:50:43.601833',6,1,99,'','Портфолио','Portfolio<br>','portfolio','',''),(9,NULL,'2020-12-07 14:03:29.406452','2020-12-23 12:56:34.974722',7,1,3,'','Портфолио','Portfolio<br>','portfolio','',''),(10,NULL,'2020-12-07 14:16:15.097324','2020-12-07 14:20:11.016938',8,1,99,'','Услуги (простой вид)','Services','simple_services','',''),(11,NULL,'2020-12-07 15:13:04.139585','2020-12-23 12:56:07.897041',9,1,3,'','Услуги (простой вид)','Services','simple_services','',''),(12,NULL,'2020-12-07 15:16:56.665389','2020-12-23 12:43:22.117763',10,1,99,'','Команда','Our team<br>','team','',''),(13,NULL,'2020-12-07 16:54:06.378898','2020-12-23 12:54:39.337455',11,1,3,'','Команда','Our team<br>','team','',''),(14,NULL,'2020-12-07 17:08:43.487720','2020-12-07 17:39:39.643839',12,1,99,'','Партнеры (простой вид)','Partners','simple_clients','',''),(16,NULL,'2020-12-07 17:41:52.756306','2020-12-23 12:55:31.685218',13,1,3,'','Партнеры (простой вид)','Partners','simple_clients','','');
/*!40000 ALTER TABLE `flatcontent_containers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flatcontent_linkcontainer`
--

DROP TABLE IF EXISTS `flatcontent_linkcontainer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flatcontent_linkcontainer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `block_id` int NOT NULL,
  `container_id` int NOT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_linkcontainer`
--

LOCK TABLES `flatcontent_linkcontainer` WRITE;
/*!40000 ALTER TABLE `flatcontent_linkcontainer` DISABLE KEYS */;
INSERT INTO `flatcontent_linkcontainer` VALUES (33,NULL,'2020-12-23 11:34:37.711614','2020-12-23 11:34:37.711688',1,1,NULL,NULL,12,5),(34,NULL,'2020-12-23 11:34:37.727535','2020-12-23 11:34:37.727574',2,1,NULL,NULL,12,9),(35,NULL,'2020-12-23 11:34:37.731883','2020-12-23 11:34:37.731909',3,1,NULL,NULL,12,11),(36,NULL,'2020-12-23 11:34:37.736086','2020-12-23 11:34:37.736115',4,1,NULL,NULL,12,13),(37,NULL,'2020-12-23 11:34:37.740879','2020-12-23 11:34:37.740896',5,1,NULL,NULL,12,16);
/*!40000 ALTER TABLE `flatcontent_linkcontainer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `languages_translate`
--

DROP TABLE IF EXISTS `languages_translate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `languages_translate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `domain_pk` int DEFAULT NULL,
  `content_type` varchar(255) DEFAULT NULL,
  `model_pk` int DEFAULT NULL,
  `field` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `text` longtext,
  PRIMARY KEY (`id`),
  KEY `languages_translate_img_5c247240` (`img`),
  KEY `languages_translate_created_f2a8a297` (`created`),
  KEY `languages_translate_updated_065269f9` (`updated`),
  KEY `languages_translate_position_0fc25465` (`position`),
  KEY `languages_translate_is_active_a43b4adc` (`is_active`),
  KEY `languages_translate_state_f745c5ee` (`state`),
  KEY `languages_translate_parents_00269b5e` (`parents`),
  KEY `languages_translate_domain_pk_e2c587c0` (`domain_pk`),
  KEY `languages_translate_content_type_b462606c` (`content_type`),
  KEY `languages_translate_model_pk_5c02b243` (`model_pk`),
  KEY `languages_translate_field_20d39d18` (`field`),
  KEY `languages_translate_value_9cecbd36` (`value`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `languages_translate`
--

LOCK TABLES `languages_translate` WRITE;
/*!40000 ALTER TABLE `languages_translate` DISABLE KEYS */;
INSERT INTO `languages_translate` VALUES (1,NULL,'2020-12-21 13:59:26.363174','2020-12-21 13:59:26.363195',1,1,NULL,NULL,1,'flatcontent.blocks',32,'html','<div><b>Infinity Ink 带你走进无穷无尽的创意空间。</b></div><div>我们是一家专业的设计工作室，对普通事物 有着独到的看法。在这里，我们一起探索设 计的奥秘。助您拔类超群, 脱颖而出的设计!&nbsp;<br><br></div><div>自2015年以来，Infinity Ink 用优秀的设计 案例帮助客户解决各类需求。 <br><b>不夸大其词，只走成功之道。&nbsp;</b></div>',''),(2,NULL,'2020-12-21 14:05:17.530817','2020-12-21 14:05:17.530854',2,1,NULL,NULL,1,'flatcontent.blocks',12,'name','首页',''),(3,NULL,'2020-12-21 14:25:41.508956','2020-12-21 14:25:41.509036',3,1,NULL,NULL,1,'flatcontent.blocks',29,'name','我们的团队',''),(4,NULL,'2020-12-23 11:42:23.440266','2020-12-23 11:42:23.440301',4,1,NULL,NULL,1,'flatcontent.blocks',13,'name','设计案例',''),(5,NULL,'2020-12-23 11:43:45.817931','2020-12-23 11:43:45.817968',5,1,NULL,NULL,1,'flatcontent.blocks',14,'name','视觉',''),(6,NULL,'2020-12-23 11:49:02.892075','2020-12-23 11:49:02.892094',6,1,NULL,NULL,1,'flatcontent.blocks',15,'name','插图',''),(7,NULL,'2020-12-23 11:49:49.939493','2020-12-23 11:49:49.939535',7,1,NULL,NULL,1,'flatcontent.blocks',16,'name','玩具设计',''),(8,NULL,'2020-12-23 11:51:44.277698','2020-12-23 11:51:44.277765',8,1,NULL,NULL,1,'flatcontent.blocks',17,'name','工业设计',''),(9,NULL,'2020-12-23 11:55:06.927691','2020-12-23 11:55:06.927731',9,1,NULL,NULL,1,'flatcontent.blocks',196,'name','包装设计',''),(10,NULL,'2020-12-23 11:56:08.562212','2020-12-23 11:56:08.562258',10,1,NULL,NULL,1,'flatcontent.blocks',197,'name','网页设计',''),(11,NULL,'2020-12-23 11:56:58.094811','2020-12-23 11:56:58.094831',11,1,NULL,NULL,1,'flatcontent.blocks',18,'name','服务项目',''),(12,NULL,'2020-12-23 11:57:12.230110','2020-12-23 11:57:12.230139',12,1,NULL,NULL,1,'flatcontent.blocks',19,'name','设计申请表格',''),(13,NULL,'2020-12-23 11:57:26.531971','2020-12-23 11:57:26.532003',13,1,NULL,NULL,1,'flatcontent.blocks',20,'name','联系方式',''),(14,NULL,'2020-12-23 12:01:32.449767','2020-12-23 12:01:32.449793',14,1,NULL,NULL,1,'flatcontent.blocks',13,'description','我们的作品',''),(15,NULL,'2020-12-23 12:02:38.037019','2020-12-23 12:02:38.037048',15,1,NULL,NULL,1,'flatcontent.blocks',13,'html','如果有什么问题，请随时联系我们<br>',''),(16,NULL,'2020-12-23 12:12:31.686743','2020-12-23 12:12:31.686782',16,1,NULL,NULL,1,'flatcontent.blocks',155,'description','设计师 | 插画师 | 创意总监',''),(17,NULL,'2020-12-23 12:14:08.198589','2020-12-23 12:14:08.198613',17,1,NULL,NULL,1,'flatcontent.blocks',155,'html','','\r\n		\r\n	\r\n	\r\n		<div>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p><div>“在西班牙、中国和俄罗斯有9年以上的设计和国际艺术项目经验。我喜欢任何类型的设计，善于将原始思想与热情和奉献精神相结合。我有一个小诀窍，可以达到期望的效果 - 折衷主义，加上独到的见解以及我对工作的<span style=\"background-color: initial;\">热爱”。&nbsp;</span></div></p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n		</div>'),(18,NULL,'2020-12-23 12:15:05.867923','2020-12-23 12:15:05.867952',18,1,NULL,NULL,1,'flatcontent.blocks',156,'description','工业设计师 | 创意工程师',''),(19,NULL,'2020-12-23 12:18:09.656417','2020-12-23 12:18:09.656459',19,1,NULL,NULL,1,'flatcontent.blocks',156,'html','<div>\"我在设计方面的经验主要致力于工业产品（机器人，工业产品，玩具...）和数字产品（网站，移动应用程序）的研究。</div><div>我喜欢所有类型的任务，无论是项目的完整设计还是在项目开发过程中的特定阶段提供及时的支持\"。</div>',''),(20,NULL,'2020-12-23 12:20:38.574693','2020-12-23 12:20:38.574731',20,1,NULL,NULL,1,'flatcontent.blocks',157,'html','\"我有超过7年的国外设计项目管理经验。精通汉语、了解中华文化，独具审美能力，所以我可以为中国客户提供最佳服务。 擅长于印刷项目、工业分析、玩具设计、以及市场建立品牌方面。 让您的设计梦想成真，是我的使命\"。&nbsp;',''),(21,NULL,'2020-12-23 12:20:57.522004','2020-12-23 12:20:57.522034',21,1,NULL,NULL,1,'flatcontent.blocks',157,'description','项目管理 | 设计总监',''),(22,NULL,'2020-12-23 12:42:51.174959','2020-12-23 12:42:51.175007',22,1,NULL,NULL,1,'flatcontent.containers',12,'description','我们的团队<br>',''),(23,NULL,'2020-12-23 12:54:39.353425','2020-12-23 12:54:39.353466',23,1,NULL,NULL,1,'flatcontent.containers',13,'description','我们的团队',''),(24,NULL,'2020-12-23 12:55:31.693729','2020-12-23 12:55:31.693752',24,1,NULL,NULL,1,'flatcontent.containers',16,'description','合作伙伴',''),(25,NULL,'2020-12-23 12:56:07.907172','2020-12-23 12:56:07.907221',25,1,NULL,NULL,1,'flatcontent.containers',11,'description','服务项目',''),(26,NULL,'2020-12-23 12:56:34.988095','2020-12-23 12:56:34.988135',26,1,NULL,NULL,1,'flatcontent.containers',9,'description','设计案例',''),(27,NULL,'2020-12-23 12:58:23.231545','2020-12-23 12:58:23.231581',27,1,NULL,NULL,1,'flatcontent.blocks',146,'name','视觉',''),(28,NULL,'2020-12-23 13:04:01.276048','2020-12-23 13:04:01.276090',28,1,NULL,NULL,1,'flatcontent.blocks',146,'html','<div>视觉设计是一项复杂的任务，正确的方案能够促成品牌或公司良好的“脸面”。企业形象是企业与目标群通过视觉元素的互动与交流。<br><br>我们综合考虑企业风格色调、字体和图形在不同条件下&nbsp;<span style=\"background-color: initial;\">(室内和室外，光线明亮和昏暗)，以及在不同媒介(海报和小型名片等)上的外观效果。</span></div>',''),(29,NULL,'2020-12-23 13:06:18.603771','2020-12-23 13:06:18.603800',29,1,NULL,NULL,1,'flatcontent.blocks',147,'name','玩具设计',''),(30,NULL,'2020-12-23 13:06:18.610741','2020-12-23 13:06:18.610775',30,1,NULL,NULL,1,'flatcontent.blocks',147,'html','<div>我们将自己童年所学习到的知识，运用到玩具设计上，并做出新颖且具有教育意义的玩具。我们的玩具会让孩子以简单的游戏方式不停地学习开发自己的智力，寓教于乐!&nbsp;</div><div>我们认为，玩具应该为孩子们提供教育价值，同时为游戏带来乐趣。我们的团队是一些完全投身致力于玩具创造的人，尽管他们已经成人，但仍然保留那颗童心。我们每个人都试图体验游戏过程，并为其注入新鲜血液，带来一些我们认为有益的东西。</div>',''),(31,NULL,'2020-12-23 13:15:27.536303','2020-12-23 13:15:27.536329',31,1,NULL,NULL,1,'flatcontent.blocks',148,'name','插图',''),(32,NULL,'2020-12-23 13:15:27.541796','2020-12-23 13:15:27.541813',32,1,NULL,NULL,1,'flatcontent.blocks',148,'html','插图能使枯燥无味的商业文案和幻灯片变得生动形象。用明亮鲜艳的图像修饰广告和商品，令人印象深刻、过目不忘。当人们拿起书本、包装或玩具时，绝大多数人会先注意到插图，因为漂亮的视觉图像会激起人们强烈的情感反应。',''),(33,NULL,'2020-12-23 13:17:14.316150','2020-12-23 13:17:14.316184',33,1,NULL,NULL,1,'flatcontent.blocks',149,'name','工业设计',''),(34,NULL,'2020-12-23 13:17:14.323437','2020-12-23 13:17:14.323457',34,1,NULL,NULL,1,'flatcontent.blocks',149,'html','产品必须具有竞争力和吸引力。如何生产满足这些条件的产品呢? 产品设计、产品改进和商业成功离不开工业设计这一重要部分。在当今市场如果没有协调的、实用的设计，就意味着丧失了竞争力。我们为大众消费品、玩具和电子设备等产品提供最新、最切合实际的设计。',''),(35,NULL,'2020-12-23 13:20:17.209809','2020-12-23 13:20:17.209853',35,1,NULL,NULL,1,'flatcontent.blocks',150,'name','包装设计',''),(36,NULL,'2020-12-23 13:20:17.221980','2020-12-23 13:20:17.222014',36,1,NULL,NULL,1,'flatcontent.blocks',150,'html','当代市场的显著特征是竞争异常激烈。在这种市场情况下，仅仅依靠产品本身的优质是不够的。正确地向潜在消费者展示与介绍更为重要。一个令人过目不忘的包装设计有助于解决此问题。能给人留下深刻印象的产品包装设计会引起消费者的关注与兴趣，而有效的设计方案能促使消费者购买。',''),(37,NULL,'2020-12-23 13:22:44.941101','2020-12-23 13:22:44.941128',37,1,NULL,NULL,1,'flatcontent.blocks',151,'name','网页设计',''),(38,NULL,'2020-12-23 13:22:44.950732','2020-12-23 13:22:44.950752',38,1,NULL,NULL,1,'flatcontent.blocks',151,'html','<div>网络形象是当代世界中最重要的业务引擎。结构化的信息使您能够正确、顺利开展工作以吸引新客户，并维持与现有客户的稳定合作。</div><div>UI / UX、网站模板、网店、广告。</div>',''),(39,NULL,'2020-12-23 13:40:47.789081','2020-12-23 13:40:47.789104',39,1,NULL,NULL,1,'flatcontent.blocks',135,'name','插图',''),(40,NULL,'2020-12-23 13:41:56.851821','2020-12-23 13:41:56.851847',40,1,NULL,NULL,1,'flatcontent.blocks',146,'description','查看更多',''),(41,NULL,'2020-12-23 13:57:06.210385','2020-12-23 13:57:06.210431',41,1,NULL,NULL,1,'flatcontent.blocks',105,'name','视觉',''),(42,NULL,'2020-12-23 13:57:12.259932','2020-12-23 13:57:12.259950',42,1,NULL,NULL,1,'flatcontent.blocks',136,'name','玩具设计',''),(43,NULL,'2020-12-23 13:57:16.988886','2020-12-23 13:57:16.988908',43,1,NULL,NULL,1,'flatcontent.blocks',137,'name','工业设计',''),(44,NULL,'2020-12-23 13:57:23.540991','2020-12-23 13:57:23.541020',44,1,NULL,NULL,1,'flatcontent.blocks',138,'name','包装设计',''),(45,NULL,'2020-12-23 13:57:28.641379','2020-12-23 13:57:28.641400',45,1,NULL,NULL,1,'flatcontent.blocks',139,'name','网页设计',''),(46,NULL,'2020-12-23 13:59:27.104940','2020-12-23 13:59:27.104969',46,1,NULL,NULL,1,'flatcontent.blocks',3,'name','中国大陆',''),(47,NULL,'2020-12-23 13:59:27.109853','2020-12-23 13:59:27.109870',47,1,NULL,NULL,1,'flatcontent.blocks',3,'html','<div>上海市静安区华山路328号氪空间225室<div>邮编：200040;&nbsp;</div></div>',''),(48,NULL,'2020-12-23 14:09:51.418451','2020-12-23 14:09:51.418504',48,1,NULL,NULL,1,'flatcontent.blocks',191,'name','俄罗斯',''),(49,NULL,'2020-12-23 14:09:51.424833','2020-12-23 14:09:51.424862',49,1,NULL,NULL,1,'flatcontent.blocks',191,'html','叶卡捷琳堡市 32号冶金家街&nbsp;#42栋 <br>邮编: 620131',''),(50,NULL,'2020-12-23 14:19:15.692351','2020-12-23 14:19:15.692386',50,1,NULL,NULL,1,'flatcontent.blocks',147,'description','查看更多',''),(51,NULL,'2020-12-23 14:19:20.353485','2020-12-23 14:19:20.353512',51,1,NULL,NULL,1,'flatcontent.blocks',148,'description','查看更多',''),(52,NULL,'2020-12-23 14:19:24.679347','2020-12-23 14:19:24.679368',52,1,NULL,NULL,1,'flatcontent.blocks',149,'description','查看更多',''),(53,NULL,'2020-12-23 14:19:28.647459','2020-12-23 14:19:28.647485',53,1,NULL,NULL,1,'flatcontent.blocks',150,'description','查看更多',''),(54,NULL,'2020-12-23 14:19:32.847610','2020-12-23 14:19:32.847650',54,1,NULL,NULL,1,'flatcontent.blocks',151,'description','查看更多',''),(55,NULL,'2020-12-23 14:54:30.976751','2020-12-23 14:54:30.976778',55,1,NULL,NULL,1,'flatcontent.blocks',194,'html','您需要设计吗？<br>请简单的描述一下你要设计的<br>项目，我们会尽快与您联系。\r\n',''),(56,NULL,'2020-12-23 14:54:50.216100','2020-12-23 14:54:50.216140',56,1,NULL,NULL,1,'flatcontent.blocks',194,'name','设计申请表格','');
/*!40000 ALTER TABLE `languages_translate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_customuser`
--

DROP TABLE IF EXISTS `login_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_customuser` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `function` varchar(255) DEFAULT NULL,
  `user_id` int NOT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_customuser`
--

LOCK TABLES `login_customuser` WRITE;
/*!40000 ALTER TABLE `login_customuser` DISABLE KEYS */;
INSERT INTO `login_customuser` VALUES (1,NULL,'2020-12-06 15:05:34.542779','2020-12-21 14:23:27.228843',1,1,NULL,NULL,NULL,NULL,1),(2,NULL,'2020-12-07 01:22:55.520042','2020-12-23 11:31:23.723812',2,1,NULL,NULL,'','Видимо дирехтор',2);
/*!40000 ALTER TABLE `login_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_extrafields`
--

DROP TABLE IF EXISTS `login_extrafields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_extrafields` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `field` varchar(255) DEFAULT NULL,
  `show_in_table` tinyint(1) NOT NULL,
  `group_id` int DEFAULT NULL,
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_extrainfo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `value` varchar(255) DEFAULT NULL,
  `field_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_extravalues` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `field_id` int DEFAULT NULL,
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_functions_config` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `attr` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `img` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `position` int DEFAULT NULL,
  `state` int DEFAULT NULL,
  `updated` datetime(6) NOT NULL,
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
  KEY `main_functions_config_updated_b30da946` (`updated`)
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_functions_tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `command` longtext NOT NULL,
  `created` datetime(6) NOT NULL,
  `img` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `position` int DEFAULT NULL,
  `state` int DEFAULT NULL,
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-26 11:51:17
