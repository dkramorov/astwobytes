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
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add user',3,'add_user'),(10,'Can change user',3,'change_user'),(11,'Can delete user',3,'delete_user'),(12,'Can view user',3,'view_user'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Админка - Настройка',6,'add_config'),(22,'Can change Админка - Настройка',6,'change_config'),(23,'Can delete Админка - Настройка',6,'delete_config'),(24,'Can view Админка - Настройка',6,'view_config'),(25,'Can add Админка - Задача',7,'add_tasks'),(26,'Can change Админка - Задача',7,'change_tasks'),(27,'Can delete Админка - Задача',7,'delete_tasks'),(28,'Can view Админка - Задача',7,'view_tasks'),(29,'Can add captcha',8,'add_captcha'),(30,'Can change captcha',8,'change_captcha'),(31,'Can delete captcha',8,'delete_captcha'),(32,'Can view captcha',8,'view_captcha'),(33,'Can add custom user',12,'add_customuser'),(34,'Can change custom user',12,'change_customuser'),(35,'Can delete custom user',12,'delete_customuser'),(36,'Can view custom user',12,'view_customuser'),(37,'Can add Стат.контет - Файл',13,'add_files'),(38,'Can change Стат.контет - Файл',13,'change_files'),(39,'Can delete Стат.контет - Файл',13,'delete_files'),(40,'Can view Стат.контет - Файл',13,'view_files'),(41,'Can add Стат.контент - Блоки',14,'add_blocks'),(42,'Can change Стат.контент - Блоки',14,'change_blocks'),(43,'Can delete Стат.контент - Блоки',14,'delete_blocks'),(44,'Can view Стат.контент - Блоки',14,'view_blocks'),(45,'Заполнение сео-полей меню',14,'seo_fields'),(46,'Can add Стат.контент - Контейнеры',15,'add_containers'),(47,'Can change Стат.контент - Контейнеры',15,'change_containers'),(48,'Can delete Стат.контент - Контейнеры',15,'delete_containers'),(49,'Can view Стат.контент - Контейнеры',15,'view_containers'),(50,'Can add Стат.контент - Линковка меню к контейнерам',16,'add_linkcontainer'),(51,'Can change Стат.контент - Линковка меню к контейнерам',16,'change_linkcontainer'),(52,'Can delete Стат.контент - Линковка меню к контейнерам',16,'delete_linkcontainer'),(53,'Can view Стат.контент - Линковка меню к контейнерам',16,'view_linkcontainer'),(54,'Can add Пользователи - пользователь',17,'add_shopper'),(55,'Can change Пользователи - пользователь',17,'change_shopper'),(56,'Can delete Пользователи - пользователь',17,'delete_shopper'),(57,'Can view Пользователи - пользователь',17,'view_shopper');
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$ptaNw5VOPnt9$zJWui6iBrIhrQIxbHcBLreGRK+ICLGV6j1neJ6PGj48=','2022-02-01 14:09:24.917896',1,'jocker','','','dkramorov@mail.ru',1,1,'2022-02-01 14:04:55.773731'),(2,'pbkdf2_sha256$150000$9aw5f82u2Yzm$wQv4UFM40yWJmP7TUgt9O7n8c4Q2OvgxvwOAaMGquS0=',NULL,1,'alex','Александр','','',1,1,'2022-02-01 14:09:48.960409'),(3,'pbkdf2_sha256$150000$Ts302GobjEqG$Vfbuv3Bqst9Z2r3kOPGsyl/RJ0IrL5XQeCyuCc+OI5M=',NULL,0,'SeoManager','','SeoManager','seo_manager@masterme.ru',1,1,'2022-02-01 14:52:08.879296');
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(13,'files','files'),(14,'flatcontent','blocks'),(15,'flatcontent','containers'),(16,'flatcontent','linkcontainer'),(12,'login','customuser'),(9,'login','extrafields'),(11,'login','extrainfo'),(10,'login','extravalues'),(8,'main_functions','captcha'),(6,'main_functions','config'),(7,'main_functions','tasks'),(17,'personal','shopper'),(5,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2022-02-01 14:04:52.268479'),(2,'contenttypes','0002_remove_content_type_name','2022-02-01 14:04:52.335043'),(3,'auth','0001_initial','2022-02-01 14:04:52.635253'),(4,'auth','0002_alter_permission_name_max_length','2022-02-01 14:04:53.022428'),(5,'auth','0003_alter_user_email_max_length','2022-02-01 14:04:53.061302'),(6,'auth','0004_alter_user_username_opts','2022-02-01 14:04:53.070161'),(7,'auth','0005_alter_user_last_login_null','2022-02-01 14:04:53.107877'),(8,'auth','0006_require_contenttypes_0002','2022-02-01 14:04:53.109950'),(9,'auth','0007_alter_validators_add_error_messages','2022-02-01 14:04:53.117014'),(10,'auth','0008_alter_user_username_max_length','2022-02-01 14:04:53.154477'),(11,'auth','0009_alter_user_last_name_max_length','2022-02-01 14:04:53.193073'),(12,'auth','0010_alter_group_name_max_length','2022-02-01 14:04:53.230157'),(13,'auth','0011_update_proxy_permissions','2022-02-01 14:04:53.239057'),(14,'files','0001_initial','2022-02-01 14:04:53.293554'),(15,'files','0002_auto_20191203_2054','2022-02-01 14:04:53.574986'),(16,'files','0003_auto_20200112_1717','2022-02-01 14:04:53.608108'),(17,'files','0004_auto_20200402_2127','2022-02-01 14:04:53.664192'),(18,'files','0005_auto_20200809_1025','2022-02-01 14:04:53.668613'),(19,'files','0006_auto_20210516_1530','2022-02-01 14:04:53.719709'),(20,'flatcontent','0001_initial','2022-02-01 14:04:53.934498'),(21,'flatcontent','0002_auto_20190825_1730','2022-02-01 14:04:54.953774'),(22,'flatcontent','0003_auto_20191203_2054','2022-02-01 14:04:55.090691'),(23,'flatcontent','0004_blocks_html','2022-02-01 14:04:55.134975'),(24,'flatcontent','0005_auto_20200112_1717','2022-02-01 14:04:55.226338'),(25,'flatcontent','0006_auto_20200314_1638','2022-02-01 14:04:55.234603'),(26,'flatcontent','0007_auto_20200402_2127','2022-02-01 14:04:55.404380'),(27,'flatcontent','0008_containers_class_name','2022-02-01 14:04:55.451550'),(28,'flatcontent','0009_blocks_class_name','2022-02-01 14:04:55.518573'),(29,'flatcontent','0010_auto_20210430_1708','2022-02-01 14:04:55.550011'),(30,'flatcontent','0011_auto_20210526_2033','2022-02-01 14:04:55.557160'),(31,'login','0001_initial','2022-02-01 14:04:55.837188'),(32,'login','0002_auto_20200925_1007','2022-02-01 14:04:56.851853'),(33,'main_functions','0001_initial','2022-02-01 14:04:56.933956'),(34,'main_functions','0002_auto_20191203_2052','2022-02-01 14:04:57.019269'),(35,'main_functions','0003_auto_20200407_1845','2022-02-01 14:04:57.765427'),(36,'main_functions','0004_config_user','2022-02-01 14:04:58.237910'),(37,'main_functions','0005_auto_20210321_1210','2022-02-01 14:04:58.283942'),(38,'main_functions','0006_captcha','2022-02-01 14:04:58.314202'),(39,'personal','0001_initial','2022-02-01 14:04:58.398463'),(40,'personal','0002_auto_20200528_1642','2022-02-01 14:04:58.948494'),(41,'personal','0003_auto_20200616_1707','2022-02-01 14:04:58.981952'),(42,'personal','0004_shopper_ip','2022-02-01 14:04:59.028146'),(43,'personal','0005_shopper_phone_confirmed','2022-02-01 14:04:59.122360'),(44,'sessions','0001_initial','2022-02-01 14:04:59.191270');
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
INSERT INTO `django_session` VALUES ('7n1ufesaywodh2pzvobh1qvf6qfrg8jj','ZThkMDFlNDVmMDY5ZjQ5M2Q5ZTQwM2IzOGU4ZTAyZjFiNmUxZDQwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImU4NDk1MjZiZjRjMDFmOTE0ZjM4YzdhZTY3NjI4MmIxMWRhYWE0NGEifQ==','2022-02-15 14:09:24.922587');
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
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
INSERT INTO `flatcontent_blocks` VALUES (1,'1.png','2022-02-01 14:52:08.799990','2022-02-01 16:09:03.395574',1,1,1,'','Логотип','Быстро, просто, удобно','/','logo',3,0,'','','Страхование','',''),(2,NULL,'2022-02-01 14:52:08.801523','2022-02-01 14:52:08.801529',2,1,3,'','Телефон',NULL,'tel:73952123321','phone',3,0,NULL,NULL,NULL,'+7(3952) 123-321',NULL),(3,NULL,'2022-02-01 14:52:08.807296','2022-02-01 14:52:08.807326',3,1,3,'','Адрес',NULL,NULL,'address',3,0,NULL,NULL,NULL,'г. Иркутск ул. Советская 32а офис 5',NULL),(4,NULL,'2022-02-01 14:52:08.814605','2022-02-01 14:52:08.814610',4,1,3,'','Email',NULL,NULL,'email',3,0,NULL,NULL,NULL,'test@test.ru',NULL),(5,NULL,'2022-02-01 14:52:08.815911','2022-02-01 14:52:08.815916',5,1,3,'','Режим работы',NULL,NULL,'worktime',3,0,NULL,NULL,NULL,'пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 17:00',NULL),(6,NULL,'2022-02-01 14:52:08.817424','2022-02-01 14:52:08.817430',6,1,3,'','Copyright',NULL,NULL,'copyright',3,0,NULL,NULL,NULL,'<p>&copy; 2020 Все права защищены</p>',NULL),(7,NULL,'2022-02-01 14:52:08.826162','2022-02-01 14:52:08.826167',7,1,3,'','Название компании',NULL,NULL,'company_name',3,0,NULL,NULL,'Company name',NULL,NULL),(8,NULL,'2022-02-01 14:52:08.827424','2022-02-01 14:52:08.827429',8,1,3,'','Favicon',NULL,NULL,'favicon',3,0,NULL,NULL,NULL,NULL,NULL),(9,NULL,'2022-02-01 14:52:08.828657','2022-02-01 14:52:08.828662',9,1,3,'','Сообщества',NULL,NULL,'social',3,0,NULL,NULL,NULL,NULL,NULL),(10,NULL,'2022-02-01 14:52:08.829904','2022-02-01 14:52:08.829908',10,1,3,'_9','instagram',NULL,NULL,'instagram',3,1,'instagram',NULL,NULL,NULL,NULL),(11,NULL,'2022-02-01 14:52:08.831120','2022-02-01 14:52:08.831125',11,1,3,'_9','vk',NULL,NULL,'vk',3,1,'vk',NULL,NULL,NULL,NULL),(12,NULL,'2022-02-01 14:52:08.832398','2022-02-01 14:52:08.832403',12,1,3,'_9','facebook',NULL,NULL,'facebook',3,1,'facebook',NULL,NULL,NULL,NULL),(13,NULL,'2022-02-01 14:52:08.833718','2022-02-01 14:52:08.833724',13,1,3,'_9','twitter',NULL,NULL,'twitter',3,1,'twitter',NULL,NULL,NULL,NULL),(14,NULL,'2022-02-01 14:52:08.835282','2022-02-01 14:52:08.835292',14,1,3,'','Яндекс.Метрика счетчик',NULL,NULL,'yandex_metrika',3,0,NULL,NULL,NULL,'<script type=\"text/javascript\"></script>',NULL),(15,NULL,'2022-02-01 14:52:08.836616','2022-02-01 14:52:08.836621',15,1,3,'','Google.Analytics счетчик',NULL,NULL,'google_analytics',3,0,NULL,NULL,NULL,'<script type=\"text/javascript\"></script>',NULL),(16,NULL,'2022-02-01 14:52:08.839971','2022-02-01 15:32:33.108318',16,1,4,'','Главная','','/','_mainmenu_mainpage',4,0,'','','','',''),(22,NULL,'2022-02-01 14:52:08.848780','2022-02-01 14:52:08.848785',22,1,4,'','О нас',NULL,'/about/','_mainmenu_aboutpage',4,0,NULL,NULL,NULL,NULL,NULL),(23,NULL,'2022-02-01 14:52:08.850016','2022-02-01 14:52:08.850021',23,1,4,'','Услуги',NULL,'/services/','_mainmenu_servicespage',4,0,NULL,NULL,NULL,NULL,NULL),(24,NULL,'2022-02-01 14:52:08.852310','2022-02-01 14:52:08.852316',24,1,4,'','Контакты',NULL,'/feedback/','_mainmenu_feedbackpage',4,0,NULL,NULL,NULL,NULL,NULL),(25,NULL,'2022-02-01 14:52:08.855136','2022-02-01 14:52:08.855141',25,1,4,'','Каталог',NULL,'/cat/','_bottommenu_catpage',5,0,NULL,NULL,NULL,NULL,NULL),(26,NULL,'2022-02-01 14:52:08.857425','2022-02-01 14:52:08.857432',26,1,4,'_25','Популярные товары',NULL,'/cat/populyarnye-tovary/','_bottommenu_catpage_popular',5,0,NULL,NULL,NULL,NULL,NULL),(27,NULL,'2022-02-01 14:52:08.859068','2022-02-01 14:52:08.859073',27,1,4,'_25','Новые товары',NULL,'/cat/novye-tovary/','_bottommenu_catpage_new',5,0,NULL,NULL,NULL,NULL,NULL),(28,NULL,'2022-02-01 14:52:08.860508','2022-02-01 14:52:08.860513',28,1,4,'_25','Товары со скидкой',NULL,'/cat/tovary-so-skidkoy/','_bottommenu_catpage_discount',5,0,NULL,NULL,NULL,NULL,NULL),(29,NULL,'2022-02-01 14:52:08.861975','2022-02-01 14:52:08.861981',29,1,4,'_25','Распродажа',NULL,'/cat/rasprodaja/','_bottommenu_catpage_sale',5,0,NULL,NULL,NULL,NULL,NULL),(30,NULL,'2022-02-01 14:52:08.863178','2022-02-01 14:52:08.863183',30,1,4,'','О нас',NULL,'/about/','_bottommenu_aboutpage',5,0,NULL,NULL,NULL,NULL,NULL),(31,NULL,'2022-02-01 14:52:08.864391','2022-02-01 14:52:08.864396',31,1,4,'','Услуги',NULL,'/services/','_bottommenu_servicespage',5,0,NULL,NULL,NULL,NULL,NULL),(32,NULL,'2022-02-01 14:52:08.865637','2022-02-01 14:52:08.865642',32,1,4,'','Контакты',NULL,'/feedback/','_bottommenu_feedbackpage',5,0,NULL,NULL,NULL,NULL,NULL),(33,'33.png','2022-02-01 15:04:19.627534','2022-02-01 15:08:47.527926',33,1,1,'','Выгодно','','/','',6,0,'','','Подробнее','Выгодное предложение специально для членов Трудовых Резервов',''),(34,'34.png','2022-02-01 15:04:20.691186','2022-02-01 15:08:52.566413',34,1,1,'','Удобно','','/','',6,0,'','','Подробнее','Тарифы на все варианты участия в мероприятиях',''),(35,'35.png','2022-02-01 15:04:21.667901','2022-02-01 15:08:57.560022',35,1,1,'','Доступно','','/','',6,0,'','','Подробнее','Синхронизация данных о страховке с мандатной комиссией',''),(36,'33.png','2022-02-01 15:09:50.431919','2022-02-01 15:09:50.431980',33,1,1,'','Выгодно','','/','',7,0,'','','Подробнее','Выгодное предложение специально для членов Трудовых Резервов',''),(37,'34.png','2022-02-01 15:09:50.437345','2022-02-01 15:09:50.437381',34,1,1,'','Удобно','','/','',7,0,'','','Подробнее','Тарифы на все варианты участия в мероприятиях',''),(38,'35.png','2022-02-01 15:09:50.442155','2022-02-01 15:09:50.442190',35,1,1,'','Доступно','','/','',7,0,'','','Подробнее','Синхронизация данных о страховке с мандатной комиссией',''),(39,NULL,'2022-02-01 15:13:32.381689','2022-02-01 15:15:18.581420',36,1,1,'','Вопрос по страхованию жизни','','','',8,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно частым и возникает обычно у человека, который решил застраховаться, но имеет недостаточно информации по этой процедуре<br>',''),(40,NULL,'2022-02-01 15:13:33.409621','2022-02-01 15:15:21.245298',37,1,1,'','Вопрос по страхованию имущества','','','',8,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(41,NULL,'2022-02-01 15:13:34.282973','2022-02-01 15:15:23.958548',38,1,1,'','Вопрос по автострахованию','','','',8,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(42,NULL,'2022-02-01 15:13:35.106173','2022-02-01 15:15:26.520410',39,1,1,'','Вопрос по стрхованию ребенка','','','',8,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(43,NULL,'2022-02-01 15:13:35.859948','2022-02-01 15:15:29.000050',40,1,1,'','Вопрос по страхованию пенсионера','','','',8,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(44,NULL,'2022-02-01 15:13:36.873947','2022-02-01 15:15:31.719473',41,1,1,'','Вопрос по выплатам','','','',8,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(45,NULL,'2022-02-01 15:16:29.398689','2022-02-01 15:16:29.398720',36,1,1,'','Вопрос по страхованию жизни','','','',9,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно частым и возникает обычно у человека, который решил застраховаться, но имеет недостаточно информации по этой процедуре<br>',''),(46,NULL,'2022-02-01 15:16:29.401125','2022-02-01 15:16:29.401152',37,1,1,'','Вопрос по страхованию имущества','','','',9,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(47,NULL,'2022-02-01 15:16:29.402556','2022-02-01 15:16:29.402582',38,1,1,'','Вопрос по автострахованию','','','',9,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(48,NULL,'2022-02-01 15:16:29.403865','2022-02-01 15:16:29.403889',39,1,1,'','Вопрос по стрхованию ребенка','','','',9,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(49,NULL,'2022-02-01 15:16:29.405161','2022-02-01 15:16:29.405186',40,1,1,'','Вопрос по страхованию пенсионера','','','',9,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(50,NULL,'2022-02-01 15:16:29.406587','2022-02-01 15:16:29.406621',41,1,1,'','Вопрос по выплатам','','','',9,0,'','','','Здесь подробный ответ по заданному вопросу, который является довольно \r\nчастым и возникает обычно у человека, который решил застраховаться, но \r\nимеет недостаточно информации по этой процедуре',''),(51,'51.jpg','2022-02-01 15:18:32.228604','2022-02-01 15:18:32.228643',42,1,1,'','Без названия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(52,'52.jpg','2022-02-01 15:18:33.095500','2022-02-01 15:18:33.095539',43,1,1,'','Без названия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(53,'53.jpg','2022-02-01 15:18:33.924683','2022-02-01 15:18:33.924723',44,1,1,'','Без названия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(54,'54.jpg','2022-02-01 15:18:34.745219','2022-02-01 15:18:34.745260',45,1,1,'','Без названия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(55,'55.jpg','2022-02-01 15:18:35.714577','2022-02-01 15:18:35.714612',46,1,1,'','Без названия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(56,'56.jpg','2022-02-01 15:18:36.770311','2022-02-01 15:18:36.770357',47,1,1,'','Без названия',NULL,NULL,NULL,10,0,NULL,NULL,NULL,NULL,NULL),(57,'51.jpg','2022-02-01 15:21:15.373446','2022-02-01 15:21:15.373491',42,1,1,'','Без названия',NULL,NULL,NULL,11,0,NULL,NULL,NULL,NULL,NULL),(58,'52.jpg','2022-02-01 15:21:15.379619','2022-02-01 15:21:15.379662',43,1,1,'','Без названия',NULL,NULL,NULL,11,0,NULL,NULL,NULL,NULL,NULL),(59,'53.jpg','2022-02-01 15:21:15.392700','2022-02-01 15:21:15.392744',44,1,1,'','Без названия',NULL,NULL,NULL,11,0,NULL,NULL,NULL,NULL,NULL),(60,'54.jpg','2022-02-01 15:21:15.396731','2022-02-01 15:21:15.396768',45,1,1,'','Без названия',NULL,NULL,NULL,11,0,NULL,NULL,NULL,NULL,NULL),(61,'55.jpg','2022-02-01 15:21:15.400714','2022-02-01 15:21:15.400752',46,1,1,'','Без названия',NULL,NULL,NULL,11,0,NULL,NULL,NULL,NULL,NULL),(62,'56.jpg','2022-02-01 15:21:15.405506','2022-02-01 15:21:15.405553',47,1,1,'','Без названия',NULL,NULL,NULL,11,0,NULL,NULL,NULL,NULL,NULL),(63,NULL,'2022-02-01 15:28:00.875343','2022-02-01 15:28:59.963537',48,1,1,'','Консультации по страхованию','','','',12,0,'','','','Мы предоставляем консультацию по телефону и также вы можете задать вопрос через сайт, наш специалист свяжется с вами и ответит на интересующие вас вопросы в удобное для вас время<br>',''),(64,NULL,'2022-02-01 15:28:01.976923','2022-02-01 15:29:08.549568',49,1,1,'','Консультации по выплатам','','','',12,0,'','','','Мы предоставляем консультацию по телефону и также вы можете задать \r\nвопрос через сайт, наш специалист свяжется с вами и ответит на \r\nинтересующие вас вопросы в удобное для вас время',''),(65,'65.jpg','2022-02-01 15:28:03.181986','2022-02-01 15:32:12.833493',50,1,1,'','Консультант Ирина','','','spec1',12,0,'','','','+7 (3952) 321-321<br>',''),(66,'66.jpg','2022-02-01 15:28:04.382353','2022-02-01 15:32:04.853988',51,1,1,'','Зам директора Аня','','','spec2',12,0,'','','','+7 (3952) 123-321<br>',''),(67,NULL,'2022-02-01 15:32:25.135342','2022-02-01 15:32:25.135387',48,1,1,'','Консультации по страхованию','','','',13,0,'','','','Мы предоставляем консультацию по телефону и также вы можете задать вопрос через сайт, наш специалист свяжется с вами и ответит на интересующие вас вопросы в удобное для вас время<br>',''),(68,NULL,'2022-02-01 15:32:25.138274','2022-02-01 15:32:25.138304',49,1,1,'','Консультации по выплатам','','','',13,0,'','','','Мы предоставляем консультацию по телефону и также вы можете задать \r\nвопрос через сайт, наш специалист свяжется с вами и ответит на \r\nинтересующие вас вопросы в удобное для вас время',''),(69,'65.jpg','2022-02-01 15:32:25.144336','2022-02-01 15:32:25.144364',50,1,1,'','Консультант Ирина','','','spec1',13,0,'','','','+7 (3952) 321-321<br>',''),(70,'66.jpg','2022-02-01 15:32:25.149684','2022-02-01 15:32:25.149739',51,1,1,'','Зам директора Аня','','','spec2',13,0,'','','','+7 (3952) 123-321<br>',''),(71,NULL,'2022-02-01 16:27:45.511364','2022-02-01 16:27:45.511410',52,1,1,'','О нас','','','about',3,0,'','','','Мы занимаемся страхованием жизни и имущества. Если вы хотите застровать себя, близких или движимое и недвижимое имущество, тогда вы определенно попали куда нужно. У нас вы сможете легко и быстро оформить страховку и получить ответы на вопросы<br>','');
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
INSERT INTO `flatcontent_containers` VALUES (1,NULL,'2022-02-01 14:47:38.802503','2022-02-01 14:47:38.802541',1,1,99,'','Демонстрационная форма','','form1','',''),(2,NULL,'2022-02-01 14:51:39.368480','2022-02-01 14:51:39.368549',2,1,3,'','Демо-форма','','form1','',''),(3,NULL,'2022-02-01 14:52:08.794883','2022-02-01 14:52:08.794895',3,1,2,NULL,'Контент для всех страничек','Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики','main',NULL,NULL),(4,NULL,'2022-02-01 14:52:08.837725','2022-02-01 14:52:08.837730',4,1,1,NULL,'Главное меню','Создано автоматически, выводит главное меню','mainmenu',NULL,NULL),(5,NULL,'2022-02-01 14:52:08.838786','2022-02-01 14:52:08.838791',5,1,1,NULL,'Нижнее меню','Создано автоматически, выводит нижнее меню','bottommenu',NULL,NULL),(6,NULL,'2022-02-01 15:01:56.112942','2022-02-01 15:03:59.453885',6,1,99,'','Преимущества','Мы предлагаем выгодное страхование с удобными условиями для вас<br>','advantages','',''),(7,NULL,'2022-02-01 15:09:50.421314','2022-02-01 15:09:50.427610',7,1,3,'','Преимущества страхования','Мы предлагаем выгодное страхование с удобными условиями для вас<br>','advantages','',''),(8,NULL,'2022-02-01 15:11:40.790869','2022-02-01 15:11:40.790903',8,1,99,'','FAQ','Ответы на часто задаваемые вопросы<br>','faq','',''),(9,NULL,'2022-02-01 15:16:29.384799','2022-02-01 15:16:29.394432',9,1,3,'','Ответы на часто задаваемые вопросы','Ответы на часто задаваемые вопросы<br>','faq','',''),(10,NULL,'2022-02-01 15:17:51.342724','2022-02-01 15:18:08.812697',10,1,99,'','Мини слайдер','Наши лицензии и сертификаты качества<br>','mini_slider','',''),(11,NULL,'2022-02-01 15:21:15.358484','2022-02-01 15:21:15.368224',11,1,3,'','Лицензии','Наши лицензии и сертификаты качества<br>','mini_slider','',''),(12,NULL,'2022-02-01 15:26:43.045122','2022-02-01 15:27:55.581190',12,1,99,'','Контакты','Вы можете связаться с нашими специалистами и получить необходимую информацию<br>','contacts','',''),(13,NULL,'2022-02-01 15:32:25.124225','2022-02-01 15:32:25.130768',13,1,3,'','Консультация','Вы можете связаться с нашими специалистами и получить необходимую информацию<br>','contacts','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_linkcontainer`
--

LOCK TABLES `flatcontent_linkcontainer` WRITE;
/*!40000 ALTER TABLE `flatcontent_linkcontainer` DISABLE KEYS */;
INSERT INTO `flatcontent_linkcontainer` VALUES (11,NULL,'2022-02-01 15:32:33.113551','2022-02-01 15:32:33.113585',1,1,NULL,NULL,16,2),(12,NULL,'2022-02-01 15:32:33.115055','2022-02-01 15:32:33.115079',2,1,NULL,NULL,16,7),(13,NULL,'2022-02-01 15:32:33.116641','2022-02-01 15:32:33.116667',3,1,NULL,NULL,16,9),(14,NULL,'2022-02-01 15:32:33.118344','2022-02-01 15:32:33.118365',4,1,NULL,NULL,16,11),(15,NULL,'2022-02-01 15:32:33.120195','2022-02-01 15:32:33.120225',5,1,NULL,NULL,16,13);
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
INSERT INTO `login_customuser` VALUES (1,NULL,'2022-02-01 14:04:55.827711','2022-02-01 14:09:24.920305',1,1,NULL,NULL,NULL,NULL,1),(2,NULL,'2022-02-01 14:09:48.963053','2022-02-01 14:09:49.021559',2,1,NULL,NULL,'','',2),(3,NULL,'2022-02-01 14:52:08.905319','2022-02-01 14:52:08.936606',3,1,NULL,NULL,NULL,NULL,3);
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-01 16:33:46
