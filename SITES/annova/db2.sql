-- MySQL dump 10.13  Distrib 5.7.34, for osx10.16 (x86_64)
--
-- Host: localhost    Database: annova
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'SEO');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,37),(2,1,40),(4,1,44),(3,1,45),(5,1,49);
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
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add user',3,'add_user'),(10,'Can change user',3,'change_user'),(11,'Can delete user',3,'delete_user'),(12,'Can view user',3,'view_user'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Админка - Настройка',6,'add_config'),(22,'Can change Админка - Настройка',6,'change_config'),(23,'Can delete Админка - Настройка',6,'delete_config'),(24,'Can view Админка - Настройка',6,'view_config'),(25,'Can add Админка - Задача',7,'add_tasks'),(26,'Can change Админка - Задача',7,'change_tasks'),(27,'Can delete Админка - Задача',7,'delete_tasks'),(28,'Can view Админка - Задача',7,'view_tasks'),(29,'Can add captcha',8,'add_captcha'),(30,'Can change captcha',8,'change_captcha'),(31,'Can delete captcha',8,'delete_captcha'),(32,'Can view captcha',8,'view_captcha'),(33,'Can add custom user',12,'add_customuser'),(34,'Can change custom user',12,'change_customuser'),(35,'Can delete custom user',12,'delete_customuser'),(36,'Can view custom user',12,'view_customuser'),(37,'Can add Стат.контет - Файл',13,'add_files'),(38,'Can change Стат.контет - Файл',13,'change_files'),(39,'Can delete Стат.контет - Файл',13,'delete_files'),(40,'Can view Стат.контет - Файл',13,'view_files'),(41,'Can add Стат.контент - Блоки',14,'add_blocks'),(42,'Can change Стат.контент - Блоки',14,'change_blocks'),(43,'Can delete Стат.контент - Блоки',14,'delete_blocks'),(44,'Can view Стат.контент - Блоки',14,'view_blocks'),(45,'Заполнение сео-полей меню',14,'seo_fields'),(46,'Can add Стат.контент - Контейнеры',15,'add_containers'),(47,'Can change Стат.контент - Контейнеры',15,'change_containers'),(48,'Can delete Стат.контент - Контейнеры',15,'delete_containers'),(49,'Can view Стат.контент - Контейнеры',15,'view_containers'),(50,'Can add Стат.контент - Линковка меню к контейнерам',16,'add_linkcontainer'),(51,'Can change Стат.контент - Линковка меню к контейнерам',16,'change_linkcontainer'),(52,'Can delete Стат.контент - Линковка меню к контейнерам',16,'delete_linkcontainer'),(53,'Can view Стат.контент - Линковка меню к контейнерам',16,'view_linkcontainer'),(54,'Can add Пользователи - пользователь',17,'add_shopper'),(55,'Can change Пользователи - пользователь',17,'change_shopper'),(56,'Can delete Пользователи - пользователь',17,'delete_shopper'),(57,'Can view Пользователи - пользователь',17,'view_shopper'),(58,'Can add Товары - товар/услуга',18,'add_products'),(59,'Can change Товары - товар/услуга',18,'change_products'),(60,'Can delete Товары - товар/услуга',18,'delete_products'),(61,'Can view Товары - товар/услуга',18,'view_products'),(62,'Can add products cats',19,'add_productscats'),(63,'Can change products cats',19,'change_productscats'),(64,'Can delete products cats',19,'delete_productscats'),(65,'Can view products cats',19,'view_productscats'),(66,'Can add products photos',20,'add_productsphotos'),(67,'Can change products photos',20,'change_productsphotos'),(68,'Can delete products photos',20,'delete_productsphotos'),(69,'Can view products photos',20,'view_productsphotos'),(70,'Can add property',21,'add_property'),(71,'Can change property',21,'change_property'),(72,'Can delete property',21,'delete_property'),(73,'Can view property',21,'view_property'),(74,'Can add properties values',22,'add_propertiesvalues'),(75,'Can change properties values',22,'change_propertiesvalues'),(76,'Can delete properties values',22,'delete_propertiesvalues'),(77,'Can view properties values',22,'view_propertiesvalues'),(78,'Can add products properties',23,'add_productsproperties'),(79,'Can change products properties',23,'change_productsproperties'),(80,'Can delete products properties',23,'delete_productsproperties'),(81,'Can view products properties',23,'view_productsproperties'),(82,'Can add costs types',24,'add_coststypes'),(83,'Can change costs types',24,'change_coststypes'),(84,'Can delete costs types',24,'delete_coststypes'),(85,'Can view costs types',24,'view_coststypes'),(86,'Can add costs',25,'add_costs'),(87,'Can change costs',25,'change_costs'),(88,'Can delete costs',25,'delete_costs'),(89,'Can view costs',25,'view_costs'),(90,'Can add property group',26,'add_propertygroup'),(91,'Can change property group',26,'change_propertygroup'),(92,'Can delete property group',26,'delete_propertygroup'),(93,'Can view property group',26,'view_propertygroup'),(94,'Can add Магазин - Заказ',27,'add_orders'),(95,'Can change Магазин - Заказ',27,'change_orders'),(96,'Can delete Магазин - Заказ',27,'delete_orders'),(97,'Can view Магазин - Заказ',27,'view_orders'),(98,'Can add Магазин - Покупки',29,'add_purchases'),(99,'Can change Магазин - Покупки',29,'change_purchases'),(100,'Can delete Магазин - Покупки',29,'delete_purchases'),(101,'Can view Магазин - Покупки',29,'view_purchases'),(102,'Can add Магазин - Транзакция',30,'add_transactions'),(103,'Can change Магазин - Транзакция',30,'change_transactions'),(104,'Can delete Магазин - Транзакция',30,'delete_transactions'),(105,'Can view Магазин - Транзакция',30,'view_transactions'),(106,'Can add Магазин - Промокод',31,'add_promocodes'),(107,'Can change Магазин - Промокод',31,'change_promocodes'),(108,'Can delete Магазин - Промокод',31,'delete_promocodes'),(109,'Can view Магазин - Промокод',31,'view_promocodes'),(110,'Can add Магазин - Доставка заказа',32,'add_ordersdelivery'),(111,'Can change Магазин - Доставка заказа',32,'change_ordersdelivery'),(112,'Can delete Магазин - Доставка заказа',32,'delete_ordersdelivery'),(113,'Can view Магазин - Доставка заказа',32,'view_ordersdelivery'),(114,'Can add Пользователь - Паспортные данные',33,'add_passport'),(115,'Can change Пользователь - Паспортные данные',33,'change_passport'),(116,'Can delete Пользователь - Паспортные данные',33,'delete_passport'),(117,'Can view Пользователь - Паспортные данные',33,'view_passport');
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$ptaNw5VOPnt9$zJWui6iBrIhrQIxbHcBLreGRK+ICLGV6j1neJ6PGj48=','2022-02-01 14:09:24.917896',1,'jocker','','','dkramorov@mail.ru',1,1,'2022-02-01 14:04:55.773731'),(2,'pbkdf2_sha256$100000$TRO8mRHFfWfF$203IsmHHe7P+BJ2G9ZQPdWALGdPoZOQ13H30krH+lus=','2022-02-03 15:51:08.386455',1,'alex','Александр','','',1,1,'2022-02-01 14:09:48.960409'),(3,'pbkdf2_sha256$150000$Ts302GobjEqG$Vfbuv3Bqst9Z2r3kOPGsyl/RJ0IrL5XQeCyuCc+OI5M=',NULL,0,'SeoManager','','SeoManager','seo_manager@masterme.ru',1,1,'2022-02-01 14:52:08.879296');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,3,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(13,'files','files'),(14,'flatcontent','blocks'),(15,'flatcontent','containers'),(16,'flatcontent','linkcontainer'),(12,'login','customuser'),(9,'login','extrafields'),(11,'login','extrainfo'),(10,'login','extravalues'),(8,'main_functions','captcha'),(6,'main_functions','config'),(7,'main_functions','tasks'),(33,'passport','passport'),(17,'personal','shopper'),(25,'products','costs'),(24,'products','coststypes'),(18,'products','products'),(19,'products','productscats'),(20,'products','productsphotos'),(23,'products','productsproperties'),(22,'products','propertiesvalues'),(21,'products','property'),(26,'products','propertygroup'),(5,'sessions','session'),(27,'shop','orders'),(32,'shop','ordersdelivery'),(31,'shop','promocodes'),(29,'shop','purchases'),(30,'shop','transactions'),(28,'shop','wishlist');
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
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2022-02-01 14:04:52.268479'),(2,'contenttypes','0002_remove_content_type_name','2022-02-01 14:04:52.335043'),(3,'auth','0001_initial','2022-02-01 14:04:52.635253'),(4,'auth','0002_alter_permission_name_max_length','2022-02-01 14:04:53.022428'),(5,'auth','0003_alter_user_email_max_length','2022-02-01 14:04:53.061302'),(6,'auth','0004_alter_user_username_opts','2022-02-01 14:04:53.070161'),(7,'auth','0005_alter_user_last_login_null','2022-02-01 14:04:53.107877'),(8,'auth','0006_require_contenttypes_0002','2022-02-01 14:04:53.109950'),(9,'auth','0007_alter_validators_add_error_messages','2022-02-01 14:04:53.117014'),(10,'auth','0008_alter_user_username_max_length','2022-02-01 14:04:53.154477'),(11,'auth','0009_alter_user_last_name_max_length','2022-02-01 14:04:53.193073'),(12,'auth','0010_alter_group_name_max_length','2022-02-01 14:04:53.230157'),(13,'auth','0011_update_proxy_permissions','2022-02-01 14:04:53.239057'),(14,'files','0001_initial','2022-02-01 14:04:53.293554'),(15,'files','0002_auto_20191203_2054','2022-02-01 14:04:53.574986'),(16,'files','0003_auto_20200112_1717','2022-02-01 14:04:53.608108'),(17,'files','0004_auto_20200402_2127','2022-02-01 14:04:53.664192'),(18,'files','0005_auto_20200809_1025','2022-02-01 14:04:53.668613'),(19,'files','0006_auto_20210516_1530','2022-02-01 14:04:53.719709'),(20,'flatcontent','0001_initial','2022-02-01 14:04:53.934498'),(21,'flatcontent','0002_auto_20190825_1730','2022-02-01 14:04:54.953774'),(22,'flatcontent','0003_auto_20191203_2054','2022-02-01 14:04:55.090691'),(23,'flatcontent','0004_blocks_html','2022-02-01 14:04:55.134975'),(24,'flatcontent','0005_auto_20200112_1717','2022-02-01 14:04:55.226338'),(25,'flatcontent','0006_auto_20200314_1638','2022-02-01 14:04:55.234603'),(26,'flatcontent','0007_auto_20200402_2127','2022-02-01 14:04:55.404380'),(27,'flatcontent','0008_containers_class_name','2022-02-01 14:04:55.451550'),(28,'flatcontent','0009_blocks_class_name','2022-02-01 14:04:55.518573'),(29,'flatcontent','0010_auto_20210430_1708','2022-02-01 14:04:55.550011'),(30,'flatcontent','0011_auto_20210526_2033','2022-02-01 14:04:55.557160'),(31,'login','0001_initial','2022-02-01 14:04:55.837188'),(32,'login','0002_auto_20200925_1007','2022-02-01 14:04:56.851853'),(33,'main_functions','0001_initial','2022-02-01 14:04:56.933956'),(34,'main_functions','0002_auto_20191203_2052','2022-02-01 14:04:57.019269'),(35,'main_functions','0003_auto_20200407_1845','2022-02-01 14:04:57.765427'),(36,'main_functions','0004_config_user','2022-02-01 14:04:58.237910'),(37,'main_functions','0005_auto_20210321_1210','2022-02-01 14:04:58.283942'),(38,'main_functions','0006_captcha','2022-02-01 14:04:58.314202'),(44,'sessions','0001_initial','2022-02-01 14:04:59.191270'),(45,'personal','0001_initial','2022-02-03 10:13:52.565548'),(46,'personal','0002_auto_20200528_1642','2022-02-03 10:13:53.113163'),(47,'personal','0003_auto_20200616_1707','2022-02-03 10:13:53.147397'),(48,'personal','0004_shopper_ip','2022-02-03 10:13:53.194394'),(49,'personal','0005_shopper_phone_confirmed','2022-02-03 10:13:53.294474'),(50,'products','0001_initial','2022-02-03 10:13:53.411520'),(51,'products','0002_productsphotos','2022-02-03 10:13:53.998079'),(52,'products','0003_auto_20200315_2217','2022-02-03 10:13:54.315316'),(53,'products','0004_auto_20200316_2329','2022-02-03 10:13:54.467405'),(54,'products','0005_auto_20200402_2127','2022-02-03 10:13:54.754690'),(55,'products','0006_auto_20200402_2351','2022-02-03 10:13:55.412562'),(56,'products','0007_property_ptype','2022-02-03 10:13:55.485516'),(57,'products','0008_property_code','2022-02-03 10:13:55.555002'),(58,'products','0009_property_measure','2022-02-03 10:13:55.623634'),(59,'products','0010_auto_20200623_1629','2022-02-03 10:13:55.755145'),(60,'products','0011_auto_20200627_1353','2022-02-03 10:13:56.231783'),(61,'products','0012_auto_20201212_1449','2022-02-03 10:13:56.387802'),(62,'products','0013_property_search_facet','2022-02-03 10:13:56.515402'),(63,'products','0014_propertiesvalues_code','2022-02-03 10:13:56.568433'),(64,'products','0015_auto_20220122_1311','2022-02-03 10:13:56.681559'),(65,'products','0016_products_stock_info','2022-02-03 10:13:57.067844'),(66,'shop','0001_initial','2022-02-03 10:13:57.276393'),(67,'shop','0002_auto_20200618_0000','2022-02-03 10:13:58.353986'),(68,'shop','0003_auto_20200621_1346','2022-02-03 10:13:59.015883'),(69,'shop','0004_purchases_cost_type','2022-02-03 10:13:59.234992'),(70,'shop','0005_transactions','2022-02-03 10:13:59.340255'),(71,'shop','0006_auto_20200719_0003','2022-02-03 10:13:59.826833'),(72,'shop','0007_auto_20200719_0146','2022-02-03 10:14:00.357126'),(73,'shop','0008_auto_20201026_1359','2022-02-03 10:14:00.474051'),(74,'shop','0009_auto_20201212_1539','2022-02-03 10:14:00.574004'),(75,'shop','0010_auto_20210208_1858','2022-02-03 10:14:00.689083'),(76,'shop','0011_orders_external_number','2022-02-03 10:14:00.767788'),(77,'shop','0012_ordersdelivery','2022-02-03 10:14:00.856131'),(78,'shop','0013_auto_20210801_1636','2022-02-03 10:14:01.182294'),(79,'shop','0014_ordersdelivery_additional_data','2022-02-03 10:14:01.240776'),(80,'shop','0015_auto_20220123_2207','2022-02-03 10:14:01.299942'),(81,'passport','0001_initial','2022-02-07 13:05:19.561313');
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
INSERT INTO `django_session` VALUES ('4a28ylx2lmb3z7vwvnagax3fpmi3xdq2','NzExMzc2MWM3NDhiOWI4OTE1YmNjNjRkZjAyZWRjMzA4MGQyYjE3Yzp7Il9hdXRoX3VzZXJfaGFzaCI6IjIyYTY2MTU3YmJhODYzYWUwNmFmMDE5NDEzODUwZTQ3ZmZmNWQ2MGQiLCJfYXV0aF91c2VyX2lkIjoiMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFwcHMubG9naW4uYmFja2VuZC5NeUJhY2tlbmQifQ==','2022-02-15 17:25:08.924389'),('7n1ufesaywodh2pzvobh1qvf6qfrg8jj','ZThkMDFlNDVmMDY5ZjQ5M2Q5ZTQwM2IzOGU4ZTAyZjFiNmUxZDQwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImU4NDk1MjZiZjRjMDFmOTE0ZjM4YzdhZTY3NjI4MmIxMWRhYWE0NGEifQ==','2022-02-15 14:09:24.922587'),('e89u114dybx2p7gwx2zg7sqxa3fnvdqg','ZmQ5NzYyNDM3NGZmNTUxNmRiOGMwNWIzNDYxMDNmNjljNTlhNDZiNjp7Il9hdXRoX3VzZXJfaGFzaCI6IjIyYTY2MTU3YmJhODYzYWUwNmFmMDE5NDEzODUwZTQ3ZmZmNWQ2MGQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhcHBzLmxvZ2luLmJhY2tlbmQuTXlCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjIifQ==','2022-02-15 17:41:26.305861'),('s0ldpi5gbjtt4kddmvhlzqw04a3pl5ay','NDA0MGRiZjcwYTc0OGMwMzA1NzZhZmYzOGJmMWRjYTllZmMyNGM2Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjIyYTY2MTU3YmJhODYzYWUwNmFmMDE5NDEzODUwZTQ3ZmZmNWQ2MGQifQ==','2022-02-17 15:51:08.419501');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files_files`
--

LOCK TABLES `files_files` WRITE;
/*!40000 ALTER TABLE `files_files` DISABLE KEYS */;
INSERT INTO `files_files` VALUES (1,NULL,'2022-02-01 14:52:08.940453','2022-02-01 14:52:08.941773',1,1,NULL,NULL,'robots.txt','/robots.txt','Файл для запретов индексации поисковым системам','text/plain','robots.txt',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
INSERT INTO `flatcontent_blocks` VALUES (1,'1.png','2022-02-01 14:52:08.799990','2022-02-01 17:57:52.179294',1,1,1,'','Логотип','Быстро, просто, удобно','/','logo',3,0,'','','Страхование','',''),(2,NULL,'2022-02-01 14:52:08.801523','2022-02-06 18:29:43.841922',2,1,1,'','Телефон','','tel:73952123321','phone',3,0,'','','','+7(914)9472292',''),(3,NULL,'2022-02-01 14:52:08.807296','2022-02-06 18:30:48.391766',3,1,1,'','Адрес','','','address',3,0,'','','','г. Иркутск ул. Ржанова 166, 3-й этаж офис 301',''),(4,NULL,'2022-02-01 14:52:08.814605','2022-02-06 18:31:24.034019',4,1,1,'','Email','','','email',3,0,'','','','ap@223-223.ru',''),(5,NULL,'2022-02-01 14:52:08.815911','2022-02-06 18:31:46.482120',5,1,1,'','Режим работы','','','worktime',3,0,'','','','пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 15:00',''),(6,NULL,'2022-02-01 14:52:08.817424','2022-02-01 14:52:08.817430',6,1,3,'','Copyright',NULL,NULL,'copyright',3,0,NULL,NULL,NULL,'<p>&copy; 2020 Все права защищены</p>',NULL),(7,NULL,'2022-02-01 14:52:08.826162','2022-02-06 18:32:22.195420',7,1,1,'','Название компании','','','company_name',3,0,'','','Company name','ООО Город АйТи',''),(8,'8.png','2022-02-01 14:52:08.827424','2022-02-06 18:33:26.473697',8,1,1,'','Favicon','','','favicon',3,0,'','','','',''),(9,NULL,'2022-02-01 14:52:08.828657','2022-02-01 14:52:08.828662',9,1,3,'','Сообщества',NULL,NULL,'social',3,0,NULL,NULL,NULL,NULL,NULL),(10,NULL,'2022-02-01 14:52:08.829904','2022-02-01 14:52:08.829908',10,1,3,'_9','instagram',NULL,NULL,'instagram',3,1,'instagram',NULL,NULL,NULL,NULL),(11,NULL,'2022-02-01 14:52:08.831120','2022-02-01 14:52:08.831125',11,1,3,'_9','vk',NULL,NULL,'vk',3,1,'vk',NULL,NULL,NULL,NULL),(12,NULL,'2022-02-01 14:52:08.832398','2022-02-01 14:52:08.832403',12,1,3,'_9','facebook',NULL,NULL,'facebook',3,1,'facebook',NULL,NULL,NULL,NULL),(13,NULL,'2022-02-01 14:52:08.833718','2022-02-01 14:52:08.833724',13,1,3,'_9','twitter',NULL,NULL,'twitter',3,1,'twitter',NULL,NULL,NULL,NULL),(14,NULL,'2022-02-01 14:52:08.835282','2022-02-01 14:52:08.835292',14,1,3,'','Яндекс.Метрика счетчик',NULL,NULL,'yandex_metrika',3,0,NULL,NULL,NULL,'<script type=\"text/javascript\"></script>',NULL),(15,NULL,'2022-02-01 14:52:08.836616','2022-02-01 14:52:08.836621',15,1,3,'','Google.Analytics счетчик',NULL,NULL,'google_analytics',3,0,NULL,NULL,NULL,'<script type=\"text/javascript\"></script>',NULL),(16,NULL,'2022-02-01 14:52:08.839971','2022-02-04 11:00:27.689684',16,1,4,'','Главная','','/','_mainmenu_mainpage',4,0,'','','','',''),(22,NULL,'2022-02-01 14:52:08.848780','2022-02-07 09:34:39.601229',22,1,4,'','О нас','','/about/','_mainmenu_aboutpage',4,0,'','','','',''),(23,NULL,'2022-02-01 14:52:08.850016','2022-02-03 16:11:52.555584',23,1,4,'','Услуги','','/services/','_mainmenu_servicespage',4,0,'','','','',''),(24,NULL,'2022-02-01 14:52:08.852310','2022-02-06 18:52:20.996229',24,1,4,'','Контакты','','/feedback/','_mainmenu_feedbackpage',4,0,'','','','',''),(25,NULL,'2022-02-01 14:52:08.855136','2022-02-01 14:52:08.855141',25,1,4,'','Каталог',NULL,'/cat/','_bottommenu_catpage',5,0,NULL,NULL,NULL,NULL,NULL),(26,NULL,'2022-02-01 14:52:08.857425','2022-02-01 14:52:08.857432',26,1,4,'_25','Популярные товары',NULL,'/cat/populyarnye-tovary/','_bottommenu_catpage_popular',5,0,NULL,NULL,NULL,NULL,NULL),(27,NULL,'2022-02-01 14:52:08.859068','2022-02-01 14:52:08.859073',27,1,4,'_25','Новые товары',NULL,'/cat/novye-tovary/','_bottommenu_catpage_new',5,0,NULL,NULL,NULL,NULL,NULL),(28,NULL,'2022-02-01 14:52:08.860508','2022-02-01 14:52:08.860513',28,1,4,'_25','Товары со скидкой',NULL,'/cat/tovary-so-skidkoy/','_bottommenu_catpage_discount',5,0,NULL,NULL,NULL,NULL,NULL),(29,NULL,'2022-02-01 14:52:08.861975','2022-02-01 14:52:08.861981',29,1,4,'_25','Распродажа',NULL,'/cat/rasprodaja/','_bottommenu_catpage_sale',5,0,NULL,NULL,NULL,NULL,NULL),(30,NULL,'2022-02-01 14:52:08.863178','2022-02-01 14:52:08.863183',30,1,4,'','О нас',NULL,'/about/','_bottommenu_aboutpage',5,0,NULL,NULL,NULL,NULL,NULL),(31,NULL,'2022-02-01 14:52:08.864391','2022-02-01 14:52:08.864396',31,1,4,'','Услуги',NULL,'/services/','_bottommenu_servicespage',5,0,NULL,NULL,NULL,NULL,NULL),(32,NULL,'2022-02-01 14:52:08.865637','2022-02-01 14:52:08.865642',32,1,4,'','Контакты',NULL,'/feedback/','_bottommenu_feedbackpage',5,0,NULL,NULL,NULL,NULL,NULL),(33,'33.png','2022-02-01 15:04:19.627534','2022-02-01 15:08:47.527926',33,1,1,'','Выгодно','','/','',6,0,'','','Подробнее','Выгодное предложение специально для членов Трудовых Резервов',''),(34,'34.png','2022-02-01 15:04:20.691186','2022-02-01 15:08:52.566413',34,1,1,'','Удобно','','/','',6,0,'','','Подробнее','Тарифы на все варианты участия в мероприятиях',''),(35,'35.png','2022-02-01 15:04:21.667901','2022-02-01 15:08:57.560022',35,1,1,'','Доступно','','/','',6,0,'','','Подробнее','Синхронизация данных о страховке с мандатной комиссией',''),(36,'33.png','2022-02-01 15:09:50.431919','2022-02-03 16:00:50.508695',33,1,1,'','Выгодно','','/','',7,0,'','','Подробнее','Выгодное предложение специально для членов КХК',''),(37,'34.png','2022-02-01 15:09:50.437345','2022-02-01 15:09:50.437381',34,1,1,'','Удобно','','/','',7,0,'','','Подробнее','Тарифы на все варианты участия в мероприятиях',''),(38,'35.png','2022-02-01 15:09:50.442155','2022-02-03 16:01:45.256996',35,1,1,'','Доступно','','/','',7,0,'','','Подробнее','Синхронизация данных о страховке с КХК',''),(39,NULL,'2022-02-01 15:13:32.381689','2022-02-01 15:15:18.581420',36,1,1,'','Вопрос по страхованию жизни','','','',8,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно частым и возникает обычно у человека, который решил застраховаться, но имеет недостаточно информации по этой процедуре<br>',''),(40,NULL,'2022-02-01 15:13:33.409621','2022-02-01 15:15:21.245298',37,1,1,'','Вопрос по страхованию имущества','','','',8,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(41,NULL,'2022-02-01 15:13:34.282973','2022-02-01 15:15:23.958548',38,1,1,'','Вопрос по автострахованию','','','',8,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(42,NULL,'2022-02-01 15:13:35.106173','2022-02-01 15:15:26.520410',39,1,1,'','Вопрос по стрхованию ребенка','','','',8,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(43,NULL,'2022-02-01 15:13:35.859948','2022-02-01 15:15:29.000050',40,1,1,'','Вопрос по страхованию пенсионера','','','',8,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(44,NULL,'2022-02-01 15:13:36.873947','2022-02-01 15:15:31.719473',41,1,1,'','Вопрос по выплатам','','','',8,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(45,NULL,'2022-02-01 15:16:29.398689','2022-02-01 15:16:29.398720',36,1,1,'','Вопрос по страхованию жизни','','','',9,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно частым и возникает обычно у человека, который решил застраховаться, но имеет недостаточно информации по этой процедуре<br>',''),(46,NULL,'2022-02-01 15:16:29.401125','2022-02-01 15:16:29.401152',37,1,1,'','Вопрос по страхованию имущества','','','',9,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(47,NULL,'2022-02-01 15:16:29.402556','2022-02-01 15:16:29.402582',38,1,1,'','Вопрос по автострахованию','','','',9,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(48,NULL,'2022-02-01 15:16:29.403865','2022-02-01 15:16:29.403889',39,1,1,'','Вопрос по стрхованию ребенка','','','',9,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(49,NULL,'2022-02-01 15:16:29.405161','2022-02-01 15:16:29.405186',40,1,1,'','Вопрос по страхованию пенсионера','','','',9,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(50,NULL,'2022-02-01 15:16:29.406587','2022-02-01 15:16:29.406621',41,1,1,'','Вопрос по выплатам','','','',9,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(51,'51.jpg','2022-02-01 15:18:32.228604','2022-02-01 15:18:32.228643',42,1,1,'','Без названия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(52,'52.jpg','2022-02-01 15:18:33.095500','2022-02-01 15:18:33.095539',43,1,1,'','Без названия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(53,'53.jpg','2022-02-01 15:18:33.924683','2022-02-01 15:18:33.924723',44,1,1,'','Без названия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(54,'54.jpg','2022-02-01 15:18:34.745219','2022-02-01 15:18:34.745260',45,1,1,'','Без названия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(55,'55.jpg','2022-02-01 15:18:35.714577','2022-02-01 15:18:35.714612',46,1,1,'','Без названия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(56,'56.jpg','2022-02-01 15:18:36.770311','2022-02-01 15:18:36.770357',47,1,1,'','Без названия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(57,'51.jpg','2022-02-01 15:21:15.373446','2022-02-01 15:21:15.373491',42,1,1,'','Без названия',NULL,NULL,NULL,11,0,NULL,NULL,NULL,NULL,NULL),(58,'52.jpg','2022-02-01 15:21:15.379619','2022-02-01 15:21:15.379662',43,1,1,'','Без названия',NULL,NULL,NULL,11,0,NULL,NULL,NULL,NULL,NULL),(59,'53.jpg','2022-02-01 15:21:15.392700','2022-02-01 15:21:15.392744',44,1,1,'','Без названия',NULL,NULL,NULL,11,0,NULL,NULL,NULL,NULL,NULL),(60,'54.jpg','2022-02-01 15:21:15.396731','2022-02-01 15:21:15.396768',45,1,1,'','Без названия',NULL,NULL,NULL,11,0,NULL,NULL,NULL,NULL,NULL),(61,'55.jpg','2022-02-01 15:21:15.400714','2022-02-01 15:21:15.400752',46,1,1,'','Без названия',NULL,NULL,NULL,11,0,NULL,NULL,NULL,NULL,NULL),(62,'56.jpg','2022-02-01 15:21:15.405506','2022-02-01 15:21:15.405553',47,1,1,'','Без названия',NULL,NULL,NULL,11,0,NULL,NULL,NULL,NULL,NULL),(63,NULL,'2022-02-01 15:28:00.875343','2022-02-01 15:28:59.963537',48,1,1,'','Консультации по страхованию','','','',12,0,'','','','Мы предоставляем консультацию по телефону и также вы можете задать вопрос через сайт, наш специалист свяжется с вами и ответит на интересующие вас вопросы в удобное для вас время<br>',''),(64,NULL,'2022-02-01 15:28:01.976923','2022-02-01 15:29:08.549568',49,1,1,'','Консультации по выплатам','','','',12,0,'','','','Мы предоставляем консультацию по телефону и также вы можете задать \r\nвопрос через сайт, наш специалист свяжется с вами и ответит на \r\nинтересующие вас вопросы в удобное для вас время',''),(65,'65.jpg','2022-02-01 15:28:03.181986','2022-02-01 15:32:12.833493',50,1,1,'','Консультант Ирина','','','spec1',12,0,'','','','+7 (3952) 321-321<br>',''),(66,'66.jpg','2022-02-01 15:28:04.382353','2022-02-01 15:32:04.853988',51,1,1,'','Зам директора Аня','','','spec2',12,0,'','','','+7 (3952) 123-321<br>',''),(67,NULL,'2022-02-01 15:32:25.135342','2022-02-01 15:32:25.135387',48,1,1,'','Консультации по страхованию','','','',13,0,'','','','Мы предоставляем консультацию по телефону и также вы можете задать вопрос через сайт, наш специалист свяжется с вами и ответит на интересующие вас вопросы в удобное для вас время<br>',''),(68,NULL,'2022-02-01 15:32:25.138274','2022-02-01 15:32:25.138304',49,1,1,'','Консультации по выплатам','','','',13,0,'','','','Мы предоставляем консультацию по телефону и также вы можете задать \r\nвопрос через сайт, наш специалист свяжется с вами и ответит на \r\nинтересующие вас вопросы в удобное для вас время',''),(69,'65.jpg','2022-02-01 15:32:25.144336','2022-02-01 15:32:25.144364',50,1,1,'','Консультант Ирина','','','spec1',13,0,'','','','+7 (3952) 321-321<br>',''),(70,'66.jpg','2022-02-01 15:32:25.149684','2022-02-01 15:32:25.149739',51,1,1,'','Зам директора Аня','','','spec2',13,0,'','','','+7 (3952) 123-321<br>',''),(71,NULL,'2022-02-01 16:27:45.511364','2022-02-06 18:35:26.673472',52,1,1,'','О нас','','','about',3,0,'','','','Мы занимаемся спортивным страхованием детей и взрослых. А также мы занимаемся страхованием жизни и имущества.. Работаем на рынке страхования с 2019 года.<br>',''),(72,NULL,'2022-02-03 15:54:39.218455','2022-02-06 18:46:48.481189',53,1,4,'','Срок страхования 1 месяц, тренировки и соревнования по хоккею (150т.р.)','Страховка: Срок страхования 1 месяц Тренировки и соревнования по хоккею Страховая сумма 150000 руб.','/product/srok-strahovaniya-1-mesyac-trenirovki-i-sorevnovaniya-po-hokkeyu-150tr-1/','product_1',14,0,NULL,'страховка хоккей','Страховка',NULL,NULL),(73,NULL,'2022-02-03 15:56:37.585938','2022-02-06 18:47:54.663749',54,1,4,'','Срок страхования 1 месяц, тренировки и соревнования по хоккею (300т.р.)','','/product/srok-strahovaniya-1-mesyac-trenirovki-i-sorevnovaniya-po-hokkeyu-300tr-2/','product_2',14,0,NULL,'','',NULL,NULL),(74,NULL,'2022-02-03 16:06:12.423214','2022-02-06 18:47:05.371380',55,1,4,'','Срок страхования 1 месяц, 24 часа включая тренировки и соревнования по хоккею (150т.р.)','Страховой полис: Срок страхования 1 месяц 24 часа включая тренировки и соревнования по хоккею Страховая сумма 150000','/product/srok-strahovaniya-1-mesyac-24-chasa-vklyuchaya-trenirovki-i-sorevnovaniya-po-hokkeyu-150tr-3/','product_3',14,0,NULL,'страховка спорт','страховка',NULL,NULL),(75,NULL,'2022-02-03 16:07:58.013655','2022-02-06 18:48:10.633286',56,1,4,'','Срок страхования 1 месяц, 24 часа включая тренировки и соревнования по хоккею (300т.р.)','','/product/srok-strahovaniya-1-mesyac-24-chasa-vklyuchaya-trenirovki-i-sorevnovaniya-po-hokkeyu-300tr-4/','product_4',14,0,NULL,'','',NULL,NULL),(76,'76.jpg','2022-02-03 16:09:40.155734','2022-02-03 16:11:34.515693',42,1,1,'','Без названия','','','',15,0,'','','','',''),(77,'52.jpg','2022-02-03 16:09:40.161228','2022-02-03 16:09:40.161255',43,1,1,'','Без названия',NULL,NULL,NULL,15,0,NULL,NULL,NULL,NULL,NULL),(78,'53.jpg','2022-02-03 16:09:40.163464','2022-02-03 16:09:40.163488',44,1,1,'','Без названия',NULL,NULL,NULL,15,0,NULL,NULL,NULL,NULL,NULL),(79,'54.jpg','2022-02-03 16:09:40.165868','2022-02-03 16:09:40.165891',45,1,1,'','Без названия',NULL,NULL,NULL,15,0,NULL,NULL,NULL,NULL,NULL),(80,'55.jpg','2022-02-03 16:09:40.168270','2022-02-03 16:09:40.168294',46,1,1,'','Без названия',NULL,NULL,NULL,15,0,NULL,NULL,NULL,NULL,NULL),(81,'56.jpg','2022-02-03 16:09:40.170430','2022-02-03 16:09:40.170454',47,1,1,'','Без названия',NULL,NULL,NULL,15,0,NULL,NULL,NULL,NULL,NULL),(82,NULL,'2022-02-06 18:39:39.538430','2022-02-06 18:47:21.566671',57,1,4,'','Срок страхования 1 год, тренировки и соревнования по хоккею (150т.р.)','','/product/srok-strahovaniya-1-god-trenirovki-i-sorevnovaniya-po-hokkeyu-150tr-5/','product_5',14,0,NULL,'','',NULL,NULL),(83,NULL,'2022-02-06 18:41:12.129045','2022-02-06 18:47:42.570036',58,1,4,'','Срок страхования 1 год, тренировки и соревнования по хоккею (300т.р.)','','/product/srok-strahovaniya-1-god-trenirovki-i-sorevnovaniya-po-hokkeyu-300tr-6/','product_6',14,0,NULL,'','',NULL,NULL),(84,NULL,'2022-02-06 18:42:30.089574','2022-02-06 18:44:34.729244',59,1,4,'','Срок страхования 1 год, 24 часа включая тренировки и соревнования по хоккею (150т.р.)','','/product/srok-strahovaniya-1-god-24-chasa-vklyuchaya-trenirovki-i-sorevnovaniya-po-hokkeyu-150tr-7/','product_7',14,0,NULL,'','',NULL,NULL),(85,NULL,'2022-02-06 18:44:56.122347','2022-02-06 18:45:33.840541',60,1,4,'','Срок страхования 1 год, 24 часа включая тренировки и соревнования по хоккею (300т.р.)','','/product/srok-strahovaniya-1-god-24-chasa-vklyuchaya-trenirovki-i-sorevnovaniya-po-hokkeyu-300tr-8/','product_8',14,0,NULL,'','',NULL,NULL),(86,NULL,'2022-02-06 18:51:50.349902','2022-02-06 18:51:50.349944',48,1,1,'','Консультации по страхованию','','','',18,0,'','','','Мы предоставляем консультацию по телефону и также вы можете задать вопрос через сайт, наш специалист свяжется с вами и ответит на интересующие вас вопросы в удобное для вас время<br>',''),(87,NULL,'2022-02-06 18:51:50.353030','2022-02-06 18:51:50.353061',49,1,1,'','Консультации по выплатам','','','',18,0,'','','','Мы предоставляем консультацию по телефону и также вы можете задать \r\nвопрос через сайт, наш специалист свяжется с вами и ответит на \r\nинтересующие вас вопросы в удобное для вас время',''),(88,'65.jpg','2022-02-06 18:51:50.354119','2022-02-06 18:51:50.354143',50,1,1,'','Консультант Ирина','','','spec1',18,0,'','','','+7 (3952) 321-321<br>',''),(89,'66.jpg','2022-02-06 18:51:50.357134','2022-02-06 18:51:50.357165',51,1,1,'','Зам директора Аня','','','spec2',18,0,'','','','+7 (3952) 123-321<br>',''),(90,'33.png','2022-02-07 09:26:02.495844','2022-02-07 09:26:02.495869',33,1,1,'','Выгодно','','/','',19,0,'','','Подробнее','Выгодное предложение специально для членов Трудовых Резервов',''),(91,'34.png','2022-02-07 09:26:02.499362','2022-02-07 09:26:02.499389',34,1,1,'','Удобно','','/','',19,0,'','','Подробнее','Тарифы на все варианты участия в мероприятиях',''),(92,'35.png','2022-02-07 09:26:02.500901','2022-02-07 09:26:02.500925',35,1,1,'','Доступно','','/','',19,0,'','','Подробнее','Синхронизация данных о страховке с мандатной комиссией',''),(93,'93.jpg','2022-02-07 11:05:06.408797','2022-02-07 11:05:26.344107',61,1,1,'','Картинка','','','',3,0,'','','','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
INSERT INTO `flatcontent_containers` VALUES (1,NULL,'2022-02-01 14:47:38.802503','2022-02-01 14:47:38.802541',1,1,99,'','Демонстрационная форма','','form1','',''),(2,NULL,'2022-02-01 14:51:39.368480','2022-02-01 14:51:39.368549',2,1,3,'','Демо-форма','','form1','',''),(3,NULL,'2022-02-01 14:52:08.794883','2022-02-01 14:52:08.794895',3,1,2,NULL,'Контент для всех страничек','Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики','main',NULL,NULL),(4,NULL,'2022-02-01 14:52:08.837725','2022-02-01 14:52:08.837730',4,1,1,NULL,'Главное меню','Создано автоматически, выводит главное меню','mainmenu',NULL,NULL),(5,NULL,'2022-02-01 14:52:08.838786','2022-02-01 14:52:08.838791',5,1,1,NULL,'Нижнее меню','Создано автоматически, выводит нижнее меню','bottommenu',NULL,NULL),(6,NULL,'2022-02-01 15:01:56.112942','2022-02-01 15:03:59.453885',6,1,99,'','Преимущества','Мы предлагаем выгодное страхование с удобными условиями для вас<br>','advantages','',''),(7,NULL,'2022-02-01 15:09:50.421314','2022-02-01 15:09:50.427610',7,1,3,'','Преимущества страхования','Мы предлагаем выгодное страхование с удобными условиями для вас<br>','advantages','',''),(8,NULL,'2022-02-01 15:11:40.790869','2022-02-01 15:11:40.790903',8,1,99,'','FAQ','Ответы на часто задаваемые вопросы<br>','faq','',''),(9,NULL,'2022-02-01 15:16:29.384799','2022-02-01 15:16:29.394432',9,1,3,'','Ответы на часто задаваемые вопросы','Ответы на часто задаваемые вопросы<br>','faq','',''),(10,NULL,'2022-02-01 15:17:51.342724','2022-02-01 15:18:08.812697',10,1,99,'','Мини слайдер','Наши лицензии и сертификаты качества<br>','mini_slider','',''),(11,NULL,'2022-02-01 15:21:15.358484','2022-02-01 15:21:15.368224',11,1,3,'','Лицензии','Наши лицензии и сертификаты качества<br>','mini_slider','',''),(12,NULL,'2022-02-01 15:26:43.045122','2022-02-01 15:27:55.581190',12,1,99,'','Контакты','Вы можете связаться с нашими специалистами и получить необходимую информацию<br>','contacts','',''),(13,NULL,'2022-02-01 15:32:25.124225','2022-02-01 15:32:25.130768',13,1,3,'','Консультация','Вы можете связаться с нашими специалистами и получить необходимую информацию<br>','contacts','',''),(14,NULL,'2022-02-03 15:54:39.211997','2022-02-03 15:54:39.212020',14,1,4,NULL,'Сео-тексты для товаров/услуг',NULL,'seo_for_products',NULL,NULL),(15,NULL,'2022-02-03 16:09:40.138810','2022-02-03 16:14:22.409604',15,1,3,'','Виды страховых полисов','Наши лицензии и сертификаты качества<br>','faq','',''),(16,NULL,'2022-02-04 10:51:42.567316','2022-02-04 10:59:18.040677',16,1,99,'','Форма страхования \"Хоккей\"','','form_hockey','',''),(17,NULL,'2022-02-04 10:59:47.680657','2022-02-04 10:59:47.680716',17,1,3,'','Форма страхования \"Хоккей\"','','form_hockey','',''),(18,NULL,'2022-02-06 18:51:50.325949','2022-02-06 18:51:50.339135',18,1,3,'','Контакты','Вы можете связаться с нашими специалистами и получить необходимую информацию<br>','contacts','',''),(19,NULL,'2022-02-07 09:26:02.479607','2022-02-07 09:33:56.298520',19,1,3,'','О нас','<div>\r\n			<div>\r\n				<div>\r\n					<p>Таблица страховых выплат «Детская»\r\n</p>\r\n					<p>в случае телесного повреждения (травмы) в результате несчастного случая\r\n/в процентах от страховой суммы/\r\n</p>\r\n					<p>Выплата может производиться по нескольким статьям одновременно. Если\r\nимеются основания для выплаты по нескольким пунктам внутри одной статьи, то\r\nвыплата начисляется по пункту, предусматривающему более высокий размер\r\nвыплаты. Если была произведена выплата по одному из пунктов статьи, а позднее\r\nпризнается основание для более высокой выплаты по этой же статье, то\r\nначисляется выплата по пункту, предусматривающему более высокий размер\r\nвыплаты, причем размер выплаты уменьшается на выплаченную ранее сумму. В\r\nлюбом случае сумма выплат не может превышать 100% страховой суммы по\r\nданному риску.\r\n</p>\r\n					<p>ЦЕНТРАЛЬНАЯ И ПЕРИФЕРИЧЕСКАЯ НЕРВНАЯ СИСТЕМА<span>1 \r\n						\r\n						Перелом костей черепа:<br>\r\nа) \r\n						\r\n						перелом наружной пластинки костей свода, расхождение 5\r\n</span></p>\r\n					<p>шва<span>б) \r\n						\r\n						перелом свода 15\r\nв) \r\n						\r\n						перелом основания 25\r\nг) \r\n						\r\n						перелом свода и основания 30\r\n</span></p>\r\n					<p>3 Внутричерепное травматическое кровоизлияние:<br>\r\nа) \r\n						\r\n						субарахноидальное 5\r\nб) \r\n						\r\n						эпидуральная гематома 10\r\nв) \r\n						\r\n						субдуральная (внутримозговая, внутрижелудочковая) 15\r\n</p>\r\n					<p>гематома\r\n</p>\r\n					<p>5 Ушиб головного мозга 10\r\n6 \r\n						\r\n						Неудаленные инородные тела полости черепа (за\r\n</p>\r\n					<p>исключением шовного и пластического материала) 15\r\n7 \r\n						\r\n						Повреждение спинного мозга на любом уровне, а\r\n</p>\r\n					<p>также «конского хвоста»:<br>\r\nа) \r\n						\r\n						ушиб 10\r\nб) \r\n						\r\n						сдавление, гематомиелия, частичный или полный разрыв 60\r\n</p>\r\n					<p>спинного мозга, хирургические операции на спинном мозге\r\n</p>\r\n				</div>\r\n			</div>\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Статья\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>ХАРАКТЕР ПОВРЕЖДЕНИЯ\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Размер\r\nстраховой\r\nвыплаты\r\n(в % от\r\nстраховой\r\nсуммы)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>2\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Открытый перелом костей черепа или оперативные\r\nвмешательства на головном мозге и его оболочках в\r\nсвязи с черепно-мозговой травмой, независимо от\r\nколичества оперативных вмешательств\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>+5\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>4\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Сотрясение головного мозга, подтвержденное\r\nневрологическим статусом, при сроках\r\nамбулаторного или стационарного лечения не менее\r\n10 дней\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>2\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n		</div>\r\n		<div>\r\n			\r\n			\r\n			\r\n			<div>\r\n				<div>\r\n					<ol>\r\n						<li>\r\n							<p>8 &nbsp;Периферическое повреждение (разрыв) черепно- 10\r\nмозговых нервов\r\n</p>\r\n						</li>\r\n						<li>\r\n							<p>9 &nbsp;Повреждение (разрыв) шейного, плечевого,\r\nпоясничного, крестцового сплетений и их нервов:\r\nПовреждение сплетений:\r\n</p>\r\n						</li>\r\n					</ol>\r\n					<p>а) частичный разрыв сплетения 40\r\nб) разрыв сплетения 70\r\n</p>\r\n					<p>в) на уровне лучезапястного, голеностопного сустава 10\r\nг) на уровне предплечья, голени 20\r\nд) на уровне плеча, локтевого сустава, бедра, коленного 40\r\n</p>\r\n					<p>сустава<span>е) разрыв ветвей лучевого, локтевого, пальцевого, срединного 1\r\n</span></p>\r\n					<p>(пальцевых нервов)\r\n</p>\r\n					<p>ОРГАНЫ ЗРЕНИЯ\r\n</p>\r\n					<ol>\r\n						<li>\r\n							<p>10 &nbsp;Паралич аккомодации одного глаза 15\r\n</p>\r\n						</li>\r\n						<li>\r\n							<p>11 &nbsp;Гемианопсия одного глаза 15\r\n</p>\r\n						</li>\r\n						<li>\r\n							<p>12 &nbsp;Сужение поля зрения одного глаза:\r\n</p>\r\n						</li>\r\n					</ol>\r\n					<p>а) неконцентрическое 3\r\nб) концентрическое 10\r\n</p>\r\n					<ol>\r\n						<li>\r\n							<p>13 &nbsp;Пульсирующий экзофтальм одного глаза 10\r\n</p>\r\n						</li>\r\n						<li>\r\n							<p>14 &nbsp;Проникающее ранение глазного яблока, рубцовый 10\r\n</p>\r\n							<p>трихиаз\r\n</p>\r\n						</li>\r\n						<li>\r\n							<p>15 &nbsp;Необратимое нарушение функции слезопроводящих 3\r\n</p>\r\n							<p>путей одного глаза\r\n</p>\r\n						</li>\r\n					</ol>\r\n					<ol>\r\n						<li>\r\n							<p>17 &nbsp;Повреждение одного глаза, повлекшее за собой 50\r\nполную потерю зрения одного глаза\r\n</p>\r\n						</li>\r\n						<li>\r\n							<p>18 &nbsp;Удаление в результате травмы глазного яблока, не 10\r\nобладавшего зрением\r\n</p>\r\n						</li>\r\n						<li>\r\n							<p>19 &nbsp;Перелом орбиты 10\r\n</p>\r\n						</li>\r\n					</ol>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Разрыв нервов шейного, плечевого, поясничного,\r\nкрестцового сплетений (подмышечного, лучевого,\r\nлоктевого, срединного, бедренного, седалищного,\r\nмалоберцового, большеберцового нервов):\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>16\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Ожоги II-III степени, непроникающие ранения\r\nглазного яблока, гемофтальм, смещение хрусталика\r\n(за исключением протезированного), не удаленные\r\nинородные тела глазного яблока и тканях глазницы,\r\nрубцы оболочек глазного яблока, не вызвавшие\r\nснижение зрения, эрозия роговицы<span>Поверхностные инородные тела на оболочках глаза не\r\nдают оснований для выплаты\r\n</span></p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>3\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>*Примечания: 1. Ожоги глаза без указания степени, а также ожоги глаза I степени,\r\nне повлекшие за собой патологических изменений, не дают оснований для\r\nстраховой выплаты.\r\n</p>\r\n						<p>2. Решение о страховой выплате по ст. 9 – 19 в общем случае принимается по\r\nитогам освидетельствования, проведенного после окончания лечения, но не ранее\r\n3-х месяцев со дня травмы (при условии сохранения диагноза на этот момент). По\r\nотдельным диагнозам возможна немедленная выплата.<br>\r\n3. Сумма выплат по ст.9 -19 не должна превышать 50% на один глаз.\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n		</div>\r\n		<div>\r\n			\r\n			<div>\r\n				<div>\r\n					<p>ОРГАНЫ СЛУХА<span>20 Повреждение ушной раковины, повлекшее за собой:<br>\r\nа) рубцовую деформацию или отсутствие 1/3 ушной раковины 3\r\nб) отсутствие половины ушной раковины 5\r\nв) полное отсутствие ушной раковины 10\r\n21 Травматическое снижение слуха, подтвержденное\r\n</span></p>\r\n					<p>аудиометрией:<br>\r\nа) на одно ухо 5\r\nб) полную глухоту (анакузия) (разговорная речь 0) 30\r\n22 Разрыв барабанной перепонки, наступивший в\r\n</p>\r\n					<p>результате травмы, без снижения слуха 5\r\n</p>\r\n					<p>ДЫХАТЕЛЬНАЯ СИСТЕМА<span>23 \r\n						\r\n						Перелом костей носа, передней стенки лобной, 1\r\n</span></p>\r\n					<p>гайморовой пазух, решетчатой кости\r\n</p>\r\n					<p>а) с одной стороны 10\r\nб) \r\n						\r\n						с двух сторон 20\r\n25 \r\n						\r\n						Повреждение легкого, повлекшее за собой:<br>\r\nа) \r\n						\r\n						удаление сегмента или нескольких сегментов легкого 15\r\nб) \r\n						\r\n						удаление доли легкого 30\r\nв) \r\n						\r\n						удаление одного легкого 50\r\n26 \r\n						\r\n						Перелом грудины 5\r\n27 \r\n						\r\n						Переломы двух или более ребер:\r\n</p>\r\n					<p>а) \r\n						\r\n						двух ребер 1\r\nб) \r\n						\r\n						трех и более 3\r\n28 \r\n						\r\n						Проникающее ранение грудной клетки, торакотомия\r\n</p>\r\n					<p>(независимо от количества) по поводу травмы:<br>\r\nа) \r\n						\r\n						при отсутствии травматического повреждения органов 3\r\n</p>\r\n					<p>грудной клетки<span>б) \r\n						\r\n						при травматическом повреждении органов грудной клетки 10\r\n*Примечание: Если легкое или его часть были удалены по причине ранения\r\nгрудной клетки, ст. 28 не применяется.<span>29 \r\n						\r\n						Повреждение гортани, трахеи, перелом 10\r\n</span></span></p>\r\n					<p>подъязычной кости\r\n</p>\r\n					<p>*Примечание: Если предусмотрены выплаты по ст. 30, ст.29 не применяется.\r\n</p>\r\n					<p>СЕРДЕЧНО-СОСУДИСТАЯ СИСТЕМА\r\n</p>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>*Примечания: Разрыв барабанной перепонки при переломах основания черепа не\r\nдаёт основания для выплаты по этой статье. Решение о выплате по ст. 20-22 в\r\nобщем случае принимается после окончания лечения, но не ранее 6 месяцев со дня\r\nтравмы, при условии сохранения диагноза на момент выплаты. Если выплата\r\nпроизводится по ст. 1 п. (в, г) ст. 21 не применяется.\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>24\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Повреждение легкого, вызвавшее подкожную\r\nэмфизему, гемоторакс, пневмонию, экссудативный\r\nплеврит; инородное тело (тела) грудной полости:\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>30\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Повреждение гортани, трахеи, подъязычной кости,\r\nщитовидного хряща, ожог верхних дыхательных\r\nпутей повлекшие за собой ношение\r\nтрахеостомической трубки\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>20\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n		</div>\r\n		<div>\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>31\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Повреждение сердца, эндо-, мио- и эпикарда и\r\nкрупных магистральных сосудов, повлекшее за\r\nсобой сердечно-сосудистую недостаточность\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>35\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n				<tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>32\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Повреждение сердца, эндо-, мио- и эпикарда,\r\nкрупных магистральных или периферических\r\nсосудов, не повлекшее за собой сердечно-\r\nсосудистую недостаточность\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>5\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n				<tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>33\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Повреждение крупных периферических сосудов,\r\nповлекшее за собой сердечно-сосудистую\r\nнедостаточность\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>25\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n				<tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>*Примечания:<br>\r\n1. К крупным магистральным сосудам следует относить: аорту, легочную,\r\nбезымянную, сонные артерии, внутренние яремные вены, верхнюю и нижнюю\r\nполые вены, воротную вену, а также магистральные сосуды, обеспечивающие\r\nкровообращение внутренних органов.<br>\r\n2. К крупным периферическим сосудам следует относить: подключичные,\r\nподмышечные (подкрыльцовые), плечевые локтевые и лучевые артерии,\r\nподвздошные, бедренные, подколенные, передние и задние большеберцовые\r\nартерии; плечеголовные, подключичные, подмышечные, бедренные и подколенные\r\nвены.<br>\r\n3. Выплата по ст.31 или ст.33 производится, если указанные осложнения будут\r\nустановлены по истечении 6 месяцев после травмы. При выплате по ст.31 или ст.33\r\nвыплата, сделанная ранее по ст.32, удерживается.\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			<div>\r\n				<div>\r\n					<p>ОРГАНЫ ПИЩЕВАРЕНИЯ<span>34 Переломы челюсти:<br>\r\nа) верхней челюсти, скуловых костей 5\r\nб) нижней челюсти 5\r\n35 Повреждение челюсти, повлекшее за собой:<br>\r\nа) отсутствие части челюсти (за исключением альвеолярного 40\r\n</span></p>\r\n					<p>отростка)<span>б) отсутствие челюсти 60\r\n*Примечание: При выплате по ст.35 учтена и потеря зубов (независимо от их\r\nколичества). Если предусмотрены выплаты по ст. 35, то ст. 34 не применяется.\r\n36 \r\n						\r\n						Повреждение языка, повлекшее за собой:<br>\r\nа) \r\n						\r\n						отсутствие языка на уровне дистальной трети 10<span>б) \r\n						\r\n						на уровне средней трети 30<span>в) \r\n						\r\n						на уровне корня, полное отсутствие 50\r\n</span></span></span></p>\r\n					<p>38 Повреждение пищевода, вызвавшее его сужение 30\r\n39 \r\n						\r\n						Повреждение органов пищеварения, повлекшее за\r\n</p>\r\n					<p>собой:<br>\r\nа) \r\n						\r\n						рубцовое сужение желудка, кишечника, заднепроходного 15\r\n</p>\r\n					<p>отверстия<span>б) \r\n						\r\n						спаечную болезнь, состояние после операции по поводу 25\r\n</span></p>\r\n					<p>спаечной непроходимости<span>в) \r\n						\r\n						кишечный свищ, кишечно-влагалищный свищ, свищ 40\r\n</span></p>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>37\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Повреждение желчного пузыря в результате\r\nтравмы, повлекшее за собой удаление желчного\r\nпузыря\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>10\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			<div>\r\n				<div>\r\n					<p>поджелудочной железы\r\n</p>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n		</div>\r\n		<div>\r\n			\r\n			<div>\r\n				<div>\r\n					<p>г) \r\n						\r\n						наложение колостомы, при условии сохранения колостомы 50\r\nпо истечению 6 мес. после травмы\r\n</p>\r\n					<p>40 \r\n						\r\n						Повреждение печени в результате травмы,\r\nповлекшее за собой:\r\n</p>\r\n					<p>а) \r\n						\r\n						подкапсульный разрыв печени, потребовавший 20\r\nоперативного вмешательства\r\n</p>\r\n					<p>б) \r\n						\r\n						подкапсульный разрыв печени, не потребовавший 5\r\nоперативного вмешательства\r\n</p>\r\n					<p>в) \r\n						\r\n						удаление более половины печени в результате травмы 30\r\n</p>\r\n					<p>41 Повреждение селезенки, повлекшее за собой:<br>\r\nа) \r\n						\r\n						подкапсульный разрыв селезенки, не потребовавший 10\r\n</p>\r\n					<p>оперативного вмешательства<span>б) \r\n						\r\n						удаление селезенки 20\r\n42 \r\n						\r\n						Повреждения желудка, поджелудочной железы,\r\n</span></p>\r\n					<p>кишечника, брыжейки, повлекшие за собой:<br>\r\nа) \r\n						\r\n						удаление части до 1/3 желудка, 1/3 кишечника 15\r\nб) \r\n						\r\n						удаление части 1/2 желудка, 1/3 хвоста поджелудочной 25\r\n</p>\r\n					<p>железы, 1/2 кишечника<span>в) \r\n						\r\n						удаление части 2/3 желудка, 2/3 кишечника, 2/3 тела 40\r\n</span></p>\r\n					<p>поджелудочной железы<span>г) \r\n						\r\n						удаление желудка, 2/3 поджелудочной железы, кишечника 50\r\nМОЧЕПОЛОВАЯ СИСТЕМА<span>43 \r\n						\r\n						Повреждение почки, повлекшее за собой:\r\n</span></span></p>\r\n					<p>б) удаление почки 50\r\n44 \r\n						\r\n						Повреждение органов мочевыделительной системы,\r\n</p>\r\n					<p>повлекшее за собой:\r\n</p>\r\n					<p>б) непроходимость мочеточника, мочеиспускательного канала, 40\r\nмочеполовые свищи\r\n</p>\r\n					<p>*Примечание: Если производится выплата по ст. 43, ст. 45 не применяется\r\n</p>\r\n					<p>46 \r\n						\r\n						Повреждение половой системы, повлекшее за собой:\r\nУ женщин:\r\n</p>\r\n					<p>а) \r\n						\r\n						потерю одного яичника, яичника и одной маточной трубы, 15\r\nяичника и двух маточных труб\r\n</p>\r\n					<p>б) \r\n						\r\n						потерю двух яичников (единственного яичника) 25\r\nв) \r\n						\r\n						потерю матки с трубами 50\r\nг) \r\n						\r\n						потерю одной молочной железы 15\r\nд) \r\n						\r\n						потерю двух молочных желез 30\r\n</p>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>*Примечание: При наличии вирусного или токсического поражения печени до\r\nнаступления несчастного случая, размер выплаты по травме печени составит 50%\r\nот размера, указанного в ст.40.\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>а)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>удаление части почки, хроническую почечную\r\nнедостаточность (если это осложнение имеется по\r\nистечении 6 месяцев после травмы)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>20\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>а)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>терминальную стадию острой почечной недостаточности в\r\nрезультате травмы органов мочевыделительной системы\r\nили травматического токсикоза\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>50\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>45\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Повреждение органов мочевыделительной системы,\r\nв связи с которым произведено одно или несколько\r\nоперативных вмешательств\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>10\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n		</div>\r\n		<div>\r\n			\r\n			\r\n			\r\n			<div>\r\n				<div>\r\n					<p>У мужчин:<br>\r\nе) \r\n						\r\n						потерю двух яичек, части полового члена 30\r\nж) \r\n						\r\n						потерю полового члена 40\r\nз) \r\n						\r\n						потерю полового члена и одного или двух яичек 50\r\nМЯГКИЕ ТКАНИ\r\n</p>\r\n					<p>а) 1% - 2% поверхности тела 1\r\nб) \r\n						\r\n						3% - 5% поверхности тела 3\r\nв) \r\n						\r\n						6% - 9% поверхности тела 10\r\nг) \r\n						\r\n						10% -20% поверхности тела 20\r\nд) \r\n						\r\n						21%-30% поверхности тела 30\r\nе) \r\n						\r\n						31% и более 60\r\n</p>\r\n					<p>а) образование рубцов площадью от 5 см2 и более или общей 10\r\nдлиной 5 см и более\r\n</p>\r\n					<p>б) \r\n						\r\n						образование рубцов площадью от 10 см2 и более или общей 20\r\nдлиной 15 см и более\r\n</p>\r\n					<p>50 Ожоговая болезнь, ожоговый шок 10\r\n</p>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>47\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Размеры страховой выплаты при ожогах II - IV\r\nстепени, за исключением ожогов, возникших в\r\nрезультате воздействия<br>\r\nультрафиолетового (солнечного) излучения,\r\nприведены в последнем разделе настоящей Таблицы\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>-\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n				<tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>48\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Повреждения (кроме ожогов) мягких тканей\r\nволосистой части головы, туловища, конечностей,\r\nприведших к образованию рубцового повреждения:\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>49\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Повреждения мягких тканей лица, передне-боковой\r\nповерхности шеи, подчелюстной области, ушных\r\nраковин, повлекшие за собой:\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>*Примечания: Если была произведена выплата по ст.47, выплата по ст.49\r\nосуществляется за вычетом ранее произведенной по ст.47 выплаты. При открытых\r\nпереломах костей и операциях выплата за рубцы не производится.\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n		</div>\r\n		<div>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>*Примечания:<br>\r\n1. К косметически заметным, подлежащим оценке по ст.48 и ст.49, относятся рубцы,\r\nотличающиеся по окраске от окружающей кожи, втянутые или выступающие над ее\r\nповерхностью, стягивающие ткани.<br>\r\n2. Площадь рубцов определяется после проведения лечения, на момент истечения\r\n3 месяцев после травмы. Площадь ожогов определяется по состоянию на момент\r\nистечения 10 дней после травмы.<br>\r\n3. Если косметическое нарушение наступило в результате переломов костей\r\nлицевого черепа или оперативных вмешательствах на костях лицевого черепа,\r\nвызванных травмой, то выплата производится с учетом и перелома, и\r\nпослеоперационного рубца путем суммирования. В остальных случаях выплата за\r\nпослеоперационный рубец или рубец, образовавшийся в результате открытого\r\nперелома, не производится. При определении площади рубцов следует учитывать и\r\nрубцы, образовавшиеся на месте взятия для замещения пораженного участка кожи\r\nкожного трансплантата.<br>\r\n4. 1% поверхности тела исследуемого равен площади ладонной поверхности его\r\nкисти и пальцев. Эта площадь определяется в квадратных сантиметрах путем\r\nумножения длины кисти, измеряемой от лучезапястного сустава до верхушки\r\nногтевой фаланги III пальца на ее ширину, измеряемую на уровне головок II - V\r\nпястных костей (без учета I пальца).\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n			<div>\r\n				<div>\r\n					<p>ПОЗВОНОЧНИК<span>51 \r\n						\r\n						Перелом тела, дуги, суставных отростков позвонков\r\n</span></p>\r\n					<p>(за исключением крестца и копчика):<br>\r\nа) \r\n						\r\n						одного-двух позвонков, если хирургические операции на 15\r\n</p>\r\n					<p>позвонках не производились\r\n</p>\r\n					<p>*Примечание: При рецидивах вывиха/подвывиха позвонка страховая выплата не\r\nпроизводится.<span>53 \r\n						\r\n						Перелом поперечных или остистых отростков:<br>\r\nа) \r\n						\r\n						одного-двух 5\r\n</span></p>\r\n					<p>б) \r\n						\r\n						трех и более 10\r\n*Примечание: Если предусмотрены выплаты по ст.51, ст.53 не применяется\r\n54 \r\n						\r\n						Перелом крестца 10\r\n55 \r\n						\r\n						Повреждение копчика:\r\n</p>\r\n					<p>а) \r\n						\r\n						перелом копчиковых позвонков 10\r\nб) \r\n						\r\n						удаление копчиковых позвонков в связи с травмой 15\r\nВЕРХНЯЯ КОНЕЧНОСТЬ (ЗА КАЖДУЮ РУКУ)<br>\r\nЛОПАТКА, КЛЮЧИЦА\r\n</p>\r\n					<p>а) перелом одной кости, отрыв клювовидного отростка 5\r\nлопатки, разрыв связок одного сочленения\r\n</p>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>б)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>трех- и более позвонков, хирургические операции на\r\nпозвонках или остистых отростках (кроме копчика), в том\r\nчисле замена или удаление позвонков (кроме копчика)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>20\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n				<tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>52\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Полный разрыв межпозвоночных связок (при\r\nгоспитализации не менее 14 дней), вывих\r\nпозвонков (за исключением копчика)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>10\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>56\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Перелом лопатки (кроме суставной впадины),\r\nключицы, полный или частичный разрыв связок\r\nакромиально-ключичного, грудино-ключичного\r\nсочленений:\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n		</div>\r\n		<div>\r\n			\r\n			<div>\r\n				<div>\r\n					<p>б) \r\n						\r\n						перелом двух костей, двойной перелом одной кости, разрыв 10\r\nсвязок двух сочленений, перелом-вывих ключицы\r\n</p>\r\n					<p>ПЛЕЧЕВОЙ СУСТАВ\r\n</p>\r\n					<p>б) перелом двух костей, перелом-вывих 10\r\n</p>\r\n					<p>58 Повреждение плечевого сустава, повлекшее за\r\nсобой:\r\n</p>\r\n					<p>б) \"болтающийся\" плечевой сустав в результате резекции\r\nсуставных поверхностей составляющих его костей 40\r\n</p>\r\n				</div>\r\n			</div>\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>в)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>несросшийся перелом (ложный сустав), перелом двух\r\nкостей и разрыв одного сочленения. Выплата по ст.56,\r\nпункт в) по диагнозу «несросшийся перелом (ложный\r\nсустав)» производится не ранее, чем через 9 месяцев со\r\nдня травмы при условии сохранения диагноза на момент\r\nвыплаты.\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>15\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>57\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Повреждение плечевого сустава (перелом суставной\r\nвпадины лопатки, головки плечевой кости,\r\nанатомической шейки плечевой кости или лопатки,\r\nотрывы бугорков плечевой кости, разрыв связок или\r\nсуставной капсулы):\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					\r\n				</tr>\r\n				<tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>а)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>разрыв связок или суставной капсулы, перелом одной\r\nкости, отрывы бугорков плечевой кости, вывих плеча\r\n(кроме привычного вывиха плеча)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>5\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>в)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>несросшийся перелом. Выплата по ст.57, пункт в)\r\nпроизводится не ранее, чем через 9 месяцев со дня травмы\r\nпри условии сохранения диагноза на момент выплаты.\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>20\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>а)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>отсутствие движений в суставе (анкилоз). Выплата по ст.58,\r\nпункт а) производится не ранее, чем через 9 месяцев со\r\nдня травмы при условии сохранения диагноза на момент\r\nвыплаты.\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>30\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>*Примечания: Если по причине повреждений, перечисленных в ст.56, 57 и 58,\r\nпроводились хирургические вмешательства, дополнительной выплате подлежит\r\n10% страховой суммы. При этом дополнительная выплата за взятие трансплантата\r\nне производится.\r\n</p>\r\n						<p>Если в связи с травмой плечевого сустава производилась выплата по ст.57, а затем\r\nвозникли осложнения, перечисленные в ст.58, выплаты производятся в\r\nсоответствии с одним из подпунктов ст.58, за вычетом ранее произведенной\r\nвыплаты.\r\n</p>\r\n						<p>Примечание к ст. 57: При рецидивах вывиха/подвывиха плеча страховая выплата\r\nне производится\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n			<div>\r\n				<div>\r\n					<p>ПЛЕЧО<span>59 Перелом плечевой кости на любом уровне* (за\r\n</span></p>\r\n					<p>исключением суставов):<br>\r\nа) без смещения 10\r\nб) со смещением, двойной перелом 15\r\n</p>\r\n					<p>*Примечание: рефрактуры (фокальные и парафокальные)\r\n</p>\r\n					<p>не являются основанием для страховой выплаты<span>60 Перелом плечевой кости, осложнённый 35\r\n</span></p>\r\n					<p>образованием ложного сустава\r\n</p>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n		</div>\r\n		<div>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>*Примечание: Выплата по ст.60 производится не ранее, чем через 9 месяцев со дня\r\nтравмы при условии сохранения диагноза на момент выплаты.<br>\r\nЕсли в связи с травмой плечевого сустава производилась выплата по ст.59, а затем\r\nвозникли осложнения, указанные в ст.60, выплаты производятся в соответствии со\r\nст.60, за вычетом ранее произведенной выплаты.\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n			<div>\r\n				<div>\r\n					<p>ЛОКТЕВОЙ СУСТАВ\r\n</p>\r\n					<p>б) перелом двух или трех костей, перелом одной-двух костей 10\r\nи разрыв связок / капсулы\r\n</p>\r\n					<p>в) \r\n						\r\n						перелом костей со смещением отломков 15\r\n62 \r\n						\r\n						Повреждение области локтевого сустава, повлекшее\r\n</p>\r\n					<p>за собой:\r\n</p>\r\n					<p>б) \"болтающийся\" локтевой сустав (в результате резекции\r\nсуставных поверхностей составляющих его костей) 40\r\n</p>\r\n					<p>ПРЕДПЛЕЧЬЕ<span>63 \r\n						\r\n						Перелом костей предплечья (локтевой, лучевой) на\r\n</span></p>\r\n					<p>любом уровне, за исключением области суставов*<br>\r\nа) \r\n						\r\n						перелом одной кости 3\r\nб) \r\n						\r\n						перелом двух костей 10\r\n</p>\r\n					<p>*Примечание: рефрактуры (фокальные и парафокальные)\r\n</p>\r\n					<p>не являются основанием для страховой выплаты\r\n</p>\r\n					<p>ЛУЧЕЗАПЯСТНЫЙ СУСТАВ\r\n</p>\r\n					<p>а) перелом костей 3<span>б) \r\n						\r\n						полный или частичный разрыв связок 1<span>65 \r\n						\r\n						Травматический анкилоз лучезапястного сустава 10\r\n*Примечание: Выплата по ст.65 производится не ранее, чем через 9 месяцев со дня\r\nтравмы при условии сохранения диагноза на момент выплаты.\r\n</span></span></p>\r\n					<p>КОСТИ КИСТИ\r\n</p>\r\n				</div>\r\n			</div>\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>61\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Повреждения области локтевого сустава (перелом в\r\nобласти суставных поверхностей, анатомической\r\nшейки локтевой, лучевой, плечевой костей, разрыв\r\nсвязок или капсулы сустава):\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					\r\n				</tr>\r\n				<tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>а)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>перелом одной кости, отрыв костных\r\nфрагментов/отростков, разрыв связок (полный или\r\nчастичный разрыв) или капсулы сустава\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>5\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>а)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>отсутствие движений в суставе. Выплата по ст.61, пункт а)\r\nпроизводится не ранее, чем через 9 месяцев со дня травмы\r\nпри условии сохранения диагноза на момент выплаты.\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>30\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>*Примечания: Если по причине повреждений, перечисленных в ст. 61 и 62,\r\nпроводились хирургические вмешательства, дополнительной выплате подлежит\r\n10% страховой суммы. При этом дополнительная выплата за взятие трансплантата\r\nне производится.<br>\r\nЕсли в связи с травмой локтевого сустава производилась выплата по ст.61, а затем\r\nвозникли осложнения, перечисленные в ст.62, выплаты производятся в\r\nсоответствии с одним из подпунктов ст.62, за вычетом ранее произведенной\r\nвыплаты.\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>64\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Перелом костей предплечья в области дистального\r\nметафиза, межсуставный перелом костей,\r\nсоставляющих лучезапястный сустав, полный или\r\nчастичный разрыв связок:\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n		</div>\r\n		<div>\r\n			\r\n			<div>\r\n				<div>\r\n					<p>66 \r\n						\r\n						Перелом или вывих костей:<br>\r\nа) \r\n						\r\n						одной кости (за исключением ладьевидной) 1\r\nб) \r\n						\r\n						двух и более костей (за исключением ладьевидной), 3\r\n</p>\r\n					<p>ладьевидной кости\r\n</p>\r\n					<p>ПАЛЬЦЫ КИСТИ: ПЕРВЫЙ ПАЛЕЦ (БОЛЬШОЙ ПАЛЕЦ)<span>67 \r\n						\r\n						Перелом, разрыв сухожилий или капсулы суставов\r\n</span></p>\r\n					<p>3\r\n</p>\r\n					<p>68 \r\n						\r\n						Повреждение пальца, повлекшее за собой\r\nотсутствие движений:\r\n</p>\r\n					<p>а) \r\n						\r\n						в одном суставе 1<span>б) \r\n						\r\n						в двух суставах 3\r\n*Примечание: Выплата по ст.68 производится не ранее, чем через 6 месяцев со дня\r\nтравмы при условии сохранения диагноза на момент выплаты.<span>69 \r\n						\r\n						Потеря первого пальца 15\r\nПАЛЬЦЫ КИСТИ: ВТОРОЙ, ТРЕТИЙ, ЧЕТВЕРТЫЙ, ПЯТЫЙ ПАЛЬЦЫ<span>70 \r\n						\r\n						Перелом, разрыв сухожилий или капсулы суставов 1\r\n</span></span></span></p>\r\n					<p>пальца - за каждый палец<span>71 \r\n						\r\n						Потеря второго пальца 5\r\n72 \r\n						\r\n						Потеря третьего, четвёртого, пятого пальца - за 3\r\n</span></p>\r\n					<p>каждый палец\r\n</p>\r\n					<p>НИЖНЯЯ КОНЕЧНОСТЬ (ЗА КАЖДУЮ НОГУ)<br>\r\nТАЗ<span>74 \r\n						\r\n						Перелом костей таза:<br>\r\nа) \r\n						\r\n						перелом крыла подвздошной кости 10\r\nб) \r\n						\r\n						перелом лонной, седалищной кости, тела подвздошной 10\r\n</span></p>\r\n					<p>кости, вертлужной впадины<span>в) \r\n						\r\n						перелом двух и более костей или двойной перелом одной 15\r\n</span></p>\r\n					<p>кости\r\n</p>\r\n					<p>75 \r\n						\r\n						Разрыв лонного, крестцово-подвздошного\r\nсочленения:\r\n</p>\r\n					<p>а) \r\n						\r\n						одного сочленения 10\r\nб) \r\n						\r\n						двух и более сочленений 15\r\n76 \r\n						\r\n						Перелом головки, шейки бедра вывих бедра,\r\n</p>\r\n					<p>полный или частичный разрыв связок:<br>\r\nа) \r\n						\r\n						перелом головки, шейки, вывих бедра 10\r\nб) \r\n						\r\n						полный и частичный разрыв связок 5\r\n77 \r\n						\r\n						Повреждение тазобедренного сустава, повлекшее за\r\n</p>\r\n					<p>собой:\r\n</p>\r\n					<p>б) \"болтающийся\" сустав (в результате резекции головки 40\r\nбедра, вертлужной впадины)\r\n</p>\r\n					<p>*Примечание к ст. 76: При рецидивах вывиха/подвывиха бедра страховая выплата\r\nне производится.<span>БЕДРО\r\n</span></p>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>73\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Травматическая ампутация всех пальцев руки или\r\nповреждение, приведшее к ампутации всех пальцев\r\nруки\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>40\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>а)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>отсутствие движений (анкилоз). Выплата по ст.77, пункт а)\r\nпроизводится не ранее, чем через 9 месяцев со дня травмы\r\nпри условии сохранения диагноза на момент выплаты.\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>20\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n		</div>\r\n		<div>\r\n			\r\n			<div>\r\n				<div>\r\n					<p>78 \r\n						\r\n						Перелом бедра на любом уровне (за исключением\r\nобласти суставов):\r\n</p>\r\n					<p>а) \r\n						\r\n						без смещения отломков 15\r\nб) \r\n						\r\n						со смещением, двойной перелом бедра 20\r\n79 \r\n						\r\n						Перелом бедра, осложнившийся образованием\r\n</p>\r\n					<p>ложного сустава (несросшийся перелом) 50\r\n</p>\r\n					<p>КОЛЕННЫЙ СУСТАВ<span>80 Повреждение области коленного сустава, повлекшее\r\n</span></p>\r\n					<p>за собой:<br>\r\nа) Разрыв мениска (менисков), разрыв связок, отрывы\r\n</p>\r\n					<p>костного фрагмента (фрагментов), гемартроз 3\r\nб) перелом коленной чашечки 10\r\n</p>\r\n					<p>81 Повреждение коленного сустава, повлекшее за\r\nсобой:\r\n</p>\r\n					<p>б) болтающийся\" коленный сустав (в результате резекции 25\r\nсуставных поверхностей составляющих его костей)\r\n</p>\r\n					<p>ГОЛЕНЬ<span>82 Перелом костей голени* (за исключением области\r\n</span></p>\r\n					<p>суставов):<br>\r\nа) малоберцовой кости 5\r\nб) большеберцовой, двойной перелом малоберцовой 10\r\nв) обеих костей, двойной перелом большеберцовой 15\r\n</p>\r\n					<p>*Примечание: рефрактуры (фокальные и парафокальные)\r\n</p>\r\n					<p>не являются основанием для страховой выплаты\r\n</p>\r\n					<p>ГОЛЕНОСТОПНЫЙ СУСТАВ<span>83 \r\n						\r\n						Повреждение области голеностопного сустава:<br>\r\nа) \r\n						\r\n						перелом одной лодыжки или края большеберцовой кости, 5\r\n</span></p>\r\n					<p>разрыв связок или суставной капсулы\r\n</p>\r\n					<p>84 Повреждение голеностопного сустава, повлекшее за\r\nсобой:\r\n</p>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			<div>\r\n				<div>\r\n					<div>\r\n						<p>*Примечания: Выплата по ст.79 производится не ранее, чем через 9 месяцев со дня\r\nтравмы при условии сохранения диагноза на момент выплаты.<br>\r\nЕсли в связи с травмой производилась выплата по ст.78, а затем возникли\r\nосложнения, перечисленные в ст.79, выплаты производятся в соответствии со\r\nст.79, за вычетом ранее произведенной выплаты.\r\n</p>\r\n					</div>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>в)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>перелом костей, составляющих коленный сустав\r\n(дистальный эпифиз бедра и проксимальный эпифиз\r\nбольшеберцовой кости)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>20\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>а)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>отсутствие движений в суставе (анкилоз). Выплата по ст.80,\r\nпункт а) производится не ранее, чем через 9 месяцев со\r\nдня травмы при условии сохранения диагноза на момент\r\nвыплаты.\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>20\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>б)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>перелом обеих лодыжек (костей голени), перелом лодыжки\r\nс краем большеберцовой кости, разрыв дистального\r\nмежберцового синдесмоза\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>10\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n				<tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>в)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>перелом одной или двух лодыжек с краем большеберцовой\r\nкости и разрыв дистального межберцового синдесмоза в\r\nсочетании с подвывихом (вывихом) стопы\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>20\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			\r\n		</div>\r\n		<div>\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>а)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>отсутствие движений в суставе (анкилоз). Выплата по ст.83,\r\nпункт а) производится не ранее, чем через 9 месяцев со\r\nдня травмы при условии сохранения диагноза на момент\r\nвыплаты.\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>20\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n				<tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>б)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>\"болтающийся\" голеностопный сустав (в результате\r\nрезекции) суставных поверхностей составляющих его\r\nкостей.\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>25\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			<div>\r\n				<div>\r\n					<p>85 Полный разрыв ахиллова сухожилия 2\r\nСТОПА, ПАЛЬЦЫ НОГ<span>86 \r\n						\r\n						Переломы костей, разрыв связок стопы:<br>\r\nа) \r\n						\r\n						перелом одной-двух костей (кроме боковой кости), разрыв 1\r\n</span></p>\r\n					<p>связок<span>б) \r\n						\r\n						перелом трех и более костей, пяточной кости 5\r\n87 \r\n						\r\n						Переломы, разрывы сухожилий одного или более\r\n</span></p>\r\n					<p>пальцев одной стопы:\r\n</p>\r\n					<p>88 Травматическая ампутация или повреждение,\r\nприведшее к ампутации пальцев ног:\r\n</p>\r\n					<p>а) \r\n						\r\n						большого пальца 2\r\nб) \r\n						\r\n						второго, третьего, четвертого, пятого пальцев - за каждый 1\r\n</p>\r\n					<p>палец\r\n</p>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>перелом или вывих одной или нескольких фаланг,\r\nповреждение сухожилий (полный или частичный разрыв)\r\nодного или более пальцев\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>1\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n			</tbody></table>\r\n			\r\n			\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>89\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Повреждение, повлекшее развитие\r\nпосттравматического тромбофлебита, лимфостаза,\r\nостеомиелита, нарушение трофики\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>1\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n				<tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>*Примечания: Ст.89 применяется при тромбофлебите, лимфостазе и нарушениях\r\nтрофики, вызванных травмой опорно-двигательного аппарата (за исключением\r\nповреждения крупных периферических сосудов и нервов), через 6 месяцев со дня\r\nтравмы, при подтверждении диагноза на момент выплаты. Нагноительные\r\nвоспаления пальцев не дают оснований для выплаты.\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n				<tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>90\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Травматический шок или шок, развившийся\r\nвследствие острой кровопотери, связанной с\r\nтравмой (геморрагический шок)\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>5\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n				</tr>\r\n				<tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>91\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Если в результате несчастного случая, наступившего\r\nв течение срока страхования, получено телесное\r\nповреждение, не предусмотренное настоящей\r\n\"Таблицей\", то страховая выплата производится\r\nисходя из срока непрерывного лечения в ЛПУ,\r\nпрямой причиной которого является указанный\r\nнесчастный случай, что подтверждено\r\nсоответствующей справкой от лечащего врача и\r\nкопией амбулаторной карты за период лечения,\r\nзаверенной медицинского учреждения, где\r\nпроводилось лечение*\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					\r\n				</tr>\r\n			</tbody></table>\r\n			<div>\r\n				<div>\r\n					<p>а) амбулаторное лечение от 9 до 14 календарных дней 1\r\nб) \r\n						\r\n						амбулаторное лечение от 15 до 30 календарных дней 3\r\nв) \r\n						\r\n						амбулаторное лечение от 31 календарных дней и более 5\r\n</p>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n		</div>\r\n		<div>\r\n			<table>\r\n				<tbody><tr>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>92\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					<td>\r\n						<div>\r\n							<div>\r\n								<p>Если в результате несчастного случая, наступившего\r\nв течение срока страхования, получено телесное\r\nповреждение, не предусмотренное настоящей\r\n\"Таблицей\" и потребовавшее стационарного\r\nлечения, то страховая выплата производится\r\nисходя из срока непрерывного пребывания на\r\nстационарном лечении, прямой причиной которого\r\nявляется указанный несчастный случай, что\r\nподтверждено соответствующим выписным\r\nэпикризом (копией истории болезни) медицинского\r\nучреждения, где проводилось стационарное\r\nлечение*\r\n</p>\r\n							</div>\r\n						</div>\r\n					</td>\r\n					\r\n				</tr>\r\n			</tbody></table>\r\n			<div>\r\n				<div>\r\n					<p>а) стационарное лечение от 3 до 14 календарных дней 3\r\nб) \r\n						\r\n						стационарное лечение от 15 до 30 календарных дней 5\r\nв) \r\n						\r\n						стационарное лечение от 31 календарных дней и более 10\r\n</p>\r\n					<p>*Примечания: Если в связи с травмой существуют основания для выплаты по ст.\r\n91 и по ст.92, то размер выплаты рассчитывается в зависимости от количества\r\nдней амбулаторного (по ст. 91) и стационарного (по ст.92) лечения.<span>РАЗМЕРЫ СТРАХОВОЙ ВЫПЛАТЫ ПРИ ОЖОГАХ\r\n</span></p>\r\n					<p>(определение размера выплаты по ст.46 настоящей Таблицы в % от\r\n</p>\r\n					<p>страховой суммы)<br>\r\nПлощадь ожога Степень ожога\r\n</p>\r\n				</div>\r\n			</div>\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			\r\n			<div>\r\n				<div>\r\n					<p>в % от поверхности<br>\r\nтела<br>\r\nОжоги мягких тканей волосистой части головы, туловища, конечностей\r\n1-2 1 2 3<span>3-5 2 4 5<span>6-9 \r\n						\r\n						5 \r\n						9 \r\n						10<span>10-20 \r\n						\r\n						15 \r\n						17 \r\n						20<span>21-30 \r\n						\r\n						25 \r\n						28 \r\n						30<span>31-40 \r\n						\r\n						50 \r\n						55 \r\n						60<span>41-60 \r\n						\r\n						70 \r\n						80 \r\n						80<span>61-90 \r\n						\r\n						80 \r\n						100 \r\n						100<span>Более 90 \r\n						\r\n						\r\n						\r\n						100 \r\n						\r\n						100 \r\n						\r\n						100\r\nОжоги мягких тканей лица, передне-боковой поверхности шеи,\r\nподчелюстной области, ушных раковин<span>1-2 5 10 15<span>3-4 10 15 20<span>5-6 15 25 30<span>7-8 20 30 40&nbsp;</span></span></span></span></span></span></span></span></span></span></span></span></p>\r\n				</div>\r\n			</div>\r\n		</div><br>','advantages','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_linkcontainer`
--

