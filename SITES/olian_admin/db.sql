-- MySQL dump 10.13  Distrib 5.7.20, for osx10.11 (x86_64)
--
-- Host: localhost    Database: destino
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
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add user',3,'add_user'),(10,'Can change user',3,'change_user'),(11,'Can delete user',3,'delete_user'),(12,'Can view user',3,'view_user'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Админка - Настрока',6,'add_config'),(22,'Can change Админка - Настрока',6,'change_config'),(23,'Can delete Админка - Настрока',6,'delete_config'),(24,'Can view Админка - Настрока',6,'view_config'),(25,'Can add Админка - Задача',7,'add_tasks'),(26,'Can change Админка - Задача',7,'change_tasks'),(27,'Can delete Админка - Задача',7,'delete_tasks'),(28,'Can view Админка - Задача',7,'view_tasks'),(29,'Can add custom user',8,'add_customuser'),(30,'Can change custom user',8,'change_customuser'),(31,'Can delete custom user',8,'delete_customuser'),(32,'Can view custom user',8,'view_customuser'),(33,'Can add Стат.контет - Файлы',9,'add_files'),(34,'Can change Стат.контет - Файлы',9,'change_files'),(35,'Can delete Стат.контет - Файлы',9,'delete_files'),(36,'Can view Стат.контет - Файлы',9,'view_files'),(37,'Can add Стат.контент - Блоки',10,'add_blocks'),(38,'Can change Стат.контент - Блоки',10,'change_blocks'),(39,'Can delete Стат.контент - Блоки',10,'delete_blocks'),(40,'Can view Стат.контент - Блоки',10,'view_blocks'),(41,'Can add Стат.контент - Контейнеры',11,'add_containers'),(42,'Can change Стат.контент - Контейнеры',11,'change_containers'),(43,'Can delete Стат.контент - Контейнеры',11,'delete_containers'),(44,'Can view Стат.контент - Контейнеры',11,'view_containers'),(45,'Can add Стат.контент - Линковка меню к контейнерам',12,'add_linkcontainer'),(46,'Can change Стат.контент - Линковка меню к контейнерам',12,'change_linkcontainer'),(47,'Can delete Стат.контент - Линковка меню к контейнерам',12,'delete_linkcontainer'),(48,'Can view Стат.контент - Линковка меню к контейнерам',12,'view_linkcontainer'),(49,'Can add Товары - товар/услуга',13,'add_products'),(50,'Can change Товары - товар/услуга',13,'change_products'),(51,'Can delete Товары - товар/услуга',13,'delete_products'),(52,'Can view Товары - товар/услуга',13,'view_products'),(53,'Can add products cats',14,'add_productscats'),(54,'Can change products cats',14,'change_productscats'),(55,'Can delete products cats',14,'delete_productscats'),(56,'Can view products cats',14,'view_productscats'),(57,'Can add products photos',15,'add_productsphotos'),(58,'Can change products photos',15,'change_productsphotos'),(59,'Can delete products photos',15,'delete_productsphotos'),(60,'Can view products photos',15,'view_productsphotos'),(61,'Can add property',16,'add_property'),(62,'Can change property',16,'change_property'),(63,'Can delete property',16,'delete_property'),(64,'Can view property',16,'view_property'),(65,'Can add properties values',17,'add_propertiesvalues'),(66,'Can change properties values',17,'change_propertiesvalues'),(67,'Can delete properties values',17,'delete_propertiesvalues'),(68,'Can view properties values',17,'view_propertiesvalues'),(69,'Can add products properties',18,'add_productsproperties'),(70,'Can change products properties',18,'change_productsproperties'),(71,'Can delete products properties',18,'delete_productsproperties'),(72,'Can view products properties',18,'view_productsproperties'),(73,'Can add Пользователи - пользователь',19,'add_shopper'),(74,'Can change Пользователи - пользователь',19,'change_shopper'),(75,'Can delete Пользователи - пользователь',19,'delete_shopper'),(76,'Can view Пользователи - пользователь',19,'view_shopper'),(77,'Can add Магазин - Заказ',20,'add_orders'),(78,'Can change Магазин - Заказ',20,'change_orders'),(79,'Can delete Магазин - Заказ',20,'delete_orders'),(80,'Can view Магазин - Заказ',20,'view_orders'),(81,'Can add wish list',21,'add_wishlist'),(82,'Can change wish list',21,'change_wishlist'),(83,'Can delete wish list',21,'delete_wishlist'),(84,'Can view wish list',21,'view_wishlist'),(85,'Can add purchases',22,'add_purchases'),(86,'Can change purchases',22,'change_purchases'),(87,'Can delete purchases',22,'delete_purchases'),(88,'Can view purchases',22,'view_purchases'),(89,'Can add costs types',23,'add_coststypes'),(90,'Can change costs types',23,'change_coststypes'),(91,'Can delete costs types',23,'delete_coststypes'),(92,'Can view costs types',23,'view_coststypes'),(93,'Can add costs',24,'add_costs'),(94,'Can change costs',24,'change_costs'),(95,'Can delete costs',24,'delete_costs'),(96,'Can view costs',24,'view_costs');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$ZjVVLFsrWpii$S6Jtx0qQ7B3xx47UrT/VJIq/fb34lyO4nDs2lyFQDTA=','2020-06-26 13:45:23.325075',1,'jocker','','','dkramorov@mail.ru',1,1,'2020-06-22 15:53:51.486061'),(2,'pbkdf2_sha256$150000$VGo3wYhBTxNs$QCOiGn8ZHlQKrp4FvMTVhyi5Z6+Ja1wijiC7oKIZixE=',NULL,1,'ap','','','',1,1,'2020-06-25 01:55:42.237286'),(3,'pbkdf2_sha256$150000$56ATfZxW04B4$FNqDeN+L4WWo+H/LUUO8Z55lxrO2Ph633L9nnp7xzOE=',NULL,1,'alex','','','',1,1,'2020-06-25 01:56:18.487682');
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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(9,'files','files'),(10,'flatcontent','blocks'),(11,'flatcontent','containers'),(12,'flatcontent','linkcontainer'),(8,'login','customuser'),(6,'main_functions','config'),(7,'main_functions','tasks'),(19,'personal','shopper'),(24,'products','costs'),(23,'products','coststypes'),(13,'products','products'),(14,'products','productscats'),(15,'products','productsphotos'),(18,'products','productsproperties'),(17,'products','propertiesvalues'),(16,'products','property'),(5,'sessions','session'),(20,'shop','orders'),(22,'shop','purchases'),(21,'shop','wishlist');
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
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-06-22 15:53:48.808234'),(2,'contenttypes','0002_remove_content_type_name','2020-06-22 15:53:48.852334'),(3,'auth','0001_initial','2020-06-22 15:53:49.945073'),(4,'auth','0002_alter_permission_name_max_length','2020-06-22 15:53:50.050841'),(5,'auth','0003_alter_user_email_max_length','2020-06-22 15:53:50.067493'),(6,'auth','0004_alter_user_username_opts','2020-06-22 15:53:50.076761'),(7,'auth','0005_alter_user_last_login_null','2020-06-22 15:53:50.091652'),(8,'auth','0006_require_contenttypes_0002','2020-06-22 15:53:50.093700'),(9,'auth','0007_alter_validators_add_error_messages','2020-06-22 15:53:50.102376'),(10,'auth','0008_alter_user_username_max_length','2020-06-22 15:53:50.120396'),(11,'auth','0009_alter_user_last_name_max_length','2020-06-22 15:53:50.134899'),(12,'auth','0010_alter_group_name_max_length','2020-06-22 15:53:50.150404'),(13,'auth','0011_update_proxy_permissions','2020-06-22 15:53:50.158688'),(14,'files','0001_initial','2020-06-22 15:53:50.273672'),(15,'files','0002_auto_20191203_2054','2020-06-22 15:53:50.327061'),(16,'files','0003_auto_20200112_1717','2020-06-22 15:53:50.335150'),(17,'files','0004_auto_20200402_2127','2020-06-22 15:53:50.350419'),(18,'flatcontent','0001_initial','2020-06-22 15:53:50.966979'),(19,'flatcontent','0002_auto_20190825_1730','2020-06-22 15:53:51.218091'),(20,'flatcontent','0003_auto_20191203_2054','2020-06-22 15:53:51.251709'),(21,'flatcontent','0004_blocks_html','2020-06-22 15:53:51.276481'),(22,'flatcontent','0005_auto_20200112_1717','2020-06-22 15:53:51.307691'),(23,'flatcontent','0006_auto_20200314_1638','2020-06-22 15:53:51.313198'),(24,'flatcontent','0007_auto_20200402_2127','2020-06-22 15:53:51.403726'),(25,'flatcontent','0008_containers_class_name','2020-06-22 15:53:51.423634'),(26,'login','0001_initial','2020-06-22 15:53:51.675196'),(27,'main_functions','0001_initial','2020-06-22 15:53:52.074961'),(28,'main_functions','0002_auto_20191203_2052','2020-06-22 15:53:52.095914'),(29,'main_functions','0003_auto_20200407_1845','2020-06-22 15:53:52.313664'),(30,'personal','0001_initial','2020-06-22 15:53:52.554469'),(31,'personal','0002_auto_20200528_1642','2020-06-22 15:53:52.705027'),(32,'personal','0003_auto_20200616_1707','2020-06-22 15:53:52.715687'),(33,'personal','0004_shopper_ip','2020-06-22 15:53:52.736585'),(34,'products','0001_initial','2020-06-22 15:53:52.976637'),(35,'products','0002_productsphotos','2020-06-22 15:53:53.216032'),(36,'products','0003_auto_20200315_2217','2020-06-22 15:53:53.319404'),(37,'products','0004_auto_20200316_2329','2020-06-22 15:53:53.375480'),(38,'products','0005_auto_20200402_2127','2020-06-22 15:53:53.719657'),(39,'products','0006_auto_20200402_2351','2020-06-22 15:53:53.871280'),(40,'products','0007_property_ptype','2020-06-22 15:53:53.893889'),(41,'products','0008_property_code','2020-06-22 15:53:53.923071'),(42,'products','0009_property_measure','2020-06-22 15:53:53.946095'),(43,'sessions','0001_initial','2020-06-22 15:53:54.093124'),(44,'shop','0001_initial','2020-06-22 15:53:54.273105'),(45,'shop','0002_auto_20200618_0000','2020-06-22 15:53:54.541212'),(46,'shop','0003_auto_20200621_1346','2020-06-22 15:53:54.785968'),(47,'products','0010_auto_20200623_1629','2020-06-23 16:30:06.626208'),(48,'shop','0004_purchases_cost_type','2020-06-26 16:36:54.474437'),(49,'products','0011_auto_20200627_1353','2020-06-27 13:53:20.626731');
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
INSERT INTO `django_session` VALUES ('4us9m2uls0mq7499inzx4scj8cyxb3qe','NTdjYjZkOGNkMTJmOGU4MDAyMjQ1YjVhZWVlMjExMzVhYTBjNDM2Mjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjM2ODMxMmJjOTY2MDMwNGM5ODJhNDg1MWE2ZjY4ZGZhMjE1NDNhZjYifQ==','2020-07-06 20:47:41.676415'),('9cbxeo2eszcz1qfy23vohdfhygtrb6qo','YmQ4MDY1YTBhNDNkZGMwY2I0ZGFmMmE0ZmI0NTdlZjhhY2Q4YjY5Zjp7InNob3BwZXIiOnsiaWQiOjIsIm5hbWUiOiJcdTA0MTNcdTA0M2VcdTA0NDFcdTA0NDJcdTA0NGMiLCJmaXJzdF9uYW1lIjpudWxsLCJsYXN0X25hbWUiOm51bGwsIm1pZGRsZV9uYW1lIjpudWxsLCJlbWFpbCI6bnVsbCwicGhvbmUiOm51bGwsImFkZHJlc3MiOm51bGwsImxvZ2luIjpudWxsLCJkaXNjb3VudCI6bnVsbCwiYmFsYW5jZSI6bnVsbCwiaXAiOiIxMjcuMC4wLjEifSwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhcHBzLmxvZ2luLmJhY2tlbmQuTXlCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMzY4MzEyYmM5NjYwMzA0Yzk4MmE0ODUxYTZmNjhkZmEyMTU0M2FmNiJ9','2020-07-10 13:45:23.329421'),('t2sh63qzvwopkkrfde822ltjqqdtk2qh','MTZkOTEyNmZiMDM2NjQ2OTU0NmE1NDk0MGQxNDNiYzMxMDgzYzg2Nzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjM2ODMxMmJjOTY2MDMwNGM5ODJhNDg1MWE2ZjY4ZGZhMjE1NDNhZjYiLCJzaG9wcGVyIjp7ImlkIjoxLCJuYW1lIjoiXHUwNDEzXHUwNDNlXHUwNDQxXHUwNDQyXHUwNDRjIiwiZmlyc3RfbmFtZSI6bnVsbCwibGFzdF9uYW1lIjpudWxsLCJtaWRkbGVfbmFtZSI6bnVsbCwiZW1haWwiOm51bGwsInBob25lIjpudWxsLCJhZGRyZXNzIjpudWxsLCJsb2dpbiI6bnVsbCwiZGlzY291bnQiOm51bGwsImJhbGFuY2UiOm51bGwsImlwIjoiMTI3LjAuMC4xIn19','2020-07-09 01:34:29.598443');
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
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
INSERT INTO `flatcontent_blocks` VALUES (1,'1.jpg','2020-06-22 20:48:07.002701','2020-06-22 20:48:07.002725',1,1,3,'','Логотип','Добро пожаловать, на наш сайт','/','logo',1,0,NULL,NULL,NULL,NULL),(2,NULL,'2020-06-22 20:48:07.005584','2020-06-22 20:48:07.005605',2,1,3,'','Телефон',NULL,'tel:73952123321','phone',1,0,NULL,NULL,NULL,'+7(3952) 123-321'),(3,NULL,'2020-06-22 20:48:07.008526','2020-06-22 20:48:07.008549',3,1,3,'','Адрес',NULL,NULL,'address',1,0,NULL,NULL,NULL,'г. Иркутск ул. Советская 32а офис 5'),(4,NULL,'2020-06-22 20:48:07.013658','2020-06-22 20:48:07.013686',4,1,3,'','Email',NULL,NULL,'email',1,0,NULL,NULL,NULL,'test@test.ru'),(5,NULL,'2020-06-22 20:48:07.016695','2020-06-22 20:48:07.016719',5,1,3,'','Режим работы',NULL,NULL,'worktime',1,0,NULL,NULL,NULL,'пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 17:00'),(6,NULL,'2020-06-22 20:48:07.019450','2020-06-22 20:48:07.019472',6,1,3,'','Copyright',NULL,NULL,'copyright',1,0,NULL,NULL,NULL,'<p>&copy; 2020 Все права защищены</p>'),(7,NULL,'2020-06-22 20:48:07.022487','2020-06-22 20:48:07.022511',7,1,3,'','Сообщества',NULL,NULL,'social',1,0,NULL,NULL,NULL,NULL),(8,NULL,'2020-06-22 20:48:07.025590','2020-06-22 20:48:07.025617',8,1,3,'_7','instagram',NULL,NULL,'instagram',1,1,'instagram',NULL,NULL,NULL),(9,NULL,'2020-06-22 20:48:07.028613','2020-06-22 20:48:07.028635',9,1,3,'_7','vk',NULL,NULL,'vk',1,1,'vk',NULL,NULL,NULL),(10,NULL,'2020-06-22 20:48:07.031412','2020-06-22 20:48:07.031434',10,1,3,'_7','facebook',NULL,NULL,'facebook',1,1,'facebook',NULL,NULL,NULL),(11,NULL,'2020-06-22 20:48:07.034175','2020-06-22 20:48:07.034198',11,1,3,'_7','twitter',NULL,NULL,'twitter',1,1,'twitter',NULL,NULL,NULL),(12,NULL,'2020-06-22 20:48:07.042490','2020-06-22 21:24:34.453895',12,1,4,'','Главная','','/','_mainmenu_mainpage',2,0,'','','',''),(13,NULL,'2020-06-22 20:48:07.045203','2020-06-22 20:48:07.045225',13,1,4,'','Каталог',NULL,'/cat/','_mainmenu_catpage',2,0,NULL,NULL,NULL,NULL),(14,NULL,'2020-06-22 20:48:07.048902','2020-06-22 20:48:07.048931',14,1,4,'_13','Популярные товары',NULL,'/cat/populyarnye-tovary/','_mainmenu_catpage_popular',2,0,NULL,NULL,NULL,NULL),(15,NULL,'2020-06-22 20:48:07.052851','2020-06-22 20:48:07.052876',15,1,4,'_13','Новые товары',NULL,'/cat/novye-tovary/','_mainmenu_catpage_new',2,0,NULL,NULL,NULL,NULL),(16,NULL,'2020-06-22 20:48:07.057110','2020-06-22 20:48:07.057141',16,1,4,'_13','Товары со скидкой',NULL,'/cat/tovary-so-skidkoy/','_mainmenu_catpage_discount',2,0,NULL,NULL,NULL,NULL),(17,NULL,'2020-06-22 20:48:07.060885','2020-06-22 20:48:07.060907',17,1,4,'_13','Распродажа',NULL,'/cat/rasprodaja/','_mainmenu_catpage_sale',2,0,NULL,NULL,NULL,NULL),(18,NULL,'2020-06-22 20:48:07.063535','2020-06-22 20:48:07.063554',18,1,4,'','О нас',NULL,'/about/','_mainmenu_aboutpage',2,0,NULL,NULL,NULL,NULL),(19,NULL,'2020-06-22 20:48:07.066066','2020-06-22 20:48:07.066096',19,1,4,'','Услуги',NULL,'/services/','_mainmenu_servicespage',2,0,NULL,NULL,NULL,NULL),(20,NULL,'2020-06-22 20:48:07.068783','2020-06-22 20:48:07.068805',20,1,4,'','Контакты',NULL,'/feedback/','_mainmenu_feedbackpage',2,0,NULL,NULL,NULL,NULL),(21,NULL,'2020-06-22 20:48:07.071513','2020-06-22 20:48:07.071539',21,1,4,'','Каталог',NULL,'/cat/','_bottommenu_catpage',3,0,NULL,NULL,NULL,NULL),(22,NULL,'2020-06-22 20:48:07.075200','2020-06-22 20:48:07.075221',22,1,4,'_21','Популярные товары',NULL,'/cat/populyarnye-tovary/','_bottommenu_catpage_popular',3,0,NULL,NULL,NULL,NULL),(23,NULL,'2020-06-22 20:48:07.078519','2020-06-22 20:48:07.078540',23,1,4,'_21','Новые товары',NULL,'/cat/novye-tovary/','_bottommenu_catpage_new',3,0,NULL,NULL,NULL,NULL),(24,NULL,'2020-06-22 20:48:07.082059','2020-06-22 20:48:07.082081',24,1,4,'_21','Товары со скидкой',NULL,'/cat/tovary-so-skidkoy/','_bottommenu_catpage_discount',3,0,NULL,NULL,NULL,NULL),(25,NULL,'2020-06-22 20:48:07.086005','2020-06-22 20:48:07.086032',25,1,4,'_21','Распродажа',NULL,'/cat/rasprodaja/','_bottommenu_catpage_sale',3,0,NULL,NULL,NULL,NULL),(26,NULL,'2020-06-22 20:48:07.088924','2020-06-22 20:48:07.088958',26,1,4,'','О нас',NULL,'/about/','_bottommenu_aboutpage',3,0,NULL,NULL,NULL,NULL),(27,NULL,'2020-06-22 20:48:07.092148','2020-06-22 20:48:07.092169',27,1,4,'','Услуги',NULL,'/services/','_bottommenu_servicespage',3,0,NULL,NULL,NULL,NULL),(28,NULL,'2020-06-22 20:48:07.094710','2020-06-22 20:48:07.094729',28,1,4,'','Контакты',NULL,'/feedback/','_bottommenu_feedbackpage',3,0,NULL,NULL,NULL,NULL),(29,'16.jpg','2020-06-22 20:48:30.939265','2020-06-22 21:05:05.180843',29,1,1,'','26 пицц','','','',4,0,'','','','авторской ручной работы от 20 см до 40 см, от 199₽ до 819₽<br>'),(30,'190.jpg','2020-06-22 21:05:50.585041','2020-06-22 21:05:54.347914',30,1,1,'','Разнообразное меню','','','',4,0,'','','','пасты, салаты, десерты<br>'),(31,'16.jpg','2020-06-22 21:14:36.039831','2020-06-22 21:14:36.039853',29,1,1,'','26 пицц','','','',5,0,'','','','авторской ручной работы от 20 см до 40 см, от 199₽ до 819₽<br>'),(32,'190.jpg','2020-06-22 21:14:36.053437','2020-06-22 21:14:36.053464',30,1,1,'','Разнообразное меню','','','',5,0,'','','','пасты, салаты, десерты<br>'),(33,'icon-1.png','2020-06-22 21:18:23.529824','2020-06-22 21:21:06.843962',31,1,1,'','Бесплатная доставка','бесплатная доставка','','',6,0,'','','','при заказе от 800₽<br>'),(35,'icon-2.png','2020-06-22 21:19:41.848903','2020-06-22 21:21:13.822923',32,1,1,'','Подарки','подарки','','',6,0,'','','','каждая шестая пицца бесплатно<br>'),(36,'icon-3.png','2020-06-22 21:20:35.807698','2020-06-22 21:21:20.759117',33,1,1,'','Быстрый заказ','быстрый заказ','','',6,0,'','','','По телефону или через сайт<br>'),(37,'icon-1.png','2020-06-22 21:24:23.980287','2020-06-22 21:24:23.980307',31,1,1,'','Бесплатная доставка','бесплатная доставка','','',7,0,'','','','при заказе от 800₽<br>'),(38,'icon-2.png','2020-06-22 21:24:23.988934','2020-06-22 21:24:23.988957',32,1,1,'','Подарки','подарки','','',7,0,'','','','каждая шестая пицца бесплатно<br>'),(39,'icon-3.png','2020-06-22 21:24:24.006884','2020-06-22 21:24:24.006908',33,1,1,'','Быстрый заказ','быстрый заказ','','',7,0,'','','','По телефону или через сайт<br>'),(40,'item-1.jpg','2020-06-22 21:35:05.700219','2020-06-22 21:35:22.468469',34,1,1,'','Бренд1','бренд 1','','',8,0,'','','',''),(41,'item-2.jpg','2020-06-22 21:35:28.256197','2020-06-22 21:35:41.975082',35,1,1,'','Бренд2','бренд2','','',8,0,'','','',''),(42,'item-3.jpg','2020-06-22 21:35:49.056987','2020-06-22 21:35:57.199751',36,1,1,'','Бренд3','бренд3','','',8,0,'','','',''),(43,'item-4.jpg','2020-06-22 21:36:04.569231','2020-06-22 21:36:14.622281',37,1,1,'','Бренд4','бренд 4','','',8,0,'','','',''),(44,'item-5.jpg','2020-06-22 21:36:20.342100','2020-06-22 21:36:28.921332',38,1,1,'','Бренд5','бренд 5','','',8,0,'','','',''),(45,'item-6.jpg','2020-06-22 21:36:34.584845','2020-06-22 21:36:42.060417',39,1,1,'','Бренд6','бренд 6','','',8,0,'','','',''),(46,NULL,'2020-06-23 01:05:23.047205','2020-06-23 01:05:23.047226',40,1,4,'_27','Доставка',NULL,'/services/dostavka/',NULL,3,0,NULL,NULL,NULL,NULL),(47,NULL,'2020-06-23 01:05:39.426325','2020-06-23 01:05:39.426350',41,1,4,'_27','Заказ еды',NULL,'/services/zakaz-edy/',NULL,3,0,NULL,NULL,NULL,NULL),(48,NULL,'2020-06-23 01:05:47.718464','2020-06-23 01:05:47.718486',42,1,4,'_28','Наши адреса',NULL,'/feedback/nashi-adresa/',NULL,3,0,NULL,NULL,NULL,NULL),(49,NULL,'2020-06-23 01:05:52.493755','2020-06-23 01:05:52.493775',43,1,4,'_28','Написать нам',NULL,'/feedback/napisat-nam/',NULL,3,0,NULL,NULL,NULL,NULL),(50,NULL,'2020-06-23 01:06:00.104211','2020-06-23 01:06:00.104232',44,1,4,'_26','О компании',NULL,'/about/o-kompanii/',NULL,3,0,NULL,NULL,NULL,NULL),(51,NULL,'2020-06-23 01:06:05.374561','2020-06-23 01:06:05.374583',45,1,4,'_26','Сотрудничество',NULL,'/about/sotrudnichestvo/',NULL,3,0,NULL,NULL,NULL,NULL),(53,'2.png','2020-06-24 10:12:03.151685','2020-06-26 12:11:46.401321',60,1,4,'','Пицца',NULL,'/cat/picca/','cat_2',9,0,NULL,NULL,'picca',NULL),(54,'3.png','2020-06-24 10:12:04.294546','2020-06-26 12:11:47.463962',2,1,4,'','Салаты',NULL,'/cat/salaty/','cat_3',9,0,NULL,NULL,'salaty',NULL),(55,'4.png','2020-06-24 10:12:05.357207','2020-06-26 12:11:48.664640',4,1,4,'','Закуски',NULL,'/cat/zakuski/','cat_4',9,0,NULL,NULL,'zakuski',NULL),(56,'5.png','2020-06-24 10:12:06.575609','2020-06-26 12:11:49.847819',5,1,4,'','Десерты и напитки',NULL,'/cat/deserty-i-napitki/','cat_5',9,0,NULL,NULL,'deserty-i-napitki',NULL),(57,'7.png','2020-06-24 10:12:07.750913','2020-06-26 12:11:51.414407',1,1,4,'','Пасты',NULL,'/cat/pasty/','cat_7',9,0,NULL,NULL,'pasty',NULL),(58,'8.png','2020-06-24 10:12:08.932719','2020-06-26 12:11:52.602359',3,1,4,'','Супы или Soup','','/cat/supy-ili-soup/','cat_8',9,0,'',NULL,'supy-ili-soup','');
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
INSERT INTO `flatcontent_containers` VALUES (1,NULL,'2020-06-22 20:48:06.997342','2020-06-22 20:48:06.997378',1,1,2,NULL,'Контент для всех страничек','Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики','main',NULL,NULL),(2,NULL,'2020-06-22 20:48:07.036708','2020-06-22 20:48:07.036732',2,1,1,NULL,'Главное меню','Создано автоматически, выводит главное меню','mainmenu',NULL,NULL),(3,NULL,'2020-06-22 20:48:07.039651','2020-06-22 20:48:07.039676',3,1,1,NULL,'Нижнее меню','Создано автоматически, выводит нижнее меню','bottommenu',NULL,NULL),(4,NULL,'2020-06-22 20:48:24.295450','2020-06-22 20:48:24.295472',4,1,99,'','Слайдер','','slider','',''),(5,NULL,'2020-06-22 21:14:36.029623','2020-06-22 21:14:36.036133',5,1,3,'','Слайдер','','slider','',''),(6,NULL,'2020-06-22 21:18:14.047801','2020-06-22 21:18:14.047821',6,1,99,'','Преимущества','','advantages','',''),(7,NULL,'2020-06-22 21:24:23.946756','2020-06-22 21:24:23.976897',7,1,3,'','Преимущества','','advantages','',''),(8,NULL,'2020-06-22 21:34:48.512170','2020-06-22 21:34:48.512189',8,1,99,'','Карусель картинок','','img_carousel','',''),(9,NULL,'2020-06-23 00:40:41.388217','2020-06-24 11:42:58.281662',9,1,7,'','Меню ресторана','','catalogue','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_linkcontainer`
--

LOCK TABLES `flatcontent_linkcontainer` WRITE;
/*!40000 ALTER TABLE `flatcontent_linkcontainer` DISABLE KEYS */;
INSERT INTO `flatcontent_linkcontainer` VALUES (2,NULL,'2020-06-22 21:24:34.461432','2020-06-22 21:24:34.461452',1,1,NULL,NULL,12,5),(3,NULL,'2020-06-22 21:24:34.462600','2020-06-22 21:24:34.462617',2,1,NULL,NULL,12,7);
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
  KEY `login_customuser_img_6a17a9f3` (`img`),
  KEY `login_customuser_created_4a29e213` (`created`),
  KEY `login_customuser_updated_dc9f9081` (`updated`),
  KEY `login_customuser_position_33445dcc` (`position`),
  KEY `login_customuser_is_active_cccf2704` (`is_active`),
  KEY `login_customuser_state_f0a75add` (`state`),
  KEY `login_customuser_parents_3604d87b` (`parents`),
  KEY `login_customuser_phone_d456dd09` (`phone`),
  CONSTRAINT `login_customuser_user_id_70d7d409_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_customuser`
--

LOCK TABLES `login_customuser` WRITE;
/*!40000 ALTER TABLE `login_customuser` DISABLE KEYS */;
INSERT INTO `login_customuser` VALUES (1,NULL,'2020-06-22 15:53:51.646161','2020-06-26 13:45:23.327835',1,1,NULL,NULL,NULL,1),(2,NULL,'2020-06-25 01:55:38.484742','2020-06-25 01:55:42.239566',2,1,NULL,NULL,'',2),(3,NULL,'2020-06-25 01:56:14.535462','2020-06-25 01:56:18.521027',3,1,NULL,NULL,'',3);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personal_shopper`
--

LOCK TABLES `personal_shopper` WRITE;
/*!40000 ALTER TABLE `personal_shopper` DISABLE KEYS */;
INSERT INTO `personal_shopper` VALUES (1,NULL,'2020-06-25 01:34:29.583819','2020-06-25 01:34:29.583847',1,1,NULL,NULL,'Гость',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'127.0.0.1'),(2,NULL,'2020-06-26 13:45:05.069899','2020-06-26 13:45:05.069930',2,1,NULL,NULL,'Гость',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'127.0.0.1');
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
) ENGINE=InnoDB AUTO_INCREMENT=799 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_costs`
--

LOCK TABLES `products_costs` WRITE;
/*!40000 ALTER TABLE `products_costs` DISABLE KEYS */;
INSERT INTO `products_costs` VALUES (471,1,199.00,2,3),(472,1,469.00,3,3),(473,1,619.00,4,3),(474,1,769.00,5,3),(490,1,469.00,3,10),(491,1,619.00,4,10),(492,1,769.00,5,10),(506,1,229.00,2,15),(507,1,469.00,3,15),(508,1,619.00,4,15),(509,1,769.00,5,15),(536,1,199.00,2,14),(537,1,469.00,3,14),(538,1,619.00,4,14),(539,1,769.00,5,14),(546,1,519.00,3,7),(547,1,669.00,4,7),(548,1,819.00,5,7),(549,1,199.00,2,2),(550,1,449.00,3,2),(551,1,599.00,4,2),(552,1,749.00,5,2),(553,1,489.00,3,12),(554,1,639.00,4,12),(555,1,789.00,5,12),(616,1,489.00,3,5),(617,1,639.00,4,5),(618,1,789.00,5,5),(622,1,519.00,3,62),(623,1,669.00,4,62),(624,1,819.00,5,62),(631,1,199.00,2,4),(632,1,469.00,3,4),(633,1,619.00,4,4),(634,1,769.00,5,4),(638,1,469.00,3,57),(639,1,619.00,4,57),(640,1,769.00,5,57),(647,1,489.00,3,86),(648,1,639.00,4,86),(649,1,789.00,5,86),(662,1,469.00,3,85),(663,1,619.00,4,85),(664,1,769.00,5,85),(667,1,399.00,3,88),(671,1,99.00,3,91),(675,1,469.00,3,92),(676,1,619.00,4,92),(677,1,769.00,5,92),(690,1,519.00,3,94),(691,1,669.00,4,94),(692,1,819.00,5,94),(702,1,489.00,3,96),(703,1,639.00,4,96),(704,1,789.00,5,96),(708,1,469.00,3,97),(709,1,619.00,4,97),(710,1,769.00,5,97),(711,1,489.00,3,6),(712,1,639.00,4,6),(713,1,789.00,5,6),(714,1,489.00,3,8),(715,1,639.00,4,8),(716,1,789.00,5,8),(717,1,519.00,3,9),(718,1,669.00,4,9),(719,1,819.00,5,9),(720,1,519.00,3,11),(721,1,669.00,4,11),(722,1,819.00,5,11),(723,1,489.00,3,13),(724,1,639.00,4,13),(725,1,789.00,5,13),(726,1,519.00,3,16),(727,1,669.00,4,16),(728,1,819.00,5,16),(729,1,519.00,3,61),(730,1,669.00,4,61),(731,1,819.00,5,61),(732,1,589.00,3,63),(733,1,739.00,4,63),(734,1,889.00,5,63),(735,1,589.00,3,80),(736,1,739.00,4,80),(737,1,889.00,5,80),(762,NULL,519.00,3,115),(763,NULL,669.00,4,115),(764,NULL,819.00,5,115),(765,NULL,489.00,3,116),(766,NULL,639.00,4,116),(767,NULL,789.00,5,116),(768,NULL,489.00,3,117),(769,NULL,639.00,4,117),(770,NULL,789.00,5,117),(774,1,489.00,3,83),(775,1,639.00,4,83),(776,1,789.00,5,83),(786,1,489.00,3,93),(787,1,639.00,4,93),(788,1,789.00,5,93),(794,1,489.00,3,95),(795,1,639.00,4,95),(796,1,789.00,5,95),(797,1,399.00,3,89),(798,1,399.00,3,90);
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_coststypes`
--

LOCK TABLES `products_coststypes` WRITE;
/*!40000 ALTER TABLE `products_coststypes` DISABLE KEYS */;
INSERT INTO `products_coststypes` VALUES (2,NULL,'2020-06-23 22:42:35.441380','2020-06-26 12:11:11.997764',1,1,NULL,'','S-20 см',NULL,NULL),(3,NULL,'2020-06-23 22:42:35.485923','2020-06-26 12:11:12.012863',2,1,NULL,NULL,'M-30 см',NULL,NULL),(4,NULL,'2020-06-23 22:42:35.496003','2020-06-26 12:11:12.015797',3,1,NULL,NULL,'L-35 см',NULL,NULL),(5,NULL,'2020-06-23 22:42:35.498744','2020-06-26 12:11:12.018763',4,1,NULL,NULL,'XL-40 см',NULL,NULL);
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
  KEY `products_products_min_price_7cb1c282` (`min_price`)
) ENGINE=InnoDB AUTO_INCREMENT=123 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_products`
--

LOCK TABLES `products_products` WRITE;
/*!40000 ALTER TABLE `products_products` DISABLE KEYS */;
INSERT INTO `products_products` VALUES (2,'2.jpg','2020-06-23 22:51:55.897707','2020-06-27 14:03:22.364265',2,1,NULL,'','Маргарита','','','',NULL,NULL,NULL,'None','Свежие томаты, помидорки «Черри», вяленные томаты, сыр «Моцарелла», соус «Песто», фирменныйтоматный соус','','2',NULL,749.00,199.00),(3,'3.jpg','2020-06-23 22:51:56.316320','2020-06-27 14:03:22.371567',3,1,NULL,NULL,'Пепперони',NULL,NULL,NULL,NULL,NULL,NULL,'None','Итальянские колбаски «Пепперони», сыр «Моцарелла», фирменный томатный соус',NULL,'3',NULL,769.00,199.00),(4,'4.jpg','2020-06-23 22:51:56.722216','2020-06-27 14:03:22.374115',4,1,NULL,NULL,'Чикен Фунги',NULL,NULL,NULL,NULL,NULL,NULL,'None','Запечённая куриная грудка, свежие шампиньоны, сыр «Моцарелла», фирменный томатный соус',NULL,'4',NULL,769.00,199.00),(5,'5.jpg','2020-06-23 22:51:57.159939','2020-06-27 14:03:22.376684',5,1,NULL,NULL,'Мясная Де Люкс',NULL,NULL,NULL,NULL,NULL,NULL,'None','<div>Запечённая куриная грудка, ветчина, итальянские колбаски «Пепперони», бекон, молотые оливки,&nbsp;<span style=\"background-color: initial;\">сыр «Моцарелла», фирменный томатный соус',NULL,'5',NULL,789.00,489.00),(6,'6.jpg','2020-06-23 22:51:57.540318','2020-06-27 14:03:22.379335',6,1,NULL,NULL,'Диабло',NULL,NULL,NULL,NULL,NULL,NULL,'None','Итальянские колбаски «Пепперони», ветчина, свежие шампиньоны, острый перчик «Халапеньо», сыр «Моцарелла», фирменный томатный соус',NULL,'6',NULL,789.00,489.00),(7,'7.jpg','2020-06-23 22:51:57.924619','2020-06-27 14:03:22.382621',7,1,NULL,NULL,'Морской микс',NULL,NULL,NULL,NULL,NULL,NULL,'None','Микс из морепродуктов: мидии, мини осьминожки, кальмары, коктейльные креветки, королевскиекреветки, помидорки «Черри», руккола, сыр «Моцарелла», сыр «Пармезан», фирменный томатныйсоус',NULL,'7',NULL,819.00,519.00),(8,'8.jpg','2020-06-23 22:51:58.408082','2020-06-27 14:03:22.385570',8,1,NULL,NULL,'Чизбургер',NULL,NULL,NULL,NULL,NULL,NULL,'None','Запечённая куриная грудка, маринованный огурчик, свежие томаты, красный лук, сыр «Моцарелла», фирменный бургер соус',NULL,'8',NULL,789.00,489.00),(9,'9.jpg','2020-06-23 22:51:58.798475','2020-06-27 14:03:22.388248',9,1,NULL,NULL,'Прошутто',NULL,NULL,NULL,NULL,NULL,NULL,'None','Сырокопченое мясо, помидорки «Черри», каперсы, руккола, сыр «Моцарелла», сыр «Филадельфия», фирменный томатный соус',NULL,'9',NULL,819.00,519.00),(10,'10.jpg','2020-06-23 22:51:59.181084','2020-06-27 14:03:22.390880',10,1,NULL,NULL,'Аля-Карбонара',NULL,NULL,NULL,NULL,NULL,NULL,'None','Бекон, сыр «Моцарелла», сыр «Пармезан», соус «Песто», фирменный сливочно-чесночный соус',NULL,'10',NULL,769.00,469.00),(11,'11.jpg','2020-06-23 22:51:59.563394','2020-06-27 14:03:22.393520',11,1,NULL,NULL,'Итальяно',NULL,NULL,NULL,NULL,NULL,NULL,'None','Сырокопченая «Салями», сырокопченый бекон, помидорки «Черри», руккола, сыр «Моцарелла», сыр «Пармезан», фирменный сливочно-чесночный соус',NULL,'11',NULL,819.00,519.00),(12,'12.jpg','2020-06-23 22:51:59.943721','2020-06-27 14:03:22.396023',12,1,NULL,NULL,'4 Сыра',NULL,NULL,NULL,NULL,NULL,NULL,'None','Сыр «Моцарелла», сыр «Пармезан», сыр «Филадельфия», сыр «Дор блю», соус «Песто», сырныйсоус',NULL,'12',NULL,789.00,489.00),(13,'13.jpg','2020-06-23 22:52:00.353196','2020-06-27 14:03:22.398808',13,1,NULL,NULL,'Барбекю',NULL,NULL,NULL,NULL,NULL,NULL,'None','Бекон, охотничьи колбаски, свежие томаты, сыр «Моцарелла», «Барбекю» соус, фирменный томатный соус',NULL,'13',NULL,789.00,489.00),(14,'14.jpg','2020-06-23 22:52:00.761272','2020-06-27 14:03:22.401646',14,1,NULL,NULL,'Гавайская',NULL,NULL,NULL,NULL,NULL,NULL,'None','Запечённая куриная грудка, ветчина, ананасы, сыр «Моцарелла», фирменный томатный соус',NULL,'14',NULL,769.00,199.00),(15,'15.jpg','2020-06-23 22:52:01.140504','2020-06-27 14:03:22.404533',15,1,NULL,NULL,'Чикен Рейнч',NULL,NULL,NULL,NULL,NULL,NULL,'None','Запечённая куриная грудка, бекон, свежие томаты, сыр «Моцарелла», фирменный сливочно-чесночный соус',NULL,'15',NULL,769.00,229.00),(16,'16.jpg','2020-06-23 22:52:01.546806','2020-06-27 14:03:22.407281',16,1,NULL,NULL,'Филадельфия',NULL,NULL,NULL,NULL,NULL,NULL,'None','Филе п/к семги, помидорки «Черри», руккола, сыр «Моцарелла», сыр «Филадельфия», фирменный томатный соус',NULL,'16',NULL,819.00,519.00),(18,'18.jpg','2020-06-23 22:53:07.869747','2020-06-27 14:03:22.410280',28,1,NULL,NULL,'Пиццетты',NULL,NULL,NULL,NULL,NULL,99.00,NULL,'<p>Небольшие порционные закрытые пиццы (20 см), изготовленные из слоеного теста с добавленеим оливкого масла, что придаеет тесту особую мягкость.&nbsp;</p><p>Идеально для обеденного перерыва или вечером с аперитивом.</p><div><div><h3>Основа: соус из свежих томатов, сыр «Мацарелла» и начинка на выбор:</h3><div>.&nbsp;Итальянские колбаски «Пепперони»</div><div>.&nbsp;Свежие шампиньоны</div><div>.&nbsp;Запеченная курочка</div><div>.&nbsp;Томаты</div></div></div>',NULL,'18',NULL,99.00,99.00),(19,'19.jpg','2020-06-23 22:53:08.279483','2020-06-27 14:03:22.419523',32,1,NULL,NULL,'Нагетсы',NULL,NULL,'6 шт',NULL,NULL,140.00,NULL,'Нагетсы из куринногго филе, с хрустящей корочкой, приготовленные во фритюре',NULL,'19',NULL,140.00,140.00),(20,'20.jpg','2020-06-23 22:53:08.752908','2020-06-27 14:03:22.428506',33,1,NULL,NULL,'Картофель фри',NULL,NULL,'130 гр',NULL,NULL,80.00,NULL,'Картофель фри, приготовленный во фритюре',NULL,'20',NULL,80.00,80.00),(21,'21.jpg','2020-06-23 22:53:09.224449','2020-06-27 14:03:22.437495',35,1,NULL,NULL,'Картофель айдахо',NULL,NULL,'130 гр',NULL,NULL,90.00,NULL,'Картофельные дольки айдахо со специями, приготовленный во фритюре',NULL,'21',NULL,90.00,90.00),(22,'22.jpg','2020-06-23 22:53:09.703885','2020-06-27 14:03:22.440491',33,1,NULL,NULL,'Салат «с Охотничьими колбасками»',NULL,NULL,'300 гр',NULL,NULL,245.00,NULL,'Охотничьи колбаски и шампиньоны обжаренные на гриле, печеный картофель Айдахо, томаты, солёный огурчик, салатный лук, сливочно-грибной соус, зелёный лук<br>',NULL,'22',NULL,245.00,245.00),(23,'23.jpg','2020-06-23 22:53:10.034880','2020-06-27 14:03:22.443537',35,1,NULL,NULL,'Салат «Тюна»',NULL,NULL,'170 гр',NULL,NULL,295.00,NULL,'Мини стейки тунца, обжаренные на гриле, в сочетании с миксом салата Айсберг и рукколы, сыром «Пармезан», дольками яиц под медово-горчичной заправкой',NULL,'23',NULL,295.00,295.00),(24,'24.jpg','2020-06-23 22:53:10.343357','2020-06-27 14:03:22.446602',36,1,NULL,NULL,'Салат «Капрезе»',NULL,NULL,'185 гр',NULL,NULL,245.00,NULL,'Классическое сочетание помидорок «Черри» и «бейби-Моцареллы» с соусом «Песто», бальзамическим кремом и кедровыми орешками<br>',NULL,'24',NULL,245.00,245.00),(32,'32.jpg','2020-06-23 22:53:10.690082','2020-06-27 14:03:22.450142',45,1,NULL,NULL,'Морс брусника&малина 0,33L',NULL,NULL,NULL,NULL,NULL,45.00,NULL,NULL,NULL,'32',NULL,45.00,45.00),(33,'33.jpg','2020-06-23 22:53:11.018573','2020-06-27 14:03:22.453239',48,1,NULL,NULL,'Морс облепиха&корица 0,33L',NULL,NULL,NULL,NULL,NULL,45.00,NULL,NULL,NULL,'33',NULL,45.00,45.00),(40,'40.jpg','2020-06-23 22:53:11.556619','2020-06-27 14:03:22.456084',68,1,NULL,NULL,'Бон Аква газ. 0,5 пэт',NULL,NULL,NULL,NULL,NULL,55.00,NULL,NULL,NULL,'40',NULL,55.00,55.00),(41,'41.jpg','2020-06-23 22:53:11.807140','2020-06-27 14:03:22.458753',69,1,NULL,NULL,'Бон Аква не/газ 0,5 пэт',NULL,NULL,NULL,NULL,NULL,55.00,NULL,NULL,NULL,'41',NULL,55.00,55.00),(43,'43.jpg','2020-06-23 22:53:12.067606','2020-06-27 14:03:22.461403',52,1,NULL,NULL,'Кока кола 0,33 ж/б',NULL,NULL,NULL,NULL,NULL,60.00,NULL,NULL,NULL,'43',NULL,60.00,60.00),(44,'44.jpg','2020-06-23 22:53:12.344914','2020-06-27 14:03:22.464006',53,1,NULL,NULL,'Кока кола 0,5 пэт',NULL,NULL,NULL,NULL,NULL,85.00,NULL,NULL,NULL,'44',NULL,85.00,85.00),(45,'45.jpg','2020-06-23 22:53:12.593950','2020-06-27 14:03:22.467138',54,1,NULL,NULL,'Спрайт 0,33 ж/б',NULL,NULL,NULL,NULL,NULL,60.00,NULL,NULL,NULL,'45',NULL,60.00,60.00),(46,'46.jpg','2020-06-23 22:53:12.843853','2020-06-27 14:03:22.470779',55,1,NULL,NULL,'Спрайт 0,5 пэт',NULL,NULL,NULL,NULL,NULL,85.00,NULL,NULL,NULL,'46',NULL,85.00,85.00),(47,'47.jpg','2020-06-23 22:53:13.100781','2020-06-27 14:03:22.473822',56,1,NULL,NULL,'Фанта 0,33 ж/б',NULL,NULL,NULL,NULL,NULL,60.00,NULL,NULL,NULL,'47',NULL,60.00,60.00),(48,'48.jpg','2020-06-23 22:53:13.356810','2020-06-27 14:03:22.476462',57,1,NULL,NULL,'Фанта 0,5 пэт',NULL,NULL,NULL,NULL,NULL,85.00,NULL,NULL,NULL,'48',NULL,85.00,85.00),(49,'49.jpg','2020-06-23 22:53:13.614326','2020-06-27 14:03:22.479099',58,1,NULL,NULL,'Нести 0,33 зеленый цитрус ж/б',NULL,NULL,NULL,NULL,NULL,55.00,NULL,NULL,NULL,'49',NULL,55.00,55.00),(50,'50.jpg','2020-06-23 22:53:13.869912','2020-06-27 14:03:22.482088',59,1,NULL,NULL,'Нести 0,33 черный лимон ж/б',NULL,NULL,NULL,NULL,NULL,55.00,NULL,NULL,NULL,'50',NULL,55.00,55.00),(51,'51.jpg','2020-06-23 22:53:14.126323','2020-06-27 14:03:22.484735',62,1,NULL,NULL,'Нести зеленый клубника и малина 0,5 пэт',NULL,NULL,NULL,NULL,NULL,80.00,NULL,NULL,NULL,'51',NULL,80.00,80.00),(52,'52.jpg','2020-06-23 22:53:14.380775','2020-06-27 14:03:22.487547',63,1,NULL,NULL,'Нести персик 0,5 пэт',NULL,NULL,NULL,NULL,NULL,80.00,NULL,NULL,NULL,'52',NULL,80.00,80.00),(53,'53.jpg','2020-06-23 22:53:14.640073','2020-06-27 14:03:22.490413',64,1,NULL,NULL,'Нести черный с лесными ягодами 0,5 пэт',NULL,NULL,NULL,NULL,NULL,80.00,NULL,NULL,NULL,'53',NULL,80.00,80.00),(54,'54.jpg','2020-06-23 22:53:14.875405','2020-06-27 14:03:22.493185',65,1,NULL,NULL,'Палпи 0,5 апельсин пэт',NULL,NULL,NULL,NULL,NULL,85.00,NULL,NULL,NULL,'54',NULL,85.00,85.00),(55,'55.jpg','2020-06-23 22:53:15.138238','2020-06-27 14:03:22.495944',66,1,NULL,NULL,'Палпи 0,5 грейпфрут пэт',NULL,NULL,NULL,NULL,NULL,85.00,NULL,NULL,NULL,'55',NULL,85.00,85.00),(56,'56.jpg','2020-06-23 22:53:15.397119','2020-06-27 14:03:22.499140',67,1,NULL,NULL,'Палпи 0,5 тропик пэт',NULL,NULL,NULL,NULL,NULL,85.00,NULL,NULL,NULL,'56',NULL,85.00,85.00),(57,'57.jpg','2020-06-23 22:53:15.654788','2020-06-27 14:03:22.502218',17,1,NULL,NULL,'Грибной Микс',NULL,NULL,NULL,NULL,NULL,NULL,'None','Лесные грибы, свежие шампиньоны, красный лук, сыр «Моцарелла», фирменный сливочно-чесночный соус',NULL,'57',NULL,769.00,469.00),(61,'61.jpg','2020-06-23 22:53:16.057756','2020-06-27 14:03:22.504991',18,1,NULL,NULL,'С Ростбифом',NULL,NULL,NULL,NULL,NULL,NULL,'None','Ростбиф (запечённая говяжья вырезка), помидорки «Черри», болгарский перец, красный лук, сыр «Моцарелла», перечный соус, фирменный томатный соус',NULL,'61',NULL,819.00,519.00),(62,'62.jpg','2020-06-23 22:53:16.468141','2020-06-27 14:03:22.507802',19,1,NULL,NULL,'Микс ГРИЛЬ',NULL,NULL,NULL,NULL,NULL,NULL,'None','Микс из трех видов мяса: Ростбиф (запечённая говяжья вырезка), запечённая куриная грудка,сырокопченый бекон, помидорки «Черри», сыр «Моцарелла», фирменный томатный соус',NULL,'62',NULL,819.00,519.00),(63,'63.jpg','2020-06-23 22:53:16.874478','2020-06-27 14:03:22.510577',20,1,NULL,NULL,'Королевская',NULL,NULL,NULL,NULL,NULL,NULL,'None','Филе п/к семги, королевские креветки, помидорки «Черри», молотые оливки, сыр «Моцарелла», фирменный сливочно-чесночный соус',NULL,'63',NULL,889.00,589.00),(69,'69.jpg','2020-06-23 22:53:17.278627','2020-06-27 14:03:22.513277',46,1,NULL,NULL,'Морс брусника&малина 0,5L',NULL,NULL,NULL,NULL,NULL,75.00,NULL,NULL,NULL,'69',NULL,75.00,75.00),(70,'70.jpg','2020-06-23 22:53:17.605097','2020-06-27 14:03:22.516753',47,1,NULL,NULL,'Морс брусника&малина 1L',NULL,NULL,NULL,NULL,NULL,145.00,NULL,NULL,NULL,'70',NULL,145.00,145.00),(71,'71.jpg','2020-06-23 22:53:17.937010','2020-06-27 14:03:22.519826',49,1,NULL,NULL,'Морс облепиха&корица 0,5L',NULL,NULL,NULL,NULL,NULL,75.00,NULL,NULL,NULL,'71',NULL,75.00,75.00),(72,'72.jpg','2020-06-23 22:53:18.263228','2020-06-27 14:03:22.522578',50,1,NULL,NULL,'Морс облепиха&корица 1L',NULL,NULL,NULL,NULL,NULL,145.00,NULL,NULL,NULL,'72',NULL,145.00,145.00),(73,'73.jpg','2020-06-23 22:53:18.597632','2020-06-27 14:03:22.525207',34,1,NULL,NULL,'Салат «с Ростбифом»',NULL,NULL,'160 гр',NULL,NULL,295.00,NULL,'Запечённый ростбиф из мраморной говядины, сыр Пармезан на зеленой подушке из салата Айсберг и рукколы, салатный лук, под соусом «Песто», маслины<br>',NULL,'73',NULL,295.00,295.00),(74,'74.jpg','2020-06-23 22:53:18.926127','2020-06-27 14:03:22.527856',37,1,NULL,NULL,'Салат с курицей и грибами',NULL,NULL,'190 гр',NULL,NULL,245.00,NULL,'Куринная грудка и грибы шампиньоны обжаренные на гриле, сыр Пармезан, помидорки «Черри», салат Айсберг, соус «Песто»<br>',NULL,'74',NULL,245.00,245.00),(75,'75.jpg','2020-06-23 22:53:19.260833','2020-06-27 14:03:22.530559',43,1,NULL,NULL,'«Карбонара»',NULL,NULL,'280 гр',NULL,NULL,285.00,NULL,'Спагетти собственного приготовления, соус из сливок, бекон, яичный желток, итальянские травы, сыр «Пармезан»',NULL,'75',NULL,285.00,285.00),(76,'76.jpg','2020-06-23 22:53:19.595713','2020-06-27 14:03:22.533516',44,1,NULL,NULL,'«3 сыра»',NULL,NULL,'230 гр',NULL,NULL,285.00,NULL,'Спагетти собственного приготовления, сливочный соус на основе сыра «Горгонзола», сыр «Креметто», итальянские травы, сыр «Пармезан»<br>',NULL,'76',NULL,285.00,285.00),(77,'77.jpg','2020-06-23 22:53:19.920198','2020-06-27 14:03:22.536625',45,1,NULL,NULL,'«Шампиньоны и курица»',NULL,NULL,'300 гр',NULL,NULL,285.00,NULL,'Паппарделле собственного приготовления , сливочный соус, куриное филе, свежие шампиньоны, помидорки «Черри», итальянские травы, сыр «Пармезан»<br>',NULL,'77',NULL,285.00,285.00),(78,'78.jpg','2020-06-23 22:53:20.249157','2020-06-27 14:03:22.539606',46,1,NULL,NULL,'«С тигровыми креветками»',NULL,NULL,'240 гр',NULL,NULL,315.00,NULL,'Феттучини собственного приготовления, тигровые креветки, сливочный соус со шпинатом, помидорки «Черри», итальянские травы, сыр «Пармезан»<br>',NULL,'78',NULL,315.00,315.00),(79,'79.jpeg','2020-06-23 22:53:20.583053','2020-06-27 14:03:22.542583',31,1,NULL,NULL,'Крылышки Баффало',NULL,NULL,'220 гр',NULL,NULL,190.00,NULL,NULL,NULL,'79',NULL,190.00,190.00),(80,'80.jpg','2020-06-23 22:53:20.915125','2020-06-27 14:03:22.545491',21,1,NULL,NULL,'Форель & Авокадо',NULL,NULL,NULL,NULL,NULL,NULL,'None','Авокадо, филе форели с/с, помидорки «Черри», кедровые орешки, сыр «Креметто», сыр «Моцарелла», фирменный томатный соус',NULL,'80',NULL,889.00,589.00),(83,'83.jpg','2020-06-23 22:53:21.320888','2020-06-27 14:03:22.548660',23,1,NULL,NULL,'Цыпленок терияки',NULL,NULL,NULL,NULL,NULL,NULL,'None','Цыпленок, помидорки «Черри», болгарский перец, семена кунжута, сыр «Моцарелла», соус «Терияки», фирменный томатный соус',NULL,'83',NULL,789.00,489.00),(85,'85.jpg','2020-06-23 22:53:21.655751','2020-06-27 14:03:22.551948',27,1,NULL,NULL,'Греческая',NULL,NULL,NULL,NULL,NULL,NULL,'None','Свежие томаты, помидорки «Черри», болгарский перец, маслины, красный лук, руккола, сыр«Креметто», соус «Песто», фирменный томатный соус',NULL,'85',NULL,769.00,469.00),(86,'86.jpg','2020-06-23 22:53:22.125030','2020-06-27 14:03:22.554611',22,1,NULL,NULL,'Расколбас',NULL,NULL,NULL,NULL,NULL,NULL,'None','Итальянские колбаски «Пепперони», сырокопченая «Салями», ветчина, охотничьи колбаски, сыр«Моцарелла», фирменный томатный соус',NULL,'86',NULL,789.00,489.00),(88,'88.jpg','2020-06-23 22:53:22.527847','2020-06-27 14:03:22.557379',72,1,NULL,NULL,'Сибирский десерт',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'<p>Байкальская брусника, кедровые орехи, сгущеное молоко, ванильный соус на основе сливочно-твороженного сыра «Cremette»</p>',NULL,'88',NULL,399.00,399.00),(89,'89.jpg','2020-06-23 22:53:22.919247','2020-06-27 14:03:22.559988',73,1,NULL,NULL,'Бананароти',NULL,NULL,NULL,NULL,NULL,NULL,'None','<p>Бананы, клубника, шоколадный крем, лепестки миндаля,&nbsp;ванильный соус на основе сливочно-творожного сыра «Cremette»</p>',NULL,'89',NULL,399.00,399.00),(90,'90.jpg','2020-06-23 22:53:23.316070','2020-06-27 14:03:22.562543',74,1,NULL,NULL,'Тропикано',NULL,NULL,NULL,NULL,NULL,NULL,'None','<p>Манго, ананасы, шоколадный крем, маршмэллоу, кокосовая стружка,&nbsp;ванильный соус на основе сливочно-творожного сыра «Cremette»<br></p>',NULL,'90',NULL,399.00,399.00),(91,'91.jpg','2020-06-23 22:53:23.719070','2020-06-28 17:09:40.608990',34,1,NULL,'','Фокача','','','',NULL,NULL,NULL,'None','<p>Фокача с сыром «Пармезан», свежим розмарином, оливковым маслом</p>','','91',NULL,99.00,99.00),(92,'92.jpg','2020-06-23 22:53:24.124474','2020-06-27 14:03:22.568953',76,1,NULL,NULL,'Ветчина&Моцарелла',NULL,NULL,NULL,NULL,NULL,NULL,'None','<p>Ветчина, сыр «Моцарелла», фирменный соус из свежих томатов</p>',NULL,'92',NULL,769.00,469.00),(93,'93.jpg','2020-06-23 22:53:24.518969','2020-06-27 14:03:22.571928',77,1,NULL,NULL,'Жульен с цыпленком',NULL,NULL,NULL,NULL,NULL,NULL,'None','<p>Цыпленок, свежие шампиньоны, красный лук,сыр «Моцарелла», сливочно-грибной соус</p>',NULL,'93',NULL,789.00,489.00),(94,'94.jpg','2020-06-23 22:53:24.915282','2020-06-27 14:03:22.574598',78,1,NULL,NULL,'Двойная пепперони',NULL,NULL,NULL,NULL,NULL,NULL,'None','<p>Двойная порция двух видов итальянских колбасок «Пепперони», сыр «Моцарелла», фирменный соус из свежих томатов</p>',NULL,'94',NULL,819.00,519.00),(95,'95.jpg','2020-06-23 22:53:25.319886','2020-06-27 14:03:22.577186',79,1,NULL,NULL,'Чикен Хот',NULL,NULL,NULL,NULL,NULL,NULL,'None','<p>Запечённая куриная грудка, сырокопченая салями, помидорки «Черри», красный лук, острый перчик «Халапеньо», острый соус «Баффало», сыр «Моцарелла», фирменный соус из свежих томатов</p>',NULL,'95',NULL,789.00,489.00),(96,'96.jpg','2020-06-23 22:53:25.721138','2020-06-27 14:03:22.579718',80,1,NULL,NULL,'4 сезона',NULL,NULL,NULL,NULL,NULL,NULL,'None','<p>Итальянские колбаски «Пепперони», свежие томаты, запечённая куриная грудка, ветчина, сыр «Моцарелла», фирменный соус из свежих томатов</p>',NULL,'96',NULL,789.00,489.00),(97,'97.jpg','2020-06-23 22:53:26.120960','2020-06-27 14:03:22.582526',81,1,NULL,NULL,'Капрезе',NULL,NULL,NULL,NULL,NULL,NULL,'None','<p>Свежие томаты, руккола, сыр «Креметто», сыр «Моцарелла», песто соус, бальзамический соус, фирменный соус из свежих томатов</p>',NULL,'97',NULL,769.00,469.00),(98,'98.jpg','2020-06-23 22:53:26.519910','2020-06-27 14:03:22.585133',82,1,NULL,NULL,'Сheese палочки классические',NULL,NULL,'шт',NULL,NULL,80.00,NULL,NULL,NULL,'98',NULL,80.00,80.00),(99,'99.jpg','2020-06-23 22:53:26.924780','2020-06-27 14:03:22.587826',83,1,NULL,NULL,'Сheese палочки с вялеными томатами',NULL,NULL,'шт',NULL,NULL,90.00,NULL,NULL,NULL,'99',NULL,90.00,90.00),(100,'100.jpg','2020-06-23 22:53:27.298621','2020-06-27 14:03:22.590585',84,1,NULL,NULL,'Сheese палочки с Пепперони',NULL,NULL,'шт',NULL,NULL,90.00,NULL,NULL,NULL,'100',NULL,90.00,90.00),(101,'101.JPEG','2020-06-23 22:53:27.704004','2020-06-27 14:03:22.593463',85,1,NULL,NULL,'КОМБО «HOT»',NULL,NULL,'шт',NULL,NULL,1333.00,'None','<div></div><p></p><div>выгода 22% (на 5-8 человек)</div><div>3 фирменные авторские пиццы 30см+1л морса+3 соуса:&nbsp;</div><div>«4 сыра», «Прошутто», «Диабло»</div><div>*-акция ежедневная</div><div>*-действует при заказе на доставку</div><p></p><div></div>',NULL,'101',NULL,1333.00,1333.00),(102,'102.jpeg','2020-06-23 22:53:28.102813','2020-06-27 14:03:22.596282',86,1,NULL,NULL,'Сет Пепперонимания',NULL,NULL,'шт',NULL,NULL,1999.00,'None','<div></div><p></p><div>выгода 23% (на 10-15 человек)</div><div>5 пицц 30 см с итальянскими колбасками «Пепперони»+5 соусов:</div><div>«Диабло», «Мясная де люкс», «Расколбас», «Пепперони», «Двойная пепперони»</div><div>*-акция ежедневная</div><p></p><div></div>',NULL,'102',NULL,1999.00,1999.00),(103,'103.jpg','2020-06-23 22:53:28.491425','2020-06-27 14:03:22.599674',87,1,NULL,NULL,'«МЯСНОЕ КОМБО»',NULL,NULL,'шт',NULL,NULL,999.00,'None','<div></div><p></p><div>выгода 33% (на 5-8 человек)</div><div>3 мясные пиццы 30 см+ 3 соуса:</div><div>«Пепперони», «Карбонара», «Гавайская»</div><div>*-акция ежедневная</div><div>*накопительные наклейки не предоставляются&nbsp;</div><p></p><div></div>',NULL,'103',NULL,999.00,999.00),(104,'104.jpeg','2020-06-23 22:53:28.897024','2020-06-27 14:03:22.602797',88,1,NULL,NULL,'«СЛАДКОЕ КОМБО»',NULL,NULL,NULL,NULL,NULL,999.00,'None','<p></p><div>выгода 17% (на 5-8 человек)</div><div>3 сладкие пиццы 30см:</div><div>«Бананароти», «Тропикана», «Сибирский десерт»</div><div>*-акция ежедневная</div><p></p>',NULL,'104',NULL,999.00,999.00),(105,'105.jpg','2020-06-23 22:53:29.297070','2020-06-27 14:03:22.605700',29,1,NULL,NULL,'Комбо снэк «Пивная закуска»',NULL,NULL,'470 гр',NULL,NULL,560.00,NULL,'Луковые кольца 100 гр., Сырные палочки 120 гр., Крылышки «Баффало» 160 гр., Картофель Айдахо 100 гр., Гарлики 60 гр.<br>',NULL,'105',NULL,560.00,560.00),(106,'106.jpg','2020-06-23 22:53:29.625930','2020-06-27 14:03:22.609554',30,1,NULL,NULL,'Сырные палочки',NULL,NULL,'6 шт',NULL,NULL,199.00,NULL,NULL,NULL,'106',NULL,199.00,199.00),(107,'107.jpg','2020-06-23 22:53:29.960866','2020-06-27 14:03:22.612448',89,1,NULL,NULL,'Салат «с курицей и беконом»',NULL,NULL,'240 гр',NULL,NULL,295.00,NULL,'Куринная грудка и слайсы бекона обжаренные на гриле, солёные огурчики, лист салата Айсберг, сыр «Пармезан», помидорки «Черри», Оливково-бальзамическая заправка',NULL,'107',NULL,295.00,295.00),(108,'108.jpg','2020-06-23 22:53:30.296528','2020-06-27 14:03:22.616053',90,1,NULL,NULL,'Салат с «Форелью и Авокадо»',NULL,NULL,'150 гр',NULL,NULL,315.00,NULL,'Филе форели с/с, руккола, авокадо, свежие огурцы, помидорки «Черри», соус «Терияки», кунжутная посыпка',NULL,'108',NULL,315.00,315.00),(109,'109.jpg','2020-06-23 22:53:30.626631','2020-06-27 14:03:22.619161',41,1,NULL,NULL,'«Болоньезе»',NULL,NULL,'220 гр',NULL,NULL,295.00,NULL,'Спагетти собственного приготовления, томатный соус «Болоньезе» на основе из фарша мраморной говядины, итальянские травы, сыр «Пармезан»',NULL,'109',NULL,295.00,295.00),(110,'110.jpg','2020-06-23 22:53:30.954403','2020-06-27 14:03:22.621851',42,1,NULL,NULL,'«Сицилия»',NULL,NULL,'380 гр',NULL,NULL,305.00,NULL,'Спагетти собственного приготовления, томатный соус, филе кальмара, мидии в панцире, итальянские травы, сыр «Пармезан»<br>',NULL,'110',NULL,305.00,305.00),(111,'111.jpg','2020-06-23 22:53:31.289249','2020-06-27 14:03:22.624452',91,1,NULL,NULL,'«Лазанья»',NULL,NULL,'355 гр',NULL,NULL,355.00,NULL,'<div>Лазанья с начинкой из фарша мраморной говядины под корочкой сыра «Пармезан» и соусом «Бешамель»<br></div>',NULL,'111',NULL,355.00,355.00),(112,'112.jpg','2020-06-23 22:53:31.620050','2020-06-27 14:03:22.627052',92,1,NULL,NULL,'«Тыквенный» крем-суп',NULL,NULL,'230 гр',NULL,NULL,215.00,NULL,NULL,NULL,'112',NULL,215.00,215.00),(113,'113.jpg','2020-06-23 22:53:31.924707','2020-06-27 14:03:22.629638',93,1,NULL,NULL,'«Грибной» крем-суп',NULL,NULL,'240 гр',NULL,NULL,215.00,NULL,NULL,NULL,'113',NULL,215.00,215.00),(114,'114.jpg','2020-06-23 22:53:32.260993','2020-06-27 14:03:22.632584',94,1,NULL,NULL,'Томатный крем-суп с морепродуктами',NULL,NULL,'250 гр',NULL,NULL,285.00,NULL,NULL,NULL,'114',NULL,285.00,285.00),(115,'115.jpg','2020-06-23 22:53:32.603153','2020-06-27 14:03:22.635533',95,1,NULL,NULL,'Фирменная Мясная',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Фарш из мраморной говядины, сырокопченая «Салями», ветчина, помидорки «Черри», маринованный огурчик, красный лук, сыр «Моцарелла», фирменный томатный соус <br>',NULL,'115',NULL,819.00,519.00),(116,'116.jpg','2020-06-23 22:53:32.987948','2020-06-27 14:03:22.638300',96,1,NULL,NULL,'Чоризо',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Сырокопченая колбаска «Салями», сырокопченая колбаска «Пепперони», свежие шампиньоны, маслины, сыр «Моцарелла», фирменный томатный соус<br>',NULL,'116',NULL,789.00,489.00),(117,'117.JPG','2020-06-23 22:53:33.299504','2020-06-27 14:03:22.641178',97,1,NULL,NULL,'Болоньезе',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Фарш из мраморной говядины, томатный соус «Болоньезе», сыр «Моцарелла»',NULL,'117',NULL,789.00,489.00),(118,'118.jpg','2020-06-23 22:53:33.694526','2020-06-27 14:03:22.643998',60,1,NULL,NULL,'Чизкейк в ассортименте',NULL,NULL,'шт',NULL,NULL,140.00,NULL,'уточнить у оператора',NULL,'118',NULL,140.00,140.00),(119,'119.jpg','2020-06-23 22:53:34.033750','2020-06-27 14:03:22.646956',61,1,NULL,NULL,'Панакота',NULL,NULL,'шт',NULL,NULL,115.00,NULL,NULL,NULL,'119',NULL,115.00,115.00),(120,'120.jpg','2020-06-23 22:53:34.368801','2020-06-27 14:03:22.650623',51,1,NULL,NULL,'Молочный коктейль в ассортименте',NULL,NULL,'шт',NULL,NULL,110.00,NULL,'уточнить у оператора',NULL,'120',NULL,110.00,110.00),(121,'121.jpg','2020-06-23 22:53:34.696416','2020-06-27 14:03:22.653422',101,1,NULL,NULL,'НАБОР «ПИЦЦА ПАТИ»','ПИЦЦА ПАТИ',NULL,NULL,NULL,NULL,3899.00,NULL,'<div>выгода 23% (на 20-25 человек)</div><div>10 самых популярных пицц 30см+10 соусов:&nbsp;</div><div>«Чизбургер», «Барбекю», «Мясная Де Люкс», «Чикен Фуге», «Диабло», «4 сыра», «Чикен Рэнч», «Пепперони», «Маргарита», «Аля-Карбонара»</div><div>*-акция ежедневная</div><br>',NULL,'121',NULL,3899.00,3899.00),(122,'122.PNG','2020-06-23 22:53:35.027503','2020-06-27 14:03:22.656140',102,1,NULL,NULL,'«КОМБО 2020»','КОМБО 2020',NULL,NULL,NULL,NULL,999.00,'None','<div>выгода 35% (на 5-8 человек)</div><div>Новый комбо набор 2020 года</div><div>3 новые пиццы 30 см+3 соуса:</div><div>«Жульен с цыпленком», «Расколбас», «Ветчина&amp;Моцарелла»</div><div>*-акция ежедневная</div><div>*накопительные наклейки не предоставляются ⠀&nbsp;</div>',NULL,'122',NULL,999.00,999.00);
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
) ENGINE=InnoDB AUTO_INCREMENT=601 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productscats`
--

LOCK TABLES `products_productscats` WRITE;
/*!40000 ALTER TABLE `products_productscats` DISABLE KEYS */;
INSERT INTO `products_productscats` VALUES (322,53,3,9),(328,53,10,9),(333,53,15,9),(342,53,14,9),(345,53,7,9),(347,53,12,9),(368,53,5,9),(370,53,62,9),(373,53,4,9),(375,53,57,9),(380,53,86,9),(385,53,85,9),(387,53,88,9),(395,53,92,9),(399,53,94,9),(403,53,96,9),(405,53,97,9),(450,55,106,9),(453,55,20,9),(454,55,21,9),(458,54,24,9),(460,54,107,9),(461,54,108,9),(464,57,75,9),(469,58,112,9),(470,58,113,9),(471,58,114,9),(480,56,40,9),(481,56,41,9),(482,56,43,9),(483,56,44,9),(484,56,45,9),(485,56,46,9),(486,56,47,9),(487,56,48,9),(488,56,49,9),(489,56,50,9),(490,56,51,9),(491,56,52,9),(492,56,53,9),(493,56,54,9),(494,56,55,9),(495,56,56,9),(523,57,77,9),(524,57,109,9),(526,57,78,9),(527,54,74,9),(528,54,23,9),(531,55,105,9),(533,55,19,9),(536,54,22,9),(537,57,76,9),(539,55,79,9),(540,53,6,9),(541,53,8,9),(542,53,9,9),(543,53,11,9),(544,53,13,9),(545,53,16,9),(546,53,61,9),(547,53,63,9),(548,53,80,9),(549,54,73,9),(559,53,115,9),(560,53,116,9),(561,56,118,9),(562,56,119,9),(563,56,120,9),(564,56,32,9),(566,56,69,9),(568,56,33,9),(569,56,71,9),(571,53,117,9),(572,57,111,9),(574,53,83,9),(578,56,70,9),(579,56,72,9),(580,53,93,9),(581,53,103,9),(582,53,102,9),(583,53,104,9),(584,53,101,9),(585,53,121,9),(587,53,122,9),(588,57,110,9),(592,53,95,9),(593,53,89,9),(594,53,90,9),(596,53,2,NULL),(599,53,91,NULL),(600,55,91,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productsphotos`
--

LOCK TABLES `products_productsphotos` WRITE;
/*!40000 ALTER TABLE `products_productsphotos` DISABLE KEYS */;
INSERT INTO `products_productsphotos` VALUES (1,'-.jpg','2020-06-28 17:09:26.701470','2020-06-28 17:09:26.701497',1,1,NULL,NULL,NULL,91),(2,'domino-s-pizza.jpg','2020-06-28 17:09:40.663686','2020-06-28 17:09:40.663712',2,1,NULL,NULL,NULL,91);
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
) ENGINE=InnoDB AUTO_INCREMENT=495 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productsproperties`
--

LOCK TABLES `products_productsproperties` WRITE;
/*!40000 ALTER TABLE `products_productsproperties` DISABLE KEYS */;
INSERT INTO `products_productsproperties` VALUES (278,3,2),(279,3,7),(289,10,7),(298,15,2),(299,15,11),(316,14,11),(319,7,14),(320,2,2),(321,2,15),(322,12,2),(323,12,15),(353,5,2),(354,5,7),(355,5,11),(358,62,2),(359,62,7),(360,62,11),(365,4,2),(366,4,16),(367,4,11),(371,57,15),(372,57,16),(378,86,7),(383,85,15),(386,88,1),(387,88,17),(391,91,1),(394,92,1),(395,92,7),(403,94,1),(404,94,7),(405,94,18),(415,96,1),(416,96,7),(417,96,11),(420,97,1),(421,97,15),(444,6,2),(445,6,7),(446,6,16),(447,6,18),(448,8,11),(449,9,2),(450,9,7),(451,11,2),(452,11,7),(453,13,7),(454,16,2),(455,16,14),(456,61,7),(457,63,14),(458,80,14),(463,83,11),(470,93,1),(471,93,11),(472,103,19),(473,102,19),(474,104,19),(475,101,19),(476,121,19),(480,122,19),(488,95,1),(489,95,11),(490,95,18),(491,89,1),(492,89,17),(493,90,1),(494,90,17);
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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_propertiesvalues`
--

