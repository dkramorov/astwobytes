-- MySQL dump 10.13  Distrib 5.7.34, for osx10.16 (x86_64)
--
-- Host: localhost    Database: appix
-- ------------------------------------------------------
-- Server version	5.7.36

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
) ENGINE=InnoDB AUTO_INCREMENT=114 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add user',3,'add_user'),(10,'Can change user',3,'change_user'),(11,'Can delete user',3,'delete_user'),(12,'Can view user',3,'view_user'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Админка - Настрока',6,'add_config'),(22,'Can change Админка - Настрока',6,'change_config'),(23,'Can delete Админка - Настрока',6,'delete_config'),(24,'Can view Админка - Настрока',6,'view_config'),(25,'Can add Админка - Задача',7,'add_tasks'),(26,'Can change Админка - Задача',7,'change_tasks'),(27,'Can delete Админка - Задача',7,'delete_tasks'),(28,'Can view Админка - Задача',7,'view_tasks'),(29,'Can add custom user',11,'add_customuser'),(30,'Can change custom user',11,'change_customuser'),(31,'Can delete custom user',11,'delete_customuser'),(32,'Can view custom user',11,'view_customuser'),(33,'Can add Стат.контет - Файл',12,'add_files'),(34,'Can change Стат.контет - Файл',12,'change_files'),(35,'Can delete Стат.контет - Файл',12,'delete_files'),(36,'Can view Стат.контет - Файл',12,'view_files'),(37,'Can add Стат.контент - Блоки',13,'add_blocks'),(38,'Can change Стат.контент - Блоки',13,'change_blocks'),(39,'Can delete Стат.контент - Блоки',13,'delete_blocks'),(40,'Can view Стат.контент - Блоки',13,'view_blocks'),(41,'Can add Стат.контент - Контейнеры',14,'add_containers'),(42,'Can change Стат.контент - Контейнеры',14,'change_containers'),(43,'Can delete Стат.контент - Контейнеры',14,'delete_containers'),(44,'Can view Стат.контент - Контейнеры',14,'view_containers'),(45,'Can add Стат.контент - Линковка меню к контейнерам',15,'add_linkcontainer'),(46,'Can change Стат.контент - Линковка меню к контейнерам',15,'change_linkcontainer'),(47,'Can delete Стат.контент - Линковка меню к контейнерам',15,'delete_linkcontainer'),(48,'Can view Стат.контент - Линковка меню к контейнерам',15,'view_linkcontainer'),(49,'Заполнение сео-полей',13,'seo_fields'),(50,'Can add captcha',16,'add_captcha'),(51,'Can change captcha',16,'change_captcha'),(52,'Can delete captcha',16,'delete_captcha'),(53,'Can view captcha',16,'view_captcha'),(54,'Can add Товары - товар/услуга',17,'add_products'),(55,'Can change Товары - товар/услуга',17,'change_products'),(56,'Can delete Товары - товар/услуга',17,'delete_products'),(57,'Can view Товары - товар/услуга',17,'view_products'),(58,'Can add products cats',18,'add_productscats'),(59,'Can change products cats',18,'change_productscats'),(60,'Can delete products cats',18,'delete_productscats'),(61,'Can view products cats',18,'view_productscats'),(62,'Can add products photos',19,'add_productsphotos'),(63,'Can change products photos',19,'change_productsphotos'),(64,'Can delete products photos',19,'delete_productsphotos'),(65,'Can view products photos',19,'view_productsphotos'),(66,'Can add property',20,'add_property'),(67,'Can change property',20,'change_property'),(68,'Can delete property',20,'delete_property'),(69,'Can view property',20,'view_property'),(70,'Can add properties values',21,'add_propertiesvalues'),(71,'Can change properties values',21,'change_propertiesvalues'),(72,'Can delete properties values',21,'delete_propertiesvalues'),(73,'Can view properties values',21,'view_propertiesvalues'),(74,'Can add products properties',22,'add_productsproperties'),(75,'Can change products properties',22,'change_productsproperties'),(76,'Can delete products properties',22,'delete_productsproperties'),(77,'Can view products properties',22,'view_productsproperties'),(78,'Can add costs types',23,'add_coststypes'),(79,'Can change costs types',23,'change_coststypes'),(80,'Can delete costs types',23,'delete_coststypes'),(81,'Can view costs types',23,'view_coststypes'),(82,'Can add costs',24,'add_costs'),(83,'Can change costs',24,'change_costs'),(84,'Can delete costs',24,'delete_costs'),(85,'Can view costs',24,'view_costs'),(86,'Can add property group',25,'add_propertygroup'),(87,'Can change property group',25,'change_propertygroup'),(88,'Can delete property group',25,'delete_propertygroup'),(89,'Can view property group',25,'view_propertygroup'),(90,'Can add Пользователи - пользователь',26,'add_shopper'),(91,'Can change Пользователи - пользователь',26,'change_shopper'),(92,'Can delete Пользователи - пользователь',26,'delete_shopper'),(93,'Can view Пользователи - пользователь',26,'view_shopper'),(94,'Can add Магазин - Заказ',27,'add_orders'),(95,'Can change Магазин - Заказ',27,'change_orders'),(96,'Can delete Магазин - Заказ',27,'delete_orders'),(97,'Can view Магазин - Заказ',27,'view_orders'),(98,'Can add Магазин - Покупки',29,'add_purchases'),(99,'Can change Магазин - Покупки',29,'change_purchases'),(100,'Can delete Магазин - Покупки',29,'delete_purchases'),(101,'Can view Магазин - Покупки',29,'view_purchases'),(102,'Can add Магазин - Транзакция',30,'add_transactions'),(103,'Can change Магазин - Транзакция',30,'change_transactions'),(104,'Can delete Магазин - Транзакция',30,'delete_transactions'),(105,'Can view Магазин - Транзакция',30,'view_transactions'),(106,'Can add Магазин - Промокод',31,'add_promocodes'),(107,'Can change Магазин - Промокод',31,'change_promocodes'),(108,'Can delete Магазин - Промокод',31,'delete_promocodes'),(109,'Can view Магазин - Промокод',31,'view_promocodes'),(110,'Can add Магазин - Доставка заказа',32,'add_ordersdelivery'),(111,'Can change Магазин - Доставка заказа',32,'change_ordersdelivery'),(112,'Can delete Магазин - Доставка заказа',32,'delete_ordersdelivery'),(113,'Can view Магазин - Доставка заказа',32,'view_ordersdelivery');
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$i0X7l5zZ4S6O$lgKisPwt18iqJPZ8H9oUR7OjCxz60YZPrsoidJu4sGs=','2022-03-11 10:11:12.560279',1,'jocker','','','dkramorov@mail.ru',1,1,'2020-08-17 11:04:14.956925'),(3,'pbkdf2_sha256$150000$UfxkWPVxVUSg$BD5Io4DV6HjZvFgBg5dUeATjQi/3cqdYSdbQxWI24t4=',NULL,1,'alex','','','',1,1,'2022-03-11 10:11:47.366861');
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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(12,'files','files'),(13,'flatcontent','blocks'),(14,'flatcontent','containers'),(15,'flatcontent','linkcontainer'),(11,'login','customuser'),(8,'login','extrafields'),(10,'login','extrainfo'),(9,'login','extravalues'),(16,'main_functions','captcha'),(6,'main_functions','config'),(7,'main_functions','tasks'),(26,'personal','shopper'),(24,'products','costs'),(23,'products','coststypes'),(17,'products','products'),(18,'products','productscats'),(19,'products','productsphotos'),(22,'products','productsproperties'),(21,'products','propertiesvalues'),(20,'products','property'),(25,'products','propertygroup'),(5,'sessions','session'),(27,'shop','orders'),(32,'shop','ordersdelivery'),(31,'shop','promocodes'),(29,'shop','purchases'),(30,'shop','transactions'),(28,'shop','wishlist');
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
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-08-17 11:04:13.518705'),(2,'contenttypes','0002_remove_content_type_name','2020-08-17 11:04:13.539116'),(3,'auth','0001_initial','2020-08-17 11:04:13.674839'),(4,'auth','0002_alter_permission_name_max_length','2020-08-17 11:04:13.886179'),(5,'auth','0003_alter_user_email_max_length','2020-08-17 11:04:13.921610'),(6,'auth','0004_alter_user_username_opts','2020-08-17 11:04:13.929944'),(7,'auth','0005_alter_user_last_login_null','2020-08-17 11:04:13.944400'),(8,'auth','0006_require_contenttypes_0002','2020-08-17 11:04:13.945744'),(9,'auth','0007_alter_validators_add_error_messages','2020-08-17 11:04:13.953217'),(10,'auth','0008_alter_user_username_max_length','2020-08-17 11:04:13.970571'),(11,'auth','0009_alter_user_last_name_max_length','2020-08-17 11:04:13.986761'),(12,'auth','0010_alter_group_name_max_length','2020-08-17 11:04:14.002915'),(13,'auth','0011_update_proxy_permissions','2020-08-17 11:04:14.013952'),(14,'files','0001_initial','2020-08-17 11:04:14.076652'),(15,'files','0002_auto_20191203_2054','2020-08-17 11:04:14.170816'),(16,'files','0003_auto_20200112_1717','2020-08-17 11:04:14.178426'),(17,'files','0004_auto_20200402_2127','2020-08-17 11:04:14.193436'),(18,'files','0005_auto_20200809_1025','2020-08-17 11:04:14.196373'),(19,'flatcontent','0001_initial','2020-08-17 11:04:14.327302'),(20,'flatcontent','0002_auto_20190825_1730','2020-08-17 11:04:14.572174'),(21,'flatcontent','0003_auto_20191203_2054','2020-08-17 11:04:14.606753'),(22,'flatcontent','0004_blocks_html','2020-08-17 11:04:14.632146'),(23,'flatcontent','0005_auto_20200112_1717','2020-08-17 11:04:14.661997'),(24,'flatcontent','0006_auto_20200314_1638','2020-08-17 11:04:14.667225'),(25,'flatcontent','0007_auto_20200402_2127','2020-08-17 11:04:14.736777'),(26,'flatcontent','0008_containers_class_name','2020-08-17 11:04:14.756621'),(27,'login','0001_initial','2020-08-17 11:04:15.131261'),(28,'main_functions','0001_initial','2020-08-17 11:04:15.378779'),(29,'main_functions','0002_auto_20191203_2052','2020-08-17 11:04:15.397201'),(30,'main_functions','0003_auto_20200407_1845','2020-08-17 11:04:15.606754'),(31,'sessions','0001_initial','2020-08-17 11:04:15.698329'),(32,'flatcontent','0009_blocks_class_name','2021-02-16 23:27:58.023693'),(33,'login','0002_auto_20200925_1007','2021-02-16 23:27:58.058380'),(34,'main_functions','0004_config_user','2021-02-16 23:27:58.096958'),(35,'flatcontent','0010_auto_20210430_1708','2021-05-12 09:27:34.741520'),(36,'main_functions','0005_auto_20210321_1210','2021-05-12 09:27:34.752523'),(37,'files','0006_auto_20210516_1530','2022-03-11 10:06:20.790228'),(38,'flatcontent','0011_auto_20210526_2033','2022-03-11 10:06:20.815908'),(39,'main_functions','0006_captcha','2022-03-11 10:06:20.842271'),(40,'personal','0001_initial','2022-03-11 11:14:53.516030'),(41,'personal','0002_auto_20200528_1642','2022-03-11 11:14:54.076601'),(42,'personal','0003_auto_20200616_1707','2022-03-11 11:14:54.113938'),(43,'personal','0004_shopper_ip','2022-03-11 11:14:54.167356'),(44,'personal','0005_shopper_phone_confirmed','2022-03-11 11:14:54.271394'),(45,'products','0001_initial','2022-03-11 11:14:54.391133'),(46,'products','0002_productsphotos','2022-03-11 11:14:54.986661'),(47,'products','0003_auto_20200315_2217','2022-03-11 11:14:55.305747'),(48,'products','0004_auto_20200316_2329','2022-03-11 11:14:55.440841'),(49,'products','0005_auto_20200402_2127','2022-03-11 11:14:55.698880'),(50,'products','0006_auto_20200402_2351','2022-03-11 11:14:56.317951'),(51,'products','0007_property_ptype','2022-03-11 11:14:56.393125'),(52,'products','0008_property_code','2022-03-11 11:14:56.460505'),(53,'products','0009_property_measure','2022-03-11 11:14:56.528604'),(54,'products','0010_auto_20200623_1629','2022-03-11 11:14:56.644542'),(55,'products','0011_auto_20200627_1353','2022-03-11 11:14:57.122265'),(56,'products','0012_auto_20201212_1449','2022-03-11 11:14:57.292169'),(57,'products','0013_property_search_facet','2022-03-11 11:14:57.417123'),(58,'products','0014_propertiesvalues_code','2022-03-11 11:14:57.492576'),(59,'products','0015_auto_20220122_1311','2022-03-11 11:14:57.619830'),(60,'products','0016_products_stock_info','2022-03-11 11:14:57.952708'),(61,'shop','0001_initial','2022-03-11 11:14:58.155754'),(62,'shop','0002_auto_20200618_0000','2022-03-11 11:14:59.213385'),(63,'shop','0003_auto_20200621_1346','2022-03-11 11:14:59.829454'),(64,'shop','0004_purchases_cost_type','2022-03-11 11:15:00.017805'),(65,'shop','0005_transactions','2022-03-11 11:15:00.112799'),(66,'shop','0006_auto_20200719_0003','2022-03-11 11:15:00.550964'),(67,'shop','0007_auto_20200719_0146','2022-03-11 11:15:01.081347'),(68,'shop','0008_auto_20201026_1359','2022-03-11 11:15:01.200895'),(69,'shop','0009_auto_20201212_1539','2022-03-11 11:15:01.286101'),(70,'shop','0010_auto_20210208_1858','2022-03-11 11:15:01.390632'),(71,'shop','0011_orders_external_number','2022-03-11 11:15:01.467062'),(72,'shop','0012_ordersdelivery','2022-03-11 11:15:01.544040'),(73,'shop','0013_auto_20210801_1636','2022-03-11 11:15:01.854815'),(74,'shop','0014_ordersdelivery_additional_data','2022-03-11 11:15:01.896440'),(75,'shop','0015_auto_20220123_2207','2022-03-11 11:15:01.946057');
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
INSERT INTO `django_session` VALUES ('1onbllg1fmb639uz2mryjan13rjplhzd','OTE3YzhlNTEyOTVlZGZmNjUyYzI0MDVjMzNhMGE0NDU0YzhiOTBlMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImVmN2M5MDAyOGVkNDRkMTE2OTQyMWY5MjVmMjk3MzAwZGI0NDBiODUifQ==','2022-03-25 10:11:12.568793'),('9thngq5pbs1wbxdtxh6l57nz7it6nu6h','OTE3YzhlNTEyOTVlZGZmNjUyYzI0MDVjMzNhMGE0NDU0YzhiOTBlMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImVmN2M5MDAyOGVkNDRkMTE2OTQyMWY5MjVmMjk3MzAwZGI0NDBiODUifQ==','2020-09-10 14:13:22.740363'),('cjf21cguon3euaqu1zcee0p4f6nrwh7l','OTE3YzhlNTEyOTVlZGZmNjUyYzI0MDVjMzNhMGE0NDU0YzhiOTBlMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImVmN2M5MDAyOGVkNDRkMTE2OTQyMWY5MjVmMjk3MzAwZGI0NDBiODUifQ==','2020-09-06 09:51:58.992906'),('i3s9nx825kxzjc52pdymxrmh73i60060','OTE3YzhlNTEyOTVlZGZmNjUyYzI0MDVjMzNhMGE0NDU0YzhiOTBlMzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImVmN2M5MDAyOGVkNDRkMTE2OTQyMWY5MjVmMjk3MzAwZGI0NDBiODUifQ==','2020-08-31 11:15:30.619275');
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
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
INSERT INTO `flatcontent_blocks` VALUES (1,'1.png','2020-08-17 11:14:59.124956','2020-08-17 11:14:59.124981',1,1,3,'','Логотип','Добро пожаловать, на наш сайт','/','logo',1,0,NULL,NULL,NULL,NULL,NULL),(2,NULL,'2020-08-17 11:14:59.133810','2020-08-17 11:14:59.133833',2,1,3,'','Телефон',NULL,'tel:73952123321','phone',1,0,NULL,NULL,NULL,'+7(3952) 123-321',NULL),(3,NULL,'2020-08-17 11:14:59.137113','2020-08-17 11:14:59.137136',3,1,3,'','Адрес',NULL,NULL,'address',1,0,NULL,NULL,NULL,'г. Иркутск ул. Советская 32а офис 5',NULL),(4,NULL,'2020-08-17 11:14:59.140102','2020-08-17 11:14:59.140127',4,1,3,'','Email',NULL,NULL,'email',1,0,NULL,NULL,NULL,'test@test.ru',NULL),(5,NULL,'2020-08-17 11:14:59.142887','2020-08-17 11:14:59.142908',5,1,3,'','Режим работы',NULL,NULL,'worktime',1,0,NULL,NULL,NULL,'пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 17:00',NULL),(6,NULL,'2020-08-17 11:14:59.145561','2020-08-17 11:14:59.145582',6,1,3,'','Copyright',NULL,NULL,'copyright',1,0,NULL,NULL,NULL,'<p>&copy; 2020 Все права защищены</p>',NULL),(7,NULL,'2020-08-17 11:14:59.148265','2020-08-17 11:14:59.148286',7,1,3,'','Сообщества',NULL,NULL,'social',1,0,NULL,NULL,NULL,NULL,NULL),(8,NULL,'2020-08-17 11:14:59.151062','2020-08-17 11:14:59.151084',8,1,3,'_7','instagram',NULL,NULL,'instagram',1,1,'instagram',NULL,NULL,NULL,NULL),(9,NULL,'2020-08-17 11:14:59.153924','2020-08-17 11:14:59.153946',9,1,3,'_7','vk',NULL,NULL,'vk',1,1,'vk',NULL,NULL,NULL,NULL),(10,NULL,'2020-08-17 11:14:59.157005','2020-08-17 11:14:59.157029',10,1,3,'_7','facebook',NULL,NULL,'facebook',1,1,'facebook',NULL,NULL,NULL,NULL),(11,NULL,'2020-08-17 11:14:59.159841','2020-08-17 11:14:59.159862',11,1,3,'_7','twitter',NULL,NULL,'twitter',1,1,'twitter',NULL,NULL,NULL,NULL),(12,NULL,'2020-08-17 11:14:59.167466','2020-08-23 10:22:16.737750',12,1,4,'','Главная','','/','_mainmenu_mainpage',2,0,'glass','','','',NULL),(13,NULL,'2020-08-17 11:14:59.170163','2020-08-17 11:14:59.170184',13,1,4,'','Каталог',NULL,'/cat/','_mainmenu_catpage',2,0,NULL,NULL,NULL,NULL,NULL),(14,NULL,'2020-08-17 11:14:59.173997','2020-08-17 11:14:59.174023',14,1,4,'_13','Популярные товары',NULL,'/cat/populyarnye-tovary/','_mainmenu_catpage_popular',2,0,NULL,NULL,NULL,NULL,NULL),(15,NULL,'2020-08-17 11:14:59.177510','2020-08-17 11:14:59.177532',15,1,4,'_13','Новые товары',NULL,'/cat/novye-tovary/','_mainmenu_catpage_new',2,0,NULL,NULL,NULL,NULL,NULL),(16,NULL,'2020-08-17 11:14:59.180964','2020-08-17 11:14:59.180988',16,1,4,'_13','Товары со скидкой',NULL,'/cat/tovary-so-skidkoy/','_mainmenu_catpage_discount',2,0,NULL,NULL,NULL,NULL,NULL),(17,NULL,'2020-08-17 11:14:59.184429','2020-08-17 11:14:59.184451',17,1,4,'_13','Распродажа',NULL,'/cat/rasprodaja/','_mainmenu_catpage_sale',2,0,NULL,NULL,NULL,NULL,NULL),(18,NULL,'2020-08-17 11:14:59.187632','2020-08-17 11:14:59.187660',18,1,4,'','О нас',NULL,'/about/','_mainmenu_aboutpage',2,0,NULL,NULL,NULL,NULL,NULL),(19,NULL,'2020-08-17 11:14:59.190529','2020-08-17 11:14:59.190552',19,1,4,'','Услуги',NULL,'/services/','_mainmenu_servicespage',2,0,NULL,NULL,NULL,NULL,NULL),(20,NULL,'2020-08-17 11:14:59.193256','2020-08-17 11:14:59.193277',20,1,4,'','Контакты',NULL,'/feedback/','_mainmenu_feedbackpage',2,0,NULL,NULL,NULL,NULL,NULL),(21,NULL,'2020-08-17 11:14:59.195982','2020-08-17 11:14:59.196005',21,1,4,'','Каталог',NULL,'/cat/','_bottommenu_catpage',3,0,NULL,NULL,NULL,NULL,NULL),(22,NULL,'2020-08-17 11:14:59.199502','2020-08-17 11:14:59.199523',22,1,4,'_21','Популярные товары',NULL,'/cat/populyarnye-tovary/','_bottommenu_catpage_popular',3,0,NULL,NULL,NULL,NULL,NULL),(23,NULL,'2020-08-17 11:14:59.202970','2020-08-17 11:14:59.202992',23,1,4,'_21','Новые товары',NULL,'/cat/novye-tovary/','_bottommenu_catpage_new',3,0,NULL,NULL,NULL,NULL,NULL),(24,NULL,'2020-08-17 11:14:59.206686','2020-08-17 11:14:59.206710',24,1,4,'_21','Товары со скидкой',NULL,'/cat/tovary-so-skidkoy/','_bottommenu_catpage_discount',3,0,NULL,NULL,NULL,NULL,NULL),(25,NULL,'2020-08-17 11:14:59.210193','2020-08-17 11:14:59.210214',25,1,4,'_21','Распродажа',NULL,'/cat/rasprodaja/','_bottommenu_catpage_sale',3,0,NULL,NULL,NULL,NULL,NULL),(26,NULL,'2020-08-17 11:14:59.212902','2020-08-17 11:14:59.212924',26,1,4,'','О нас',NULL,'/about/','_bottommenu_aboutpage',3,0,NULL,NULL,NULL,NULL,NULL),(27,NULL,'2020-08-17 11:14:59.215626','2020-08-17 11:14:59.215648',27,1,4,'','Услуги',NULL,'/services/','_bottommenu_servicespage',3,0,NULL,NULL,NULL,NULL,NULL),(28,NULL,'2020-08-17 11:14:59.218334','2020-08-17 11:14:59.218356',28,1,4,'','Контакты',NULL,'/feedback/','_bottommenu_feedbackpage',3,0,NULL,NULL,NULL,NULL,NULL),(29,NULL,'2020-08-17 11:54:37.160505','2020-08-17 12:35:52.978665',29,1,1,'','Слайд 1','Разработка сайтов, интернет-магазинов','/','',5,0,'','','','Современные технологии<br>digigal инструментов<br>',NULL),(30,NULL,'2020-08-17 11:54:41.667940','2020-08-17 12:35:46.836253',30,1,1,'','Слайд 2','Разработка сайтов, интернет-магазинов','/','',5,0,'','','','Современные технологии<br>digigal инструментов',NULL),(31,NULL,'2020-08-17 12:36:25.707889','2022-03-11 10:38:09.230316',29,1,1,'','Проектирование','Разработка сайтов, интернет-магазинов','/','',6,0,'','','','<div>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>Разработка и согласование\r\nвсех<br> разделов проектной\r\nдокументации\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n		</div>',''),(32,NULL,'2020-08-17 12:36:25.713974','2022-03-11 10:38:25.176947',30,1,1,'','Дизайн','Разработка сайтов, интернет-магазинов','/','',6,0,'','','','<div>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>Разработка и визуализация<br>\r\nдизайн-проектов\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n		</div>',''),(33,'1.jpg','2020-08-17 12:50:21.951218','2020-08-17 12:58:55.530121',31,1,1,'','ПОЧЕМУ НАС ВЫБИРАЮТ','Наше портфолио','/','',7,0,'','','','Каждый месяц мы стараемся улучшить наши результаты по рекламным кампаниям клиентов, постоянно предлагая и прорабатывая новые идеи, технология и площадки.С каждым годом рекламные площадки становятся все сложнее, а конкуренция растет. Все меняется. Если не быть на шаг впереди, то развивать бизнес становится достаточно тяжело.',NULL),(35,'1.jpg','2020-08-17 12:59:35.931963','2020-08-17 12:59:35.931992',31,1,1,'','ПОЧЕМУ НАС ВЫБИРАЮТ','Наше портфолио','/','',9,0,'','','','Каждый месяц мы стараемся улучшить наши результаты по рекламным кампаниям клиентов, постоянно предлагая и прорабатывая новые идеи, технология и площадки.С каждым годом рекламные площадки становятся все сложнее, а конкуренция растет. Все меняется. Если не быть на шаг впереди, то развивать бизнес становится достаточно тяжело.',NULL),(36,'1.jpg','2020-08-17 13:02:28.363398','2020-08-17 13:02:28.363423',31,1,1,'','ПОЧЕМУ НАС ВЫБИРАЮТ','Наше портфолио','/','',10,0,'','','','Каждый месяц мы стараемся улучшить наши результаты по рекламным кампаниям клиентов, постоянно предлагая и прорабатывая новые идеи, технология и площадки.С каждым годом рекламные площадки становятся все сложнее, а конкуренция растет. Все меняется. Если не быть на шаг впереди, то развивать бизнес становится достаточно тяжело.',NULL),(37,'1.jpg','2020-08-17 13:02:34.243829','2020-08-17 13:02:34.243859',31,1,1,'','ПОЧЕМУ НАС ВЫБИРАЮТ','Наше портфолио','/','',11,0,'','','','Каждый месяц мы стараемся улучшить наши результаты по рекламным кампаниям клиентов, постоянно предлагая и прорабатывая новые идеи, технология и площадки.С каждым годом рекламные площадки становятся все сложнее, а конкуренция растет. Все меняется. Если не быть на шаг впереди, то развивать бизнес становится достаточно тяжело.',NULL),(38,'icon-3.png','2020-08-17 13:06:14.493178','2020-08-17 13:07:42.645795',32,1,1,'','Работаем под ключ','','','',12,0,'','','','Проектируем решение специально для ваших нужд, вы получаете гибкий инструмент для ваших задач<br>',NULL),(39,'icon-2.png','2020-08-17 13:08:56.718450','2020-08-17 13:10:45.005389',33,1,1,'','Адаптивный дизайн','','','',12,0,'','','','Мы делаем адаптивные дизайны, что позволяет вашим пользователям комфортно пользотваться сайтом<br>',NULL),(40,'icon-1.png','2020-08-17 13:09:09.610539','2020-08-17 13:13:01.087438',34,1,1,'','Современный дизайн и стиль','','','',12,0,'','','','Мы придерживаемся совеременного дизайна и строго стиля, а также мы предоставляем возможность изменить это<br>',NULL),(41,'icon-4.png','2020-08-17 13:09:19.364629','2020-08-17 13:14:20.599860',35,1,1,'','Развитие и поддержка','','','',12,0,'','','','Мы занимаемся совпровождением продукта после ввода его в эксплуатацию, проект продолжает развиваться<br>',NULL),(43,'icon-3.png','2020-08-17 13:15:57.425786','2020-08-17 13:15:57.425811',32,1,1,'','Работаем под ключ','','','',13,0,'','','','Проектируем решение специально для ваших нужд, вы получаете гибкий инструмент для ваших задач<br>',NULL),(44,'icon-2.png','2020-08-17 13:15:57.427365','2020-08-17 13:15:57.427389',33,1,1,'','Адаптивный дизайн','','','',13,0,'','','','Мы делаем адаптивные дизайны, что позволяет вашим пользователям комфортно пользотваться сайтом<br>',NULL),(45,'icon-1.png','2020-08-17 13:15:57.434331','2020-08-17 13:15:57.434355',34,1,1,'','Современный дизайн и стиль','','','',13,0,'','','','Мы придерживаемся совеременного дизайна и строго стиля, а также мы предоставляем возможность изменить это<br>',NULL),(46,'icon-4.png','2020-08-17 13:15:57.441522','2020-08-17 13:15:57.441548',35,1,1,'','Развитие и поддержка','','','',13,0,'','','','Мы занимаемся совпровождением продукта после ввода его в эксплуатацию, проект продолжает развиваться<br>',NULL),(47,NULL,'2020-08-17 13:24:05.955453','2020-08-17 17:18:13.627378',36,1,1,'','Первый раздел','','','left',14,0,'','','','',NULL),(48,NULL,'2020-08-17 13:24:35.687067','2020-08-17 17:20:52.017462',37,1,1,'_47','Отличный дизайн','','','',14,0,'bullhorn','','','Индивидуальный дизайн под ключ<br>',NULL),(49,NULL,'2020-08-17 13:59:33.964309','2020-08-17 17:25:24.492816',38,1,1,'','Второй раздел (Изображения)','','','center',14,0,'','','','',NULL),(50,NULL,'2020-08-17 17:18:36.502943','2020-08-17 17:18:40.273250',39,1,1,'','Третий раздел','','','right',14,0,'','','','',NULL),(51,NULL,'2020-08-17 17:20:55.437722','2020-08-17 17:21:56.547011',40,1,1,'_47','Адаптивный дизайн','','','',14,0,'android','','','Для всех устройств контент можно просматривать комфортно благодаря адаптивности<br>',NULL),(52,NULL,'2020-08-17 17:22:03.906758','2020-08-17 17:23:14.278079',41,1,1,'_47','Технологии быстрых страничек','','','',14,0,'bitbucket','','','Мы предоставляем оптимизацию страничек, создаем быстрые странички<br>',NULL),(53,NULL,'2020-08-17 17:23:18.078157','2020-08-17 17:24:33.124197',42,1,1,'_47','Быстрое выполнение','','','',14,0,'calendar','','','Мы максимально быстро выполняем заказ без потерь в качестве выполнения работы<br>',NULL),(54,'54.png','2020-08-17 17:25:29.742519','2020-08-17 17:25:29.742541',43,1,1,'_49','Без названия',NULL,NULL,NULL,14,0,NULL,NULL,NULL,NULL,NULL),(55,'55.png','2020-08-17 17:30:12.728756','2020-08-17 17:30:12.728779',44,1,1,'_49','Без названия',NULL,NULL,NULL,14,0,NULL,NULL,NULL,NULL,NULL),(56,'56.png','2020-08-17 17:30:21.897534','2020-08-17 17:30:21.897555',45,1,1,'_49','Без названия',NULL,NULL,NULL,14,0,NULL,NULL,NULL,NULL,NULL),(57,NULL,'2020-08-17 17:30:32.530600','2020-08-17 17:32:07.339096',46,1,1,'_50','Экономия','','','',14,0,'money','','','Мы предлагаем выгодные предложения как для небольших, так и больших проектов<br>',NULL),(58,NULL,'2020-08-17 17:30:33.702263','2020-08-17 17:33:34.010388',47,1,1,'_50','Оптимизация','','','',14,0,'road','','','Мы профессионально занимаемся оптимизацией и предлагаем полный спект услуг по ней<br>',NULL),(59,NULL,'2020-08-17 17:30:34.881446','2020-08-17 17:34:19.453627',48,1,1,'_50','Поддержка','','','',14,0,'headphones','','','Вы всегда можете получить от нас консультацию по любым услугам<br>',NULL),(60,NULL,'2020-08-17 17:30:39.233887','2020-08-17 17:35:16.405744',49,1,1,'_50','Документация','','','',14,0,'book','','','Мы предоставляем возможность получить специальные текстовые и видео материалы<br>',NULL),(61,NULL,'2020-08-17 17:44:39.869492','2020-08-17 17:44:39.869515',36,1,1,'','Первый раздел','','','left',15,0,'','','','',NULL),(62,NULL,'2020-08-17 17:44:39.870361','2020-08-17 17:44:39.870386',37,1,1,'_61','Отличный дизайн','','','',15,0,'bullhorn','','','Индивидуальный дизайн под ключ<br>',NULL),(63,NULL,'2020-08-17 17:44:39.871539','2020-08-17 17:44:39.871565',40,1,1,'_61','Адаптивный дизайн','','','',15,0,'android','','','Для всех устройств контент можно просматривать комфортно благодаря адаптивности<br>',NULL),(64,NULL,'2020-08-17 17:44:39.872501','2020-08-17 17:44:39.872522',41,1,1,'_61','Технологии быстрых страничек','','','',15,0,'bitbucket','','','Мы предоставляем оптимизацию страничек, создаем быстрые странички<br>',NULL),(65,NULL,'2020-08-17 17:44:39.873273','2020-08-17 17:44:39.873293',42,1,1,'_61','Быстрое выполнение','','','',15,0,'calendar','','','Мы максимально быстро выполняем заказ без потерь в качестве выполнения работы<br>',NULL),(66,NULL,'2020-08-17 17:44:39.874083','2020-08-17 17:44:39.874102',38,1,1,'','Второй раздел (Изображения)','','','center',15,0,'','','','',NULL),(67,'54.png','2020-08-17 17:44:39.874854','2020-08-17 17:44:39.874875',43,1,1,'_66','Без названия',NULL,NULL,NULL,15,0,NULL,NULL,NULL,NULL,NULL),(68,'55.png','2020-08-17 17:44:39.878228','2020-08-17 17:44:39.878273',44,1,1,'_66','Без названия',NULL,NULL,NULL,15,0,NULL,NULL,NULL,NULL,NULL),(69,'56.png','2020-08-17 17:44:39.886092','2020-08-17 17:44:39.886113',45,1,1,'_66','Без названия',NULL,NULL,NULL,15,0,NULL,NULL,NULL,NULL,NULL),(70,NULL,'2020-08-17 17:44:39.893150','2020-08-17 17:44:39.893187',39,1,1,'','Третий раздел','','','right',15,0,'','','','',NULL),(71,NULL,'2020-08-17 17:44:39.899783','2020-08-17 17:44:39.899805',46,1,1,'_70','Экономия','','','',15,0,'money','','','Мы предлагаем выгодные предложения как для небольших, так и больших проектов<br>',NULL),(72,NULL,'2020-08-17 17:44:39.912176','2020-08-17 17:44:39.912230',47,1,1,'_70','Оптимизация','','','',15,0,'road','','','Мы профессионально занимаемся оптимизацией и предлагаем полный спект услуг по ней<br>',NULL),(73,NULL,'2020-08-17 17:44:39.919467','2020-08-17 17:44:39.919506',48,1,1,'_70','Поддержка','','','',15,0,'headphones','','','Вы всегда можете получить от нас консультацию по любым услугам<br>',NULL),(74,NULL,'2020-08-17 17:44:39.921044','2020-08-17 17:44:39.921094',49,1,1,'_70','Документация','','','',15,0,'book','','','Мы предоставляем возможность получить специальные текстовые и видео материалы<br>',NULL),(75,NULL,'2020-08-17 17:48:39.111926','2020-08-17 17:48:44.905018',50,1,1,'','Видос','','https://www.youtube.com/watch?v=apQvhu9TUnY','',16,0,'','','','',NULL),(76,NULL,'2020-08-17 17:49:04.928510','2020-08-17 17:49:04.928543',50,1,1,'','Видос','','https://www.youtube.com/watch?v=apQvhu9TUnY','',17,0,'','','','',NULL),(77,NULL,'2020-08-23 09:52:59.460197','2020-08-23 09:57:59.046743',51,1,1,'','Обычный','1000','','',18,0,'','','','Визитка<br>',NULL),(78,NULL,'2020-08-23 09:53:03.888296','2020-08-23 10:03:18.368064',52,1,1,'','Про','2000','','',18,0,'','','Рекомендуем','Каталог',NULL),(79,NULL,'2020-08-23 09:53:07.757086','2020-08-23 09:58:32.920232',53,1,1,'','Премиум','3000','','',18,0,'','','','Магазин<br>',NULL),(80,NULL,'2020-08-23 09:58:57.520422','2020-08-23 09:59:09.749181',54,1,1,'_77','Хостинг','','','',18,0,'','','','',NULL),(81,NULL,'2020-08-23 09:59:12.371954','2020-08-23 09:59:17.256601',55,1,1,'_77','Домен','','','',18,0,'','','','',NULL),(82,NULL,'2020-08-23 09:59:21.888959','2020-08-23 09:59:33.556407',56,1,1,'_77','10Gb диск','','','',18,0,'','','','',NULL),(83,NULL,'2020-08-23 09:59:36.953181','2020-08-23 09:59:40.239230',57,1,1,'_77','Дизайн','','','',18,0,'','','','',NULL),(84,NULL,'2020-08-23 09:59:50.040190','2020-08-23 09:59:50.040212',58,1,1,'_78','Хостинг',NULL,NULL,NULL,18,0,NULL,NULL,NULL,NULL,NULL),(85,NULL,'2020-08-23 09:59:53.033753','2020-08-23 09:59:53.033774',59,1,1,'_78','Домен',NULL,NULL,NULL,18,0,NULL,NULL,NULL,NULL,NULL),(86,NULL,'2020-08-23 10:00:02.543527','2020-08-23 10:00:02.543555',60,1,1,'_78','20Gb диск',NULL,NULL,NULL,18,0,NULL,NULL,NULL,NULL,NULL),(87,NULL,'2020-08-23 10:00:06.269649','2020-08-23 10:00:06.269671',61,1,1,'_78','Дизайн',NULL,NULL,NULL,18,0,NULL,NULL,NULL,NULL,NULL),(88,NULL,'2020-08-23 10:00:11.546290','2020-08-23 10:00:11.546312',62,1,1,'_78','Панель управления',NULL,NULL,NULL,18,0,NULL,NULL,NULL,NULL,NULL),(89,NULL,'2020-08-23 10:00:15.867239','2020-08-23 10:00:15.867261',63,1,1,'_79','Хостинг',NULL,NULL,NULL,18,0,NULL,NULL,NULL,NULL,NULL),(90,NULL,'2020-08-23 10:00:19.421590','2020-08-23 10:00:19.421610',64,1,1,'_79','Домен',NULL,NULL,NULL,18,0,NULL,NULL,NULL,NULL,NULL),(91,NULL,'2020-08-23 10:00:27.870171','2020-08-23 10:00:27.870193',65,1,1,'_79','30Gb диск',NULL,NULL,NULL,18,0,NULL,NULL,NULL,NULL,NULL),(92,NULL,'2020-08-23 10:00:31.391767','2020-08-23 10:00:31.391793',66,1,1,'_79','Дизайн',NULL,NULL,NULL,18,0,NULL,NULL,NULL,NULL,NULL),(93,NULL,'2020-08-23 10:00:35.834148','2020-08-23 10:00:35.834169',67,1,1,'_79','Панель управления',NULL,NULL,NULL,18,0,NULL,NULL,NULL,NULL,NULL),(94,NULL,'2020-08-23 10:00:45.003725','2020-08-23 10:00:45.003746',68,1,1,'_79','Онлайн-оплата',NULL,NULL,NULL,18,0,NULL,NULL,NULL,NULL,NULL),(95,NULL,'2020-08-23 10:05:42.301154','2020-08-23 10:05:42.301174',51,1,1,'','Обычный','1000','','',19,0,'','','','Визитка<br>',NULL),(96,NULL,'2020-08-23 10:05:42.302549','2020-08-23 10:05:42.302568',54,1,1,'_95','Хостинг','','','',19,0,'','','','',NULL),(97,NULL,'2020-08-23 10:05:42.303363','2020-08-23 10:05:42.303386',55,1,1,'_95','Домен','','','',19,0,'','','','',NULL),(98,NULL,'2020-08-23 10:05:42.304326','2020-08-23 10:05:42.304345',56,1,1,'_95','10Gb диск','','','',19,0,'','','','',NULL),(99,NULL,'2020-08-23 10:05:42.305188','2020-08-23 10:05:42.305207',57,1,1,'_95','Дизайн','','','',19,0,'','','','',NULL),(100,NULL,'2020-08-23 10:05:42.305951','2020-08-23 10:05:42.305973',52,1,1,'','Про','2000','','',19,0,'','','Рекомендуем','Каталог',NULL),(101,NULL,'2020-08-23 10:05:42.308022','2020-08-23 10:05:42.308041',58,1,1,'_100','Хостинг',NULL,NULL,NULL,19,0,NULL,NULL,NULL,NULL,NULL),(102,NULL,'2020-08-23 10:05:42.308779','2020-08-23 10:05:42.308797',59,1,1,'_100','Домен',NULL,NULL,NULL,19,0,NULL,NULL,NULL,NULL,NULL),(103,NULL,'2020-08-23 10:05:42.309538','2020-08-23 10:05:42.309556',60,1,1,'_100','20Gb диск',NULL,NULL,NULL,19,0,NULL,NULL,NULL,NULL,NULL),(104,NULL,'2020-08-23 10:05:42.310348','2020-08-23 10:05:42.310370',61,1,1,'_100','Дизайн',NULL,NULL,NULL,19,0,NULL,NULL,NULL,NULL,NULL),(105,NULL,'2020-08-23 10:05:42.312686','2020-08-23 10:05:42.312709',62,1,1,'_100','Панель управления',NULL,NULL,NULL,19,0,NULL,NULL,NULL,NULL,NULL),(106,NULL,'2020-08-23 10:05:42.313486','2020-08-23 10:05:42.313504',53,1,1,'','Премиум','3000','','',19,0,'','','','Магазин<br>',NULL),(107,NULL,'2020-08-23 10:05:42.314254','2020-08-23 10:05:42.314272',63,1,1,'_106','Хостинг',NULL,NULL,NULL,19,0,NULL,NULL,NULL,NULL,NULL),(108,NULL,'2020-08-23 10:05:42.315090','2020-08-23 10:05:42.315115',64,1,1,'_106','Домен',NULL,NULL,NULL,19,0,NULL,NULL,NULL,NULL,NULL),(109,NULL,'2020-08-23 10:05:42.316043','2020-08-23 10:05:42.316076',65,1,1,'_106','30Gb диск',NULL,NULL,NULL,19,0,NULL,NULL,NULL,NULL,NULL),(110,NULL,'2020-08-23 10:05:42.317025','2020-08-23 10:05:42.317047',66,1,1,'_106','Дизайн',NULL,NULL,NULL,19,0,NULL,NULL,NULL,NULL,NULL),(111,NULL,'2020-08-23 10:05:42.317833','2020-08-23 10:05:42.317853',67,1,1,'_106','Панель управления',NULL,NULL,NULL,19,0,NULL,NULL,NULL,NULL,NULL),(112,NULL,'2020-08-23 10:05:42.318672','2020-08-23 10:05:42.318691',68,1,1,'_106','Онлайн-оплата',NULL,NULL,NULL,19,0,NULL,NULL,NULL,NULL,NULL),(113,NULL,'2020-08-23 10:09:25.614156','2020-08-23 10:09:44.799473',69,1,1,'','PlayStore','','','',20,0,'android','','','',NULL),(114,NULL,'2020-08-23 10:09:49.531341','2020-08-23 10:09:55.845805',70,1,1,'','ITunes','','','',20,0,'apple','','','',NULL),(115,NULL,'2020-08-23 10:11:33.523091','2020-08-23 10:11:33.523135',69,1,1,'','PlayStore','','','',21,0,'android','','','',NULL),(116,NULL,'2020-08-23 10:11:33.523970','2020-08-23 10:11:33.523988',70,1,1,'','ITunes','','','',21,0,'apple','','','',NULL),(117,NULL,'2020-08-27 14:33:54.771126','2020-08-27 14:33:54.771150',71,1,4,'','Информация',NULL,'/informaciya/',NULL,24,0,NULL,NULL,NULL,NULL,NULL),(118,NULL,'2020-08-27 14:34:00.995295','2020-08-27 14:34:08.819588',72,1,4,'','Статьи',NULL,'/bez-nazvaniya/',NULL,24,0,NULL,NULL,NULL,NULL,NULL),(119,NULL,'2020-08-27 14:34:13.556403','2020-08-27 14:34:13.556426',73,1,4,'_118','Как выбрать окна',NULL,'/bez-nazvaniya/kak-vybrat-okna/',NULL,24,0,NULL,NULL,NULL,NULL,NULL),(120,NULL,'2020-08-27 14:34:19.249758','2020-08-27 14:34:27.921017',74,1,4,'_118','Как выбрать кондиционер','','/bez-nazvaniya/bez-nazvaniya/','',24,0,'','','','',NULL),(121,NULL,'2020-08-27 14:34:33.186275','2020-08-27 14:34:41.353148',75,1,4,'_118','Как выбрать вентилляцию','','/bez-nazvaniya/kak-vybrat/','',24,0,'','','','',NULL),(122,NULL,'2020-08-27 14:34:58.399065','2020-08-27 14:34:58.399087',76,1,4,'_118','Остекление балкона',NULL,'/bez-nazvaniya/osteklenie-balkona/',NULL,24,0,NULL,NULL,NULL,NULL,NULL),(123,NULL,'2020-08-27 14:35:04.506899','2020-08-27 14:35:04.506922',77,1,4,'_117','Как сделать заказ',NULL,'/informaciya/kak-sdelat-zakaz/',NULL,24,0,NULL,NULL,NULL,NULL,NULL),(124,NULL,'2020-08-27 14:35:10.131119','2020-08-27 14:35:10.131142',78,1,4,'_117','Доставка',NULL,'/informaciya/dostavka/',NULL,24,0,NULL,NULL,NULL,NULL,NULL),(125,NULL,'2020-08-27 14:35:15.285763','2020-08-27 14:35:15.285785',79,1,4,'_117','Способы оплаты',NULL,'/informaciya/sposoby-oplaty/',NULL,24,0,NULL,NULL,NULL,NULL,NULL),(126,NULL,'2020-08-27 14:35:26.452630','2020-08-27 14:35:26.452651',80,1,4,'_117','Гарантия возврата',NULL,'/informaciya/garantiya-vozvrata/',NULL,24,0,NULL,NULL,NULL,NULL,NULL),(127,'blog-1.jpg','2020-08-27 15:21:53.156989','2020-08-27 15:53:52.635430',81,1,1,'','Какие приложения безопасны','','','',25,0,'','','','Небольшое описание, буквально пару предложений, чтобы осветить тему, которая будет развернута в статье, основная идея, чтобы заинтересовать пользователя<br>',NULL),(128,'blog-8.jpg','2020-08-27 15:22:07.089041','2020-08-27 15:53:57.212905',82,1,1,'','Полный комплекс разработки','','','',25,0,'','','','Небольшое описание, буквально пару предложений, чтобы осветить тему, \r\nкоторая будет развернута в статье, основная идея, чтобы заинтересовать \r\nпользователя',NULL),(129,'blog-3.jpg','2020-08-27 15:22:10.509660','2020-08-27 15:54:00.575865',83,1,1,'','Дизайн и стиль','','','',25,0,'','','','Небольшое описание, буквально пару предложений, чтобы осветить тему, \r\nкоторая будет развернута в статье, основная идея, чтобы заинтересовать \r\nпользователя',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
INSERT INTO `flatcontent_containers` VALUES (1,NULL,'2020-08-17 11:14:59.109163','2020-08-17 11:14:59.109201',1,1,2,NULL,'Контент для всех страничек','Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики','main',NULL,NULL),(2,NULL,'2020-08-17 11:14:59.162215','2020-08-17 11:14:59.162237',2,1,1,NULL,'Главное меню','Создано автоматически, выводит главное меню','mainmenu',NULL,NULL),(3,NULL,'2020-08-17 11:14:59.164706','2020-08-17 11:14:59.164729',3,1,1,NULL,'Нижнее меню','Создано автоматически, выводит нижнее меню','bottommenu',NULL,NULL),(4,NULL,'2020-08-17 11:16:50.287808','2020-08-17 11:16:50.287835',4,1,7,NULL,'Каталог товаров',NULL,'catalogue',NULL,NULL),(5,'5.jpg','2020-08-17 11:54:03.527727','2020-08-17 11:54:03.527749',5,1,99,'','Слайдер','','slider','',''),(6,'5.jpg','2020-08-17 12:36:25.690080','2022-03-11 10:23:08.851435',6,1,3,'','Слайдер','','slider','','main-slider-overlay2'),(7,NULL,'2020-08-17 12:49:40.692686','2020-08-17 12:50:16.097992',7,1,99,'','Статья','ВСЕ СКЛАДЫВАЕТСЯ ИЗ МЕЛОЧЕЙ<br>ЧТОБЫ ДОБИВАТЬСЯ РЕЗУЛЬТАТА НУЖНО ПОСТОЯННО РАБОТАТЬ НАД МЕЛОЧАМИ','article','',''),(9,NULL,'2020-08-17 12:59:35.926912','2020-08-17 12:59:42.136685',7,1,99,'','Статья (Вариант 2)','ВСЕ СКЛАДЫВАЕТСЯ ИЗ МЕЛОЧЕЙ<br>ЧТОБЫ ДОБИВАТЬСЯ РЕЗУЛЬТАТА НУЖНО ПОСТОЯННО РАБОТАТЬ НАД МЕЛОЧАМИ','article2','',''),(10,NULL,'2020-08-17 13:02:28.328261','2020-08-17 13:02:28.360928',8,1,3,'','Статья','ВСЕ СКЛАДЫВАЕТСЯ ИЗ МЕЛОЧЕЙ<br>ЧТОБЫ ДОБИВАТЬСЯ РЕЗУЛЬТАТА НУЖНО ПОСТОЯННО РАБОТАТЬ НАД МЕЛОЧАМИ','article','',''),(11,NULL,'2020-08-17 13:02:34.235819','2020-08-17 13:02:34.241658',9,1,3,'','Статья (Вариант 2)','ВСЕ СКЛАДЫВАЕТСЯ ИЗ МЕЛОЧЕЙ<br>ЧТОБЫ ДОБИВАТЬСЯ РЕЗУЛЬТАТА НУЖНО ПОСТОЯННО РАБОТАТЬ НАД МЕЛОЧАМИ','article2','',''),(12,NULL,'2020-08-17 13:05:46.210417','2020-08-17 13:05:46.210438',10,1,99,'','Преимущества','','advantages','',''),(13,NULL,'2020-08-17 13:15:57.417059','2020-08-17 13:15:57.423275',11,1,3,'','Преимущества','','advantages','',''),(14,NULL,'2020-08-17 13:17:48.014798','2020-08-17 13:19:29.578282',12,1,99,'','Премимущества (Вариант 2)','Невозможно быть идеальным, но мы стремимся к этому<br>','advantages2','',''),(15,NULL,'2020-08-17 17:44:39.830954','2020-08-17 17:44:39.866596',13,1,3,'','Премимущества (Вариант 2)','Невозможно быть идеальным, но мы стремимся к этому<br>','advantages2','',''),(16,NULL,'2020-08-17 17:48:31.831149','2020-08-17 17:48:31.831172',14,1,99,'','Видео','','video','',''),(17,NULL,'2020-08-17 17:49:04.920500','2020-08-17 17:49:04.926207',15,1,3,'','Видео','','video','',''),(18,NULL,'2020-08-23 09:52:46.747564','2020-08-23 09:52:46.747600',16,1,99,'','Тарифы','Выбирайте подходящий тариф, вы всегда можете прейти на более дорогой или дешевый<br>','tarif','',''),(19,NULL,'2020-08-23 10:05:42.290810','2020-08-23 10:05:42.297850',17,1,3,'','Тарифы','Выбирайте подходящий тариф, вы всегда можете прейти на более дорогой или дешевый<br>','tarif','',''),(20,NULL,'2020-08-23 10:08:45.699539','2020-08-23 10:09:15.097126',18,1,99,'','Заголовок (кнопки)','Вы также можете найти информацию и сделать заказ через приложения<br>','title','',''),(21,NULL,'2020-08-23 10:11:33.514897','2020-08-23 10:11:33.520880',19,1,3,'','Заголовок (кнопки)','Вы также можете найти информацию и сделать заказ через приложения<br>','title','',''),(22,NULL,'2020-08-23 10:16:43.160427','2020-08-23 10:18:02.405891',20,1,99,'','Написать нам','Мы с удовольствием примем от вас заявку через сайт, прочитаем ваше мнение о нас или любую другую информацию, которую вы нам отправите через форму обратной связи.<br>Заполняя эту форму на нашем сайте, вы соглашаетесь с обработкой персональных данных, которые вы вводите<br>','feedback','',''),(23,NULL,'2020-08-23 10:22:06.480477','2020-08-23 10:22:06.517488',21,1,3,'','Написать нам','Мы с удовольствием примем от вас заявку через сайт, прочитаем ваше мнение о нас или любую другую информацию, которую вы нам отправите через форму обратной связи.<br>Заполняя эту форму на нашем сайте, вы соглашаетесь с обработкой персональных данных, которые вы вводите<br>','feedback','',''),(24,NULL,'2020-08-27 14:33:22.677515','2020-08-27 14:33:22.677541',22,1,1,'','Меню в футере','','othermenu','',''),(25,NULL,'2020-08-27 15:21:36.482778','2020-08-27 15:21:36.482799',23,1,99,'','Блоги','','blogs','',''),(26,NULL,'2020-08-27 15:55:56.441407','2020-08-27 15:55:56.441432',24,1,99,'','Блог - Статья','','blog_detail','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_linkcontainer`
--

LOCK TABLES `flatcontent_linkcontainer` WRITE;
/*!40000 ALTER TABLE `flatcontent_linkcontainer` DISABLE KEYS */;
INSERT INTO `flatcontent_linkcontainer` VALUES (35,NULL,'2020-08-23 10:22:16.745165','2020-08-23 10:22:16.745188',1,1,NULL,NULL,12,6),(36,NULL,'2020-08-23 10:22:16.746604','2020-08-23 10:22:16.746626',2,1,NULL,NULL,12,10),(37,NULL,'2020-08-23 10:22:16.747962','2020-08-23 10:22:16.747984',3,1,NULL,NULL,12,11),(38,NULL,'2020-08-23 10:22:16.749318','2020-08-23 10:22:16.749339',4,1,NULL,NULL,12,13),(39,NULL,'2020-08-23 10:22:16.750718','2020-08-23 10:22:16.750742',5,1,NULL,NULL,12,15),(40,NULL,'2020-08-23 10:22:16.752113','2020-08-23 10:22:16.752135',6,1,NULL,NULL,12,17),(41,NULL,'2020-08-23 10:22:16.754812','2020-08-23 10:22:16.754832',7,1,NULL,NULL,12,19),(42,NULL,'2020-08-23 10:22:16.756279','2020-08-23 10:22:16.756299',8,1,NULL,NULL,12,21),(43,NULL,'2020-08-23 10:22:16.757704','2020-08-23 10:22:16.757724',9,1,NULL,NULL,12,23);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_customuser`
--

LOCK TABLES `login_customuser` WRITE;
/*!40000 ALTER TABLE `login_customuser` DISABLE KEYS */;
INSERT INTO `login_customuser` VALUES (1,NULL,'2020-08-17 11:04:15.113317','2022-03-11 10:11:12.566642',1,1,NULL,NULL,NULL,NULL,1),(3,NULL,'2022-03-11 10:11:47.373720','2022-03-11 10:11:47.427534',3,1,NULL,NULL,'','',3);
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
-- Table structure for table `main_functions_captcha`
--

DROP TABLE IF EXISTS `main_functions_captcha`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_functions_captcha` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_functions_captcha_value_9a934589` (`value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_functions_captcha`
--

LOCK TABLES `main_functions_captcha` WRITE;
/*!40000 ALTER TABLE `main_functions_captcha` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_functions_captcha` ENABLE KEYS */;
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
  `phone_confirmed` tinyint(1) NOT NULL,
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
  KEY `personal_shopper_ip_86d54b2b` (`ip`),
  KEY `personal_shopper_phone_confirmed_b4c3f6dd` (`phone_confirmed`)
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
  `stock_info` varchar(255) DEFAULT NULL,
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
  KEY `products_products_multiplicity_d783aa0f` (`multiplicity`),
  KEY `products_products_stock_info_95e99d54` (`stock_info`)
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
  `code` varchar(255) DEFAULT NULL,
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
  KEY `products_propertiesvalues_code_bebd589c` (`code`),
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
  `group_id` int(11) DEFAULT NULL,
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
  KEY `products_property_search_facet_a9b2f085` (`search_facet`),
  KEY `products_property_group_id_b794a8f2_fk_products_propertygroup_id` (`group_id`),
  CONSTRAINT `products_property_group_id_b794a8f2_fk_products_propertygroup_id` FOREIGN KEY (`group_id`) REFERENCES `products_propertygroup` (`id`)
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
-- Table structure for table `products_propertygroup`
--

DROP TABLE IF EXISTS `products_propertygroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_propertygroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `code` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_propertygroup_img_610d5e0d` (`img`),
  KEY `products_propertygroup_created_733ff1a3` (`created`),
  KEY `products_propertygroup_updated_ff737f55` (`updated`),
  KEY `products_propertygroup_position_985477b7` (`position`),
  KEY `products_propertygroup_is_active_423f973b` (`is_active`),
  KEY `products_propertygroup_state_96092c63` (`state`),
  KEY `products_propertygroup_parents_0358c639` (`parents`),
  KEY `products_propertygroup_name_5da27b7e` (`name`),
  KEY `products_propertygroup_code_81d425a3` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_propertygroup`
--

LOCK TABLES `products_propertygroup` WRITE;
/*!40000 ALTER TABLE `products_propertygroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_propertygroup` ENABLE KEYS */;
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
-- Table structure for table `shop_ordersdelivery`
--

DROP TABLE IF EXISTS `shop_ordersdelivery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_ordersdelivery` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `latitude` decimal(30,25) DEFAULT NULL,
  `longitude` decimal(30,25) DEFAULT NULL,
  `time` datetime(6) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  `additional_data` longtext,
  `cost` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `shop_ordersdelivery_order_id_85596f72_fk_shop_orders_id` (`order_id`),
  KEY `shop_ordersdelivery_img_db632418` (`img`),
  KEY `shop_ordersdelivery_created_351f1096` (`created`),
  KEY `shop_ordersdelivery_updated_b6b893e2` (`updated`),
  KEY `shop_ordersdelivery_position_f2c9db69` (`position`),
  KEY `shop_ordersdelivery_is_active_1773c3f8` (`is_active`),
  KEY `shop_ordersdelivery_state_f0b2e7a1` (`state`),
  KEY `shop_ordersdelivery_parents_69bd1cb7` (`parents`),
  KEY `shop_ordersdelivery_latitude_a1310b42` (`latitude`),
  KEY `shop_ordersdelivery_longitude_9602d9e9` (`longitude`),
  KEY `shop_ordersdelivery_time_7975dde7` (`time`),
  KEY `shop_ordersdelivery_cost_f1df93d2` (`cost`),
  CONSTRAINT `shop_ordersdelivery_order_id_85596f72_fk_shop_orders_id` FOREIGN KEY (`order_id`) REFERENCES `shop_orders` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shop_ordersdelivery`
--

LOCK TABLES `shop_ordersdelivery` WRITE;
/*!40000 ALTER TABLE `shop_ordersdelivery` DISABLE KEYS */;
/*!40000 ALTER TABLE `shop_ordersdelivery` ENABLE KEYS */;
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

-- Dump completed on 2022-03-11 11:15:19
