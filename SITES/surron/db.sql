-- MySQL dump 10.13  Distrib 5.7.31, for osx10.12 (x86_64)
--
-- Host: localhost    Database: surron
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
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add user',3,'add_user'),(10,'Can change user',3,'change_user'),(11,'Can delete user',3,'delete_user'),(12,'Can view user',3,'view_user'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Админка - Настрока',6,'add_config'),(22,'Can change Админка - Настрока',6,'change_config'),(23,'Can delete Админка - Настрока',6,'delete_config'),(24,'Can view Админка - Настрока',6,'view_config'),(25,'Can add Админка - Задача',7,'add_tasks'),(26,'Can change Админка - Задача',7,'change_tasks'),(27,'Can delete Админка - Задача',7,'delete_tasks'),(28,'Can view Админка - Задача',7,'view_tasks'),(29,'Can add custom user',11,'add_customuser'),(30,'Can change custom user',11,'change_customuser'),(31,'Can delete custom user',11,'delete_customuser'),(32,'Can view custom user',11,'view_customuser'),(33,'Can add Стат.контет - Файл',12,'add_files'),(34,'Can change Стат.контет - Файл',12,'change_files'),(35,'Can delete Стат.контет - Файл',12,'delete_files'),(36,'Can view Стат.контет - Файл',12,'view_files'),(37,'Can add Стат.контент - Блоки',13,'add_blocks'),(38,'Can change Стат.контент - Блоки',13,'change_blocks'),(39,'Can delete Стат.контент - Блоки',13,'delete_blocks'),(40,'Can view Стат.контент - Блоки',13,'view_blocks'),(41,'Can add Стат.контент - Контейнеры',14,'add_containers'),(42,'Can change Стат.контент - Контейнеры',14,'change_containers'),(43,'Can delete Стат.контент - Контейнеры',14,'delete_containers'),(44,'Can view Стат.контент - Контейнеры',14,'view_containers'),(45,'Can add Стат.контент - Линковка меню к контейнерам',15,'add_linkcontainer'),(46,'Can change Стат.контент - Линковка меню к контейнерам',15,'change_linkcontainer'),(47,'Can delete Стат.контент - Линковка меню к контейнерам',15,'delete_linkcontainer'),(48,'Can view Стат.контент - Линковка меню к контейнерам',15,'view_linkcontainer'),(49,'Can add Товары - товар/услуга',16,'add_products'),(50,'Can change Товары - товар/услуга',16,'change_products'),(51,'Can delete Товары - товар/услуга',16,'delete_products'),(52,'Can view Товары - товар/услуга',16,'view_products'),(53,'Can add products cats',17,'add_productscats'),(54,'Can change products cats',17,'change_productscats'),(55,'Can delete products cats',17,'delete_productscats'),(56,'Can view products cats',17,'view_productscats'),(57,'Can add products photos',18,'add_productsphotos'),(58,'Can change products photos',18,'change_productsphotos'),(59,'Can delete products photos',18,'delete_productsphotos'),(60,'Can view products photos',18,'view_productsphotos'),(61,'Can add property',19,'add_property'),(62,'Can change property',19,'change_property'),(63,'Can delete property',19,'delete_property'),(64,'Can view property',19,'view_property'),(65,'Can add properties values',20,'add_propertiesvalues'),(66,'Can change properties values',20,'change_propertiesvalues'),(67,'Can delete properties values',20,'delete_propertiesvalues'),(68,'Can view properties values',20,'view_propertiesvalues'),(69,'Can add products properties',21,'add_productsproperties'),(70,'Can change products properties',21,'change_productsproperties'),(71,'Can delete products properties',21,'delete_productsproperties'),(72,'Can view products properties',21,'view_productsproperties'),(73,'Can add costs types',22,'add_coststypes'),(74,'Can change costs types',22,'change_coststypes'),(75,'Can delete costs types',22,'delete_coststypes'),(76,'Can view costs types',22,'view_coststypes'),(77,'Can add costs',23,'add_costs'),(78,'Can change costs',23,'change_costs'),(79,'Can delete costs',23,'delete_costs'),(80,'Can view costs',23,'view_costs'),(81,'Can add Пользователи - пользователь',24,'add_shopper'),(82,'Can change Пользователи - пользователь',24,'change_shopper'),(83,'Can delete Пользователи - пользователь',24,'delete_shopper'),(84,'Can view Пользователи - пользователь',24,'view_shopper'),(85,'Can add Магазин - Заказ',25,'add_orders'),(86,'Can change Магазин - Заказ',25,'change_orders'),(87,'Can delete Магазин - Заказ',25,'delete_orders'),(88,'Can view Магазин - Заказ',25,'view_orders'),(89,'Can add Магазин - Покупки',27,'add_purchases'),(90,'Can change Магазин - Покупки',27,'change_purchases'),(91,'Can delete Магазин - Покупки',27,'delete_purchases'),(92,'Can view Магазин - Покупки',27,'view_purchases'),(93,'Can add Магазин - Транзакция',28,'add_transactions'),(94,'Can change Магазин - Транзакция',28,'change_transactions'),(95,'Can delete Магазин - Транзакция',28,'delete_transactions'),(96,'Can view Магазин - Транзакция',28,'view_transactions'),(97,'Can add Магазин - Промокод',29,'add_promocodes'),(98,'Can change Магазин - Промокод',29,'change_promocodes'),(99,'Can delete Магазин - Промокод',29,'delete_promocodes'),(100,'Can view Магазин - Промокод',29,'view_promocodes');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$pKK8oQ6hms3g$3gw8gcsfXQ+b+JfgSgqjLq32O2wXdJb0/WmJPxbP+pI=','2021-02-27 13:26:05.727568',1,'jocker','','','dkramorov@mail.ru',1,1,'2021-02-26 15:26:44.291931'),(2,'pbkdf2_sha256$150000$xZv7tfJ6HL28$mqqO4PN0YZy3wwcDRenqZU3nQqHv/TF3sVe4nO06HJg=','2021-02-27 13:13:05.369478',1,'phil','Рома','Обухов','',1,1,'2021-02-27 13:12:57.858108');
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
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(12,'files','files'),(13,'flatcontent','blocks'),(14,'flatcontent','containers'),(15,'flatcontent','linkcontainer'),(11,'login','customuser'),(8,'login','extrafields'),(10,'login','extrainfo'),(9,'login','extravalues'),(6,'main_functions','config'),(7,'main_functions','tasks'),(24,'personal','shopper'),(23,'products','costs'),(22,'products','coststypes'),(16,'products','products'),(17,'products','productscats'),(18,'products','productsphotos'),(21,'products','productsproperties'),(20,'products','propertiesvalues'),(19,'products','property'),(5,'sessions','session'),(25,'shop','orders'),(29,'shop','promocodes'),(27,'shop','purchases'),(28,'shop','transactions'),(26,'shop','wishlist');
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
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-02-26 15:26:42.876329'),(2,'contenttypes','0002_remove_content_type_name','2021-02-26 15:26:42.923746'),(3,'auth','0001_initial','2021-02-26 15:26:43.071824'),(4,'auth','0002_alter_permission_name_max_length','2021-02-26 15:26:43.324866'),(5,'auth','0003_alter_user_email_max_length','2021-02-26 15:26:43.344431'),(6,'auth','0004_alter_user_username_opts','2021-02-26 15:26:43.352897'),(7,'auth','0005_alter_user_last_login_null','2021-02-26 15:26:43.368864'),(8,'auth','0006_require_contenttypes_0002','2021-02-26 15:26:43.372190'),(9,'auth','0007_alter_validators_add_error_messages','2021-02-26 15:26:43.380021'),(10,'auth','0008_alter_user_username_max_length','2021-02-26 15:26:43.402266'),(11,'auth','0009_alter_user_last_name_max_length','2021-02-26 15:26:43.418217'),(12,'auth','0010_alter_group_name_max_length','2021-02-26 15:26:43.433901'),(13,'auth','0011_update_proxy_permissions','2021-02-26 15:26:43.440794'),(14,'files','0001_initial','2021-02-26 15:26:43.461288'),(15,'files','0002_auto_20191203_2054','2021-02-26 15:26:43.517986'),(16,'files','0003_auto_20200112_1717','2021-02-26 15:26:43.528818'),(17,'files','0004_auto_20200402_2127','2021-02-26 15:26:43.552305'),(18,'files','0005_auto_20200809_1025','2021-02-26 15:26:43.555543'),(19,'flatcontent','0001_initial','2021-02-26 15:26:43.650926'),(20,'flatcontent','0002_auto_20190825_1730','2021-02-26 15:26:43.925390'),(21,'flatcontent','0003_auto_20191203_2054','2021-02-26 15:26:43.958594'),(22,'flatcontent','0004_blocks_html','2021-02-26 15:26:43.983171'),(23,'flatcontent','0005_auto_20200112_1717','2021-02-26 15:26:44.015384'),(24,'flatcontent','0006_auto_20200314_1638','2021-02-26 15:26:44.020727'),(25,'flatcontent','0007_auto_20200402_2127','2021-02-26 15:26:44.103514'),(26,'flatcontent','0008_containers_class_name','2021-02-26 15:26:44.127051'),(27,'flatcontent','0009_blocks_class_name','2021-02-26 15:26:44.155248'),(28,'login','0001_initial','2021-02-26 15:26:44.423403'),(29,'login','0002_auto_20200925_1007','2021-02-26 15:26:44.755281'),(30,'main_functions','0001_initial','2021-02-26 15:26:44.782146'),(31,'main_functions','0002_auto_20191203_2052','2021-02-26 15:26:44.804440'),(32,'main_functions','0003_auto_20200407_1845','2021-02-26 15:26:45.024993'),(33,'main_functions','0004_config_user','2021-02-26 15:26:45.134810'),(34,'personal','0001_initial','2021-02-26 15:26:45.180971'),(35,'personal','0002_auto_20200528_1642','2021-02-26 15:26:45.317302'),(36,'personal','0003_auto_20200616_1707','2021-02-26 15:26:45.327689'),(37,'personal','0004_shopper_ip','2021-02-26 15:26:45.347424'),(38,'products','0001_initial','2021-02-26 15:26:45.396554'),(39,'products','0002_productsphotos','2021-02-26 15:26:45.530470'),(40,'products','0003_auto_20200315_2217','2021-02-26 15:26:45.609125'),(41,'products','0004_auto_20200316_2329','2021-02-26 15:26:45.659039'),(42,'products','0005_auto_20200402_2127','2021-02-26 15:26:45.765429'),(43,'products','0006_auto_20200402_2351','2021-02-26 15:26:45.925017'),(44,'products','0007_property_ptype','2021-02-26 15:26:45.948106'),(45,'products','0008_property_code','2021-02-26 15:26:45.970326'),(46,'products','0009_property_measure','2021-02-26 15:26:45.993206'),(47,'products','0010_auto_20200623_1629','2021-02-26 15:26:46.042071'),(48,'products','0011_auto_20200627_1353','2021-02-26 15:26:46.178426'),(49,'products','0012_auto_20201212_1449','2021-02-26 15:26:46.239507'),(50,'products','0013_property_search_facet','2021-02-26 15:26:46.271285'),(51,'sessions','0001_initial','2021-02-26 15:26:46.293604'),(52,'shop','0001_initial','2021-02-26 15:26:46.392105'),(53,'shop','0002_auto_20200618_0000','2021-02-26 15:26:46.727297'),(54,'shop','0003_auto_20200621_1346','2021-02-26 15:26:46.969276'),(55,'shop','0004_purchases_cost_type','2021-02-26 15:26:47.030039'),(56,'shop','0005_transactions','2021-02-26 15:26:47.093578'),(57,'shop','0006_auto_20200719_0003','2021-02-26 15:26:47.266802'),(58,'shop','0007_auto_20200719_0146','2021-02-26 15:26:47.454130'),(59,'shop','0008_auto_20201026_1359','2021-02-26 15:26:47.502928'),(60,'shop','0009_auto_20201212_1539','2021-02-26 15:26:47.561334'),(61,'shop','0010_auto_20210208_1858','2021-02-26 15:26:47.616624'),(62,'shop','0011_orders_external_number','2021-02-26 15:26:47.650450');
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
INSERT INTO `django_session` VALUES ('bhhw5et1xhkznc1nj56b12jhkhdx2p8q','YTFmY2YzYTc2NTc1YzY0Y2ZjNThmZDNmNGM1Njg2Zjg3MTRlMGRiNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6Ijg1NjhlNDAzN2Y4YjJiZDM3NTExODM1MGVhN2Q2ZGVlZjVhMmJiMmUifQ==','2021-03-13 13:26:05.744162');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files_files`
--

LOCK TABLES `files_files` WRITE;
/*!40000 ALTER TABLE `files_files` DISABLE KEYS */;
INSERT INTO `files_files` VALUES (1,NULL,'2021-02-28 13:20:22.492407','2021-02-28 13:25:29.599623',1,1,NULL,'','Видео-фон','/video-bg.mp4','','video/mp4','path_1.mp4');
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
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
INSERT INTO `flatcontent_blocks` VALUES (1,'header-icon.png','2021-02-26 15:44:11.685949','2021-02-26 15:55:36.110218',1,1,1,'','Логотип','Добро пожаловать, на наш сайт','/','logo',1,0,'','','SurRon','',''),(2,NULL,'2021-02-26 15:44:11.694758','2021-02-26 15:44:11.694802',2,1,3,'','Телефон',NULL,'tel:73952123321','phone',1,0,NULL,NULL,NULL,'+7(3952) 123-321',NULL),(3,NULL,'2021-02-26 15:44:11.702777','2021-02-26 15:44:11.702798',3,1,3,'','Адрес',NULL,NULL,'address',1,0,NULL,NULL,NULL,'г. Иркутск ул. Советская 32а офис 5',NULL),(4,NULL,'2021-02-26 15:44:11.705357','2021-02-26 15:44:11.705377',4,1,3,'','Email',NULL,NULL,'email',1,0,NULL,NULL,NULL,'test@test.ru',NULL),(5,NULL,'2021-02-26 15:44:11.707883','2021-02-26 15:44:11.707900',5,1,3,'','Режим работы',NULL,NULL,'worktime',1,0,NULL,NULL,NULL,'пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 17:00',NULL),(6,NULL,'2021-02-26 15:44:11.710325','2021-02-26 18:03:39.162528',6,1,1,'','Copyright','','','copyright',1,0,'','','','© 2020 Все права защищены',''),(7,NULL,'2021-02-26 15:44:11.712721','2021-02-26 16:17:09.394848',7,1,1,'','Название компании','','','company_name',1,0,'','','SurRon','',''),(8,'favicon-16.jpg','2021-02-26 15:44:11.715254','2021-02-27 13:26:37.701678',8,1,1,'','Favicon','','','favicon',1,0,'','','','',''),(9,NULL,'2021-02-26 15:44:11.717876','2021-02-26 15:44:11.717893',9,1,3,'','Сообщества',NULL,NULL,'social',1,0,NULL,NULL,NULL,NULL,NULL),(10,NULL,'2021-02-26 15:44:11.720474','2021-02-26 15:44:11.720494',10,1,3,'_9','instagram',NULL,NULL,'instagram',1,1,'instagram',NULL,NULL,NULL,NULL),(11,NULL,'2021-02-26 15:44:11.723768','2021-02-26 15:44:11.723793',11,1,3,'_9','vk',NULL,NULL,'vk',1,1,'vk',NULL,NULL,NULL,NULL),(12,NULL,'2021-02-26 15:44:11.726632','2021-02-26 15:44:11.726655',12,1,3,'_9','facebook',NULL,NULL,'facebook',1,1,'facebook',NULL,NULL,NULL,NULL),(13,NULL,'2021-02-26 15:44:11.729605','2021-02-26 15:44:11.729626',13,1,3,'_9','twitter',NULL,NULL,'twitter',1,1,'twitter',NULL,NULL,NULL,NULL),(14,NULL,'2021-02-26 15:44:11.732268','2021-02-26 15:44:11.732289',14,1,3,'','Яндекс.Метрика счетчик',NULL,NULL,'yandex_metrika',1,0,NULL,NULL,NULL,'<script type=\"text/javascript\"></script>',NULL),(15,NULL,'2021-02-26 15:44:11.734935','2021-02-26 15:44:11.734954',15,1,3,'','Google.Analytics счетчик',NULL,NULL,'google_analytics',1,0,NULL,NULL,NULL,'<script type=\"text/javascript\"></script>',NULL),(16,NULL,'2021-02-26 15:44:11.742814','2021-02-26 15:56:01.205342',16,1,4,'','Light Bee','','/light-bee/','',2,0,'','','','',''),(33,NULL,'2021-02-26 15:56:14.625659','2021-02-26 15:56:14.625679',33,1,4,'','Light Bee S',NULL,'/light-bee-s/',NULL,2,0,NULL,NULL,NULL,NULL,NULL),(34,NULL,'2021-02-26 15:56:25.424995','2021-02-26 15:56:25.425014',34,1,4,'','Storm Bee',NULL,'/storm-bee/',NULL,2,0,NULL,NULL,NULL,NULL,NULL),(35,NULL,'2021-02-26 15:56:31.768608','2021-02-27 13:11:01.551425',35,1,4,'','Двигатель','','/power/','',2,0,'','','','',''),(38,NULL,'2021-02-26 16:57:30.268620','2021-02-26 16:59:20.983471',38,1,4,'','Главная','','#home','home',4,0,'home','','','',''),(39,NULL,'2021-02-26 16:57:33.884019','2021-02-26 17:00:09.527948',39,1,4,'','О нас','','#about','about',4,0,'book','','','',''),(40,NULL,'2021-02-26 16:57:34.697404','2021-02-26 17:00:54.336403',40,1,4,'','Проекты','','#gallery','gallery',4,0,'camera','','','',''),(41,NULL,'2021-02-26 16:57:36.159600','2021-02-26 17:01:10.021194',41,1,4,'','Подписаться','','#subscribe','subscribe',4,0,'envelope-o','','','',''),(42,NULL,'2021-02-26 16:57:48.613668','2021-02-26 17:01:44.653121',42,1,4,'','Контакты','','#contact','contact',4,0,'phone','','','',''),(44,NULL,'2021-02-26 17:24:12.700597','2021-02-26 17:24:12.700616',43,1,4,'','Light Bee',NULL,'/light-bee/',NULL,3,0,NULL,NULL,NULL,NULL,NULL),(45,NULL,'2021-02-26 17:24:19.963714','2021-02-26 17:24:19.963738',44,1,4,'','Light Bee S',NULL,'/light-bee-s/',NULL,3,0,NULL,NULL,NULL,NULL,NULL),(46,NULL,'2021-02-26 17:24:27.610461','2021-02-26 17:24:27.610481',45,1,4,'','Light Bee L1e',NULL,'/light-bee-l1e/',NULL,3,0,NULL,NULL,NULL,NULL,NULL),(47,NULL,'2021-02-26 17:24:35.428053','2021-02-26 17:24:35.428073',46,1,4,'','Storm Bee',NULL,'/storm-bee/',NULL,3,0,NULL,NULL,NULL,NULL,NULL),(48,NULL,'2021-02-26 17:24:43.168258','2021-02-27 13:11:49.196725',47,1,4,'','Двигатель','','/power/','',3,0,'','','','',''),(51,NULL,'2021-02-26 17:25:09.379567','2021-02-27 13:11:55.617583',50,1,4,'','Магазин','','/shop/','',3,0,'','','','',''),(52,NULL,'2021-02-26 17:26:00.921122','2021-02-27 13:11:37.503126',51,1,4,'','Магазин','','/shop/','',2,0,'','','','',''),(53,NULL,'2021-02-26 17:57:54.483008','2021-02-26 17:59:51.706080',52,1,1,'','Спец предложение','Подробнее','#about','',5,0,'','','','Мы предлагаем вам познакомиться поближе с Light Bee, который точно не оставит вас равнодушным и подарит массу положительных впечатлений<br>',''),(54,NULL,'2021-02-26 18:05:09.792685','2021-02-26 18:05:09.792709',52,1,1,'','Спец предложение','Подробнее','#about','',6,0,'','','','Мы предлагаем вам познакомиться поближе с Light Bee, который точно не оставит вас равнодушным и подарит массу положительных впечатлений<br>',''),(55,NULL,'2021-02-26 18:06:02.087282','2021-02-28 14:04:19.767361',53,1,4,'','Главная','','/','',7,0,'','','','',''),(56,NULL,'2021-02-26 18:27:09.929893','2021-02-26 18:29:45.963627',54,1,1,'','Мы - официальный представитель','Подробнее','#services','',8,0,'','','','Мы представляем компанию поставщика, предлагаем лучшие цены, большие скидки и полный уровень сервиса и технического обслуживания. Вы не сможете найти предложение лучше чем наше, мы полностью берем на себя все подготовительные операции по проверке функционирования и правильной работы техники<br>',''),(57,NULL,'2021-02-26 18:30:12.764421','2021-02-26 18:30:12.764439',54,1,1,'','Мы - официальный представитель','Подробнее','#services','',9,0,'','','','Мы представляем компанию поставщика, предлагаем лучшие цены, большие скидки и полный уровень сервиса и технического обслуживания. Вы не сможете найти предложение лучше чем наше, мы полностью берем на себя все подготовительные операции по проверке функционирования и правильной работы техники<br>',''),(58,'58.jpg','2021-02-26 18:45:34.432716','2021-02-26 19:03:31.498813',55,1,1,'','Light Bee','Подробнее','/','',10,0,'','','','SUR-RON Light Bee предназначен для дорог общего пользования',''),(59,'59.jpg','2021-02-26 18:47:21.572456','2021-02-26 19:05:57.969386',56,1,1,'','Light Bee S','Подробнее','/','',10,0,'','','','SUR-RON Light Bee S предназначен для дорог общего пользования',''),(60,'60.jpg','2021-02-26 18:48:55.033588','2021-02-26 19:05:31.621127',57,1,1,'','Storm Bee','Подробнее','/','',10,0,'','','','Sur-ron Storm bee мощный, надежный и эффективный',''),(62,'62.jpg','2021-02-26 19:06:51.969013','2021-02-26 19:06:51.969044',55,1,1,'','Light Bee','Подробнее','/','',11,0,'','','','SUR-RON Light Bee предназначен для дорог общего пользования',''),(63,'63.jpg','2021-02-26 19:06:51.971622','2021-02-26 19:06:51.971639',56,1,1,'','Light Bee S','Подробнее','/','',11,0,'','','','SUR-RON Light Bee S предназначен для дорог общего пользования',''),(64,'64.jpg','2021-02-26 19:06:51.979823','2021-02-26 19:06:51.979848',57,1,1,'','Storm Bee','Подробнее','/','',11,0,'','','','Sur-ron Storm bee мощный, надежный и эффективный',''),(66,'big1.jpg','2021-02-27 10:23:51.256904','2021-02-27 10:41:59.576813',59,1,1,'','Light Bee S','Подробнее','/','',12,0,'','','','SUR-RON Light Bee S предназначен для дорог общего пользования',''),(67,'light-bee-one-bg.jpg','2021-02-27 10:24:02.253305','2021-02-27 10:42:40.223807',60,1,1,'','Storm Bee','Подробнее','/','',12,0,'','','','Sur-ron Storm bee мощный, надежный и эффективный',''),(68,'big1.jpg','2021-02-27 10:44:26.722783','2021-02-27 10:44:26.722804',59,1,1,'','Light Bee S','Подробнее','/','',13,0,'','','','SUR-RON Light Bee S предназначен для дорог общего пользования',''),(69,'light-bee-one-bg.jpg','2021-02-27 10:44:26.730121','2021-02-27 10:44:26.730142',60,1,1,'','Storm Bee','Подробнее','/','',13,0,'','','','Sur-ron Storm bee мощный, надежный и эффективный',''),(70,NULL,'2021-02-27 10:58:02.039459','2021-02-27 10:59:13.292436',61,1,1,'','Тех обслуживание','Продукция','/','link',14,0,'','','','Мы производим реализацию, обслуживание и тестирование всей нашей продукции<br>',''),(71,'image-21-08-20-10-42-2.jpeg','2021-02-27 10:59:26.202483','2021-02-27 11:04:29.639084',62,1,1,'','Light Bee S','Подробнее','/','',14,0,'','','Для города','Удобное решение для движения по городу, экономичный, стильный и компактный<br>',''),(72,'undefined.jpg','2021-02-27 10:59:45.012233','2021-02-27 11:04:46.497905',63,1,1,'','Storm Bee','Подробнее','/','',14,0,'','','Для любой местности','Мощный, проходимый и неприхотливый, позволит вам пересечь даже сложную местность<br>',''),(73,NULL,'2021-02-27 11:07:39.943550','2021-02-27 11:07:39.943568',61,1,1,'','Тех обслуживание','Продукция','/','link',15,0,'','','','Мы производим реализацию, обслуживание и тестирование всей нашей продукции<br>',''),(74,'image-21-08-20-10-42-2.jpeg','2021-02-27 11:07:39.944423','2021-02-27 11:07:39.944438',62,1,1,'','Light Bee S','Подробнее','/','',15,0,'','','Для города','Удобное решение для движения по городу, экономичный, стильный и компактный<br>',''),(75,'undefined.jpg','2021-02-27 11:07:39.945921','2021-02-27 11:07:39.945937',63,1,1,'','Storm Bee','Подробнее','/','',15,0,'','','Для любой местности','Мощный, проходимый и неприхотливый, позволит вам пересечь даже сложную местность<br>',''),(76,NULL,'2021-02-27 11:10:17.359743','2021-02-27 11:10:17.359766',61,1,1,'','Тех обслуживание','Продукция','/','link',16,0,'','','','Мы производим реализацию, обслуживание и тестирование всей нашей продукции<br>',''),(77,'image-21-08-20-10-42-2.jpeg','2021-02-27 11:10:17.360675','2021-02-27 11:39:27.654238',62,1,1,'','Light Bee S','Подробнее','/','',16,0,'road','','Для города','Удобное решение для движения по городу, экономичный, стильный и компактный<br>',''),(78,'undefined.jpg','2021-02-27 11:10:17.362303','2021-02-27 11:39:42.320891',63,1,1,'','Storm Bee','Подробнее','/','',16,0,'road','','Для любой местности','Мощный, проходимый и неприхотливый, позволит вам пересечь даже сложную местность<br>',''),(79,NULL,'2021-02-27 11:41:57.048055','2021-02-27 11:41:57.048077',61,1,1,'','Тех обслуживание','Продукция','/','link',17,0,'','','','Мы производим реализацию, обслуживание и тестирование всей нашей продукции<br>',''),(80,'image-21-08-20-10-42-2.jpeg','2021-02-27 11:41:57.053523','2021-02-27 11:41:57.053545',62,1,1,'','Light Bee S','Подробнее','/','',17,0,'road','','Для города','Удобное решение для движения по городу, экономичный, стильный и компактный<br>',''),(81,'undefined.jpg','2021-02-27 11:41:57.057218','2021-02-27 11:41:57.057240',63,1,1,'','Storm Bee','Подробнее','/','',17,0,'road','','Для любой местности','Мощный, проходимый и неприхотливый, позволит вам пересечь даже сложную местность<br>',''),(82,NULL,'2021-02-27 11:46:28.918295','2021-02-27 11:46:28.918321',61,1,1,'','Тех обслуживание','Продукция','/','link',18,0,'','','','Мы производим реализацию, обслуживание и тестирование всей нашей продукции<br>',''),(83,'83.jpg','2021-02-27 11:46:28.919334','2021-02-27 12:12:56.809852',62,1,1,'','Light Bee S','Подробнее','/','',18,0,'','','350 000 ₽','Удобное решение для движения по городу<br>',''),(84,'84.jpg','2021-02-27 11:46:28.922278','2021-02-27 12:08:18.046057',63,1,1,'','Storm Bee','Подробнее','/','',18,0,'','','400 000 ₽','Мощный, проходимый и неприхотливый<br>',''),(85,'85.jpg','2021-02-27 11:58:45.990301','2021-02-27 12:04:48.930270',64,1,1,'','Light Bee','Подробнее','/','',18,0,'','','300 000 ₽','Удобное решение для движения по городу',''),(86,NULL,'2021-02-27 12:13:38.920292','2021-02-27 12:13:38.920310',61,1,1,'','Тех обслуживание','Продукция','/','link',19,0,'','','','Мы производим реализацию, обслуживание и тестирование всей нашей продукции<br>',''),(87,'87.jpg','2021-02-27 12:13:38.921235','2021-02-27 12:13:38.921251',62,1,1,'','Light Bee S','Подробнее','/','',19,0,'','','350 000 ₽','Удобное решение для движения по городу<br>',''),(88,'88.jpg','2021-02-27 12:13:38.922541','2021-02-27 12:13:38.922556',63,1,1,'','Storm Bee','Подробнее','/','',19,0,'','','400 000 ₽','Мощный, проходимый и неприхотливый<br>',''),(89,'89.jpg','2021-02-27 12:13:38.929705','2021-02-27 12:13:38.929723',64,1,1,'','Light Bee','Подробнее','/','',19,0,'','','300 000 ₽','Удобное решение для движения по городу',''),(90,NULL,'2021-02-27 12:35:59.340234','2021-02-27 12:36:23.930679',65,1,1,'','Без названия','','','',20,0,'','','','Будьте в курсе наших акций и последних новостей<br>',''),(91,NULL,'2021-02-27 12:37:21.439176','2021-02-27 12:37:21.439197',65,1,1,'','Без названия','','','',21,0,'','','','Будьте в курсе наших акций и последних новостей<br>',''),(92,NULL,'2021-02-27 12:47:15.618793','2021-02-27 12:54:12.030265',2,1,1,'','Бесплатный','Выбрать','/','',22,0,'','','0 ₽','в мес<br>',''),(93,NULL,'2021-02-27 12:47:16.562756','2021-02-27 12:55:22.531915',3,1,1,'','Стандартный','Выбрать','/','featured',22,0,'','','3 000 ₽','в мес<br>',''),(94,NULL,'2021-02-27 12:47:18.102289','2021-02-27 12:54:20.095929',4,1,1,'','Корпоративный','Выбрать','/','',22,0,'','','8 000 ₽','в мес<br>',''),(95,NULL,'2021-02-27 12:50:10.242202','2021-02-27 12:51:00.884367',1,1,1,'','Описание','','','',22,0,'','','','Мы предлагаем вам различные варианты обслуживания, выберите для себя подходящее решение<br>',''),(96,NULL,'2021-02-27 12:51:05.201868','2021-02-27 12:58:14.291234',70,1,1,'_92','Консультация','','','',22,0,'check-circle','','','',''),(97,NULL,'2021-02-27 12:51:06.675292','2021-02-27 12:58:06.070159',71,1,1,'_93','Консультация','','','',22,0,'check-circle','','','',''),(98,NULL,'2021-02-27 12:51:08.591811','2021-02-27 12:57:57.487583',72,1,1,'_94','Консультация','','','',22,0,'check-circle','','','',''),(99,NULL,'2021-02-27 12:58:38.432425','2021-02-27 13:01:07.629441',73,1,1,'_92','Обслуживание','','','',22,0,'times-circle','','','','disabled'),(100,NULL,'2021-02-27 12:58:44.182998','2021-02-27 13:01:24.988893',74,1,1,'_93','Обслуживание','','','',22,0,'check-circle','','','',''),(101,NULL,'2021-02-27 12:58:46.444267','2021-02-27 13:01:43.023439',75,1,1,'_94','Обслуживание','','','',22,0,'check-circle','','','',''),(102,NULL,'2021-02-27 13:00:07.643419','2021-02-27 13:01:13.336255',76,1,1,'_92','Тех помощь','','','',22,0,'times-circle','','','','disabled'),(103,NULL,'2021-02-27 13:00:12.920378','2021-02-27 13:01:33.619744',77,1,1,'_93','Тех помощь','','','',22,0,'times-circle','','','','disabled'),(104,NULL,'2021-02-27 13:00:14.843617','2021-02-27 13:01:52.240928',78,1,1,'_94','Тех помощь','','','',22,0,'check-circle','','','',''),(105,NULL,'2021-02-27 13:02:17.241086','2021-02-27 13:02:17.241106',2,1,1,'','Бесплатный','Выбрать','/','',23,0,'','','0 ₽','в мес<br>',''),(106,NULL,'2021-02-27 13:02:17.241987','2021-02-27 13:02:17.242009',70,1,1,'_105','Консультация','','','',23,0,'check-circle','','','',''),(107,NULL,'2021-02-27 13:02:17.246415','2021-02-27 13:02:17.246438',73,1,1,'_105','Обслуживание','','','',23,0,'times-circle','','','','disabled'),(108,NULL,'2021-02-27 13:02:17.247480','2021-02-27 13:02:17.247518',76,1,1,'_105','Тех помощь','','','',23,0,'times-circle','','','','disabled'),(109,NULL,'2021-02-27 13:02:17.248469','2021-02-27 13:02:17.248488',3,1,1,'','Стандартный','Выбрать','/','featured',23,0,'','','3 000 ₽','в мес<br>',''),(110,NULL,'2021-02-27 13:02:17.249495','2021-02-27 13:02:17.249514',71,1,1,'_109','Консультация','','','',23,0,'check-circle','','','',''),(111,NULL,'2021-02-27 13:02:17.250364','2021-02-27 13:02:17.250382',74,1,1,'_109','Обслуживание','','','',23,0,'check-circle','','','',''),(112,NULL,'2021-02-27 13:02:17.251276','2021-02-27 13:02:17.251305',77,1,1,'_109','Тех помощь','','','',23,0,'times-circle','','','','disabled'),(113,NULL,'2021-02-27 13:02:17.252351','2021-02-27 13:02:17.252388',4,1,1,'','Корпоративный','Выбрать','/','',23,0,'','','8 000 ₽','в мес<br>',''),(114,NULL,'2021-02-27 13:02:17.254726','2021-02-27 13:02:17.254746',72,1,1,'_113','Консультация','','','',23,0,'check-circle','','','',''),(115,NULL,'2021-02-27 13:02:17.255513','2021-02-27 13:02:17.255531',75,1,1,'_113','Обслуживание','','','',23,0,'check-circle','','','',''),(116,NULL,'2021-02-27 13:02:17.256288','2021-02-27 13:02:17.256305',78,1,1,'_113','Тех помощь','','','',23,0,'check-circle','','','',''),(117,NULL,'2021-02-27 13:02:17.257083','2021-02-27 13:02:17.257102',1,1,1,'','Описание','','','',23,0,'','','','Мы предлагаем вам различные варианты обслуживания, выберите для себя подходящее решение<br>',''),(118,NULL,'2021-02-27 13:08:14.088836','2021-02-27 13:08:50.715266',79,1,1,'','Контакты','','','',24,0,'','','','Напишите нам и мы обязательно вам ответим<br>тел + 7 (3952) 123-321<br>адрес: Ржанова 164, офис 204<br>',''),(119,NULL,'2021-02-27 13:09:37.867927','2021-02-27 13:09:37.867945',79,1,1,'','Контакты','','','',25,0,'','','','Напишите нам и мы обязательно вам ответим<br>тел + 7 (3952) 123-321<br>адрес: Ржанова 164, офис 204<br>',''),(120,NULL,'2021-02-28 13:17:04.412383','2021-02-28 13:28:35.498051',80,1,1,'','Ссылка на видео mp4 из файлов','','/media/misc/loop-bg.mp4','',26,0,'','','','',''),(121,NULL,'2021-02-28 13:17:45.021916','2021-02-28 13:27:48.022724',80,1,1,'','Ссылка на видео mp4 из файлов','','/video-bg.mp4','',27,0,'','','','',''),(126,NULL,'2021-02-28 14:01:27.821191','2021-02-28 14:01:59.896638',81,1,1,'','Главная','','#home','home',28,0,'home','','','',''),(127,NULL,'2021-02-28 14:02:07.908317','2021-02-28 14:02:38.817245',82,1,1,'','О нас','','#about','about',28,0,'book','','','',''),(128,NULL,'2021-02-28 14:02:11.031651','2021-02-28 14:02:51.864372',83,1,1,'','Проекты','','#gallery','gallery',28,0,'camera','','','',''),(129,NULL,'2021-02-28 14:02:16.497285','2021-02-28 14:03:04.862502',84,1,1,'','Подписаться','','#subscribe','subscribe',28,0,'envelope-o','','','',''),(130,NULL,'2021-02-28 14:02:19.932196','2021-02-28 14:03:17.368578',85,1,1,'','Контакты','','#contact','contact',28,0,'phone','','','',''),(131,NULL,'2021-02-28 14:03:58.889287','2021-02-28 14:03:58.889313',81,1,1,'','Главная','','#home','home',29,0,'home','','','',''),(132,NULL,'2021-02-28 14:03:58.890239','2021-02-28 14:03:58.890257',82,1,1,'','О нас','','#about','about',29,0,'book','','','',''),(133,NULL,'2021-02-28 14:03:58.891014','2021-02-28 14:03:58.891030',83,1,1,'','Проекты','','#gallery','gallery',29,0,'camera','','','',''),(134,NULL,'2021-02-28 14:03:58.891779','2021-02-28 14:03:58.891795',84,1,1,'','Подписаться','','#subscribe','subscribe',29,0,'envelope-o','','','',''),(135,NULL,'2021-02-28 14:03:58.903709','2021-02-28 14:03:58.903732',85,1,1,'','Контакты','','#contact','contact',29,0,'phone','','','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
INSERT INTO `flatcontent_containers` VALUES (1,NULL,'2021-02-26 15:44:11.676667','2021-02-26 15:44:11.676704',1,1,2,NULL,'Контент для всех страничек','Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики','main',NULL,NULL),(2,NULL,'2021-02-26 15:44:11.737535','2021-02-26 15:44:11.737561',2,1,1,NULL,'Главное меню','Создано автоматически, выводит главное меню','mainmenu',NULL,NULL),(3,NULL,'2021-02-26 15:44:11.740051','2021-02-26 17:23:22.528148',3,1,1,'','Мобильное меню','','mobilemenu','',''),(4,NULL,'2021-02-26 16:57:11.045760','2021-02-28 13:56:14.488095',4,0,1,'','Слайдер меню','','slidermenu','',''),(5,NULL,'2021-02-26 17:49:38.093154','2021-02-26 17:52:22.183578',5,1,99,'','Контейнер homepage','Light Bee<br>','homepage','',''),(6,NULL,'2021-02-26 18:05:09.778302','2021-02-26 18:05:09.789028',6,1,3,'','Главный экран','Light Bee<br>','homepage','',''),(7,NULL,'2021-02-26 18:05:54.333699','2021-02-27 11:08:08.034700',7,1,1,'','Главная страничка','','','',''),(8,NULL,'2021-02-26 18:13:47.769575','2021-02-26 18:13:58.588017',8,1,99,'','Контейнер aboutpage','О нас<br>','aboutpage','',''),(9,NULL,'2021-02-26 18:30:12.754771','2021-02-26 18:30:12.760885',9,1,3,'','О нас','О нас<br>','aboutpage','',''),(10,NULL,'2021-02-26 18:37:35.171155','2021-02-27 12:14:52.353020',10,1,99,'','Контейнер carouselpage','Наши предложения<br>','carouselpage','',''),(11,NULL,'2021-02-26 19:06:51.953027','2021-02-26 19:08:59.396658',11,1,3,'','Слайдер','Наши предложения<br>','carouselpage','',''),(12,NULL,'2021-02-26 19:09:21.624339','2021-02-26 19:09:25.486065',12,1,99,'','Контейнер sliderpage','','sliderpage','',''),(13,NULL,'2021-02-27 10:44:26.671535','2021-02-27 10:44:26.671553',13,1,3,'','Слайдер байков','','sliderpage','',''),(14,NULL,'2021-02-27 10:49:32.453725','2021-02-27 10:49:50.304720',14,1,99,'','Контейнер twoblockspage','Предложения<br>','twoblockspage','',''),(15,NULL,'2021-02-27 11:07:39.933605','2021-02-27 11:07:39.939843',15,1,3,'','Два блока с мопедами','Предложения<br>','twoblockspage','',''),(16,NULL,'2021-02-27 11:10:17.349748','2021-02-27 11:10:30.857417',14,1,99,'','Контейнер twonewspage','Предложения<br>','twonewspage','',''),(17,NULL,'2021-02-27 11:41:52.325657','2021-02-27 11:41:57.044213',16,1,3,'','Два блока с мопедами (альт)','Предложения<br>','twonewspage','',''),(18,NULL,'2021-02-27 11:46:28.862859','2021-02-27 11:46:38.915483',14,1,99,'','Контейнер threeblockspage','Предложения<br>','threeblockspage','',''),(19,NULL,'2021-02-27 12:13:38.912026','2021-02-27 12:13:38.916382',17,1,3,'','Наши товары','Предложения<br>','threeblockspage','',''),(20,NULL,'2021-02-27 12:35:52.340531','2021-02-27 12:36:39.311753',18,1,99,'','Подписаться на новости','Подпишись на новости<br>','subscribepage','',''),(21,NULL,'2021-02-27 12:37:21.425674','2021-02-27 12:37:21.435323',19,1,3,'','Подписаться на новости','Подпишись на новости<br>','subscribepage','',''),(22,NULL,'2021-02-27 12:46:53.349079','2021-02-27 12:54:39.743922',20,1,99,'','Тарифный план','Тарифный план<br>','priceplanpage','',''),(23,NULL,'2021-02-27 13:02:17.183570','2021-02-27 13:02:17.231021',21,1,3,'','Тарифный план','Тарифный план<br>','priceplanpage','',''),(24,NULL,'2021-02-27 13:07:51.883380','2021-02-27 13:07:58.614493',22,1,99,'','Контакты','Написать нам<br>','contactspage','',''),(25,NULL,'2021-02-27 13:09:37.855025','2021-02-27 13:09:37.862961',23,1,3,'','Контакты','Написать нам<br>','contactspage','',''),(26,NULL,'2021-02-28 13:13:35.284889','2021-02-28 13:28:06.670508',24,1,99,'','Видео фон странички','','video_bg','',''),(27,NULL,'2021-02-28 13:17:44.961524','2021-02-28 13:17:44.961543',25,1,3,'','Демонстрационный фон с видео','','video_bg','',''),(28,NULL,'2021-02-28 13:57:49.008992','2021-02-28 13:57:49.009011',26,1,99,'','Слайдер-меню для странички','','slider_menu','',''),(29,NULL,'2021-02-28 14:03:52.961709','2021-02-28 14:03:58.842375',27,1,3,'','Слайдер-меню для главной странички','','slider_menu','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_linkcontainer`
--

