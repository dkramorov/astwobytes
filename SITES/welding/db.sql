-- MySQL dump 10.13  Distrib 5.7.20, for osx10.11 (x86_64)
--
-- Host: localhost    Database: allstore
-- ------------------------------------------------------
-- Server version	5.7.20-log

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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add user',3,'add_user'),(10,'Can change user',3,'change_user'),(11,'Can delete user',3,'delete_user'),(12,'Can view user',3,'view_user'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Админка - Настрока',6,'add_config'),(22,'Can change Админка - Настрока',6,'change_config'),(23,'Can delete Админка - Настрока',6,'delete_config'),(24,'Can view Админка - Настрока',6,'view_config'),(25,'Can add Админка - Задача',7,'add_tasks'),(26,'Can change Админка - Задача',7,'change_tasks'),(27,'Can delete Админка - Задача',7,'delete_tasks'),(28,'Can view Админка - Задача',7,'view_tasks'),(29,'Can add custom user',8,'add_customuser'),(30,'Can change custom user',8,'change_customuser'),(31,'Can delete custom user',8,'delete_customuser'),(32,'Can view custom user',8,'view_customuser'),(33,'Can add Стат.контет - Файлы',9,'add_files'),(34,'Can change Стат.контет - Файлы',9,'change_files'),(35,'Can delete Стат.контет - Файлы',9,'delete_files'),(36,'Can view Стат.контет - Файлы',9,'view_files'),(37,'Can add Стат.контент - Блоки',10,'add_blocks'),(38,'Can change Стат.контент - Блоки',10,'change_blocks'),(39,'Can delete Стат.контент - Блоки',10,'delete_blocks'),(40,'Can view Стат.контент - Блоки',10,'view_blocks'),(41,'Can add Стат.контент - Контейнеры',11,'add_containers'),(42,'Can change Стат.контент - Контейнеры',11,'change_containers'),(43,'Can delete Стат.контент - Контейнеры',11,'delete_containers'),(44,'Can view Стат.контент - Контейнеры',11,'view_containers'),(45,'Can add Стат.контент - Линковка меню к контейнерам',12,'add_linkcontainer'),(46,'Can change Стат.контент - Линковка меню к контейнерам',12,'change_linkcontainer'),(47,'Can delete Стат.контент - Линковка меню к контейнерам',12,'delete_linkcontainer'),(48,'Can view Стат.контент - Линковка меню к контейнерам',12,'view_linkcontainer'),(49,'Can add Товары - товар/услуга',13,'add_products'),(50,'Can change Товары - товар/услуга',13,'change_products'),(51,'Can delete Товары - товар/услуга',13,'delete_products'),(52,'Can view Товары - товар/услуга',13,'view_products'),(53,'Can add products cats',14,'add_productscats'),(54,'Can change products cats',14,'change_productscats'),(55,'Can delete products cats',14,'delete_productscats'),(56,'Can view products cats',14,'view_productscats'),(57,'Can add products photos',15,'add_productsphotos'),(58,'Can change products photos',15,'change_productsphotos'),(59,'Can delete products photos',15,'delete_productsphotos'),(60,'Can view products photos',15,'view_productsphotos'),(61,'Can add property',16,'add_property'),(62,'Can change property',16,'change_property'),(63,'Can delete property',16,'delete_property'),(64,'Can view property',16,'view_property'),(65,'Can add properties values',17,'add_propertiesvalues'),(66,'Can change properties values',17,'change_propertiesvalues'),(67,'Can delete properties values',17,'delete_propertiesvalues'),(68,'Can view properties values',17,'view_propertiesvalues'),(69,'Can add products properties',18,'add_productsproperties'),(70,'Can change products properties',18,'change_productsproperties'),(71,'Can delete products properties',18,'delete_productsproperties'),(72,'Can view products properties',18,'view_productsproperties'),(73,'Can add Promotion - семантический словарь',19,'add_vocabulary'),(74,'Can change Promotion - семантический словарь',19,'change_vocabulary'),(75,'Can delete Promotion - семантический словарь',19,'delete_vocabulary'),(76,'Can view Promotion - семантический словарь',19,'view_vocabulary'),(77,'Can add Promotion - посещение сайта',20,'add_svisits'),(78,'Can change Promotion - посещение сайта',20,'change_svisits'),(79,'Can delete Promotion - посещение сайта',20,'delete_svisits'),(80,'Can view Promotion - посещение сайта',20,'view_svisits');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$JF2BzhsxIn48$+WhVDGZtLBCbP06Mbz4WtNu9D2MDTAM1fCOdKytNbjo=','2020-05-08 17:47:40.944562',1,'jocker','','','dkramorov@mail.ru',1,1,'2020-05-04 16:51:55.788140');
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(9,'files','files'),(10,'flatcontent','blocks'),(11,'flatcontent','containers'),(12,'flatcontent','linkcontainer'),(8,'login','customuser'),(6,'main_functions','config'),(7,'main_functions','tasks'),(13,'products','products'),(14,'products','productscats'),(15,'products','productsphotos'),(18,'products','productsproperties'),(17,'products','propertiesvalues'),(16,'products','property'),(20,'promotion','svisits'),(19,'promotion','vocabulary'),(5,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-05-04 16:51:53.294521'),(2,'contenttypes','0002_remove_content_type_name','2020-05-04 16:51:53.319164'),(3,'auth','0001_initial','2020-05-04 16:51:54.189194'),(4,'auth','0002_alter_permission_name_max_length','2020-05-04 16:51:54.300700'),(5,'auth','0003_alter_user_email_max_length','2020-05-04 16:51:54.316368'),(6,'auth','0004_alter_user_username_opts','2020-05-04 16:51:54.325088'),(7,'auth','0005_alter_user_last_login_null','2020-05-04 16:51:54.339940'),(8,'auth','0006_require_contenttypes_0002','2020-05-04 16:51:54.341462'),(9,'auth','0007_alter_validators_add_error_messages','2020-05-04 16:51:54.351329'),(10,'auth','0008_alter_user_username_max_length','2020-05-04 16:51:54.370561'),(11,'auth','0009_alter_user_last_name_max_length','2020-05-04 16:51:54.384232'),(12,'auth','0010_alter_group_name_max_length','2020-05-04 16:51:54.398888'),(13,'auth','0011_update_proxy_permissions','2020-05-04 16:51:54.406709'),(14,'files','0001_initial','2020-05-04 16:51:54.560178'),(15,'files','0002_auto_20191203_2054','2020-05-04 16:51:54.681807'),(16,'files','0003_auto_20200112_1717','2020-05-04 16:51:54.689811'),(17,'files','0004_auto_20200402_2127','2020-05-04 16:51:54.704226'),(18,'flatcontent','0001_initial','2020-05-04 16:51:55.271968'),(19,'flatcontent','0002_auto_20190825_1730','2020-05-04 16:51:55.569802'),(20,'flatcontent','0003_auto_20191203_2054','2020-05-04 16:51:55.604736'),(21,'flatcontent','0004_blocks_html','2020-05-04 16:51:55.627570'),(22,'flatcontent','0005_auto_20200112_1717','2020-05-04 16:51:55.657489'),(23,'flatcontent','0006_auto_20200314_1638','2020-05-04 16:51:55.662848'),(24,'flatcontent','0007_auto_20200402_2127','2020-05-04 16:51:55.730125'),(25,'login','0001_customuser','2020-05-04 16:51:56.046381'),(26,'main_functions','0001_initial','2020-05-04 16:51:56.397682'),(27,'main_functions','0002_auto_20191203_2052','2020-05-04 16:51:56.419374'),(28,'main_functions','0003_auto_20200407_1845','2020-05-04 16:51:56.729029'),(29,'products','0001_initial','2020-05-04 16:51:56.894149'),(30,'products','0002_productsphotos','2020-05-04 16:51:57.036229'),(31,'products','0003_auto_20200315_2217','2020-05-04 16:51:57.113947'),(32,'products','0004_auto_20200316_2329','2020-05-04 16:51:57.161130'),(33,'products','0005_auto_20200402_2127','2020-05-04 16:51:57.289323'),(34,'products','0006_auto_20200402_2351','2020-05-04 16:51:57.423841'),(35,'products','0007_property_ptype','2020-05-04 16:51:57.445701'),(36,'products','0008_property_code','2020-05-04 16:51:57.467171'),(37,'sessions','0001_initial','2020-05-04 16:51:57.634595'),(38,'promotion','0001_initial','2020-05-06 13:54:49.595913'),(39,'login','0002_auto_20200506_1354','2020-05-06 13:54:58.265209'),(40,'promotion','0002_svisits','2020-05-06 13:54:58.322609'),(41,'promotion','0003_svisits_ip','2020-05-06 15:37:23.827777'),(42,'products','0009_property_measure','2020-05-07 09:36:37.283203');
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
INSERT INTO `django_session` VALUES ('hjpo85r4duagxmuy62tsozti02q787q1','Mzk5MWFjYmVmMWQ5NmVhNDkyNzIyMTQ4Y2Y0NjU2ZTQ0Y2NlYjAzZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjA0ZjRhZTgyMzVmYTA0N2MyY2E1OTMwZmJkMjVlYWQ0MGU0ZjliMjMifQ==','2020-05-21 09:09:32.163742'),('lgzx4az278lxo6ubkiaj6zpa39s0wiu4','Mzk5MWFjYmVmMWQ5NmVhNDkyNzIyMTQ4Y2Y0NjU2ZTQ0Y2NlYjAzZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjA0ZjRhZTgyMzVmYTA0N2MyY2E1OTMwZmJkMjVlYWQ0MGU0ZjliMjMifQ==','2020-05-18 16:52:08.156935'),('m1yoxlvyrd6gef8g88a7el1r9kbnj4bk','Mzk5MWFjYmVmMWQ5NmVhNDkyNzIyMTQ4Y2Y0NjU2ZTQ0Y2NlYjAzZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjA0ZjRhZTgyMzVmYTA0N2MyY2E1OTMwZmJkMjVlYWQ0MGU0ZjliMjMifQ==','2020-05-20 13:50:43.356859'),('syhukne4by24nv2mvuc4i2vhkb6vnt6w','Mzk5MWFjYmVmMWQ5NmVhNDkyNzIyMTQ4Y2Y0NjU2ZTQ0Y2NlYjAzZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjA0ZjRhZTgyMzVmYTA0N2MyY2E1OTMwZmJkMjVlYWQ0MGU0ZjliMjMifQ==','2020-05-22 17:47:40.982895');
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
  CONSTRAINT `flatcontent_blocks_container_id_5864baa1_fk_flatconte` FOREIGN KEY (`container_id`) REFERENCES `flatcontent_containers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=273 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
INSERT INTO `flatcontent_blocks` VALUES (10,NULL,'2020-05-04 20:14:44.578227','2020-05-04 20:14:44.578254',1,1,3,'','Телефон',NULL,'tel:73952123321','phone',3,0,NULL,NULL,NULL,'+7(3952) 123-321'),(11,NULL,'2020-05-04 20:14:44.581169','2020-05-04 20:14:44.581192',2,1,3,'','Адрес',NULL,NULL,'address',3,0,NULL,NULL,NULL,'г. Иркутск ул. Советская 32а офис 5'),(12,NULL,'2020-05-04 20:14:44.584684','2020-05-04 20:14:44.584726',3,1,3,'','Сообщества',NULL,NULL,'social',3,0,NULL,NULL,NULL,NULL),(13,NULL,'2020-05-04 20:14:44.587917','2020-05-04 20:14:44.587938',4,1,3,'_12','instagram',NULL,NULL,'instagram',3,1,'instagram',NULL,NULL,NULL),(14,NULL,'2020-05-04 20:14:44.597536','2020-05-04 20:14:44.597562',5,1,3,'_12','vk',NULL,NULL,'vk',3,1,'vk',NULL,NULL,NULL),(15,NULL,'2020-05-04 20:14:44.600630','2020-05-04 20:14:44.600662',6,1,3,'_12','facebook',NULL,NULL,'facebook',3,1,'facebook',NULL,NULL,NULL),(16,NULL,'2020-05-04 20:14:44.603769','2020-05-04 20:14:44.603792',7,1,3,'_12','twitter',NULL,NULL,'twitter',3,1,'twitter',NULL,NULL,NULL),(17,NULL,'2020-05-04 20:18:49.923367','2020-05-04 20:18:49.923403',4,1,3,'','Email',NULL,NULL,'email',3,0,NULL,NULL,NULL,'test@test.ru'),(18,NULL,'2020-05-04 20:18:49.938005','2020-05-04 20:18:49.938034',5,1,3,'','Режим работы',NULL,NULL,'worktime',3,0,NULL,NULL,NULL,'пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 17:00'),(19,'2_Disney_400.png','2020-05-05 11:36:59.072589','2020-05-07 23:41:36.656072',6,1,1,'','Логотип','Добро пожаловать, на наш сайт','/','logo',3,0,'','','','Мы работаем для вас<br>'),(113,NULL,'2020-05-05 12:30:09.939921','2020-05-07 23:32:25.295075',80,1,4,'','Главная','','/','_mainmenu_mainpage',9,0,'','','',''),(114,NULL,'2020-05-05 12:30:09.943864','2020-05-05 12:30:09.943890',81,1,4,'','Каталог',NULL,'/cat/','_mainmenu_catpage',9,0,NULL,NULL,NULL,NULL),(115,NULL,'2020-05-05 12:30:09.947635','2020-05-05 12:30:09.947655',82,1,4,'_114','Популярные товары',NULL,'/cat/populyarnye-tovary/','_mainmenu_catpage_popular',9,0,NULL,NULL,NULL,NULL),(116,NULL,'2020-05-05 12:30:09.951023','2020-05-05 12:30:09.951043',83,1,4,'_114','Новые товары',NULL,'/cat/novye-tovary/','_mainmenu_catpage_new',9,0,NULL,NULL,NULL,NULL),(117,NULL,'2020-05-05 12:30:09.954694','2020-05-05 12:30:09.954714',84,1,4,'_114','Товары со скидкой',NULL,'/cat/tovary-so-skidkoy/','_mainmenu_catpage_discount',9,0,NULL,NULL,NULL,NULL),(118,NULL,'2020-05-05 12:30:09.958338','2020-05-05 12:30:09.958359',85,1,4,'_114','Распродажа',NULL,'/cat/rasprodaja/','_mainmenu_catpage_sale',9,0,NULL,NULL,NULL,NULL),(119,NULL,'2020-05-05 12:30:09.961255','2020-05-05 12:30:09.961280',86,1,4,'','О нас',NULL,'/about/','_mainmenu_aboutpage',9,0,NULL,NULL,NULL,NULL),(120,NULL,'2020-05-05 12:30:09.964139','2020-05-05 12:30:09.964170',87,1,4,'','Услуги',NULL,'/services/','_mainmenu_servicespage',9,0,NULL,NULL,NULL,NULL),(121,NULL,'2020-05-05 12:30:09.967054','2020-05-05 12:30:09.967076',88,1,4,'','Контакты',NULL,'/feedback/','_mainmenu_feedbackpage',9,0,NULL,NULL,NULL,NULL),(122,NULL,'2020-05-05 12:30:09.970117','2020-05-05 12:30:09.970140',89,1,4,'','Каталог',NULL,'/cat/','_bottommenu_catpage',10,0,NULL,NULL,NULL,NULL),(123,NULL,'2020-05-05 12:30:09.973928','2020-05-05 12:30:09.973953',90,1,4,'_122','Популярные товары',NULL,'/cat/populyarnye-tovary/','_bottommenu_catpage_popular',10,0,NULL,NULL,NULL,NULL),(124,NULL,'2020-05-05 12:30:09.977755','2020-05-05 12:30:09.977777',91,1,4,'_122','Новые товары',NULL,'/cat/novye-tovary/','_bottommenu_catpage_new',10,0,NULL,NULL,NULL,NULL),(125,NULL,'2020-05-05 12:30:09.981454','2020-05-05 12:30:09.981479',92,1,4,'_122','Товары со скидкой',NULL,'/cat/tovary-so-skidkoy/','_bottommenu_catpage_discount',10,0,NULL,NULL,NULL,NULL),(126,NULL,'2020-05-05 12:30:09.985171','2020-05-05 12:30:09.985194',93,1,4,'_122','Распродажа',NULL,'/cat/rasprodaja/','_bottommenu_catpage_sale',10,0,NULL,NULL,NULL,NULL),(127,NULL,'2020-05-05 12:30:09.988416','2020-05-08 00:01:53.676655',94,1,4,'','Информация','','/informaciya/','',10,0,'','','',''),(128,NULL,'2020-05-05 12:30:09.991641','2020-05-08 00:03:33.719935',95,1,4,'','Статьи',NULL,'/services/','_bottommenu_servicespage',10,0,NULL,NULL,NULL,NULL),(129,NULL,'2020-05-05 12:30:09.994653','2020-05-08 00:04:43.629096',96,1,4,'','Сотрудничество',NULL,'/feedback/','_bottommenu_feedbackpage',10,0,NULL,NULL,NULL,NULL),(130,'130.jpg','2020-05-05 13:29:48.709129','2020-05-05 13:34:02.606597',97,1,1,'','Скидки на товары до 90%','','/','',11,0,'','','','Сделайте покупку на 10 000 рублей до конца сезона, чтобы получить скидку до 90% на последующие покупки<br>'),(131,'131.jpg','2020-05-05 13:29:56.129088','2020-05-05 13:33:55.520348',98,1,1,'','Выгодное предложение','','/','',11,0,'','','','Приобретая комплект, вы получаете дополнительную гарантию на 3 года и скидку на следующую покупку до 50%<br>'),(132,'132.jpg','2020-05-05 13:30:02.406932','2020-05-05 13:34:05.676302',99,1,1,'','2 по цене 1','','/','',11,0,'','','','Покупая акционные товары вы получите второй товар бесплатно, спешите успеть совершить покупку до конца сезона<br>'),(133,'130.jpg','2020-05-05 13:34:19.440749','2020-05-05 13:34:19.440770',97,1,1,'','Скидки на товары до 90%','','/','',12,0,'','','','Сделайте покупку на 10 000 рублей до конца сезона, чтобы получить скидку до 90% на последующие покупки<br>'),(134,'131.jpg','2020-05-05 13:34:19.442255','2020-05-05 13:34:19.442274',98,1,1,'','Выгодное предложение','','/','',12,0,'','','','Приобретая комплект, вы получаете дополнительную гарантию на 3 года и скидку на следующую покупку до 50%<br>'),(135,'132.jpg','2020-05-05 13:34:19.449176','2020-05-05 13:34:19.449198',99,1,1,'','2 по цене 1','','/','',12,0,'','','','Покупая акционные товары вы получите второй товар бесплатно, спешите успеть совершить покупку до конца сезона<br>'),(136,NULL,'2020-05-07 18:39:17.438061','2020-05-10 15:52:42.297902',100,1,1,'','Популярные','','','',13,0,'','','',''),(137,NULL,'2020-05-07 18:39:23.314116','2020-05-10 15:52:53.407413',101,1,1,'','Скидки','','','',13,0,'','','',''),(138,NULL,'2020-05-07 18:39:28.515049','2020-05-10 15:53:05.698873',102,1,1,'','Выгодное предложение','','','',13,0,'','','',''),(139,NULL,'2020-05-07 19:03:03.660929','2020-05-10 15:58:25.740905',100,1,1,'','Популярные','','','',14,0,'','','',''),(140,NULL,'2020-05-07 19:03:03.667223','2020-05-10 15:58:07.565967',101,1,1,'','Скидки','','','',14,0,'','','',''),(141,NULL,'2020-05-07 19:03:03.673004','2020-05-10 15:58:15.886409',102,1,1,'','Выгодное предложение','','','',14,0,'','','',''),(142,'1.jpg','2020-05-07 21:15:39.609730','2020-05-07 21:27:12.284355',103,1,1,'','Акции для вас','до конца сезона','','style_11',15,0,'','','','выгодное предложение<br>'),(143,'2.jpg','2020-05-07 21:15:40.981061','2020-05-07 21:23:04.260717',104,1,1,'','Компактно и выгодно','','','style_22',15,0,'','','','На выбор оригинал или аналоги<br>'),(144,'3.jpg','2020-05-07 21:15:42.115736','2020-05-07 21:23:11.529724',105,1,1,'','Быстро и эффективно','','','style_21',15,0,'','','','Удобная и быстрая доставка<br>'),(145,'4.jpg','2020-05-07 21:15:43.175729','2020-05-07 21:23:18.086740',106,1,1,'','Большой ассортимент','','','style_21',15,0,'','','','Большой выбор предложений<br>'),(146,'5.jpg','2020-05-07 21:15:44.220764','2020-05-07 21:23:25.240651',107,1,1,'','Умный выбор','','','style_22',15,0,'','','','Лояльная политика возврата<br>'),(147,'6.jpg','2020-05-07 21:15:46.404457','2020-05-07 21:23:30.924830',108,1,1,'','Специальное предложение','Предложение ограничено','','style_12',15,0,'','','','В подарок вы получаете скидочную карту<br>'),(148,'1.jpg','2020-05-07 21:27:29.465362','2020-05-07 21:27:29.465387',103,1,1,'','Акции для вас','до конца сезона','','style_11',16,0,'','','','выгодное предложение<br>'),(149,'2.jpg','2020-05-07 21:27:29.467035','2020-05-07 21:27:29.467059',104,1,1,'','Компактно и выгодно','','','style_22',16,0,'','','','На выбор оригинал или аналоги<br>'),(150,'3.jpg','2020-05-07 21:27:29.479564','2020-05-07 21:27:29.479587',105,1,1,'','Быстро и эффективно','','','style_21',16,0,'','','','Удобная и быстрая доставка<br>'),(151,'4.jpg','2020-05-07 21:27:29.486696','2020-05-07 21:27:29.486717',106,1,1,'','Большой ассортимент','','','style_21',16,0,'','','','Большой выбор предложений<br>'),(152,'5.jpg','2020-05-07 21:27:29.493754','2020-05-07 21:27:29.493775',107,1,1,'','Умный выбор','','','style_22',16,0,'','','','Лояльная политика возврата<br>'),(153,'6.jpg','2020-05-07 21:27:29.501446','2020-05-07 21:27:29.501483',108,1,1,'','Специальное предложение','Предложение ограничено','','style_12',16,0,'','','','В подарок вы получаете скидочную карту<br>'),(154,NULL,'2020-05-07 21:36:11.560998','2020-05-07 21:38:34.826901',109,1,1,'','Специальное предложение','','','',17,0,'','','','<p>Подарочная карта за покупку<br> на сумму более 5 000 ₽<br></p>'),(155,NULL,'2020-05-07 21:40:58.608141','2020-05-07 21:40:58.608165',109,1,1,'','Специальное предложение','','','',18,0,'','','','<p>Подарочная карта за покупку<br> на сумму более 5 000 ₽<br></p>'),(156,'blog1.jpg','2020-05-07 23:17:05.941197','2020-05-07 23:17:55.326823',110,1,1,'','Программы лояльности','','','',19,0,'','','',''),(157,'blog2.jpg','2020-05-07 23:17:13.687096','2020-05-07 23:18:02.977191',111,1,1,'','Сертификация','','','',19,0,'','','',''),(158,'blog3.jpg','2020-05-07 23:17:35.137618','2020-05-07 23:18:11.464595',112,1,1,'','Доставка транспортной компанией','','','',19,0,'','','',''),(159,'blog1.jpg','2020-05-07 23:19:45.786562','2020-05-07 23:19:45.786597',110,1,1,'','Программы лояльности','','','',20,0,'','','',''),(160,'blog2.jpg','2020-05-07 23:19:45.788222','2020-05-07 23:19:45.788243',111,1,1,'','Сертификация','','','',20,0,'','','',''),(161,'blog3.jpg','2020-05-07 23:19:45.794976','2020-05-07 23:19:45.794998',112,1,1,'','Доставка транспортной компанией','','','',20,0,'','','',''),(162,'1.jpg','2020-05-07 23:22:43.049168','2020-05-07 23:31:22.975293',113,1,1,'','Ирина Макарова','Покупатель','','',21,0,'','','','Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. '),(163,'2.jpg','2020-05-07 23:22:48.546671','2020-05-07 23:31:26.534812',114,1,1,'','Илья Герасимов','Покупатель','','',21,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(164,'5.jpg','2020-05-07 23:22:55.216651','2020-05-07 23:31:29.760032',115,1,1,'','Виталий Шахнов','Покупатель','','',21,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(165,'3.jpg','2020-05-07 23:23:11.383869','2020-05-07 23:31:33.340398',116,1,1,'','Маргарита Ильина','Покупатель','','',21,0,'','','','Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. '),(166,'4.jpg','2020-05-07 23:23:18.928739','2020-05-07 23:31:37.139801',117,1,1,'','Раиса Микина','Покупатель','','',21,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(167,'9.jpg','2020-05-07 23:23:29.385938','2020-05-07 23:31:40.470194',118,1,1,'','Наталья Ковальчук','Покупатель','','',21,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(168,'6.jpg','2020-05-07 23:23:38.880146','2020-05-07 23:31:43.665040',119,1,1,'','Борис Нектаров','Покупатель','','',21,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(169,'7.jpg','2020-05-07 23:23:48.361938','2020-05-07 23:31:47.128636',120,1,1,'','Данил Липин','Покупатель','','',21,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(170,'11.jpg','2020-05-07 23:24:02.491488','2020-05-07 23:31:49.818328',121,1,1,'','Вероника Каримова','Покупатель','','',21,0,'','','','Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. '),(171,'8.jpg','2020-05-07 23:24:11.744164','2020-05-07 23:31:52.777238',122,1,1,'','Максим Вуткин','Покупатель','','',21,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(172,'1.jpg','2020-05-07 23:32:10.802870','2020-05-07 23:32:10.802895',113,1,1,'','Ирина Макарова','Покупатель','','',22,0,'','','','Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. '),(173,'2.jpg','2020-05-07 23:32:10.804661','2020-05-07 23:32:10.804739',114,1,1,'','Илья Герасимов','Покупатель','','',22,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(174,'5.jpg','2020-05-07 23:32:10.811884','2020-05-07 23:32:10.811908',115,1,1,'','Виталий Шахнов','Покупатель','','',22,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(175,'3.jpg','2020-05-07 23:32:10.819097','2020-05-07 23:32:10.819120',116,1,1,'','Маргарита Ильина','Покупатель','','',22,0,'','','','Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. '),(176,'4.jpg','2020-05-07 23:32:10.826435','2020-05-07 23:32:10.826462',117,1,1,'','Раиса Микина','Покупатель','','',22,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(177,'9.jpg','2020-05-07 23:32:10.833814','2020-05-07 23:32:10.833836',118,1,1,'','Наталья Ковальчук','Покупатель','','',22,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(178,'6.jpg','2020-05-07 23:32:10.841004','2020-05-07 23:32:10.841028',119,1,1,'','Борис Нектаров','Покупатель','','',22,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(179,'7.jpg','2020-05-07 23:32:10.848218','2020-05-07 23:32:10.848242',120,1,1,'','Данил Липин','Покупатель','','',22,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(180,'11.jpg','2020-05-07 23:32:10.854996','2020-05-07 23:32:10.855019',121,1,1,'','Вероника Каримова','Покупатель','','',22,0,'','','','Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. '),(181,'8.jpg','2020-05-07 23:32:10.862416','2020-05-07 23:32:10.862438',122,1,1,'','Максим Вуткин','Покупатель','','',22,0,'','','','<p>Отличная компания, буду рекомендовать пользоваться услугами своим \r\nзнакомым, сервис хороший, доставка быстрая, при возникновении вопросов \r\nнезамедлительно менеджер приходит на помощь, все очень понравилось. </p>'),(182,NULL,'2020-05-07 23:42:34.876546','2020-05-07 23:44:06.336974',7,1,1,'','Полезное','','','useful',3,0,'','','',''),(183,'1.jpg','2020-05-07 23:42:44.555712','2020-05-07 23:52:34.861842',2,1,1,'_182','О нас','','','',3,0,'fa-info-circle','','','<p>Немного информации о нашей компании</p>'),(184,'2.jpg','2020-05-07 23:42:51.610645','2020-05-07 23:52:39.980163',3,1,1,'_182','Задать вопрос','','','',3,0,'fa-phone','','','<p>Задайте вопрос и мы на него ответим</p>'),(185,'3.jpg','2020-05-07 23:43:04.942075','2020-05-07 23:52:44.738384',4,1,1,'_182','Видео','','','',3,0,'fa-play-circle','','','<p>Ознакомьтесь с нашей деятельностью в видеообращении</p>'),(186,'4.jpg','2020-05-07 23:43:15.437575','2020-05-07 23:52:50.296930',5,1,1,'_182','Наш адрес','','','',3,0,'fa-map-marker','','','<p>Решили посетить наш магазин?</p>'),(187,'map.png','2020-05-07 23:43:29.950960','2020-05-07 23:57:11.108995',128,1,1,'','Карта','','','mapa',3,0,'','','','<p>Зоны нашей доставки</p>'),(188,NULL,'2020-05-08 00:02:17.702124','2020-05-08 00:02:17.702144',129,1,4,'_127','Как оформить заказ',NULL,'/informaciya/kak-oformit-zakaz/',NULL,10,0,NULL,NULL,NULL,NULL),(189,NULL,'2020-05-08 00:02:23.342531','2020-05-08 00:02:23.342552',130,1,4,'_127','Политика возврата',NULL,'/informaciya/politika-vozvrata/',NULL,10,0,NULL,NULL,NULL,NULL),(190,NULL,'2020-05-08 00:02:39.184129','2020-05-08 00:02:39.184151',131,1,4,'_127','Доставка',NULL,'/informaciya/dostavka/',NULL,10,0,NULL,NULL,NULL,NULL),(191,NULL,'2020-05-08 00:02:43.773295','2020-05-08 00:02:43.773316',132,1,4,'_127','Реквизиты',NULL,'/informaciya/rekvizity/',NULL,10,0,NULL,NULL,NULL,NULL),(192,NULL,'2020-05-08 00:03:38.651249','2020-05-08 00:03:38.651271',133,1,4,'_128','Как выбрать масло',NULL,'/services/kak-vybrat-maslo/',NULL,10,0,NULL,NULL,NULL,NULL),(193,NULL,'2020-05-08 00:03:43.870769','2020-05-08 00:03:43.870790',134,1,4,'_128','Как выбрать свечи',NULL,'/services/kak-vybrat-svechi/',NULL,10,0,NULL,NULL,NULL,NULL),(194,NULL,'2020-05-08 00:03:51.576762','2020-05-08 00:03:51.576786',135,1,4,'_128','Как выбрать ГРМ',NULL,'/services/kak-vybrat-grm/',NULL,10,0,NULL,NULL,NULL,NULL),(195,NULL,'2020-05-08 00:04:14.650153','2020-05-08 00:04:14.650175',136,1,4,'_128','Как выбрать аммортизаторы',NULL,'/services/kak-vybrat-ammortizatory/',NULL,10,0,NULL,NULL,NULL,NULL),(196,NULL,'2020-05-08 00:04:22.123996','2020-05-08 00:04:47.579248',137,1,4,'_129','Вакансии',NULL,'/feedback/bez-nazvaniya/',NULL,10,0,NULL,NULL,NULL,NULL),(198,NULL,'2020-05-08 00:04:55.715205','2020-05-08 00:04:55.715226',138,1,4,'_129','Партнерская программа',NULL,'/feedback/partnerskaya-programma/',NULL,10,0,NULL,NULL,NULL,NULL),(199,NULL,'2020-05-08 00:05:29.722860','2020-05-08 00:05:29.722881',139,1,4,'_129','Анкета партнера',NULL,'/feedback/anketa-partnera/',NULL,10,0,NULL,NULL,NULL,NULL),(200,NULL,'2020-05-08 00:09:53.097024','2020-05-08 00:09:53.097059',140,1,3,'','Copyright',NULL,NULL,'copyright',3,0,NULL,NULL,NULL,'<p>&copy; 2020 Все права защищены</p>'),(201,NULL,'2020-05-08 00:09:53.136227','2020-05-08 00:09:53.136256',141,1,4,'','О нас',NULL,'/about/','_bottommenu_aboutpage',10,0,NULL,NULL,NULL,NULL),(204,NULL,'2020-05-10 15:51:50.342645','2020-05-10 15:51:50.342677',142,1,4,'','Защита и гигиена',NULL,'/cat/zashhita-i-gigiena/','_cat_90',25,0,NULL,NULL,NULL,NULL),(205,NULL,'2020-05-10 15:51:50.354634','2020-05-10 15:51:50.354658',143,1,4,'','Оригинальные аксессуары',NULL,'/cat/originalnye-aksessuary/','_cat_76',25,0,NULL,NULL,NULL,NULL),(206,NULL,'2020-05-10 15:51:50.357547','2020-05-10 15:51:50.357571',144,1,4,'','Автосервис',NULL,'/cat/avtoservis/','_cat_65',25,0,NULL,NULL,NULL,NULL),(207,NULL,'2020-05-10 15:51:50.360544','2020-05-10 15:51:50.360569',145,1,4,'','Масла',NULL,'/cat/masla/','_cat_7',25,0,NULL,NULL,NULL,NULL),(208,NULL,'2020-05-10 15:51:50.365629','2020-05-10 15:51:50.365655',146,1,4,'_207','Масла моторные',NULL,'/cat/masla/masla-motornye/','_cat_9',25,0,NULL,NULL,NULL,NULL),(209,NULL,'2020-05-10 15:51:50.369413','2020-05-10 15:51:50.369436',147,1,4,'_207','Масла трансмиссионные и ГУР',NULL,'/cat/masla/masla-transmissionnye-i-gur/','_cat_10',25,0,NULL,NULL,NULL,NULL),(210,NULL,'2020-05-10 15:51:50.380143','2020-05-10 15:51:50.380166',148,1,4,'_207','Масла индустриальные',NULL,'/cat/masla/masla-industrialnye/','_cat_8',25,0,NULL,NULL,NULL,NULL),(211,NULL,'2020-05-10 15:51:50.383072','2020-05-10 15:51:50.383093',149,1,4,'','Жидкости',NULL,'/cat/jidkosti/','_cat_77',25,0,NULL,NULL,NULL,NULL),(212,NULL,'2020-05-10 15:51:50.387735','2020-05-10 15:51:50.387757',150,1,4,'_211','Жидкости гидравлические',NULL,'/cat/jidkosti/jidkosti-gidravlicheskie/','_cat_81',25,0,NULL,NULL,NULL,NULL),(213,NULL,'2020-05-10 15:51:50.391546','2020-05-10 15:51:50.391568',151,1,4,'_211','Жидкости амортизаторные',NULL,'/cat/jidkosti/jidkosti-amortizatornye/','_cat_75',25,0,NULL,NULL,NULL,NULL),(214,NULL,'2020-05-10 15:51:50.395146','2020-05-10 15:51:50.395168',152,1,4,'_211','Жидкости для омывателя стекла',NULL,'/cat/jidkosti/jidkosti-dlya-omyvatelya-stekla/','_cat_46',25,0,NULL,NULL,NULL,NULL),(215,NULL,'2020-05-10 15:51:50.398791','2020-05-10 15:51:50.398813',153,1,4,'_211','Жидкости охлаждающие',NULL,'/cat/jidkosti/jidkosti-ohlajdayushhie/','_cat_21',25,0,NULL,NULL,NULL,NULL),(216,NULL,'2020-05-10 15:51:50.402423','2020-05-10 15:51:50.402446',154,1,4,'_211','Жидкости тормозные',NULL,'/cat/jidkosti/jidkosti-tormoznye/','_cat_22',25,0,NULL,NULL,NULL,NULL),(217,NULL,'2020-05-10 15:51:50.406451','2020-05-10 15:51:50.406474',155,1,4,'_211','Жидкости ГУР',NULL,'/cat/jidkosti/jidkosti-gur/','_cat_83',25,0,NULL,NULL,NULL,NULL),(218,NULL,'2020-05-10 15:51:50.409365','2020-05-10 15:51:50.409387',156,1,4,'','Автохимия',NULL,'/cat/avtohimiya/','_cat_78',25,0,NULL,NULL,NULL,NULL),(219,NULL,'2020-05-10 15:51:50.414117','2020-05-10 15:51:50.414139',157,1,4,'_218','Автохимия',NULL,'/cat/avtohimiya/avtohimiya/','_cat_26',25,0,NULL,NULL,NULL,NULL),(220,NULL,'2020-05-10 15:51:50.417731','2020-05-10 15:51:50.417753',158,1,4,'_218','Автокосметика',NULL,'/cat/avtohimiya/avtokosmetika/','_cat_24',25,0,NULL,NULL,NULL,NULL),(221,NULL,'2020-05-10 15:51:50.421293','2020-05-10 15:51:50.421316',159,1,4,'_218','Ароматизаторы',NULL,'/cat/avtohimiya/aromatizatory/','_cat_45',25,0,NULL,NULL,NULL,NULL),(222,NULL,'2020-05-10 15:51:50.425611','2020-05-10 15:51:50.425638',160,1,4,'_218','Присадки',NULL,'/cat/avtohimiya/prisadki/','_cat_23',25,0,NULL,NULL,NULL,NULL),(223,NULL,'2020-05-10 15:51:50.429370','2020-05-10 15:51:50.429393',161,1,4,'_218','Смазки',NULL,'/cat/avtohimiya/smazki/','_cat_25',25,0,NULL,NULL,NULL,NULL),(224,NULL,'2020-05-10 15:51:50.432297','2020-05-10 15:51:50.432320',162,1,4,'','Электрооборудование',NULL,'/cat/elektrooborudovanie/','_cat_27',25,0,NULL,NULL,NULL,NULL),(225,NULL,'2020-05-10 15:51:50.437089','2020-05-10 15:51:50.437111',163,1,4,'_224','Аккумуляторные батареи',NULL,'/cat/elektrooborudovanie/akkumulyatornye-batarei/','_cat_36',25,0,NULL,NULL,NULL,NULL),(226,NULL,'2020-05-10 15:51:50.440904','2020-05-10 15:51:50.440927',164,1,4,'_224','Пуско-зарядные устройства',NULL,'/cat/elektrooborudovanie/pusko-zaryadnye-ustroystva/','_cat_39',25,0,NULL,NULL,NULL,NULL),(227,NULL,'2020-05-10 15:51:50.444547','2020-05-10 15:51:50.444570',165,1,4,'_224','Провода для прикуривания',NULL,'/cat/elektrooborudovanie/provoda-dlya-prikurivaniya/','_cat_40',25,0,NULL,NULL,NULL,NULL),(228,NULL,'2020-05-10 15:51:50.448206','2020-05-10 15:51:50.448227',166,1,4,'_224','Автоэлектроника',NULL,'/cat/elektrooborudovanie/avtoelektronika/','_cat_41',25,0,NULL,NULL,NULL,NULL),(229,NULL,'2020-05-10 15:51:50.451776','2020-05-10 15:51:50.451799',167,1,4,'_224','Автозвук',NULL,'/cat/elektrooborudovanie/avtozvuk/','_cat_47',25,0,NULL,NULL,NULL,NULL),(230,NULL,'2020-05-10 15:51:50.455524','2020-05-10 15:51:50.455547',168,1,4,'_224','Мойки высокого давления',NULL,'/cat/elektrooborudovanie/moyki-vysokogo-davleniya/','_cat_48',25,0,NULL,NULL,NULL,NULL),(231,NULL,'2020-05-10 15:51:50.459109','2020-05-10 15:51:50.459131',169,1,4,'_224','Автомобильные пылесосы',NULL,'/cat/elektrooborudovanie/avtomobilnye-pylesosy/','_cat_49',25,0,NULL,NULL,NULL,NULL),(232,NULL,'2020-05-10 15:51:50.462696','2020-05-10 15:51:50.462718',170,1,4,'_224','Автосвет',NULL,'/cat/elektrooborudovanie/avtosvet/','_cat_50',25,0,NULL,NULL,NULL,NULL),(233,NULL,'2020-05-10 15:51:50.466366','2020-05-10 15:51:50.466389',171,1,4,'_224','Видеорегистраторы',NULL,'/cat/elektrooborudovanie/videoregistratory/','_cat_52',25,0,NULL,NULL,NULL,NULL),(234,NULL,'2020-05-10 15:51:50.469980','2020-05-10 15:51:50.470002',172,1,4,'_224','Противоугонные устройства',NULL,'/cat/elektrooborudovanie/protivougonnye-ustroystva/','_cat_54',25,0,NULL,NULL,NULL,NULL),(235,NULL,'2020-05-10 15:51:50.473563','2020-05-10 15:51:50.473584',173,1,4,'_224','Парковочные радары и камеры',NULL,'/cat/elektrooborudovanie/parkovochnye-radary-i-kamery/','_cat_55',25,0,NULL,NULL,NULL,NULL),(236,NULL,'2020-05-10 15:51:50.477217','2020-05-10 15:51:50.477239',174,1,4,'_224','Радар-детекторы',NULL,'/cat/elektrooborudovanie/radar-detektory/','_cat_56',25,0,NULL,NULL,NULL,NULL),(237,NULL,'2020-05-10 15:51:50.480816','2020-05-10 15:51:50.480838',175,1,4,'_224','Компрессоры, насосы и манометры',NULL,'/cat/elektrooborudovanie/kompressory-nasosy-i-manometry/','_cat_38',25,0,NULL,NULL,NULL,NULL),(238,NULL,'2020-05-10 15:51:50.484380','2020-05-10 15:51:50.484402',176,1,4,'_224','Подогреватели двигателя',NULL,'/cat/elektrooborudovanie/podogrevateli-dvigatelya/','_cat_44',25,0,NULL,NULL,NULL,NULL),(239,NULL,'2020-05-10 15:51:50.487207','2020-05-10 15:51:50.487229',177,1,4,'','Шины и диски',NULL,'/cat/shiny-i-diski/','_cat_20',25,0,NULL,NULL,NULL,NULL),(240,NULL,'2020-05-10 15:51:50.492025','2020-05-10 15:51:50.492047',178,1,4,'_239','Шины',NULL,'/cat/shiny-i-diski/shiny/','_cat_17',25,0,NULL,NULL,NULL,NULL),(241,NULL,'2020-05-10 15:51:50.495606','2020-05-10 15:51:50.495628',179,1,4,'_239','Диски',NULL,'/cat/shiny-i-diski/diski/','_cat_3',25,0,NULL,NULL,NULL,NULL),(242,NULL,'2020-05-10 15:51:50.499257','2020-05-10 15:51:50.499279',180,1,4,'_239','Крепежи',NULL,'/cat/shiny-i-diski/krepeji/','_cat_84',25,0,NULL,NULL,NULL,NULL),(243,NULL,'2020-05-10 15:51:50.502866','2020-05-10 15:51:50.502887',181,1,4,'_239','Камеры',NULL,'/cat/shiny-i-diski/kamery/','_cat_86',25,0,NULL,NULL,NULL,NULL),(244,NULL,'2020-05-10 15:51:50.506434','2020-05-10 15:51:50.506456',182,1,4,'_239','Колпаки',NULL,'/cat/shiny-i-diski/kolpaki/','_cat_87',25,0,NULL,NULL,NULL,NULL),(245,NULL,'2020-05-10 15:51:50.509313','2020-05-10 15:51:50.509335',183,1,4,'','Аксессуары',NULL,'/cat/aksessuary/','_cat_2',25,0,NULL,NULL,NULL,NULL),(246,NULL,'2020-05-10 15:51:50.514085','2020-05-10 15:51:50.514108',184,1,4,'_245','Дефлекторы',NULL,'/cat/aksessuary/deflektory/','_cat_60',25,0,NULL,NULL,NULL,NULL),(247,NULL,'2020-05-10 15:51:50.517699','2020-05-10 15:51:50.517720',185,1,4,'_245','Внешний декор',NULL,'/cat/aksessuary/vneshniy-dekor/','_cat_28',25,0,NULL,NULL,NULL,NULL),(248,NULL,'2020-05-10 15:51:50.521392','2020-05-10 15:51:50.521415',186,1,4,'_245','Защита',NULL,'/cat/aksessuary/zashhita/','_cat_29',25,0,NULL,NULL,NULL,NULL),(249,NULL,'2020-05-10 15:51:50.525061','2020-05-10 15:51:50.525082',187,1,4,'_245','Коврики',NULL,'/cat/aksessuary/kovriki/','_cat_32',25,0,NULL,NULL,NULL,NULL),(250,NULL,'2020-05-10 15:51:50.528607','2020-05-10 15:51:50.528629',188,1,4,'_245','Фаркопы',NULL,'/cat/aksessuary/farkopy/','_cat_30',25,0,NULL,NULL,NULL,NULL),(251,NULL,'2020-05-10 15:51:50.532293','2020-05-10 15:51:50.532317',189,1,4,'_245','Щетки стеклоочистителя',NULL,'/cat/aksessuary/shhetki-stekloochistitelya/','_cat_31',25,0,NULL,NULL,NULL,NULL),(252,NULL,'2020-05-10 15:51:50.535969','2020-05-10 15:51:50.535990',190,1,4,'_245','Крепление для багажа',NULL,'/cat/aksessuary/kreplenie-dlya-bagaja/','_cat_34',25,0,NULL,NULL,NULL,NULL),(253,NULL,'2020-05-10 15:51:50.539592','2020-05-10 15:51:50.539615',191,1,4,'_245','Чехлы и накидки',NULL,'/cat/aksessuary/chehly-i-nakidki/','_cat_33',25,0,NULL,NULL,NULL,NULL),(254,NULL,'2020-05-10 15:51:50.543189','2020-05-10 15:51:50.543211',192,1,4,'_245','Автолитература',NULL,'/cat/aksessuary/avtoliteratura/','_cat_58',25,0,NULL,NULL,NULL,NULL),(255,NULL,'2020-05-10 15:51:50.546778','2020-05-10 15:51:50.546799',193,1,4,'_245','Багажные системы',NULL,'/cat/aksessuary/bagajnye-sistemy/','_cat_59',25,0,NULL,NULL,NULL,NULL),(256,NULL,'2020-05-10 15:51:50.550421','2020-05-10 15:51:50.550443',194,1,4,'_245','Сувенирная продукция',NULL,'/cat/aksessuary/suvenirnaya-produkciya/','_cat_16',25,0,NULL,NULL,NULL,NULL),(257,NULL,'2020-05-10 15:51:50.554076','2020-05-10 15:51:50.554099',195,1,4,'_245','Одежда и обувь',NULL,'/cat/aksessuary/odejda-i-obuv/','_cat_11',25,0,NULL,NULL,NULL,NULL),(258,NULL,'2020-05-10 15:51:50.557770','2020-05-10 15:51:50.557792',196,1,4,'_245','Прочие аксессуары',NULL,'/cat/aksessuary/prochie-aksessuary/','_cat_35',25,0,NULL,NULL,NULL,NULL),(259,NULL,'2020-05-10 15:51:50.561368','2020-05-10 15:51:50.561391',197,1,4,'_245','Автокресла',NULL,'/cat/aksessuary/avtokresla/','_cat_43',25,0,NULL,NULL,NULL,NULL),(260,NULL,'2020-05-10 15:51:50.564208','2020-05-10 15:51:50.564229',198,1,4,'','Прочее',NULL,'/cat/prochee/','_cat_12',25,0,NULL,NULL,NULL,NULL),(261,NULL,'2020-05-10 15:51:50.569043','2020-05-10 15:51:50.569065',199,1,4,'_260','Держатели и столики',NULL,'/cat/prochee/derjateli-i-stoliki/','_cat_42',25,0,NULL,NULL,NULL,NULL),(262,NULL,'2020-05-10 15:51:50.572636','2020-05-10 15:51:50.572659',200,1,4,'_260','Руководство по эксплуатации',NULL,'/cat/prochee/rukovodstvo-po-ekspluatacii/','_cat_13',25,0,NULL,NULL,NULL,NULL),(263,NULL,'2020-05-10 15:51:50.575582','2020-05-10 15:51:50.575604',201,1,4,'','Инструменты',NULL,'/cat/instrumenty/','_cat_64',25,0,NULL,NULL,NULL,NULL),(264,NULL,'2020-05-10 15:51:50.580256','2020-05-10 15:51:50.580278',202,1,4,'_263','Домкраты',NULL,'/cat/instrumenty/domkraty/','_cat_66',25,0,NULL,NULL,NULL,NULL),(265,NULL,'2020-05-10 15:51:50.583831','2020-05-10 15:51:50.583854',203,1,4,'_263','Лебёдки',NULL,'/cat/instrumenty/lebyodki/','_cat_89',25,0,NULL,NULL,NULL,NULL),(266,NULL,'2020-05-10 15:51:50.587453','2020-05-10 15:51:50.587474',204,1,4,'_263','Измерительный',NULL,'/cat/instrumenty/izmeritelnyy/','_cat_67',25,0,NULL,NULL,NULL,NULL),(267,NULL,'2020-05-10 15:51:50.591202','2020-05-10 15:51:50.591226',205,1,4,'_263','Наборы инструмента',NULL,'/cat/instrumenty/nabory-instrumenta/','_cat_68',25,0,NULL,NULL,NULL,NULL),(268,NULL,'2020-05-10 15:51:50.594826','2020-05-10 15:51:50.594847',206,1,4,'_263','Расходные материалы',NULL,'/cat/instrumenty/rashodnye-materialy/','_cat_69',25,0,NULL,NULL,NULL,NULL),(269,NULL,'2020-05-10 15:51:50.598392','2020-05-10 15:51:50.598413',207,1,4,'_263','Ручной инструмент',NULL,'/cat/instrumenty/ruchnoy-instrument/','_cat_70',25,0,NULL,NULL,NULL,NULL),(270,NULL,'2020-05-10 15:51:50.601915','2020-05-10 15:51:50.601937',208,1,4,'_263','Хранение инструмента',NULL,'/cat/instrumenty/hranenie-instrumenta/','_cat_71',25,0,NULL,NULL,NULL,NULL),(271,NULL,'2020-05-10 15:51:50.605482','2020-05-10 15:51:50.605504',209,1,4,'_263','Электроинструмент',NULL,'/cat/instrumenty/elektroinstrument/','_cat_72',25,0,NULL,NULL,NULL,NULL),(272,NULL,'2020-05-10 15:51:50.609072','2020-05-10 15:51:50.609094',210,1,4,'_263','Пневматические инструменты',NULL,'/cat/instrumenty/pnevmaticheskie-instrumenty/','_cat_74',25,0,NULL,NULL,NULL,NULL);
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
  KEY `flatcontent_containers_img_59d06f2c` (`img`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
INSERT INTO `flatcontent_containers` VALUES (3,NULL,'2020-05-04 20:14:44.543875','2020-05-04 20:14:44.543909',1,1,2,NULL,'Контент для всех страничек','Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики','main',NULL),(9,NULL,'2020-05-05 12:30:09.933945','2020-05-05 12:30:09.933980',3,1,1,NULL,'Главное меню','Создано автоматически, выводит главное меню','mainmenu',NULL),(10,NULL,'2020-05-05 12:30:09.936748','2020-05-05 12:30:09.936769',4,1,1,NULL,'Нижнее меню','Создано автоматически, выводит нижнее меню','bottommenu',NULL),(11,NULL,'2020-05-05 13:29:29.942595','2020-05-05 13:29:29.942618',5,1,99,'','Слайдер','','slider',''),(12,NULL,'2020-05-05 13:34:19.428588','2020-05-05 13:34:19.437123',6,1,3,'','Слайдер','','slider',''),(13,NULL,'2020-05-07 18:38:45.587736','2020-05-07 18:38:45.587766',7,1,99,'','Товары - Вкладки','','products_tabs',''),(14,NULL,'2020-05-07 19:03:03.649348','2020-05-07 19:03:03.656326',8,1,3,'','Товары - Вкладки','','products_tabs',''),(15,NULL,'2020-05-07 19:05:18.149865','2020-05-07 19:05:18.149887',9,1,99,'','Баннеры','','banners',''),(16,NULL,'2020-05-07 21:27:29.455016','2020-05-07 21:27:29.461762',10,1,3,'','Баннеры','','banners',''),(17,NULL,'2020-05-07 21:35:17.254015','2020-05-10 15:59:21.729654',11,1,99,'','Товары - Слайдер','','products_slider',''),(18,NULL,'2020-05-07 21:40:58.592318','2020-05-10 16:00:31.086309',12,1,3,'','Товары - Слайдер','','products_slider',''),(19,NULL,'2020-05-07 23:16:42.565354','2020-05-07 23:16:42.565378',13,1,99,'','Новости','','news',''),(20,NULL,'2020-05-07 23:19:45.777213','2020-05-07 23:19:45.782922',14,1,3,'','Новости','','news',''),(21,NULL,'2020-05-07 23:22:29.220921','2020-05-07 23:22:29.220941',15,1,99,'','Отзывы','','reviews',''),(22,NULL,'2020-05-07 23:32:10.791704','2020-05-07 23:32:10.798493',16,1,3,'','Отзывы','','reviews',''),(23,NULL,'2020-05-10 14:19:18.601147','2020-05-10 16:01:23.812162',17,1,99,'','Популярные товары','','products_sidebar_slider',''),(24,NULL,'2020-05-10 15:48:37.205453','2020-05-10 15:48:37.205473',18,1,99,'','Каталог','','catalogue',''),(25,NULL,'2020-05-10 15:48:51.552867','2020-05-10 15:48:51.558277',19,1,7,'','Каталог','','catalogue','');
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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_linkcontainer`
--

LOCK TABLES `flatcontent_linkcontainer` WRITE;
/*!40000 ALTER TABLE `flatcontent_linkcontainer` DISABLE KEYS */;
INSERT INTO `flatcontent_linkcontainer` VALUES (16,NULL,'2020-05-07 23:32:25.302469','2020-05-07 23:32:25.302503',1,1,NULL,NULL,113,12),(17,NULL,'2020-05-07 23:32:25.303919','2020-05-07 23:32:25.303939',2,1,NULL,NULL,113,14),(18,NULL,'2020-05-07 23:32:25.305441','2020-05-07 23:32:25.305461',3,1,NULL,NULL,113,16),(19,NULL,'2020-05-07 23:32:25.306832','2020-05-07 23:32:25.306852',4,1,NULL,NULL,113,18),(20,NULL,'2020-05-07 23:32:25.308186','2020-05-07 23:32:25.308206',5,1,NULL,NULL,113,20),(21,NULL,'2020-05-07 23:32:25.309614','2020-05-07 23:32:25.309634',6,1,NULL,NULL,113,22);
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
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `login_customuser_created_4a29e213` (`created`),
  KEY `login_customuser_updated_dc9f9081` (`updated`),
  KEY `login_customuser_position_33445dcc` (`position`),
  KEY `login_customuser_is_active_cccf2704` (`is_active`),
  KEY `login_customuser_state_f0a75add` (`state`),
  KEY `login_customuser_parents_3604d87b` (`parents`),
  KEY `login_customuser_img_6a17a9f3` (`img`),
  KEY `login_customuser_phone_d456dd09` (`phone`),
  CONSTRAINT `login_customuser_user_id_70d7d409_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_customuser`
--

LOCK TABLES `login_customuser` WRITE;
/*!40000 ALTER TABLE `login_customuser` DISABLE KEYS */;
INSERT INTO `login_customuser` VALUES (1,NULL,'2020-05-04 16:51:56.000925','2020-05-08 17:47:40.975986',1,1,NULL,NULL,NULL,1);
/*!40000 ALTER TABLE `login_customuser` ENABLE KEYS */;
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
-- Table structure for table `products_products`
--

DROP TABLE IF EXISTS `products_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `altname` varchar(255) DEFAULT NULL,
  `manufacturer` varchar(255) DEFAULT NULL,
  `measure` varchar(255) DEFAULT NULL,
  `currency` int(11) DEFAULT NULL,
  `old_price` decimal(13,2) DEFAULT NULL,
  `price` decimal(13,2) DEFAULT NULL,
  `dj_info` varchar(255) DEFAULT NULL,
  `mini_info` longtext,
  `info` longtext,
  `code` varchar(255) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_products_img_f679aa79` (`img`),
  KEY `products_products_created_4ed1d7db` (`created`),
  KEY `products_products_updated_c1270b99` (`updated`),
  KEY `products_products_position_78f586f8` (`position`),
  KEY `products_products_is_active_7cc0d5d1` (`is_active`),
  KEY `products_products_state_dfece9ba` (`state`),
  KEY `products_products_parents_5a6d11d6` (`parents`),
  KEY `products_products_name_5a04f704` (`name`),
  KEY `products_products_altname_23fdd5ad` (`altname`),
  KEY `products_products_manufacturer_af812d05` (`manufacturer`),
  KEY `products_products_measure_187e0e95` (`measure`),
  KEY `products_products_currency_6608b7c0` (`currency`),
  KEY `products_products_old_price_648a4886` (`old_price`),
  KEY `products_products_price_20f0b593` (`price`),
  KEY `products_products_dj_info_6058aa31` (`dj_info`),
  KEY `products_products_code_d2de949b` (`code`),
  KEY `products_products_count_8ac0f722` (`count`)
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_products`
--

LOCK TABLES `products_products` WRITE;
/*!40000 ALTER TABLE `products_products` DISABLE KEYS */;
INSERT INTO `products_products` VALUES (67,'67.jpg','2020-05-10 15:49:00.386445','2020-05-10 15:51:50.966009',1,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S40240','Bosch',NULL,NULL,NULL,5344.00,NULL,'Аккумуляторная батарея','Размеры: 232х173х225, тип крепления: B00, тип клемм: T1, емкость: 60, пусковой ток: 540, полярность обратная','_em_79241227',105),(68,'68.jpg','2020-05-10 15:49:02.100629','2020-05-10 15:51:51.006677',2,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S40260','Bosch',NULL,NULL,NULL,6785.00,NULL,'Аккумуляторная батарея','Размеры: 261х175х220, тип крепления: B01, тип клемм: T1, емкость: 70, пусковой ток: 630, полярность обратная','_em_79241228',124),(69,'69.jpg','2020-05-10 15:49:03.857432','2020-05-10 15:51:51.044509',3,1,NULL,NULL,'Аккумулятор BOSCH 60 A/ч ОБР','0092S40050','Bosch',NULL,NULL,NULL,5320.00,NULL,'Аккумулятор BOSCH 60 A/ч ОБР','Аккумулятор BOSCH 60 A/ч S40 05 ОБР 242x175x190 EN 540','_em_79241218',119),(70,'70.jpg','2020-05-10 15:49:05.760906','2020-05-10 15:51:51.082332',4,1,NULL,NULL,'Аккумулятор EXIDE PREMIUM 64Ah EN640 о.п.(242х175х190) (EA640)','EA640','Exide',NULL,NULL,NULL,5381.00,NULL,'Аккумулятор 6ст - 64 (Exide Premium) - оп','Аккумулятор EXIDE PREMIUM 64Ah EN640 о.п.(242х175х190) (EA640)','_em_98650212',90),(71,'71.jpg','2020-05-10 15:49:06.502937','2020-05-10 15:51:51.122978',5,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S40040','Bosch',NULL,NULL,NULL,4920.00,NULL,'Аккумуляторная батарея','Размеры: 242х175х175, тип крепления: B13, тип клемм: T1, емкость: 60, пусковой ток: 540, полярность обратная','_em_79241217',102),(72,'72.jpg','2020-05-10 15:49:08.133171','2020-05-10 15:51:51.160248',6,1,NULL,NULL,'Аккумулятор BOSCH 95 A/ч ОБР','0092S40280','Bosch',NULL,NULL,NULL,8256.00,NULL,'Аккумулятор BOSCH 95 A/ч ОБР','Аккумулятор BOSCH 95 A/ч S40 28 выс ОБР 306x173x225 EN 830','_em_79241230',112),(73,'73.jpg','2020-05-10 15:49:08.972075','2020-05-10 15:51:51.197774',7,1,NULL,NULL,'Аккумулятор BOSCH 45 A/ч ОБР','0092S40210','Bosch',NULL,NULL,NULL,4175.00,NULL,'Аккумуляторная батарея','Аккумулятор BOSCH 45 A/ч S40 21 стд кл выс ОБР 238x129x227 EN 330','_em_79241225',103),(74,'74.jpg','2020-05-10 15:49:10.591592','2020-05-10 15:51:51.234954',8,1,NULL,NULL,'Аккумулятор BOSCH 100 A/ч ОБР','0092S50130','Bosch',NULL,NULL,NULL,9845.00,NULL,'Аккумуляторная батарея','Размеры: 353х175х190, тип крепления: B13, тип клемм: T1, емкость: 100, пусковой ток: 830, полярность обратная','_em_78989678',115),(75,'75.jpg','2020-05-10 15:49:12.186064','2020-05-10 15:51:51.272288',9,1,NULL,NULL,'Аккумуляторная батарея Exide','EA1000','Exide',NULL,NULL,NULL,9458.00,NULL,'Аккумуляторная батарея','Размеры: 353х175х190, тип крепления: B13, тип клемм: T1, емкость: 100, пусковой ток: 900, полярность обратная','_em_98650210',100),(76,'76.jpg','2020-05-10 15:49:12.974098','2020-05-10 15:51:51.312905',10,1,NULL,NULL,'Аккумулятор BOSCH 40 A/ч','0092S40190','Bosch',NULL,NULL,NULL,3765.00,NULL,'Аккумулятор BOSCH 40 A/ч','Аккумулятор BOSCH 40 A/ч S40 19 узк кл выс 187x127x227 EN 330','_em_79241224',81),(77,'77.jpg','2020-05-10 15:49:14.604815','2020-05-10 15:51:51.350359',11,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S40080','Bosch',NULL,NULL,NULL,6225.00,NULL,'Аккумулятор BOSCH 74 A/ч ОБР.','Аккумулятор BOSCH 74 A/ч S40 08 ОБР. 278x175x190 EN 680','_em_79241220',117),(78,'78.jpg','2020-05-10 15:49:16.185389','2020-05-10 15:51:51.387620',12,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S30050','Bosch',NULL,NULL,NULL,4850.00,NULL,'Аккумуляторная батарея','Размеры: 242х175х190, тип крепления: B13, тип клемм: T1, емкость: 56, пусковой ток: 480, полярность обратная','_em_79241208',104),(79,'79.jpg','2020-05-10 15:49:16.916226','2020-05-10 15:51:51.424903',13,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S40060','Bosch',NULL,NULL,NULL,6072.00,NULL,'Аккумуляторная батарея','Размеры: 242х175х190, тип крепления: B13, тип клемм: T1, емкость: 60, пусковой ток: 540, полярность прямая','_em_79241219',109),(80,'80.jpg','2020-05-10 15:49:18.445831','2020-05-10 15:51:51.463142',14,1,NULL,NULL,'Аккумулятор BOSCH 63 A/ч ОБР','0092S50050','Bosch',NULL,NULL,NULL,6108.00,NULL,'Аккумулятор BOSCH 63 A/ч ОБР','Аккумулятор BOSCH 63 A/ч S50 05 ОБР 242x175x190 EN 610','_em_78989677',93),(81,'81.jpg','2020-05-10 15:49:20.083002','2020-05-10 15:51:51.500644',15,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S40290','Bosch',NULL,NULL,NULL,8809.00,NULL,'Аккумуляторная батарея','Размеры: 306х173х225, тип крепления: B01, тип клемм: T1, емкость: 95, пусковой ток: 830, полярность прямая','_em_79241231',98),(82,'82.jpg','2020-05-10 15:49:21.687869','2020-05-10 15:51:51.538361',16,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S50040','Bosch',NULL,NULL,NULL,5951.00,NULL,'Аккумуляторная батарея','Размеры: 242х175х175, тип крепления: B13, тип клемм: T1, емкость: 61, пусковой ток: 600, полярность обратная','_em_79241233',90),(83,'83.jpg','2020-05-10 15:49:23.452318','2020-05-10 15:51:51.575710',17,1,NULL,NULL,'Аккумуляторная батарея Exide','EA530','Exide',NULL,NULL,NULL,5437.00,NULL,'EXIDE PREMIUM 53Ah EN540 о.п.(207х175х190) (EA530)','Размеры: 207х175х190, тип крепления: B13, тип клемм: T1, емкость: 53, пусковой ток: 540, полярность обратная','_em_101978329',82),(84,'84.jpg','2020-05-10 15:49:24.183940','2020-05-10 15:51:51.616229',18,1,NULL,NULL,'Bosch S4 Asia 018 40Ач R+ EN330A 187x127x227 540 126 033 B00','0092S40180','Bosch',NULL,NULL,NULL,3615.00,NULL,'Bosch S4 Asia 018 40Ач R+ EN330A 187x127x227 540 126 033 B00','Аккумуляторная батареяBosch S4 Asia 018 40Ач R+ EN330A 187x127x227 540 126 033 B00','_em_79241223',85),(85,'85.jpg','2020-05-10 15:49:25.759389','2020-05-10 15:51:51.650836',19,1,NULL,NULL,'Аккумулятор EXIDE EXCELL 62Ah EN540 о.п.(242х175х190) (EB620)','EB620','Exide',NULL,NULL,NULL,4778.00,NULL,'EXIDE EXCELL 62Ah EN540 о.п.(242х175х190) (EB620)','Аккумулятор EXIDE EXCELL 62Ah EN540 о.п.(242х175х190) (EB620)','_em_98650219',74),(86,'86.jpg','2020-05-10 15:49:26.477332','2020-05-10 15:51:51.692459',20,1,NULL,NULL,'Аккумулятор 6ст - 62 Exide Exell - пп','EB621','Exide',NULL,NULL,NULL,4970.00,NULL,'Аккумулятор 6ст - 62 Exide Exell - пп','Аккумулятор 6ст - 62 Exide Exell - пп','_em_98650220',86),(87,'87.jpg','2020-05-10 15:49:27.209524','2020-05-10 15:51:51.733295',21,1,NULL,NULL,'Аккумулятор EXIDE PREMIUM 75Ah EN630 о.п.(270х173х222) (EA754) (борт)','EA754','Exide',NULL,NULL,NULL,6598.00,NULL,'EXIDE PREMIUM 75Ah EN630 о.п.(270х173х222) (EA754) (борт)','Аккумулятор EXIDE PREMIUM 75Ah EN630 о.п.(270х173х222) (EA754) (борт)','_em_98703687',87),(88,'88.jpg','2020-05-10 15:49:27.920888','2020-05-10 15:51:51.773888',22,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S50060','Bosch',NULL,NULL,NULL,6513.00,NULL,'Аккумуляторная батарея','Размеры: 242х175х190, тип крепления: B13, тип клемм: T1, емкость: 63, пусковой ток: 610, полярность прямая','_em_79342211',86),(89,'89.jpg','2020-05-10 15:49:29.408346','2020-05-10 15:51:51.811197',23,1,NULL,NULL,'Аккумулятор EXIDE EXCELL 95Ah EN800 о.п.(353х175х190) (EB950)','EB950','Exide',NULL,NULL,NULL,8519.00,NULL,'EXIDE EXCELL 95Ah EN800 о.п.(353х175х190) (EB950)','Размеры: 353x175x190 Тип крепления: B13 Тип клемм: 1 Емкость: 95ч Пусковой ток: 800 Полярность: обратная Напряжение: 12B','_em_101978339',85),(90,'90.jpg','2020-05-10 15:49:30.196657','2020-05-10 15:51:51.851959',24,1,NULL,NULL,'Аккумулятор 6ст - 65 (Exide Premium) Asia - оп','EA654','Exide',NULL,NULL,NULL,5832.00,NULL,'Аккумулятор 6ст - 65 (Exide Premium) Asia - оп','Аккумулятор 6ст - 65 (Exide Premium) Asia - оп','_em_101978330',96),(91,'91.jpg','2020-05-10 15:49:30.892457','2020-05-10 15:51:51.892519',25,1,NULL,NULL,'Аккумулятор BOSCH 74 A/ч ОБР','0092S50070','Bosch',NULL,NULL,NULL,7199.00,NULL,'Аккумулятор BOSCH 74 A/ч ОБР','Аккумулятор BOSCH 74 A/ч S50 07 низк ОБР 278x175x175 EN 750','_em_79241234',108),(92,'92.jpg','2020-05-10 15:49:32.584675','2020-05-10 15:51:51.929917',26,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S30060','Bosch',NULL,NULL,NULL,4453.00,NULL,'Аккумуляторная батарея','Размеры: 242х175х190, тип крепления: B13, тип клемм: T1, емкость: 56, пусковой ток: 480, полярность прямая','_em_79241209',92),(93,'93.jpg','2020-05-10 15:49:34.103816','2020-05-10 15:51:51.968207',27,1,NULL,NULL,'Аккумулятор BOSCH 70 A/ч ОБР','0092S30070','Bosch',NULL,NULL,NULL,6018.00,NULL,'Аккумулятор BOSCH 70 A/ч ОБР','Аккумулятор BOSCH 70 A/ч S30 07 низк ОБР 278x175x175 EN 640','_em_79241210',89),(94,'94.jpg','2020-05-10 15:49:35.699818','2020-05-10 15:51:52.005691',28,1,NULL,NULL,'Аккумулятор EXIDE PREMIUM 77Ah EN760 о.п.(278х175х190) (EA770)','EA770','Exide',NULL,NULL,NULL,6687.00,NULL,'EXIDE PREMIUM 77Ah EN760 о.п.(278х175х190) (EA770)','Аккумулятор EXIDE PREMIUM 77Ah EN760 о.п.(278х175х190) (EA770)','_em_99196503',96),(95,'95.jpg','2020-05-10 15:49:36.392979','2020-05-10 15:51:52.046406',29,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S40130','Bosch',NULL,NULL,NULL,8809.00,NULL,'Аккумуляторная батарея','Размеры: 353х175х190, тип крепления: B13, тип клемм: T1, емкость: 95, пусковой ток: 800, полярность обратная','_em_79241222',86),(96,'96.jpg','2020-05-10 15:49:37.847356','2020-05-10 15:51:52.084128',30,1,NULL,NULL,'Bosch S4 Asia 020 45Ач R+ EN330A 238x129x227 545 155 033 B00','0092S40200','Bosch',NULL,NULL,NULL,4380.00,NULL,'Bosch S4 Asia 020 45Ач R+ EN330A 238x129x227 545 155 033 B00','Аккумуляторная батареяBosch S4 Asia 020 45Ач R+ EN330A 238x129x227 545 155 033 B00','_em_81390688',92),(97,'97.jpg','2020-05-10 15:49:39.344693','2020-05-10 15:51:52.118575',31,1,NULL,NULL,'Аккумулятор BOSCH 77 A/ч ОБР.','0092S50080','Bosch',NULL,NULL,NULL,7633.00,NULL,'Аккумулятор BOSCH 77 A/ч ОБР.','Аккумулятор BOSCH 77 A/ч S50 08 ОБР. 278x175x190 EN 780','_em_79241235',88),(98,'98.jpg','2020-05-10 15:49:40.902591','2020-05-10 15:51:52.155796',32,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S30020','Bosch',NULL,NULL,NULL,3925.00,NULL,'Аккумуляторная батарея','Размеры: 207х175х190, тип крепления: B13 тип клемм: T1 емкость: 45 пусковой ток: 400 полярность обратная','_em_79241206',71),(99,NULL,'2020-05-10 15:49:42.640106','2020-05-10 15:51:52.193208',33,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S40010','Bosch',NULL,NULL,NULL,4107.00,NULL,'Аккумуляторная батарея','Размеры: 207х175х190, тип крепления: B13 тип клемм: T1 емкость: 44 пусковой ток: 440 полярность обратная','_em_79241215',64),(100,'100.jpg','2020-05-10 15:49:42.671071','2020-05-10 15:51:52.220228',34,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S40100','Bosch',NULL,NULL,NULL,7422.00,NULL,'Аккумулятор BOSCH 80 A/ч ОБР.','Аккумулятор BOSCH 80 A/ч S40 10 ОБР. 315x175x175 EN 740','_em_79066169',114),(101,'101.jpg','2020-05-10 15:49:44.195973','2020-05-10 15:51:52.257163',35,1,NULL,NULL,'Аккумулятор BOSCH 60 A/ч','0092S40250','Bosch',NULL,NULL,NULL,5552.00,NULL,'Аккумулятор BOSCH 60 A/ч','Аккумулятор BOSCH 60 A/ч S40 25 выс 232x173x225 EN 540','_em_79066170',81),(102,'102.jpg','2020-05-10 15:49:45.828261','2020-05-10 15:51:52.294655',36,1,NULL,NULL,'Аккумулятор BOSCH 52 A/ч ОБР','0092S40020','Bosch',NULL,NULL,NULL,5913.00,NULL,'Аккумулятор BOSCH 52 A/ч ОБР','Размеры: 207х175х190, тип крепления: B13 тип клемм: T1 емкость: 52 пусковой ток: 470 полярность обратная','_em_79241216',100),(103,'103.jpg','2020-05-10 15:49:47.590485','2020-05-10 15:51:52.332500',37,1,NULL,NULL,'Аккумулятор BOSCH 72 A/ч ОБР.','0092S40070','Bosch',NULL,NULL,NULL,6636.00,NULL,'Аккумулятор BOSCH 72 A/ч ОБР.','Аккумулятор BOSCH 72 A/ч S40 07 ОБР. 278x175x175 EN 680','_em_79450911',104),(104,NULL,'2020-05-10 15:49:49.272719','2020-05-10 15:51:52.369931',38,1,NULL,NULL,'Аккумуляторная батарея Exide 71/Ч Excell EB712','EB712','Exide',NULL,NULL,NULL,5592.00,NULL,'EXIDE EXCELL 71Ah EN670 о.п.(278х175х175) (EB712)','Размеры: 278x175x175 Тип крепления: B13 Тип клемм: 1 Емкость: 71ч Пусковой ток: 670 Полярность: обратная Напряжение: 12B','_em_101978337',77),(105,'105.jpg','2020-05-10 15:49:49.319140','2020-05-10 15:51:52.410599',39,1,NULL,NULL,'Аккумулятор BOSCH 54 A/ч ОБР','0092S50020','Bosch',NULL,NULL,NULL,5430.00,NULL,'Аккумулятор BOSCH 54 A/ч ОБР','Размеры: 207х175х190, тип крепления: B13, тип клемм: T1, емкость: 54, пусковой ток: 530, полярность обратная','_em_79715832',88),(106,'106.jpg','2020-05-10 15:49:50.930673','2020-05-10 15:51:52.449234',40,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S40220','Bosch',NULL,NULL,NULL,4175.00,NULL,'Аккумуляторная батарея','Аккумулятор BOSCH 45 A/ч S40 22 узк кл выс 238x129x227 EN 330','_em_79450912',82),(107,'107.jpg','2020-05-10 15:49:52.392781','2020-05-10 15:51:52.486549',41,1,NULL,NULL,'Аккумуляторная батарея Varta Blue Dynamic D47 60/Ч 560410054','560410054','Varta',NULL,NULL,NULL,5220.00,NULL,'Аккумулятор 6ст - 60 (Varta) D47 Blue Dynamic Asia . 560 410 054 - оп','Размеры: 232x173x225, тип крепления B00, тип клемм 1, емкость 60, пусковой ток 540, напряжение 12В, обратная полярность','_em_86094047',89),(108,NULL,'2020-05-10 15:49:53.073694','2020-05-10 15:51:52.527458',42,1,NULL,NULL,'Аккумулятор EXIDE EXCELL 74Ah EN680 о.п.(278х175х190) (EB740)','EB740','Exide',NULL,NULL,NULL,5758.00,NULL,'EXIDE EXCELL 74Ah EN680 о.п.(278х175х190) (EB740)','Аккумулятор EXIDE EXCELL 74Ah EN680 о.п.(278х175х190) (EB740)','_em_98650221',75),(109,'109.jpg','2020-05-10 15:49:53.121603','2020-05-10 15:51:52.568631',43,1,NULL,NULL,'Тюменский медведь Silver Ca/Ca 60.0 Asia 65D23L','4607175655224','Алькор',NULL,NULL,NULL,4483.00,NULL,'Тюменский медведь','Плюс справа, вес залитого 16.3, габариты 230х173х221мм, емкость60 А/ч, полярность обратная, пусковой ток I2, тип клемм Euro 1, тип крепления B01','_em_156733861',1),(110,'110.jpg','2020-05-10 15:49:53.904884','2020-05-10 15:51:52.602701',44,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S50150','Bosch',NULL,NULL,NULL,10441.00,NULL,'Аккумулятор BOSCH 110 A/ч ОБР','Аккумулятор BOSCH 110 A/ч S50 15 ОБР 393x175x190 EN 920','_em_79450914',108),(111,'111.jpg','2020-05-10 15:49:55.315520','2020-05-10 15:51:52.640172',45,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S30080','Bosch',NULL,NULL,NULL,6018.00,NULL,'Аккумуляторная батарея','Размеры: 278х175х190, тип крепления: B13, тип клемм: T1, емкость: 70, пусковой ток: 640, полярность обратная','_em_79241211',85),(112,'112.jpg','2020-05-10 15:49:57.065179','2020-05-10 15:51:52.677556',46,1,NULL,NULL,'Аккумулятор EXIDE PREMIUM 85Ah EN800 о.п.(315х175х175) (EA852)','EA852','Exide',NULL,NULL,NULL,7541.00,NULL,'EXIDE PREMIUM 85Ah EN800 о.п.(315х175х175) (EA852)','Размеры: 315x175x175 Тип крепления: B13 Тип клемм: 1 Емкость: 85ч Пусковой ток: 800 Полярность: обратная Напряжение: 12B','_em_98650214',91),(113,NULL,'2020-05-10 15:49:57.839613','2020-05-10 15:51:52.718649',47,1,NULL,NULL,'Аккумулятор EXIDE EXCELL 50Ah EN450 п.п.(207х175х190) (EB501)','EB501','Exide',NULL,NULL,NULL,4855.00,NULL,'EXIDE EXCELL 50Ah EN450 п.п.(207х175х190) (EB501)','Аккумулятор EXIDE EXCELL 50Ah EN450 п.п.(207х175х190) (EB501)','_em_106261267',14),(114,'114.jpg','2020-05-10 15:49:57.886330','2020-05-10 15:51:52.758942',48,1,NULL,NULL,'Аккумулятор EXIDE EXCELL 60Ah EN390 о.п.(230х172х220) (EB604)','EB604','Exide',NULL,NULL,NULL,5073.00,NULL,'EXIDE EXCELL 60Ah EN390 о.п.(230х172х220) (EB604)','Аккумулятор EXIDE EXCELL 60Ah EN390 о.п.(230х172х220) (EB604)','_em_98650218',70),(115,NULL,'2020-05-10 15:49:58.563900','2020-05-10 15:51:52.799380',49,1,NULL,NULL,'Аккумуляторная батарея Varta','5601270543132','Varta',NULL,NULL,NULL,5706.00,NULL,'Аккумуляторная батарея','Размеры: 242х175х190, тип крепления: B13, тип клемм: T1, емкость: 60, пусковой ток: 540, полярность прямая','_em_87976942',8),(116,NULL,'2020-05-10 15:49:58.595120','2020-05-10 15:51:52.827459',50,1,NULL,NULL,'Аккумуляторная батарея Varta','5604100543132','Varta',NULL,NULL,NULL,5706.00,NULL,'Аккумуляторная батарея','Размеры: 232х173х225, тип крепления: B00, тип клемм: T1, емкость: 60, пусковой ток: 540, полярность обратная','_em_87976945',10),(117,NULL,'2020-05-10 15:49:58.633870','2020-05-10 15:51:52.858092',51,1,NULL,NULL,'Аккумуляторная батарея Varta','6004020833162','Varta',NULL,NULL,NULL,10112.00,NULL,'Аккумуляторная батарея','Размеры: 353х175х190, тип крепления: B13, тип клемм: T1, емкость: 100, пусковой ток: 830, полярность обратная','_em_87976957',34),(118,'118.jpg','2020-05-10 15:49:58.666536','2020-05-10 15:51:52.885427',52,1,NULL,NULL,'Тюменский Медведь 60.0','4607175650922','Алькор',NULL,NULL,NULL,3777.00,NULL,'Тюменский медведь','Плюс справа','_em_156733803',1),(119,NULL,'2020-05-10 15:49:59.574583','2020-05-10 15:51:52.916321',53,1,NULL,NULL,'Аккумуляторная батарея Varta','5604080543132','Varta',NULL,NULL,NULL,5706.00,NULL,'Аккумуляторная батарея','Размеры: 242х175х190, тип крепления: B13, тип клемм: T1, емкость: 60, пусковой ток: 540, полярность обратная','_em_87976943',9),(120,'120.jpg','2020-05-10 15:49:59.605175','2020-05-10 15:51:52.943961',54,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S50100','Bosch',NULL,NULL,NULL,8355.00,NULL,'Аккумуляторная батарея','Размеры: 315х175х175, тип крепления: B13, тип клемм: T1, емкость: 85, пусковой ток: 800, полярность обратная','_em_79450913',102),(121,'121.jpg','2020-05-10 15:50:01.180091','2020-05-10 15:51:52.981404',55,1,NULL,NULL,'Аккумуляторная батарея Exide 72/Ч Premium EA722','EA722','Exide',NULL,NULL,NULL,5814.00,NULL,'Аккумулятор 6ст - 72 (Exide Premium) - низк.оп','Размеры: 278x175x175 Тип крепления: B13 Тип клемм: 1 Емкость: 72ч Пусковой ток: 720 Полярность: обратная Напряжение: 12B','_em_98650213',80),(122,NULL,'2020-05-10 15:50:01.894691','2020-05-10 15:51:53.022367',56,1,NULL,NULL,'Аккумуляторная батарея Varta','5604090543132','Varta',NULL,NULL,NULL,5706.00,NULL,'Аккумуляторная батарея','Размеры: 242х175х175, тип крепления: B13, тип клемм: T1, емкость: 60, пусковой ток: 540, полярность обратная','_em_87976944',9),(123,'123.jpg','2020-05-10 15:50:01.925966','2020-05-10 15:51:53.050306',57,1,NULL,NULL,'Аккумуляторная батарея Bosch','0092S30130','Bosch',NULL,NULL,NULL,7382.00,NULL,'Аккумуляторная батарея','Размеры: 353х175х190, тип крепления: B13, тип клемм: T1, емкость: 90, пусковой ток: 720, полярность обратная','_em_79241213',100),(124,'124.jpg','2020-05-10 15:50:03.317628','2020-05-10 15:51:53.088014',58,1,NULL,NULL,'Аккумулятор BOSCH 74 A/ч','0092S40090','Bosch',NULL,NULL,NULL,6447.00,NULL,'Аккумуляторная батарея','Размеры: 278х175х190, тип крепления: B13, тип клемм: T1, емкость: 74, пусковой ток: 680, полярность прямая','_em_79241221',97),(125,NULL,'2020-05-10 15:50:04.991741','2020-05-10 15:51:53.125510',59,1,NULL,NULL,'Аккумуляторная батарея Varta','5852000803162','Varta',NULL,NULL,NULL,8607.00,NULL,'Аккумуляторная батарея','Размеры: 315х175х175, тип крепления: B13, тип клемм: T1, емкость: 85, пусковой ток: 800, полярность обратная','_em_87976954',3),(126,'126.jpg','2020-05-10 15:50:05.022588','2020-05-10 15:51:53.153047',60,1,NULL,NULL,'Тюменский медведь SILVER Ca/Ca 62.0 (низкая)','4607175654104','Алькор',NULL,NULL,NULL,4351.00,NULL,'Тюменский медведь','Плюс справа','_em_156733845',2),(127,'127.jpg','2020-05-10 15:50:05.806065','2020-05-10 15:51:53.184067',61,1,NULL,NULL,'Аккумуляторная батарея Exide 74/Ч Excell EB741','EB741','Exide',NULL,NULL,NULL,6108.00,NULL,'EXIDE EXCELL 74Ah EN680 п.п.(278х175х190) (EB741)','Размеры: 278x175x190 Тип крепления: B13 Тип клемм: 1 Емкость: 74ч Пусковой ток: 680 Полярность: прямая Напряжение: 12B','_em_101978338',78),(128,NULL,'2020-05-10 15:50:06.513486','2020-05-10 15:51:53.224864',62,1,NULL,NULL,'Аккумулятор BOSCH 7Ah EN110 о.п.(113х70х105) (YTZ7S-4/YTZ7S-BS) (Y5) AGM','0092M60090','Bosch',NULL,NULL,NULL,2515.00,NULL,'BOSCH 7Ah EN110 о.п.(113х70х105) (YTZ7S-4/YTZ7S-BS) (Y5) AGM','Аккумулятор BOSCH 7Ah EN110 о.п.(113х70х105) (YTZ7S-4/YTZ7S-BS) (Y5) AGM','_em_110374121',38),(129,'129.jpg','2020-05-10 15:50:06.566293','2020-05-10 15:51:53.265325',63,1,NULL,NULL,'Solite 95D26L 85Ач R+ EN650A 260x168x220 B00','95D26L','Solite',NULL,NULL,NULL,5453.00,NULL,'Solite 95D26L 85Ач R+ EN650A 260x168x220 B00','Аккумуляторная батареяSolite 95D26L 85Ач R+ EN650A 260x168x220 B00','_em_150377991',11),(130,'130.jpg','2020-05-10 15:50:08.148237','2020-05-10 15:51:53.299352',64,1,NULL,NULL,'SPACE Ca/Ca 65.0 ASIA 75D23L','4607175657692','Алькор',NULL,NULL,NULL,4322.00,NULL,'SPACE Ca/Ca 65.0 ASIA 75D23L','Плюс справа','_em_156862714',1);
/*!40000 ALTER TABLE `products_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_productscats`
--

DROP TABLE IF EXISTS `products_productscats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_productscats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_id` int(11) DEFAULT NULL,
  `product_id` int(11) NOT NULL,
  `container_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_productscat_product_id_6cc6463e_fk_products_` (`product_id`),
  KEY `products_productscats_cat_id_71130549_fk_flatcontent_blocks_id` (`cat_id`),
  KEY `products_productscat_container_id_2151481b_fk_flatconte` (`container_id`),
  CONSTRAINT `products_productscat_container_id_2151481b_fk_flatconte` FOREIGN KEY (`container_id`) REFERENCES `flatcontent_containers` (`id`),
  CONSTRAINT `products_productscat_product_id_6cc6463e_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_products` (`id`),
  CONSTRAINT `products_productscats_cat_id_71130549_fk_flatcontent_blocks_id` FOREIGN KEY (`cat_id`) REFERENCES `flatcontent_blocks` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=710 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productscats`
--

LOCK TABLES `products_productscats` WRITE;
/*!40000 ALTER TABLE `products_productscats` DISABLE KEYS */;
INSERT INTO `products_productscats` VALUES (595,225,67,25),(596,225,68,25),(597,225,69,25),(598,225,70,25),(599,225,71,25),(600,225,72,25),(601,225,73,25),(602,225,74,25),(603,225,75,25),(604,225,76,25),(605,225,77,25),(606,225,78,25),(607,225,79,25),(608,225,80,25),(609,225,81,25),(610,225,82,25),(611,225,83,25),(612,225,84,25),(613,225,85,25),(614,225,86,25),(615,225,87,25),(616,225,88,25),(617,225,89,25),(618,225,90,25),(619,225,91,25),(620,225,92,25),(621,225,93,25),(622,225,94,25),(623,225,95,25),(624,225,96,25),(625,225,97,25),(626,225,98,25),(627,225,99,25),(628,225,100,25),(629,225,101,25),(630,225,102,25),(631,225,103,25),(632,225,104,25),(633,225,105,25),(634,225,106,25),(635,225,107,25),(636,225,108,25),(637,225,109,25),(638,225,110,25),(639,225,111,25),(640,225,112,25),(641,225,113,25),(642,225,114,25),(643,225,115,25),(644,225,116,25),(645,225,117,25),(646,225,118,25),(647,225,119,25),(648,225,120,25),(649,225,121,25),(650,225,122,25),(651,225,123,25),(652,225,124,25),(653,225,125,25),(654,225,126,25),(655,225,127,25),(656,225,128,25),(657,225,129,25),(658,225,130,25),(659,136,69,13),(660,136,70,13),(661,136,71,13),(662,136,67,13),(663,136,68,13),(664,137,72,13),(665,137,88,13),(666,137,117,13),(667,137,105,13),(668,137,111,13),(669,138,71,13),(670,138,93,13),(671,138,120,13),(672,138,92,13),(673,138,90,13),(674,139,68,14),(675,139,70,14),(676,141,69,14),(677,141,70,14),(678,140,94,14),(679,140,103,14),(680,140,100,14),(681,140,92,14),(682,140,87,14),(683,141,90,14),(684,141,104,14),(685,141,94,14),(686,139,85,14),(687,139,129,14),(688,139,128,14),(689,NULL,67,17),(690,NULL,90,17),(691,NULL,84,17),(692,NULL,89,17),(693,NULL,71,17),(694,NULL,70,18),(695,NULL,68,18),(696,NULL,69,18),(697,NULL,67,18),(698,NULL,99,18),(699,NULL,69,23),(700,NULL,91,23),(701,NULL,83,23),(702,NULL,81,23),(703,NULL,88,23),(704,NULL,89,23),(705,NULL,87,23),(706,NULL,68,23),(707,NULL,71,23),(708,NULL,72,23),(709,NULL,84,23);
/*!40000 ALTER TABLE `products_productscats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_productsphotos`
--

DROP TABLE IF EXISTS `products_productsphotos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_productsphotos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_productspho_product_id_1dd25946_fk_products_` (`product_id`),
  KEY `products_productsphotos_img_bd5ed46f` (`img`),
  KEY `products_productsphotos_created_7e4c8398` (`created`),
  KEY `products_productsphotos_updated_1296c4e1` (`updated`),
  KEY `products_productsphotos_position_3b4fe066` (`position`),
  KEY `products_productsphotos_is_active_65702a06` (`is_active`),
  KEY `products_productsphotos_state_8bd2feb8` (`state`),
  KEY `products_productsphotos_parents_12f539e9` (`parents`),
  KEY `products_productsphotos_name_f19259af` (`name`),
  CONSTRAINT `products_productspho_product_id_1dd25946_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productsphotos`
--

LOCK TABLES `products_productsphotos` WRITE;
/*!40000 ALTER TABLE `products_productsphotos` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_productsphotos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_productsproperties`
--

DROP TABLE IF EXISTS `products_productsproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_productsproperties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `prop_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_productspro_product_id_50131a5d_fk_products_` (`product_id`),
  KEY `products_productspro_prop_id_4d9b9492_fk_products_` (`prop_id`),
  CONSTRAINT `products_productspro_product_id_50131a5d_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_products` (`id`),
  CONSTRAINT `products_productspro_prop_id_4d9b9492_fk_products_` FOREIGN KEY (`prop_id`) REFERENCES `products_propertiesvalues` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1906 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productsproperties`
--

LOCK TABLES `products_productsproperties` WRITE;
/*!40000 ALTER TABLE `products_productsproperties` DISABLE KEYS */;
INSERT INTO `products_productsproperties` VALUES (1277,67,156),(1278,67,157),(1279,67,158),(1280,67,159),(1281,67,160),(1282,67,161),(1283,67,162),(1284,67,163),(1285,67,164),(1286,67,165),(1287,68,156),(1288,68,166),(1289,68,167),(1290,68,159),(1291,68,160),(1292,68,161),(1293,68,168),(1294,68,163),(1295,68,164),(1296,68,169),(1297,69,156),(1298,69,157),(1299,69,158),(1300,69,159),(1301,69,170),(1302,69,161),(1303,69,171),(1304,69,172),(1305,69,164),(1306,69,173),(1307,70,174),(1308,70,175),(1309,70,176),(1310,70,177),(1311,70,178),(1312,70,161),(1313,70,171),(1314,70,172),(1315,70,164),(1316,70,179),(1317,70,180),(1318,71,156),(1319,71,157),(1320,71,158),(1321,71,159),(1322,71,181),(1323,71,161),(1324,71,182),(1325,71,172),(1326,71,164),(1327,71,183),(1328,72,156),(1329,72,184),(1330,72,185),(1331,72,159),(1332,72,160),(1333,72,161),(1334,72,186),(1335,72,172),(1336,72,164),(1337,72,187),(1338,73,156),(1339,73,188),(1340,73,189),(1341,73,159),(1342,73,160),(1343,73,161),(1344,73,190),(1345,73,163),(1346,73,164),(1347,73,191),(1348,74,156),(1349,74,192),(1350,74,185),(1351,74,159),(1352,74,181),(1353,74,161),(1354,74,196),(1355,74,172),(1356,74,164),(1357,74,197),(1358,75,174),(1359,75,192),(1360,75,193),(1361,75,177),(1362,75,178),(1363,75,161),(1364,75,194),(1365,75,172),(1366,75,164),(1367,75,179),(1368,75,195),(1369,76,156),(1370,76,198),(1371,76,189),(1372,76,199),(1373,76,160),(1374,76,200),(1375,76,201),(1376,76,163),(1377,76,164),(1378,76,202),(1379,77,156),(1380,77,203),(1381,77,204),(1382,77,159),(1383,77,181),(1384,77,161),(1385,77,205),(1386,77,172),(1387,77,164),(1388,77,206),(1389,78,156),(1390,78,207),(1391,78,208),(1392,78,159),(1393,78,181),(1394,78,161),(1395,78,171),(1396,78,172),(1397,78,164),(1398,78,209),(1399,79,156),(1400,79,157),(1401,79,158),(1402,79,199),(1403,79,181),(1404,79,161),(1405,79,210),(1406,79,172),(1407,79,164),(1408,79,211),(1409,80,156),(1410,80,212),(1411,80,213),(1412,80,159),(1413,80,181),(1414,80,161),(1415,80,171),(1416,80,172),(1417,80,164),(1418,80,214),(1419,81,156),(1420,81,184),(1421,81,185),(1422,81,199),(1423,81,160),(1424,81,161),(1425,81,186),(1426,81,172),(1427,81,164),(1428,81,215),(1429,82,156),(1430,82,216),(1431,82,217),(1432,82,159),(1433,82,181),(1434,82,161),(1435,82,182),(1436,82,172),(1437,82,164),(1438,82,211),(1439,83,174),(1440,83,218),(1441,83,158),(1442,83,177),(1443,83,178),(1444,83,161),(1445,83,219),(1446,83,172),(1447,83,164),(1448,83,179),(1449,83,220),(1450,84,156),(1451,84,198),(1452,84,189),(1453,84,177),(1454,84,170),(1455,84,200),(1456,84,221),(1457,84,163),(1458,84,222),(1459,85,174),(1460,85,223),(1461,85,158),(1462,85,177),(1463,85,178),(1464,85,161),(1465,85,171),(1466,85,172),(1467,85,164),(1468,85,179),(1469,85,224),(1470,86,174),(1471,86,223),(1472,86,158),(1473,86,225),(1474,86,178),(1475,86,161),(1476,86,171),(1477,86,172),(1478,86,164),(1479,86,179),(1480,86,224),(1481,87,174),(1482,87,226),(1483,87,167),(1484,87,177),(1485,87,170),(1486,87,161),(1487,87,227),(1488,87,163),(1489,87,164),(1490,87,179),(1491,87,228),(1492,88,156),(1493,88,212),(1494,88,213),(1495,88,199),(1496,88,181),(1497,88,161),(1498,88,171),(1499,88,172),(1500,88,164),(1501,88,214),(1502,89,174),(1503,89,184),(1504,89,237),(1505,89,159),(1506,89,178),(1507,89,161),(1508,89,194),(1509,89,172),(1510,89,164),(1511,89,179),(1512,89,238),(1513,90,174),(1514,90,229),(1515,90,230),(1516,90,177),(1517,90,231),(1518,90,161),(1519,90,232),(1520,90,163),(1521,90,164),(1522,90,179),(1523,90,233),(1524,91,156),(1525,91,203),(1526,91,234),(1527,91,159),(1528,91,181),(1529,91,161),(1530,91,235),(1531,91,172),(1532,91,164),(1533,91,236),(1534,92,156),(1535,92,207),(1536,92,208),(1537,92,199),(1538,92,181),(1539,92,161),(1540,92,171),(1541,92,172),(1542,92,164),(1543,92,209),(1544,93,156),(1545,93,166),(1546,93,176),(1547,93,159),(1548,93,181),(1549,93,161),(1550,93,235),(1551,93,172),(1552,93,164),(1553,93,239),(1554,94,174),(1555,94,241),(1556,94,242),(1557,94,159),(1558,94,178),(1559,94,161),(1560,94,205),(1561,94,172),(1562,94,164),(1563,94,179),(1564,94,243),(1565,95,156),(1566,95,184),(1567,95,237),(1568,95,159),(1569,95,181),(1570,95,161),(1571,95,194),(1572,95,172),(1573,95,164),(1574,95,240),(1575,96,156),(1576,96,188),(1577,96,189),(1578,96,177),(1579,96,170),(1580,96,200),(1581,96,190),(1582,96,163),(1583,96,244),(1584,97,156),(1585,97,241),(1586,97,245),(1587,97,159),(1588,97,181),(1589,97,161),(1590,97,205),(1591,97,172),(1592,97,164),(1593,97,246),(1594,98,156),(1595,98,188),(1596,98,247),(1597,98,159),(1598,98,181),(1599,98,161),(1600,98,248),(1601,98,172),(1602,98,164),(1603,98,249),(1604,99,156),(1605,99,250),(1606,99,251),(1607,99,159),(1608,99,161),(1609,99,252),(1610,99,253),(1611,100,156),(1612,100,254),(1613,100,255),(1614,100,159),(1615,100,181),(1616,100,161),(1617,100,256),(1618,100,172),(1619,100,164),(1620,100,257),(1621,101,156),(1622,101,157),(1623,101,158),(1624,101,199),(1625,101,160),(1626,101,161),(1627,101,258),(1628,101,163),(1629,101,164),(1630,101,165),(1631,102,156),(1632,102,259),(1633,102,260),(1634,102,159),(1635,102,181),(1636,102,161),(1637,102,219),(1638,102,172),(1639,102,164),(1640,102,261),(1641,103,156),(1642,103,262),(1643,103,204),(1644,103,159),(1645,103,181),(1646,103,161),(1647,103,235),(1648,103,172),(1649,103,164),(1650,103,263),(1651,104,174),(1652,104,264),(1653,104,265),(1654,104,159),(1655,104,178),(1656,104,161),(1657,104,235),(1658,104,172),(1659,104,164),(1660,104,179),(1661,104,266),(1662,105,156),(1663,105,267),(1664,105,268),(1665,105,159),(1666,105,181),(1667,105,161),(1668,105,219),(1669,105,172),(1670,105,164),(1671,105,269),(1672,106,156),(1673,106,188),(1674,106,189),(1675,106,199),(1676,106,160),(1677,106,200),(1678,106,190),(1679,106,163),(1680,106,164),(1681,106,191),(1682,107,270),(1683,107,157),(1684,107,158),(1685,107,177),(1686,107,170),(1687,107,161),(1688,107,258),(1689,107,163),(1690,107,164),(1691,107,271),(1692,107,272),(1693,108,174),(1694,108,203),(1695,108,204),(1696,108,159),(1697,108,178),(1698,108,161),(1699,108,205),(1700,108,172),(1701,108,164),(1702,108,179),(1703,108,266),(1704,109,273),(1705,109,157),(1706,109,268),(1707,109,159),(1708,109,231),(1709,109,274),(1710,109,275),(1711,109,163),(1712,109,276),(1713,110,156),(1714,110,277),(1715,110,278),(1716,110,159),(1717,110,181),(1718,110,161),(1719,110,279),(1720,110,172),(1721,110,164),(1722,110,280),(1723,111,156),(1724,111,166),(1725,111,176),(1726,111,159),(1727,111,181),(1728,111,161),(1729,111,205),(1730,111,172),(1731,111,164),(1732,111,239),(1733,112,174),(1734,112,284),(1735,112,237),(1736,112,159),(1737,112,178),(1738,112,161),(1739,112,256),(1740,112,172),(1741,112,164),(1742,112,179),(1743,112,285),(1744,113,174),(1745,113,286),(1746,113,287),(1747,113,199),(1748,113,178),(1749,113,161),(1750,113,219),(1751,113,172),(1752,113,164),(1753,113,179),(1754,113,288),(1755,114,174),(1756,114,157),(1757,114,281),(1758,114,159),(1759,114,170),(1760,114,161),(1761,114,282),(1762,114,163),(1763,114,164),(1764,114,179),(1765,114,283),(1766,115,270),(1767,115,157),(1768,115,158),(1769,115,199),(1770,115,161),(1771,115,171),(1772,115,173),(1773,116,270),(1774,116,157),(1775,116,158),(1776,116,159),(1777,116,161),(1778,116,258),(1779,116,163),(1780,116,289),(1781,117,270),(1782,117,192),(1783,117,185),(1784,117,159),(1785,117,161),(1786,117,194),(1787,117,292),(1788,118,273),(1789,118,157),(1790,118,290),(1791,118,159),(1792,118,178),(1793,118,274),(1794,118,171),(1795,118,291),(1796,119,270),(1797,119,157),(1798,119,158),(1799,119,159),(1800,119,161),(1801,119,171),(1802,119,293),(1803,120,156),(1804,120,284),(1805,120,237),(1806,120,159),(1807,120,181),(1808,120,161),(1809,120,256),(1810,120,172),(1811,120,164),(1812,120,296),(1813,121,174),(1814,121,262),(1815,121,294),(1816,121,177),(1817,121,178),(1818,121,161),(1819,121,235),(1820,121,172),(1821,121,164),(1822,121,179),(1823,121,295),(1824,122,270),(1825,122,157),(1826,122,158),(1827,122,159),(1828,122,161),(1829,122,182),(1830,122,293),(1831,123,156),(1832,123,184),(1833,123,294),(1834,123,159),(1835,123,181),(1836,123,161),(1837,123,194),(1838,123,172),(1839,123,164),(1840,123,297),(1841,124,156),(1842,124,203),(1843,124,204),(1844,124,199),(1845,124,181),(1846,124,161),(1847,124,205),(1848,124,172),(1849,124,164),(1850,124,206),(1851,125,270),(1852,125,284),(1853,125,237),(1854,125,159),(1855,125,161),(1856,125,256),(1857,125,298),(1858,126,273),(1859,126,223),(1860,126,299),(1861,126,159),(1862,126,178),(1863,126,274),(1864,126,182),(1865,126,300),(1866,127,174),(1867,127,203),(1868,127,204),(1869,127,199),(1870,127,178),(1871,127,161),(1872,127,205),(1873,127,172),(1874,127,164),(1875,127,179),(1876,127,266),(1877,128,156),(1878,128,301),(1879,128,302),(1880,128,159),(1881,128,170),(1882,128,303),(1883,128,304),(1884,128,172),(1885,128,305),(1886,128,179),(1887,128,306),(1888,129,307),(1889,129,284),(1890,129,308),(1891,129,177),(1892,129,170),(1893,129,161),(1894,129,309),(1895,129,163),(1896,129,310),(1897,130,273),(1898,130,229),(1899,130,311),(1900,130,159),(1901,130,231),(1902,130,274),(1903,130,312),(1904,130,163),(1905,130,313);
/*!40000 ALTER TABLE `products_productsproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_propertiesvalues`
--

DROP TABLE IF EXISTS `products_propertiesvalues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_propertiesvalues` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `str_value` varchar(255) DEFAULT NULL,
  `prop_id` int(11) NOT NULL,
  `digit_value` decimal(13,4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_propertiesv_prop_id_45598b2c_fk_products_` (`prop_id`),
  KEY `products_propertiesvalues_img_45d2822c` (`img`),
  KEY `products_propertiesvalues_created_9d9eb660` (`created`),
  KEY `products_propertiesvalues_updated_08b8a80f` (`updated`),
  KEY `products_propertiesvalues_position_fe4565de` (`position`),
  KEY `products_propertiesvalues_is_active_74e17f76` (`is_active`),
  KEY `products_propertiesvalues_state_7e4300c9` (`state`),
  KEY `products_propertiesvalues_parents_4c64ff20` (`parents`),
  KEY `products_propertiesvalues_str_value_483ecc58` (`str_value`),
  KEY `products_propertiesvalues_digit_value_98cb8771` (`digit_value`),
  CONSTRAINT `products_propertiesv_prop_id_45598b2c_fk_products_` FOREIGN KEY (`prop_id`) REFERENCES `products_property` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=314 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_propertiesvalues`
--

LOCK TABLES `products_propertiesvalues` WRITE;
/*!40000 ALTER TABLE `products_propertiesvalues` DISABLE KEYS */;
INSERT INTO `products_propertiesvalues` VALUES (156,NULL,'2020-05-07 13:12:14.581592','2020-05-07 13:12:14.581616',1,1,NULL,NULL,'Bosch',1,NULL),(157,NULL,'2020-05-07 13:12:14.588633','2020-05-07 13:12:14.588668',2,1,NULL,NULL,'60',2,60.0000),(158,NULL,'2020-05-07 13:12:14.620186','2020-05-07 13:12:14.620213',3,1,NULL,NULL,'540',3,540.0000),(159,NULL,'2020-05-07 13:12:14.631350','2020-05-07 13:12:14.631372',4,1,NULL,NULL,'обратная',4,NULL),(160,NULL,'2020-05-07 13:12:14.636811','2020-05-07 13:12:14.636831',5,1,NULL,NULL,'Верхняя планка',5,NULL),(161,NULL,'2020-05-07 13:12:14.641745','2020-05-07 13:12:14.641766',6,1,NULL,NULL,'T1',6,NULL),(162,NULL,'2020-05-07 13:12:14.646681','2020-05-07 13:12:14.646701',7,1,NULL,NULL,'232x175x225',7,NULL),(163,NULL,'2020-05-07 13:12:14.652344','2020-05-07 13:12:14.652371',8,1,NULL,NULL,'да',8,NULL),(164,NULL,'2020-05-07 13:12:14.657661','2020-05-07 13:12:14.657685',9,1,NULL,NULL,'Нет',9,NULL),(165,NULL,'2020-05-07 13:12:14.662711','2020-05-07 13:12:14.662733',10,1,NULL,NULL,'14,54',10,NULL),(166,NULL,'2020-05-07 13:12:14.675898','2020-05-07 13:12:14.675922',11,1,NULL,NULL,'70',2,70.0000),(167,NULL,'2020-05-07 13:12:14.681042','2020-05-07 13:12:14.681065',12,1,NULL,NULL,'630',3,630.0000),(168,NULL,'2020-05-07 13:12:14.698509','2020-05-07 13:12:14.698533',13,1,NULL,NULL,'261x175x220',7,NULL),(169,NULL,'2020-05-07 13:12:14.712194','2020-05-07 13:12:14.712220',14,1,NULL,NULL,'17,32',10,NULL),(170,NULL,'2020-05-07 13:12:14.737176','2020-05-07 13:12:14.737202',15,1,NULL,NULL,'B00',5,NULL),(171,NULL,'2020-05-07 13:12:14.746332','2020-05-07 13:12:14.746355',16,1,NULL,NULL,'242x175x190',7,NULL),(172,NULL,'2020-05-07 13:12:14.752019','2020-05-07 13:12:14.752044',17,1,NULL,NULL,'Нет',8,NULL),(173,NULL,'2020-05-07 13:12:14.761224','2020-05-07 13:12:14.761247',18,1,NULL,NULL,'14,89',10,NULL),(174,NULL,'2020-05-07 13:12:14.769873','2020-05-07 13:12:14.769897',19,1,NULL,NULL,'Exide',1,NULL),(175,NULL,'2020-05-07 13:12:14.775088','2020-05-07 13:12:14.775111',20,1,NULL,NULL,'64',2,64.0000),(176,NULL,'2020-05-07 13:12:14.780244','2020-05-07 13:12:14.780266',21,1,NULL,NULL,'640',3,640.0000),(177,NULL,'2020-05-07 13:12:14.785928','2020-05-07 13:12:14.785953',22,1,NULL,NULL,'0',4,0.0000),(178,NULL,'2020-05-07 13:12:14.791201','2020-05-07 13:12:14.791225',23,1,NULL,NULL,'B13',5,NULL),(179,NULL,'2020-05-07 13:12:14.812612','2020-05-07 13:12:14.812636',24,1,NULL,NULL,'Да',11,NULL),(180,NULL,'2020-05-07 13:12:14.818160','2020-05-07 13:12:14.818186',25,1,NULL,NULL,'16,4',10,NULL),(181,NULL,'2020-05-07 13:12:14.843132','2020-05-07 13:12:14.843157',26,1,NULL,NULL,'Универсальный',5,NULL),(182,NULL,'2020-05-07 13:12:14.852558','2020-05-07 13:12:14.852594',27,1,NULL,NULL,'242x175x175',7,NULL),(183,NULL,'2020-05-07 13:12:14.865725','2020-05-07 13:12:14.865749',28,1,NULL,NULL,'13,89',10,NULL),(184,NULL,'2020-05-07 13:12:14.878369','2020-05-07 13:12:14.878391',29,1,NULL,NULL,'95',2,95.0000),(185,NULL,'2020-05-07 13:12:14.883649','2020-05-07 13:12:14.883677',30,1,NULL,NULL,'830',3,830.0000),(186,NULL,'2020-05-07 13:12:14.902053','2020-05-07 13:12:14.902084',31,1,NULL,NULL,'306x173x225',7,NULL),(187,NULL,'2020-05-07 13:12:14.914970','2020-05-07 13:12:14.914990',32,1,NULL,NULL,'20,23',10,NULL),(188,NULL,'2020-05-07 13:12:14.927368','2020-05-07 13:12:14.927391',33,1,NULL,NULL,'45',2,45.0000),(189,NULL,'2020-05-07 13:12:14.932507','2020-05-07 13:12:14.932529',34,1,NULL,NULL,'330',3,330.0000),(190,NULL,'2020-05-07 13:12:14.950447','2020-05-07 13:12:14.950473',35,1,NULL,NULL,'238x129x227',7,NULL),(191,NULL,'2020-05-07 13:12:14.963825','2020-05-07 13:12:14.963849',36,1,NULL,NULL,'13,1',10,NULL),(192,NULL,'2020-05-07 13:12:14.976866','2020-05-07 13:12:14.976891',37,1,NULL,NULL,'100',2,100.0000),(193,NULL,'2020-05-07 13:12:14.982016','2020-05-07 13:12:14.982040',38,1,NULL,NULL,'900',3,900.0000),(194,NULL,'2020-05-07 13:12:14.999356','2020-05-07 13:12:14.999381',39,1,NULL,NULL,'353x175x190',7,NULL),(195,NULL,'2020-05-07 13:12:15.017422','2020-05-07 13:12:15.017449',40,1,NULL,NULL,'22,5',10,NULL),(196,NULL,'2020-05-07 13:12:15.050256','2020-05-07 13:12:15.050283',41,1,NULL,NULL,'353x190x175',7,NULL),(197,NULL,'2020-05-07 13:12:15.063634','2020-05-07 13:12:15.063658',42,1,NULL,NULL,'21,92',10,NULL),(198,NULL,'2020-05-07 13:12:15.076616','2020-05-07 13:12:15.076642',43,1,NULL,NULL,'40',2,40.0000),(199,NULL,'2020-05-07 13:12:15.086175','2020-05-07 13:12:15.086200',44,1,NULL,NULL,'прямая',4,NULL),(200,NULL,'2020-05-07 13:12:15.095327','2020-05-07 13:12:15.095350',45,1,NULL,NULL,'T3',6,NULL),(201,NULL,'2020-05-07 13:12:15.100871','2020-05-07 13:12:15.100897',46,1,NULL,NULL,'187x227x127',7,NULL),(202,NULL,'2020-05-07 13:12:15.113960','2020-05-07 13:12:15.113983',47,1,NULL,NULL,'10,1',10,NULL),(203,NULL,'2020-05-07 13:12:15.126677','2020-05-07 13:12:15.126703',48,1,NULL,NULL,'74',2,74.0000),(204,NULL,'2020-05-07 13:12:15.131824','2020-05-07 13:12:15.131846',49,1,NULL,NULL,'680',3,680.0000),(205,NULL,'2020-05-07 13:12:15.149905','2020-05-07 13:12:15.149931',50,1,NULL,NULL,'278x175x190',7,NULL),(206,NULL,'2020-05-07 13:12:15.163977','2020-05-07 13:12:15.164001',51,1,NULL,NULL,'17,87',10,NULL),(207,NULL,'2020-05-07 13:12:15.176598','2020-05-07 13:12:15.176624',52,1,NULL,NULL,'56',2,56.0000),(208,NULL,'2020-05-07 13:12:15.181747','2020-05-07 13:12:15.181770',53,1,NULL,NULL,'480',3,480.0000),(209,NULL,'2020-05-07 13:12:15.211904','2020-05-07 13:12:15.211929',54,1,NULL,NULL,'13,7',10,NULL),(210,NULL,'2020-05-07 13:12:15.244704','2020-05-07 13:12:15.244729',55,1,NULL,NULL,'242x175x1790',7,NULL),(211,NULL,'2020-05-07 13:12:15.258655','2020-05-07 13:12:15.258680',56,1,NULL,NULL,'14,34',10,NULL),(212,NULL,'2020-05-07 13:12:15.271402','2020-05-07 13:12:15.271427',57,1,NULL,NULL,'63',2,63.0000),(213,NULL,'2020-05-07 13:12:15.276606','2020-05-07 13:12:15.276630',58,1,NULL,NULL,'610',3,610.0000),(214,NULL,'2020-05-07 13:12:15.307575','2020-05-07 13:12:15.307605',59,1,NULL,NULL,'14,78',10,NULL),(215,NULL,'2020-05-07 13:12:15.352537','2020-05-07 13:12:15.352563',60,1,NULL,NULL,'22,21',10,NULL),(216,NULL,'2020-05-07 13:12:15.364840','2020-05-07 13:12:15.364862',61,1,NULL,NULL,'61',2,61.0000),(217,NULL,'2020-05-07 13:12:15.370478','2020-05-07 13:12:15.370502',62,1,NULL,NULL,'600',3,600.0000),(218,NULL,'2020-05-07 13:12:15.411829','2020-05-07 13:12:15.411854',63,1,NULL,NULL,'53',2,53.0000),(219,NULL,'2020-05-07 13:12:15.433734','2020-05-07 13:12:15.433780',64,1,NULL,NULL,'207x175x190',7,NULL),(220,NULL,'2020-05-07 13:12:15.451363','2020-05-07 13:12:15.451387',65,1,NULL,NULL,'13',10,13.0000),(221,NULL,'2020-05-07 13:12:15.484645','2020-05-07 13:12:15.484671',66,1,NULL,NULL,'187x127x227',7,NULL),(222,NULL,'2020-05-07 13:12:15.494250','2020-05-07 13:12:15.494274',67,1,NULL,NULL,'10',10,10.0000),(223,NULL,'2020-05-07 13:12:15.507432','2020-05-07 13:12:15.507459',68,1,NULL,NULL,'62',2,62.0000),(224,NULL,'2020-05-07 13:12:15.545884','2020-05-07 13:12:15.545909',69,1,NULL,NULL,'15,8',10,NULL),(225,NULL,'2020-05-07 13:12:15.566849','2020-05-07 13:12:15.566874',70,1,NULL,NULL,'1',4,1.0000),(226,NULL,'2020-05-07 13:12:15.608857','2020-05-07 13:12:15.608882',71,1,NULL,NULL,'75',2,75.0000),(227,NULL,'2020-05-07 13:12:15.630768','2020-05-07 13:12:15.630794',72,1,NULL,NULL,'258x170x225',7,NULL),(228,NULL,'2020-05-07 13:12:15.648487','2020-05-07 13:12:15.648513',73,1,NULL,NULL,'18,9',10,NULL),(229,NULL,'2020-05-07 13:12:15.709348','2020-05-07 13:12:15.709369',74,1,NULL,NULL,'65',2,65.0000),(230,NULL,'2020-05-07 13:12:15.715801','2020-05-07 13:12:15.715821',75,1,NULL,NULL,'580',3,580.0000),(231,NULL,'2020-05-07 13:12:15.725710','2020-05-07 13:12:15.725731',76,1,NULL,NULL,'B01',5,NULL),(232,NULL,'2020-05-07 13:12:15.735282','2020-05-07 13:12:15.735303',77,1,NULL,NULL,'230x170x225',7,NULL),(233,NULL,'2020-05-07 13:12:15.752733','2020-05-07 13:12:15.752760',78,1,NULL,NULL,'16,2',10,NULL),(234,NULL,'2020-05-07 13:12:15.812371','2020-05-07 13:12:15.812395',79,1,NULL,NULL,'750',3,750.0000),(235,NULL,'2020-05-07 13:12:15.830022','2020-05-07 13:12:15.830047',80,1,NULL,NULL,'278x175x175',7,NULL),(236,NULL,'2020-05-07 13:12:15.843706','2020-05-07 13:12:15.843731',81,1,NULL,NULL,'17,11',10,NULL),(237,NULL,'2020-05-07 13:12:15.860609','2020-05-07 13:12:15.860634',82,1,NULL,NULL,'800',3,800.0000),(238,NULL,'2020-05-07 13:12:15.894440','2020-05-07 13:12:15.894466',83,1,NULL,NULL,'22,9',10,NULL),(239,NULL,'2020-05-07 13:12:15.939738','2020-05-07 13:12:15.939763',84,1,NULL,NULL,'16,75',10,NULL),(240,NULL,'2020-05-07 13:12:15.985176','2020-05-07 13:12:15.985202',85,1,NULL,NULL,'21,32',10,NULL),(241,NULL,'2020-05-07 13:12:15.997595','2020-05-07 13:12:15.997618',86,1,NULL,NULL,'77',2,77.0000),(242,NULL,'2020-05-07 13:12:16.003648','2020-05-07 13:12:16.003674',87,1,NULL,NULL,'760',3,760.0000),(243,NULL,'2020-05-07 13:12:16.041741','2020-05-07 13:12:16.041767',88,1,NULL,NULL,'18',10,18.0000),(244,NULL,'2020-05-07 13:12:16.081967','2020-05-07 13:12:16.081993',89,1,NULL,NULL,'11',10,11.0000),(245,NULL,'2020-05-07 13:12:16.099153','2020-05-07 13:12:16.099177',90,1,NULL,NULL,'780',3,780.0000),(246,NULL,'2020-05-07 13:12:16.129981','2020-05-07 13:12:16.130008',91,1,NULL,NULL,'17,94',10,NULL),(247,NULL,'2020-05-07 13:12:16.146683','2020-05-07 13:12:16.146703',92,1,NULL,NULL,'400',3,400.0000),(248,NULL,'2020-05-07 13:12:16.168103','2020-05-07 13:12:16.168131',93,1,NULL,NULL,'207x190x175',7,NULL),(249,NULL,'2020-05-07 13:12:16.181378','2020-05-07 13:12:16.181399',94,1,NULL,NULL,'11,43',10,NULL),(250,NULL,'2020-05-07 13:12:16.193620','2020-05-07 13:12:16.193644',95,1,NULL,NULL,'44',2,44.0000),(251,NULL,'2020-05-07 13:12:16.198744','2020-05-07 13:12:16.198766',96,1,NULL,NULL,'440',3,440.0000),(252,NULL,'2020-05-07 13:12:16.213136','2020-05-07 13:12:16.213161',97,1,NULL,NULL,'207x175x175',7,NULL),(253,NULL,'2020-05-07 13:12:16.218815','2020-05-07 13:12:16.218841',98,1,NULL,NULL,'11,68',10,NULL),(254,NULL,'2020-05-07 13:12:16.231160','2020-05-07 13:12:16.231184',99,1,NULL,NULL,'80',2,80.0000),(255,NULL,'2020-05-07 13:12:16.236789','2020-05-07 13:12:16.236814',100,1,NULL,NULL,'740',3,740.0000),(256,NULL,'2020-05-07 13:12:16.254457','2020-05-07 13:12:16.254482',101,1,NULL,NULL,'315x175x175',7,NULL),(257,NULL,'2020-05-07 13:12:16.268031','2020-05-07 13:12:16.268056',102,1,NULL,NULL,'19,21',10,NULL),(258,NULL,'2020-05-07 13:12:16.301071','2020-05-07 13:12:16.301098',103,1,NULL,NULL,'232x173x225',7,NULL),(259,NULL,'2020-05-07 13:12:16.325990','2020-05-07 13:12:16.326014',104,1,NULL,NULL,'52',2,52.0000),(260,NULL,'2020-05-07 13:12:16.331164','2020-05-07 13:12:16.331187',105,1,NULL,NULL,'470',3,470.0000),(261,NULL,'2020-05-07 13:12:16.364586','2020-05-07 13:12:16.364610',106,1,NULL,NULL,'12,4',10,NULL),(262,NULL,'2020-05-07 13:12:16.377169','2020-05-07 13:12:16.377189',107,1,NULL,NULL,'72',2,72.0000),(263,NULL,'2020-05-07 13:12:16.410220','2020-05-07 13:12:16.410245',108,1,NULL,NULL,'17,05',10,NULL),(264,NULL,'2020-05-07 13:12:16.423138','2020-05-07 13:12:16.423164',109,1,NULL,NULL,'71',2,71.0000),(265,NULL,'2020-05-07 13:12:16.428249','2020-05-07 13:12:16.428271',110,1,NULL,NULL,'670',3,670.0000),(266,NULL,'2020-05-07 13:12:16.462560','2020-05-07 13:12:16.462586',111,1,NULL,NULL,'17',10,17.0000),(267,NULL,'2020-05-07 13:12:16.475765','2020-05-07 13:12:16.475789',112,1,NULL,NULL,'54',2,54.0000),(268,NULL,'2020-05-07 13:12:16.480842','2020-05-07 13:12:16.480864',113,1,NULL,NULL,'530',3,530.0000),(269,NULL,'2020-05-07 13:12:16.514472','2020-05-07 13:12:16.514497',114,1,NULL,NULL,'13,4',10,NULL),(270,NULL,'2020-05-07 13:12:16.566794','2020-05-07 13:12:16.566820',115,1,NULL,NULL,'Varta',1,NULL),(271,NULL,'2020-05-07 13:12:16.604885','2020-05-07 13:12:16.604910',116,1,NULL,NULL,'V2',11,NULL),(272,NULL,'2020-05-07 13:12:16.610005','2020-05-07 13:12:16.610028',117,1,NULL,NULL,'14',10,14.0000),(273,NULL,'2020-05-07 13:12:16.670122','2020-05-07 13:12:16.670141',118,1,NULL,NULL,'Алькор',1,NULL),(274,NULL,'2020-05-07 13:12:16.691503','2020-05-07 13:12:16.691529',119,1,NULL,NULL,'Европа',6,NULL),(275,NULL,'2020-05-07 13:12:16.696629','2020-05-07 13:12:16.696652',120,1,NULL,NULL,'230x173x221',7,NULL),(276,NULL,'2020-05-07 13:12:16.706280','2020-05-07 13:12:16.706305',121,1,NULL,NULL,'16,3',10,NULL),(277,NULL,'2020-05-07 13:12:16.719068','2020-05-07 13:12:16.719094',122,1,NULL,NULL,'110',2,110.0000),(278,NULL,'2020-05-07 13:12:16.724375','2020-05-07 13:12:16.724398',123,1,NULL,NULL,'920',3,920.0000),(279,NULL,'2020-05-07 13:12:16.742099','2020-05-07 13:12:16.742124',124,1,NULL,NULL,'393x190x175',7,NULL),(280,NULL,'2020-05-07 13:12:16.756164','2020-05-07 13:12:16.756189',125,1,NULL,NULL,'25,1',10,NULL),(281,NULL,'2020-05-07 13:12:16.807545','2020-05-07 13:12:16.807565',126,1,NULL,NULL,'390',3,390.0000),(282,NULL,'2020-05-07 13:12:16.824235','2020-05-07 13:12:16.824254',127,1,NULL,NULL,'230X172X220',7,NULL),(283,NULL,'2020-05-07 13:12:16.842105','2020-05-07 13:12:16.842130',128,1,NULL,NULL,'16',10,16.0000),(284,NULL,'2020-05-07 13:12:16.855164','2020-05-07 13:12:16.855189',129,1,NULL,NULL,'85',2,85.0000),(285,NULL,'2020-05-07 13:12:16.894069','2020-05-07 13:12:16.894107',130,1,NULL,NULL,'19,6',10,NULL),(286,NULL,'2020-05-07 13:12:16.909935','2020-05-07 13:12:16.909956',131,1,NULL,NULL,'50',2,50.0000),(287,NULL,'2020-05-07 13:12:16.915206','2020-05-07 13:12:16.915227',132,1,NULL,NULL,'450',3,450.0000),(288,NULL,'2020-05-07 13:12:16.948794','2020-05-07 13:12:16.948820',133,1,NULL,NULL,'12',10,12.0000),(289,NULL,'2020-05-07 13:12:17.030879','2020-05-07 13:12:17.030905',134,1,NULL,NULL,'16,13',10,NULL),(290,NULL,'2020-05-07 13:12:17.047577','2020-05-07 13:12:17.047601',135,1,NULL,NULL,'510',3,510.0000),(291,NULL,'2020-05-07 13:12:17.069660','2020-05-07 13:12:17.069686',136,1,NULL,NULL,'16,7',10,NULL),(292,NULL,'2020-05-07 13:12:17.103027','2020-05-07 13:12:17.103053',137,1,NULL,NULL,'23,17',10,NULL),(293,NULL,'2020-05-07 13:12:17.136054','2020-05-07 13:12:17.136079',138,1,NULL,NULL,'14,45',10,NULL),(294,NULL,'2020-05-07 13:12:17.152968','2020-05-07 13:12:17.152992',139,1,NULL,NULL,'720',3,720.0000),(295,NULL,'2020-05-07 13:12:17.187055','2020-05-07 13:12:17.187081',140,1,NULL,NULL,'17,8',10,NULL),(296,NULL,'2020-05-07 13:12:17.232182','2020-05-07 13:12:17.232207',141,1,NULL,NULL,'19,02',10,NULL),(297,NULL,'2020-05-07 13:12:17.309588','2020-05-07 13:12:17.309613',142,1,NULL,NULL,'20,78',10,NULL),(298,NULL,'2020-05-07 13:12:17.435684','2020-05-07 13:12:17.435710',143,1,NULL,NULL,'20,13',10,NULL),(299,NULL,'2020-05-07 13:12:17.452767','2020-05-07 13:12:17.452791',144,1,NULL,NULL,'620',3,620.0000),(300,NULL,'2020-05-07 13:12:17.474006','2020-05-07 13:12:17.474031',145,1,NULL,NULL,'14,6',10,NULL),(301,NULL,'2020-05-07 13:12:17.487070','2020-05-07 13:12:17.487094',146,1,NULL,NULL,'7',2,7.0000),(302,NULL,'2020-05-07 13:12:17.491990','2020-05-07 13:12:17.492009',147,1,NULL,NULL,'110',3,110.0000),(303,NULL,'2020-05-07 13:12:17.505149','2020-05-07 13:12:17.505174',148,1,NULL,NULL,'Под болт',6,NULL),(304,NULL,'2020-05-07 13:12:17.510226','2020-05-07 13:12:17.510248',149,1,NULL,NULL,'113x70x105',7,NULL),(305,NULL,'2020-05-07 13:12:17.520116','2020-05-07 13:12:17.520143',150,1,NULL,NULL,'да',9,NULL),(306,NULL,'2020-05-07 13:12:17.529430','2020-05-07 13:12:17.529454',151,1,NULL,NULL,'2,1',10,NULL),(307,NULL,'2020-05-07 13:12:17.538467','2020-05-07 13:12:17.538492',152,1,NULL,NULL,'Solite',1,NULL),(308,NULL,'2020-05-07 13:12:17.547836','2020-05-07 13:12:17.547860',153,1,NULL,NULL,'650',3,650.0000),(309,NULL,'2020-05-07 13:12:17.565796','2020-05-07 13:12:17.565820',154,1,NULL,NULL,'260x168x220',7,NULL),(310,NULL,'2020-05-07 13:12:17.574994','2020-05-07 13:12:17.575020',155,1,NULL,NULL,'18,2',10,NULL),(311,NULL,'2020-05-10 15:50:08.892065','2020-05-10 15:50:08.892090',156,1,NULL,NULL,'590',3,590.0000),(312,NULL,'2020-05-10 15:50:08.928682','2020-05-10 15:50:08.928706',157,1,NULL,NULL,'230x173x220',7,NULL),(313,NULL,'2020-05-10 15:50:08.938149','2020-05-10 15:50:08.938174',158,1,NULL,NULL,'17,3',10,17.3000);
/*!40000 ALTER TABLE `products_propertiesvalues` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_property`
--

DROP TABLE IF EXISTS `products_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_property` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `ptype` int(11) DEFAULT NULL,
  `code` varchar(255) DEFAULT NULL,
  `measure` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_property_img_d69874df` (`img`),
  KEY `products_property_created_357be73e` (`created`),
  KEY `products_property_updated_4d692374` (`updated`),
  KEY `products_property_position_5551b555` (`position`),
  KEY `products_property_is_active_c101d4e8` (`is_active`),
  KEY `products_property_state_b069dbb9` (`state`),
  KEY `products_property_parents_4f8d9c8c` (`parents`),
  KEY `products_property_name_5d6be2ec` (`name`),
  KEY `products_property_ptype_2dd430a0` (`ptype`),
  KEY `products_property_code_7453be39` (`code`),
  KEY `products_property_measure_5824486e` (`measure`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_property`
--

LOCK TABLES `products_property` WRITE;
/*!40000 ALTER TABLE `products_property` DISABLE KEYS */;
INSERT INTO `products_property` VALUES (1,NULL,'2020-05-07 10:27:58.798546','2020-05-07 10:27:58.798573',1,1,NULL,NULL,'Производитель:',NULL,'Make',NULL),(2,NULL,'2020-05-07 10:27:58.821467','2020-05-07 10:27:58.821491',2,1,NULL,NULL,'Емкость:',NULL,'Capacity','А/ч'),(3,NULL,'2020-05-07 10:27:58.828566','2020-05-07 10:27:58.828586',3,1,NULL,NULL,'Пусковой ток:',NULL,'StartupCurrent','A'),(4,NULL,'2020-05-07 10:27:58.837042','2020-05-07 10:27:58.837070',4,1,NULL,NULL,'Полярность:',NULL,'Polarity',NULL),(5,NULL,'2020-05-07 10:27:58.843530','2020-05-07 10:27:58.843550',5,1,NULL,NULL,'Тип крепления:',NULL,'MountType',NULL),(6,NULL,'2020-05-07 10:27:58.849726','2020-05-07 10:27:58.849746',6,1,NULL,NULL,'Тип клемм:',NULL,'TerminalType',NULL),(7,NULL,'2020-05-07 10:27:58.855758','2020-05-07 10:27:58.855777',7,1,NULL,NULL,'Габариты:',NULL,'Dimensions','мм'),(8,NULL,'2020-05-07 10:27:58.861731','2020-05-07 10:27:58.861753',8,1,NULL,NULL,'Азиатский тип:',NULL,'AsianType',NULL),(9,NULL,'2020-05-07 10:27:58.868738','2020-05-07 10:27:58.868764',9,1,NULL,NULL,'Технология AGM:',NULL,'AgmTechnology',NULL),(10,NULL,'2020-05-07 10:27:58.874994','2020-05-07 10:27:58.875014',10,1,NULL,NULL,'Вес залитого:',NULL,'FilledWeight','кг'),(11,NULL,'2020-05-07 10:27:59.028128','2020-05-07 10:27:59.028154',11,1,NULL,NULL,'Устойчивость к вибрации:',NULL,'VibrationResistance',NULL);
/*!40000 ALTER TABLE `products_property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotion_svisits`
--

DROP TABLE IF EXISTS `promotion_svisits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotion_svisits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  `profile` varchar(255) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `ip` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `promotion_svisits_img_2032e608` (`img`),
  KEY `promotion_svisits_created_8112873c` (`created`),
  KEY `promotion_svisits_updated_d0c6fb3e` (`updated`),
  KEY `promotion_svisits_position_ef76d277` (`position`),
  KEY `promotion_svisits_is_active_ac0d3ae1` (`is_active`),
  KEY `promotion_svisits_state_bf81e8ce` (`state`),
  KEY `promotion_svisits_parents_9a1610ec` (`parents`),
  KEY `promotion_svisits_date_3d4538a0` (`date`),
  KEY `promotion_svisits_company_id_c37a79b0` (`company_id`),
  KEY `promotion_svisits_profile_ba9e618c` (`profile`),
  KEY `promotion_svisits_count_ac15f839` (`count`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotion_svisits`
--

LOCK TABLES `promotion_svisits` WRITE;
/*!40000 ALTER TABLE `promotion_svisits` DISABLE KEYS */;
INSERT INTO `promotion_svisits` VALUES (3,NULL,'2020-05-06 15:11:47.876973','2020-05-06 15:42:07.921907',2,1,NULL,NULL,'2020-04-04',92126,'bertolia',1,'http://localhost:8000'),(4,NULL,'2020-05-06 15:11:47.885714','2020-05-06 15:42:07.950022',3,1,NULL,NULL,'2020-04-04',360,'bertolia',1,'http://localhost:8000'),(5,NULL,'2020-05-06 15:11:47.896162','2020-05-06 15:42:07.952409',4,1,NULL,NULL,'2020-04-04',5494,'bertolia',1,'http://localhost:8000'),(6,NULL,'2020-05-06 15:11:47.899158','2020-05-06 15:42:07.955705',5,1,NULL,NULL,'2020-04-04',5499,'bertolia',1,'http://localhost:8000'),(7,NULL,'2020-05-06 15:11:47.901629','2020-05-06 15:42:07.958041',6,1,NULL,NULL,'2020-04-04',86836,'bertolia',1,'http://localhost:8000'),(8,NULL,'2020-05-06 15:11:47.904014','2020-05-06 15:42:07.960394',7,1,NULL,NULL,'2020-04-04',86837,'osyashig',1,'http://localhost:8000'),(9,NULL,'2020-05-06 15:11:47.906457','2020-05-06 15:42:07.971082',8,1,NULL,NULL,'2020-04-04',86904,'osyashig',1,'http://localhost:8000'),(10,NULL,'2020-05-06 15:11:47.908753','2020-05-06 15:42:07.973795',9,1,NULL,NULL,'2020-04-04',86907,'osyashig',1,'http://localhost:8000'),(11,NULL,'2020-05-06 15:11:47.911180','2020-05-06 15:42:07.976326',10,1,NULL,NULL,'2020-04-04',86925,'osyashig',1,'http://localhost:8000'),(12,NULL,'2020-05-06 15:11:47.913587','2020-05-06 15:42:07.978622',11,1,NULL,NULL,'2020-04-04',86926,'osyashig',1,'http://localhost:8000'),(13,NULL,'2020-05-06 15:11:47.916852','2020-05-06 15:42:07.980830',12,1,NULL,NULL,'2020-04-04',110640,'osyashig',1,'http://localhost:8000'),(14,NULL,'2020-05-06 15:11:47.919356','2020-05-06 15:42:07.983035',13,1,NULL,NULL,'2020-04-04',110751,'osyashig',1,'http://localhost:8000'),(15,NULL,'2020-05-06 15:11:47.921910','2020-05-06 15:42:07.985440',14,1,NULL,NULL,'2020-04-04',110759,'osyashig',1,'http://localhost:8000'),(16,NULL,'2020-05-06 15:11:47.924438','2020-05-06 15:42:07.987866',15,1,NULL,NULL,'2020-04-04',111125,'osyashig',1,'http://localhost:8000'),(17,NULL,'2020-05-06 15:11:47.926861','2020-05-06 15:42:07.990086',16,1,NULL,NULL,'2020-04-04',111624,'osyashig',1,'http://localhost:8000'),(18,NULL,'2020-05-06 15:11:47.929289','2020-05-06 15:42:07.992436',17,1,NULL,NULL,'2020-04-04',92126,'bbugoga14',1,'http://localhost:8000'),(19,NULL,'2020-05-06 15:11:47.931837','2020-05-06 15:42:07.994959',18,1,NULL,NULL,'2020-04-04',360,'bbugoga14',1,'http://localhost:8000'),(20,NULL,'2020-05-06 15:11:47.934370','2020-05-06 15:42:07.997396',19,1,NULL,NULL,'2020-04-04',5494,'bbugoga14',1,'http://localhost:8000'),(21,NULL,'2020-05-06 15:11:47.936805','2020-05-06 15:42:07.999804',20,1,NULL,NULL,'2020-04-04',5499,'bbugoga14',1,'http://localhost:8000'),(22,NULL,'2020-05-06 15:11:47.939263','2020-05-06 15:42:08.002367',21,1,NULL,NULL,'2020-04-04',86836,'bbugoga14',1,'http://localhost:8000'),(23,NULL,'2020-05-06 15:11:47.948457','2020-05-06 15:42:08.011087',22,1,NULL,NULL,'2020-04-05',86837,'autenko',1,'http://localhost:8000'),(24,NULL,'2020-05-06 15:11:47.957045','2020-05-06 15:42:08.013401',23,1,NULL,NULL,'2020-04-05',86904,'autenko',1,'http://localhost:8000'),(25,NULL,'2020-05-06 15:11:47.965762','2020-05-06 15:42:08.015559',24,1,NULL,NULL,'2020-04-05',86907,'autenko',1,'http://localhost:8000'),(26,NULL,'2020-05-06 15:11:47.968714','2020-05-06 15:42:08.018102',25,1,NULL,NULL,'2020-04-05',86925,'autenko',1,'http://localhost:8000'),(27,NULL,'2020-05-06 15:11:47.971031','2020-05-06 15:42:08.020742',26,1,NULL,NULL,'2020-04-05',86926,'autenko',1,'http://localhost:8000'),(28,NULL,'2020-05-06 15:11:47.980921','2020-05-06 15:42:08.028601',27,1,NULL,NULL,'2020-04-09',86836,'pirkami',1,'http://localhost:8000'),(29,NULL,'2020-05-06 15:11:47.989375','2020-05-06 15:42:08.031007',28,1,NULL,NULL,'2020-04-09',86837,'pirkami',1,'http://localhost:8000'),(30,NULL,'2020-05-06 15:11:48.004845','2020-05-06 15:42:08.033399',29,1,NULL,NULL,'2020-04-09',86904,'pirkami',1,'http://localhost:8000'),(31,NULL,'2020-05-06 15:11:48.007605','2020-05-06 15:42:08.035632',30,1,NULL,NULL,'2020-04-09',86907,'pirkami',1,'http://localhost:8000'),(32,NULL,'2020-05-06 15:11:48.009938','2020-05-06 15:42:08.037853',31,1,NULL,NULL,'2020-04-09',86925,'pirkami',1,'http://localhost:8000'),(33,NULL,'2020-05-06 15:11:48.018187','2020-05-06 15:42:08.046711',32,1,NULL,NULL,'2020-04-18',129840,'kimadav',1,'http://localhost:8000'),(34,NULL,'2020-05-06 15:11:48.020599','2020-05-06 15:42:08.049003',33,1,NULL,NULL,'2020-04-18',130007,'kimadav',1,'http://localhost:8000'),(35,NULL,'2020-05-06 15:11:48.023213','2020-05-06 15:42:08.051279',34,1,NULL,NULL,'2020-04-18',130027,'kimadav',1,'http://localhost:8000'),(36,NULL,'2020-05-06 15:11:48.025690','2020-05-06 15:42:08.053761',35,1,NULL,NULL,'2020-04-18',130235,'kimadav',1,'http://localhost:8000'),(37,NULL,'2020-05-06 15:11:48.028452','2020-05-06 15:42:08.055951',36,1,NULL,NULL,'2020-04-18',130620,'kimadav',1,'http://localhost:8000'),(38,NULL,'2020-05-06 15:11:48.038586','2020-05-06 15:42:08.064377',37,1,NULL,NULL,'2020-05-01',131831,'for_skype',1,'http://localhost:8000'),(39,NULL,'2020-05-06 15:11:48.048407','2020-05-06 15:42:08.066644',38,1,NULL,NULL,'2020-05-01',131968,'for_skype',1,'http://localhost:8000'),(40,NULL,'2020-05-06 15:11:48.057121','2020-05-06 15:42:08.069057',39,1,NULL,NULL,'2020-05-01',132041,'for_skype',1,'http://localhost:8000'),(41,NULL,'2020-05-06 15:11:48.059669','2020-05-06 15:42:08.071372',40,1,NULL,NULL,'2020-05-01',132237,'for_skype',1,'http://localhost:8000'),(42,NULL,'2020-05-06 15:11:48.062108','2020-05-06 15:42:08.073559',41,1,NULL,NULL,'2020-05-01',132276,'for_skype',1,'http://localhost:8000'),(43,NULL,'2020-05-06 15:50:55.915749','2020-05-06 15:51:25.097332',42,1,NULL,NULL,'2020-04-04',92126,'bertolia',1,'iMac-Jocker.local'),(44,NULL,'2020-05-06 15:50:55.920887','2020-05-06 15:51:25.102438',43,1,NULL,NULL,'2020-04-04',360,'bertolia',1,'iMac-Jocker.local'),(45,NULL,'2020-05-06 15:50:55.923637','2020-05-06 15:51:25.106534',44,1,NULL,NULL,'2020-04-04',5494,'bertolia',1,'iMac-Jocker.local'),(46,NULL,'2020-05-06 15:50:55.926543','2020-05-06 15:51:25.109988',45,1,NULL,NULL,'2020-04-04',5499,'bertolia',1,'iMac-Jocker.local'),(47,NULL,'2020-05-06 15:50:55.929251','2020-05-06 15:51:25.113173',46,1,NULL,NULL,'2020-04-04',86836,'bertolia',1,'iMac-Jocker.local'),(48,NULL,'2020-05-06 15:50:55.932850','2020-05-06 15:51:25.115997',47,1,NULL,NULL,'2020-04-04',86837,'osyashig',1,'iMac-Jocker.local'),(49,NULL,'2020-05-06 15:50:55.935952','2020-05-06 15:51:25.118765',48,1,NULL,NULL,'2020-04-04',86904,'osyashig',1,'iMac-Jocker.local'),(50,NULL,'2020-05-06 15:50:55.938477','2020-05-06 15:51:25.121229',49,1,NULL,NULL,'2020-04-04',86907,'osyashig',1,'iMac-Jocker.local'),(51,NULL,'2020-05-06 15:50:55.941006','2020-05-06 15:51:25.123646',50,1,NULL,NULL,'2020-04-04',86925,'osyashig',1,'iMac-Jocker.local'),(52,NULL,'2020-05-06 15:50:55.943526','2020-05-06 15:51:25.126451',51,1,NULL,NULL,'2020-04-04',86926,'osyashig',1,'iMac-Jocker.local'),(53,NULL,'2020-05-06 15:50:55.946127','2020-05-06 15:51:25.129215',52,1,NULL,NULL,'2020-04-04',110640,'osyashig',1,'iMac-Jocker.local'),(54,NULL,'2020-05-06 15:50:55.949679','2020-05-06 15:51:25.131612',53,1,NULL,NULL,'2020-04-04',110751,'osyashig',1,'iMac-Jocker.local'),(55,NULL,'2020-05-06 15:50:55.952334','2020-05-06 15:51:25.133901',54,1,NULL,NULL,'2020-04-04',110759,'osyashig',1,'iMac-Jocker.local'),(56,NULL,'2020-05-06 15:50:55.955066','2020-05-06 15:51:25.136380',55,1,NULL,NULL,'2020-04-04',111125,'osyashig',1,'iMac-Jocker.local'),(57,NULL,'2020-05-06 15:50:55.957597','2020-05-06 15:51:25.139205',56,1,NULL,NULL,'2020-04-04',111624,'osyashig',1,'iMac-Jocker.local'),(58,NULL,'2020-05-06 15:50:55.960204','2020-05-06 15:51:25.141849',57,1,NULL,NULL,'2020-04-04',92126,'bbugoga14',1,'iMac-Jocker.local'),(59,NULL,'2020-05-06 15:50:55.963227','2020-05-06 15:51:25.144258',58,1,NULL,NULL,'2020-04-04',360,'bbugoga14',1,'iMac-Jocker.local'),(60,NULL,'2020-05-06 15:50:55.966194','2020-05-06 15:51:25.146837',59,1,NULL,NULL,'2020-04-04',5494,'bbugoga14',1,'iMac-Jocker.local'),(61,NULL,'2020-05-06 15:50:55.968979','2020-05-06 15:51:25.149547',60,1,NULL,NULL,'2020-04-04',5499,'bbugoga14',1,'iMac-Jocker.local'),(62,NULL,'2020-05-06 15:50:55.971933','2020-05-06 15:51:25.152362',61,1,NULL,NULL,'2020-04-04',86836,'bbugoga14',1,'iMac-Jocker.local'),(63,NULL,'2020-05-06 15:50:55.980851','2020-05-06 15:51:25.163684',62,1,NULL,NULL,'2020-04-05',86837,'autenko',1,'iMac-Jocker.local'),(64,NULL,'2020-05-06 15:50:55.983683','2020-05-06 15:51:25.166408',63,1,NULL,NULL,'2020-04-05',86904,'autenko',1,'iMac-Jocker.local'),(65,NULL,'2020-05-06 15:50:55.986566','2020-05-06 15:51:25.169198',64,1,NULL,NULL,'2020-04-05',86907,'autenko',1,'iMac-Jocker.local'),(66,NULL,'2020-05-06 15:50:55.989540','2020-05-06 15:51:25.171843',65,1,NULL,NULL,'2020-04-05',86925,'autenko',1,'iMac-Jocker.local'),(67,NULL,'2020-05-06 15:50:55.992312','2020-05-06 15:51:25.174804',66,1,NULL,NULL,'2020-04-05',86926,'autenko',1,'iMac-Jocker.local'),(68,NULL,'2020-05-06 15:50:56.000599','2020-05-06 15:51:25.183668',67,1,NULL,NULL,'2020-04-09',86836,'pirkami',1,'iMac-Jocker.local'),(69,NULL,'2020-05-06 15:50:56.003564','2020-05-06 15:51:25.186629',68,1,NULL,NULL,'2020-04-09',86837,'pirkami',1,'iMac-Jocker.local'),(70,NULL,'2020-05-06 15:50:56.006357','2020-05-06 15:51:25.189914',69,1,NULL,NULL,'2020-04-09',86904,'pirkami',1,'iMac-Jocker.local'),(71,NULL,'2020-05-06 15:50:56.009782','2020-05-06 15:51:25.192928',70,1,NULL,NULL,'2020-04-09',86907,'pirkami',1,'iMac-Jocker.local'),(72,NULL,'2020-05-06 15:50:56.012763','2020-05-06 15:51:25.195498',71,1,NULL,NULL,'2020-04-09',86925,'pirkami',1,'iMac-Jocker.local'),(73,NULL,'2020-05-06 15:50:56.020981','2020-05-06 15:51:25.205821',72,1,NULL,NULL,'2020-04-18',129840,'kimadav',1,'iMac-Jocker.local'),(74,NULL,'2020-05-06 15:50:56.023563','2020-05-06 15:51:25.208490',73,1,NULL,NULL,'2020-04-18',130007,'kimadav',1,'iMac-Jocker.local'),(75,NULL,'2020-05-06 15:50:56.026117','2020-05-06 15:51:25.210930',74,1,NULL,NULL,'2020-04-18',130027,'kimadav',1,'iMac-Jocker.local'),(76,NULL,'2020-05-06 15:50:56.028632','2020-05-06 15:51:25.213313',75,1,NULL,NULL,'2020-04-18',130235,'kimadav',1,'iMac-Jocker.local'),(77,NULL,'2020-05-06 15:50:56.031231','2020-05-06 15:51:25.215728',76,1,NULL,NULL,'2020-04-18',130620,'kimadav',1,'iMac-Jocker.local'),(78,NULL,'2020-05-06 15:50:56.039868','2020-05-06 15:51:25.226850',77,1,NULL,NULL,'2020-05-01',131831,'for_skype',1,'iMac-Jocker.local'),(79,NULL,'2020-05-06 15:50:56.042331','2020-05-06 15:51:25.229775',78,1,NULL,NULL,'2020-05-01',131968,'for_skype',1,'iMac-Jocker.local'),(80,NULL,'2020-05-06 15:50:56.044841','2020-05-06 15:51:25.233052',79,1,NULL,NULL,'2020-05-01',132041,'for_skype',1,'iMac-Jocker.local'),(81,NULL,'2020-05-06 15:50:56.047399','2020-05-06 15:51:25.235939',80,1,NULL,NULL,'2020-05-01',132237,'for_skype',1,'iMac-Jocker.local'),(82,NULL,'2020-05-06 15:50:56.051580','2020-05-06 15:51:25.238853',81,1,NULL,NULL,'2020-05-01',132276,'for_skype',1,'iMac-Jocker.local');
/*!40000 ALTER TABLE `promotion_svisits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotion_vocabulary`
--

DROP TABLE IF EXISTS `promotion_vocabulary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `promotion_vocabulary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `promotion_vocabulary_img_09f529f6` (`img`),
  KEY `promotion_vocabulary_created_06d9edd9` (`created`),
  KEY `promotion_vocabulary_updated_dbc78e03` (`updated`),
  KEY `promotion_vocabulary_position_212ea086` (`position`),
  KEY `promotion_vocabulary_is_active_b920c9c6` (`is_active`),
  KEY `promotion_vocabulary_state_5ebc7b6f` (`state`),
  KEY `promotion_vocabulary_parents_c77b5c59` (`parents`),
  KEY `promotion_vocabulary_name_04b84c6c` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotion_vocabulary`
--

LOCK TABLES `promotion_vocabulary` WRITE;
/*!40000 ALTER TABLE `promotion_vocabulary` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotion_vocabulary` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-10 16:15:05
