-- MySQL dump 10.13  Distrib 5.7.31, for osx10.12 (x86_64)
--
-- Host: localhost    Database: vanilla
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$vQG7Y4SyOzXP$iBcTYXRSGG8RMV20tCnVsUmdXo2qeEUbfFWtul64RX0=','2021-02-22 21:42:27.023424',1,'jocker','','','dkramorov@mail.ru',1,1,'2021-02-22 16:18:30.887992'),(2,'pbkdf2_sha256$150000$W9x4P0S4DvU5$cERi9tLfIQQYbAJTibqXRvYTF90tOGStl0IYqK36Y/c=',NULL,1,'ap','','','',0,1,'2021-02-23 13:44:39.929743');
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
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-02-22 16:18:29.330355'),(2,'contenttypes','0002_remove_content_type_name','2021-02-22 16:18:29.384197'),(3,'auth','0001_initial','2021-02-22 16:18:29.579628'),(4,'auth','0002_alter_permission_name_max_length','2021-02-22 16:18:29.814665'),(5,'auth','0003_alter_user_email_max_length','2021-02-22 16:18:29.835973'),(6,'auth','0004_alter_user_username_opts','2021-02-22 16:18:29.843423'),(7,'auth','0005_alter_user_last_login_null','2021-02-22 16:18:29.861779'),(8,'auth','0006_require_contenttypes_0002','2021-02-22 16:18:29.864456'),(9,'auth','0007_alter_validators_add_error_messages','2021-02-22 16:18:29.870683'),(10,'auth','0008_alter_user_username_max_length','2021-02-22 16:18:29.889831'),(11,'auth','0009_alter_user_last_name_max_length','2021-02-22 16:18:29.906839'),(12,'auth','0010_alter_group_name_max_length','2021-02-22 16:18:29.923700'),(13,'auth','0011_update_proxy_permissions','2021-02-22 16:18:29.930291'),(14,'files','0001_initial','2021-02-22 16:18:29.978064'),(15,'files','0002_auto_20191203_2054','2021-02-22 16:18:30.038026'),(16,'files','0003_auto_20200112_1717','2021-02-22 16:18:30.047208'),(17,'files','0004_auto_20200402_2127','2021-02-22 16:18:30.068233'),(18,'files','0005_auto_20200809_1025','2021-02-22 16:18:30.073154'),(19,'flatcontent','0001_initial','2021-02-22 16:18:30.168740'),(20,'flatcontent','0002_auto_20190825_1730','2021-02-22 16:18:30.479254'),(21,'flatcontent','0003_auto_20191203_2054','2021-02-22 16:18:30.516897'),(22,'flatcontent','0004_blocks_html','2021-02-22 16:18:30.538613'),(23,'flatcontent','0005_auto_20200112_1717','2021-02-22 16:18:30.573960'),(24,'flatcontent','0006_auto_20200314_1638','2021-02-22 16:18:30.579297'),(25,'flatcontent','0007_auto_20200402_2127','2021-02-22 16:18:30.669403'),(26,'flatcontent','0008_containers_class_name','2021-02-22 16:18:30.688081'),(27,'flatcontent','0009_blocks_class_name','2021-02-22 16:18:30.715870'),(28,'login','0001_initial','2021-02-22 16:18:31.025336'),(29,'login','0002_auto_20200925_1007','2021-02-22 16:18:31.324181'),(30,'main_functions','0001_initial','2021-02-22 16:18:31.365077'),(31,'main_functions','0002_auto_20191203_2052','2021-02-22 16:18:31.388757'),(32,'main_functions','0003_auto_20200407_1845','2021-02-22 16:18:31.638739'),(33,'main_functions','0004_config_user','2021-02-22 16:18:31.747518'),(34,'personal','0001_initial','2021-02-22 16:18:31.812593'),(35,'personal','0002_auto_20200528_1642','2021-02-22 16:18:31.949002'),(36,'personal','0003_auto_20200616_1707','2021-02-22 16:18:31.959721'),(37,'personal','0004_shopper_ip','2021-02-22 16:18:31.998086'),(38,'products','0001_initial','2021-02-22 16:18:32.047833'),(39,'products','0002_productsphotos','2021-02-22 16:18:32.213081'),(40,'products','0003_auto_20200315_2217','2021-02-22 16:18:32.299451'),(41,'products','0004_auto_20200316_2329','2021-02-22 16:18:32.355257'),(42,'products','0005_auto_20200402_2127','2021-02-22 16:18:32.463320'),(43,'products','0006_auto_20200402_2351','2021-02-22 16:18:32.621159'),(44,'products','0007_property_ptype','2021-02-22 16:18:32.643212'),(45,'products','0008_property_code','2021-02-22 16:18:32.669297'),(46,'products','0009_property_measure','2021-02-22 16:18:32.692994'),(47,'products','0010_auto_20200623_1629','2021-02-22 16:18:32.741249'),(48,'products','0011_auto_20200627_1353','2021-02-22 16:18:32.872237'),(49,'products','0012_auto_20201212_1449','2021-02-22 16:18:32.927046'),(50,'products','0013_property_search_facet','2021-02-22 16:18:32.960433'),(51,'sessions','0001_initial','2021-02-22 16:18:32.983070'),(52,'shop','0001_initial','2021-02-22 16:18:33.081120'),(53,'shop','0002_auto_20200618_0000','2021-02-22 16:18:33.384201'),(54,'shop','0003_auto_20200621_1346','2021-02-22 16:18:33.641425'),(55,'shop','0004_purchases_cost_type','2021-02-22 16:18:33.709135'),(56,'shop','0005_transactions','2021-02-22 16:18:33.768951'),(57,'shop','0006_auto_20200719_0003','2021-02-22 16:18:33.945061'),(58,'shop','0007_auto_20200719_0146','2021-02-22 16:18:34.090347'),(59,'shop','0008_auto_20201026_1359','2021-02-22 16:18:34.140923'),(60,'shop','0009_auto_20201212_1539','2021-02-22 16:18:34.197562'),(61,'shop','0010_auto_20210208_1858','2021-02-22 16:18:34.242849'),(62,'shop','0011_orders_external_number','2021-02-22 16:18:34.272856');
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
INSERT INTO `django_session` VALUES ('bsf3ln4ysqmljosxlckkga7fl5gis18a','MzBmMTI0MTA0MTNlYzA3ZmIyMGYwZjg1ZWY1ZWQ0YmVmYjQ3NDcxNjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImY0MGFkNzM5ZTQwZTRiMWFhYjE4ZjA0YjA5YjE2YmU1MmU5NDlmNWQiLCJzaG9wcGVyIjp7ImlkIjoxLCJuYW1lIjoiXHUwNDEzXHUwNDNlXHUwNDQxXHUwNDQyXHUwNDRjIiwiZmlyc3RfbmFtZSI6bnVsbCwibGFzdF9uYW1lIjpudWxsLCJtaWRkbGVfbmFtZSI6bnVsbCwiZW1haWwiOiJka0AyMjMtMjIzLnJ1IiwicGhvbmUiOiI4KDEyMikxIDMzMi0xMTIiLCJhZGRyZXNzIjpudWxsLCJsb2dpbiI6bnVsbCwiZGlzY291bnQiOm51bGwsImJhbGFuY2UiOm51bGwsImlwIjoiMTI3LjAuMC4xIn19','2021-03-09 13:18:06.020507'),('ld4kplg0k69i1o00jbwpg7cdmbjgn0u6','NTc3ZjU1NWQ4NzY4MDI4NTE2ZGE5ZTQzYWNlMjdmNjkwNWUzNDNlNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImY0MGFkNzM5ZTQwZTRiMWFhYjE4ZjA0YjA5YjE2YmU1MmU5NDlmNWQifQ==','2021-03-08 16:19:49.673590');
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
) ENGINE=InnoDB AUTO_INCREMENT=114 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
INSERT INTO `flatcontent_blocks` VALUES (1,'1.png','2021-02-22 16:22:10.443556','2021-02-22 17:07:37.970396',1,1,1,'','Логотип','Добро пожаловать, на наш сайт','/','logo',1,0,'','','','',''),(2,NULL,'2021-02-22 16:22:10.446823','2021-02-22 16:22:10.446844',2,1,3,'','Телефон',NULL,'tel:73952123321','phone',1,0,NULL,NULL,NULL,'+7(3952) 123-321',NULL),(3,NULL,'2021-02-22 16:22:10.450435','2021-02-22 16:22:10.450458',3,1,3,'','Адрес',NULL,NULL,'address',1,0,NULL,NULL,NULL,'г. Иркутск ул. Советская 32а офис 5',NULL),(4,NULL,'2021-02-22 16:22:10.453091','2021-02-22 16:22:10.453112',4,1,3,'','Email',NULL,NULL,'email',1,0,NULL,NULL,NULL,'test@test.ru',NULL),(5,NULL,'2021-02-22 16:22:10.455737','2021-02-22 16:22:10.455758',5,1,3,'','Режим работы',NULL,NULL,'worktime',1,0,NULL,NULL,NULL,'пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 17:00',NULL),(6,NULL,'2021-02-22 16:22:10.458657','2021-02-22 16:22:10.458681',6,1,3,'','Copyright',NULL,NULL,'copyright',1,0,NULL,NULL,NULL,'<p>&copy; 2020 Все права защищены</p>',NULL),(7,NULL,'2021-02-22 16:22:10.461324','2021-02-22 16:22:10.461344',7,1,3,'','Название компании',NULL,NULL,'company_name',1,0,NULL,NULL,'RGBA и COMPыта',NULL,NULL),(8,NULL,'2021-02-22 16:22:10.463969','2021-02-22 16:22:10.463989',8,1,3,'','Сообщества',NULL,NULL,'social',1,0,NULL,NULL,NULL,NULL,NULL),(9,NULL,'2021-02-22 16:22:10.466763','2021-02-22 16:22:10.466782',9,1,3,'_8','instagram',NULL,NULL,'instagram',1,1,'instagram',NULL,NULL,NULL,NULL),(10,NULL,'2021-02-22 16:22:10.469832','2021-02-22 16:22:10.469856',10,1,3,'_8','vk',NULL,NULL,'vk',1,1,'vk',NULL,NULL,NULL,NULL),(11,NULL,'2021-02-22 16:22:10.472765','2021-02-22 16:22:10.472787',11,1,3,'_8','facebook',NULL,NULL,'facebook',1,1,'facebook',NULL,NULL,NULL,NULL),(12,NULL,'2021-02-22 16:22:10.475510','2021-02-22 16:22:10.475529',12,1,3,'_8','twitter',NULL,NULL,'twitter',1,1,'twitter',NULL,NULL,NULL,NULL),(13,NULL,'2021-02-22 16:22:10.482534','2021-02-22 23:07:46.010061',13,1,4,'','Главная','','/','_mainmenu_mainpage',2,0,'','','','',''),(14,NULL,'2021-02-22 16:22:10.484954','2021-02-23 11:26:08.657565',14,1,4,'','Каталог','','/cat/','_mainmenu_catpage',2,0,'','','','',''),(19,NULL,'2021-02-22 16:22:10.501295','2021-02-22 16:22:10.501317',19,1,4,'','О нас',NULL,'/about/','_mainmenu_aboutpage',2,0,NULL,NULL,NULL,NULL,NULL),(20,NULL,'2021-02-22 16:22:10.504034','2021-02-22 16:22:10.504055',20,1,4,'','Услуги',NULL,'/services/','_mainmenu_servicespage',2,0,NULL,NULL,NULL,NULL,NULL),(21,NULL,'2021-02-22 16:22:10.506614','2021-02-22 16:22:10.506634',21,1,4,'','Контакты',NULL,'/feedback/','_mainmenu_feedbackpage',2,0,NULL,NULL,NULL,NULL,NULL),(22,NULL,'2021-02-22 16:22:10.509230','2021-02-22 16:22:10.509250',22,1,4,'','Каталог',NULL,'/cat/','_bottommenu_catpage',3,0,NULL,NULL,NULL,NULL,NULL),(23,NULL,'2021-02-22 16:22:10.512852','2021-02-22 16:22:10.512872',23,1,4,'_22','Популярные товары',NULL,'/cat/populyarnye-tovary/','_bottommenu_catpage_popular',3,0,NULL,NULL,NULL,NULL,NULL),(24,NULL,'2021-02-22 16:22:10.516350','2021-02-22 16:22:10.516371',24,1,4,'_22','Новые товары',NULL,'/cat/novye-tovary/','_bottommenu_catpage_new',3,0,NULL,NULL,NULL,NULL,NULL),(25,NULL,'2021-02-22 16:22:10.519843','2021-02-22 16:22:10.519864',25,1,4,'_22','Товары со скидкой',NULL,'/cat/tovary-so-skidkoy/','_bottommenu_catpage_discount',3,0,NULL,NULL,NULL,NULL,NULL),(26,NULL,'2021-02-22 16:22:10.523587','2021-02-22 16:22:10.523608',26,1,4,'_22','Распродажа',NULL,'/cat/rasprodaja/','_bottommenu_catpage_sale',3,0,NULL,NULL,NULL,NULL,NULL),(27,NULL,'2021-02-22 16:22:10.526182','2021-02-22 16:22:10.526202',27,1,4,'','О нас',NULL,'/about/','_bottommenu_aboutpage',3,0,NULL,NULL,NULL,NULL,NULL),(28,NULL,'2021-02-22 16:22:10.528752','2021-02-22 16:22:10.528771',28,1,4,'','Услуги',NULL,'/services/','_bottommenu_servicespage',3,0,NULL,NULL,NULL,NULL,NULL),(29,NULL,'2021-02-22 16:22:10.531313','2021-02-22 16:22:10.531333',29,1,4,'','Контакты',NULL,'/feedback/','_bottommenu_feedbackpage',3,0,NULL,NULL,NULL,NULL,NULL),(30,NULL,'2021-02-22 16:33:53.359462','2021-02-22 17:02:24.868337',30,1,1,'','Объявление','','','top_banner',1,0,'','','','Натуральная стручковая ваниль из Индонезии без посредников',''),(31,NULL,'2021-02-22 21:42:12.590816','2021-02-22 21:42:12.590840',46,1,1,'','2020 год','Смотреть все','/',NULL,4,0,NULL,NULL,NULL,'<p><b>Расширение дилерской сети и производственных мощностей. </b></p>\r\n<p>По итогам 2020 года компания WHITE SIBERIA продала на рынке КНР свыше\r\n 3500 единиц электротранспорта, а на рынке стран СНГ - свыше 10 000. </p>\r\n<p>В странах СНГ компанию представляют 26 дилеров. В 2020 году состоялся выход на рынки Казахстана и Украины.</p>\r\n<p>Количество сборочных линий на производстве электротранспорта было увеличено до 4.</p>',NULL),(32,NULL,'2021-02-22 21:42:12.602555','2021-02-22 21:42:12.602574',47,1,1,'','2019 год',NULL,NULL,NULL,4,0,NULL,NULL,NULL,'<p><b>Масштабирование компании, повышение спроса и завоевание новых рынков сбыта. </b></p>\r\n<p>За 2019 год на территории КНР было продано свыше 3000 единиц \r\nэлектротранспорта. Это позволило компании масштабироваться и выйти на \r\nновые рынки сбыта. В начале года был открыт офис в Сочи, а буквально \r\nчерез 6 месяцев - в Москве и Минске.</p>',NULL),(33,NULL,'2021-02-22 21:42:12.603476','2021-02-22 21:42:12.603492',48,1,1,'','2018 год',NULL,NULL,NULL,4,0,NULL,NULL,NULL,'<p><b>Мощный рывок в развитии компании и выход в топ.</b></p>\r\n<p>В начале 2018 года состоялось открытие первого офиса и магазина \r\nэлектротранспорта в Шанхае, а к концу года WHITE SIBERIA вошла в топ \r\nкомпаний по продажам электротранспорта иностранцам, проживающим на \r\nтерритории КНР.</p>',NULL),(34,NULL,'2021-02-22 21:42:12.605553','2021-02-22 21:42:12.605576',49,1,1,'','2014 год',NULL,NULL,NULL,4,0,NULL,NULL,NULL,'<p><b>Год основания компании WHITE SIBERIA.</b></p>\r\n<p>В 2014 году в Шанхае была основана компания, которая до 2017 года \r\nзанималась продажей запчастей и комплектующих для коммерческого \r\nтранспорта.</p>',NULL),(35,NULL,'2021-02-22 21:42:12.614007','2021-02-22 21:42:12.614029',52,1,1,'','Политика в отношении обработки персональных данных',NULL,NULL,NULL,5,0,NULL,NULL,NULL,'<h3>1. Общие положения</h3>\r\n<p>Настоящая политика обработки персональных данных составлена в \r\nсоответствии с требованиями Федерального закона от 27.07.2006. №152-ФЗ \r\n«О персональных данных» и определяет порядок обработки персональных \r\nданных и меры по обеспечению безопасности персональных данных, \r\nпредпринимаемые ИП Соболев И.П. (далее – Оператор).</p>\r\n<ul><li>1.1. Оператор ставит своей важнейшей целью и условием осуществления\r\n своей деятельности соблюдение прав и свобод человека и гражданина при \r\nобработке его персональных данных, в том числе защиты прав на \r\nнеприкосновенность частной жизни, личную и семейную тайну.</li><li>1.2. Настоящая политика Оператора в отношении обработки \r\nперсональных данных (далее – Политика) применяется ко всей информации, \r\nкоторую Оператор может получить о посетителях <a href=\"https://white-siberia.com/\">веб-сайта</a>.</li></ul>\r\n<h3>2. Основные понятия, используемые в Политике</h3>\r\n<ul><li>2.1. Автоматизированная обработка персональных данных – обработка персональных данных с помощью средств вычислительной техники;</li><li>2.2. Блокирование персональных данных – временное прекращение \r\nобработки персональных данных (за исключением случаев, если обработка \r\nнеобходима для уточнения персональных данных);</li><li>2.3. Веб-сайт – совокупность графических и информационных \r\nматериалов, а также программ для ЭВМ и баз данных, обеспечивающих их \r\nдоступность в сети интернет по сетевому адресу <a href=\"https://white-siberia.com/\">https://www.white-siberia.com/</a>;</li><li>2.4. Информационная система персональных данных — совокупность \r\nсодержащихся в базах данных персональных данных, и обеспечивающих их \r\nобработку информационных технологий и технических средств;</li><li>2.5. Обезличивание персональных данных — действия, в результате \r\nкоторых невозможно определить без использования дополнительной \r\nинформации принадлежность персональных данных конкретному Пользователю \r\nили иному субъекту персональных данных;</li><li>2.6. Обработка персональных данных – любое действие (операция) или \r\nсовокупность действий (операций), совершаемых с использованием средств \r\nавтоматизации или без использования таких средств с персональными \r\nданными, включая сбор, запись, систематизацию, накопление, хранение, \r\nуточнение (обновление, изменение), извлечение, использование, передачу \r\n(распространение, предоставление, доступ), обезличивание, блокирование, \r\nудаление, уничтожение персональных данных;</li><li>2.7. Оператор – государственный орган, муниципальный орган, \r\nюридическое или физическое лицо, самостоятельно или совместно с другими \r\nлицами организующие и (или) осуществляющие обработку персональных \r\nданных, а также определяющие цели обработки персональных данных, состав \r\nперсональных данных, подлежащих обработке, действия (операции), \r\nсовершаемые с персональными данными;</li><li>2.8. Персональные данные – любая информация, относящаяся прямо или косвенно к определенному или определяемому Пользователю <a href=\"https://white-siberia.com/\">веб-сайта</a>;</li><li>2.9. Пользователь – любой посетитель <a href=\"https://white-siberia.com/\">веб-сайта</a>;</li><li>2.10. Предоставление персональных данных – действия, направленные \r\nна раскрытие персональных данных определенному лицу или определенному \r\nкругу лиц;</li><li>2.11. Распространение персональных данных – любые действия, \r\nнаправленные на раскрытие персональных данных неопределенному кругу лиц \r\n(передача персональных данных) или на ознакомление с персональными \r\nданными неограниченного круга лиц, в том числе обнародование \r\nперсональных данных в средствах массовой информации, размещение в \r\nинформационно-телекоммуникационных сетях или предоставление доступа к \r\nперсональным данным каким-либо иным способом;</li><li>2.12. Трансграничная передача персональных данных – передача \r\nперсональных данных на территорию иностранного государства органу власти\r\n иностранного государства, иностранному физическому или иностранному \r\nюридическому лицу;</li><li>2.13. Уничтожение персональных данных – любые действия, в \r\nрезультате которых персональные данные уничтожаются безвозвратно с \r\nневозможностью дальнейшего восстановления содержания персональных данных\r\n в информационной системе персональных данных и (или) уничтожаются \r\nматериальные носители персональных данных.</li></ul>\r\n<h3>3. Оператор может обрабатывать следующие персональные данные Пользователя</h3>\r\n<ul><li>3.1. Фамилия, имя, отчество;</li><li>3.2. Электронный адрес;</li><li>3.3. Номера телефонов;</li><li>3.4. Название организации;</li><li>3.5. Также на сайте происходит сбор и обработка обезличенных данных\r\n о посетителях (в т.ч. файлов «cookie») с помощью сервисов \r\nинтернет-статистики (Яндекс Метрика и Гугл Аналитика и других).</li><li>3.6. Вышеперечисленные данные далее по тексту Политики объединены общим понятием Персональные данные.</li></ul>\r\n<h3>4. Цели обработки персональных данных</h3>\r\n<ul><li>4.1. Цель обработки персональных данных Пользователя — заключение, \r\nисполнение и прекращение гражданско-правовых договоров; предоставление \r\nдоступа Пользователю к сервисам, информации и/или материалам, \r\nсодержащимся на веб-сайте.</li><li>4.2. Также Оператор имеет право направлять Пользователю уведомления\r\n о новых продуктах и услугах, специальных предложениях и различных \r\nсобытиях. Пользователь всегда может отказаться от получения \r\nинформационных сообщений, направив Оператору письмо на адрес электронной\r\n почты <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a> с пометкой «Отказ от уведомлений о новых продуктах и услугах и специальных предложениях».</li><li>4.3. Обезличенные данные Пользователей, собираемые с помощью \r\nсервисов интернет-статистики, служат для сбора информации о действиях \r\nПользователей на сайте, улучшения качества сайта и его содержания.</li></ul>\r\n<h3>5. Правовые основания обработки персональных данных</h3>\r\n<ul><li>5.1. Оператор обрабатывает персональные данные Пользователя только в\r\n случае их заполнения и/или отправки Пользователем самостоятельно через \r\nспециальные формы, расположенные на <a href=\"https://white-siberia.com/\">сайте</a>.\r\n Заполняя соответствующие формы и/или отправляя свои персональные данные\r\n Оператору, Пользователь выражает свое согласие с данной Политикой.</li><li>5.2. Оператор обрабатывает обезличенные данные о Пользователе в \r\nслучае, если это разрешено в настройках браузера Пользователя (включено \r\nсохранение файлов «cookie» и использование технологии JavaScript).</li></ul>\r\n<h3>6. Порядок сбора, хранения, передачи и других видов обработки персональных данных</h3>\r\n<p>Безопасность персональных данных, которые обрабатываются Оператором, \r\nобеспечивается путем реализации правовых, организационных и технических \r\nмер, необходимых для выполнения в полном объеме требований действующего \r\nзаконодательства в области защиты персональных данных.</p>\r\n<ul><li>6.1. Оператор обеспечивает сохранность персональных данных и \r\nпринимает все возможные меры, исключающие доступ к персональным данным \r\nнеуполномоченных лиц.</li><li>6.2. Персональные данные Пользователя никогда, ни при каких \r\nусловиях не будут переданы третьим лицам, за исключением случаев, \r\nсвязанных с исполнением действующего законодательства.</li><li>6.3. В случае выявления неточностей в персональных данных, \r\nПользователь может актуализировать их самостоятельно, путем направления \r\nОператору уведомление на адрес электронной почты Оператора <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a> с пометкой «Актуализация персональных данных».</li><li>6.4. Срок обработки персональных данных является неограниченным. \r\nПользователь может в любой момент отозвать свое согласие на обработку \r\nперсональных данных, направив Оператору уведомление посредством \r\nэлектронной почты на электронный адрес Оператора <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a> с пометкой «Отзыв согласия на обработку персональных данных».</li></ul>\r\n<h3>7. Трансграничная передача персональных данных</h3>\r\n<ul><li>7.1. Оператор до начала осуществления трансграничной передачи \r\nперсональных данных обязан убедиться в том, что иностранным \r\nгосударством, на территорию которого предполагается осуществлять \r\nпередачу персональных данных, обеспечивается надежная защита прав \r\nсубъектов персональных данных.</li><li>7.2. Трансграничная передача персональных данных на территории \r\nиностранных государств, не отвечающих вышеуказанным требованиям, может \r\nосуществляться только в случае наличия согласия в письменной форме \r\nсубъекта персональных данных на трансграничную передачу его персональных\r\n данных и/или исполнения договора, стороной которого является субъект \r\nперсональных данных.</li></ul>\r\n<h3>8. Заключительные положения</h3>\r\n<ul><li>8.1. Пользователь может получить любые разъяснения по интересующим \r\nвопросам, касающимся обработки его персональных данных, обратившись к \r\nОператору с помощью электронной почты <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a>.</li><li>8.2. В данном документе будут отражены любые изменения политики \r\nобработки персональных данных Оператором. Политика действует бессрочно \r\nдо замены ее новой версией.</li><li>8.3. Актуальная версия Политики в свободном доступе расположена в сети Интернет на <a href=\"https://white-siberia.com/privacy/\">этой странице</a>.</li></ul>',NULL),(36,'ower-2.png','2021-02-22 21:42:12.620571','2021-02-22 21:42:12.620588',122,1,1,'','Надежность, функциональность и мощь',NULL,NULL,NULL,6,0,NULL,NULL,NULL,'<div>\r\n											<ul><li>Грузоподъемность до 260 кг</li><li>Мотор тягового типа мощностью 3000 Вт</li><li>Возможность всесезонной эксплуатации</li><li>Шикарная комплектация: бокс, сетка-багажник, держатель для телефона, удобная спинка</li></ul>\r\n										</div>',NULL),(37,'ower-3.png','2021-02-22 21:42:12.629421','2021-02-22 21:42:12.629442',123,1,1,'','Максимальный комфорт даже на бездорожье',NULL,NULL,NULL,6,0,NULL,NULL,NULL,'<div>\r\n											<ul><li>Комфортная и динамичная езда благодаря 10–дюймовым колёсам</li><li>Большое и мягкое сиденье </li><li>Настраиваемая подвеска</li></ul>\r\n										</div>',NULL),(38,'ower-1.png','2021-02-22 21:42:12.645431','2021-02-22 21:42:12.645456',124,1,1,'','Безопасное передвижение в темное время суток',NULL,NULL,NULL,6,0,NULL,NULL,NULL,'<div>\r\n											<ul><li>1 мощная фара + 2 стробоскопа (вспомогательный свет)</li><li>Яркие задние ходовые огни, сертифицированные ECC</li><li>Поворотники LED с ярким свечением </li></ul>\r\n										</div>',NULL),(39,'ower-4.png','2021-02-22 21:42:12.660021','2021-02-22 21:42:12.660049',125,1,1,'','Уверенность в каждом километре',NULL,NULL,NULL,6,0,NULL,NULL,NULL,'<div>\r\n											<ul><li>Максимальная скорость до 45 км/ч</li><li>Тормозная система нового вида с возможностью регулировки</li><li>Обновленная тормозная система с возможностью регулировки</li><li>Масляные амортизаторы с возможностью регулировки</li><li>Плавность старта и торможения</li></ul>\r\n										</div>',NULL),(40,'ower-5.png','2021-02-22 21:42:12.678293','2021-02-22 21:42:12.678325',126,1,1,'','Инновационный LI-ION аккумулятор',NULL,NULL,NULL,6,0,NULL,NULL,NULL,'<div>\r\n											<ul><li>Пробег до 60 км на одном заряде</li><li>Быстросъёмный аккумулятор с балансировочной платой</li><li>Возможность установить вторую батарею и проезжать до 100 км</li><li>Производство TAIWAN</li></ul>\r\n										</div>',NULL),(41,'ower-6.png','2021-02-22 21:42:12.692333','2021-02-22 21:42:12.692360',127,1,1,'','Удобство и простота использования',NULL,NULL,NULL,6,0,NULL,NULL,NULL,'<div>\r\n											<ul><li>Большие, интуитивно понятные кнопки управления</li><li>Бортовой компьютер с LED-дисплеем</li><li>Большие зеркала без искажения</li><li>Держатель телефона с USB</li><li>Вместительный бокс и сетка-багажник</li><li>Кнопка Start-Stop</li><li>Сигнализация</li></ul>\r\n										</div>',NULL),(42,'banner.png','2021-02-22 21:42:12.722513','2021-02-22 21:42:12.722545',50,1,1,'','В семью!','Подробнее','/',NULL,7,0,NULL,NULL,NULL,'<p>Электротранспорт под брендом WHITE SIBERIA – это качество, \r\nнадежность, стильный дизайн и приемлемая цена. Именно поэтому наша \r\nдилерская сеть стремительно растет, а ассортимент техники на витринах \r\nмагазинов в России и странах СНГ – расширяется.</p>\r\n						<p>Если Вы хотите стать участником нашей дилерской сети и \r\nприсоединиться к выполнению нашей миссии – заполните форму, и мы \r\nобязательно свяжемся с Вами.</p>',NULL),(43,'surron-logo.png','2021-02-22 21:42:12.765560','2021-02-22 21:42:12.765589',98,1,1,'','SUR-RON','Перейти на сайт','https://surronrussia.ru/',NULL,8,1,NULL,NULL,NULL,'Мы являемся<br>официальными представителями<br>техники SUR-RON',NULL),(44,NULL,'2021-02-22 21:42:12.800248','2021-02-22 21:42:12.800268',54,1,1,'','Россия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(45,NULL,'2021-02-22 21:42:12.801124','2021-02-22 21:42:12.801142',58,1,1,'_44','Адреса',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(46,NULL,'2021-02-22 21:42:12.802142','2021-02-22 21:42:12.802160',69,1,1,'_44_45','Адрес1',NULL,NULL,NULL,10,0,'map-marker',NULL,NULL,'г. Москва, дер. Марушкино, ул. Северная\r\n<br>',NULL),(47,NULL,'2021-02-22 21:42:12.803069','2021-02-22 21:42:12.803088',70,1,1,'_44_45','Адрес2',NULL,NULL,NULL,10,0,'map-marker',NULL,NULL,'г. Сочи, Адлерский р-н, ул. Садовая 48',NULL),(48,NULL,'2021-02-22 21:42:12.803996','2021-02-22 21:42:12.804016',62,1,1,'_44','Оптовый отдел',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(49,NULL,'2021-02-22 21:42:12.805181','2021-02-22 21:42:12.805206',75,1,1,'_44_48','Телефон',NULL,NULL,NULL,10,0,'phone',NULL,NULL,'<a href=\"tel:+79384704147\">+7 938 470 41 47</a>',NULL),(50,NULL,'2021-02-22 21:42:12.806377','2021-02-22 21:42:12.806400',76,1,1,'_44_48','WhatsApp',NULL,NULL,NULL,10,0,'phone-square',NULL,NULL,'+7 938 470 41 47',NULL),(51,NULL,'2021-02-22 21:42:12.807425','2021-02-22 21:42:12.807445',77,1,1,'_44_48','Email',NULL,NULL,NULL,10,0,'envelope-o',NULL,NULL,'opt@white-siberia.com',NULL),(52,NULL,'2021-02-22 21:42:12.808556','2021-02-22 21:42:12.808578',66,1,1,'_44','Розничный отдел',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(53,NULL,'2021-02-22 21:42:12.809573','2021-02-22 21:42:12.809592',78,1,1,'_44_52','Телефон',NULL,NULL,NULL,10,0,'phone',NULL,NULL,'+7 988 169 16 39',NULL),(54,NULL,'2021-02-22 21:42:12.810538','2021-02-22 21:42:12.810558',79,1,1,'_44_52','WhatsApp',NULL,NULL,NULL,10,0,'phone-square',NULL,NULL,'+7 988 403 85 43',NULL),(55,NULL,'2021-02-22 21:42:12.811467','2021-02-22 21:42:12.811486',80,1,1,'_44_52','Email',NULL,NULL,NULL,10,0,'envelope-o',NULL,NULL,'roznica@white-siberia.com',NULL),(56,NULL,'2021-02-22 21:42:12.814779','2021-02-22 21:42:12.814800',67,1,1,'_44','Гарантийный отдел',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(57,NULL,'2021-02-22 21:42:12.815776','2021-02-22 21:42:12.815796',81,1,1,'_44_56','Телефон',NULL,NULL,NULL,10,0,'phone',NULL,NULL,'+7 989 085 87 45',NULL),(58,NULL,'2021-02-22 21:42:12.816699','2021-02-22 21:42:12.816719',82,1,1,'_44_56','WhatsApp',NULL,NULL,NULL,10,0,'phone-square',NULL,NULL,'+7 989 085 87 45',NULL),(59,NULL,'2021-02-22 21:42:12.817819','2021-02-22 21:42:12.817839',83,1,1,'_44_56','Email',NULL,NULL,NULL,10,0,'envelope-o',NULL,NULL,'guarantee@white-siberia.com',NULL),(60,NULL,'2021-02-22 21:42:12.818801','2021-02-22 21:42:12.818822',55,1,1,'','Беларусь',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(61,NULL,'2021-02-22 21:42:12.819917','2021-02-22 21:42:12.819936',59,1,1,'_60','Адреса',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(62,NULL,'2021-02-22 21:42:12.821078','2021-02-22 21:42:12.821097',71,1,1,'_60_61','Адрес1',NULL,NULL,NULL,10,0,'map-marker',NULL,NULL,'г. Минск Новая Боровая, Авиационная 10',NULL),(63,NULL,'2021-02-22 21:42:12.822040','2021-02-22 21:42:12.822057',63,1,1,'_60','Оптовый отдел',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(64,NULL,'2021-02-22 21:42:12.822955','2021-02-22 21:42:12.822973',84,1,1,'_60_63','Телефон',NULL,NULL,NULL,10,0,'phone',NULL,NULL,'<a href=\"tel:+375333274526\">+375 33 327 45 26</a>',NULL),(65,NULL,'2021-02-22 21:42:12.823837','2021-02-22 21:42:12.823856',85,1,1,'_60_63','WhatsApp',NULL,NULL,NULL,10,0,'phone-square',NULL,NULL,'<a href=\"https://wa.me/375333274526\">+375 33 327 45 26</a>',NULL),(66,NULL,'2021-02-22 21:42:12.824667','2021-02-22 21:42:12.824683',86,1,1,'_60_63','Email',NULL,NULL,NULL,10,0,'envelope-o',NULL,NULL,'<a href=\"mailto:opt@white-siberia.com\">opt@white-siberia.com</a>',NULL),(67,NULL,'2021-02-22 21:42:12.826707','2021-02-22 21:42:12.826723',56,1,1,'','Китай',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(68,NULL,'2021-02-22 21:42:12.827708','2021-02-22 21:42:12.827725',60,1,1,'_67','Адреса',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(69,NULL,'2021-02-22 21:42:12.828513','2021-02-22 21:42:12.828529',72,1,1,'_67_68','Адрес1',NULL,NULL,NULL,10,0,'map-marker',NULL,NULL,'Shanghai Channing district Channing street 398',NULL),(70,NULL,'2021-02-22 21:42:12.829361','2021-02-22 21:42:12.829379',73,1,1,'_67_68','Адрес2',NULL,NULL,NULL,10,0,'map-marker',NULL,NULL,'Shanghai Jiading district JiaSongbei street 6855',NULL),(71,NULL,'2021-02-22 21:42:12.830163','2021-02-22 21:42:12.830182',64,1,1,'_67','Оптовый отдел',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(72,NULL,'2021-02-22 21:42:12.831047','2021-02-22 21:42:12.831064',87,1,1,'_67_71','Телефон',NULL,NULL,NULL,10,0,'phone',NULL,NULL,'<a href=\"tel:+8613167039323\">+86 131 6703 9323</a>',NULL),(73,NULL,'2021-02-22 21:42:12.831890','2021-02-22 21:42:12.831905',88,1,1,'_67_71','WhatsApp',NULL,NULL,NULL,10,0,'phone-square',NULL,NULL,'<a href=\"https://wa.me/8613167039323\">+86 131 6703 9323</a>',NULL),(74,NULL,'2021-02-22 21:42:12.832952','2021-02-22 21:42:12.832968',89,1,1,'_67_71','Email',NULL,NULL,NULL,10,0,'envelope-o',NULL,NULL,'<a href=\"mailto:opt@white-siberia.com\">opt@white-siberia.com</a>',NULL),(75,NULL,'2021-02-22 21:42:12.833737','2021-02-22 21:42:12.833753',68,1,1,'_67','WeChat ID',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(76,NULL,'2021-02-22 21:42:12.834488','2021-02-22 21:42:12.834503',90,1,1,'_67_75','Без названия',NULL,NULL,NULL,10,0,'wechat',NULL,NULL,'motobike-shanghai',NULL),(77,NULL,'2021-02-22 21:42:12.835565','2021-02-22 21:42:12.835581',57,1,1,'','Казахстан',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(78,NULL,'2021-02-22 21:42:12.836354','2021-02-22 21:42:12.836370',61,1,1,'_77','Адреса',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(79,NULL,'2021-02-22 21:42:12.837131','2021-02-22 21:42:12.837146',74,1,1,'_77_78','Адрес1',NULL,NULL,NULL,10,0,'map-marker',NULL,NULL,'г. Караганда, ул. Крылова, д. 101',NULL),(80,NULL,'2021-02-22 21:42:12.838044','2021-02-22 21:42:12.838062',65,1,1,'_77','Оптовый отдел',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(81,NULL,'2021-02-22 21:42:12.838926','2021-02-22 21:42:12.838943',91,1,1,'_77_80','Телефон',NULL,NULL,NULL,10,0,'phone',NULL,NULL,'<a href=\"tel:+77711290202\">+7 771 129 02 02</a>',NULL),(82,NULL,'2021-02-22 21:42:12.839726','2021-02-22 21:42:12.839741',92,1,1,'_77_80','WhatsApp',NULL,NULL,NULL,10,0,'phone-square',NULL,NULL,'<a href=\"https://wa.me/77711290202\">+7 771 129 02 02</a>',NULL),(83,NULL,'2021-02-22 21:42:12.840876','2021-02-22 21:42:12.840902',93,1,1,'_77_80','Email',NULL,NULL,NULL,10,0,'envelope-o',NULL,NULL,'<a href=\"mailto:opt@white-siberia.com\">opt@white-siberia.com</a>',NULL),(85,NULL,'2021-02-22 21:42:12.856527','2021-02-22 21:42:12.856551',51,1,1,'','Описание',NULL,NULL,NULL,12,0,NULL,NULL,NULL,'<p>Если Вы хотите стать участником нашей дилерской сети и \r\nпопуляризировать электротранспорт вместе с нами – заполните форму, и мы \r\nобязательно свяжемся с Вами в ближайшее время. </p>\r\n<p>В графе «Дополнительные сведения» просим Вас указать следующую информацию: </p>\r\n<p>Есть ли у Вас опыт продаж или обслуживания электротранспорта?</p>\r\n<p>Вы планируете продажи онлайн или оффлайн? </p>\r\n<p>Есть ли у Вас розничная точка продаж? </p>\r\n<p>Укажите Ваш сайт (если есть).</p>\r\n<p>Будем рады поработать вместе с Вами!</p>',NULL),(86,'40.jpg','2021-02-22 21:42:12.881247','2021-02-22 21:42:12.881268',38,1,1,'','WS-PRO 2WD',NULL,'/',NULL,14,0,NULL,NULL,NULL,'60v 4000w',NULL),(87,'41.jpg','2021-02-22 21:42:12.890237','2021-02-22 21:42:12.890266',39,1,1,'','WS-PRO MAX+',NULL,'/',NULL,14,0,NULL,NULL,NULL,'60v 3000w',NULL),(88,'42.png','2021-02-22 21:42:12.921278','2021-02-22 21:42:12.921307',40,1,1,'','WS-TAIGA',NULL,'/',NULL,14,0,NULL,NULL,NULL,'48v 800w',NULL),(89,NULL,'2021-02-22 21:42:12.951253','2021-02-22 21:42:12.951279',99,1,1,'','video1','Перейти на YouTube','https://www.youtube.com/channel/UCLMxls9urKSgQdE7setOt9w',NULL,15,1,'youtube-play',NULL,NULL,'<iframe src=\"https://www.youtube.com/embed/u8Tx7XC5q8k\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" width=\"398\" height=\"199\" frameborder=\"0\"></iframe>',NULL),(90,NULL,'2021-02-22 21:42:12.962496','2021-02-22 21:42:12.962521',100,1,1,'','video2',NULL,NULL,NULL,15,0,NULL,NULL,NULL,'<iframe width=\"398\" height=\"199\" src=\"https://www.youtube.com/embed/L8OU9xwCUXE\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>',NULL),(91,NULL,'2021-02-22 21:42:12.963539','2021-02-22 21:42:12.963558',101,1,1,'','video3',NULL,NULL,NULL,15,0,NULL,NULL,NULL,'<iframe width=\"398\" height=\"199\" src=\"https://www.youtube.com/embed/t_l9If6U_J4\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>',NULL),(92,NULL,'2021-02-22 21:42:12.964412','2021-02-22 21:42:12.964430',102,1,1,'','video4',NULL,NULL,NULL,15,0,NULL,NULL,NULL,'<iframe src=\"https://www.youtube.com/embed/lfSkjl0Qu68\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" width=\"398\" height=\"199\" frameborder=\"0\"></iframe>',NULL),(93,'43.png','2021-02-22 21:46:57.900483','2021-02-22 21:48:54.490095',38,1,1,'','Качество в деталях','','/o-kompanii/','',16,0,'','','','Натуральная 100% ваниль',''),(94,'44.png','2021-02-22 21:46:57.905616','2021-02-22 21:49:27.481494',39,1,1,'','Ваниль для кондитеров','','/o-kompanii/','',16,0,'','','','и пищевой промышленности',''),(95,'45.jpg','2021-02-22 21:46:57.914510','2021-02-22 21:50:01.969228',40,1,1,'','Прямые поставки','','/o-kompanii/','',16,0,'','','','от производителя',''),(96,NULL,'2021-02-22 22:11:30.365920','2021-02-22 22:12:49.218020',46,1,1,'','2020 год','Смотреть все','/','',18,0,'','','','<p><b>Расширение дилерской сети и производственных мощностей. </b></p>\r\n<p></p><p>По итогам 2020 года компания ТопВанила продала на рынке России свыше\r\n 35000 единиц упаковок ванили, а на рынке стран СНГ - свыше 40 000. </p>\r\n<p>В странах СНГ компанию представляют 26 дилеров. В 2020 году состоялся выход на рынки Казахстана и Украины.</p><p></p>',''),(97,NULL,'2021-02-22 22:11:30.368282','2021-02-22 22:12:56.110993',47,1,1,'','2019 год','','','',18,0,'','','','<p><b>Масштабирование компании, повышение спроса и завоевание новых рынков сбыта. </b></p>\r\n<p>За 2019 год на территории России было продано свыше 33000 единиц \r\nупаковок ванили. Это позволило компании масштабироваться и выйти на \r\nновые рынки сбыта.</p>',''),(98,NULL,'2021-02-22 22:11:30.369135','2021-02-22 22:13:08.735203',48,1,1,'','2018 год','','','',18,0,'','','','<p><b>Мощный рывок в развитии компании и выход в топ.</b></p>\r\n<p>В начале 2018 года состоялось открытие первого офиса и магазина \r\nванили в Москве, а к концу года ТопВанила вошла в топ \r\nкомпаний по продажам ванили в России и странах содружества.</p>',''),(99,NULL,'2021-02-22 22:11:30.370055','2021-02-22 22:13:20.356203',49,1,1,'','2014 год','','','',18,0,'','','','<p><b>Год основания компании WHITE SIBERIA.</b></p>\r\n<p>В 2014 году в Индонезии было основано производство ванили. Начало \r\nоптовых поставок в Россию и СНГ. Товар сразу был принят и оценен, как \r\nпродукт высочайшего качества.</p>',''),(100,'60.png','2021-02-22 22:14:06.734354','2021-02-22 22:16:27.770854',50,1,1,'','В мир природного качества!','Подробнее','/','',19,0,'','','','<p>Ваниль – это лиана с длинным, высоко взбирающимся на деревья стеблем, образующим воздушные корни.</p>\r\n<p>\r\nЛистья мясистые, продолговато-овальные и кольцевидные, желто-зеленые цветки в кистях, одна тычинка и пестик спрятаны в лепестке-трубочке, что затрудняем опыление. Плод – узкий трехгранный стручок длиной 7 – 30 см. \r\n</p>',''),(101,NULL,'2021-02-22 22:21:22.650014','2021-02-22 22:21:52.116777',235,1,4,'','Ваниль в стручках','Собственное производство ванили в стручках в индонезии','/product/vanil-v-struchkah-1/','product_1',20,0,NULL,'ваниль, стручки, vanilla','ваниль в стручках',NULL,NULL),(102,NULL,'2021-02-22 22:22:13.370455','2021-02-22 22:23:29.765656',236,1,4,'','Молотая ваниль','Натуральную ваниль очень мелко размалывают','/product/molotaya-vanil-2/','product_2',20,0,NULL,'молотая ваниль, порошковая ваниль, vanilla','Молотая ваниль',NULL,NULL),(103,NULL,'2021-02-22 22:23:41.869498','2021-02-22 22:25:01.857877',237,1,4,'','Эстракт ванили','Натуральную ваниль очень мелко размалывают','/product/estrakt-vanili-3/','product_3',20,0,NULL,'молотая ваниль, порошковая ваниль, vanilla','Молотая ваниль',NULL,NULL),(104,'client-1.jpg','2021-02-22 22:41:58.163548','2021-02-22 22:44:41.984167',238,1,1,'','Оксана - Бизнесмен','','','',22,0,'','','','Покупаю в розничных сетях продукцию, довольна качеством, но гораздо выгоднее купить оптом - большая экономия и на цене и на доставке, планирую наращивать объемы закупок для увеличения прибыли, бизнес выгодный<br>',''),(105,'client-2.jpg','2021-02-22 22:42:05.949398','2021-02-22 22:46:06.167786',239,1,1,'','Марина - Бизнесмен','','','',22,0,'','','','Поставляю продукцию в регионы, цена ниже рыночной, качество - выше. Как посредние довольна тем, что поставки стабильные, никаких проволочек нет. Будем укреплять сотрудничество для взаимной выгоды<br>',''),(106,'client-1.jpg','2021-02-22 22:47:38.578164','2021-02-22 22:47:38.578182',238,1,1,'','Оксана - Бизнесмен','','','',23,0,'','','','Покупаю в розничных сетях продукцию, довольна качеством, но гораздо выгоднее купить оптом - большая экономия и на цене и на доставке, планирую наращивать объемы закупок для увеличения прибыли, бизнес выгодный<br>',''),(107,'client-2.jpg','2021-02-22 22:47:38.581680','2021-02-22 22:47:38.581699',239,1,1,'','Марина - Бизнесмен','','','',23,0,'','','','Поставляю продукцию в регионы, цена ниже рыночной, качество - выше. Как посредние довольна тем, что поставки стабильные, никаких проволочек нет. Будем укреплять сотрудничество для взаимной выгоды<br>',''),(108,NULL,'2021-02-22 22:59:57.264585','2021-02-22 23:00:41.461161',240,1,1,'','Круглосуточная консультация','','','',24,0,'headphones','','','Мы проконсультируем вас о всех интересующих вас вопросах в любое время суток - удобное для вас<br>',''),(109,NULL,'2021-02-22 22:59:58.114602','2021-02-22 23:01:49.069860',241,1,1,'','Безопасная оплата','','','',24,0,'money','','','Оплата производится безопасно для вас, мы гарантируем, что деньги будут заморожены до тех пор, пока вы не получите покупку<br>',''),(110,NULL,'2021-02-22 22:59:59.116231','2021-02-22 23:02:35.082496',242,1,1,'','Удобный возврат','','','',24,0,'retweet','','','Вы можете возвратить товар, либо обменять если вас не устраивает качество, также вы можете вернуть деньги<br>',''),(111,NULL,'2021-02-22 23:03:08.168563','2021-02-22 23:03:08.168581',240,1,1,'','Круглосуточная консультация','','','',25,0,'headphones','','','Мы проконсультируем вас о всех интересующих вас вопросах в любое время суток - удобное для вас<br>',''),(112,NULL,'2021-02-22 23:03:08.169537','2021-02-22 23:03:08.169560',241,1,1,'','Безопасная оплата','','','',25,0,'money','','','Оплата производится безопасно для вас, мы гарантируем, что деньги будут заморожены до тех пор, пока вы не получите покупку<br>',''),(113,NULL,'2021-02-22 23:03:08.170475','2021-02-22 23:03:08.170493',242,1,1,'','Удобный возврат','','','',25,0,'retweet','','','Вы можете возвратить товар, либо обменять если вас не устраивает качество, также вы можете вернуть деньги<br>','');
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
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
INSERT INTO `flatcontent_containers` VALUES (1,NULL,'2021-02-22 16:22:10.438512','2021-02-22 16:22:10.438548',1,1,2,NULL,'Контент для всех страничек','Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики','main',NULL,NULL),(2,NULL,'2021-02-22 16:22:10.477777','2021-02-22 16:22:10.477795',2,1,1,NULL,'Главное меню','Создано автоматически, выводит главное меню','mainmenu',NULL,NULL),(3,NULL,'2021-02-22 16:22:10.480046','2021-02-23 11:52:18.696793',3,1,1,'','Полезная информация','Создано автоматически, выводит нижнее меню','bottommenu','',''),(4,NULL,'2021-02-22 21:42:12.568656','2021-02-22 21:42:12.568688',4,1,99,NULL,'О нас','О компании<br>','about',NULL,NULL),(5,NULL,'2021-02-22 21:42:12.612145','2021-02-22 21:42:12.612170',5,1,99,NULL,'Простая статья','Приватность','article',NULL,NULL),(6,NULL,'2021-02-22 21:42:12.618970','2021-02-22 21:42:12.618991',6,1,99,NULL,'Статья (Вариант 2)',NULL,'article2',NULL,NULL),(7,NULL,'2021-02-22 21:42:12.714613','2021-02-22 21:42:12.714638',7,1,99,NULL,'Статья - Темный фон','Добро пожаловать','article_dark',NULL,NULL),(8,'surron.png','2021-02-22 21:42:12.743680','2021-02-22 21:42:12.743706',8,1,99,NULL,'Заголовок',NULL,'call_to_action',NULL,NULL),(9,NULL,'2021-02-22 21:42:12.788209','2021-02-22 21:42:12.788236',9,1,99,NULL,'Каталог',NULL,'catalogue',NULL,NULL),(10,NULL,'2021-02-22 21:42:12.798242','2021-02-22 21:42:12.798268',10,1,99,NULL,'Контакты','Контакты<br>','contacts',NULL,NULL),(12,NULL,'2021-02-22 21:42:12.848972','2021-02-22 21:42:12.848990',12,1,99,NULL,'Написать  нам','Стать дилером','feedback',NULL,NULL),(13,NULL,'2021-02-22 21:42:12.875816','2021-02-22 22:32:19.086691',13,1,99,'','Товары','Наши предложения<br>','products','',''),(14,NULL,'2021-02-22 21:42:12.879548','2021-02-22 21:42:12.879571',14,1,99,NULL,'Слайдер',NULL,'slider',NULL,NULL),(15,NULL,'2021-02-22 21:42:12.943359','2021-02-22 21:42:12.943385',15,1,99,NULL,'Видео','Обзоры техники','videos',NULL,NULL),(16,NULL,'2021-02-22 21:46:57.887181','2021-02-22 21:46:57.887199',16,1,3,'','Слайдер на главной','','slider','',''),(17,NULL,'2021-02-22 21:47:24.006817','2021-02-22 21:47:24.006841',17,1,7,NULL,'Каталог товаров',NULL,'catalogue',NULL,NULL),(18,NULL,'2021-02-22 22:11:30.355325','2021-02-22 22:11:30.362355',18,1,3,'','О компании','О компании<br>','about','',''),(19,NULL,'2021-02-22 22:14:06.723395','2021-02-22 22:14:06.730160',19,1,3,'','Статья на главной (темный фон)','Добро пожаловать','article_dark','',''),(20,NULL,'2021-02-22 22:21:22.646328','2021-02-22 22:21:22.646351',20,1,4,NULL,'Сео-тексты для товаров/услуг',NULL,'seo_for_products',NULL,NULL),(21,NULL,'2021-02-22 22:26:17.445843','2021-02-22 22:26:24.807426',21,1,3,'','Наши предложения','Наши предложения<br>','products','',''),(22,NULL,'2021-02-22 22:35:29.624659','2021-02-22 22:35:40.574599',22,1,99,'','Отзывы','Что говорят покупатели?<br>','reviews','',''),(23,NULL,'2021-02-22 22:47:38.568501','2021-02-22 22:47:38.573908',23,1,3,'','Отзывы','Что говорят покупатели?<br>','reviews','',''),(24,NULL,'2021-02-22 22:59:48.966679','2021-02-22 22:59:52.163040',24,1,99,'','Преимущества','','advantages','',''),(25,NULL,'2021-02-22 23:03:08.161541','2021-02-22 23:03:08.161561',25,1,3,'','Преимущества','','advantages','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_linkcontainer`
--

LOCK TABLES `flatcontent_linkcontainer` WRITE;
/*!40000 ALTER TABLE `flatcontent_linkcontainer` DISABLE KEYS */;
INSERT INTO `flatcontent_linkcontainer` VALUES (22,NULL,'2021-02-22 23:07:46.016655','2021-02-22 23:07:46.016676',1,1,NULL,NULL,13,16),(23,NULL,'2021-02-22 23:07:46.018151','2021-02-22 23:07:46.018171',2,1,NULL,NULL,13,18),(24,NULL,'2021-02-22 23:07:46.019488','2021-02-22 23:07:46.019508',3,1,NULL,NULL,13,19),(25,NULL,'2021-02-22 23:07:46.021068','2021-02-22 23:07:46.021089',4,1,NULL,NULL,13,21),(26,NULL,'2021-02-22 23:07:46.022496','2021-02-22 23:07:46.022516',5,1,NULL,NULL,13,25),(27,NULL,'2021-02-22 23:07:46.023979','2021-02-22 23:07:46.023999',6,1,NULL,NULL,13,23),(28,NULL,'2021-02-23 11:26:08.663715','2021-02-23 11:26:08.663735',7,1,NULL,NULL,14,21);
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
INSERT INTO `login_customuser` VALUES (1,NULL,'2021-02-22 16:18:31.007103','2021-02-22 21:42:27.026224',1,1,NULL,NULL,NULL,NULL,1),(2,NULL,'2021-02-23 13:44:39.932919','2021-02-23 13:44:40.092301',2,1,NULL,NULL,'','sadf',2);
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
INSERT INTO `main_functions_config` VALUES (1,'Почта обратной связи','flatcontent_feedback','dkramorov@mail.ru','2021-02-22 16:22:10.534449',NULL,1,NULL,1,NULL,'2021-02-22 16:22:10.534472',NULL);
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
INSERT INTO `personal_shopper` VALUES (1,NULL,'2021-02-23 11:25:42.655905','2021-02-23 11:25:42.655924',1,1,NULL,NULL,'Гость',NULL,NULL,NULL,'dk@223-223.ru','8(122)1 332-112',NULL,NULL,NULL,NULL,NULL,NULL,'127.0.0.1');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_products`
--

LOCK TABLES `products_products` WRITE;
/*!40000 ALTER TABLE `products_products` DISABLE KEYS */;
INSERT INTO `products_products` VALUES (1,'21.jpg','2021-02-22 22:21:22.612166','2021-02-22 22:21:52.111110',1,1,NULL,'','Ваниль в стручках','','Индонезия','гр',NULL,950.00,880.00,'','Стручки натуральной ванили, влажность 25-35%. Самое высокое качество!','Стручки ванили -это древняя пряность и специя, которая применяется в производстве огромного количества продуктов.&nbsp;<br>Наше\r\n собственное производство гарантирует высочайшее качество продукта. \r\nНашими клиентами являются крупные сети ресторанов и производства пищевых\r\n продуктов.','1',NULL,880.00,880.00,NULL,NULL),(2,'442.png','2021-02-22 22:22:13.327882','2021-02-22 22:23:28.161197',2,1,NULL,'','Молотая ваниль','','Индонезия','гр',NULL,2150.00,1850.00,'','Молотая ваниль немного дешевле стручковой за счет того, что перемалывают некандиционые стручки ванили','Молотая ваниль очень долго сохраняет свои свойства в закрытой таре или пакете','2',NULL,1850.00,1850.00,NULL,NULL),(3,'114_ehkstrakt_vanili_rayner_s.jpg','2021-02-22 22:23:41.759510','2021-02-22 22:25:01.390727',3,1,NULL,'','Эстракт ванили','','Индонезия','гр',NULL,950.00,880.00,'','Экстракт натуральной ванили плотности X2, не пахнет спиртом.','Наш экстракт не содержит отдушек, глицерина, ароматизаторов, пищевых Е \r\nдобавок. Эта ароматная спиртовая вытяжка используется для кондитерских \r\nизделий, в производстве пива, мороженого и т.д. Классическая \r\nамериканская рецепура (CFR 169.175): этиловый спирт, вода, стручки \r\nванили, за что пользуется большим спросом у кондитерских фабрик. Имеются\r\n сертификаты соответствия.\r\n<br><br>Где можно применить экстракт в домашних условиях:<p>Пудинг, \r\nщербет, кексы, крем, торты, бисквиты, печенья, соусы, молочные коктейли,\r\n взбитые сливки, некоторые мясные блюда и гарниры.</p>','3',NULL,880.00,880.00,NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productscats`
--

LOCK TABLES `products_productscats` WRITE;
/*!40000 ALTER TABLE `products_productscats` DISABLE KEYS */;
INSERT INTO `products_productscats` VALUES (1,NULL,1,21),(2,NULL,2,21),(3,NULL,3,21),(4,NULL,2,13),(5,NULL,1,13),(6,NULL,3,13);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productsphotos`
--

LOCK TABLES `products_productsphotos` WRITE;
/*!40000 ALTER TABLE `products_productsphotos` DISABLE KEYS */;
INSERT INTO `products_productsphotos` VALUES (1,'440.jpg','2021-02-22 22:21:43.972348','2021-02-22 22:21:43.972373',1,1,NULL,NULL,NULL,1),(2,'441.jpg','2021-02-22 22:21:52.122148','2021-02-22 22:21:52.122169',2,1,NULL,NULL,NULL,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_orders`
--

LOCK TABLES `shop_orders` WRITE;
/*!40000 ALTER TABLE `shop_orders` DISABLE KEYS */;
INSERT INTO `shop_orders` VALUES (1,NULL,'2021-02-23 13:15:19.305798','2021-02-23 13:15:19.305826',1,1,2,NULL,NULL,5370.00,NULL,1,'','dk@223-223.ru','127.0.0.1','Гость','8(122)1 332-112',0.00,NULL,NULL,NULL),(2,NULL,'2021-02-23 13:17:37.866428','2021-02-23 13:17:37.866447',2,1,2,NULL,NULL,2730.00,NULL,1,'','dk@223-223.ru','127.0.0.1','Гость','8(122)1 332-112',0.00,NULL,NULL,NULL),(3,NULL,'2021-02-23 13:18:04.369356','2021-02-23 13:18:04.369394',3,1,2,NULL,NULL,2730.00,NULL,1,'','dk@223-223.ru','127.0.0.1','Гость','8(122)1 332-112',0.00,NULL,NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_purchases`
--

LOCK TABLES `shop_purchases` WRITE;
/*!40000 ALTER TABLE `shop_purchases` DISABLE KEYS */;
INSERT INTO `shop_purchases` VALUES (7,NULL,'2021-02-23 12:45:21.490715','2021-02-23 12:45:21.490738',1,1,NULL,NULL,1,'1','Ваниль в стручках',2,880.00,1,1,NULL,'Индонезия','гр',880.00,NULL,NULL,NULL),(8,NULL,'2021-02-23 12:45:22.455876','2021-02-23 12:45:22.455895',2,1,NULL,NULL,2,'2','Молотая ваниль',1,1850.00,1,1,NULL,'Индонезия','гр',1850.00,NULL,NULL,NULL),(9,NULL,'2021-02-23 12:45:23.107652','2021-02-23 12:45:23.107691',3,1,NULL,NULL,3,'3','Эстракт ванили',2,880.00,1,1,NULL,'Индонезия','гр',880.00,NULL,NULL,NULL),(10,NULL,'2021-02-23 13:17:28.978829','2021-02-23 13:17:28.978847',4,1,NULL,NULL,1,'1','Ваниль в стручках',1,880.00,2,1,NULL,'Индонезия','гр',880.00,NULL,NULL,NULL),(11,NULL,'2021-02-23 13:17:29.506835','2021-02-23 13:17:29.506854',5,1,NULL,NULL,2,'2','Молотая ваниль',1,1850.00,2,1,NULL,'Индонезия','гр',1850.00,NULL,NULL,NULL),(12,NULL,'2021-02-23 13:18:00.050282','2021-02-23 13:18:00.050301',6,1,NULL,NULL,1,'1','Ваниль в стручках',1,880.00,3,1,NULL,'Индонезия','гр',880.00,NULL,NULL,NULL),(13,NULL,'2021-02-23 13:18:00.646231','2021-02-23 13:18:00.646249',7,1,NULL,NULL,2,'2','Молотая ваниль',1,1850.00,3,1,NULL,'Индонезия','гр',1850.00,NULL,NULL,NULL),(16,NULL,'2021-02-23 13:40:04.958057','2021-02-23 13:40:04.958076',8,1,NULL,NULL,2,'2','Молотая ваниль',5,1850.00,NULL,1,NULL,'Индонезия','гр',1850.00,NULL,NULL,NULL);
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

-- Dump completed on 2021-02-23 13:44:55