LOCK TABLES `flatcontent_linkcontainer` WRITE;
/*!40000 ALTER TABLE `flatcontent_linkcontainer` DISABLE KEYS */;
INSERT INTO `flatcontent_linkcontainer` VALUES (67,NULL,'2021-02-28 14:04:19.774998','2021-02-28 14:04:19.775020',1,1,NULL,NULL,55,6),(68,NULL,'2021-02-28 14:04:19.776658','2021-02-28 14:04:19.776679',2,1,NULL,NULL,55,9),(69,NULL,'2021-02-28 14:04:19.777987','2021-02-28 14:04:19.778007',3,1,NULL,NULL,55,11),(70,NULL,'2021-02-28 14:04:19.779247','2021-02-28 14:04:19.779266',4,1,NULL,NULL,55,13),(71,NULL,'2021-02-28 14:04:19.781572','2021-02-28 14:04:19.781594',5,1,NULL,NULL,55,15),(72,NULL,'2021-02-28 14:04:19.783638','2021-02-28 14:04:19.783658',6,1,NULL,NULL,55,17),(73,NULL,'2021-02-28 14:04:19.784957','2021-02-28 14:04:19.784975',7,1,NULL,NULL,55,19),(74,NULL,'2021-02-28 14:04:19.786257','2021-02-28 14:04:19.786278',8,1,NULL,NULL,55,21),(75,NULL,'2021-02-28 14:04:19.787577','2021-02-28 14:04:19.787598',9,1,NULL,NULL,55,23),(76,NULL,'2021-02-28 14:04:19.790029','2021-02-28 14:04:19.790049',10,1,NULL,NULL,55,25),(77,NULL,'2021-02-28 14:04:19.791338','2021-02-28 14:04:19.791358',11,1,NULL,NULL,55,27),(78,NULL,'2021-02-28 14:04:19.792691','2021-02-28 14:04:19.792712',12,1,NULL,NULL,55,29);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_customuser`
--

LOCK TABLES `login_customuser` WRITE;
/*!40000 ALTER TABLE `login_customuser` DISABLE KEYS */;
INSERT INTO `login_customuser` VALUES (1,NULL,'2021-02-26 15:26:44.385523','2021-02-27 13:26:05.732350',1,1,NULL,NULL,NULL,NULL,1),(2,NULL,'2021-02-27 13:12:47.424656','2021-02-27 13:13:05.379194',2,1,NULL,NULL,'','',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_functions_config`
--

