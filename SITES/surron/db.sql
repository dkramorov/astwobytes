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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$pKK8oQ6hms3g$3gw8gcsfXQ+b+JfgSgqjLq32O2wXdJb0/WmJPxbP+pI=','2021-03-12 23:01:56.243680',1,'jocker','','','dkramorov@mail.ru',1,1,'2021-02-26 15:26:44.291931'),(2,'pbkdf2_sha256$150000$xZv7tfJ6HL28$mqqO4PN0YZy3wwcDRenqZU3nQqHv/TF3sVe4nO06HJg=','2021-02-27 13:13:05.369478',1,'phil','Рома','Обухов','',1,1,'2021-02-27 13:12:57.858108');
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
INSERT INTO `django_session` VALUES ('35jfccm65nudb4g6rh91qi5xgnqlr9wp','YTFmY2YzYTc2NTc1YzY0Y2ZjNThmZDNmNGM1Njg2Zjg3MTRlMGRiNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6Ijg1NjhlNDAzN2Y4YjJiZDM3NTExODM1MGVhN2Q2ZGVlZjVhMmJiMmUifQ==','2021-03-24 10:44:37.572496'),('bfahmv2bnz12fsfontaj8486095x1f6f','YTFmY2YzYTc2NTc1YzY0Y2ZjNThmZDNmNGM1Njg2Zjg3MTRlMGRiNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6Ijg1NjhlNDAzN2Y4YjJiZDM3NTExODM1MGVhN2Q2ZGVlZjVhMmJiMmUifQ==','2021-03-26 23:01:56.253489'),('bhhw5et1xhkznc1nj56b12jhkhdx2p8q','YTFmY2YzYTc2NTc1YzY0Y2ZjNThmZDNmNGM1Njg2Zjg3MTRlMGRiNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6Ijg1NjhlNDAzN2Y4YjJiZDM3NTExODM1MGVhN2Q2ZGVlZjVhMmJiMmUifQ==','2021-03-13 13:26:05.744162'),('tmo1vrd08dkimra4x76kmbx3xrnqgcpf','YTFmY2YzYTc2NTc1YzY0Y2ZjNThmZDNmNGM1Njg2Zjg3MTRlMGRiNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6Ijg1NjhlNDAzN2Y4YjJiZDM3NTExODM1MGVhN2Q2ZGVlZjVhMmJiMmUifQ==','2021-03-19 11:48:21.439969'),('v987ykqdvmnkeb6guh4njvjbas6hko03','MGEzNDZlMWI2NjJmNjdmNmRmY2VkNjdiODVlYmY3ZDYyMzM4ZGJiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6Ijg1NjhlNDAzN2Y4YjJiZDM3NTExODM1MGVhN2Q2ZGVlZjVhMmJiMmUiLCJzaG9wcGVyIjp7ImlkIjoxLCJuYW1lIjoiS3JhbW9yb3YgRGVuIiwiZmlyc3RfbmFtZSI6IkRlbiIsImxhc3RfbmFtZSI6IktyYW1vcm92IiwibWlkZGxlX25hbWUiOm51bGwsImVtYWlsIjoiZGtAMjIzLTIyMy5ydSIsInBob25lIjoiOCg5MTQpOCA5NTktMjIzIiwiYWRkcmVzcyI6bnVsbCwibG9naW4iOm51bGwsImRpc2NvdW50IjpudWxsLCJiYWxhbmNlIjpudWxsLCJpcCI6IjEyNy4wLjAuMSJ9fQ==','2021-03-23 13:52:15.302571'),('xjm02wvq0ss1y56wnn1s4qkx2krilte8','YTFmY2YzYTc2NTc1YzY0Y2ZjNThmZDNmNGM1Njg2Zjg3MTRlMGRiNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6Ijg1NjhlNDAzN2Y4YjJiZDM3NTExODM1MGVhN2Q2ZGVlZjVhMmJiMmUifQ==','2021-03-19 11:48:49.661989');
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files_files`
--

LOCK TABLES `files_files` WRITE;
/*!40000 ALTER TABLE `files_files` DISABLE KEYS */;
INSERT INTO `files_files` VALUES (1,NULL,'2021-02-28 13:20:22.492407','2021-02-28 13:25:29.599623',1,1,NULL,'','Видео-фон','/video-bg.mp4','','video/mp4','path_1.mp4'),(2,NULL,'2021-03-10 23:16:10.486751','2021-03-10 23:17:00.138791',2,1,NULL,'','Видео для Light Bee (2 видео)','/light_bee_two_videos.mp4','','video/mp4','path_2.mp4'),(4,NULL,'2021-03-11 00:31:34.857872','2021-03-11 00:31:52.155581',3,1,NULL,'','Light Bee Мотор','/light_bee_motor.mp4','','video/mp4','path_4.mp4'),(5,NULL,'2021-03-15 11:17:25.307894','2021-03-15 11:17:49.548107',4,1,NULL,'','Light Bee S video 1','/light_bee_s_1.mp4','','video/mp4','path_5.mp4'),(6,NULL,'2021-03-15 11:30:52.140107','2021-03-15 11:31:03.246494',5,1,NULL,'','Light Bee S  video 2','/light_bee_s_2.mp4','','video/mp4','path_6.mp4');
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
) ENGINE=InnoDB AUTO_INCREMENT=356 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
INSERT INTO `flatcontent_blocks` VALUES (1,'header-icon.png','2021-02-26 15:44:11.685949','2021-02-26 15:55:36.110218',1,1,1,'','Логотип','Добро пожаловать, на наш сайт','/','logo',1,0,'','','SurRon','',''),(2,NULL,'2021-02-26 15:44:11.694758','2021-02-26 15:44:11.694802',2,1,3,'','Телефон',NULL,'tel:73952123321','phone',1,0,NULL,NULL,NULL,'+7(3952) 123-321',NULL),(3,NULL,'2021-02-26 15:44:11.702777','2021-02-26 15:44:11.702798',3,1,3,'','Адрес',NULL,NULL,'address',1,0,NULL,NULL,NULL,'г. Иркутск ул. Советская 32а офис 5',NULL),(4,NULL,'2021-02-26 15:44:11.705357','2021-02-26 15:44:11.705377',4,1,3,'','Email',NULL,NULL,'email',1,0,NULL,NULL,NULL,'test@test.ru',NULL),(5,NULL,'2021-02-26 15:44:11.707883','2021-02-26 15:44:11.707900',5,1,3,'','Режим работы',NULL,NULL,'worktime',1,0,NULL,NULL,NULL,'пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 17:00',NULL),(6,NULL,'2021-02-26 15:44:11.710325','2021-02-26 18:03:39.162528',6,1,1,'','Copyright','','','copyright',1,0,'','','','© 2020 Все права защищены',''),(7,NULL,'2021-02-26 15:44:11.712721','2021-02-26 16:17:09.394848',7,1,1,'','Название компании','','','company_name',1,0,'','','SurRon','',''),(8,'favicon-16.jpg','2021-02-26 15:44:11.715254','2021-02-27 13:26:37.701678',8,1,1,'','Favicon','','','favicon',1,0,'','','','',''),(9,NULL,'2021-02-26 15:44:11.717876','2021-02-26 15:44:11.717893',9,1,3,'','Сообщества',NULL,NULL,'social',1,0,NULL,NULL,NULL,NULL,NULL),(10,NULL,'2021-02-26 15:44:11.720474','2021-02-26 15:44:11.720494',10,1,3,'_9','instagram',NULL,NULL,'instagram',1,1,'instagram',NULL,NULL,NULL,NULL),(11,NULL,'2021-02-26 15:44:11.723768','2021-02-26 15:44:11.723793',11,1,3,'_9','vk',NULL,NULL,'vk',1,1,'vk',NULL,NULL,NULL,NULL),(12,NULL,'2021-02-26 15:44:11.726632','2021-02-26 15:44:11.726655',12,1,3,'_9','facebook',NULL,NULL,'facebook',1,1,'facebook',NULL,NULL,NULL,NULL),(13,NULL,'2021-02-26 15:44:11.729605','2021-02-26 15:44:11.729626',13,1,3,'_9','twitter',NULL,NULL,'twitter',1,1,'twitter',NULL,NULL,NULL,NULL),(14,NULL,'2021-02-26 15:44:11.732268','2021-02-26 15:44:11.732289',14,1,3,'','Яндекс.Метрика счетчик',NULL,NULL,'yandex_metrika',1,0,NULL,NULL,NULL,'<script type=\"text/javascript\"></script>',NULL),(15,NULL,'2021-02-26 15:44:11.734935','2021-02-26 15:44:11.734954',15,1,3,'','Google.Analytics счетчик',NULL,NULL,'google_analytics',1,0,NULL,NULL,NULL,'<script type=\"text/javascript\"></script>',NULL),(16,NULL,'2021-02-26 15:44:11.742814','2021-03-13 11:41:58.517547',16,1,4,'','Light Bee','','/light-bee/','',2,0,'','','','',''),(33,NULL,'2021-02-26 15:56:14.625659','2021-03-15 11:40:20.284535',33,1,4,'','Light Bee S','','/light-bee-s/','',2,0,'','','','',''),(34,NULL,'2021-02-26 15:56:25.424995','2021-02-26 15:56:25.425014',34,1,4,'','Storm Bee',NULL,'/storm-bee/',NULL,2,0,NULL,NULL,NULL,NULL,NULL),(35,NULL,'2021-02-26 15:56:31.768608','2021-02-27 13:11:01.551425',35,1,4,'','Двигатель','','/power/','',2,0,'','','','',''),(38,NULL,'2021-02-26 16:57:30.268620','2021-02-26 16:59:20.983471',38,1,4,'','Главная','','#home','home',4,0,'home','','','',''),(39,NULL,'2021-02-26 16:57:33.884019','2021-02-26 17:00:09.527948',39,1,4,'','О нас','','#about','about',4,0,'book','','','',''),(40,NULL,'2021-02-26 16:57:34.697404','2021-02-26 17:00:54.336403',40,1,4,'','Проекты','','#gallery','gallery',4,0,'camera','','','',''),(41,NULL,'2021-02-26 16:57:36.159600','2021-02-26 17:01:10.021194',41,1,4,'','Подписаться','','#subscribe','subscribe',4,0,'envelope-o','','','',''),(42,NULL,'2021-02-26 16:57:48.613668','2021-02-26 17:01:44.653121',42,1,4,'','Контакты','','#contact','contact',4,0,'phone','','','',''),(44,NULL,'2021-02-26 17:24:12.700597','2021-03-11 00:20:43.657689',2,1,4,'','Light Bee','','/light-bee/','',3,0,'','','','',''),(45,NULL,'2021-02-26 17:24:19.963714','2021-02-26 17:24:19.963738',3,1,4,'','Light Bee S',NULL,'/light-bee-s/',NULL,3,0,NULL,NULL,NULL,NULL,NULL),(46,NULL,'2021-02-26 17:24:27.610461','2021-02-26 17:24:27.610481',4,1,4,'','Light Bee L1e',NULL,'/light-bee-l1e/',NULL,3,0,NULL,NULL,NULL,NULL,NULL),(47,NULL,'2021-02-26 17:24:35.428053','2021-02-26 17:24:35.428073',5,1,4,'','Storm Bee',NULL,'/storm-bee/',NULL,3,0,NULL,NULL,NULL,NULL,NULL),(48,NULL,'2021-02-26 17:24:43.168258','2021-02-27 13:11:49.196725',6,1,4,'','Двигатель','','/power/','',3,0,'','','','',''),(51,NULL,'2021-02-26 17:25:09.379567','2021-03-06 12:10:50.310111',7,1,4,'','Магазин','','/cat/','',3,0,'','','','',''),(52,NULL,'2021-02-26 17:26:00.921122','2021-03-03 23:36:06.893483',51,1,4,'','Магазин','','/cat/','',2,0,'','','','',''),(53,NULL,'2021-02-26 17:57:54.483008','2021-03-10 23:13:50.541888',52,1,1,'','Спец предложение','Подробнее','#about','',5,0,'','','','Мы предлагаем вам познакомиться поближе с Light Bee, который точно не оставит вас равнодушным и подарит массу положительных впечатлений<br>',''),(55,NULL,'2021-02-26 18:06:02.087282','2021-03-10 14:51:57.677134',53,1,4,'','Главная','','/','',7,0,'','','','',''),(56,NULL,'2021-02-26 18:27:09.929893','2021-02-26 18:29:45.963627',54,1,1,'','Мы - официальный представитель','Подробнее','#services','',8,0,'','','','Мы представляем компанию поставщика, предлагаем лучшие цены, большие скидки и полный уровень сервиса и технического обслуживания. Вы не сможете найти предложение лучше чем наше, мы полностью берем на себя все подготовительные операции по проверке функционирования и правильной работы техники<br>',''),(57,NULL,'2021-02-26 18:30:12.764421','2021-02-26 18:30:12.764439',54,1,1,'','Мы - официальный представитель','Подробнее','#services','',9,0,'','','','Мы представляем компанию поставщика, предлагаем лучшие цены, большие скидки и полный уровень сервиса и технического обслуживания. Вы не сможете найти предложение лучше чем наше, мы полностью берем на себя все подготовительные операции по проверке функционирования и правильной работы техники<br>',''),(58,'58.jpg','2021-02-26 18:45:34.432716','2021-02-26 19:03:31.498813',55,1,1,'','Light Bee','Подробнее','/','',10,0,'','','','SUR-RON Light Bee предназначен для дорог общего пользования',''),(59,'59.jpg','2021-02-26 18:47:21.572456','2021-02-26 19:05:57.969386',56,1,1,'','Light Bee S','Подробнее','/','',10,0,'','','','SUR-RON Light Bee S предназначен для дорог общего пользования',''),(60,'60.jpg','2021-02-26 18:48:55.033588','2021-02-26 19:05:31.621127',57,1,1,'','Storm Bee','Подробнее','/','',10,0,'','','','Sur-ron Storm bee мощный, надежный и эффективный',''),(62,'62.jpg','2021-02-26 19:06:51.969013','2021-02-26 19:06:51.969044',55,1,1,'','Light Bee','Подробнее','/','',11,0,'','','','SUR-RON Light Bee предназначен для дорог общего пользования',''),(63,'63.jpg','2021-02-26 19:06:51.971622','2021-02-26 19:06:51.971639',56,1,1,'','Light Bee S','Подробнее','/','',11,0,'','','','SUR-RON Light Bee S предназначен для дорог общего пользования',''),(64,'64.jpg','2021-02-26 19:06:51.979823','2021-02-26 19:06:51.979848',57,1,1,'','Storm Bee','Подробнее','/','',11,0,'','','','Sur-ron Storm bee мощный, надежный и эффективный',''),(66,'big1.jpg','2021-02-27 10:23:51.256904','2021-02-27 10:41:59.576813',59,1,1,'','Light Bee S','Подробнее','/','',12,0,'','','','SUR-RON Light Bee S предназначен для дорог общего пользования',''),(67,'light-bee-one-bg.jpg','2021-02-27 10:24:02.253305','2021-02-27 10:42:40.223807',60,1,1,'','Storm Bee','Подробнее','/','',12,0,'','','','Sur-ron Storm bee мощный, надежный и эффективный',''),(68,'big1.jpg','2021-02-27 10:44:26.722783','2021-02-27 10:44:26.722804',59,1,1,'','Light Bee S','Подробнее','/','',13,0,'','','','SUR-RON Light Bee S предназначен для дорог общего пользования',''),(69,'light-bee-one-bg.jpg','2021-02-27 10:44:26.730121','2021-02-27 10:44:26.730142',60,1,1,'','Storm Bee','Подробнее','/','',13,0,'','','','Sur-ron Storm bee мощный, надежный и эффективный',''),(70,NULL,'2021-02-27 10:58:02.039459','2021-02-27 10:59:13.292436',61,1,1,'','Тех обслуживание','Продукция','/','link',14,0,'','','','Мы производим реализацию, обслуживание и тестирование всей нашей продукции<br>',''),(71,'image-21-08-20-10-42-2.jpeg','2021-02-27 10:59:26.202483','2021-02-27 11:04:29.639084',62,1,1,'','Light Bee S','Подробнее','/','',14,0,'','','Для города','Удобное решение для движения по городу, экономичный, стильный и компактный<br>',''),(72,'undefined.jpg','2021-02-27 10:59:45.012233','2021-02-27 11:04:46.497905',63,1,1,'','Storm Bee','Подробнее','/','',14,0,'','','Для любой местности','Мощный, проходимый и неприхотливый, позволит вам пересечь даже сложную местность<br>',''),(73,NULL,'2021-02-27 11:07:39.943550','2021-02-27 11:07:39.943568',61,1,1,'','Тех обслуживание','Продукция','/','link',15,0,'','','','Мы производим реализацию, обслуживание и тестирование всей нашей продукции<br>',''),(74,'image-21-08-20-10-42-2.jpeg','2021-02-27 11:07:39.944423','2021-02-27 11:07:39.944438',62,1,1,'','Light Bee S','Подробнее','/','',15,0,'','','Для города','Удобное решение для движения по городу, экономичный, стильный и компактный<br>',''),(75,'undefined.jpg','2021-02-27 11:07:39.945921','2021-02-27 11:07:39.945937',63,1,1,'','Storm Bee','Подробнее','/','',15,0,'','','Для любой местности','Мощный, проходимый и неприхотливый, позволит вам пересечь даже сложную местность<br>',''),(76,NULL,'2021-02-27 11:10:17.359743','2021-02-27 11:10:17.359766',61,1,1,'','Тех обслуживание','Продукция','/','link',16,0,'','','','Мы производим реализацию, обслуживание и тестирование всей нашей продукции<br>',''),(77,'image-21-08-20-10-42-2.jpeg','2021-02-27 11:10:17.360675','2021-02-27 11:39:27.654238',62,1,1,'','Light Bee S','Подробнее','/','',16,0,'road','','Для города','Удобное решение для движения по городу, экономичный, стильный и компактный<br>',''),(78,'undefined.jpg','2021-02-27 11:10:17.362303','2021-02-27 11:39:42.320891',63,1,1,'','Storm Bee','Подробнее','/','',16,0,'road','','Для любой местности','Мощный, проходимый и неприхотливый, позволит вам пересечь даже сложную местность<br>',''),(79,NULL,'2021-02-27 11:41:57.048055','2021-02-27 11:41:57.048077',61,1,1,'','Тех обслуживание','Продукция','/','link',17,0,'','','','Мы производим реализацию, обслуживание и тестирование всей нашей продукции<br>',''),(80,'image-21-08-20-10-42-2.jpeg','2021-02-27 11:41:57.053523','2021-02-27 11:41:57.053545',62,1,1,'','Light Bee S','Подробнее','/','',17,0,'road','','Для города','Удобное решение для движения по городу, экономичный, стильный и компактный<br>',''),(81,'undefined.jpg','2021-02-27 11:41:57.057218','2021-02-27 11:41:57.057240',63,1,1,'','Storm Bee','Подробнее','/','',17,0,'road','','Для любой местности','Мощный, проходимый и неприхотливый, позволит вам пересечь даже сложную местность<br>',''),(82,NULL,'2021-02-27 11:46:28.918295','2021-02-27 11:46:28.918321',61,1,1,'','Тех обслуживание','Продукция','/','link',18,0,'','','','Мы производим реализацию, обслуживание и тестирование всей нашей продукции<br>',''),(83,'83.jpg','2021-02-27 11:46:28.919334','2021-02-27 12:12:56.809852',62,1,1,'','Light Bee S','Подробнее','/','',18,0,'','','350 000 ₽','Удобное решение для движения по городу<br>',''),(84,'84.jpg','2021-02-27 11:46:28.922278','2021-02-27 12:08:18.046057',63,1,1,'','Storm Bee','Подробнее','/','',18,0,'','','400 000 ₽','Мощный, проходимый и неприхотливый<br>',''),(85,'85.jpg','2021-02-27 11:58:45.990301','2021-02-27 12:04:48.930270',64,1,1,'','Light Bee','Подробнее','/','',18,0,'','','300 000 ₽','Удобное решение для движения по городу',''),(86,NULL,'2021-02-27 12:13:38.920292','2021-02-27 12:13:38.920310',61,1,1,'','Тех обслуживание','Продукция','/','link',19,0,'','','','Мы производим реализацию, обслуживание и тестирование всей нашей продукции<br>',''),(87,'87.jpg','2021-02-27 12:13:38.921235','2021-02-27 12:13:38.921251',62,1,1,'','Light Bee S','Подробнее','/','',19,0,'','','350 000 ₽','Удобное решение для движения по городу<br>',''),(88,'88.jpg','2021-02-27 12:13:38.922541','2021-02-27 12:13:38.922556',63,1,1,'','Storm Bee','Подробнее','/','',19,0,'','','400 000 ₽','Мощный, проходимый и неприхотливый<br>',''),(89,'89.jpg','2021-02-27 12:13:38.929705','2021-02-27 12:13:38.929723',64,1,1,'','Light Bee','Подробнее','/','',19,0,'','','300 000 ₽','Удобное решение для движения по городу',''),(90,NULL,'2021-02-27 12:35:59.340234','2021-02-27 12:36:23.930679',65,1,1,'','Без названия','','','',20,0,'','','','Будьте в курсе наших акций и последних новостей<br>',''),(91,NULL,'2021-02-27 12:37:21.439176','2021-02-27 12:37:21.439197',65,1,1,'','Без названия','','','',21,0,'','','','Будьте в курсе наших акций и последних новостей<br>',''),(92,NULL,'2021-02-27 12:47:15.618793','2021-02-27 12:54:12.030265',2,1,1,'','Бесплатный','Выбрать','/','',22,0,'','','0 ₽','в мес<br>',''),(93,NULL,'2021-02-27 12:47:16.562756','2021-02-27 12:55:22.531915',3,1,1,'','Стандартный','Выбрать','/','featured',22,0,'','','3 000 ₽','в мес<br>',''),(94,NULL,'2021-02-27 12:47:18.102289','2021-02-27 12:54:20.095929',4,1,1,'','Корпоративный','Выбрать','/','',22,0,'','','8 000 ₽','в мес<br>',''),(95,NULL,'2021-02-27 12:50:10.242202','2021-02-27 12:51:00.884367',1,1,1,'','Описание','','','',22,0,'','','','Мы предлагаем вам различные варианты обслуживания, выберите для себя подходящее решение<br>',''),(96,NULL,'2021-02-27 12:51:05.201868','2021-02-27 12:58:14.291234',70,1,1,'_92','Консультация','','','',22,0,'check-circle','','','',''),(97,NULL,'2021-02-27 12:51:06.675292','2021-02-27 12:58:06.070159',71,1,1,'_93','Консультация','','','',22,0,'check-circle','','','',''),(98,NULL,'2021-02-27 12:51:08.591811','2021-02-27 12:57:57.487583',72,1,1,'_94','Консультация','','','',22,0,'check-circle','','','',''),(99,NULL,'2021-02-27 12:58:38.432425','2021-02-27 13:01:07.629441',73,1,1,'_92','Обслуживание','','','',22,0,'times-circle','','','','disabled'),(100,NULL,'2021-02-27 12:58:44.182998','2021-02-27 13:01:24.988893',74,1,1,'_93','Обслуживание','','','',22,0,'check-circle','','','',''),(101,NULL,'2021-02-27 12:58:46.444267','2021-02-27 13:01:43.023439',75,1,1,'_94','Обслуживание','','','',22,0,'check-circle','','','',''),(102,NULL,'2021-02-27 13:00:07.643419','2021-02-27 13:01:13.336255',76,1,1,'_92','Тех помощь','','','',22,0,'times-circle','','','','disabled'),(103,NULL,'2021-02-27 13:00:12.920378','2021-02-27 13:01:33.619744',77,1,1,'_93','Тех помощь','','','',22,0,'times-circle','','','','disabled'),(104,NULL,'2021-02-27 13:00:14.843617','2021-02-27 13:01:52.240928',78,1,1,'_94','Тех помощь','','','',22,0,'check-circle','','','',''),(105,NULL,'2021-02-27 13:02:17.241086','2021-02-27 13:02:17.241106',2,1,1,'','Бесплатный','Выбрать','/','',23,0,'','','0 ₽','в мес<br>',''),(106,NULL,'2021-02-27 13:02:17.241987','2021-02-27 13:02:17.242009',70,1,1,'_105','Консультация','','','',23,0,'check-circle','','','',''),(107,NULL,'2021-02-27 13:02:17.246415','2021-02-27 13:02:17.246438',73,1,1,'_105','Обслуживание','','','',23,0,'times-circle','','','','disabled'),(108,NULL,'2021-02-27 13:02:17.247480','2021-02-27 13:02:17.247518',76,1,1,'_105','Тех помощь','','','',23,0,'times-circle','','','','disabled'),(109,NULL,'2021-02-27 13:02:17.248469','2021-02-27 13:02:17.248488',3,1,1,'','Стандартный','Выбрать','/','featured',23,0,'','','3 000 ₽','в мес<br>',''),(110,NULL,'2021-02-27 13:02:17.249495','2021-02-27 13:02:17.249514',71,1,1,'_109','Консультация','','','',23,0,'check-circle','','','',''),(111,NULL,'2021-02-27 13:02:17.250364','2021-02-27 13:02:17.250382',74,1,1,'_109','Обслуживание','','','',23,0,'check-circle','','','',''),(112,NULL,'2021-02-27 13:02:17.251276','2021-02-27 13:02:17.251305',77,1,1,'_109','Тех помощь','','','',23,0,'times-circle','','','','disabled'),(113,NULL,'2021-02-27 13:02:17.252351','2021-02-27 13:02:17.252388',4,1,1,'','Корпоративный','Выбрать','/','',23,0,'','','8 000 ₽','в мес<br>',''),(114,NULL,'2021-02-27 13:02:17.254726','2021-02-27 13:02:17.254746',72,1,1,'_113','Консультация','','','',23,0,'check-circle','','','',''),(115,NULL,'2021-02-27 13:02:17.255513','2021-02-27 13:02:17.255531',75,1,1,'_113','Обслуживание','','','',23,0,'check-circle','','','',''),(116,NULL,'2021-02-27 13:02:17.256288','2021-02-27 13:02:17.256305',78,1,1,'_113','Тех помощь','','','',23,0,'check-circle','','','',''),(117,NULL,'2021-02-27 13:02:17.257083','2021-02-27 13:02:17.257102',1,1,1,'','Описание','','','',23,0,'','','','Мы предлагаем вам различные варианты обслуживания, выберите для себя подходящее решение<br>',''),(118,NULL,'2021-02-27 13:08:14.088836','2021-02-27 13:08:50.715266',79,1,1,'','Контакты','','','',24,0,'','','','Напишите нам и мы обязательно вам ответим<br>тел + 7 (3952) 123-321<br>адрес: Ржанова 164, офис 204<br>',''),(119,NULL,'2021-02-27 13:09:37.867927','2021-02-27 13:09:37.867945',79,1,1,'','Контакты','','','',25,0,'','','','Напишите нам и мы обязательно вам ответим<br>тел + 7 (3952) 123-321<br>адрес: Ржанова 164, офис 204<br>',''),(120,NULL,'2021-02-28 13:17:04.412383','2021-02-28 13:28:35.498051',80,1,1,'','Ссылка на видео mp4 из файлов','','/media/misc/loop-bg.mp4','',26,0,'','','','',''),(121,NULL,'2021-02-28 13:17:45.021916','2021-02-28 13:27:48.022724',80,1,1,'','Ссылка на видео mp4 из файлов','','/video-bg.mp4','',27,0,'','','','',''),(126,NULL,'2021-02-28 14:01:27.821191','2021-02-28 14:01:59.896638',81,1,1,'','Главная','','#home','home',28,0,'home','','','',''),(127,NULL,'2021-02-28 14:02:07.908317','2021-02-28 14:02:38.817245',82,1,1,'','О нас','','#about','about',28,0,'book','','','',''),(128,NULL,'2021-02-28 14:02:11.031651','2021-02-28 14:02:51.864372',83,1,1,'','Проекты','','#gallery','gallery',28,0,'camera','','','',''),(129,NULL,'2021-02-28 14:02:16.497285','2021-02-28 14:03:04.862502',84,1,1,'','Подписаться','','#subscribe','subscribe',28,0,'envelope-o','','','',''),(130,NULL,'2021-02-28 14:02:19.932196','2021-02-28 14:03:17.368578',85,1,1,'','Контакты','','#contact','contact',28,0,'phone','','','',''),(131,NULL,'2021-02-28 14:03:58.889287','2021-03-10 14:56:54.382963',81,1,1,'','Light Bee','','#homepage','homepage',29,0,'','','','',''),(132,NULL,'2021-02-28 14:03:58.890239','2021-03-10 14:56:50.697413',82,1,1,'','Storm Bee','','#imagepage','imagepage',29,0,'','','','',''),(133,NULL,'2021-02-28 14:03:58.891014','2021-03-10 14:56:47.583217',83,1,1,'','Новости','','#newspage','newspage',29,0,'','','','',''),(136,NULL,'2021-03-03 21:42:12.871998','2021-03-05 19:11:34.434973',86,1,4,'','Электро Байк SUR-RON X Light bee','','/product/elektro-bayk-sur-ron-x-light-bee-1/','product_1',31,0,NULL,'','',NULL,NULL),(137,'137.jpg','2021-03-03 21:43:29.454621','2021-03-03 23:32:20.395135',87,1,4,'','Продукция','','/cat/produkciya/','',30,0,'','','','',''),(138,'08e66b592a05f63426bc098fdc5a0622.png','2021-03-03 21:43:34.216121','2021-03-03 23:32:59.423467',88,1,4,'','Аксессуары','','/cat/aksessuary/','',30,0,'','','','',''),(139,'4341a13401a537fcc8a081a2e2447b0b.jpg','2021-03-03 21:43:38.448929','2021-03-03 23:33:27.189001',89,1,4,'','Запчасти','','/cat/zapchasti/','',30,0,'','','','',''),(140,NULL,'2021-03-03 22:40:19.808011','2021-03-03 22:40:19.808036',46,1,1,'','2020 год','Смотреть все','/',NULL,32,0,NULL,NULL,NULL,'<p><b>Расширение дилерской сети и производственных мощностей. </b></p>\r\n<p>По итогам 2020 года компания WHITE SIBERIA продала на рынке КНР свыше\r\n 3500 единиц электротранспорта, а на рынке стран СНГ - свыше 10 000. </p>\r\n<p>В странах СНГ компанию представляют 26 дилеров. В 2020 году состоялся выход на рынки Казахстана и Украины.</p>\r\n<p>Количество сборочных линий на производстве электротранспорта было увеличено до 4.</p>',NULL),(141,NULL,'2021-03-03 22:40:19.809113','2021-03-03 22:40:19.809130',47,1,1,'','2019 год',NULL,NULL,NULL,32,0,NULL,NULL,NULL,'<p><b>Масштабирование компании, повышение спроса и завоевание новых рынков сбыта. </b></p>\r\n<p>За 2019 год на территории КНР было продано свыше 3000 единиц \r\nэлектротранспорта. Это позволило компании масштабироваться и выйти на \r\nновые рынки сбыта. В начале года был открыт офис в Сочи, а буквально \r\nчерез 6 месяцев - в Москве и Минске.</p>',NULL),(142,NULL,'2021-03-03 22:40:19.812453','2021-03-03 22:40:19.812475',48,1,1,'','2018 год',NULL,NULL,NULL,32,0,NULL,NULL,NULL,'<p><b>Мощный рывок в развитии компании и выход в топ.</b></p>\r\n<p>В начале 2018 года состоялось открытие первого офиса и магазина \r\nэлектротранспорта в Шанхае, а к концу года WHITE SIBERIA вошла в топ \r\nкомпаний по продажам электротранспорта иностранцам, проживающим на \r\nтерритории КНР.</p>',NULL),(143,NULL,'2021-03-03 22:40:19.815972','2021-03-03 22:40:19.815992',49,1,1,'','2014 год',NULL,NULL,NULL,32,0,NULL,NULL,NULL,'<p><b>Год основания компании WHITE SIBERIA.</b></p>\r\n<p>В 2014 году в Шанхае была основана компания, которая до 2017 года \r\nзанималась продажей запчастей и комплектующих для коммерческого \r\nтранспорта.</p>',NULL),(144,NULL,'2021-03-03 22:40:19.835716','2021-03-03 22:40:19.835754',52,1,1,'','Политика в отношении обработки персональных данных',NULL,NULL,NULL,33,0,NULL,NULL,NULL,'<h3>1. Общие положения</h3>\r\n<p>Настоящая политика обработки персональных данных составлена в \r\nсоответствии с требованиями Федерального закона от 27.07.2006. №152-ФЗ \r\n«О персональных данных» и определяет порядок обработки персональных \r\nданных и меры по обеспечению безопасности персональных данных, \r\nпредпринимаемые ИП Соболев И.П. (далее – Оператор).</p>\r\n<ul><li>1.1. Оператор ставит своей важнейшей целью и условием осуществления\r\n своей деятельности соблюдение прав и свобод человека и гражданина при \r\nобработке его персональных данных, в том числе защиты прав на \r\nнеприкосновенность частной жизни, личную и семейную тайну.</li><li>1.2. Настоящая политика Оператора в отношении обработки \r\nперсональных данных (далее – Политика) применяется ко всей информации, \r\nкоторую Оператор может получить о посетителях <a href=\"https://white-siberia.com/\">веб-сайта</a>.</li></ul>\r\n<h3>2. Основные понятия, используемые в Политике</h3>\r\n<ul><li>2.1. Автоматизированная обработка персональных данных – обработка персональных данных с помощью средств вычислительной техники;</li><li>2.2. Блокирование персональных данных – временное прекращение \r\nобработки персональных данных (за исключением случаев, если обработка \r\nнеобходима для уточнения персональных данных);</li><li>2.3. Веб-сайт – совокупность графических и информационных \r\nматериалов, а также программ для ЭВМ и баз данных, обеспечивающих их \r\nдоступность в сети интернет по сетевому адресу <a href=\"https://white-siberia.com/\">https://www.white-siberia.com/</a>;</li><li>2.4. Информационная система персональных данных — совокупность \r\nсодержащихся в базах данных персональных данных, и обеспечивающих их \r\nобработку информационных технологий и технических средств;</li><li>2.5. Обезличивание персональных данных — действия, в результате \r\nкоторых невозможно определить без использования дополнительной \r\nинформации принадлежность персональных данных конкретному Пользователю \r\nили иному субъекту персональных данных;</li><li>2.6. Обработка персональных данных – любое действие (операция) или \r\nсовокупность действий (операций), совершаемых с использованием средств \r\nавтоматизации или без использования таких средств с персональными \r\nданными, включая сбор, запись, систематизацию, накопление, хранение, \r\nуточнение (обновление, изменение), извлечение, использование, передачу \r\n(распространение, предоставление, доступ), обезличивание, блокирование, \r\nудаление, уничтожение персональных данных;</li><li>2.7. Оператор – государственный орган, муниципальный орган, \r\nюридическое или физическое лицо, самостоятельно или совместно с другими \r\nлицами организующие и (или) осуществляющие обработку персональных \r\nданных, а также определяющие цели обработки персональных данных, состав \r\nперсональных данных, подлежащих обработке, действия (операции), \r\nсовершаемые с персональными данными;</li><li>2.8. Персональные данные – любая информация, относящаяся прямо или косвенно к определенному или определяемому Пользователю <a href=\"https://white-siberia.com/\">веб-сайта</a>;</li><li>2.9. Пользователь – любой посетитель <a href=\"https://white-siberia.com/\">веб-сайта</a>;</li><li>2.10. Предоставление персональных данных – действия, направленные \r\nна раскрытие персональных данных определенному лицу или определенному \r\nкругу лиц;</li><li>2.11. Распространение персональных данных – любые действия, \r\nнаправленные на раскрытие персональных данных неопределенному кругу лиц \r\n(передача персональных данных) или на ознакомление с персональными \r\nданными неограниченного круга лиц, в том числе обнародование \r\nперсональных данных в средствах массовой информации, размещение в \r\nинформационно-телекоммуникационных сетях или предоставление доступа к \r\nперсональным данным каким-либо иным способом;</li><li>2.12. Трансграничная передача персональных данных – передача \r\nперсональных данных на территорию иностранного государства органу власти\r\n иностранного государства, иностранному физическому или иностранному \r\nюридическому лицу;</li><li>2.13. Уничтожение персональных данных – любые действия, в \r\nрезультате которых персональные данные уничтожаются безвозвратно с \r\nневозможностью дальнейшего восстановления содержания персональных данных\r\n в информационной системе персональных данных и (или) уничтожаются \r\nматериальные носители персональных данных.</li></ul>\r\n<h3>3. Оператор может обрабатывать следующие персональные данные Пользователя</h3>\r\n<ul><li>3.1. Фамилия, имя, отчество;</li><li>3.2. Электронный адрес;</li><li>3.3. Номера телефонов;</li><li>3.4. Название организации;</li><li>3.5. Также на сайте происходит сбор и обработка обезличенных данных\r\n о посетителях (в т.ч. файлов «cookie») с помощью сервисов \r\nинтернет-статистики (Яндекс Метрика и Гугл Аналитика и других).</li><li>3.6. Вышеперечисленные данные далее по тексту Политики объединены общим понятием Персональные данные.</li></ul>\r\n<h3>4. Цели обработки персональных данных</h3>\r\n<ul><li>4.1. Цель обработки персональных данных Пользователя — заключение, \r\nисполнение и прекращение гражданско-правовых договоров; предоставление \r\nдоступа Пользователю к сервисам, информации и/или материалам, \r\nсодержащимся на веб-сайте.</li><li>4.2. Также Оператор имеет право направлять Пользователю уведомления\r\n о новых продуктах и услугах, специальных предложениях и различных \r\nсобытиях. Пользователь всегда может отказаться от получения \r\nинформационных сообщений, направив Оператору письмо на адрес электронной\r\n почты <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a> с пометкой «Отказ от уведомлений о новых продуктах и услугах и специальных предложениях».</li><li>4.3. Обезличенные данные Пользователей, собираемые с помощью \r\nсервисов интернет-статистики, служат для сбора информации о действиях \r\nПользователей на сайте, улучшения качества сайта и его содержания.</li></ul>\r\n<h3>5. Правовые основания обработки персональных данных</h3>\r\n<ul><li>5.1. Оператор обрабатывает персональные данные Пользователя только в\r\n случае их заполнения и/или отправки Пользователем самостоятельно через \r\nспециальные формы, расположенные на <a href=\"https://white-siberia.com/\">сайте</a>.\r\n Заполняя соответствующие формы и/или отправляя свои персональные данные\r\n Оператору, Пользователь выражает свое согласие с данной Политикой.</li><li>5.2. Оператор обрабатывает обезличенные данные о Пользователе в \r\nслучае, если это разрешено в настройках браузера Пользователя (включено \r\nсохранение файлов «cookie» и использование технологии JavaScript).</li></ul>\r\n<h3>6. Порядок сбора, хранения, передачи и других видов обработки персональных данных</h3>\r\n<p>Безопасность персональных данных, которые обрабатываются Оператором, \r\nобеспечивается путем реализации правовых, организационных и технических \r\nмер, необходимых для выполнения в полном объеме требований действующего \r\nзаконодательства в области защиты персональных данных.</p>\r\n<ul><li>6.1. Оператор обеспечивает сохранность персональных данных и \r\nпринимает все возможные меры, исключающие доступ к персональным данным \r\nнеуполномоченных лиц.</li><li>6.2. Персональные данные Пользователя никогда, ни при каких \r\nусловиях не будут переданы третьим лицам, за исключением случаев, \r\nсвязанных с исполнением действующего законодательства.</li><li>6.3. В случае выявления неточностей в персональных данных, \r\nПользователь может актуализировать их самостоятельно, путем направления \r\nОператору уведомление на адрес электронной почты Оператора <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a> с пометкой «Актуализация персональных данных».</li><li>6.4. Срок обработки персональных данных является неограниченным. \r\nПользователь может в любой момент отозвать свое согласие на обработку \r\nперсональных данных, направив Оператору уведомление посредством \r\nэлектронной почты на электронный адрес Оператора <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a> с пометкой «Отзыв согласия на обработку персональных данных».</li></ul>\r\n<h3>7. Трансграничная передача персональных данных</h3>\r\n<ul><li>7.1. Оператор до начала осуществления трансграничной передачи \r\nперсональных данных обязан убедиться в том, что иностранным \r\nгосударством, на территорию которого предполагается осуществлять \r\nпередачу персональных данных, обеспечивается надежная защита прав \r\nсубъектов персональных данных.</li><li>7.2. Трансграничная передача персональных данных на территории \r\nиностранных государств, не отвечающих вышеуказанным требованиям, может \r\nосуществляться только в случае наличия согласия в письменной форме \r\nсубъекта персональных данных на трансграничную передачу его персональных\r\n данных и/или исполнения договора, стороной которого является субъект \r\nперсональных данных.</li></ul>\r\n<h3>8. Заключительные положения</h3>\r\n<ul><li>8.1. Пользователь может получить любые разъяснения по интересующим \r\nвопросам, касающимся обработки его персональных данных, обратившись к \r\nОператору с помощью электронной почты <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a>.</li><li>8.2. В данном документе будут отражены любые изменения политики \r\nобработки персональных данных Оператором. Политика действует бессрочно \r\nдо замены ее новой версией.</li><li>8.3. Актуальная версия Политики в свободном доступе расположена в сети Интернет на <a href=\"https://white-siberia.com/privacy/\">этой странице</a>.</li></ul>',NULL),(145,'ower-2.png','2021-03-03 22:40:19.885488','2021-03-03 22:40:19.885513',122,1,1,'','Надежность, функциональность и мощь',NULL,NULL,NULL,34,0,NULL,NULL,NULL,'<div>\r\n											<ul><li>Грузоподъемность до 260 кг</li><li>Мотор тягового типа мощностью 3000 Вт</li><li>Возможность всесезонной эксплуатации</li><li>Шикарная комплектация: бокс, сетка-багажник, держатель для телефона, удобная спинка</li></ul>\r\n										</div>',NULL),(146,'ower-3.png','2021-03-03 22:40:19.903218','2021-03-03 22:40:19.903245',123,1,1,'','Максимальный комфорт даже на бездорожье',NULL,NULL,NULL,34,0,NULL,NULL,NULL,'<div>\r\n											<ul><li>Комфортная и динамичная езда благодаря 10–дюймовым колёсам</li><li>Большое и мягкое сиденье </li><li>Настраиваемая подвеска</li></ul>\r\n										</div>',NULL),(147,'ower-1.png','2021-03-03 22:40:19.940814','2021-03-03 22:40:19.940841',124,1,1,'','Безопасное передвижение в темное время суток',NULL,NULL,NULL,34,0,NULL,NULL,NULL,'<div>\r\n											<ul><li>1 мощная фара + 2 стробоскопа (вспомогательный свет)</li><li>Яркие задние ходовые огни, сертифицированные ECC</li><li>Поворотники LED с ярким свечением </li></ul>\r\n										</div>',NULL),(148,'ower-4.png','2021-03-03 22:40:19.957465','2021-03-03 22:40:19.957491',125,1,1,'','Уверенность в каждом километре',NULL,NULL,NULL,34,0,NULL,NULL,NULL,'<div>\r\n											<ul><li>Максимальная скорость до 45 км/ч</li><li>Тормозная система нового вида с возможностью регулировки</li><li>Обновленная тормозная система с возможностью регулировки</li><li>Масляные амортизаторы с возможностью регулировки</li><li>Плавность старта и торможения</li></ul>\r\n										</div>',NULL),(149,'ower-5.png','2021-03-03 22:40:19.990669','2021-03-03 22:40:19.990705',126,1,1,'','Инновационный LI-ION аккумулятор',NULL,NULL,NULL,34,0,NULL,NULL,NULL,'<div>\r\n											<ul><li>Пробег до 60 км на одном заряде</li><li>Быстросъёмный аккумулятор с балансировочной платой</li><li>Возможность установить вторую батарею и проезжать до 100 км</li><li>Производство TAIWAN</li></ul>\r\n										</div>',NULL),(150,'ower-6.png','2021-03-03 22:40:20.021968','2021-03-03 22:40:20.022005',127,1,1,'','Удобство и простота использования',NULL,NULL,NULL,34,0,NULL,NULL,NULL,'<div>\r\n											<ul><li>Большие, интуитивно понятные кнопки управления</li><li>Бортовой компьютер с LED-дисплеем</li><li>Большие зеркала без искажения</li><li>Держатель телефона с USB</li><li>Вместительный бокс и сетка-багажник</li><li>Кнопка Start-Stop</li><li>Сигнализация</li></ul>\r\n										</div>',NULL),(151,'banner.png','2021-03-03 22:40:20.078778','2021-03-03 22:40:20.078805',50,1,1,'','В семью!','Подробнее','/',NULL,35,0,NULL,NULL,NULL,'<p>Электротранспорт под брендом WHITE SIBERIA – это качество, \r\nнадежность, стильный дизайн и приемлемая цена. Именно поэтому наша \r\nдилерская сеть стремительно растет, а ассортимент техники на витринах \r\nмагазинов в России и странах СНГ – расширяется.</p>\r\n						<p>Если Вы хотите стать участником нашей дилерской сети и \r\nприсоединиться к выполнению нашей миссии – заполните форму, и мы \r\nобязательно свяжемся с Вами.</p>',NULL),(152,'surron-logo.png','2021-03-03 22:40:20.136762','2021-03-03 22:40:20.136787',98,1,1,'','SUR-RON','Перейти на сайт','https://surronrussia.ru/',NULL,36,1,NULL,NULL,NULL,'Мы являемся<br>официальными представителями<br>техники SUR-RON',NULL),(153,NULL,'2021-03-03 22:40:20.196420','2021-03-03 22:40:20.196445',54,1,1,'','Россия',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(154,NULL,'2021-03-03 22:40:20.197368','2021-03-03 22:40:20.197385',58,1,1,'_153','Адреса',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(155,NULL,'2021-03-03 22:40:20.198145','2021-03-03 22:40:20.198161',69,1,1,'_153_154','Адрес1',NULL,NULL,NULL,38,0,'map-marker',NULL,NULL,'г. Москва, дер. Марушкино, ул. Северная\r\n<br>',NULL),(156,NULL,'2021-03-03 22:40:20.198947','2021-03-03 22:40:20.198963',70,1,1,'_153_154','Адрес2',NULL,NULL,NULL,38,0,'map-marker',NULL,NULL,'г. Сочи, Адлерский р-н, ул. Садовая 48',NULL),(157,NULL,'2021-03-03 22:40:20.199747','2021-03-03 22:40:20.199762',62,1,1,'_153','Оптовый отдел',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(158,NULL,'2021-03-03 22:40:20.200793','2021-03-03 22:40:20.200817',75,1,1,'_153_157','Телефон',NULL,NULL,NULL,38,0,'phone',NULL,NULL,'<a href=\"tel:+79384704147\">+7 938 470 41 47</a>',NULL),(159,NULL,'2021-03-03 22:40:20.201747','2021-03-03 22:40:20.201765',76,1,1,'_153_157','WhatsApp',NULL,NULL,NULL,38,0,'phone-square',NULL,NULL,'+7 938 470 41 47',NULL),(160,NULL,'2021-03-03 22:40:20.202546','2021-03-03 22:40:20.202562',77,1,1,'_153_157','Email',NULL,NULL,NULL,38,0,'envelope-o',NULL,NULL,'opt@white-siberia.com',NULL),(161,NULL,'2021-03-03 22:40:20.203313','2021-03-03 22:40:20.203328',66,1,1,'_153','Розничный отдел',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(162,NULL,'2021-03-03 22:40:20.204097','2021-03-03 22:40:20.204113',78,1,1,'_153_161','Телефон',NULL,NULL,NULL,38,0,'phone',NULL,NULL,'+7 988 169 16 39',NULL),(163,NULL,'2021-03-03 22:40:20.204883','2021-03-03 22:40:20.204898',79,1,1,'_153_161','WhatsApp',NULL,NULL,NULL,38,0,'phone-square',NULL,NULL,'+7 988 403 85 43',NULL),(164,NULL,'2021-03-03 22:40:20.205650','2021-03-03 22:40:20.205665',80,1,1,'_153_161','Email',NULL,NULL,NULL,38,0,'envelope-o',NULL,NULL,'roznica@white-siberia.com',NULL),(165,NULL,'2021-03-03 22:40:20.206662','2021-03-03 22:40:20.206681',67,1,1,'_153','Гарантийный отдел',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(166,NULL,'2021-03-03 22:40:20.207598','2021-03-03 22:40:20.207616',81,1,1,'_153_165','Телефон',NULL,NULL,NULL,38,0,'phone',NULL,NULL,'+7 989 085 87 45',NULL),(167,NULL,'2021-03-03 22:40:20.208518','2021-03-03 22:40:20.208536',82,1,1,'_153_165','WhatsApp',NULL,NULL,NULL,38,0,'phone-square',NULL,NULL,'+7 989 085 87 45',NULL),(168,NULL,'2021-03-03 22:40:20.209319','2021-03-03 22:40:20.209334',83,1,1,'_153_165','Email',NULL,NULL,NULL,38,0,'envelope-o',NULL,NULL,'guarantee@white-siberia.com',NULL),(169,NULL,'2021-03-03 22:40:20.210078','2021-03-03 22:40:20.210093',55,1,1,'','Беларусь',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(170,NULL,'2021-03-03 22:40:20.210824','2021-03-03 22:40:20.210839',59,1,1,'_169','Адреса',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(171,NULL,'2021-03-03 22:40:20.211603','2021-03-03 22:40:20.211618',71,1,1,'_169_170','Адрес1',NULL,NULL,NULL,38,0,'map-marker',NULL,NULL,'г. Минск Новая Боровая, Авиационная 10',NULL),(172,NULL,'2021-03-03 22:40:20.212388','2021-03-03 22:40:20.212403',63,1,1,'_169','Оптовый отдел',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(173,NULL,'2021-03-03 22:40:20.213141','2021-03-03 22:40:20.213156',84,1,1,'_169_172','Телефон',NULL,NULL,NULL,38,0,'phone',NULL,NULL,'<a href=\"tel:+375333274526\">+375 33 327 45 26</a>',NULL),(174,NULL,'2021-03-03 22:40:20.213905','2021-03-03 22:40:20.213920',85,1,1,'_169_172','WhatsApp',NULL,NULL,NULL,38,0,'phone-square',NULL,NULL,'<a href=\"https://wa.me/375333274526\">+375 33 327 45 26</a>',NULL),(175,NULL,'2021-03-03 22:40:20.214662','2021-03-03 22:40:20.214677',86,1,1,'_169_172','Email',NULL,NULL,NULL,38,0,'envelope-o',NULL,NULL,'<a href=\"mailto:opt@white-siberia.com\">opt@white-siberia.com</a>',NULL),(176,NULL,'2021-03-03 22:40:20.215447','2021-03-03 22:40:20.215462',56,1,1,'','Китай',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(177,NULL,'2021-03-03 22:40:20.218023','2021-03-03 22:40:20.218049',60,1,1,'_176','Адреса',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(178,NULL,'2021-03-03 22:40:20.218966','2021-03-03 22:40:20.218985',72,1,1,'_176_177','Адрес1',NULL,NULL,NULL,38,0,'map-marker',NULL,NULL,'Shanghai Channing district Channing street 398',NULL),(179,NULL,'2021-03-03 22:40:20.219851','2021-03-03 22:40:20.219869',73,1,1,'_176_177','Адрес2',NULL,NULL,NULL,38,0,'map-marker',NULL,NULL,'Shanghai Jiading district JiaSongbei street 6855',NULL),(180,NULL,'2021-03-03 22:40:20.220705','2021-03-03 22:40:20.220722',64,1,1,'_176','Оптовый отдел',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(181,NULL,'2021-03-03 22:40:20.221571','2021-03-03 22:40:20.221588',87,1,1,'_176_180','Телефон',NULL,NULL,NULL,38,0,'phone',NULL,NULL,'<a href=\"tel:+8613167039323\">+86 131 6703 9323</a>',NULL),(182,NULL,'2021-03-03 22:40:20.222466','2021-03-03 22:40:20.222483',88,1,1,'_176_180','WhatsApp',NULL,NULL,NULL,38,0,'phone-square',NULL,NULL,'<a href=\"https://wa.me/8613167039323\">+86 131 6703 9323</a>',NULL),(183,NULL,'2021-03-03 22:40:20.223316','2021-03-03 22:40:20.223333',89,1,1,'_176_180','Email',NULL,NULL,NULL,38,0,'envelope-o',NULL,NULL,'<a href=\"mailto:opt@white-siberia.com\">opt@white-siberia.com</a>',NULL),(184,NULL,'2021-03-03 22:40:20.224107','2021-03-03 22:40:20.224124',68,1,1,'_176','WeChat ID',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(185,NULL,'2021-03-03 22:40:20.224874','2021-03-03 22:40:20.224890',90,1,1,'_176_184','Без названия',NULL,NULL,NULL,38,0,'wechat',NULL,NULL,'motobike-shanghai',NULL),(186,NULL,'2021-03-03 22:40:20.225657','2021-03-03 22:40:20.225673',57,1,1,'','Казахстан',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(187,NULL,'2021-03-03 22:40:20.226445','2021-03-03 22:40:20.226461',61,1,1,'_186','Адреса',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(188,NULL,'2021-03-03 22:40:20.227330','2021-03-03 22:40:20.227350',74,1,1,'_186_187','Адрес1',NULL,NULL,NULL,38,0,'map-marker',NULL,NULL,'г. Караганда, ул. Крылова, д. 101',NULL),(189,NULL,'2021-03-03 22:40:20.228266','2021-03-03 22:40:20.228282',65,1,1,'_186','Оптовый отдел',NULL,NULL,NULL,38,0,NULL,NULL,NULL,NULL,NULL),(190,NULL,'2021-03-03 22:40:20.229051','2021-03-03 22:40:20.229068',91,1,1,'_186_189','Телефон',NULL,NULL,NULL,38,0,'phone',NULL,NULL,'<a href=\"tel:+77711290202\">+7 771 129 02 02</a>',NULL),(191,NULL,'2021-03-03 22:40:20.229851','2021-03-03 22:40:20.229867',92,1,1,'_186_189','WhatsApp',NULL,NULL,NULL,38,0,'phone-square',NULL,NULL,'<a href=\"https://wa.me/77711290202\">+7 771 129 02 02</a>',NULL),(192,NULL,'2021-03-03 22:40:20.232023','2021-03-03 22:40:20.232039',93,1,1,'_186_189','Email',NULL,NULL,NULL,38,0,'envelope-o',NULL,NULL,'<a href=\"mailto:opt@white-siberia.com\">opt@white-siberia.com</a>',NULL),(193,NULL,'2021-03-03 22:40:20.255287','2021-03-03 22:40:20.255312',234,1,1,'','Без названия',NULL,NULL,NULL,39,0,NULL,NULL,NULL,NULL,NULL),(194,NULL,'2021-03-03 22:40:20.271483','2021-03-03 22:40:20.271507',51,1,1,'','Описание',NULL,NULL,NULL,40,0,NULL,NULL,NULL,'<p>Если Вы хотите стать участником нашей дилерской сети и \r\nпопуляризировать электротранспорт вместе с нами – заполните форму, и мы \r\nобязательно свяжемся с Вами в ближайшее время. </p>\r\n<p>В графе «Дополнительные сведения» просим Вас указать следующую информацию: </p>\r\n<p>Есть ли у Вас опыт продаж или обслуживания электротранспорта?</p>\r\n<p>Вы планируете продажи онлайн или оффлайн? </p>\r\n<p>Есть ли у Вас розничная точка продаж? </p>\r\n<p>Укажите Ваш сайт (если есть).</p>\r\n<p>Будем рады поработать вместе с Вами!</p>',NULL),(195,'40.jpg','2021-03-03 22:40:20.324233','2021-03-03 22:40:20.324268',38,1,1,'','WS-PRO 2WD',NULL,'/',NULL,42,0,NULL,NULL,NULL,'60v 4000w',NULL),(196,'41.jpg','2021-03-03 22:40:20.341570','2021-03-03 22:40:20.341595',39,1,1,'','WS-PRO MAX+',NULL,'/',NULL,42,0,NULL,NULL,NULL,'60v 3000w',NULL),(197,'42.png','2021-03-03 22:40:20.359011','2021-03-03 22:40:20.359034',40,1,1,'','WS-TAIGA',NULL,'/',NULL,42,0,NULL,NULL,NULL,'48v 800w',NULL),(198,NULL,'2021-03-03 22:40:20.399302','2021-03-03 22:40:20.399326',99,1,1,'','video1','Перейти на YouTube','https://www.youtube.com/channel/UCLMxls9urKSgQdE7setOt9w',NULL,43,1,'youtube-play',NULL,NULL,'<iframe src=\"https://www.youtube.com/embed/u8Tx7XC5q8k\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" width=\"398\" height=\"199\" frameborder=\"0\"></iframe>',NULL),(199,NULL,'2021-03-03 22:40:20.406040','2021-03-03 22:40:20.406064',100,1,1,'','video2',NULL,NULL,NULL,43,0,NULL,NULL,NULL,'<iframe width=\"398\" height=\"199\" src=\"https://www.youtube.com/embed/L8OU9xwCUXE\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>',NULL),(200,NULL,'2021-03-03 22:40:20.411806','2021-03-03 22:40:20.411828',101,1,1,'','video3',NULL,NULL,NULL,43,0,NULL,NULL,NULL,'<iframe width=\"398\" height=\"199\" src=\"https://www.youtube.com/embed/t_l9If6U_J4\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>',NULL),(201,NULL,'2021-03-03 22:40:20.412661','2021-03-03 22:40:20.412677',102,1,1,'','video4',NULL,NULL,NULL,43,0,NULL,NULL,NULL,'<iframe src=\"https://www.youtube.com/embed/lfSkjl0Qu68\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" width=\"398\" height=\"199\" frameborder=\"0\"></iframe>',NULL),(202,NULL,'2021-03-03 22:47:36.726924','2021-03-03 22:47:52.868816',99,1,1,'','video1','Перейти на YouTube','','',44,1,'youtube-play','','','<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/jcf5lLeU1Ko\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>',''),(203,NULL,'2021-03-03 22:47:36.729015','2021-03-03 22:48:24.598272',100,1,1,'','video2','','','',44,0,'','','','<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/Dms456im8fQ\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>',''),(206,NULL,'2021-03-05 09:31:29.013993','2021-03-05 19:11:22.103821',235,1,4,'','Электро Байк SUR-RON S Light bee','','/product/elektro-bayk-sur-ron-s-light-bee-2/','product_2',31,0,NULL,'','',NULL,NULL),(207,NULL,'2021-03-05 19:05:47.294339','2021-03-05 19:06:25.798458',236,1,4,'','Электро Байк SUR-RON L1E Light bee','','/product/elektro-bayk-sur-ron-l1e-light-bee-3/','product_3',31,0,NULL,'','',NULL,NULL),(208,NULL,'2021-03-05 19:08:05.799027','2021-03-06 11:30:17.274735',237,1,4,'','SUR-RON Storm BEE Кросс','','/product/sur-ron-storm-bee-kross-4/','product_4',31,0,NULL,'','',NULL,NULL),(209,NULL,'2021-03-06 11:27:14.626750','2021-03-06 11:37:20.254373',238,1,4,'','SUR-RON Storm BEE Кросс','','/product/sur-ron-storm-bee-kross-5/','product_5',31,0,NULL,'','',NULL,NULL),(210,NULL,'2021-03-06 11:56:27.406241','2021-03-06 11:56:27.406274',239,1,1,'','Без названия',NULL,NULL,NULL,46,0,NULL,NULL,NULL,NULL,NULL),(212,NULL,'2021-03-06 12:02:02.584655','2021-03-06 12:02:02.584682',239,1,1,'','Без названия',NULL,NULL,NULL,48,0,NULL,NULL,NULL,NULL,NULL),(213,NULL,'2021-03-08 13:20:05.055506','2021-03-08 13:20:07.838344',1,1,4,'','Каталог','','/cat/','',49,0,'','','','',''),(214,NULL,'2021-03-08 13:20:16.015574','2021-03-08 13:20:16.015596',2,1,4,'','Написать нам',NULL,'/napisat-nam/',NULL,49,0,NULL,NULL,NULL,NULL,NULL),(215,NULL,'2021-03-08 13:20:20.744639','2021-03-08 13:20:20.744658',3,1,4,'','Как нас найти',NULL,'/kak-nas-nayti/',NULL,49,0,NULL,NULL,NULL,NULL,NULL),(216,NULL,'2021-03-08 13:20:25.390196','2021-03-08 13:20:32.321531',4,1,4,'','Light Bee','','/bez-nazvaniya/','',49,0,'','','','',''),(217,NULL,'2021-03-08 13:20:38.894061','2021-03-08 13:20:38.894081',5,1,4,'','Light Bee S',NULL,'/light-bee-s/',NULL,49,0,NULL,NULL,NULL,NULL,NULL),(218,NULL,'2021-03-08 13:20:48.099370','2021-03-08 13:20:48.099389',6,1,4,'','Storm Bee',NULL,'/storm-bee/',NULL,49,0,NULL,NULL,NULL,NULL,NULL),(221,NULL,'2021-03-10 11:42:38.671325','2021-03-10 11:43:58.117919',52,1,1,'','Light Bee','Подробнее','/light-bee/','',6,0,'','','','Мы предлагаем вам познакомиться поближе с Light Bee, который точно не оставит вас равнодушным и подарит массу положительных впечатлений<br>',''),(222,'two-section-bg.jpg','2021-03-10 11:49:28.111447','2021-03-10 11:53:45.070109',59,1,1,'','Storm Bee','Подробнее','/','',50,0,'','','','SUR-RON Light Bee S предназначен для дорог общего пользования',''),(224,'two-section-bg.jpg','2021-03-10 11:55:06.079578','2021-03-10 11:55:06.079604',59,1,1,'','Storm Bee','Подробнее','/','',51,0,'','','','SUR-RON Light Bee S предназначен для дорог общего пользования',''),(225,'race-big-1.jpg','2021-03-10 13:36:53.054150','2021-03-10 13:57:48.274990',240,1,1,'','Соревнования 2019','','','half',52,0,'','','','<span><span>Серия соревнований Guangzhou Motorcycle Extreme Challenge 2019 открыла последний этап, и последний этап является самым сложным.</span></span>',''),(226,'race-big-en-3.jpg','2021-03-10 13:38:40.470167','2021-03-10 13:57:51.196696',241,1,1,'','Гарантия безопасности','','','half',52,0,'','','','Продукты surron требуют много исследований, проработанного дизайна и полного тестирования, которые были сделаны за небольшие сроки<br><br>',''),(227,'race-small-1.jpg','2021-03-10 13:58:15.671744','2021-03-10 14:45:59.860369',242,1,1,'','Название события 1','','','',52,0,'','','','Краткое описание события 1<br>',''),(228,'race-small-2.jpg','2021-03-10 13:58:32.853347','2021-03-10 14:46:13.997721',243,1,1,'','Название события 2','','','',52,0,'','','','Краткое описание события 2<br>',''),(229,'race-small-3.jpg','2021-03-10 13:58:47.420676','2021-03-10 14:46:37.709649',244,1,1,'','Название события 3','','','',52,0,'','','','Краткое описание события 4',''),(230,'race-small-4.jpg','2021-03-10 13:59:04.331865','2021-03-10 14:46:33.415000',245,1,1,'','Название события 4','','','',52,0,'','','','Краткое описание события 4<br>',''),(231,'star-big-1.jpg','2021-03-10 14:48:59.442805','2021-03-10 14:50:13.954164',246,1,1,'','Крупное событие 1','','','half',52,0,'','','','Краткое описание крупного события 1<br>',''),(233,'star-big-2.jpg','2021-03-10 14:49:10.209406','2021-03-10 14:50:10.353297',247,1,1,'','Крупное событие 2','','','half',52,0,'','','','Краткое описание крупного события 2<br>',''),(234,'race-big-1.jpg','2021-03-10 14:50:45.661483','2021-03-10 14:50:45.661512',240,1,1,'','Соревнования 2019','','','half',53,0,'','','','<span><span>Серия соревнований Guangzhou Motorcycle Extreme Challenge 2019 открыла последний этап, и последний этап является самым сложным.</span></span>',''),(235,'race-big-en-3.jpg','2021-03-10 14:50:45.690350','2021-03-10 14:50:45.690377',241,1,1,'','Гарантия безопасности','','','half',53,0,'','','','Продукты surron требуют много исследований, проработанного дизайна и полного тестирования, которые были сделаны за небольшие сроки<br><br>',''),(236,'race-small-1.jpg','2021-03-10 14:50:45.705293','2021-03-10 14:50:45.705319',242,1,1,'','Название события 1','','','',53,0,'','','','Краткое описание события 1<br>',''),(237,'race-small-2.jpg','2021-03-10 14:50:45.721157','2021-03-10 14:50:45.721186',243,1,1,'','Название события 2','','','',53,0,'','','','Краткое описание события 2<br>',''),(238,'race-small-3.jpg','2021-03-10 14:50:45.745156','2021-03-10 14:50:45.745189',244,1,1,'','Название события 3','','','',53,0,'','','','Краткое описание события 4',''),(239,'race-small-4.jpg','2021-03-10 14:50:45.775142','2021-03-10 14:50:45.775170',245,1,1,'','Название события 4','','','',53,0,'','','','Краткое описание события 4<br>',''),(240,'star-big-1.jpg','2021-03-10 14:50:45.790901','2021-03-10 14:50:45.790928',246,1,1,'','Крупное событие 1','','','half',53,0,'','','','Краткое описание крупного события 1<br>',''),(241,'star-big-2.jpg','2021-03-10 14:50:45.806862','2021-03-10 14:50:45.806889',247,1,1,'','Крупное событие 2','','','half',53,0,'','','','Краткое описание крупного события 2<br>',''),(242,NULL,'2021-03-10 15:52:49.519605','2021-03-10 16:27:45.410011',52,1,1,'','50 кг','Подробнее','#about','',54,0,'','','','Снаряженная масса\r\nСверхлегкая конструкция',''),(244,NULL,'2021-03-10 16:06:28.231172','2021-03-10 16:28:08.237074',248,1,1,'','100+ км','','','',54,0,'','','','Эффективный запас хода\r\nБыстрая зарядка за 3 часа',''),(245,NULL,'2021-03-10 16:06:54.051312','2021-03-10 16:28:48.388912',249,1,1,'','250 N.M','','','',54,0,'','','','Максимальный крутящий момент\r\nПод углом более 45 градусов',''),(246,NULL,'2021-03-10 16:07:31.374830','2021-03-10 16:08:05.663115',250,1,1,'','Заказать','','','',54,0,'','','','',''),(247,NULL,'2021-03-10 16:43:33.453688','2021-03-10 16:43:33.453709',52,1,1,'','50 кг','Подробнее','#about','',56,0,'','','','Снаряженная масса\r\nСверхлегкая конструкция',''),(248,NULL,'2021-03-10 16:43:33.466323','2021-03-10 16:43:33.466345',248,1,1,'','100+ км','','','',56,0,'','','','Эффективный запас хода\r\nБыстрая зарядка за 3 часа',''),(249,NULL,'2021-03-10 16:43:33.480089','2021-03-10 16:43:33.480119',249,1,1,'','250 N.M','','','',56,0,'','','','Максимальный крутящий момент\r\nПод углом более 45 градусов',''),(250,NULL,'2021-03-10 16:43:33.483370','2021-03-10 16:43:33.483391',250,1,1,'','Заказать','','','',56,0,'','','','',''),(251,NULL,'2021-03-10 16:57:53.450628','2021-03-10 16:57:53.450654',239,1,1,'','Без названия',NULL,NULL,NULL,57,0,NULL,NULL,NULL,NULL,NULL),(252,NULL,'2021-03-10 17:44:28.157356','2021-03-10 22:19:02.603549',251,1,1,'','Отличные характеристики в сочетании с захватывающим внешним видом','Подробнее','','test360/34',58,0,'','','','<span><span>Light Bee сочетает в себе высокий крутящий момент от мотоцикла для бездорожья и легкий вес и маневренность велосипеда для скоростного спуска. Под динамичным внешним видом скрывается дикая и неудержимая сила</span></span>',''),(253,NULL,'2021-03-10 19:04:31.900644','2021-03-10 22:07:53.108012',251,1,1,'','Отличные характеристики в сочетании с захватывающим внешним видом','Подробнее','','light_bee/72',59,0,'','','','<span><span>Light Bee сочетает в себе высокий крутящий момент от мотоцикла для бездорожья и легкий вес и маневренность велосипеда для скоростного спуска. Под динамичным внешним видом скрывается дикая и неудержимая сила</span></span>',''),(254,NULL,'2021-03-10 22:48:10.185921','2021-03-10 22:52:25.777485',81,1,1,'','Light Bee X Version','','#advantagespage','advantagespage',60,0,'','','','',''),(255,NULL,'2021-03-10 22:48:10.197271','2021-03-15 11:22:19.260300',82,1,1,'','360° просмотр','','#spinner360','spinner360',60,0,'','','','',''),(256,NULL,'2021-03-10 22:48:10.198385','2021-03-15 11:22:28.821605',83,1,1,'','Легкий дизайн','','#videopage','videopage',60,0,'','','','',''),(257,NULL,'2021-03-10 22:48:10.200578','2021-03-15 11:22:35.549933',84,1,1,'','Произоводительность','','#videopage2','videopage2',60,0,'','','','',''),(258,NULL,'2021-03-10 22:48:10.202699','2021-03-15 11:22:43.169255',85,1,1,'','Система двигателя','','#videopage3','videopage3',60,0,'','','','',''),(259,NULL,'2021-03-10 22:51:16.623506','2021-03-15 11:22:55.061032',252,1,1,'','Проходимость','','#sliderpage2','sliderpage2',60,0,'','','','',''),(260,NULL,'2021-03-10 22:51:39.310657','2021-03-15 11:23:02.564439',253,1,1,'','Легкая управляемость','','#sliderpage3','sliderpage3',60,0,'','','','',''),(261,NULL,'2021-03-10 23:07:26.928527','2021-03-10 23:26:32.158862',52,1,1,'','Система задней подвески Intersect TR собственной разработки','Подробнее','/light_bee_two_videos.mp4','',61,0,'','','','<span><span>После тысяч испытаний на бездорожье и городских дорожных испытаний мы создали удивительную многорычажную систему задней подвески для легкой пчелы.</span> <span>Внешний вид сочетается с общей структурой автомобиля, а характеристики амортизации также регулируются в соответствии с характеристиками использования электрических велосипедов, чтобы шины могли постоянно поддерживать наилучшее сцепление с дорогой.</span></span>',''),(262,NULL,'2021-03-10 23:44:55.874523','2021-03-10 23:44:55.874552',52,1,1,'','Система задней подвески Intersect TR собственной разработки','Подробнее','/light_bee_two_videos.mp4','',62,0,'','','','<span><span>После тысяч испытаний на бездорожье и городских дорожных испытаний мы создали удивительную многорычажную систему задней подвески для легкой пчелы.</span> <span>Внешний вид сочетается с общей структурой автомобиля, а характеристики амортизации также регулируются в соответствии с характеристиками использования электрических велосипедов, чтобы шины могли постоянно поддерживать наилучшее сцепление с дорогой.</span></span>',''),(270,NULL,'2021-03-11 00:22:43.923074','2021-03-11 00:24:50.599266',52,1,1,'','Отличные спортивные результаты','Подробнее','/video-bg.mp4','',64,0,'','','','<span><span>В спортивном режиме высокая выходная мощность до 5 кВт и мгновенный крутящий момент на колесе с 250 Н · м позволяют легко справляться с такими навыками, как прыжки, наездник и т. д. Кроме того, набор профессиональных 19-дюймовых колес для бездорожья</span> <span>отлично владеет способностями к прохождению и никогда не застревает.</span> <span>Все это способствует улучшению спортивных результатов.</span></span>',''),(271,NULL,'2021-03-11 00:22:44.015576','2021-03-11 00:22:44.015603',254,1,1,'_270','1260 мм','','','',64,0,'','','','<span><span>Короткая колесная база<br> Легкость в управлении</span></span>',''),(272,NULL,'2021-03-11 00:22:44.027983','2021-03-11 00:22:44.028036',255,1,1,'_270','270 мм','','','',64,0,'','','','<span><span>Минимальный дорожный просвет<br> Легко восстанавливать при застревании</span></span>',''),(273,NULL,'2021-03-11 00:22:44.039977','2021-03-11 00:22:44.040001',256,1,1,'_270','203 мм','','','',64,0,'','','','<span><span>Дисковый тормоз большого размера<br> Высокая эффективность торможения</span></span>',''),(274,NULL,'2021-03-11 00:25:31.384554','2021-03-11 00:25:31.384580',52,1,1,'','Отличные спортивные результаты','Подробнее','/video-bg.mp4','',65,0,'','','','<span><span>В спортивном режиме высокая выходная мощность до 5 кВт и мгновенный крутящий момент на колесе с 250 Н · м позволяют легко справляться с такими навыками, как прыжки, наездник и т. д. Кроме того, набор профессиональных 19-дюймовых колес для бездорожья</span> <span>отлично владеет способностями к прохождению и никогда не застревает.</span> <span>Все это способствует улучшению спортивных результатов.</span></span>',''),(275,NULL,'2021-03-11 00:25:31.390119','2021-03-11 00:25:31.390144',254,1,1,'_274','1260 мм','','','',65,0,'','','','<span><span>Короткая колесная база<br> Легкость в управлении</span></span>',''),(276,NULL,'2021-03-11 00:25:31.396616','2021-03-11 00:25:31.396644',255,1,1,'_274','270 мм','','','',65,0,'','','','<span><span>Минимальный дорожный просвет<br> Легко восстанавливать при застревании</span></span>',''),(277,NULL,'2021-03-11 00:25:31.398775','2021-03-11 00:25:31.398798',256,1,1,'_274','203 мм','','','',65,0,'','','','<span><span>Дисковый тормоз большого размера<br> Высокая эффективность торможения</span></span>',''),(278,NULL,'2021-03-11 00:30:52.764555','2021-03-11 00:37:28.952229',52,1,1,'','Хорошо подобранная система EIC','Подробнее','/light_bee_motor.mp4','',66,0,'','','','<span><span>Система EIC разработана SURRON самостоятельно.</span> <span>После пяти тестовых поездок в провинции Сычуань и Тибет, а также постоянной обратной связи от лучших райдеров со всего мира, система EIC настроена на адаптацию к более сложным и суровым сценариям катания.</span></span>',''),(279,NULL,'2021-03-11 00:30:52.784097','2021-03-11 00:33:41.182826',254,1,1,'_278','Высокая производительность мотора','','','',66,0,'','','','<span><span><span><span>Максимальная частота вращения 5400 об / мин<br>Степень защиты IP55</span></span> </span></span>',''),(280,NULL,'2021-03-11 00:30:52.790882','2021-03-11 00:34:19.390971',255,1,1,'_278','FOC-контроллер синусоидальной волны','','','',66,0,'','','','<span><span><span><span>Составные алгоритмы с несколькими кривыми<br> Полная структура инкапсуляции</span></span> </span></span>',''),(281,NULL,'2021-03-11 00:30:52.799682','2021-03-11 00:34:59.567711',256,1,1,'_278','Аккумулятор повышенной мощности','','','',66,0,'','','','<span><span><span><span>Высокая скорость 18650 ячеек<br>Безопасный и надежный</span></span> </span></span>',''),(282,NULL,'2021-03-11 00:38:06.573786','2021-03-11 00:38:06.573807',52,1,1,'','Хорошо подобранная система EIC','Подробнее','/light_bee_motor.mp4','',67,0,'','','','<span><span>Система EIC разработана SURRON самостоятельно.</span> <span>После пяти тестовых поездок в провинции Сычуань и Тибет, а также постоянной обратной связи от лучших райдеров со всего мира, система EIC настроена на адаптацию к более сложным и суровым сценариям катания.</span></span>',''),(283,NULL,'2021-03-11 00:38:06.582088','2021-03-11 00:38:06.582108',254,1,1,'_282','Высокая производительность мотора','','','',67,0,'','','','<span><span><span><span>Максимальная частота вращения 5400 об / мин<br>Степень защиты IP55</span></span> </span></span>',''),(284,NULL,'2021-03-11 00:38:06.582867','2021-03-11 00:38:06.582882',255,1,1,'_282','FOC-контроллер синусоидальной волны','','','',67,0,'','','','<span><span><span><span>Составные алгоритмы с несколькими кривыми<br> Полная структура инкапсуляции</span></span> </span></span>',''),(285,NULL,'2021-03-11 00:38:06.586417','2021-03-11 00:38:06.586437',256,1,1,'_282','Аккумулятор повышенной мощности','','','',67,0,'','','','<span><span><span><span>Высокая скорость 18650 ячеек<br>Безопасный и надежный</span></span> </span></span>',''),(288,'light-bee-six-bg1.jpg','2021-03-13 10:15:26.044307','2021-03-13 10:17:40.832082',257,1,1,'','slide1','','','',68,0,'','','','',''),(289,'light-bee-six-bg2.jpg','2021-03-13 10:15:53.257236','2021-03-13 10:17:44.939321',258,1,1,'','slide2','','','',68,0,'','','','',''),(290,'light-bee-six-bg3.jpg','2021-03-13 10:16:12.759457','2021-03-13 10:17:49.439023',259,1,1,'','slide3','','','',68,0,'','','','',''),(291,'light-bee-six-bg4.jpg','2021-03-13 10:16:24.904907','2021-03-13 10:17:53.073170',260,1,1,'','slide4','','','',68,0,'','','','',''),(292,'light-bee-six-bg5.jpg','2021-03-13 10:16:35.332139','2021-03-13 10:17:56.886091',261,1,1,'','slide5','','','',68,0,'','','','',''),(293,'light-bee-six-bg6.jpg','2021-03-13 10:16:48.449049','2021-03-13 10:18:00.913505',262,1,1,'','slide6','','','',68,0,'','','','',''),(294,NULL,'2021-03-13 10:18:04.927540','2021-03-13 10:19:09.757320',263,1,1,'','Light Bee - ваше движение по бездорожью','','','',68,0,'','','','<span><span>Будь то горные тропы, снежный лес, профессиональные соревнования или уличные переулки, пчела Light может адаптироваться к любым дорожным условиям, а также продемонстрировать свое уникальное отношение и способность заряжаться в любое время и в любом месте.</span><span></span></span>',''),(301,NULL,'2021-03-13 11:36:04.119980','2021-03-13 11:38:02.380059',263,1,1,'','Легкая управляемость','','','',69,0,'','','','<span><span>Дрифтинг, перегорание шин и прыжки - все эти навыки можно легко освоить после катания на Light Bee.</span> <span>Его можно использовать для первого обучения новичкам, соревнований среди друзей, взаимодействия родителей и детей и профессионального обучения.</span> <span>Каждый может получить удовольствие от катания на Light Bee.</span> <span>Верхом на <span>Light Bee.</span></span></span>',''),(302,'light-bee-seven-bg1.jpg','2021-03-13 11:38:15.881592','2021-03-13 11:38:34.521551',264,1,1,'','slide1','','','',69,0,'','','','',''),(303,'light-bee-seven-bg2.jpg','2021-03-13 11:38:49.960115','2021-03-13 11:38:52.406566',265,1,1,'','slide2','','','',69,0,'','','','',''),(304,'light-bee-seven-bg3.jpg','2021-03-13 11:39:04.147470','2021-03-13 11:39:06.095319',266,1,1,'','slide3','','','',69,0,'','','','',''),(305,'light-bee-seven-bg4.jpg','2021-03-13 11:39:16.307629','2021-03-13 11:39:19.291952',267,1,1,'','slide4','','','',69,0,'','','','',''),(306,'light-bee-seven-bg5.jpg','2021-03-13 11:39:32.689261','2021-03-13 11:39:36.236928',268,1,1,'','slide5','','','',69,0,'','','','',''),(307,'light-bee-seven-bg6.jpg','2021-03-13 11:39:47.896071','2021-03-13 11:39:50.161393',269,1,1,'','slide6','','','',69,0,'','','','',''),(308,'light-bee-six-bg1.jpg','2021-03-13 11:41:25.635681','2021-03-13 11:41:25.635702',257,1,1,'','slide1','','','',70,0,'','','','',''),(309,'light-bee-six-bg2.jpg','2021-03-13 11:41:25.639278','2021-03-13 11:41:25.639296',258,1,1,'','slide2','','','',70,0,'','','','',''),(310,'light-bee-six-bg3.jpg','2021-03-13 11:41:25.646352','2021-03-13 11:41:25.646371',259,1,1,'','slide3','','','',70,0,'','','','',''),(311,'light-bee-six-bg4.jpg','2021-03-13 11:41:25.653617','2021-03-13 11:41:25.653639',260,1,1,'','slide4','','','',70,0,'','','','',''),(312,'light-bee-six-bg5.jpg','2021-03-13 11:41:25.666534','2021-03-13 11:41:25.666571',261,1,1,'','slide5','','','',70,0,'','','','',''),(313,'light-bee-six-bg6.jpg','2021-03-13 11:41:25.674685','2021-03-13 11:41:25.674713',262,1,1,'','slide6','','','',70,0,'','','','',''),(314,NULL,'2021-03-13 11:41:25.682246','2021-03-13 11:41:25.682273',263,1,1,'','Light Bee - ваше движение по бездорожью','','','',70,0,'','','','<span><span>Будь то горные тропы, снежный лес, профессиональные соревнования или уличные переулки, пчела Light может адаптироваться к любым дорожным условиям, а также продемонстрировать свое уникальное отношение и способность заряжаться в любое время и в любом месте.</span><span></span></span>',''),(315,NULL,'2021-03-13 11:41:43.962590','2021-03-13 11:41:43.962615',263,1,1,'','Легкая управляемость','','','',71,0,'','','','<span><span>Дрифтинг, перегорание шин и прыжки - все эти навыки можно легко освоить после катания на Light Bee.</span> <span>Его можно использовать для первого обучения новичкам, соревнований среди друзей, взаимодействия родителей и детей и профессионального обучения.</span> <span>Каждый может получить удовольствие от катания на Light Bee.</span> <span>Верхом на <span>Light Bee.</span></span></span>',''),(316,'light-bee-seven-bg1.jpg','2021-03-13 11:41:43.964394','2021-03-13 11:41:43.964412',264,1,1,'','slide1','','','',71,0,'','','','',''),(317,'light-bee-seven-bg2.jpg','2021-03-13 11:41:43.967989','2021-03-13 11:41:43.968007',265,1,1,'','slide2','','','',71,0,'','','','',''),(318,'light-bee-seven-bg3.jpg','2021-03-13 11:41:43.975281','2021-03-13 11:41:43.975306',266,1,1,'','slide3','','','',71,0,'','','','',''),(319,'light-bee-seven-bg4.jpg','2021-03-13 11:41:43.983226','2021-03-13 11:41:43.983252',267,1,1,'','slide4','','','',71,0,'','','','',''),(320,'light-bee-seven-bg5.jpg','2021-03-13 11:41:43.991253','2021-03-13 11:41:43.991280',268,1,1,'','slide5','','','',71,0,'','','','',''),(321,'light-bee-seven-bg6.jpg','2021-03-13 11:41:43.998820','2021-03-13 11:41:43.998842',269,1,1,'','slide6','','','',71,0,'','','','',''),(322,NULL,'2021-03-14 16:35:52.769355','2021-03-14 16:35:58.117179',1,1,4,'','Главная','','/','',3,0,'','','','',''),(323,NULL,'2021-03-14 18:41:44.190041','2021-03-14 18:55:44.184234',81,1,1,'','Light Bee S','','#advantagespage','advantagespage',72,0,'','','','',''),(329,NULL,'2021-03-14 18:50:28.631714','2021-03-14 18:50:28.631739',239,1,1,'','Без названия',NULL,NULL,NULL,73,0,NULL,NULL,NULL,NULL,NULL),(330,NULL,'2021-03-14 18:51:53.245481','2021-03-14 18:53:18.845507',52,1,1,'','40 кг','Подробнее','#about','',74,0,'','','','<span><span>чрезвычайно легкий дизай<br></span></span>',''),(331,NULL,'2021-03-14 18:51:53.253440','2021-03-14 18:54:04.803451',248,1,1,'','4 ч','','','',74,0,'','','','<span><span>быстрая зарядка в дороге</span></span>',''),(332,NULL,'2021-03-14 18:51:53.254663','2021-03-14 18:51:53.254683',249,1,1,'','250 N.M','','','',74,0,'','','','Максимальный крутящий момент\r\nПод углом более 45 градусов',''),(333,NULL,'2021-03-14 18:51:53.255485','2021-03-14 18:54:39.130150',250,1,1,'','Заказать','','','',74,0,'','','','',''),(334,NULL,'2021-03-15 10:44:28.928361','2021-03-15 10:58:37.664764',251,1,1,'','Сила и компактность','Подробнее','','light_bee_s/49',75,0,'','','','<span><span>Система питания разработана по </span><span>версии Light Bee X Super<br>Ллегко</span><span>весные части оборудованы</span><span> специально разработанной одинарной короно</span><span>вилкой, 17 дюймов спереди и сзади<br></span><span> Колесо - ведущая звездочка 58T д</span><span>елает Light Bee еще более компактным, но </span><span>мощным</span></span>',''),(335,NULL,'2021-03-15 11:16:57.931630','2021-03-15 11:21:02.810798',52,1,1,'','Специально разработанная перевернутая вилка Single Crown','Подробнее','/light_bee_s_1.mp4','',76,0,'','','','<span><span>Предназначен специально для Light Bee S, длина 550 мм, с эффективным ходом 150 мм, регулируемый, </span><span>благодаря настройке отскока Light Bee S подходит для большинства дорожных условий.</span> <span>это делает движение комфортным</span><span>, независимо от того, едете вы по асфальту или грунтовой дороге.</span></span>',''),(336,NULL,'2021-03-15 11:21:17.889799','2021-03-15 11:23:09.290360',270,1,1,'','360° просмотр','','#spinner360','spinner360',72,0,'','','','',''),(337,NULL,'2021-03-15 11:23:39.990988','2021-03-15 11:23:51.644493',271,1,1,'','Система подвески','','#videopage','videopage',72,0,'','','','',''),(338,NULL,'2021-03-15 11:25:46.637498','2021-03-15 11:30:33.647865',52,1,1,'','Система задней подвески Intersect TR, разработанная Sur-ron','Подробнее','/light_bee_s_2.mp4','',77,0,'','','','<span><span>Проведя несколько масштабных городских гонок, получены гоночные данные, которые были учтены</span><span> нашими инженерами и была разработана специальная многорычажная задняя подвеска. Э</span><span>та система имеет форму, соответствующую раме, и уникальную настройку только для Light Bee S. Мы в</span><span>сегда на высоте.</span></span>',''),(342,NULL,'2021-03-15 11:32:51.427060','2021-03-15 11:32:58.860228',272,1,1,'','Задняя подвеска','','#videopage2','videopage2',72,0,'','','','',''),(347,NULL,'2021-03-15 11:41:35.632763','2021-03-15 11:44:57.087803',52,1,1,'','Наслаждайтесь поездкой','Подробнее','','',79,0,'','','','<span><span>Система EIC разработана SURRON самостоятельно.</span> <span>После пяти тестовых поездок в провинции Сычуань и Тибет, а также постоянной обратной связи от лучших райдеров со всего мира, система EIC настроена на адаптацию к более сложным и суровым сценариям катания.</span></span>',''),(348,NULL,'2021-03-15 11:41:35.634491','2021-03-15 11:42:43.686874',254,1,1,'_347','1250 мм','','','',79,0,'','','','<span><span><span><span><span>Ультракороткая колесная база<br>Легкий и быстрый</span> </span></span> </span></span>',''),(349,NULL,'2021-03-15 11:41:35.635390','2021-03-15 11:42:51.394733',255,1,1,'_347','220 мм','','','',79,0,'','','','<span>Дорожный просвет<br>Проблемы не достанут до вас</span>',''),(350,NULL,'2021-03-15 11:41:35.636491','2021-03-15 11:42:58.648965',256,1,1,'_347','58 T','','','',79,0,'','','','<span><span><span><span><span>Большая звездочка<br>Еще больший крутящий момент</span> </span></span> </span></span>',''),(351,NULL,'2021-03-15 11:46:27.236162','2021-03-15 11:46:27.236186',52,1,1,'','Наслаждайтесь поездкой','Подробнее','','',78,0,'','','','<span><span>Система EIC разработана SURRON самостоятельно.</span> <span>После пяти тестовых поездок в провинции Сычуань и Тибет, а также постоянной обратной связи от лучших райдеров со всего мира, система EIC настроена на адаптацию к более сложным и суровым сценариям катания.</span></span>',''),(352,NULL,'2021-03-15 11:46:27.249042','2021-03-15 11:46:27.249063',254,1,1,'_351','1250 мм','','','',78,0,'','','','<span><span><span><span><span>Ультракороткая колесная база<br>Легкий и быстрый</span> </span></span> </span></span>',''),(353,NULL,'2021-03-15 11:46:27.254580','2021-03-15 11:46:27.254601',255,1,1,'_351','220 мм','','','',78,0,'','','','<span>Дорожный просвет<br>Проблемы не достанут до вас</span>',''),(354,NULL,'2021-03-15 11:46:27.255489','2021-03-15 11:46:27.255510',256,1,1,'_351','58 T','','','',78,0,'','','','<span><span><span><span><span>Большая звездочка<br>Еще больший крутящий момент</span> </span></span> </span></span>',''),(355,NULL,'2021-03-15 12:04:22.361015','2021-03-15 12:04:50.514624',273,1,1,'','Опыт езды','','#imagepage2','imagepage2',72,0,'','','','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
INSERT INTO `flatcontent_containers` VALUES (1,NULL,'2021-02-26 15:44:11.676667','2021-02-26 15:44:11.676704',1,1,2,NULL,'Контент для всех страничек','Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики','main',NULL,NULL),(2,NULL,'2021-02-26 15:44:11.737535','2021-02-26 15:44:11.737561',2,1,1,NULL,'Главное меню','Создано автоматически, выводит главное меню','mainmenu',NULL,NULL),(3,NULL,'2021-02-26 15:44:11.740051','2021-02-26 17:23:22.528148',3,1,1,'','Мобильное меню','','mobilemenu','',''),(4,NULL,'2021-02-26 16:57:11.045760','2021-02-28 13:56:14.488095',4,0,1,'','Слайдер меню','','slidermenu','',''),(5,NULL,'2021-02-26 17:49:38.093154','2021-02-26 17:52:22.183578',1,1,99,'','Контейнер homepage','Light Bee<br>','homepage','',''),(6,NULL,'2021-02-26 18:05:09.778302','2021-03-10 11:42:38.659011',6,1,3,'','Главный экран','Light Bee<br>','homepage','',''),(7,NULL,'2021-02-26 18:05:54.333699','2021-02-27 11:08:08.034700',7,1,1,'','Главная страничка','','','',''),(8,NULL,'2021-02-26 18:13:47.769575','2021-02-26 18:13:58.588017',2,1,99,'','Контейнер aboutpage','О нас<br>','aboutpage','',''),(9,NULL,'2021-02-26 18:30:12.754771','2021-02-26 18:30:12.760885',9,1,3,'','О нас','О нас<br>','aboutpage','',''),(10,NULL,'2021-02-26 18:37:35.171155','2021-02-27 12:14:52.353020',3,1,99,'','Контейнер carouselpage','Наши предложения<br>','carouselpage','',''),(11,NULL,'2021-02-26 19:06:51.953027','2021-02-26 19:08:59.396658',11,1,3,'','Слайдер','Наши предложения<br>','carouselpage','',''),(12,NULL,'2021-02-26 19:09:21.624339','2021-02-26 19:09:25.486065',4,1,99,'','Контейнер sliderpage','','sliderpage','',''),(13,NULL,'2021-02-27 10:44:26.671535','2021-02-27 10:44:26.671553',13,1,3,'','Слайдер байков','','sliderpage','',''),(14,NULL,'2021-02-27 10:49:32.453725','2021-02-27 10:49:50.304720',6,1,99,'','Контейнер twoblockspage','Предложения<br>','twoblockspage','',''),(15,NULL,'2021-02-27 11:07:39.933605','2021-02-27 11:07:39.939843',15,1,3,'','Два блока с мопедами','Предложения<br>','twoblockspage','',''),(16,NULL,'2021-02-27 11:10:17.349748','2021-02-27 11:10:30.857417',7,1,99,'','Контейнер twonewspage','Предложения<br>','twonewspage','',''),(17,NULL,'2021-02-27 11:41:52.325657','2021-02-27 11:41:57.044213',16,1,3,'','Два блока с мопедами (альт)','Предложения<br>','twonewspage','',''),(18,NULL,'2021-02-27 11:46:28.862859','2021-02-27 11:46:38.915483',8,1,99,'','Контейнер threeblockspage','Предложения<br>','threeblockspage','',''),(19,NULL,'2021-02-27 12:13:38.912026','2021-02-27 12:13:38.916382',17,1,3,'','Наши товары','Предложения<br>','threeblockspage','',''),(20,NULL,'2021-02-27 12:35:52.340531','2021-02-27 12:36:39.311753',9,1,99,'','Подписаться на новости','Подпишись на новости<br>','subscribepage','',''),(21,NULL,'2021-02-27 12:37:21.425674','2021-02-27 12:37:21.435323',19,1,3,'','Подписаться на новости','Подпишись на новости<br>','subscribepage','',''),(22,NULL,'2021-02-27 12:46:53.349079','2021-02-27 12:54:39.743922',10,1,99,'','Тарифный план','Тарифный план<br>','priceplanpage','',''),(23,NULL,'2021-02-27 13:02:17.183570','2021-02-27 13:02:17.231021',21,1,3,'','Тарифный план','Тарифный план<br>','priceplanpage','',''),(24,NULL,'2021-02-27 13:07:51.883380','2021-02-27 13:07:58.614493',11,1,99,'','Контакты','Написать нам<br>','contactspage','',''),(25,NULL,'2021-02-27 13:09:37.855025','2021-02-27 13:09:37.862961',23,1,3,'','Контакты','Написать нам<br>','contactspage','',''),(26,NULL,'2021-02-28 13:13:35.284889','2021-02-28 13:28:06.670508',12,1,99,'','Видео фон странички','','video_bg','',''),(27,NULL,'2021-02-28 13:17:44.961524','2021-02-28 13:17:44.961543',25,1,3,'','Демонстрационный фон с видео','','video_bg','',''),(28,NULL,'2021-02-28 13:57:49.008992','2021-02-28 13:57:49.009011',13,1,99,'','Слайдер-меню для странички','','slider_menu','',''),(29,NULL,'2021-02-28 14:03:52.961709','2021-02-28 14:03:58.842375',27,1,3,'','Слайдер-меню для главной странички','','slider_menu','',''),(30,NULL,'2021-03-03 21:36:56.560311','2021-03-03 21:36:56.560337',28,1,7,NULL,'Каталог товаров',NULL,'catalogue',NULL,NULL),(31,NULL,'2021-03-03 21:42:12.862438','2021-03-03 21:42:12.862462',29,1,4,NULL,'Сео-тексты для товаров/услуг',NULL,'seo_for_products',NULL,NULL),(32,NULL,'2021-03-03 22:40:19.792696','2021-03-03 22:40:19.792732',14,1,99,NULL,'О нас','О компании<br>','about',NULL,NULL),(33,NULL,'2021-03-03 22:40:19.821849','2021-03-03 22:40:19.821878',15,1,99,NULL,'Простая статья','Приватность','article',NULL,NULL),(34,NULL,'2021-03-03 22:40:19.876828','2021-03-03 22:40:19.876863',16,1,99,NULL,'Статья (Вариант 2)',NULL,'article2',NULL,NULL),(35,NULL,'2021-03-03 22:40:20.053512','2021-03-03 22:40:20.053536',17,1,99,NULL,'Статья - Темный фон','Добро пожаловать','article_dark',NULL,NULL),(36,'surron.png','2021-03-03 22:40:20.093785','2021-03-03 22:40:20.093815',18,1,99,NULL,'Заголовок',NULL,'call_to_action',NULL,NULL),(37,NULL,'2021-03-03 22:40:20.153517','2021-03-03 22:40:20.153543',19,1,99,NULL,'Каталог',NULL,'catalogue',NULL,NULL),(38,NULL,'2021-03-03 22:40:20.171349','2021-03-03 22:40:20.171375',20,1,99,NULL,'Контакты','Контакты<br>','contacts',NULL,NULL),(39,NULL,'2021-03-03 22:40:20.236333','2021-03-03 22:40:20.236358',21,1,99,NULL,'Дилеры','Дилеры<br>','dealers',NULL,NULL),(40,NULL,'2021-03-03 22:40:20.263728','2021-03-03 22:40:20.263751',22,1,99,NULL,'Написать  нам','Стать дилером','feedback',NULL,NULL),(41,NULL,'2021-03-03 22:40:20.292610','2021-03-03 23:29:35.451703',23,1,99,'','Товары','Наши предложения<br>','products','',''),(42,NULL,'2021-03-03 22:40:20.304111','2021-03-03 22:40:20.304136',24,1,99,NULL,'Слайдер',NULL,'slider',NULL,NULL),(43,NULL,'2021-03-03 22:40:20.385915','2021-03-03 22:40:20.385939',25,1,99,NULL,'Видео','Обзоры техники','videos',NULL,NULL),(44,NULL,'2021-03-03 22:47:36.716266','2021-03-03 22:48:35.255452',42,1,3,'','Видео на Электро Байк SUR-RON X Light bee','Обзоры техники','videos','',''),(45,NULL,'2021-03-03 23:35:55.833565','2021-03-03 23:35:55.833582',43,1,3,'','Каталог','','catalogue','',''),(46,'big1.jpg','2021-03-06 11:55:21.838461','2021-03-06 11:59:42.109231',26,1,99,'','Фоновое изображение','','img_bg','',''),(48,'phone-index-one.jpg','2021-03-06 12:02:02.547213','2021-03-06 12:02:05.928540',45,1,3,'','Фонове изображение для главной странички (мобильная версия)','','img_bg','',''),(49,NULL,'2021-03-08 13:16:11.286754','2021-03-08 13:19:16.359110',46,1,1,'','Информация','','bottommenu','',''),(50,NULL,'2021-03-10 11:49:28.092353','2021-03-10 11:49:38.908816',5,1,99,'','Контейнер imagepage','','imagepage','',''),(51,NULL,'2021-03-10 11:55:06.066754','2021-03-10 11:55:06.066772',47,1,3,'','Storm Bee картинка на главной','','imagepage','',''),(52,NULL,'2021-03-10 12:01:10.169196','2021-03-10 12:01:39.905404',27,1,99,'','События','События<br>','newspage','',''),(53,NULL,'2021-03-10 14:50:45.574507','2021-03-10 14:50:45.599687',49,1,3,'','Новости (события) на главной страничке','События<br>','newspage','',''),(54,'light-bee-one-bg.jpg','2021-03-10 15:52:49.475118','2021-03-10 16:29:41.339572',28,1,99,'','Контейнер advantagespages','Light Bee<br>','advantagespage','',''),(56,'light-bee-one-bg.jpg','2021-03-10 16:43:33.428659','2021-03-10 16:43:33.443967',50,1,3,'','Light Bee Преимущества','Light Bee<br>','advantagespage','',''),(57,'light-bee-one-bg.jpg','2021-03-10 16:57:53.393428','2021-03-10 16:57:56.843156',51,1,3,'','Light Bee фоновое изображение','','img_bg','',''),(58,NULL,'2021-03-10 17:25:26.106114','2021-03-10 17:25:26.106138',52,1,99,'','360 градусов','','spinner360','',''),(59,NULL,'2021-03-10 19:04:27.431960','2021-03-10 19:04:31.849346',53,1,3,'','3d  вид Light Bee (spinner 360)','','spinner360','',''),(60,NULL,'2021-03-10 22:48:10.168642','2021-03-10 22:48:10.168666',54,1,3,'','Light Bee слайдер меню','','slider_menu','',''),(61,NULL,'2021-03-10 23:07:26.890770','2021-03-10 23:07:35.404725',55,1,99,'','Контейнер videopage','Light Bee<br>','videopage','',''),(62,NULL,'2021-03-10 23:44:55.852257','2021-03-11 00:38:37.084766',56,1,3,'','Light Bee Видео 1 - 2 видео','Light Bee<br>','videopage','',''),(64,NULL,'2021-03-11 00:22:43.882252','2021-03-11 00:22:48.476001',58,1,99,'','Контейнер videopage2','Light Bee<br>','videopage2','',''),(65,NULL,'2021-03-11 00:25:31.324712','2021-03-11 00:38:22.527098',59,1,3,'','Light Bee Видео 2 - лес','Light Bee<br>','videopage2','',''),(66,NULL,'2021-03-11 00:30:52.754033','2021-03-11 00:30:58.088374',60,1,99,'','Контейнер videopage3','Light Bee<br>','videopage3','',''),(67,NULL,'2021-03-11 00:38:06.554594','2021-03-11 00:38:06.568205',61,1,3,'','Light Bee Видео 3 - Мотор','Light Bee<br>','videopage3','',''),(68,NULL,'2021-03-13 10:14:24.179766','2021-03-13 10:14:26.899602',62,1,99,'','Контейнер sliderpage2','','sliderpage2','',''),(69,NULL,'2021-03-13 11:36:04.035062','2021-03-13 11:36:14.481424',63,1,99,'','Контейнер sliderpage3','','sliderpage3','',''),(70,NULL,'2021-03-13 11:41:18.187491','2021-03-13 11:41:25.626317',64,1,3,'','Light Bee slider 1','','sliderpage2','',''),(71,NULL,'2021-03-13 11:41:43.953338','2021-03-13 11:41:43.953356',65,1,3,'','Light Bee slider2','','sliderpage3','',''),(72,NULL,'2021-03-14 18:41:44.170472','2021-03-14 18:41:44.170497',66,1,3,'','Слайдер меню для Light Bee S','','slider_menu','',''),(73,'big1.jpg','2021-03-14 18:50:28.587652','2021-03-14 18:50:28.604181',67,1,3,'','Light Bee S - Фоновое изображение','','img_bg','',''),(74,'light-bee-one-bg.jpg','2021-03-14 18:51:53.197619','2021-03-14 18:51:53.209928',68,1,3,'','Light Bee S Преимущества','Light Bee<br>','advantagespage','',''),(75,NULL,'2021-03-15 10:44:28.895492','2021-03-15 10:44:28.895516',69,1,3,'','Light Bee S 360 градусов spinner','','spinner360','',''),(76,NULL,'2021-03-15 11:16:57.916828','2021-03-15 11:26:04.266849',70,1,3,'','Light Bee S видео 1','Light Bee S<br>','videopage','',''),(77,NULL,'2021-03-15 11:25:46.593893','2021-03-15 11:25:53.730821',71,1,3,'','Light Bee S видео 2','Light Bee S<br>','videopage2','',''),(78,'79.jpg','2021-03-15 11:34:05.855145','2021-03-15 11:46:27.226200',72,1,3,'','Light Bee S - Видео 3','Light Bee S<br>','imagepage2','',''),(79,'79.jpg','2021-03-15 11:41:35.599100','2021-03-15 11:41:48.792428',73,1,99,'','Контейнер imagepage2','Light Bee S<br>','imagepage2','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=221 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_linkcontainer`
--

