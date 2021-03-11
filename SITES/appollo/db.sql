-- MySQL dump 10.13  Distrib 5.7.31, for osx10.12 (x86_64)
--
-- Host: localhost    Database: appollo
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
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add user',3,'add_user'),(10,'Can change user',3,'change_user'),(11,'Can delete user',3,'delete_user'),(12,'Can view user',3,'view_user'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Админка - Настрока',6,'add_config'),(22,'Can change Админка - Настрока',6,'change_config'),(23,'Can delete Админка - Настрока',6,'delete_config'),(24,'Can view Админка - Настрока',6,'view_config'),(25,'Can add Админка - Задача',7,'add_tasks'),(26,'Can change Админка - Задача',7,'change_tasks'),(27,'Can delete Админка - Задача',7,'delete_tasks'),(28,'Can view Админка - Задача',7,'view_tasks'),(29,'Can add custom user',11,'add_customuser'),(30,'Can change custom user',11,'change_customuser'),(31,'Can delete custom user',11,'delete_customuser'),(32,'Can view custom user',11,'view_customuser'),(33,'Can add Стат.контет - Файл',12,'add_files'),(34,'Can change Стат.контет - Файл',12,'change_files'),(35,'Can delete Стат.контет - Файл',12,'delete_files'),(36,'Can view Стат.контет - Файл',12,'view_files'),(37,'Can add Стат.контент - Блоки',13,'add_blocks'),(38,'Can change Стат.контент - Блоки',13,'change_blocks'),(39,'Can delete Стат.контент - Блоки',13,'delete_blocks'),(40,'Can view Стат.контент - Блоки',13,'view_blocks'),(41,'Can add Стат.контент - Контейнеры',14,'add_containers'),(42,'Can change Стат.контент - Контейнеры',14,'change_containers'),(43,'Can delete Стат.контент - Контейнеры',14,'delete_containers'),(44,'Can view Стат.контент - Контейнеры',14,'view_containers'),(45,'Can add Стат.контент - Линковка меню к контейнерам',15,'add_linkcontainer'),(46,'Can change Стат.контент - Линковка меню к контейнерам',15,'change_linkcontainer'),(47,'Can delete Стат.контент - Линковка меню к контейнерам',15,'delete_linkcontainer'),(48,'Can view Стат.контент - Линковка меню к контейнерам',15,'view_linkcontainer');
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$PGH4RfFve7FD$l3hOxDq8BWI5yhsnZAw06qVS4lfySTNXT3C3wQprpn0=','2021-03-09 21:57:25.656913',1,'jocker','','','dkramorov@mail.ru',1,1,'2021-03-09 21:45:30.765576');
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(12,'files','files'),(13,'flatcontent','blocks'),(14,'flatcontent','containers'),(15,'flatcontent','linkcontainer'),(11,'login','customuser'),(8,'login','extrafields'),(10,'login','extrainfo'),(9,'login','extravalues'),(6,'main_functions','config'),(7,'main_functions','tasks'),(5,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-03-09 21:45:28.562878'),(2,'contenttypes','0002_remove_content_type_name','2021-03-09 21:45:28.661036'),(3,'auth','0001_initial','2021-03-09 21:45:28.917391'),(4,'auth','0002_alter_permission_name_max_length','2021-03-09 21:45:29.322976'),(5,'auth','0003_alter_user_email_max_length','2021-03-09 21:45:29.346957'),(6,'auth','0004_alter_user_username_opts','2021-03-09 21:45:29.355292'),(7,'auth','0005_alter_user_last_login_null','2021-03-09 21:45:29.382287'),(8,'auth','0006_require_contenttypes_0002','2021-03-09 21:45:29.384122'),(9,'auth','0007_alter_validators_add_error_messages','2021-03-09 21:45:29.390837'),(10,'auth','0008_alter_user_username_max_length','2021-03-09 21:45:29.412373'),(11,'auth','0009_alter_user_last_name_max_length','2021-03-09 21:45:29.430480'),(12,'auth','0010_alter_group_name_max_length','2021-03-09 21:45:29.454111'),(13,'auth','0011_update_proxy_permissions','2021-03-09 21:45:29.461368'),(14,'files','0001_initial','2021-03-09 21:45:29.488849'),(15,'files','0002_auto_20191203_2054','2021-03-09 21:45:29.560390'),(16,'files','0003_auto_20200112_1717','2021-03-09 21:45:29.570602'),(17,'files','0004_auto_20200402_2127','2021-03-09 21:45:29.606744'),(18,'files','0005_auto_20200809_1025','2021-03-09 21:45:29.609999'),(19,'flatcontent','0001_initial','2021-03-09 21:45:29.732034'),(20,'flatcontent','0002_auto_20190825_1730','2021-03-09 21:45:30.236694'),(21,'flatcontent','0003_auto_20191203_2054','2021-03-09 21:45:30.279256'),(22,'flatcontent','0004_blocks_html','2021-03-09 21:45:30.308297'),(23,'flatcontent','0005_auto_20200112_1717','2021-03-09 21:45:30.392810'),(24,'flatcontent','0006_auto_20200314_1638','2021-03-09 21:45:30.399921'),(25,'flatcontent','0007_auto_20200402_2127','2021-03-09 21:45:30.546401'),(26,'flatcontent','0008_containers_class_name','2021-03-09 21:45:30.572595'),(27,'flatcontent','0009_blocks_class_name','2021-03-09 21:45:30.606505'),(28,'login','0001_initial','2021-03-09 21:45:30.885122'),(29,'login','0002_auto_20200925_1007','2021-03-09 21:45:31.714542'),(30,'main_functions','0001_initial','2021-03-09 21:45:31.782410'),(31,'main_functions','0002_auto_20191203_2052','2021-03-09 21:45:31.804171'),(32,'main_functions','0003_auto_20200407_1845','2021-03-09 21:45:32.383550'),(33,'main_functions','0004_config_user','2021-03-09 21:45:32.527595'),(34,'sessions','0001_initial','2021-03-09 21:45:32.591120');
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
INSERT INTO `django_session` VALUES ('tbf3sxmuq50x762v9nxacye0ujrk65bt','OGE1OThmODYxNDVjYWRhZWFkZTEwNDgyODllMGNlZDQzODk1ZTI1Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjNlYTE1NDZlMjJmNzY2Yzk0MjQxMGUzZjEyZWYzNWI5NGI1YTExN2UifQ==','2021-03-23 21:57:25.686541');
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
) ENGINE=InnoDB AUTO_INCREMENT=182 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
INSERT INTO `flatcontent_blocks` VALUES (1,'1.png','2021-03-09 21:57:21.569812','2021-03-09 21:59:13.621736',1,1,1,'','Логотип','из-за бугра','/','logo',1,0,'','','Звони на 8800 бесплатно','',''),(2,NULL,'2021-03-09 21:57:21.572728','2021-03-09 21:57:21.572750',2,1,3,'','Телефон',NULL,'tel:73952123321','phone',1,0,NULL,NULL,NULL,'+7(3952) 123-321',NULL),(3,NULL,'2021-03-09 21:57:21.575884','2021-03-09 21:57:21.575909',3,1,3,'','Адрес',NULL,NULL,'address',1,0,NULL,NULL,NULL,'г. Иркутск ул. Советская 32а офис 5',NULL),(4,NULL,'2021-03-09 21:57:21.579305','2021-03-09 21:57:21.579327',4,1,3,'','Email',NULL,NULL,'email',1,0,NULL,NULL,NULL,'test@test.ru',NULL),(5,NULL,'2021-03-09 21:57:21.582092','2021-03-09 21:57:21.582113',5,1,3,'','Режим работы',NULL,NULL,'worktime',1,0,NULL,NULL,NULL,'пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 17:00',NULL),(6,NULL,'2021-03-09 21:57:21.584730','2021-03-09 21:57:21.584749',6,1,3,'','Copyright',NULL,NULL,'copyright',1,0,NULL,NULL,NULL,'<p>&copy; 2020 Все права защищены</p>',NULL),(7,NULL,'2021-03-09 21:57:21.587331','2021-03-09 22:00:07.988956',7,1,1,'','Название компании','','','company_name',1,0,'','','Бесплатные звонки на 8800','',''),(8,NULL,'2021-03-09 21:57:21.589990','2021-03-09 21:57:21.590009',8,1,3,'','Favicon',NULL,NULL,'favicon',1,0,NULL,NULL,NULL,NULL,NULL),(9,NULL,'2021-03-09 21:57:21.592906','2021-03-09 21:57:21.592932',9,1,3,'','Сообщества',NULL,NULL,'social',1,0,NULL,NULL,NULL,NULL,NULL),(10,NULL,'2021-03-09 21:57:21.595801','2021-03-09 21:57:21.595824',10,1,3,'_9','instagram',NULL,NULL,'instagram',1,1,'instagram',NULL,NULL,NULL,NULL),(11,NULL,'2021-03-09 21:57:21.598619','2021-03-09 21:57:21.598642',11,1,3,'_9','vk',NULL,NULL,'vk',1,1,'vk',NULL,NULL,NULL,NULL),(12,NULL,'2021-03-09 21:57:21.601346','2021-03-09 21:57:21.601366',12,1,3,'_9','facebook',NULL,NULL,'facebook',1,1,'facebook',NULL,NULL,NULL,NULL),(13,NULL,'2021-03-09 21:57:21.604029','2021-03-09 21:57:21.604051',13,1,3,'_9','twitter',NULL,NULL,'twitter',1,1,'twitter',NULL,NULL,NULL,NULL),(14,NULL,'2021-03-09 21:57:21.606690','2021-03-09 21:57:21.606711',14,1,3,'','Яндекс.Метрика счетчик',NULL,NULL,'yandex_metrika',1,0,NULL,NULL,NULL,'<script type=\"text/javascript\"></script>',NULL),(15,NULL,'2021-03-09 21:57:21.609624','2021-03-09 21:57:21.609648',15,1,3,'','Google.Analytics счетчик',NULL,NULL,'google_analytics',1,0,NULL,NULL,NULL,'<script type=\"text/javascript\"></script>',NULL),(17,NULL,'2021-03-09 21:57:21.619712','2021-03-10 01:20:16.296221',17,1,4,'','О нас','','#start','_mainmenu_catpage',2,0,'','','','',''),(22,NULL,'2021-03-09 21:57:21.636330','2021-03-10 01:20:40.174596',22,1,4,'','Как звонить','','#video','_mainmenu_aboutpage',2,0,'','','','',''),(24,NULL,'2021-03-09 21:57:21.641808','2021-03-10 01:21:18.479080',24,1,4,'','Отзывы','','#reviews','_mainmenu_feedbackpage',2,0,'','','','',''),(33,NULL,'2021-03-09 22:50:41.643500','2021-03-09 22:51:25.266050',33,1,1,'','Звони на 8800','это очень','','animate',5,0,'','','','',''),(34,NULL,'2021-03-09 22:51:18.921588','2021-03-09 22:51:37.010330',34,1,1,'_33','легко','','','',5,0,'','','','',''),(35,NULL,'2021-03-09 22:51:40.667381','2021-03-09 22:51:40.667400',35,1,1,'_33','быстро',NULL,NULL,NULL,5,0,NULL,NULL,NULL,NULL,NULL),(36,NULL,'2021-03-09 22:51:44.603730','2021-03-09 22:51:44.603749',36,1,1,'_33','безопасно',NULL,NULL,NULL,5,0,NULL,NULL,NULL,NULL,NULL),(37,NULL,'2021-03-09 22:51:47.261049','2021-03-09 22:51:47.261069',37,1,1,'_33','удобно',NULL,NULL,NULL,5,0,NULL,NULL,NULL,NULL,NULL),(38,NULL,'2021-03-09 22:55:02.219193','2021-03-09 22:55:04.733696',38,1,1,'','Изображения','','','images',5,0,'','','','',''),(39,'undefined.jpg','2021-03-09 22:55:08.491812','2021-03-09 22:55:10.741423',39,1,1,'_38','Без названия','','','',5,0,'','','','',''),(40,'undefined.jpg','2021-03-09 22:55:15.831141','2021-03-09 22:55:26.435921',40,1,1,'_38','Без названия','','','',5,0,'','','','',''),(41,'undefined.jpg','2021-03-09 22:55:36.941432','2021-03-09 22:55:39.327391',41,1,1,'_38','Без названия','','','',5,0,'','','','',''),(42,'undefined.jpg','2021-03-09 22:55:55.754159','2021-03-09 22:55:58.024341',42,1,1,'_38','Без названия','','','',5,0,'','','','',''),(43,'undefined.jpg','2021-03-09 22:56:08.158480','2021-03-09 22:56:09.365591',43,1,1,'_38','Без названия','','','',5,0,'','','','',''),(44,NULL,'2021-03-09 22:56:21.074002','2021-03-09 22:56:29.151972',44,1,1,'','Кнопки','','','buttons',5,0,'','','','',''),(45,NULL,'2021-03-09 22:56:24.169510','2021-03-09 22:56:52.552701',45,1,1,'_44','Приложение на AppStore','AppStore','','',5,0,'apple','','','',''),(46,NULL,'2021-03-09 22:56:25.655899','2021-03-09 22:57:10.945857',46,1,1,'_44','Приложение на GooglePlay','GooglePlay','','',5,0,'android','','','',''),(47,NULL,'2021-03-09 22:59:05.487380','2021-03-09 22:59:05.487412',33,1,1,'','Звони на 8800','это очень','','animate',6,0,'','','','',''),(48,NULL,'2021-03-09 22:59:05.488341','2021-03-09 22:59:05.488361',34,1,1,'_47','легко','','','',6,0,'','','','',''),(49,NULL,'2021-03-09 22:59:05.489153','2021-03-09 22:59:05.489169',35,1,1,'_47','быстро',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(50,NULL,'2021-03-09 22:59:05.489901','2021-03-09 22:59:05.489917',36,1,1,'_47','безопасно',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(51,NULL,'2021-03-09 22:59:05.490720','2021-03-09 22:59:05.490736',37,1,1,'_47','удобно',NULL,NULL,NULL,6,0,NULL,NULL,NULL,NULL,NULL),(52,NULL,'2021-03-09 22:59:05.491480','2021-03-09 22:59:05.491497',38,1,1,'','Изображения','','','images',6,0,'','','','',''),(53,'undefined.jpg','2021-03-09 22:59:05.492261','2021-03-09 22:59:05.492277',39,1,1,'_52','Без названия','','','',6,0,'','','','',''),(54,'undefined.jpg','2021-03-09 22:59:05.493727','2021-03-09 22:59:05.493746',40,1,1,'_52','Без названия','','','',6,0,'','','','',''),(55,'undefined.jpg','2021-03-09 22:59:05.507662','2021-03-09 22:59:05.507687',41,1,1,'_52','Без названия','','','',6,0,'','','','',''),(56,'undefined.jpg','2021-03-09 22:59:05.515139','2021-03-09 22:59:05.515174',42,1,1,'_52','Без названия','','','',6,0,'','','','',''),(57,'undefined.jpg','2021-03-09 22:59:05.522650','2021-03-09 22:59:05.522672',43,1,1,'_52','Без названия','','','',6,0,'','','','',''),(58,NULL,'2021-03-09 22:59:05.529739','2021-03-09 22:59:05.529772',44,1,1,'','Кнопки','','','buttons',6,0,'','','','',''),(59,NULL,'2021-03-09 22:59:05.536408','2021-03-09 22:59:05.536433',45,1,1,'_58','Приложение на AppStore','AppStore','','',6,0,'apple','','','',''),(60,NULL,'2021-03-09 22:59:05.543125','2021-03-09 22:59:05.543145',46,1,1,'_58','Приложение на GooglePlay','GooglePlay','','',6,0,'android','','','',''),(61,NULL,'2021-03-09 22:59:40.250268','2021-03-10 01:15:21.494253',47,1,4,'','Главная','','/','',3,0,'','','','',''),(62,NULL,'2021-03-09 23:02:37.226109','2021-03-09 23:04:39.450417',48,1,1,'','Безопасно','','','',7,0,'lock','','','Вы звоните через наш сервис через браузер, если вы не нарушаете закон Российской Федерации, то вы полностью анонимны<br>',''),(63,NULL,'2021-03-09 23:02:38.146684','2021-03-09 23:05:46.481799',49,1,1,'','Бесплатно','','','',7,0,'money','','','Вы платите только за ваш интернет, которым вы пользуетесь, заходите на наш сайт и звоните абсолютно бесплатно<br>',''),(64,NULL,'2021-03-09 23:02:39.636211','2021-03-09 23:06:44.273683',50,1,1,'','Удобно','','','',7,0,'thumbs-o-up','','','Если у вас есть интернет, то вы можете совершать звонки через наш сайт на любые номера 8-800, удобнее и не придумаешь<br>',''),(65,NULL,'2021-03-09 23:07:00.648079','2021-03-09 23:07:00.648097',48,1,1,'','Безопасно','','','',8,0,'lock','','','Вы звоните через наш сервис через браузер, если вы не нарушаете закон Российской Федерации, то вы полностью анонимны<br>',''),(66,NULL,'2021-03-09 23:07:00.648876','2021-03-09 23:07:00.648892',49,1,1,'','Бесплатно','','','',8,0,'money','','','Вы платите только за ваш интернет, которым вы пользуетесь, заходите на наш сайт и звоните абсолютно бесплатно<br>',''),(67,NULL,'2021-03-09 23:07:00.649685','2021-03-09 23:07:00.649701',50,1,1,'','Удобно','','','',8,0,'thumbs-o-up','','','Если у вас есть интернет, то вы можете совершать звонки через наш сайт на любые номера 8-800, удобнее и не придумаешь<br>',''),(68,'undefined.jpg','2021-03-09 23:12:48.369323','2021-03-09 23:19:52.030090',2,1,1,'','Текст 2','','','',9,0,'','','','<ul><li>Удобно</li><li>Быстро</li><li>Просто</li><li>Надежно</li><li>Бесплатно</li></ul>',''),(69,'undefined.jpg','2021-03-09 23:12:49.487838','2021-03-09 23:22:28.686070',1,1,1,'','Текст 1','','','',9,0,'','','','Пользоваться нашим сервисом просто и удобно, все что вам нужно иметь это доступ в интернет и наушники с микрофоном, в этом случае, вы сможете звонить на номер 8-800 через наш сайт, это удобно, быстро и просто.<br><br>Попробуйте совершить звонок, он абсолютно бесплатный, вы платите только за свой интернет.<br>',''),(70,NULL,'2021-03-09 23:22:44.948657','2021-03-09 23:23:53.281657',51,1,1,'','Текст 3','','','',9,0,'','','','Если вам что-нибудь не понравится, вы всегда можете написать нам об этом, мы положительно воспринимаем критику и готовы работать над качеством нашего сервиса.<br><br>Если вы оставите отзыв, мы будем признательны вам<br>',''),(71,'undefined.jpg','2021-03-09 23:24:12.612406','2021-03-09 23:24:12.612427',2,1,1,'','Текст 2','','','',10,0,'','','','<ul><li>Удобно</li><li>Быстро</li><li>Просто</li><li>Надежно</li><li>Бесплатно</li></ul>',''),(72,'undefined.jpg','2021-03-09 23:24:12.615034','2021-03-09 23:24:12.615054',1,1,1,'','Текст 1','','','',10,0,'','','','Пользоваться нашим сервисом просто и удобно, все что вам нужно иметь это доступ в интернет и наушники с микрофоном, в этом случае, вы сможете звонить на номер 8-800 через наш сайт, это удобно, быстро и просто.<br><br>Попробуйте совершить звонок, он абсолютно бесплатный, вы платите только за свой интернет.<br>',''),(73,NULL,'2021-03-09 23:24:12.628665','2021-03-09 23:24:12.628685',51,1,1,'','Текст 3','','','',10,0,'','','','Если вам что-нибудь не понравится, вы всегда можете написать нам об этом, мы положительно воспринимаем критику и готовы работать над качеством нашего сервиса.<br><br>Если вы оставите отзыв, мы будем признательны вам<br>',''),(74,NULL,'2021-03-09 23:30:52.707712','2021-03-09 23:31:59.714499',52,1,1,'','Видео инструкция','','https://www.youtube.com/watch?v=T6AK9YFO1kw','',11,0,'','','','Посмотрите видео как&nbsp; звонить<br>',''),(75,NULL,'2021-03-09 23:32:41.824728','2021-03-09 23:32:41.824749',52,1,1,'','Видео инструкция','','https://www.youtube.com/watch?v=T6AK9YFO1kw','',12,0,'','','','Посмотрите видео как&nbsp; звонить<br>',''),(76,NULL,'2021-03-09 23:43:03.715688','2021-03-09 23:47:24.501705',53,1,1,'','Регистрация','','','left',13,0,'list-alt','','','Чтобы совершать звонки, вам необходимо зарегистрироваться<br>',''),(77,NULL,'2021-03-09 23:43:07.360593','2021-03-09 23:47:46.728962',54,1,1,'','Авторизация','','','left',13,0,'sign-in','','','После регистрации, необходимо войти на сайт<br>',''),(78,NULL,'2021-03-09 23:43:13.142726','2021-03-09 23:48:14.946957',55,1,1,'','Разрешение','','','left',13,0,'microphone','','','При наборе номера браузер вас спросит разрешаете ли вы ему использовать микрофон, ответье утвердительно<br>',''),(79,'undefined.jpg','2021-03-09 23:44:37.073276','2021-03-09 23:44:46.282457',56,1,1,'','Изображение','','','',13,0,'','','','',''),(80,NULL,'2021-03-09 23:44:49.811744','2021-03-09 23:49:04.152392',57,1,1,'','Набор номера','','','right',13,0,'th','','','После рашрешения использовать микрофон ваш звонок пройдет и вам ответят<br>',''),(81,NULL,'2021-03-09 23:44:50.678089','2021-03-09 23:49:25.889099',58,1,1,'','Звонок','','','right',13,0,'headphones','','','Разговаривайте, не закрывая страничку в браузере на которой вы звоните<br>',''),(82,NULL,'2021-03-09 23:44:51.814355','2021-03-09 23:50:09.234257',59,1,1,'','Готово','','','right',13,0,'thumbs-o-up','','','После разговора вы можете покинуть страничку или написать ваше мнение о нашем сайте<br>',''),(83,NULL,'2021-03-09 23:50:45.990685','2021-03-09 23:50:45.990704',53,1,1,'','Регистрация','','','left',14,0,'list-alt','','','Чтобы совершать звонки, вам необходимо зарегистрироваться<br>',''),(84,NULL,'2021-03-09 23:50:45.991556','2021-03-09 23:50:45.991572',54,1,1,'','Авторизация','','','left',14,0,'sign-in','','','После регистрации, необходимо войти на сайт<br>',''),(85,NULL,'2021-03-09 23:50:45.992347','2021-03-09 23:50:45.992363',55,1,1,'','Разрешение','','','left',14,0,'microphone','','','При наборе номера браузер вас спросит разрешаете ли вы ему использовать микрофон, ответье утвердительно<br>',''),(86,'undefined.jpg','2021-03-09 23:50:45.993141','2021-03-09 23:50:45.993156',56,1,1,'','Изображение','','','',14,0,'','','','',''),(87,NULL,'2021-03-09 23:50:45.995598','2021-03-09 23:50:45.995617',57,1,1,'','Набор номера','','','right',14,0,'th','','','После рашрешения использовать микрофон ваш звонок пройдет и вам ответят<br>',''),(88,NULL,'2021-03-09 23:50:46.018450','2021-03-09 23:50:46.018477',58,1,1,'','Звонок','','','right',14,0,'headphones','','','Разговаривайте, не закрывая страничку в браузере на которой вы звоните<br>',''),(89,NULL,'2021-03-09 23:50:46.025346','2021-03-09 23:50:46.025379',59,1,1,'','Готово','','','right',14,0,'thumbs-o-up','','','После разговора вы можете покинуть страничку или написать ваше мнение о нашем сайте<br>',''),(90,'undefined.jpg','2021-03-09 23:54:48.751077','2021-03-09 23:54:58.415132',60,1,1,'','Без названия','','','',15,0,'','','','',''),(91,'undefined.jpg','2021-03-09 23:54:49.565840','2021-03-09 23:55:07.320789',61,1,1,'','Без названия','','','',15,0,'','','','',''),(92,'undefined.jpg','2021-03-09 23:54:50.367377','2021-03-09 23:55:15.183436',62,1,1,'','Без названия','','','',15,0,'','','','',''),(93,'undefined.jpg','2021-03-09 23:54:51.887372','2021-03-09 23:55:23.756341',63,1,1,'','Без названия','','','',15,0,'','','','',''),(94,'undefined.jpg','2021-03-09 23:55:31.790440','2021-03-09 23:55:34.085539',64,1,1,'','Без названия','','','',15,0,'','','','',''),(95,'undefined.jpg','2021-03-09 23:56:34.628543','2021-03-09 23:56:34.628565',60,1,1,'','Без названия','','','',16,0,'','','','',''),(96,'undefined.jpg','2021-03-09 23:56:34.630411','2021-03-09 23:56:34.630430',61,1,1,'','Без названия','','','',16,0,'','','','',''),(97,'undefined.jpg','2021-03-09 23:56:34.643873','2021-03-09 23:56:34.643892',62,1,1,'','Без названия','','','',16,0,'','','','',''),(98,'undefined.jpg','2021-03-09 23:56:34.651149','2021-03-09 23:56:34.651172',63,1,1,'','Без названия','','','',16,0,'','','','',''),(99,'undefined.jpg','2021-03-09 23:56:34.658269','2021-03-09 23:56:34.658295',64,1,1,'','Без названия','','','',16,0,'','','','',''),(100,'100.jpeg','2021-03-10 00:01:55.701371','2021-03-10 00:06:08.342798',65,1,1,'','Виктор Брянцев','','','',17,0,'','','','Очень приятно, что все еще можно встретить сервисы предназначенные для людей, а не только выбивалки денег, которые наполнили интернет с кучей навязчивой рекламы и попыткой вытянуть из тебя денег<br>',''),(101,'101.jpeg','2021-03-10 00:01:56.669410','2021-03-10 00:07:34.070514',66,1,1,'','Радеон Бородач','','','',17,0,'','','','Мне нравится, плохо обслужили в магазине, нагрубили в торговом центре - захожу на сайт, набираю номер горячей линии на 8-800 - жалуюсь, думаю, я делаю правильное дело, а этот сайт помогает в этом<br>',''),(102,'102.jpeg','2021-03-10 00:01:57.533133','2021-03-10 00:08:47.903737',67,1,1,'','Оксана Шигорина','','','',17,0,'','','','Обычно не пользуюсь бесплатными услугами, потому что бесплатный только сыр в мышеловке, но тут дают сыр без нее, прочитала, попробовала - не увидела никаких рисков для себя - действительно бесплатно можно звонить<br>',''),(103,'103.jpeg','2021-03-10 00:01:58.357452','2021-03-10 00:09:37.416030',68,1,1,'','Альберт Шеметов','','','',17,0,'','','','Жаль, что только 8 800 - очень большой потенциал если появятся и другие направления, а если будут доступны звонки на сотовые, то боюсь телефон для звонков уже можно будет не использовать<br>',''),(105,'100.jpeg','2021-03-10 00:11:03.110173','2021-03-10 00:11:03.110191',65,1,1,'','Виктор Брянцев','','','',18,0,'','','','Очень приятно, что все еще можно встретить сервисы предназначенные для людей, а не только выбивалки денег, которые наполнили интернет с кучей навязчивой рекламы и попыткой вытянуть из тебя денег<br>',''),(106,'101.jpeg','2021-03-10 00:11:03.113711','2021-03-10 00:11:03.113737',66,1,1,'','Радеон Бородач','','','',18,0,'','','','Мне нравится, плохо обслужили в магазине, нагрубили в торговом центре - захожу на сайт, набираю номер горячей линии на 8-800 - жалуюсь, думаю, я делаю правильное дело, а этот сайт помогает в этом<br>',''),(107,'102.jpeg','2021-03-10 00:11:03.121702','2021-03-10 00:11:03.121734',67,1,1,'','Оксана Шигорина','','','',18,0,'','','','Обычно не пользуюсь бесплатными услугами, потому что бесплатный только сыр в мышеловке, но тут дают сыр без нее, прочитала, попробовала - не увидела никаких рисков для себя - действительно бесплатно можно звонить<br>',''),(108,'103.jpeg','2021-03-10 00:11:03.129682','2021-03-10 00:11:03.129703',68,1,1,'','Альберт Шеметов','','','',18,0,'','','','Жаль, что только 8 800 - очень большой потенциал если появятся и другие направления, а если будут доступны звонки на сотовые, то боюсь телефон для звонков уже можно будет не использовать<br>',''),(109,'109.jpeg','2021-03-10 00:18:01.135395','2021-03-10 00:19:51.261147',69,1,1,'','Артур Пирожков','','','',19,0,'','','','Специалист по VOIP связи<br>',''),(110,'110.jpeg','2021-03-10 00:18:01.904377','2021-03-10 00:19:57.208121',70,1,1,'','Татьяна Лазаервна','','','',19,0,'','','','Маркетолог',''),(111,'111.jpeg','2021-03-10 00:18:02.734030','2021-03-10 00:20:07.784107',71,1,1,'','Михаил Доярский','','','',19,0,'','','','Разработчик',''),(112,'112.jpeg','2021-03-10 00:18:03.693793','2021-03-10 00:20:19.213618',72,1,1,'','Виктор Пиктор','','','',19,0,'','','','Дизайнер',''),(113,NULL,'2021-03-10 00:20:27.461782','2021-03-10 00:20:33.492946',73,1,1,'_109','instagram','','','',19,0,'instagram','','','',''),(114,NULL,'2021-03-10 00:20:36.764712','2021-03-10 00:20:48.586274',74,1,1,'_110','instagram','','','',19,0,'instagram','','','',''),(115,NULL,'2021-03-10 00:20:51.323883','2021-03-10 00:21:00.757778',75,1,1,'_111','instagram','','','',19,0,'instagram','','','',''),(116,NULL,'2021-03-10 00:21:05.185241','2021-03-10 00:21:12.125481',76,1,1,'_112','instagram','','','',19,0,'instagram','','','',''),(117,'109.jpeg','2021-03-10 00:21:31.868461','2021-03-10 00:21:31.868483',69,1,1,'','Артур Пирожков','','','',20,0,'','','','Специалист по VOIP связи<br>',''),(118,NULL,'2021-03-10 00:21:31.870609','2021-03-10 00:21:31.870627',73,1,1,'_117','instagram','','','',20,0,'instagram','','','',''),(119,'110.jpeg','2021-03-10 00:21:31.877221','2021-03-10 00:21:31.877241',70,1,1,'','Татьяна Лазаервна','','','',20,0,'','','','Маркетолог',''),(120,NULL,'2021-03-10 00:21:31.884937','2021-03-10 00:21:31.884962',74,1,1,'_119','instagram','','','',20,0,'instagram','','','',''),(121,'111.jpeg','2021-03-10 00:21:31.891765','2021-03-10 00:21:31.891786',71,1,1,'','Михаил Доярский','','','',20,0,'','','','Разработчик',''),(122,NULL,'2021-03-10 00:21:31.899583','2021-03-10 00:21:31.899603',75,1,1,'_121','instagram','','','',20,0,'instagram','','','',''),(123,'112.jpeg','2021-03-10 00:21:31.918044','2021-03-10 00:21:31.918067',72,1,1,'','Виктор Пиктор','','','',20,0,'','','','Дизайнер',''),(124,NULL,'2021-03-10 00:21:31.925867','2021-03-10 00:21:31.925890',76,1,1,'_123','instagram','','','',20,0,'instagram','','','',''),(125,NULL,'2021-03-10 00:28:14.890301','2021-03-10 00:28:56.700114',77,1,1,'','скачиваний приложения','k','','',21,0,'','','12','',''),(126,NULL,'2021-03-10 00:28:22.431282','2021-03-10 00:29:03.673364',78,1,1,'','счастливых пользователей','k','','',21,0,'','','32','',''),(127,NULL,'2021-03-10 00:28:34.343389','2021-03-10 00:29:10.881813',79,1,1,'','звонков','k','','',21,0,'','','542','',''),(128,NULL,'2021-03-10 00:28:46.481801','2021-03-10 00:29:15.935628',80,1,1,'','наград','','','',21,0,'','','18','',''),(129,NULL,'2021-03-10 00:32:26.506721','2021-03-10 00:32:26.506744',77,1,1,'','скачиваний приложения','k','','',22,0,'','','12','',''),(130,NULL,'2021-03-10 00:32:26.507973','2021-03-10 00:32:26.507991',78,1,1,'','счастливых пользователей','k','','',22,0,'','','32','',''),(131,NULL,'2021-03-10 00:32:26.510085','2021-03-10 00:32:26.510102',79,1,1,'','звонков','k','','',22,0,'','','542','',''),(132,NULL,'2021-03-10 00:32:26.510852','2021-03-10 00:32:26.510869',80,1,1,'','наград','','','',22,0,'','','18','',''),(133,NULL,'2021-03-10 00:33:42.605728','2021-03-10 00:35:16.523215',81,1,1,'','Стартовый','Выбрать','/','',23,0,'','','0 ₽','',''),(134,NULL,'2021-03-10 00:33:43.443120','2021-03-10 00:38:44.425659',82,1,1,'','Стандартный','Выбрать','/','optimal',23,0,'','','1000 ₽','',''),(135,NULL,'2021-03-10 00:33:45.097903','2021-03-10 00:35:09.648501',83,1,1,'','Премиум','Выбрать','/','',23,0,'','','5000 ₽','',''),(136,NULL,'2021-03-10 00:42:15.487740','2021-03-10 00:44:11.106074',84,1,1,'_133','Звонки 8 800','не ограничены','','',23,0,'','','','',''),(137,NULL,'2021-03-10 00:42:20.439070','2021-03-10 00:44:31.683497',85,1,1,'_134','Звонки 8 800','не ограничены','','',23,0,'','','','',''),(138,NULL,'2021-03-10 00:42:27.666473','2021-03-10 00:44:56.353043',86,1,1,'_135','Звонки 8 800','не ограничены','','',23,0,'','','','',''),(139,NULL,'2021-03-10 00:42:44.897600','2021-03-10 00:44:16.584999',87,1,1,'_133','Консультация','менеджера','','',23,0,'','','','',''),(140,NULL,'2021-03-10 00:42:59.713017','2021-03-10 00:44:29.026323',88,1,1,'_133','История звонков','на 8 800','','',23,0,'','','','',''),(141,NULL,'2021-03-10 00:43:08.261167','2021-03-10 00:44:35.281057',89,1,1,'_134','Звонки на городские','не ограничены','','',23,0,'','','','',''),(142,NULL,'2021-03-10 00:43:13.988859','2021-03-10 00:44:40.275835',90,1,1,'_134','Консультация','менеджера','','',23,0,'','','','',''),(143,NULL,'2021-03-10 00:43:18.825177','2021-03-10 00:44:53.719820',91,1,1,'_134','История звонков','на 8 800/городские','','',23,0,'','','','',''),(144,NULL,'2021-03-10 00:43:25.147880','2021-03-10 00:45:02.900391',92,1,1,'_135','Звонки на городские','не ограничены','','',23,0,'','','','',''),(145,NULL,'2021-03-10 00:43:30.696186','2021-03-10 00:45:05.151200',93,1,1,'_135','Звонки на сотовые','не ограничены','','',23,0,'','','','',''),(146,NULL,'2021-03-10 00:43:35.589354','2021-03-10 00:45:09.020933',94,1,1,'_135','Консультация','менеджера','','',23,0,'','','','',''),(147,NULL,'2021-03-10 00:43:43.193386','2021-03-10 00:45:14.679935',95,1,1,'_135','История звонков','на все','','',23,0,'','','','',''),(148,NULL,'2021-03-10 00:45:59.582260','2021-03-10 00:45:59.582278',81,1,1,'','Стартовый','Выбрать','/','',24,0,'','','0 ₽','',''),(149,NULL,'2021-03-10 00:45:59.583172','2021-03-10 00:45:59.583188',84,1,1,'_148','Звонки 8 800','не ограничены','','',24,0,'','','','',''),(150,NULL,'2021-03-10 00:45:59.583916','2021-03-10 00:45:59.583931',87,1,1,'_148','Консультация','менеджера','','',24,0,'','','','',''),(151,NULL,'2021-03-10 00:45:59.584683','2021-03-10 00:45:59.584699',88,1,1,'_148','История звонков','на 8 800','','',24,0,'','','','',''),(152,NULL,'2021-03-10 00:45:59.585413','2021-03-10 00:45:59.585428',82,1,1,'','Стандартный','Выбрать','/','optimal',24,0,'','','1000 ₽','',''),(153,NULL,'2021-03-10 00:45:59.586157','2021-03-10 00:45:59.586172',85,1,1,'_152','Звонки 8 800','не ограничены','','',24,0,'','','','',''),(154,NULL,'2021-03-10 00:45:59.586874','2021-03-10 00:45:59.586889',89,1,1,'_152','Звонки на городские','не ограничены','','',24,0,'','','','',''),(155,NULL,'2021-03-10 00:45:59.587612','2021-03-10 00:45:59.587627',90,1,1,'_152','Консультация','менеджера','','',24,0,'','','','',''),(156,NULL,'2021-03-10 00:45:59.588374','2021-03-10 00:45:59.588399',91,1,1,'_152','История звонков','на 8 800/городские','','',24,0,'','','','',''),(157,NULL,'2021-03-10 00:45:59.589106','2021-03-10 00:45:59.589121',83,1,1,'','Премиум','Выбрать','/','',24,0,'','','5000 ₽','',''),(158,NULL,'2021-03-10 00:45:59.589902','2021-03-10 00:45:59.589917',86,1,1,'_157','Звонки 8 800','не ограничены','','',24,0,'','','','',''),(159,NULL,'2021-03-10 00:45:59.590623','2021-03-10 00:45:59.590637',92,1,1,'_157','Звонки на городские','не ограничены','','',24,0,'','','','',''),(160,NULL,'2021-03-10 00:45:59.591378','2021-03-10 00:45:59.591393',93,1,1,'_157','Звонки на сотовые','не ограничены','','',24,0,'','','','',''),(161,NULL,'2021-03-10 00:45:59.592141','2021-03-10 00:45:59.592157',94,1,1,'_157','Консультация','менеджера','','',24,0,'','','','',''),(162,NULL,'2021-03-10 00:45:59.592929','2021-03-10 00:45:59.592947',95,1,1,'_157','История звонков','на все','','',24,0,'','','','',''),(163,'undefined.jpg','2021-03-10 00:51:57.201373','2021-03-10 00:52:14.086340',4,1,1,'','Изображение','','','',25,0,'','','','',''),(164,'undefined.jpg','2021-03-10 00:51:58.222380','2021-03-10 00:52:22.693064',5,1,1,'','Изображение','','','',25,0,'','','','',''),(165,NULL,'2021-03-10 00:52:33.605169','2021-03-10 00:54:11.200165',1,1,1,'','Можно ли звонить не только на 8800?','','','',25,0,'','','','Да, но, к сожалению, пока мы не можем разрешить звонки всем бесплатно на любые номера, поэтому на данный момент предусмотрены платные услуги, но, может в скором времени наши возможности позволят звонить бесплатно на все номера<br>',''),(166,NULL,'2021-03-10 00:52:34.865763','2021-03-10 00:54:57.964608',2,1,1,'','Можно ли мне такую же услугу на сайт?','','','',25,0,'','','','Если вы хотите давать возможность звонить со своего сайта, тогда вам следует связаться с нашим менеджером, мы проконсультируем вас как это можно сделать и что для этого потребуется<br>',''),(167,NULL,'2021-03-10 00:52:36.280280','2021-03-10 00:56:44.031521',3,1,1,'','Что будет если хулиганы воспользуются сервисом?','','','',25,0,'','','','К сожалению, такое может произойти, в этом случае как и в любом другом - инцидент будет рассмотрен правохранительными органами, мы передадим всю имеющуюся информацию компетентным структурам и вопрос будет решен согласно законам РФ<br>',''),(168,'undefined.jpg','2021-03-10 01:00:09.477789','2021-03-10 01:00:09.477812',4,1,1,'','Изображение','','','',26,0,'','','','',''),(169,'undefined.jpg','2021-03-10 01:00:09.492283','2021-03-10 01:00:09.492306',5,1,1,'','Изображение','','','',26,0,'','','','',''),(170,NULL,'2021-03-10 01:00:09.500251','2021-03-10 01:00:09.500274',1,1,1,'','Можно ли звонить не только на 8800?','','','',26,0,'','','','Да, но, к сожалению, пока мы не можем разрешить звонки всем бесплатно на любые номера, поэтому на данный момент предусмотрены платные услуги, но, может в скором времени наши возможности позволят звонить бесплатно на все номера<br>',''),(171,NULL,'2021-03-10 01:00:09.506910','2021-03-10 01:00:09.506931',2,1,1,'','Можно ли мне такую же услугу на сайт?','','','',26,0,'','','','Если вы хотите давать возможность звонить со своего сайта, тогда вам следует связаться с нашим менеджером, мы проконсультируем вас как это можно сделать и что для этого потребуется<br>',''),(172,NULL,'2021-03-10 01:00:09.513309','2021-03-10 01:00:09.513331',3,1,1,'','Что будет если хулиганы воспользуются сервисом?','','','',26,0,'','','','К сожалению, такое может произойти, в этом случае как и в любом другом - инцидент будет рассмотрен правохранительными органами, мы передадим всю имеющуюся информацию компетентным структурам и вопрос будет решен согласно законам РФ<br>',''),(173,'173.jpeg','2021-03-10 01:09:15.257931','2021-03-10 01:10:59.785157',96,1,1,'','Поддержка webrtc в safari','','','',27,0,'','','','Теперь вы можете звонить с safari браузера, ранее такой возможности не было, так как apple придерживалась минимализма в сафари браузере и не добавляло поддержку популярного протокола webrtc<br>',''),(174,'174.jpeg','2021-03-10 01:09:16.167764','2021-03-10 01:12:07.001099',97,1,1,'','Новый M1 на apple','','','',27,0,'','','','Apple выпустило новые ноутбуки с процессором М1, который обгоняет по производительности самые мощные игровые ноутбуки, огрызок при этом даже не включает вентиллятор<br>',''),(175,'175.jpeg','2021-03-10 01:09:17.169352','2021-03-10 01:12:52.067954',98,1,1,'','Звони без сети','','','',27,0,'','','','С нашим сервисом вам достаточно подключиться к любому вай-фаю и даже если ваша сеть не ловит или вы в роуминге, то используя наш сервис вы сможете звонить бесплатно<br>',''),(176,'173.jpeg','2021-03-10 01:15:13.952714','2021-03-10 01:15:13.952732',96,1,1,'','Поддержка webrtc в safari','','','',28,0,'','','','Теперь вы можете звонить с safari браузера, ранее такой возможности не было, так как apple придерживалась минимализма в сафари браузере и не добавляло поддержку популярного протокола webrtc<br>',''),(177,'174.jpeg','2021-03-10 01:15:13.955141','2021-03-10 01:15:13.955157',97,1,1,'','Новый M1 на apple','','','',28,0,'','','','Apple выпустило новые ноутбуки с процессором М1, который обгоняет по производительности самые мощные игровые ноутбуки, огрызок при этом даже не включает вентиллятор<br>',''),(178,'175.jpeg','2021-03-10 01:15:13.963390','2021-03-10 01:15:13.963411',98,1,1,'','Звони без сети','','','',28,0,'','','','С нашим сервисом вам достаточно подключиться к любому вай-фаю и даже если ваша сеть не ловит или вы в роуминге, то используя наш сервис вы сможете звонить бесплатно<br>',''),(179,NULL,'2021-03-10 01:21:39.756525','2021-03-10 01:21:43.515645',99,1,4,'','Тарифы','','#price','',2,0,'','','','',''),(180,NULL,'2021-03-10 01:21:54.267088','2021-03-10 01:21:56.881376',100,1,4,'','FAQ','','#faq','',2,0,'','','','',''),(181,NULL,'2021-03-10 01:22:15.868850','2021-03-10 01:22:21.699211',101,1,4,'','Новости','','#blog','',2,0,'','','','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
INSERT INTO `flatcontent_containers` VALUES (1,NULL,'2021-03-09 21:57:21.554513','2021-03-09 21:57:21.554548',1,1,2,NULL,'Контент для всех страничек','Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики','main',NULL,NULL),(2,NULL,'2021-03-09 21:57:21.612079','2021-03-09 21:57:21.612098',2,1,1,NULL,'Главное меню','Создано автоматически, выводит главное меню','mainmenu',NULL,NULL),(3,NULL,'2021-03-09 21:57:21.614378','2021-03-09 22:59:32.542172',3,1,1,'','Главная страничка','','','',''),(4,NULL,'2021-03-09 22:02:49.640557','2021-03-09 22:02:49.640584',4,1,7,NULL,'Каталог товаров',NULL,'catalogue',NULL,NULL),(5,NULL,'2021-03-09 22:21:18.810478','2021-03-09 22:21:18.810502',5,1,99,'','Слайдер','','slider','',''),(6,NULL,'2021-03-09 22:59:05.481206','2021-03-09 22:59:05.481237',6,1,3,'','Слайдер на главной','','slider','',''),(7,NULL,'2021-03-09 23:02:30.934530','2021-03-09 23:02:30.934549',7,1,99,'','Преимущества','','advantages','',''),(8,NULL,'2021-03-09 23:07:00.644031','2021-03-09 23:07:00.644050',8,1,3,'','Преимущества','','advantages','',''),(9,NULL,'2021-03-09 23:07:29.453970','2021-03-09 23:07:55.511722',9,1,99,'','Статья','О нашей компании<br>','article','',''),(10,NULL,'2021-03-09 23:24:12.604558','2021-03-09 23:24:30.980942',10,1,3,'','Звонки через наш сайт','О нашем сервисе<br>','article','',''),(11,NULL,'2021-03-09 23:28:04.339447','2021-03-09 23:28:04.339466',11,1,99,'','Кнопка - Заголовок','','call_to_action','',''),(12,NULL,'2021-03-09 23:32:41.817823','2021-03-09 23:32:41.817845',12,1,3,'','Видео-инструкция','','call_to_action','',''),(13,NULL,'2021-03-09 23:36:45.260885','2021-03-09 23:36:54.877758',13,1,99,'','Услуги','Как работает наш сервис?<br>','services','',''),(14,NULL,'2021-03-09 23:50:45.983190','2021-03-09 23:50:45.988463',14,1,3,'','Звоните через браузер','Как работает наш сервис?<br>','services','',''),(15,NULL,'2021-03-09 23:51:55.143313','2021-03-09 23:56:20.528717',15,1,99,'','Галерея','Звонить через браузер - легко<br>','gallery','',''),(16,NULL,'2021-03-09 23:56:34.622899','2021-03-09 23:56:34.626304',16,1,3,'','Как сделать звонок?','Звонить через браузер - легко<br>','gallery','',''),(17,NULL,'2021-03-10 00:01:48.261574','2021-03-10 00:01:48.261592',17,1,99,'','Отзывы','Что говорят наши пользователи?<br>','reviews','',''),(18,NULL,'2021-03-10 00:11:03.103701','2021-03-10 00:11:03.108089',18,1,3,'','Отзывы','Что говорят наши пользователи?<br>','reviews','',''),(19,NULL,'2021-03-10 00:11:40.333919','2021-03-10 00:11:51.777316',19,1,99,'','Команда','Наша команда альтруистов<br>','team','',''),(20,NULL,'2021-03-10 00:21:31.860988','2021-03-10 00:21:31.865934',20,1,3,'','Команда','Наша команда альтруистов<br>','team','',''),(21,NULL,'2021-03-10 00:25:12.144303','2021-03-10 00:25:12.144325',21,1,99,'','Счетчики','','counters','',''),(22,NULL,'2021-03-10 00:32:26.500898','2021-03-10 00:32:26.500921',22,1,3,'','Счетчики','','counters','',''),(23,NULL,'2021-03-10 00:33:21.546921','2021-03-10 00:33:34.481359',23,1,99,'','Прайс-лист','Тарифные планы<br>','prices','',''),(24,NULL,'2021-03-10 00:45:59.574581','2021-03-10 00:45:59.579812',24,1,3,'','Тарифы','Тарифные планы<br>','prices','',''),(25,NULL,'2021-03-10 00:48:34.012169','2021-03-10 01:00:29.249758',25,1,99,'','FAQ','Ответы на вопросы','faq','',''),(26,NULL,'2021-03-10 01:00:09.456262','2021-03-10 01:00:16.794939',26,1,3,'','FAQ','Ответы на вопросы<br>','faq','',''),(27,NULL,'2021-03-10 01:09:08.371786','2021-03-10 01:09:08.371806',27,1,99,'','Новости','Последние новости<br>','news','',''),(28,NULL,'2021-03-10 01:15:13.944035','2021-03-10 01:15:13.950515',28,1,3,'','Новости','Последние новости<br>','news','','');
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
INSERT INTO `flatcontent_linkcontainer` VALUES (67,NULL,'2021-03-10 01:15:21.500908','2021-03-10 01:15:21.500931',1,1,NULL,NULL,61,6),(68,NULL,'2021-03-10 01:15:21.502330','2021-03-10 01:15:21.502349',2,1,NULL,NULL,61,8),(69,NULL,'2021-03-10 01:15:21.503674','2021-03-10 01:15:21.503692',3,1,NULL,NULL,61,10),(70,NULL,'2021-03-10 01:15:21.504996','2021-03-10 01:15:21.505016',4,1,NULL,NULL,61,12),(71,NULL,'2021-03-10 01:15:21.506399','2021-03-10 01:15:21.506419',5,1,NULL,NULL,61,14),(72,NULL,'2021-03-10 01:15:21.507735','2021-03-10 01:15:21.507753',6,1,NULL,NULL,61,16),(73,NULL,'2021-03-10 01:15:21.509090','2021-03-10 01:15:21.509108',7,1,NULL,NULL,61,18),(74,NULL,'2021-03-10 01:15:21.510452','2021-03-10 01:15:21.510471',8,1,NULL,NULL,61,20),(75,NULL,'2021-03-10 01:15:21.511783','2021-03-10 01:15:21.511801',9,1,NULL,NULL,61,22),(76,NULL,'2021-03-10 01:15:21.513077','2021-03-10 01:15:21.513095',10,1,NULL,NULL,61,24),(77,NULL,'2021-03-10 01:15:21.514401','2021-03-10 01:15:21.514419',11,1,NULL,NULL,61,26),(78,NULL,'2021-03-10 01:15:21.515745','2021-03-10 01:15:21.515763',12,1,NULL,NULL,61,28);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_customuser`
--

LOCK TABLES `login_customuser` WRITE;
/*!40000 ALTER TABLE `login_customuser` DISABLE KEYS */;
INSERT INTO `login_customuser` VALUES (1,NULL,'2021-03-09 21:45:30.863149','2021-03-09 21:57:25.665666',1,1,NULL,NULL,NULL,NULL,1);
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
INSERT INTO `main_functions_config` VALUES (1,'Почта обратной связи','flatcontent_feedback','dkramorov@mail.ru','2021-03-09 21:57:21.669157',NULL,1,NULL,1,NULL,'2021-03-09 21:57:21.669178',NULL);
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-10  1:27:22