LOCK TABLES `main_functions_config` WRITE;
/*!40000 ALTER TABLE `main_functions_config` DISABLE KEYS */;
INSERT INTO `main_functions_config` VALUES (1,'Почта обратной связи','flatcontent_feedback','dkramorov@mail.ru','2021-02-26 15:44:11.795063',NULL,1,NULL,1,NULL,'2021-02-26 15:44:11.795083',NULL);
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
-- Table structure for table `personal_shopper`
--

DROP TABLE IF EXISTS `personal_shopper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `personal_shopper` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `passwd` varchar(255) DEFAULT NULL,
  `oauth` int(11) DEFAULT NULL,
  `discount` int(11) DEFAULT NULL,
  `balance` decimal(13,2) DEFAULT NULL,
  `login` varchar(255) DEFAULT NULL,
  `ip` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `personal_shopper_img_27adcfca` (`img`),
  KEY `personal_shopper_created_8714f2f0` (`created`),
  KEY `personal_shopper_updated_5bb722b7` (`updated`),
  KEY `personal_shopper_position_b36dded1` (`position`),
  KEY `personal_shopper_is_active_3c7f8d97` (`is_active`),
  KEY `personal_shopper_state_6cf650eb` (`state`),
  KEY `personal_shopper_parents_f8aa5f1d` (`parents`),
  KEY `personal_shopper_name_dcee2987` (`name`),
  KEY `personal_shopper_first_name_17b48468` (`first_name`),
  KEY `personal_shopper_last_name_9839cd34` (`last_name`),
  KEY `personal_shopper_middle_name_4c97334b` (`middle_name`),
  KEY `personal_shopper_email_ec60fc6e` (`email`),
  KEY `personal_shopper_phone_8fc7729b` (`phone`),
  KEY `personal_shopper_address_7a53bfcf` (`address`),
  KEY `personal_shopper_passwd_a3de9219` (`passwd`),
  KEY `personal_shopper_oauth_8c254e92` (`oauth`),
  KEY `personal_shopper_discont_c1ad0dbd` (`discount`),
  KEY `personal_shopper_balance_73b360f3` (`balance`),
  KEY `personal_shopper_login_f66d2194` (`login`),
  KEY `personal_shopper_ip_86d54b2b` (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personal_shopper`