LOCK TABLES `products_propertiesvalues` WRITE;
/*!40000 ALTER TABLE `products_propertiesvalues` DISABLE KEYS */;
INSERT INTO `products_propertiesvalues` VALUES (1,NULL,'2020-06-24 10:15:51.028712','2020-06-26 12:11:54.057683',1,1,NULL,NULL,NULL,1,NULL),(2,NULL,'2020-06-24 10:15:51.034529','2020-06-26 12:11:54.059729',2,1,NULL,NULL,NULL,1,NULL),(7,NULL,'2020-06-24 10:15:51.037567','2020-06-26 12:11:54.061465',3,1,NULL,NULL,NULL,1,NULL),(11,NULL,'2020-06-24 10:15:51.040587','2020-06-26 12:11:54.063915',4,1,NULL,NULL,NULL,1,NULL),(14,NULL,'2020-06-24 10:15:51.043438','2020-06-26 12:11:54.065900',5,1,NULL,NULL,NULL,1,NULL),(15,NULL,'2020-06-24 10:15:51.046245','2020-06-26 12:11:54.067860',6,1,NULL,NULL,NULL,1,NULL),(16,NULL,'2020-06-24 10:15:51.049572','2020-06-26 12:11:54.069692',7,1,NULL,NULL,NULL,1,NULL),(17,NULL,'2020-06-24 10:15:51.053065','2020-06-26 12:11:54.071505',8,1,NULL,NULL,NULL,1,NULL),(18,NULL,'2020-06-24 10:15:51.056599','2020-06-26 12:11:54.073715',9,1,NULL,NULL,NULL,1,NULL),(19,NULL,'2020-06-24 10:15:51.059684','2020-06-26 12:11:54.075952',10,1,NULL,NULL,NULL,1,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_property`
--

LOCK TABLES `products_property` WRITE;
/*!40000 ALTER TABLE `products_property` DISABLE KEYS */;
INSERT INTO `products_property` VALUES (1,NULL,'2020-06-24 10:15:51.022889','2020-06-26 12:11:54.055052',1,1,NULL,NULL,'Свойства',4,'pizza',NULL);
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
  CONSTRAINT `shop_purchases_cost_type_id_29172c16_fk_products_coststypes_id` FOREIGN KEY (`cost_type_id`) REFERENCES `products_coststypes` (`id`),
  CONSTRAINT `shop_purchases_order_id_7309c2ce_fk_shop_orders_id` FOREIGN KEY (`order_id`) REFERENCES `shop_orders` (`id`),
  CONSTRAINT `shop_purchases_shopper_id_49fcf0ae_fk_personal_shopper_id` FOREIGN KEY (`shopper_id`) REFERENCES `personal_shopper` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_purchases`
--

LOCK TABLES `shop_purchases` WRITE;
/*!40000 ALTER TABLE `shop_purchases` DISABLE KEYS */;
INSERT INTO `shop_purchases` VALUES (11,NULL,'2020-06-29 00:26:22.184651','2020-06-29 00:26:22.184679',1,1,NULL,NULL,3,'3','Пепперони',1,199.00,NULL,2,NULL,NULL,NULL,199.00,2),(12,NULL,'2020-06-29 00:26:23.409077','2020-06-29 00:26:23.409099',2,1,NULL,NULL,10,'10','Аля-Карбонара',21,619.00,NULL,2,NULL,NULL,NULL,619.00,4),(13,NULL,'2020-06-29 00:26:25.390443','2020-06-29 00:26:25.390465',3,1,NULL,NULL,7,'7','Морской микс',3,669.00,NULL,2,NULL,NULL,NULL,669.00,4),(14,NULL,'2020-06-29 00:26:28.212539','2020-06-29 00:26:28.212560',4,1,NULL,NULL,106,'106','Сырные палочки',1,199.00,NULL,2,NULL,NULL,'6 шт',199.00,NULL),(15,NULL,'2020-06-29 00:26:28.841464','2020-06-29 00:26:28.841486',5,1,NULL,NULL,20,'20','Картофель фри',1,80.00,NULL,2,NULL,NULL,'130 гр',80.00,NULL);
/*!40000 ALTER TABLE `shop_purchases` ENABLE KEYS */;
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

-- Dump completed on 2020-06-29  0:30:40
