-- MySQL dump 10.13  Distrib 5.7.20, for osx10.11 (x86_64)
--
-- Host: localhost    Database: borey
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
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add user',3,'add_user'),(10,'Can change user',3,'change_user'),(11,'Can delete user',3,'delete_user'),(12,'Can view user',3,'view_user'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Админка - Настрока',6,'add_config'),(22,'Can change Админка - Настрока',6,'change_config'),(23,'Can delete Админка - Настрока',6,'delete_config'),(24,'Can view Админка - Настрока',6,'view_config'),(25,'Can add Админка - Задача',7,'add_tasks'),(26,'Can change Админка - Задача',7,'change_tasks'),(27,'Can delete Админка - Задача',7,'delete_tasks'),(28,'Can view Админка - Задача',7,'view_tasks'),(29,'Can add custom user',8,'add_customuser'),(30,'Can change custom user',8,'change_customuser'),(31,'Can delete custom user',8,'delete_customuser'),(32,'Can view custom user',8,'view_customuser'),(33,'Can add Стат.контет - Файлы',9,'add_files'),(34,'Can change Стат.контет - Файлы',9,'change_files'),(35,'Can delete Стат.контет - Файлы',9,'delete_files'),(36,'Can view Стат.контет - Файлы',9,'view_files'),(37,'Can add Стат.контент - Блоки',10,'add_blocks'),(38,'Can change Стат.контент - Блоки',10,'change_blocks'),(39,'Can delete Стат.контент - Блоки',10,'delete_blocks'),(40,'Can view Стат.контент - Блоки',10,'view_blocks'),(41,'Can add Стат.контент - Контейнеры',11,'add_containers'),(42,'Can change Стат.контент - Контейнеры',11,'change_containers'),(43,'Can delete Стат.контент - Контейнеры',11,'delete_containers'),(44,'Can view Стат.контент - Контейнеры',11,'view_containers'),(45,'Can add Стат.контент - Линковка меню к контейнерам',12,'add_linkcontainer'),(46,'Can change Стат.контент - Линковка меню к контейнерам',12,'change_linkcontainer'),(47,'Can delete Стат.контент - Линковка меню к контейнерам',12,'delete_linkcontainer'),(48,'Can view Стат.контент - Линковка меню к контейнерам',12,'view_linkcontainer');
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$VuC2x9xOr3GR$ivM3prk56DX2+yWFK973lJ+SZisvCXrm2uZOs//RZCU=','2020-04-06 21:17:43.229664',1,'jocker','','','dkramorov@mail.ru',1,1,'2020-04-06 21:16:30.541562'),(2,'pbkdf2_sha256$150000$yuQ5qsnd09dY$U0TlZWbri9UzrU7ZjCogJV7o7h5sF0HxQ4lsSoOb5Xk=',NULL,1,'seva','','','',1,1,'2020-04-06 23:06:39.925784');
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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(9,'files','files'),(10,'flatcontent','blocks'),(11,'flatcontent','containers'),(12,'flatcontent','linkcontainer'),(8,'login','customuser'),(6,'main_functions','config'),(7,'main_functions','tasks'),(5,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-04-06 21:16:29.342942'),(2,'contenttypes','0002_remove_content_type_name','2020-04-06 21:16:29.364500'),(3,'auth','0001_initial','2020-04-06 21:16:29.624322'),(4,'auth','0002_alter_permission_name_max_length','2020-04-06 21:16:29.723420'),(5,'auth','0003_alter_user_email_max_length','2020-04-06 21:16:29.739331'),(6,'auth','0004_alter_user_username_opts','2020-04-06 21:16:29.749317'),(7,'auth','0005_alter_user_last_login_null','2020-04-06 21:16:29.765190'),(8,'auth','0006_require_contenttypes_0002','2020-04-06 21:16:29.766331'),(9,'auth','0007_alter_validators_add_error_messages','2020-04-06 21:16:29.773588'),(10,'auth','0008_alter_user_username_max_length','2020-04-06 21:16:29.791928'),(11,'auth','0009_alter_user_last_name_max_length','2020-04-06 21:16:29.807300'),(12,'auth','0010_alter_group_name_max_length','2020-04-06 21:16:29.823380'),(13,'auth','0011_update_proxy_permissions','2020-04-06 21:16:29.833198'),(14,'files','0001_initial','2020-04-06 21:16:29.873767'),(15,'files','0002_auto_20191203_2054','2020-04-06 21:16:29.924236'),(16,'files','0003_auto_20200112_1717','2020-04-06 21:16:29.932461'),(17,'files','0004_auto_20200402_2127','2020-04-06 21:16:29.947614'),(18,'flatcontent','0001_initial','2020-04-06 21:16:30.079451'),(19,'flatcontent','0002_auto_20190825_1730','2020-04-06 21:16:30.323971'),(20,'flatcontent','0003_auto_20191203_2054','2020-04-06 21:16:30.357859'),(21,'flatcontent','0004_blocks_html','2020-04-06 21:16:30.381411'),(22,'flatcontent','0005_auto_20200112_1717','2020-04-06 21:16:30.416275'),(23,'flatcontent','0006_auto_20200314_1638','2020-04-06 21:16:30.422947'),(24,'flatcontent','0007_auto_20200402_2127','2020-04-06 21:16:30.491895'),(25,'login','0001_customuser','2020-04-06 21:16:30.744940'),(26,'login','0002_auto_20191203_2054','2020-04-06 21:16:30.811957'),(27,'login','0003_auto_20200112_1717','2020-04-06 21:16:30.829046'),(28,'login','0004_auto_20200402_2127','2020-04-06 21:16:30.899080'),(29,'main_functions','0001_initial','2020-04-06 21:16:30.946925'),(30,'main_functions','0002_auto_20191203_2052','2020-04-06 21:16:30.966250'),(31,'sessions','0001_initial','2020-04-06 21:16:30.987129');
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
INSERT INTO `django_session` VALUES ('irtbhkj59699o8gacets54s9a3sx4vpl','ODk4NGFhOWE5Y2Y1ZTFkM2MyNDY1Njk1MDNlZjI4OGEyNGNkODhlZjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjQyMTczODJmZGVlZWRjYWNiODM0ZjE3YzE1YjY4ZjQ1OGEzMDUwYTEifQ==','2020-04-20 21:17:43.234932');
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
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
INSERT INTO `flatcontent_blocks` VALUES (1,'1.png','2020-04-06 21:33:02.983587','2020-04-06 21:33:11.946625',1,1,1,'','Логотип','','','logo',1,0,'','','',''),(2,'2.jpg','2020-04-06 21:57:00.311381','2020-04-06 22:09:39.565917',2,1,1,'','Подавление пыли','чистый воздух','','',2,0,'','','','Комплексные инженерные решения по подавлению пыли чистый воздух \"под ключ\"<br>'),(3,NULL,'2020-04-06 22:00:40.482528','2020-04-06 22:02:38.541756',2,1,1,'_2','Заказать','','/','',2,0,'','','',''),(4,NULL,'2020-04-06 22:00:44.565627','2020-04-06 22:02:35.865660',1,1,1,'_2','Подробнее','','/','',2,0,'','','',''),(6,'6.jpg','2020-04-06 22:23:35.945048','2020-04-06 22:23:35.945074',2,1,1,'','Подавление пыли','чистый воздух','','',4,0,'','','','Комплексные инженерные решения по подавлению пыли чистый воздух \"под ключ\"<br>'),(7,NULL,'2020-04-06 22:23:35.947407','2020-04-06 22:23:35.947445',2,1,1,'_6','Заказать','','/','',4,0,'','','',''),(8,NULL,'2020-04-06 22:23:35.954057','2020-04-06 22:23:35.954081',1,1,1,'_6','Подробнее','','/','',4,0,'','','',''),(12,'12.jpg','2020-04-06 22:33:52.693620','2020-04-06 22:33:52.693645',2,1,1,'','Подавление пыли','чистый воздух','','',6,0,'','','','Комплексные инженерные решения по подавлению пыли чистый воздух \"под ключ\"<br>'),(14,NULL,'2020-04-06 22:33:52.715366','2020-04-06 22:36:57.849296',1,1,1,'_12','Смотреть','','/','play',6,0,'','','',''),(15,'15.jpg','2020-04-06 22:39:28.048153','2020-04-06 22:39:28.048174',2,1,1,'','Подавление пыли','чистый воздух','','',7,0,'','','','Комплексные инженерные решения по подавлению пыли чистый воздух \"под ключ\"<br>'),(17,NULL,'2020-04-06 22:39:28.068421','2020-04-06 22:39:28.068448',1,1,1,'_15','Подробнее','','/','',7,0,'','','',''),(18,NULL,'2020-04-06 22:54:33.526491','2020-04-06 23:05:28.823823',1,1,4,'','Главная','','/','',8,0,'','','',''),(19,NULL,'2020-04-06 22:55:00.850231','2020-04-06 22:55:00.850252',3,1,4,'','Услуги',NULL,'/uslugi/',NULL,8,0,NULL,NULL,NULL,NULL),(20,NULL,'2020-04-06 22:55:04.583935','2020-04-06 22:55:04.583955',4,1,4,'','Продукты',NULL,'/produkty/',NULL,8,0,NULL,NULL,NULL,NULL),(21,NULL,'2020-04-06 22:55:07.992621','2020-04-06 22:55:07.992644',5,1,4,'','Контакты',NULL,'/kontakty/',NULL,8,0,NULL,NULL,NULL,NULL),(22,NULL,'2020-04-06 22:55:11.503175','2020-04-06 22:55:11.503197',2,1,4,'','О нас',NULL,'/o-nas/',NULL,8,0,NULL,NULL,NULL,NULL),(23,NULL,'2020-04-06 22:55:37.978668','2020-04-06 22:55:37.978688',6,1,4,'','Продукция',NULL,'/produkciya/',NULL,9,0,NULL,NULL,NULL,NULL),(24,NULL,'2020-04-06 22:55:41.655660','2020-04-06 22:55:41.655685',7,1,4,'','Информация',NULL,'/informaciya/',NULL,9,0,NULL,NULL,NULL,NULL),(25,NULL,'2020-04-06 22:55:45.896488','2020-04-06 22:55:45.896512',8,1,4,'_23','Услуги',NULL,'/produkciya/uslugi/',NULL,9,0,NULL,NULL,NULL,NULL),(26,NULL,'2020-04-06 22:55:49.462929','2020-04-06 22:55:49.462948',9,1,4,'_23','Продукты',NULL,'/produkciya/produkty/',NULL,9,0,NULL,NULL,NULL,NULL),(27,NULL,'2020-04-06 22:55:54.231949','2020-04-06 22:55:54.231970',10,1,4,'_23','Как заказать',NULL,'/produkciya/kak-zakazat/',NULL,9,0,NULL,NULL,NULL,NULL),(28,NULL,'2020-04-06 22:55:59.091937','2020-04-06 22:55:59.091957',11,1,4,'_24','Политика возврата',NULL,'/informaciya/politika-vozvrata/',NULL,9,0,NULL,NULL,NULL,NULL),(29,NULL,'2020-04-06 22:56:11.939273','2020-04-06 22:56:11.939293',12,1,4,'_24','Условия доставки',NULL,'/informaciya/usloviya-dostavki/',NULL,9,0,NULL,NULL,NULL,NULL),(30,NULL,'2020-04-06 22:56:14.942611','2020-04-06 22:56:14.942632',13,1,4,'_24','Скидки',NULL,'/informaciya/skidki/',NULL,9,0,NULL,NULL,NULL,NULL),(31,NULL,'2020-04-06 22:58:03.553327','2020-04-06 22:58:24.165519',14,1,1,'','Телефон','','','phone',1,0,'','','','8 (3952) 123-321<br>'),(32,NULL,'2020-04-06 22:58:07.850809','2020-04-06 22:58:42.943606',15,1,1,'','Адрес','','','address',1,0,'','','','г Иркутск ул Гоголя 54А<br>'),(33,NULL,'2020-04-06 22:58:13.463711','2020-04-06 22:58:46.891231',16,1,1,'','Сообщества','','','social',1,0,'','','',''),(34,NULL,'2020-04-06 22:58:51.118479','2020-04-06 22:59:06.422336',17,1,1,'_33','vk','','','vk',1,0,'','','',''),(35,NULL,'2020-04-06 22:58:55.897912','2020-04-06 22:59:14.464269',18,1,1,'_33','instagram','','','instagram',1,0,'','','',''),(36,NULL,'2020-04-06 22:59:00.185126','2020-04-06 22:59:17.623572',19,1,1,'_33','twitter','','','twitter',1,0,'','','',''),(37,NULL,'2020-04-06 22:59:03.601971','2020-04-06 22:59:20.852805',20,1,1,'_33','facebook','','','facebook',1,0,'','','',''),(38,NULL,'2020-04-06 23:03:16.213430','2020-04-06 23:03:39.795261',21,1,1,'','Копирайт','','','copyright',1,0,'','','','&copy; 2020 Все права защищены'),(39,'15.jpg','2020-04-06 23:04:54.026202','2020-04-06 23:04:54.026225',2,1,1,'','Подавление пыли','чистый воздух','','',10,0,'','','','Комплексные инженерные решения по подавлению пыли чистый воздух \"под ключ\"<br>'),(40,NULL,'2020-04-06 23:04:54.029915','2020-04-06 23:04:54.029936',1,1,1,'_39','Подробнее','','/','',10,0,'','','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
INSERT INTO `flatcontent_containers` VALUES (1,NULL,'2020-04-06 21:32:53.869774','2020-04-06 21:32:53.869796',1,1,2,'','Контент для всех страничек','','main',''),(2,NULL,'2020-04-06 21:49:48.278965','2020-04-06 22:33:20.807725',2,1,99,'','Слайдер','','slider',''),(4,NULL,'2020-04-06 22:23:35.938102','2020-04-06 22:24:58.529262',2,1,99,'','Слайдер (Вариант 2)','','slider2',''),(6,NULL,'2020-04-06 22:33:52.667962','2020-04-06 22:34:04.219108',2,1,99,'','Слайдер (Вариант 3)','','slider3',''),(7,NULL,'2020-04-06 22:39:28.021117','2020-04-06 22:39:35.472772',2,1,99,'','Слайдер (Вариант 4)','','slider4',''),(8,NULL,'2020-04-06 22:54:26.281916','2020-04-06 22:54:26.281942',3,1,1,'','Главное меню','','mainmenu',''),(9,NULL,'2020-04-06 22:55:26.537497','2020-04-06 22:55:26.537517',4,1,1,'','Нижнее меню','','bottommenu',''),(10,NULL,'2020-04-06 23:04:54.018072','2020-04-06 23:04:54.023910',5,1,3,'','Слайдер (Вариант 4)','','slider4','');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_linkcontainer`
--

LOCK TABLES `flatcontent_linkcontainer` WRITE;
/*!40000 ALTER TABLE `flatcontent_linkcontainer` DISABLE KEYS */;
INSERT INTO `flatcontent_linkcontainer` VALUES (1,NULL,'2020-04-06 23:05:28.829896','2020-04-06 23:05:28.829917',1,1,NULL,NULL,18,10);
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
  KEY `login_customuser_phone_d456dd09` (`phone`),
  KEY `login_customuser_img_6a17a9f3` (`img`),
  CONSTRAINT `login_customuser_user_id_70d7d409_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_customuser`
--

LOCK TABLES `login_customuser` WRITE;
/*!40000 ALTER TABLE `login_customuser` DISABLE KEYS */;
INSERT INTO `login_customuser` VALUES (1,NULL,'2020-04-06 21:16:30.715815','2020-04-06 21:17:43.233208',1,1,NULL,NULL,NULL,1),(2,NULL,'2020-04-06 23:06:39.930139','2020-04-06 23:06:40.167103',2,1,NULL,NULL,'',2);
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
  PRIMARY KEY (`id`),
  KEY `main_functions_config_name_923c9fba` (`name`),
  KEY `main_functions_config_attr_99aeb037` (`attr`),
  KEY `main_functions_config_value_463dd357` (`value`)
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
  `start` datetime(6) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
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

-- Dump completed on 2020-04-06 23:06:46