--

LOCK TABLES `personal_shopper` WRITE;
/*!40000 ALTER TABLE `personal_shopper` DISABLE KEYS */;
/*!40000 ALTER TABLE `personal_shopper` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_costs`
--

DROP TABLE IF EXISTS `products_costs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_costs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `measure` int(11) DEFAULT NULL,
  `cost` decimal(13,2) DEFAULT NULL,
  `cost_type_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_costs_cost_type_id_107dbde9_fk_products_coststypes_id` (`cost_type_id`),
  KEY `products_costs_product_id_17019dcf_fk_products_products_id` (`product_id`),
  KEY `products_costs_measure_d41f1f9c` (`measure`),
  KEY `products_costs_cost_f67c70f7` (`cost`),
  CONSTRAINT `products_costs_cost_type_id_107dbde9_fk_products_coststypes_id` FOREIGN KEY (`cost_type_id`) REFERENCES `products_coststypes` (`id`),
  CONSTRAINT `products_costs_product_id_17019dcf_fk_products_products_id` FOREIGN KEY (`product_id`) REFERENCES `products_products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_costs`
--

LOCK TABLES `products_costs` WRITE;
/*!40000 ALTER TABLE `products_costs` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_costs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_coststypes`
--

DROP TABLE IF EXISTS `products_coststypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_coststypes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `tag` varchar(255) DEFAULT NULL,
  `currency` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_coststypes_img_e68688b6` (`img`),
  KEY `products_coststypes_created_aeb582a6` (`created`),
  KEY `products_coststypes_updated_377149fe` (`updated`),
  KEY `products_coststypes_position_97c095f4` (`position`),
  KEY `products_coststypes_is_active_2d96b101` (`is_active`),
  KEY `products_coststypes_state_c139eeac` (`state`),
  KEY `products_coststypes_parents_08bcdf0f` (`parents`),
  KEY `products_coststypes_name_5911ece6` (`name`),
  KEY `products_coststypes_tag_87ab0d61` (`tag`),
  KEY `products_coststypes_currency_46d344cf` (`currency`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_coststypes`
--

LOCK TABLES `products_coststypes` WRITE;
/*!40000 ALTER TABLE `products_coststypes` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_coststypes` ENABLE KEYS */;
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
  `max_price` decimal(13,2) DEFAULT NULL,
  `min_price` decimal(13,2) DEFAULT NULL,
  `min_count` int(11) DEFAULT NULL,
  `multiplicity` int(11) DEFAULT NULL,
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
  KEY `products_products_count_8ac0f722` (`count`),
  KEY `products_products_max_price_d7fdf069` (`max_price`),
  KEY `products_products_min_price_7cb1c282` (`min_price`),
  KEY `products_products_min_count_327e2504` (`min_count`),
  KEY `products_products_multiplicity_d783aa0f` (`multiplicity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_products`
--

LOCK TABLES `products_products` WRITE;
/*!40000 ALTER TABLE `products_products` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productscats`
--

LOCK TABLES `products_productscats` WRITE;
/*!40000 ALTER TABLE `products_productscats` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productsproperties`
--

LOCK TABLES `products_productsproperties` WRITE;
/*!40000 ALTER TABLE `products_productsproperties` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_propertiesvalues`
--

LOCK TABLES `products_propertiesvalues` WRITE;
/*!40000 ALTER TABLE `products_propertiesvalues` DISABLE KEYS */;
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
  `search_facet` tinyint(1) NOT NULL,
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
  KEY `products_property_measure_5824486e` (`measure`),
  KEY `products_property_search_facet_a9b2f085` (`search_facet`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_property`
--

LOCK TABLES `products_property` WRITE;
/*!40000 ALTER TABLE `products_property` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_orders`
--

DROP TABLE IF EXISTS `shop_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `number` varchar(255) DEFAULT NULL,
  `total` decimal(13,2) DEFAULT NULL,
  `comments` varchar(255) DEFAULT NULL,
  `shopper_id` int(11) DEFAULT NULL,
  `shopper_address` varchar(255) DEFAULT NULL,
  `shopper_email` varchar(255) DEFAULT NULL,
  `shopper_ip` varchar(255) DEFAULT NULL,
  `shopper_name` varchar(255) DEFAULT NULL,
  `shopper_phone` varchar(255) DEFAULT NULL,
  `discount` decimal(13,2) DEFAULT NULL,
  `promocode_id` int(11) DEFAULT NULL,
  `payed` decimal(13,2) DEFAULT NULL,
  `external_number` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `shop_orders_img_89a0f42d` (`img`),
  KEY `shop_orders_created_f4f7ad2a` (`created`),
  KEY `shop_orders_updated_c63e3f75` (`updated`),
  KEY `shop_orders_position_93545035` (`position`),
  KEY `shop_orders_is_active_2cacc96e` (`is_active`),
  KEY `shop_orders_state_c02d2396` (`state`),
  KEY `shop_orders_parents_907e9242` (`parents`),
  KEY `shop_orders_number_6fd689bc` (`number`),
  KEY `shop_orders_comments_4a9b55e1` (`comments`),
  KEY `shop_orders_shopper_id_65a5fb7c_fk_personal_shopper_id` (`shopper_id`),
  KEY `shop_orders_shopper_address_599eb5eb` (`shopper_address`),
  KEY `shop_orders_shopper_email_6cdbdb3d` (`shopper_email`),
  KEY `shop_orders_shopper_ip_558ccd11` (`shopper_ip`),
  KEY `shop_orders_shopper_name_f94f3317` (`shopper_name`),
  KEY `shop_orders_shopper_phone_dfa9ca32` (`shopper_phone`),
  KEY `shop_orders_total_99508ca3` (`total`),
  KEY `shop_orders_discount_fa591db5` (`discount`),
  KEY `shop_orders_promocode_id_b424c7c1_fk_shop_promocodes_id` (`promocode_id`),
  KEY `shop_orders_payed_467c77b9` (`payed`),
  KEY `shop_orders_external_number_74c28d3d` (`external_number`),
  CONSTRAINT `shop_orders_promocode_id_b424c7c1_fk_shop_promocodes_id` FOREIGN KEY (`promocode_id`) REFERENCES `shop_promocodes` (`id`),
  CONSTRAINT `shop_orders_shopper_id_65a5fb7c_fk_personal_shopper_id` FOREIGN KEY (`shopper_id`) REFERENCES `personal_shopper` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_orders`
--

LOCK TABLES `shop_orders` WRITE;
/*!40000 ALTER TABLE `shop_orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `shop_orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_promocodes`
--

DROP TABLE IF EXISTS `shop_promocodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_promocodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `percent` int(11) DEFAULT NULL,
  `value` int(11) DEFAULT NULL,
  `code` varchar(255) DEFAULT NULL,
  `start_date` datetime(6) DEFAULT NULL,
  `end_date` datetime(6) DEFAULT NULL,
  `use_count` int(11) DEFAULT NULL,
  `personal_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `shop_promocodes_personal_id_745753e5_fk_personal_shopper_id` (`personal_id`),
  KEY `shop_promocodes_img_c334f5e0` (`img`),
  KEY `shop_promocodes_created_54fdc250` (`created`),
  KEY `shop_promocodes_updated_a2a13db9` (`updated`),
  KEY `shop_promocodes_position_57ab65f5` (`position`),
  KEY `shop_promocodes_is_active_bd112f26` (`is_active`),
  KEY `shop_promocodes_state_76fe5eb7` (`state`),
  KEY `shop_promocodes_parents_afa16efa` (`parents`),
  KEY `shop_promocodes_name_433a2b48` (`name`),
  KEY `shop_promocodes_percent_c0249e3e` (`percent`),
  KEY `shop_promocodes_value_b465b96d` (`value`),
  KEY `shop_promocodes_code_531acef2` (`code`),
  KEY `shop_promocodes_start_date_57049461` (`start_date`),
  KEY `shop_promocodes_end_date_3e7c4e18` (`end_date`),
  KEY `shop_promocodes_use_count_a001cb4d` (`use_count`),
  CONSTRAINT `shop_promocodes_personal_id_745753e5_fk_personal_shopper_id` FOREIGN KEY (`personal_id`) REFERENCES `personal_shopper` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_promocodes`
--

LOCK TABLES `shop_promocodes` WRITE;
/*!40000 ALTER TABLE `shop_promocodes` DISABLE KEYS */;
/*!40000 ALTER TABLE `shop_promocodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_purchases`
--

DROP TABLE IF EXISTS `shop_purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_purchases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_code` varchar(255) DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `cost` decimal(13,2) DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  `shopper_id` int(11) DEFAULT NULL,
  `discount_info` varchar(255) DEFAULT NULL,
  `product_manufacturer` varchar(255) DEFAULT NULL,
  `product_measure` varchar(255) DEFAULT NULL,
  `product_price` decimal(13,2) DEFAULT NULL,
  `cost_type_id` int(11) DEFAULT NULL,
  `product_min_count` int(11) DEFAULT NULL,
  `product_multiplicity` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `shop_purchases_order_id_7309c2ce_fk_shop_orders_id` (`order_id`),
  KEY `shop_purchases_img_6aa377d3` (`img`),
  KEY `shop_purchases_created_c423b588` (`created`),
  KEY `shop_purchases_updated_0dc8a0f9` (`updated`),
  KEY `shop_purchases_position_0d22dcd7` (`position`),
  KEY `shop_purchases_is_active_e6830a3e` (`is_active`),
  KEY `shop_purchases_state_33431c06` (`state`),
  KEY `shop_purchases_parents_45c9e6c4` (`parents`),
  KEY `shop_purchases_product_id_909aeb58` (`product_id`),
  KEY `shop_purchases_product_code_636790fb` (`product_code`),
  KEY `shop_purchases_product_name_4c4abf61` (`product_name`),
  KEY `shop_purchases_count_98f46158` (`count`),
  KEY `shop_purchases_discount_info_200ee1dd` (`discount_info`),
  KEY `shop_purchases_product_manufacturer_2685f7c9` (`product_manufacturer`),
  KEY `shop_purchases_product_measure_44500ae1` (`product_measure`),
  KEY `shop_purchases_shopper_id_49fcf0ae_fk_personal_shopper_id` (`shopper_id`),
  KEY `shop_purchases_cost_type_id_29172c16_fk_products_coststypes_id` (`cost_type_id`),
  KEY `shop_purchases_cost_0153dfed` (`cost`),
  KEY `shop_purchases_product_price_ea7e7453` (`product_price`),
  KEY `shop_purchases_product_min_count_0d9acb57` (`product_min_count`),
  KEY `shop_purchases_product_multiplicity_be5331ab` (`product_multiplicity`),
  CONSTRAINT `shop_purchases_cost_type_id_29172c16_fk_products_coststypes_id` FOREIGN KEY (`cost_type_id`) REFERENCES `products_coststypes` (`id`),
  CONSTRAINT `shop_purchases_order_id_7309c2ce_fk_shop_orders_id` FOREIGN KEY (`order_id`) REFERENCES `shop_orders` (`id`),
  CONSTRAINT `shop_purchases_shopper_id_49fcf0ae_fk_personal_shopper_id` FOREIGN KEY (`shopper_id`) REFERENCES `personal_shopper` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_purchases`
--

LOCK TABLES `shop_purchases` WRITE;
/*!40000 ALTER TABLE `shop_purchases` DISABLE KEYS */;
/*!40000 ALTER TABLE `shop_purchases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_transactions`
--

DROP TABLE IF EXISTS `shop_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_transactions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  `ptype` int(11) DEFAULT NULL,
  `success` tinyint(1) NOT NULL,
  `body` longtext,
  `order_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `shop_transactions_order_id_df0f9f4d_fk_shop_orders_id` (`order_id`),
  KEY `shop_transactions_img_0a2fc12d` (`img`),
  KEY `shop_transactions_created_8339e1a8` (`created`),
  KEY `shop_transactions_updated_d7db47b3` (`updated`),
  KEY `shop_transactions_position_38d2ba3d` (`position`),
  KEY `shop_transactions_is_active_62c8d736` (`is_active`),
  KEY `shop_transactions_state_3c7ae23d` (`state`),
  KEY `shop_transactions_parents_6298bcfa` (`parents`),
  KEY `shop_transactions_uuid_5084fd1d` (`uuid`),
  KEY `shop_transactions_ptype_e34ea4f8` (`ptype`),
  KEY `shop_transactions_success_aeef13cc` (`success`),
  CONSTRAINT `shop_transactions_order_id_df0f9f4d_fk_shop_orders_id` FOREIGN KEY (`order_id`) REFERENCES `shop_orders` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_transactions`
--

LOCK TABLES `shop_transactions` WRITE;
/*!40000 ALTER TABLE `shop_transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `shop_transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shop_wishlist`
--

DROP TABLE IF EXISTS `shop_wishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_wishlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `shopper_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `shop_wishlist_product_id_0fc70568_fk_products_products_id` (`product_id`),
  KEY `shop_wishlist_img_9cc8d6b2` (`img`),
  KEY `shop_wishlist_created_5afac261` (`created`),
  KEY `shop_wishlist_updated_562383b8` (`updated`),
  KEY `shop_wishlist_position_d20beef8` (`position`),
  KEY `shop_wishlist_is_active_32b112fb` (`is_active`),
  KEY `shop_wishlist_state_d78b0872` (`state`),
  KEY `shop_wishlist_parents_e51e38bc` (`parents`),
  KEY `shop_wishlist_shopper_id_b3ccbbb2_fk_personal_shopper_id` (`shopper_id`),
  CONSTRAINT `shop_wishlist_product_id_0fc70568_fk_products_products_id` FOREIGN KEY (`product_id`) REFERENCES `products_products` (`id`),
  CONSTRAINT `shop_wishlist_shopper_id_b3ccbbb2_fk_personal_shopper_id` FOREIGN KEY (`shopper_id`) REFERENCES `personal_shopper` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_wishlist`
--

LOCK TABLES `shop_wishlist` WRITE;
/*!40000 ALTER TABLE `shop_wishlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `shop_wishlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-03 12:05:52