LOCK TABLES `flatcontent_linkcontainer` WRITE;
/*!40000 ALTER TABLE `flatcontent_linkcontainer` DISABLE KEYS */;
INSERT INTO `flatcontent_linkcontainer` VALUES (16,NULL,'2022-02-03 16:11:52.562443','2022-02-03 16:11:52.562478',6,1,NULL,NULL,23,15),(17,NULL,'2022-02-04 11:00:27.695975','2022-02-04 11:00:27.695998',7,1,NULL,NULL,16,17),(18,NULL,'2022-02-04 11:00:27.697410','2022-02-04 11:00:27.697432',8,1,NULL,NULL,16,7),(19,NULL,'2022-02-04 11:00:27.698799','2022-02-04 11:00:27.698821',9,1,NULL,NULL,16,9),(20,NULL,'2022-02-04 11:00:27.700228','2022-02-04 11:00:27.700263',10,1,NULL,NULL,16,11),(21,NULL,'2022-02-04 11:00:27.701616','2022-02-04 11:00:27.701640',11,1,NULL,NULL,16,13),(22,NULL,'2022-02-06 18:52:21.005186','2022-02-06 18:52:21.005208',12,1,NULL,NULL,24,18);
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
INSERT INTO `login_customuser` VALUES (1,NULL,'2022-02-01 14:04:55.827711','2022-02-01 14:09:24.920305',1,1,NULL,NULL,NULL,NULL,1),(2,NULL,'2022-02-01 14:09:48.963053','2022-02-03 15:51:08.391169',2,1,NULL,NULL,'','',2),(3,NULL,'2022-02-01 14:52:08.905319','2022-02-01 14:52:08.936606',3,1,NULL,NULL,NULL,NULL,3);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_functions_config`
--

LOCK TABLES `main_functions_config` WRITE;
/*!40000 ALTER TABLE `main_functions_config` DISABLE KEYS */;
INSERT INTO `main_functions_config` VALUES (1,'Почта обратной связи','flatcontent_feedback','dkramorov@mail.ru','2022-02-01 14:52:08.866938',NULL,1,NULL,1,NULL,'2022-02-01 14:52:08.866942',NULL);
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
-- Table structure for table `passport_passport`
--

DROP TABLE IF EXISTS `passport_passport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `passport_passport` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `series` varchar(64) DEFAULT NULL,
  `number` varchar(64) DEFAULT NULL,
  `issued` varchar(255) DEFAULT NULL,
  `issued_date` date DEFAULT NULL,
  `registration` varchar(255) DEFAULT NULL,
  `shopper_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `passport_passport_shopper_id_69252db1_fk_personal_shopper_id` (`shopper_id`),
  KEY `passport_passport_img_a6c3874c` (`img`),
  KEY `passport_passport_created_57afc772` (`created`),
  KEY `passport_passport_updated_858ae44f` (`updated`),
  KEY `passport_passport_position_9d52179d` (`position`),
  KEY `passport_passport_is_active_1e06ac0e` (`is_active`),
  KEY `passport_passport_state_1bb92186` (`state`),
  KEY `passport_passport_parents_aace8491` (`parents`),
  KEY `passport_passport_birthday_827280d5` (`birthday`),
  KEY `passport_passport_series_018c9d2b` (`series`),
  KEY `passport_passport_number_4aa7fc84` (`number`),
  KEY `passport_passport_issued_6bf95fc8` (`issued`),
  KEY `passport_passport_issued_date_1ad0306d` (`issued_date`),
  KEY `passport_passport_registration_4ca44b3b` (`registration`),
  CONSTRAINT `passport_passport_shopper_id_69252db1_fk_personal_shopper_id` FOREIGN KEY (`shopper_id`) REFERENCES `personal_shopper` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passport_passport`