LOCK TABLES `flatcontent_linkcontainer` WRITE;
/*!40000 ALTER TABLE `flatcontent_linkcontainer` DISABLE KEYS */;
INSERT INTO `flatcontent_linkcontainer` VALUES (79,NULL,'2021-03-03 22:48:50.305459','2021-03-03 22:48:50.305480',0,1,NULL,NULL,136,44),(80,NULL,'2021-03-03 23:36:06.900467','2021-03-03 23:36:06.900487',14,1,NULL,NULL,52,45),(81,NULL,'2021-03-05 19:11:22.108401','2021-03-05 19:11:22.108423',15,1,NULL,NULL,206,44),(125,NULL,'2021-03-10 14:51:57.701334','2021-03-10 14:51:57.701357',16,1,NULL,NULL,55,29),(126,NULL,'2021-03-10 14:51:57.710014','2021-03-10 14:51:57.710035',17,1,NULL,NULL,55,48),(127,NULL,'2021-03-10 14:51:57.716267','2021-03-10 14:51:57.716286',18,1,NULL,NULL,55,27),(128,NULL,'2021-03-10 14:51:57.718278','2021-03-10 14:51:57.718298',19,1,NULL,NULL,55,6),(129,NULL,'2021-03-10 14:51:57.720197','2021-03-10 14:51:57.720216',20,1,NULL,NULL,55,51),(130,NULL,'2021-03-10 14:51:57.721456','2021-03-10 14:51:57.721476',21,1,NULL,NULL,55,53),(176,NULL,'2021-03-13 11:41:58.526681','2021-03-13 11:41:58.526702',22,1,NULL,NULL,16,60),(177,NULL,'2021-03-13 11:41:58.528172','2021-03-13 11:41:58.528196',23,1,NULL,NULL,16,57),(178,NULL,'2021-03-13 11:41:58.529610','2021-03-13 11:41:58.529631',24,1,NULL,NULL,16,56),(179,NULL,'2021-03-13 11:41:58.530916','2021-03-13 11:41:58.530935',25,1,NULL,NULL,16,59),(180,NULL,'2021-03-13 11:41:58.532283','2021-03-13 11:41:58.532304',26,1,NULL,NULL,16,62),(181,NULL,'2021-03-13 11:41:58.533657','2021-03-13 11:41:58.533676',27,1,NULL,NULL,16,65),(182,NULL,'2021-03-13 11:41:58.535078','2021-03-13 11:41:58.535099',28,1,NULL,NULL,16,67),(183,NULL,'2021-03-13 11:41:58.536493','2021-03-13 11:41:58.536513',29,1,NULL,NULL,16,70),(184,NULL,'2021-03-13 11:41:58.537887','2021-03-13 11:41:58.537918',30,1,NULL,NULL,16,71),(214,NULL,'2021-03-15 11:40:20.318437','2021-03-15 11:40:20.318460',31,1,NULL,NULL,33,72),(215,NULL,'2021-03-15 11:40:20.319832','2021-03-15 11:40:20.319854',32,1,NULL,NULL,33,73),(216,NULL,'2021-03-15 11:40:20.321100','2021-03-15 11:40:20.321118',33,1,NULL,NULL,33,74),(217,NULL,'2021-03-15 11:40:20.322447','2021-03-15 11:40:20.322467',34,1,NULL,NULL,33,75),(218,NULL,'2021-03-15 11:40:20.323691','2021-03-15 11:40:20.323707',35,1,NULL,NULL,33,76),(219,NULL,'2021-03-15 11:40:20.324811','2021-03-15 11:40:20.324827',36,1,NULL,NULL,33,77),(220,NULL,'2021-03-15 11:40:20.326046','2021-03-15 11:40:20.326063',37,1,NULL,NULL,33,78);
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
INSERT INTO `login_customuser` VALUES (1,NULL,'2021-02-26 15:26:44.385523','2021-03-12 23:01:56.251145',1,1,NULL,NULL,NULL,NULL,1),(2,NULL,'2021-02-27 13:12:47.424656','2021-02-27 13:13:05.379194',2,1,NULL,NULL,'','',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personal_shopper`
--

LOCK TABLES `personal_shopper` WRITE;
/*!40000 ALTER TABLE `personal_shopper` DISABLE KEYS */;
INSERT INTO `personal_shopper` VALUES (1,NULL,'2021-03-03 23:50:00.941297','2021-03-03 23:50:00.941325',1,1,NULL,NULL,'Гость','Den','Kramorov',NULL,'dk@223-223.ru','8(914)8 959-223',NULL,NULL,NULL,NULL,NULL,NULL,'127.0.0.1');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_products`
--

LOCK TABLES `products_products` WRITE;
/*!40000 ALTER TABLE `products_products` DISABLE KEYS */;
INSERT INTO `products_products` VALUES (1,'6581f90b4468daf1173f8ce287f1e930.jpg','2021-03-03 21:42:12.830449','2021-03-05 19:11:34.383090',1,1,NULL,'','Электро Байк SUR-RON X Light bee','','','',NULL,290000.00,245000.00,'','Версия X создана для бездорожья, пересечённой местности, кроссовых трасс.<br>Многорычажная подвеска байка справляется с любыми неровностями.<br>Внедорожная резина даёт максимальное сцепление с грязью, песком, камнями<br>Контроллер настроен на максимальные обороты двигателя 5400 об/мин<br>','<h4>Аккумулятор (съемный)</h4>\r\nРеволюционные технологии. Максимально достижимая емкость батареи. Улучшенный жизненный цикл<br><br>\r\n<ul>\r\n <li>Минимальное время зарядки.</li>\r\n <li>Съемный аккумулятор</li>\r\n <li>Ёмкость батареи 32Ah</li>\r\n <li>Рабочее напряжение 60V</li>\r\n <li>Вес батареи 11 кг</li>\r\n <li>Запас хода до 100 км</li>\r\n <li>Время зарядки 3-4 часа</li>\r\n <li>18650 аккумуляторных элементов</li>\r\n <li>4 датчика температуры в режиме реального времени</li>\r\n <li>Дисплей для отслеживания заряда аккумулятора<br><br></li>\r\n</ul><h4>\r\n\r\nДВИГАТЕЛЬ SUR-RON Оптимальное соотношение мощности</h4>\r\nДвигатель Sur-Ron имеет максимально высокое соотношение мощности , благодаря чему легко разгоняется до скорости 80 километров в час, оставляя всех конкурентов позади\r\n<br><br>\r\nВысокопроизводительный бесщеточный двигатель с постоянными магнитами, технологии Nine Dragons специально разработан для SUR-RON X, с эффективной функцией электронного тормоза IP55 защитой от влаги, высококачественный материал , выдерживает высокие температуры до 180 ° C, максимальный крутящий момент до 32 N.m\r\n<br><br>\r\n<ul>\r\n <li>Высокопроизводительный двигатель</li>\r\n <li>Мощность двигателя 5400 W</li>\r\n <li>Крутящий момент двигателя 32 Nm</li>\r\n <li>0-80 Км/ч за 6,02 сек</li>\r\n <li>Байк может подняться в гору с углом более 50 градусов</li>\r\n <li>Степень защиты от воды IP55</li>\r\n <li>Активная система торможения двигателем</li>\r\n <li>Рекуперация функция подзаряда батареи двигателем на холостом ходу<br></li>\r\n</ul>\r\n<h4>КОНТРОЛЛЕР SINE-WAVE X</h4>\r\nИнтеллектуальный векторный контроллер FOC обеспечит максимально ровную мощность во всем рабочем диапазоне оборотов двигателя.<br><br>\r\nFOC-контроллер оптимизирует мощность и ресурс использования заряда с максимальной точностью.<br>\r\n На 30% меньше шума по сравнению со стандартными контроллерами. На 25% увеличена мощность крутящего момента. Более плавный отклик газа.<br><br>\r\nКомпания Nine Dragons Technology самостоятельно разрабатывала программу которая отслеживает степень поворота, скорость, крутящий момент и интенсивность тока в режиме реального времени и будет постоянно анализировать и изучать ваши ежедневные данные о вождении, чтобы соответствовать вашим привычкам вождения<br><br>\r\n<h4>Тормозная система</h4>\r\n<ul>\r\n <li>Высокопроизводительная тормозная система Shimano</li>\r\n <li>Четырех поршневая гидравлическая дисковая тормозная система, стабильная и надежная</li>\r\n <li>Все металлические тормозные колодки долговечны и имеют низкую теплопроводность</li>\r\n <li>Отличается высокой мощностью торможения и увеличенной долговечностью</li>\r\n <li>Надежная конструкция, обеспечивающая превосходные показатели торможения при катании в самых разных стилях</li>\r\n <li>Прочный главный цилиндр обтекаемой формы</li>\r\n <li>4-поршневый калипер для уверенности на сложных трассах и удовольствия от катания</li>\r\n <li>Теплоизолированные поршни для стабильного торможения и сокращения износа колодок</li>\r\n <li>Односторонняя подача масла в калипер и прокачка с воронкой для быстрого и удобного обслуживания тормозной гидролинии</li>\r\n</ul>','1',NULL,245000.00,245000.00,NULL,NULL),(2,'0db2263fc44a165f15574b39f2448f41.jpg','2021-03-05 09:31:28.764496','2021-03-05 19:11:22.090782',2,1,NULL,'','Электро Байк SUR-RON S Light bee','','','',NULL,245000.00,220000.00,'','Молодежная версия байка Sur-Ron Light bee<br>Младшая модель в линейке, для возраста от 10-ти лет и выше <br>Защита цепи, 17 колеса, переднее крыло, гидравлические тормоза SHIMANO.<br>Подвеска, резина, двигатель и все остальные узлы, как у модели X<br>','<h4>Батарея Panasonic Li 48V/20A</h4>\r\nРеволюционные технологии. Максимально достижимая емкость батареи. Улучшенный жизненный цикл<br><br>\r\n<ul>\r\n <li>Минимальное время зарядки</li>\r\n <li>Съемный аккумулятор</li>\r\n <li>Ёмкость батареи 20Ah</li>\r\n <li>Рабочее напряжение 48V</li>\r\n <li>Вес батареи 11 кг</li>\r\n <li>Запас хода до 50 км</li>\r\n <li>Время зарядки 2-3&nbsp;часа</li>\r\n <li>18650 аккумуляторные элементы</li>\r\n <li>4 датчика температуры в режиме реального времени</li>\r\n <li>Дисплей для отслеживания заряда аккумулятора</li>\r\n</ul>\r\n<h4>ДВИГАТЕЛЬ SUR-RON Оптимальное соотношение мощности</h4>\r\nДвигатель Sur-Ron имеет максимально высокое соотношение мощности , благодаря чему легко разгоняется до скорости 80 километров в час, оставляя всех конкурентов позади\r\n<br><br>\r\nВысокопроизводительный бесщеточный двигатель с постоянными магнитами, технологии Nine Dragons специально разработан для SUR-RON X, с эффективной функцией электронного тормоза IP55 защитой от влаги, высококачественный материал , выдерживает высокие температуры до 180 ° C, максимальный крутящий момент до 32 N.m\r\n<br><br>\r\n<ul>\r\n <li>Высокопроизводительный двигатель</li>\r\n <li>Мощность двигателя 2900 W</li>\r\n <li>Крутящий момент двигателя 32 Nm</li>\r\n <li>0-50 Км/ч за 5,02 сек</li>\r\n <li>Байк может подняться в гору с углом более 40 градусов</li>\r\n <li>Степень защиты от воды IP55</li>\r\n <li>Активная система торможения двигателем</li>\r\n <li>Рекуперация функция подзаряда батареи двигателем на холостом ходу</li>\r\n</ul>\r\n<h4>КОНТРОЛЛЕР SINE-WAVE X</h4>\r\nИнтеллектуальный векторный контроллер FOC обеспечит максимально ровную мощность во всем рабочем диапазоне оборотов двигателя<br><br>\r\nFOC-контроллер оптимизирует мощность и ресурс использования заряда с максимальной точностью.<br>\r\n На 30% меньше шума по сравнению со стандартными контроллерами. На 25% увеличена мощность крутящего момента. Более плавный отклик газа<br><br>\r\nКомпания Nine Dragons Technology самостоятельно разрабатывала программу которая отслеживает степень поворота, скорость, крутящий момент и интенсивность тока в режиме реального времени и будет постоянно анализировать и изучать ваши ежедневные данные о вождении, чтобы соответствовать вашим привычкам вождения<br><br>\r\n<h4>Тормозная система</h4>\r\n<ul>\r\n <li>Высокопроизводительная тормозная система Shimano</li>\r\n <li>Четырех поршневая гидравлическая дисковая тормозная система, стабильная и надежная</li>\r\n <li>Все металлические тормозные колодки долговечны и имеют низкую теплопроводность</li>\r\n <li>Отличается высокой мощностью торможения и увеличенной долговечностью</li>\r\n <li>Надежная конструкция, обеспечивающая превосходные показатели торможения при катании в самых разных стилях</li>\r\n <li>Прочный главный цилиндр обтекаемой формы</li>\r\n <li>4-поршневый калипер для уверенности на сложных трассах и удовольствия от катания</li>\r\n <li>Теплоизолированные поршни для стабильного торможения и сокращения износа колодок</li>\r\n <li>Односторонняя подача масла в калипер и прокачка с воронкой для быстрого и удобного обслуживания тормозной гидролинии</li>\r\n</ul>','2',NULL,220000.00,220000.00,NULL,NULL),(4,'c054809af7e025bff9bc46a13c096340.jpg','2021-03-05 19:08:05.732410','2021-03-06 11:30:17.262915',3,1,NULL,'','SUR-RON Storm BEE Кросс','','','',NULL,680000.00,580000.00,'','Долгожданная премьера нового ЭлектроБайка от Китайской фабрики SUR-RON под громким названием <b>SUR-RON Storm Bee</b> намечена в России на осень 2020!<br>\r\n <br>\r\n Активно идут предзаказы на модель, готовится к отправке в Россию первая партия ЭлектроБайков SUR-RON Storm Bee.<br>\r\n <br>\r\n Официальный дилер, магазин&nbsp;<b>«I SUR-RON»</b>&nbsp;по прежнему предлагает своим покупателям два варианта покупки SUR-RON Storme Bee.<br>\r\n Вы можете <b>купить ЭлектроБайк SUR-RON Storm&nbsp;Bee</b> в наличии со склада в России по рыночной цене, а так же на этапе комплектации контейнера на фабрике в Китае по цене гораздо ниже и сэкономить при этом существенную сумму.<br>','Итак, что же мы знаем о ЭлектроБайке <b>SUR-RON Storm Bee Кросс</b>?!<br>\r\nУверенно можно сказать на данный момент что это самая ожидаемая премьера года 2020, множество предзаказов, долгое ожидание, все это говорит нам о том что Китайцы снова сделали нечто из ряда вон... <b>SUR-RON Storm Bee Кросс</b> станет хитом продаж сезона 2021 вне всякого сомнения.<br>\r\n <br>\r\n Данная версия SUR-RON Storm Bee Кросс не имеет фары головного света, зеркал, стоп-сигнала, поворотников и на порядок легче чем Эндуро версия Storm Bee.<br>\r\n Можно провести аналогию с моделями SUR-RON X и L1E (евро) в линейке ЭлектроБайков SUR-RON Light Bee, так что Кросс версия обещает быть более востребованной на рынке.<br>\r\n Версия выпускается в двух фирменных расцветках от фабрики SUR-RON Белый и Черный<br>','4',NULL,580000.00,580000.00,NULL,NULL),(5,'20693b411f33534e081dcf8976ebad41.jpg','2021-03-06 11:27:14.566148','2021-03-06 11:37:19.635478',4,1,NULL,'','SUR-RON Storm BEE Кросс','','','',NULL,710000.00,610000.00,'','ЭлектроБайк SUR-RON Storm Bee Эндуро версия, имеет светотехнику в виде LED фары головного света, поворотников, заднего стоп-сигнала, а так же зеркала для удобной езды на дорогах общего пользования, хоть и стихия данного электробайка суррон шторм по прежнему пересеченная местность, на нем можно комфортно доехать до места по дорогам общего пользования.<br><br>\r\n\r\nОфициальный дилер, магазин «I SUR-RON» по прежнему предлагает своим покупателям два варианта покупки SUR-RON Storme Bee Эндуро.<br>Вы можете купить ЭлектроБайк SUR-RON Storm Bee Эндуро в наличии со склада в России по рыночной цене, а так же на этапе комплектации контейнера на фабрике в Китае по цене гораздо ниже и сэкономить при этом существенную сумму.','Итак, что же мы знаем о ЭлектроБайке <b>SUR-RON Storm Bee Эндуро</b>?<br>\r\n Уверенно&nbsp;можно сказать на данный момент что это самая ожидаемая премьера года 2020, множество предзаказов, долгое ожидание, все это говорит нам о том что Китайцы снова сделали нечто из ряда вон... <b>SUR-RON Storm Bee Эндуро</b> станет хитом продаж сезона 2021 вне всякого сомнения.<br>\r\n <br>\r\n Данная Эндуро версия SUR-RON Storm Bee имеет фару головного света, зеркала, стоп-сигнал и поворотники, новейшую высокоэффективную систему электропитания Snapdragon, обладающую высокой мощностью, а также цельнометаллическую раму из алюминиевого сплава и литиевую аккумуляторную батарею с максимальной мощностью разряда 10C. Передняя и задняя подвеска имеет ход демпфирования 290 мм, а дорожная версия байка оснащена системой ABS.\r\n<p>\r\n Рама из авиационного алюминия, мощный контроллер. Sur-Ron Storm открывает новые возможности в классе полноразмерных мощных мотоциклов!\r\n</p>\r\n Эндуро версия выпускается в двух фирменных расцветках от фабрики SUR-RON Белый и Черный','5',NULL,610000.00,610000.00,NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productscats`
--

LOCK TABLES `products_productscats` WRITE;
/*!40000 ALTER TABLE `products_productscats` DISABLE KEYS */;
INSERT INTO `products_productscats` VALUES (23,NULL,1,41),(25,NULL,2,NULL),(32,NULL,4,NULL),(38,137,2,NULL),(39,137,1,NULL),(40,NULL,5,NULL),(46,137,4,NULL),(49,137,5,NULL),(50,53,1,5),(51,221,1,6),(54,246,1,54),(55,250,1,56),(56,252,1,58),(57,253,1,59),(58,261,1,61),(59,262,1,62),(61,270,1,64),(62,274,1,65),(63,278,1,66),(64,282,1,67),(65,294,1,68),(66,301,1,69),(67,314,1,70),(68,315,1,71),(70,333,2,74),(72,334,2,75),(74,335,2,76),(76,338,2,77),(79,347,2,79),(80,351,2,78);
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productsphotos`
--

LOCK TABLES `products_productsphotos` WRITE;
/*!40000 ALTER TABLE `products_productsphotos` DISABLE KEYS */;
INSERT INTO `products_productsphotos` VALUES (1,'ff1d617aaa4f2989e2947788cfba87e5.jpg','2021-03-03 22:37:38.489107','2021-03-03 22:46:26.322489',1,1,NULL,NULL,'6',1),(2,'33f4b1de08ac7520df813835f1fc0ddf.jpg','2021-03-03 22:37:53.090570','2021-03-03 22:46:25.404353',2,1,NULL,NULL,'4',1),(3,'a278fa70bf151c1dc3464f339409f01e.jpg','2021-03-03 22:38:01.192697','2021-03-03 22:46:27.345496',3,1,NULL,NULL,'1',1),(4,'f2d2843cf7fa2b1dfc264e194994b9ae.jpg','2021-03-03 22:38:13.228182','2021-03-03 22:46:28.087701',4,1,NULL,NULL,'2',1),(5,'c07513039105bcea8633ad6c3018c961.jpg','2021-03-03 22:38:36.501824','2021-03-03 22:46:28.684383',5,1,NULL,NULL,'3',1),(6,'a4a26f2403c1d2e55f4f584b6e5c475c.jpg','2021-03-03 22:38:42.387682','2021-03-03 22:46:29.234741',6,1,NULL,NULL,'3',1),(7,'c3a184e33f84f9eddba52ed73752447a.jpg','2021-03-03 22:38:49.638684','2021-03-03 22:46:29.753569',7,1,NULL,NULL,'3',1),(8,'6581f90b4468daf1173f8ce287f1e930.jpg','2021-03-03 22:45:48.888048','2021-03-03 22:46:30.349822',8,1,NULL,NULL,'5',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=185 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productsproperties`
--

LOCK TABLES `products_productsproperties` WRITE;
/*!40000 ALTER TABLE `products_productsproperties` DISABLE KEYS */;
INSERT INTO `products_productsproperties` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,35),(10,1,36),(11,1,37),(12,1,9),(13,1,10),(14,1,11),(15,1,12),(16,1,13),(17,1,14),(18,1,15),(19,1,16),(20,1,17),(21,1,18),(22,1,19),(23,1,20),(24,1,21),(25,1,22),(26,1,23),(27,1,24),(28,1,25),(29,1,26),(30,1,27),(31,1,28),(32,1,29),(33,1,30),(34,1,31),(35,1,32),(36,1,33),(37,1,34),(38,2,1),(39,2,2),(40,2,6),(41,2,7),(42,2,44),(43,2,4),(44,2,5),(45,2,8),(46,2,35),(47,2,36),(48,2,46),(49,2,47),(50,2,48),(51,2,11),(52,2,12),(53,2,49),(54,2,14),(55,2,50),(56,2,16),(57,2,17),(58,2,18),(103,4,1),(104,4,2),(105,4,54),(106,4,55),(107,4,51),(108,4,52),(109,4,53),(110,4,56),(111,4,57),(112,4,58),(113,4,59),(114,4,60),(115,4,48),(118,4,61),(119,4,62),(120,4,15),(121,4,63),(122,4,64),(123,4,18),(124,4,65),(125,4,20),(126,4,21),(127,4,66),(128,4,67),(129,4,68),(130,4,69),(131,4,70),(132,4,26),(133,4,71),(134,4,72),(135,4,73),(136,4,74),(137,4,75),(138,4,31),(139,4,32),(140,4,76),(141,4,33),(142,4,77),(143,4,34),(144,4,78),(145,5,1),(146,5,2),(147,5,54),(148,5,55),(149,5,51),(150,5,52),(151,5,53),(152,5,79),(153,5,80),(154,5,58),(155,5,59),(156,5,60),(157,5,48),(158,5,61),(159,5,62),(160,5,15),(161,5,63),(162,5,64),(163,5,18),(164,5,81),(165,5,20),(166,5,21),(167,5,66),(168,5,67),(169,5,68),(170,5,69),(171,5,70),(172,5,26),(173,5,71),(174,5,72),(175,5,73),(176,5,82),(177,5,83),(178,5,84),(179,5,85),(180,5,76),(181,5,33),(182,5,77),(183,5,34),(184,5,78);
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
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_propertiesvalues`
--

LOCK TABLES `products_propertiesvalues` WRITE;
/*!40000 ALTER TABLE `products_propertiesvalues` DISABLE KEYS */;
INSERT INTO `products_propertiesvalues` VALUES (1,NULL,'2021-03-03 22:50:07.662555','2021-03-05 17:48:54.137526',1,1,NULL,NULL,'SUR-RON',1,NULL),(2,NULL,'2021-03-03 22:50:25.727373','2021-03-05 18:55:32.282981',2,1,NULL,NULL,'Китай',2,NULL),(3,NULL,'2021-03-03 22:50:48.744621','2021-03-05 18:15:56.896163',3,1,NULL,NULL,'87',3,87.0000),(4,NULL,'2021-03-03 22:51:08.840752','2021-03-05 18:55:39.008157',4,1,NULL,NULL,'200 Н*М',4,NULL),(5,NULL,'2021-03-03 22:51:25.813259','2021-03-05 18:55:44.146752',5,1,NULL,NULL,'1885',5,1885.0000),(6,NULL,'2021-03-03 22:51:44.397847','2021-03-05 17:48:43.932614',6,1,NULL,NULL,'1050',6,1050.0000),(7,NULL,'2021-03-03 22:52:01.074725','2021-03-05 18:55:51.559579',7,1,NULL,NULL,'780',7,780.0000),(8,NULL,'2021-03-03 22:52:19.160946','2021-03-05 18:55:54.784391',8,1,NULL,NULL,'50',8,50.0000),(9,NULL,'2021-03-03 22:52:35.980257','2021-03-05 18:56:11.495462',9,1,NULL,NULL,'100',9,100.0000),(10,NULL,'2021-03-03 22:52:55.149927','2021-03-05 18:56:14.837858',10,1,NULL,NULL,'IP55',10,NULL),(11,NULL,'2021-03-03 22:53:19.889385','2021-03-05 18:56:17.818108',11,1,NULL,NULL,'24',11,24.0000),(12,NULL,'2021-03-03 22:53:35.492024','2021-03-05 18:56:21.339605',12,1,NULL,NULL,'26',12,26.0000),(13,NULL,'2021-03-03 22:53:51.885038','2021-03-05 18:56:24.249901',13,1,NULL,NULL,'5 400 W',13,NULL),(14,NULL,'2021-03-03 22:54:08.893652','2021-03-05 18:56:27.268189',14,1,NULL,NULL,'4',14,4.0000),(15,NULL,'2021-03-03 22:54:19.312296','2021-03-05 18:56:31.070809',15,1,NULL,NULL,'100',15,100.0000),(16,NULL,'2021-03-03 22:54:36.693697','2021-03-05 18:56:34.344822',16,1,NULL,NULL,'BLDC (Безщеточный прямой ток)',16,NULL),(17,NULL,'2021-03-03 22:55:00.547952','2021-03-05 18:56:37.528898',17,1,NULL,NULL,'FOC (Field-Oriented Control) 2 режима езды (эконом/спорт)',17,NULL),(18,NULL,'2021-03-03 22:55:18.892184','2021-03-05 18:56:40.295849',18,1,NULL,NULL,'Гидравлические дисковые тормоза',18,NULL),(19,NULL,'2021-03-03 22:55:35.975391','2021-03-05 18:56:43.231482',19,1,NULL,NULL,'830',19,830.0000),(20,NULL,'2021-03-03 22:55:55.151832','2021-03-05 18:56:45.960747',20,1,NULL,NULL,'26 °',20,NULL),(21,NULL,'2021-03-03 22:56:13.636557','2021-03-05 18:56:48.452252',21,1,NULL,NULL,'45 °',21,NULL),(22,NULL,'2021-03-03 22:56:31.466467','2021-03-05 18:56:51.422542',22,1,NULL,NULL,'46 °',22,NULL),(23,NULL,'2021-03-03 22:56:49.414350','2021-03-05 18:56:54.453240',23,1,NULL,NULL,'4500 об / мин',23,NULL),(24,NULL,'2021-03-03 22:57:05.960040','2021-03-05 18:56:59.905280',24,1,NULL,NULL,'1:7,6',24,NULL),(25,NULL,'2021-03-03 22:57:23.565457','2021-03-05 18:57:06.598536',25,1,NULL,NULL,'Ремень + Цепь',25,NULL),(26,NULL,'2021-03-03 22:57:46.495307','2021-03-05 18:57:10.097666',26,1,NULL,NULL,'Кованая рама полностью из алюминиевого сплава 6082',26,NULL),(27,NULL,'2021-03-03 22:58:06.229564','2021-03-05 18:57:12.764986',27,1,NULL,NULL,'19 х 1.4',27,NULL),(28,NULL,'2021-03-03 22:58:25.452996','2021-03-05 18:57:15.891378',28,1,NULL,NULL,'70/100-19',28,NULL),(29,NULL,'2021-03-03 22:58:40.809184','2021-03-05 18:57:18.635954',29,1,NULL,NULL,'LED Фонарь',29,NULL),(30,NULL,'2021-03-03 22:58:59.956795','2021-03-05 18:57:21.314510',30,1,NULL,NULL,'Есть',30,NULL),(31,NULL,'2021-03-03 22:59:15.561124','2021-03-05 18:57:23.912615',31,1,NULL,NULL,'Отсутствуют',31,NULL),(32,NULL,'2021-03-03 22:59:33.404584','2021-03-05 17:47:31.223870',32,1,NULL,NULL,'Отсутствуют',32,NULL),(33,NULL,'2021-03-03 22:59:51.606059','2021-03-05 18:57:31.226571',33,1,NULL,NULL,'USB-2.1A с одним разъемом',33,NULL),(34,NULL,'2021-03-03 23:00:07.141961','2021-03-05 18:25:15.501943',34,1,NULL,NULL,'Восстановление энергии в спортивном режиме',34,NULL),(35,NULL,'2021-03-03 23:02:08.261027','2021-03-05 18:55:58.513599',35,1,NULL,NULL,'270',35,270.0000),(36,NULL,'2021-03-03 23:02:31.205782','2021-03-05 18:56:03.453180',36,1,NULL,NULL,'1265',36,1265.0000),(37,NULL,'2021-03-03 23:02:50.156347','2021-03-05 18:56:07.536562',37,1,NULL,NULL,'60V 32ah',37,NULL),(44,NULL,'2021-03-05 19:01:40.053054','2021-03-05 19:01:40.053075',38,1,NULL,NULL,'50',3,50.0000),(46,NULL,'2021-03-05 19:03:23.902585','2021-03-05 19:03:23.902604',39,1,NULL,NULL,'48V 20ah',37,NULL),(47,NULL,'2021-03-05 19:03:32.428142','2021-03-05 19:03:32.428162',40,1,NULL,NULL,'80',9,80.0000),(48,NULL,'2021-03-05 19:03:40.877169','2021-03-05 19:03:40.877195',41,1,NULL,NULL,'IP65',10,NULL),(49,NULL,'2021-03-05 19:04:00.455527','2021-03-05 19:04:00.455550',42,1,NULL,NULL,'2 900 W',13,NULL),(50,NULL,'2021-03-05 19:04:13.321243','2021-03-05 19:04:13.321263',43,1,NULL,NULL,'70',15,70.0000),(51,NULL,'2021-03-05 19:12:17.717485','2021-03-05 19:12:17.717505',44,1,NULL,NULL,'110',3,110.0000),(52,NULL,'2021-03-05 19:12:26.115158','2021-03-05 19:12:26.115181',45,1,NULL,NULL,'520 Н*М',4,NULL),(53,NULL,'2021-03-05 19:12:37.371317','2021-03-05 19:12:37.371336',46,1,NULL,NULL,'2120',5,2120.0000),(54,NULL,'2021-03-05 19:12:47.834546','2021-03-05 19:12:47.834569',47,1,NULL,NULL,'1430',6,1430.0000),(55,NULL,'2021-03-05 19:12:55.302865','2021-03-05 19:12:55.302886',48,1,NULL,NULL,'810',7,810.0000),(56,NULL,'2021-03-05 19:13:02.288061','2021-03-05 19:13:02.288080',49,1,NULL,NULL,'118',8,118.0000),(57,NULL,'2021-03-05 19:13:10.602354','2021-03-05 19:13:10.602374',50,1,NULL,NULL,'300',35,300.0000),(58,NULL,'2021-03-05 19:13:16.588770','2021-03-05 19:13:16.588792',51,1,NULL,NULL,'1436',36,1436.0000),(59,NULL,'2021-03-05 19:13:24.158031','2021-03-05 19:13:24.158050',52,1,NULL,NULL,'96V 48ah',37,NULL),(60,NULL,'2021-03-05 19:13:30.290061','2021-03-05 19:13:30.290080',53,1,NULL,NULL,'120',9,120.0000),(61,NULL,'2021-03-05 19:13:59.698711','2021-03-05 19:13:59.698730',54,1,NULL,NULL,'22 500 W',13,NULL),(62,NULL,'2021-03-05 19:14:04.963955','2021-03-05 19:14:04.963975',55,1,NULL,NULL,'3',14,3.0000),(63,NULL,'2021-03-05 19:14:27.217077','2021-03-05 19:14:27.217098',56,1,NULL,NULL,'Бесщеточный центробежный двигатель постоянного тока с воздушным охлаждением, установленным в центре',16,NULL),(64,NULL,'2021-03-05 19:14:39.371126','2021-03-05 19:14:39.371146',57,1,NULL,NULL,'Векторный контроллер синусоидальной волны 150 В FOC',17,NULL),(65,NULL,'2021-03-05 19:15:00.041219','2021-03-05 19:15:00.041239',58,1,NULL,NULL,'900',19,900.0000),(66,NULL,'2021-03-05 19:15:46.909385','2021-03-05 19:15:46.909404',59,1,NULL,NULL,'45 °',22,NULL),(67,NULL,'2021-03-05 19:16:02.579653','2021-03-05 19:16:02.579672',60,1,NULL,NULL,'8000 об / мин',23,NULL),(68,NULL,'2021-03-05 19:16:17.388528','2021-03-05 19:16:17.388546',61,1,NULL,NULL,'8.0113',24,8.0113),(69,NULL,'2021-03-05 19:16:29.985921','2021-03-05 19:16:29.985940',62,1,NULL,NULL,'520 усиленная роликовая',25,NULL),(70,NULL,'2021-03-05 19:17:12.249577','2021-03-05 19:17:12.249599',63,1,NULL,NULL,'Экономичный / Грязевой / Sport + TURBO',39,NULL),(71,NULL,'2021-03-05 19:19:55.693744','2021-03-05 19:20:59.329494',64,1,NULL,NULL,'Передний обод: 19 x 2.50 / Задний обод: 17x 3.75',27,NULL),(72,NULL,'2021-03-05 19:21:40.312143','2021-03-05 19:21:40.312162',65,1,NULL,NULL,'Передний: 110 / 80 - R19 Задний: 140 / 70 - R17',28,NULL),(73,NULL,'2021-03-05 19:21:53.298205','2021-03-05 19:21:53.298224',66,1,NULL,NULL,'ASR + BERS',40,NULL),(74,NULL,'2021-03-05 19:22:04.666139','2021-03-05 19:22:04.666158',67,1,NULL,NULL,'Отсутствует',29,NULL),(75,NULL,'2021-03-05 19:22:14.889125','2021-03-05 19:22:14.889146',68,1,NULL,NULL,'Отсутствует',30,NULL),(76,NULL,'2021-03-05 19:22:46.759479','2021-03-05 19:22:46.759499',69,1,NULL,NULL,'Постоянный ток и постоянное напряжение 105 В / 20 А',41,NULL),(77,NULL,'2021-03-05 19:23:13.824545','2021-03-05 19:23:13.824568',70,1,NULL,NULL,'GPS',42,NULL),(78,NULL,'2021-03-05 19:23:35.848536','2021-03-05 19:23:35.848557',71,1,NULL,NULL,'Сертификация CE',43,NULL),(79,NULL,'2021-03-06 11:32:16.725703','2021-03-06 11:32:16.725724',72,1,NULL,NULL,'126',8,126.0000),(80,NULL,'2021-03-06 11:32:30.481145','2021-03-06 11:32:30.481164',73,1,NULL,NULL,'320',35,320.0000),(81,NULL,'2021-03-06 11:33:42.210098','2021-03-06 11:33:42.210119',74,1,NULL,NULL,'920',19,920.0000),(82,NULL,'2021-03-06 11:35:50.936347','2021-03-06 11:35:50.936367',75,1,NULL,NULL,'Светодиодная LED',29,NULL),(83,NULL,'2021-03-06 11:36:02.016000','2021-03-06 11:36:02.016020',76,1,NULL,NULL,'Светодиод',30,NULL),(84,NULL,'2021-03-06 11:36:12.501670','2021-03-06 11:36:12.501692',77,1,NULL,NULL,'Светодиод',31,NULL),(85,NULL,'2021-03-06 11:36:23.142958','2021-03-06 11:36:23.142983',78,1,NULL,NULL,'Имеются',32,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_property`
--

LOCK TABLES `products_property` WRITE;
/*!40000 ALTER TABLE `products_property` DISABLE KEYS */;
INSERT INTO `products_property` VALUES (1,NULL,'2021-03-03 22:49:45.645426','2021-03-03 22:49:45.645446',1,1,NULL,'','Производитель',NULL,'','',0),(2,NULL,'2021-03-03 22:50:18.504311','2021-03-03 22:50:18.504358',2,1,NULL,'','Страна производства',NULL,'','',0),(3,NULL,'2021-03-03 22:50:44.839390','2021-03-03 22:50:44.839409',3,1,NULL,'','Макс. скорость (км/ч)',NULL,'','',0),(4,NULL,'2021-03-03 22:51:01.033020','2021-03-03 22:51:01.033042',4,1,NULL,'','Крутящий момент',NULL,'','',0),(5,NULL,'2021-03-03 22:51:18.628569','2021-03-03 22:51:18.628588',5,1,NULL,'','Длина (мм)',NULL,'','',0),(6,NULL,'2021-03-03 22:51:40.985764','2021-03-03 22:51:40.985786',6,1,NULL,'','Высота (мм)',NULL,'','',0),(7,NULL,'2021-03-03 22:51:57.083409','2021-03-03 22:51:57.083428',7,1,NULL,'','Ширина (мм)',NULL,'','',0),(8,NULL,'2021-03-03 22:52:11.640568','2021-03-03 22:52:11.640592',8,1,NULL,'','Вес (кг)',NULL,'','',0),(9,NULL,'2021-03-03 22:52:31.824048','2021-03-03 22:52:31.824069',12,1,NULL,'','Грузоподъемность (кг)',NULL,'','',0),(10,NULL,'2021-03-03 22:52:48.289342','2021-03-03 22:52:48.289360',13,1,NULL,'','Класс защиты',NULL,'','',0),(11,NULL,'2021-03-03 22:53:16.686981','2021-03-03 22:53:16.687001',14,1,NULL,'','Распределение веса передней оси (кг)',NULL,'','',0),(12,NULL,'2021-03-03 22:53:32.146891','2021-03-03 22:53:32.146914',15,1,NULL,'','Распределение веса задней оси (кг)',NULL,'','',0),(13,NULL,'2021-03-03 22:53:48.607776','2021-03-03 22:53:48.607795',16,1,NULL,'','Мощность двигателя',NULL,'','',0),(14,NULL,'2021-03-03 22:54:00.631148','2021-03-03 22:54:00.631180',17,1,NULL,'','Время зарядки (ч)',NULL,'','',0),(15,NULL,'2021-03-03 22:54:14.052770','2021-03-03 22:54:14.052789',18,1,NULL,'','Запас хода (км)',NULL,'','',0),(16,NULL,'2021-03-03 22:54:32.698571','2021-03-03 22:54:32.698589',19,1,NULL,'','Двигатель',NULL,'','',0),(17,NULL,'2021-03-03 22:54:49.199950','2021-03-03 22:54:49.199970',20,1,NULL,'','Контроллер',NULL,'','',0),(18,NULL,'2021-03-03 22:55:15.445138','2021-03-03 22:55:15.445157',21,1,NULL,'','Тормозная система',NULL,'','',0),(19,NULL,'2021-03-03 22:55:28.852377','2021-03-03 22:55:28.852422',22,1,NULL,'','Высота сиденья (мм)',NULL,'','',0),(20,NULL,'2021-03-03 22:55:50.692485','2021-03-03 22:55:50.692506',23,1,NULL,'','Угол наклона вперед',NULL,'','',0),(21,NULL,'2021-03-03 22:56:05.649693','2021-03-03 22:56:05.649711',24,1,NULL,'','Макс. угол подъема',NULL,'','',0),(22,NULL,'2021-03-03 22:56:24.440757','2021-03-03 22:56:24.440811',25,1,NULL,'','Угол поворота руля',NULL,'','',0),(23,NULL,'2021-03-03 22:56:40.877011','2021-03-03 22:56:40.877031',26,1,NULL,'','Макс. обороты двигателя',NULL,'','',0),(24,NULL,'2021-03-03 22:57:02.262152','2021-03-03 22:57:02.262171',27,1,NULL,'','Передаточное число',NULL,'','',0),(25,NULL,'2021-03-03 22:57:16.488597','2021-03-03 22:57:16.488615',28,1,NULL,'','Трансмиссия',NULL,'','',0),(26,NULL,'2021-03-03 22:57:34.090798','2021-03-03 22:57:34.090817',29,1,NULL,'','Тип рамы',NULL,'','',0),(27,NULL,'2021-03-03 22:57:55.914892','2021-03-03 22:57:55.914912',30,1,NULL,'','Размер обода',NULL,'','',0),(28,NULL,'2021-03-03 22:58:22.031485','2021-03-03 22:58:22.031504',31,1,NULL,'','Размер шин',NULL,'','',0),(29,NULL,'2021-03-03 22:58:37.374300','2021-03-03 22:58:37.374319',32,1,NULL,'','Фара',NULL,'','',0),(30,NULL,'2021-03-03 22:58:57.063327','2021-03-03 22:58:57.063346',33,1,NULL,'','Задний фонарь',NULL,'','',0),(31,NULL,'2021-03-03 22:59:09.826306','2021-03-03 22:59:09.826329',34,1,NULL,'','Поворотники',NULL,'','',0),(32,NULL,'2021-03-03 22:59:26.634017','2021-03-03 22:59:26.634037',35,1,NULL,'','Зеркала заднего вида',NULL,'','',0),(33,NULL,'2021-03-03 22:59:43.903887','2021-03-03 22:59:43.903906',36,1,NULL,'','USB разъём',NULL,'','',0),(34,NULL,'2021-03-03 23:00:04.258033','2021-03-03 23:00:04.258065',37,1,NULL,'','Рекуперация',NULL,'','',0),(35,NULL,'2021-03-03 23:02:03.270356','2021-03-03 23:02:03.270374',9,1,NULL,'','Минимальный дорожный просвет (мм)',NULL,'','',0),(36,NULL,'2021-03-03 23:02:27.624780','2021-03-03 23:02:27.624801',10,1,NULL,'','Колесная база (мм)',NULL,'','',0),(37,NULL,'2021-03-03 23:02:46.507772','2021-03-03 23:02:46.507793',11,1,NULL,'','Аккумулятор',NULL,'','',0),(39,NULL,'2021-03-05 19:17:07.848702','2021-03-05 19:17:07.848719',38,1,NULL,'','Режимы езды',NULL,'','',0),(40,NULL,'2021-03-05 19:17:47.118500','2021-03-05 19:17:47.118522',39,1,NULL,'','Система ABS',NULL,'','',0),(41,NULL,'2021-03-05 19:18:27.392584','2021-03-05 19:18:27.392601',40,1,NULL,'','Тип зарядного устройства',NULL,'','',0),(42,NULL,'2021-03-05 19:18:46.794705','2021-03-05 19:18:46.794725',41,1,NULL,'','Система геолокации',NULL,'','',0),(43,NULL,'2021-03-05 19:19:02.569221','2021-03-05 19:19:02.569239',42,1,NULL,'','Сертификация продукции',NULL,'','',0);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_orders`
--

LOCK TABLES `shop_orders` WRITE;
/*!40000 ALTER TABLE `shop_orders` DISABLE KEYS */;
INSERT INTO `shop_orders` VALUES (1,NULL,'2021-03-09 13:49:30.707977','2021-03-09 13:49:30.708017',1,1,2,NULL,NULL,735000.00,NULL,1,'','dk@223-223.ru','127.0.0.1','Гость','8(914)8 959-223',0.00,NULL,NULL,NULL),(2,NULL,'2021-03-09 13:52:13.441344','2021-03-09 13:52:13.441368',2,1,2,NULL,NULL,465000.00,NULL,1,'','dk@223-223.ru','127.0.0.1','Kramorov Den','8(914)8 959-223',0.00,NULL,NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_purchases`
--

LOCK TABLES `shop_purchases` WRITE;
/*!40000 ALTER TABLE `shop_purchases` DISABLE KEYS */;
INSERT INTO `shop_purchases` VALUES (2,NULL,'2021-03-09 12:25:48.518005','2021-03-09 12:25:48.518035',1,1,NULL,NULL,1,'1','Электро Байк SUR-RON X Light bee',3,245000.00,1,1,NULL,'','',245000.00,NULL,NULL,NULL),(3,NULL,'2021-03-09 13:52:07.829409','2021-03-09 13:52:07.829429',2,1,NULL,NULL,1,'1','Электро Байк SUR-RON X Light bee',1,245000.00,2,1,NULL,'','',245000.00,NULL,NULL,NULL),(4,NULL,'2021-03-09 13:52:08.465427','2021-03-09 13:52:08.465464',3,1,NULL,NULL,2,'2','Электро Байк SUR-RON S Light bee',1,220000.00,2,1,NULL,'','',220000.00,NULL,NULL,NULL);
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

-- Dump completed on 2021-03-15 12:06:50