--

LOCK TABLES `passport_passport` WRITE;
/*!40000 ALTER TABLE `passport_passport` DISABLE KEYS */;
/*!40000 ALTER TABLE `passport_passport` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_products`
--

LOCK TABLES `products_products` WRITE;
/*!40000 ALTER TABLE `products_products` DISABLE KEYS */;
INSERT INTO `products_products` VALUES (1,NULL,'2022-02-03 15:54:39.202179','2022-02-06 18:46:48.471316',1,1,NULL,'','Срок страхования 1 месяц, тренировки и соревнования по хоккею (150т.р.)','','СК Согласие','1 мес.',NULL,500.00,465.00,'','Страховой полис:<br>Срок страхования 1 месяц<br>Тренировки и соревнования по хоккею<br>Страховая сумма 150000 руб.','','1',NULL,465.00,465.00,NULL,NULL,''),(2,NULL,'2022-02-03 15:56:37.573970','2022-02-06 18:47:54.651795',2,1,NULL,'','Срок страхования 1 месяц, тренировки и соревнования по хоккею (300т.р.)','','СК Согласие','1 мес.',NULL,1000.00,915.00,'','Страховой полис:<br>Срок страхования 1 месяц<br>Тренировки и соревнования по хоккею<br>Страховая сумма 300000 руб.','','2',NULL,915.00,915.00,NULL,NULL,''),(3,NULL,'2022-02-03 16:06:12.406812','2022-02-06 18:47:05.359220',3,1,NULL,'','Срок страхования 1 месяц, 24 часа включая тренировки и соревнования по хоккею (150т.р.)','','СК Согласие','1 мес.',NULL,700.00,660.00,'','Страховой полис:<br>Срок страхования 1 месяц<br>24 часа включая тренировки и соревнования по хоккею<br>Страховая сумма 150000','','3',NULL,660.00,660.00,NULL,NULL,''),(4,NULL,'2022-02-03 16:07:57.999472','2022-02-06 18:48:10.621441',4,1,NULL,'','Срок страхования 1 месяц, 24 часа включая тренировки и соревнования по хоккею (300т.р.)','','СК Согласие','',NULL,1400.00,1305.00,'','Страховой полис:<br>Срок страхования 1 месяц<br>24 часа включая тренировки и соревнования по хоккею<br>Страховая сумма 300000','','4',NULL,1305.00,1305.00,NULL,NULL,''),(5,NULL,'2022-02-06 18:39:39.524097','2022-02-06 18:47:21.554918',5,1,NULL,'','Срок страхования 1 год, тренировки и соревнования по хоккею (150т.р.)','','СК Согласие','12 мес',NULL,2500.00,2310.00,'','Страховой полис:<br>Срок страхования 1 год<br>Тренировки и соревнования по хоккею<br>Страховая сумма 150000 руб.','','5',NULL,2310.00,2310.00,NULL,NULL,''),(6,NULL,'2022-02-06 18:41:12.115809','2022-02-06 18:47:42.556592',6,1,NULL,'','Срок страхования 1 год, тренировки и соревнования по хоккею (300т.р.)','','СК Согласие','',NULL,5000.00,4545.00,'','Страховой полис:<br>Срок страхования 1 год<br>Тренировки и соревнования по хоккею<br>Сьраховая сумма 300000 руб.','','6',NULL,4545.00,4545.00,NULL,NULL,''),(7,NULL,'2022-02-06 18:42:30.069257','2022-02-06 18:44:34.718471',7,1,NULL,'','Срок страхования 1 год, 24 часа включая тренировки и соревнования по хоккею (150т.р.)','','СК Согласие','12 мес.',NULL,3500.00,3240.00,'','Страховой полис:<br>Срок страхования 1 год<br>Тренировки и соревнования по хоккею<br>Сьраховая сумма 150000 руб.','','6-DOUBLE',NULL,3240.00,3240.00,NULL,NULL,''),(8,NULL,'2022-02-06 18:44:56.103077','2022-02-06 18:45:33.829469',8,1,NULL,'','Срок страхования 1 год, 24 часа включая тренировки и соревнования по хоккею (300т.р.)','','СК Согласие','12 мес.',NULL,7500.00,6480.00,'','Страховой полис:<br>Срок страхования 1 год<br>Тренировки и соревнования по хоккею<br>Сьраховая сумма 300000 руб.','','6-DOUBLE-DOUBLE',NULL,6480.00,6480.00,NULL,NULL,'');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productscats`
--

LOCK TABLES `products_productscats` WRITE;
/*!40000 ALTER TABLE `products_productscats` DISABLE KEYS */;
INSERT INTO `products_productscats` VALUES (1,76,1,15),(2,NULL,1,15),(3,NULL,2,15),(4,NULL,3,15),(5,NULL,4,15);
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

-- Dump completed on 2022-02-07 13:05:49
