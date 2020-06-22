-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 20, 2020 at 01:51 PM
-- Server version: 5.6.39-83.1
-- PHP Version: 5.6.40

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dsarhirus_porto`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can view permission', 1, 'view_permission'),
(5, 'Can add group', 2, 'add_group'),
(6, 'Can change group', 2, 'change_group'),
(7, 'Can delete group', 2, 'delete_group'),
(8, 'Can view group', 2, 'view_group'),
(9, 'Can add user', 3, 'add_user'),
(10, 'Can change user', 3, 'change_user'),
(11, 'Can delete user', 3, 'delete_user'),
(12, 'Can view user', 3, 'view_user'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add Админка - Настрока', 6, 'add_config'),
(22, 'Can change Админка - Настрока', 6, 'change_config'),
(23, 'Can delete Админка - Настрока', 6, 'delete_config'),
(24, 'Can view Админка - Настрока', 6, 'view_config'),
(25, 'Can add Админка - Задача', 7, 'add_tasks'),
(26, 'Can change Админка - Задача', 7, 'change_tasks'),
(27, 'Can delete Админка - Задача', 7, 'delete_tasks'),
(28, 'Can view Админка - Задача', 7, 'view_tasks'),
(29, 'Can add custom user', 8, 'add_customuser'),
(30, 'Can change custom user', 8, 'change_customuser'),
(31, 'Can delete custom user', 8, 'delete_customuser'),
(32, 'Can view custom user', 8, 'view_customuser'),
(33, 'Can add Стат.контет - Файлы', 9, 'add_files'),
(34, 'Can change Стат.контет - Файлы', 9, 'change_files'),
(35, 'Can delete Стат.контет - Файлы', 9, 'delete_files'),
(36, 'Can view Стат.контет - Файлы', 9, 'view_files'),
(37, 'Can add Стат.контент - Блоки', 10, 'add_blocks'),
(38, 'Can change Стат.контент - Блоки', 10, 'change_blocks'),
(39, 'Can delete Стат.контент - Блоки', 10, 'delete_blocks'),
(40, 'Can view Стат.контент - Блоки', 10, 'view_blocks'),
(41, 'Can add Стат.контент - Контейнеры', 11, 'add_containers'),
(42, 'Can change Стат.контент - Контейнеры', 11, 'change_containers'),
(43, 'Can delete Стат.контент - Контейнеры', 11, 'delete_containers'),
(44, 'Can view Стат.контент - Контейнеры', 11, 'view_containers'),
(45, 'Can add Стат.контент - Линковка меню к контейнерам', 12, 'add_linkcontainer'),
(46, 'Can change Стат.контент - Линковка меню к контейнерам', 12, 'change_linkcontainer'),
(47, 'Can delete Стат.контент - Линковка меню к контейнерам', 12, 'delete_linkcontainer'),
(48, 'Can view Стат.контент - Линковка меню к контейнерам', 12, 'view_linkcontainer'),
(49, 'Can add Товары - товар/услуга', 13, 'add_products'),
(50, 'Can change Товары - товар/услуга', 13, 'change_products'),
(51, 'Can delete Товары - товар/услуга', 13, 'delete_products'),
(52, 'Can view Товары - товар/услуга', 13, 'view_products'),
(53, 'Can add products cats', 14, 'add_productscats'),
(54, 'Can change products cats', 14, 'change_productscats'),
(55, 'Can delete products cats', 14, 'delete_productscats'),
(56, 'Can view products cats', 14, 'view_productscats'),
(57, 'Can add products photos', 15, 'add_productsphotos'),
(58, 'Can change products photos', 15, 'change_productsphotos'),
(59, 'Can delete products photos', 15, 'delete_productsphotos'),
(60, 'Can view products photos', 15, 'view_productsphotos'),
(61, 'Can add property', 16, 'add_property'),
(62, 'Can change property', 16, 'change_property'),
(63, 'Can delete property', 16, 'delete_property'),
(64, 'Can view property', 16, 'view_property'),
(65, 'Can add properties values', 17, 'add_propertiesvalues'),
(66, 'Can change properties values', 17, 'change_propertiesvalues'),
(67, 'Can delete properties values', 17, 'delete_propertiesvalues'),
(68, 'Can view properties values', 17, 'view_propertiesvalues'),
(69, 'Can add products properties', 18, 'add_productsproperties'),
(70, 'Can change products properties', 18, 'change_productsproperties'),
(71, 'Can delete products properties', 18, 'delete_productsproperties'),
(72, 'Can view products properties', 18, 'view_productsproperties'),
(73, 'Can add Пользователи - пользователь', 19, 'add_shopper'),
(74, 'Can change Пользователи - пользователь', 19, 'change_shopper'),
(75, 'Can delete Пользователи - пользователь', 19, 'delete_shopper'),
(76, 'Can view Пользователи - пользователь', 19, 'view_shopper'),
(77, 'Can add Магазин - Заказ', 20, 'add_orders'),
(78, 'Can change Магазин - Заказ', 20, 'change_orders'),
(79, 'Can delete Магазин - Заказ', 20, 'delete_orders'),
(80, 'Can view Магазин - Заказ', 20, 'view_orders'),
(81, 'Can add wish list', 21, 'add_wishlist'),
(82, 'Can change wish list', 21, 'change_wishlist'),
(83, 'Can delete wish list', 21, 'delete_wishlist'),
(84, 'Can view wish list', 21, 'view_wishlist'),
(85, 'Can add purchases', 22, 'add_purchases'),
(86, 'Can change purchases', 22, 'change_purchases'),
(87, 'Can delete purchases', 22, 'delete_purchases'),
(88, 'Can view purchases', 22, 'view_purchases');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
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

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$150000$2DYMxwp5mzTd$9bUU4LXCPZJIa0BuUWIn7QxaOMSHOBrRF9gu9MJFq8w=', '2020-06-20 14:03:58.764602', 1, 'jocker', '', '', 'dkramorov@mail.ru', 1, 1, '2020-06-20 12:06:44.330715'),
(2, 'pbkdf2_sha256$100000$lp4j7taES6yW$c3zQgT0d1plG3b4q3tGa16oyQie+BuIJPhQJ/jliguY=', '2020-06-20 14:45:13.062155', 1, 'seva', '', '', '', 1, 1, '2020-06-20 14:03:40.293730'),
(3, 'pbkdf2_sha256$100000$AFntK9t2PE12$eZ1JG7HcaS482r26RpX7NkVhbUo0jB9vQU+ZvM2jkFI=', '2020-06-20 15:36:14.030744', 0, 'manager', '', '', '', 0, 1, '2020-06-20 14:43:04.917842');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `auth_user_user_permissions`
--

INSERT INTO `auth_user_user_permissions` (`id`, `user_id`, `permission_id`) VALUES
(1, 3, 49),
(2, 3, 50),
(3, 3, 51),
(4, 3, 52);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(2, 'auth', 'group'),
(1, 'auth', 'permission'),
(3, 'auth', 'user'),
(4, 'contenttypes', 'contenttype'),
(9, 'files', 'files'),
(10, 'flatcontent', 'blocks'),
(11, 'flatcontent', 'containers'),
(12, 'flatcontent', 'linkcontainer'),
(8, 'login', 'customuser'),
(6, 'main_functions', 'config'),
(7, 'main_functions', 'tasks'),
(19, 'personal', 'shopper'),
(13, 'products', 'products'),
(14, 'products', 'productscats'),
(15, 'products', 'productsphotos'),
(18, 'products', 'productsproperties'),
(17, 'products', 'propertiesvalues'),
(16, 'products', 'property'),
(5, 'sessions', 'session'),
(20, 'shop', 'orders'),
(22, 'shop', 'purchases'),
(21, 'shop', 'wishlist');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2020-06-20 12:06:43.147563'),
(2, 'contenttypes', '0002_remove_content_type_name', '2020-06-20 12:06:43.168574'),
(3, 'auth', '0001_initial', '2020-06-20 12:06:43.372780'),
(4, 'auth', '0002_alter_permission_name_max_length', '2020-06-20 12:06:43.466376'),
(5, 'auth', '0003_alter_user_email_max_length', '2020-06-20 12:06:43.486892'),
(6, 'auth', '0004_alter_user_username_opts', '2020-06-20 12:06:43.504289'),
(7, 'auth', '0005_alter_user_last_login_null', '2020-06-20 12:06:43.519403'),
(8, 'auth', '0006_require_contenttypes_0002', '2020-06-20 12:06:43.520500'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2020-06-20 12:06:43.536828'),
(10, 'auth', '0008_alter_user_username_max_length', '2020-06-20 12:06:43.557206'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2020-06-20 12:06:43.573591'),
(12, 'auth', '0010_alter_group_name_max_length', '2020-06-20 12:06:43.590133'),
(13, 'auth', '0011_update_proxy_permissions', '2020-06-20 12:06:43.600980'),
(14, 'files', '0001_initial', '2020-06-20 12:06:43.642114'),
(15, 'files', '0002_auto_20191203_2054', '2020-06-20 12:06:43.688524'),
(16, 'files', '0003_auto_20200112_1717', '2020-06-20 12:06:43.696714'),
(17, 'files', '0004_auto_20200402_2127', '2020-06-20 12:06:43.711054'),
(18, 'flatcontent', '0001_initial', '2020-06-20 12:06:43.848321'),
(19, 'flatcontent', '0002_auto_20190825_1730', '2020-06-20 12:06:44.077036'),
(20, 'flatcontent', '0003_auto_20191203_2054', '2020-06-20 12:06:44.109869'),
(21, 'flatcontent', '0004_blocks_html', '2020-06-20 12:06:44.129110'),
(22, 'flatcontent', '0005_auto_20200112_1717', '2020-06-20 12:06:44.160517'),
(23, 'flatcontent', '0006_auto_20200314_1638', '2020-06-20 12:06:44.167155'),
(24, 'flatcontent', '0007_auto_20200402_2127', '2020-06-20 12:06:44.234834'),
(25, 'flatcontent', '0008_containers_class_name', '2020-06-20 12:06:44.276547'),
(26, 'login', '0001_initial', '2020-06-20 12:06:44.525542'),
(27, 'main_functions', '0001_initial', '2020-06-20 12:06:44.872179'),
(28, 'main_functions', '0002_auto_20191203_2052', '2020-06-20 12:06:44.890765'),
(29, 'main_functions', '0003_auto_20200407_1845', '2020-06-20 12:06:45.096637'),
(30, 'personal', '0001_initial', '2020-06-20 12:06:45.337244'),
(31, 'personal', '0002_auto_20200528_1642', '2020-06-20 12:06:45.492085'),
(32, 'personal', '0003_auto_20200616_1707', '2020-06-20 12:06:45.503294'),
(33, 'personal', '0004_shopper_ip', '2020-06-20 12:06:45.523353'),
(34, 'products', '0001_initial', '2020-06-20 12:06:45.746862'),
(35, 'products', '0002_productsphotos', '2020-06-20 12:06:45.941306'),
(36, 'products', '0003_auto_20200315_2217', '2020-06-20 12:06:46.049035'),
(37, 'products', '0004_auto_20200316_2329', '2020-06-20 12:06:46.104796'),
(38, 'products', '0005_auto_20200402_2127', '2020-06-20 12:06:46.455792'),
(39, 'products', '0006_auto_20200402_2351', '2020-06-20 12:06:46.602764'),
(40, 'products', '0007_property_ptype', '2020-06-20 12:06:46.624198'),
(41, 'products', '0008_property_code', '2020-06-20 12:06:46.653535'),
(42, 'products', '0009_property_measure', '2020-06-20 12:06:46.676008'),
(43, 'sessions', '0001_initial', '2020-06-20 12:06:46.806449'),
(44, 'shop', '0001_initial', '2020-06-20 12:06:47.263202'),
(45, 'shop', '0002_auto_20200618_0000', '2020-06-20 12:06:47.557061');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('39lxbf276pav27up5ekcpabahb723gbp', 'NmQ5NmEyMDYwNGQxMGM4ZTVmMjFiMWYyZGY4YTkyN2I1NGE4MDBmNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjhlYmI0Nzc3YTRmNzZkZTYzMGYxOTNkMTI0NTY3ZDMwYmMyNDJiNTAifQ==', '2020-07-04 14:03:58.768360'),
('6118t66lo3b37frymedebck6pmgq6zss', 'MWZhNjFhYzJjNmYyZThkNzcwZjk5N2ZjYzAxNmZmNzc4YjY4NTE3Nzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImFwcHMubG9naW4uYmFja2VuZC5NeUJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1YWM4ODE3ZjgxOGZlNTIxZjBlZTRmNzI4ZGRlYWNkZTg4NDUwMjZkIiwiX2F1dGhfdXNlcl9pZCI6IjIifQ==', '2020-07-04 14:23:26.088128'),
('7w86k2c60pl472nf2nd2fv5v4s6ny2xj', 'NDFiYWI3ODA3ZTVhNzFkNDkwMWY0YjdjMDQxN2E1NzQ4ZTljNzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjVhYzg4MTdmODE4ZmU1MjFmMGVlNGY3MjhkZGVhY2RlODg0NTAyNmQifQ==', '2020-07-04 14:45:13.084619'),
('cwuf2ujyu01ywzs2ayiknb2iuttbzv9b', 'OTVhYjExNWI3ZTI2M2Q2MmZmYWMwYzc5MTI1MTE5NzI2MjZlN2I2Nzp7Il9hdXRoX3VzZXJfaGFzaCI6ImRkODFlYTM0YjQ3OTg0YzkxMzA2OWMyNzA2MWEyZjg5NzM2NTZhODMiLCJfYXV0aF91c2VyX2lkIjoiMyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFwcHMubG9naW4uYmFja2VuZC5NeUJhY2tlbmQifQ==', '2020-07-04 15:36:14.051993');

-- --------------------------------------------------------

--
-- Table structure for table `files_files`
--

DROP TABLE IF EXISTS `files_files`;
CREATE TABLE IF NOT EXISTS `files_files` (
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

-- --------------------------------------------------------

--
-- Table structure for table `flatcontent_blocks`
--

DROP TABLE IF EXISTS `flatcontent_blocks`;
CREATE TABLE IF NOT EXISTS `flatcontent_blocks` (
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
  KEY `flatcontent_blocks_img_876dc659` (`img`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `flatcontent_blocks`
--

INSERT INTO `flatcontent_blocks` (`id`, `img`, `created`, `updated`, `position`, `is_active`, `state`, `parents`, `name`, `description`, `link`, `tag`, `container_id`, `blank`, `icon`, `keywords`, `title`, `html`) VALUES
(1, '1.png', '2020-06-20 12:13:05.699885', '2020-06-20 12:13:05.699911', 1, 1, 3, '', 'Логотип', 'Добро пожаловать, на наш сайт', '/', 'logo', 1, 0, NULL, NULL, NULL, NULL),
(2, NULL, '2020-06-20 12:13:05.708738', '2020-06-20 12:13:05.708808', 2, 1, 3, '', 'Телефон', NULL, 'tel:73952123321', 'phone', 1, 0, NULL, NULL, NULL, '+7(3952) 123-321'),
(3, NULL, '2020-06-20 12:13:05.717357', '2020-06-20 12:13:05.717379', 3, 1, 3, '', 'Адрес', NULL, NULL, 'address', 1, 0, NULL, NULL, NULL, 'г. Иркутск ул. Советская 32а офис 5'),
(4, NULL, '2020-06-20 12:13:05.734443', '2020-06-20 12:13:05.734491', 4, 1, 3, '', 'Email', NULL, NULL, 'email', 1, 0, NULL, NULL, NULL, 'test@test.ru'),
(5, NULL, '2020-06-20 12:13:05.737375', '2020-06-20 12:13:05.737398', 5, 1, 3, '', 'Режим работы', NULL, NULL, 'worktime', 1, 0, NULL, NULL, NULL, 'пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 17:00'),
(6, NULL, '2020-06-20 12:13:05.740308', '2020-06-20 12:13:05.740333', 6, 1, 3, '', 'Copyright', NULL, NULL, 'copyright', 1, 0, NULL, NULL, NULL, '<p>&copy; 2020 Все права защищены</p>'),
(7, NULL, '2020-06-20 12:13:05.743475', '2020-06-20 12:13:05.743502', 7, 1, 3, '', 'Сообщества', NULL, NULL, 'social', 1, 0, NULL, NULL, NULL, NULL),
(8, NULL, '2020-06-20 12:13:05.746519', '2020-06-20 12:13:05.746542', 8, 1, 3, '_7', 'instagram', NULL, NULL, 'instagram', 1, 1, 'instagram', NULL, NULL, NULL),
(10, NULL, '2020-06-20 12:13:05.752129', '2020-06-20 12:13:05.752150', 10, 1, 3, '_7', 'facebook', NULL, NULL, 'facebook', 1, 1, 'facebook', NULL, NULL, NULL),
(11, NULL, '2020-06-20 12:13:05.755361', '2020-06-20 12:13:05.755388', 11, 1, 3, '_7', 'twitter', NULL, NULL, 'twitter', 1, 1, 'twitter', NULL, NULL, NULL),
(12, NULL, '2020-06-20 12:13:05.763255', '2020-06-20 13:01:53.026875', 12, 1, 4, '', 'Главная', '', '/', '_mainmenu_mainpage', 2, 0, '', '', '', ''),
(13, NULL, '2020-06-20 12:13:05.765808', '2020-06-20 12:13:05.765827', 13, 1, 4, '', 'Каталог', NULL, '/cat/', '_mainmenu_catpage', 2, 0, NULL, NULL, NULL, NULL),
(14, NULL, '2020-06-20 12:13:05.769317', '2020-06-20 12:13:05.769338', 14, 1, 4, '_13', 'Популярные товары', NULL, '/cat/populyarnye-tovary/', '_mainmenu_catpage_popular', 2, 0, NULL, NULL, NULL, NULL),
(15, NULL, '2020-06-20 12:13:05.772660', '2020-06-20 12:13:05.772679', 15, 1, 4, '_13', 'Новые товары', NULL, '/cat/novye-tovary/', '_mainmenu_catpage_new', 2, 0, NULL, NULL, NULL, NULL),
(16, NULL, '2020-06-20 12:13:05.776414', '2020-06-20 12:13:05.776439', 16, 1, 4, '_13', 'Товары со скидкой', NULL, '/cat/tovary-so-skidkoy/', '_mainmenu_catpage_discount', 2, 0, NULL, NULL, NULL, NULL),
(17, NULL, '2020-06-20 12:13:05.780411', '2020-06-20 12:13:05.780439', 17, 1, 4, '_13', 'Распродажа', NULL, '/cat/rasprodaja/', '_mainmenu_catpage_sale', 2, 0, NULL, NULL, NULL, NULL),
(18, NULL, '2020-06-20 12:13:05.783299', '2020-06-20 18:46:16.144800', 18, 1, 4, '', 'О нас', '', '/about/', '_mainmenu_aboutpage', 2, 0, '', '', '', ''),
(19, NULL, '2020-06-20 12:13:05.786236', '2020-06-20 12:13:05.786260', 19, 1, 4, '', 'Услуги', NULL, '/services/', '_mainmenu_servicespage', 2, 0, NULL, NULL, NULL, NULL),
(20, NULL, '2020-06-20 12:13:05.789082', '2020-06-20 12:13:05.789104', 20, 1, 4, '', 'Контакты', NULL, '/feedback/', '_mainmenu_feedbackpage', 2, 0, NULL, NULL, NULL, NULL),
(21, NULL, '2020-06-20 12:13:05.792450', '2020-06-20 12:13:05.792477', 21, 1, 4, '', 'Каталог', NULL, '/cat/', '_bottommenu_catpage', 3, 0, NULL, NULL, NULL, NULL),
(22, NULL, '2020-06-20 12:13:05.795995', '2020-06-20 12:13:05.796016', 22, 1, 4, '_21', 'Популярные товары', NULL, '/cat/populyarnye-tovary/', '_bottommenu_catpage_popular', 3, 0, NULL, NULL, NULL, NULL),
(23, NULL, '2020-06-20 12:13:05.799333', '2020-06-20 12:13:05.799352', 23, 1, 4, '_21', 'Новые товары', NULL, '/cat/novye-tovary/', '_bottommenu_catpage_new', 3, 0, NULL, NULL, NULL, NULL),
(24, NULL, '2020-06-20 12:13:05.802791', '2020-06-20 12:13:05.802810', 24, 1, 4, '_21', 'Товары со скидкой', NULL, '/cat/tovary-so-skidkoy/', '_bottommenu_catpage_discount', 3, 0, NULL, NULL, NULL, NULL),
(25, NULL, '2020-06-20 12:13:05.806270', '2020-06-20 12:13:05.806290', 25, 1, 4, '_21', 'Распродажа', NULL, '/cat/rasprodaja/', '_bottommenu_catpage_sale', 3, 0, NULL, NULL, NULL, NULL),
(26, NULL, '2020-06-20 12:13:05.809822', '2020-06-20 12:13:05.809861', 26, 1, 4, '', 'О нас', NULL, '/about/', '_bottommenu_aboutpage', 3, 0, NULL, NULL, NULL, NULL),
(27, NULL, '2020-06-20 12:13:05.813356', '2020-06-20 12:13:05.813382', 27, 1, 4, '', 'Услуги', NULL, '/services/', '_bottommenu_servicespage', 3, 0, NULL, NULL, NULL, NULL),
(28, NULL, '2020-06-20 12:13:05.816504', '2020-06-20 12:13:05.816535', 28, 1, 4, '', 'Контакты', NULL, '/feedback/', '_bottommenu_feedbackpage', 3, 0, NULL, NULL, NULL, NULL),
(29, '29.png', '2020-06-20 12:41:09.518989', '2020-06-20 12:43:41.584406', 29, 1, 1, '', 'Предложение для вас', 'Вы останетесь довольны', '', '', 4, 0, '', '', '', 'Мы подготовили предложение специально для вас<br>'),
(30, '30.png', '2020-06-20 12:41:59.938071', '2020-06-20 12:47:09.399373', 30, 1, 1, '', 'Это то, что вам нужно', 'Мы знаем!', '', '', 4, 0, '', '', '', 'Не знаете, что делать?<br>'),
(31, '29.png', '2020-06-20 13:01:35.706158', '2020-06-20 13:01:35.706183', 29, 1, 1, '', 'Предложение для вас', 'Вы останетесь довольны', '', '', 5, 0, '', '', '', 'Мы подготовили предложение специально для вас<br>'),
(32, '30.png', '2020-06-20 13:01:35.779967', '2020-06-20 13:01:35.779996', 30, 1, 1, '', 'Это то, что вам нужно', 'Мы знаем!', '', '', 5, 0, '', '', '', 'Не знаете, что делать?<br>'),
(33, NULL, '2020-06-20 13:21:45.997008', '2020-06-20 13:24:06.614879', 31, 1, 1, '', 'Преимущества (footer)', '', '', 'advantages', 1, 0, '', '', '', ''),
(34, NULL, '2020-06-20 13:21:51.078984', '2020-06-20 13:22:37.290411', 2, 1, 1, '_33', 'Гарантия возврата', '', '', '', 1, 0, '', '', '', 'Мы вернем вам деньги если продукция вас не устроит<br>'),
(35, NULL, '2020-06-20 13:22:54.442913', '2020-06-20 13:23:16.475476', 1, 1, 1, '_33', 'Быстрая доставка', '', '', '', 1, 0, '', '', '', 'Мы сделаем все, чтобы вы получили товар быстро<br>'),
(36, NULL, '2020-06-20 13:23:23.107789', '2020-06-20 13:23:47.888639', 32, 1, 1, '_33', 'Поддержка', '', '', '', 1, 0, '', '', '', 'Мы ответим на любые вопросы по нашей продукции<br>'),
(37, NULL, '2020-06-20 13:52:55.782543', '2020-06-20 13:52:55.782567', 33, 1, 4, '_26', 'О компании', NULL, '/about/o-kompanii/', NULL, 3, 0, NULL, NULL, NULL, NULL),
(38, NULL, '2020-06-20 13:52:59.840428', '2020-06-20 13:52:59.840448', 34, 1, 4, '_26', 'Реквизиты', NULL, '/about/rekvizity/', NULL, 3, 0, NULL, NULL, NULL, NULL),
(39, NULL, '2020-06-20 13:53:05.087903', '2020-06-20 13:53:05.087927', 35, 1, 4, '_27', 'Доставка', NULL, '/services/dostavka/', NULL, 3, 0, NULL, NULL, NULL, NULL),
(40, NULL, '2020-06-20 13:53:11.827855', '2020-06-20 13:53:11.827877', 36, 1, 4, '_27', 'Поддержка', NULL, '/services/podderjka/', NULL, 3, 0, NULL, NULL, NULL, NULL),
(41, NULL, '2020-06-20 13:53:15.408408', '2020-06-20 13:53:15.408429', 37, 1, 4, '_27', 'Заказ', NULL, '/services/zakaz/', NULL, 3, 0, NULL, NULL, NULL, NULL),
(42, NULL, '2020-06-20 13:53:18.784756', '2020-06-20 13:53:18.784780', 38, 1, 4, '_28', 'Карта', NULL, '/feedback/karta/', NULL, 3, 0, NULL, NULL, NULL, NULL),
(43, NULL, '2020-06-20 13:53:23.024069', '2020-06-20 13:53:23.024089', 39, 1, 4, '_28', 'Обратная связь', NULL, '/feedback/obratnaya-svyaz/', NULL, 3, 0, NULL, NULL, NULL, NULL),
(44, NULL, '2020-06-20 17:15:07.370711', '2020-06-20 17:15:07.370747', 40, 1, 1, '', 'Рубрика 1', NULL, NULL, NULL, 6, 0, NULL, NULL, NULL, NULL),
(45, '45.png', '2020-06-20 17:16:47.637939', '2020-06-20 17:17:07.328856', 41, 1, 1, '', 'Рассказ обо мне', '', '', '', 7, 0, '', '', '', '<p>Психолог, гипнолог, член профессиональной психотерапевтической лиги, \r\nаккредитована по 12 программам психодкоррекции и психотерапии, \r\nтетахилер, специалист по квантовому смещению, Ййя Ориша (не пугайтесь, \r\nпо африкански это жрица)</p><p>Я обучалась у жрецов в Нигерии, Индии, \r\nИндонезии, на Кубе, во Вьетнаме и других странах. Мне было невероятно \r\nинетресно увидеть, как рождается этническая магия.</p>\r\n'),
(46, '45.png', '2020-06-20 17:17:33.124399', '2020-06-20 17:17:33.124422', 41, 1, 1, '', 'Рассказ обо мне', '', '', '', 8, 0, '', '', '', '<p>Психолог, гипнолог, член профессиональной психотерапевтической лиги, \r\nаккредитована по 12 программам психодкоррекции и психотерапии, \r\nтетахилер, специалист по квантовому смещению, Ййя Ориша (не пугайтесь, \r\nпо африкански это жрица)</p><p>Я обучалась у жрецов в Нигерии, Индии, \r\nИндонезии, на Кубе, во Вьетнаме и других странах. Мне было невероятно \r\nинетресно увидеть, как рождается этническая магия.</p>\r\n'),
(47, 'member-1.jpg', '2020-06-20 17:19:04.705470', '2020-06-20 17:20:17.543981', 42, 1, 1, '', 'Специалист 1', '', '', '', 9, 0, '', '', '', ''),
(48, 'member-2.jpg', '2020-06-20 17:19:08.940942', '2020-06-20 17:20:25.380858', 43, 1, 1, '', 'Специалист 2', '', '', '', 9, 0, '', '', '', ''),
(49, 'member-3.jpg', '2020-06-20 17:19:13.726262', '2020-06-20 17:20:31.399931', 44, 1, 1, '', 'Специалист 3', '', '', '', 9, 0, '', '', '', ''),
(50, 'member-4.jpg', '2020-06-20 17:19:20.096983', '2020-06-20 17:20:37.499623', 45, 1, 1, '', 'Специалист 4', '', '', '', 9, 0, '', '', '', ''),
(51, 'member-5.jpg', '2020-06-20 17:19:24.152863', '2020-06-20 17:20:43.305247', 46, 1, 1, '', 'Специалист 5', '', '', '', 9, 0, '', '', '', ''),
(52, 'member-6.jpg', '2020-06-20 17:20:03.761118', '2020-06-20 17:20:49.036623', 47, 1, 1, '', 'Специалист 6', '', '', '', 9, 0, '', '', '', ''),
(53, '53.png', '2020-06-20 17:26:38.980778', '2020-06-20 17:27:27.864208', 48, 1, 1, '', 'Поддержка', '', '', '', 10, 0, '', '', '', 'Мы всегда готовы ответить на любые ваши вопросы<br>'),
(54, '54.png', '2020-06-20 17:26:55.551560', '2020-06-20 17:27:40.862693', 49, 1, 1, '', 'Быстрая доставка', '', '', '', 10, 0, '', '', '', 'Вы получите товар максимально быстро<br>'),
(55, '55.png', '2020-06-20 17:27:02.603402', '2020-06-20 17:27:56.807027', 50, 1, 1, '', 'Гарантия возврата', '', '', '', 10, 0, '', '', '', 'Вернем деньги, если вы не получите должного результата<br>'),
(56, '56.png', '2020-06-20 17:27:13.432921', '2020-06-20 17:28:21.583409', 51, 1, 1, '', 'Инновации', '', '', '', 10, 0, '', '', '', 'Мы работаем самыми передовыми методами<br>'),
(57, '45.png', '2020-06-20 18:37:41.894184', '2020-06-20 18:37:41.894221', 41, 1, 1, '', 'Рассказ обо мне', '', '', '', 11, 0, '', '', '', '<p>Психолог, гипнолог, член профессиональной психотерапевтической лиги, \r\nаккредитована по 12 программам психодкоррекции и психотерапии, \r\nтетахилер, специалист по квантовому смещению, Ййя Ориша (не пугайтесь, \r\nпо африкански это жрица)</p><p>Я обучалась у жрецов в Нигерии, Индии, \r\nИндонезии, на Кубе, во Вьетнаме и других странах. Мне было невероятно \r\nинетресно увидеть, как рождается этническая магия.</p>\r\n'),
(58, '45.png', '2020-06-20 18:39:17.421357', '2020-06-20 18:39:17.421380', 41, 1, 1, '', 'Рассказ обо мне', '', '', '', 12, 0, '', '', '', '<p>Психолог, гипнолог, член профессиональной психотерапевтической лиги, \r\nаккредитована по 12 программам психодкоррекции и психотерапии, \r\nтетахилер, специалист по квантовому смещению, Ййя Ориша (не пугайтесь, \r\nпо африкански это жрица)</p><p>Я обучалась у жрецов в Нигерии, Индии, \r\nИндонезии, на Кубе, во Вьетнаме и других странах. Мне было невероятно \r\nинетресно увидеть, как рождается этническая магия.</p>\r\n'),
(59, '53.png', '2020-06-20 18:40:02.296228', '2020-06-20 18:40:02.296255', 48, 1, 1, '', 'Поддержка', '', '', '', 13, 0, '', '', '', 'Мы всегда готовы ответить на любые ваши вопросы<br>'),
(60, '54.png', '2020-06-20 18:40:02.305894', '2020-06-20 18:40:02.305923', 49, 1, 1, '', 'Быстрая доставка', '', '', '', 13, 0, '', '', '', 'Вы получите товар максимально быстро<br>'),
(61, '55.png', '2020-06-20 18:40:02.308158', '2020-06-20 18:40:02.308180', 50, 1, 1, '', 'Гарантия возврата', '', '', '', 13, 0, '', '', '', 'Вернем деньги, если вы не получите должного результата<br>'),
(62, '56.png', '2020-06-20 18:40:02.310132', '2020-06-20 18:40:02.310153', 51, 1, 1, '', 'Инновации', '', '', '', 13, 0, '', '', '', 'Мы работаем самыми передовыми методами<br>'),
(63, '63.png', '2020-06-20 18:41:23.783187', '2020-06-20 18:44:58.433129', 29, 1, 1, '', '.', '', '', '', 14, 0, '', '', '', '<br>\r\n');

-- --------------------------------------------------------

--
-- Table structure for table `flatcontent_containers`
--

DROP TABLE IF EXISTS `flatcontent_containers`;
CREATE TABLE IF NOT EXISTS `flatcontent_containers` (
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `flatcontent_containers`
--

INSERT INTO `flatcontent_containers` (`id`, `img`, `created`, `updated`, `position`, `is_active`, `state`, `parents`, `name`, `description`, `tag`, `template_position`, `class_name`) VALUES
(1, NULL, '2020-06-20 12:13:05.690360', '2020-06-20 12:13:05.690392', 1, 1, 2, NULL, 'Контент для всех страничек', 'Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики', 'main', NULL, NULL),
(2, NULL, '2020-06-20 12:13:05.758303', '2020-06-20 12:13:05.758329', 2, 1, 1, NULL, 'Главное меню', 'Создано автоматически, выводит главное меню', 'mainmenu', NULL, NULL),
(3, NULL, '2020-06-20 12:13:05.760686', '2020-06-20 12:13:05.760707', 3, 1, 1, NULL, 'Нижнее меню', 'Создано автоматически, выводит нижнее меню', 'bottommenu', NULL, NULL),
(4, '4.png', '2020-06-20 12:39:21.780619', '2020-06-20 12:40:55.758471', 4, 1, 99, '', 'Слайдер', '', 'slider', '', ''),
(5, '4.png', '2020-06-20 13:01:35.627306', '2020-06-20 13:01:35.694854', 5, 1, 3, '', 'Слайдер', '', 'slider', '', ''),
(6, NULL, '2020-06-20 17:01:13.537685', '2020-06-20 17:01:13.537724', 6, 1, 7, NULL, 'Каталог товаров', NULL, 'catalogue', NULL, NULL),
(7, NULL, '2020-06-20 17:16:23.371809', '2020-06-20 17:16:23.371841', 7, 1, 99, '', 'Статья', '', 'article', '', ''),
(8, '8.png', '2020-06-20 17:17:33.115431', '2020-06-20 17:17:43.001895', 7, 1, 99, '', 'Статья (Вариант 2)', '', 'article2', '', ''),
(9, NULL, '2020-06-20 17:18:52.080435', '2020-06-20 17:18:52.080466', 8, 1, 99, '', 'Наша команда', 'С нами лучшие специалисты в своей области<br>', '', '', ''),
(10, NULL, '2020-06-20 17:26:05.647712', '2020-06-20 17:26:05.647738', 9, 1, 99, '', 'Преимущества', '', 'advantages', '', ''),
(11, NULL, '2020-06-20 18:37:41.880436', '2020-06-20 18:38:56.714232', 10, 1, 3, '', 'Рассказ обо мне', '', 'article', '', ''),
(12, '12.png', '2020-06-20 18:39:17.404159', '2020-06-20 18:49:41.561796', 11, 1, 3, '', 'Статья 2', '', 'article2', '', ''),
(13, NULL, '2020-06-20 18:40:02.284999', '2020-06-20 18:40:02.285034', 12, 1, 3, '', 'Преимущества', '', 'advantages', '', ''),
(14, NULL, '2020-06-20 18:41:23.765821', '2020-06-20 18:47:52.189869', 13, 1, 3, '', 'Слайдер о нас', '', 'slider', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `flatcontent_linkcontainer`
--

DROP TABLE IF EXISTS `flatcontent_linkcontainer`;
CREATE TABLE IF NOT EXISTS `flatcontent_linkcontainer` (
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
  KEY `flatcontent_linkcontainer_img_2d8c4e0a` (`img`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `flatcontent_linkcontainer`
--

INSERT INTO `flatcontent_linkcontainer` (`id`, `img`, `created`, `updated`, `position`, `is_active`, `state`, `parents`, `block_id`, `container_id`) VALUES
(1, NULL, '2020-06-20 13:01:53.033095', '2020-06-20 13:01:53.033115', 1, 1, NULL, NULL, 12, 5),
(11, NULL, '2020-06-20 18:46:16.152652', '2020-06-20 18:46:16.152706', 2, 1, NULL, NULL, 18, 14),
(12, NULL, '2020-06-20 18:46:16.154388', '2020-06-20 18:46:16.154409', 3, 1, NULL, NULL, 18, 11),
(13, NULL, '2020-06-20 18:46:16.155901', '2020-06-20 18:46:16.155922', 4, 1, NULL, NULL, 18, 12),
(14, NULL, '2020-06-20 18:46:16.157339', '2020-06-20 18:46:16.157361', 5, 1, NULL, NULL, 18, 13);

-- --------------------------------------------------------

--
-- Table structure for table `login_customuser`
--

DROP TABLE IF EXISTS `login_customuser`;
CREATE TABLE IF NOT EXISTS `login_customuser` (
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
  KEY `login_customuser_phone_d456dd09` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `login_customuser`
--

INSERT INTO `login_customuser` (`id`, `img`, `created`, `updated`, `position`, `is_active`, `state`, `parents`, `phone`, `user_id`) VALUES
(1, NULL, '2020-06-20 12:06:44.507497', '2020-06-20 14:03:58.766885', 1, 1, NULL, NULL, NULL, 1),
(2, NULL, '2020-06-20 14:03:40.298217', '2020-06-20 14:45:13.065541', 2, 1, NULL, NULL, '', 2),
(3, NULL, '2020-06-20 14:43:04.922959', '2020-06-20 15:36:14.034801', 3, 1, NULL, NULL, '', 3);

-- --------------------------------------------------------

--
-- Table structure for table `main_functions_config`
--

DROP TABLE IF EXISTS `main_functions_config`;
CREATE TABLE IF NOT EXISTS `main_functions_config` (
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

-- --------------------------------------------------------

--
-- Table structure for table `main_functions_tasks`
--

DROP TABLE IF EXISTS `main_functions_tasks`;
CREATE TABLE IF NOT EXISTS `main_functions_tasks` (
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

-- --------------------------------------------------------

--
-- Table structure for table `personal_shopper`
--

DROP TABLE IF EXISTS `personal_shopper`;
CREATE TABLE IF NOT EXISTS `personal_shopper` (
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

-- --------------------------------------------------------

--
-- Table structure for table `products_products`
--

DROP TABLE IF EXISTS `products_products`;
CREATE TABLE IF NOT EXISTS `products_products` (
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `products_products`
--

INSERT INTO `products_products` (`id`, `img`, `created`, `updated`, `position`, `is_active`, `state`, `parents`, `name`, `altname`, `manufacturer`, `measure`, `currency`, `old_price`, `price`, `dj_info`, `mini_info`, `info`, `code`, `count`) VALUES
(2, '2.png', '2020-06-20 14:38:47.548355', '2020-06-20 16:30:24.049502', 2, 1, NULL, '', 'Родонит', '', '', 'шт.', NULL, NULL, '4300.00', '', 'Для материальных благ и накопительства, укрепление семьи', 'Камень является магнитом для материальных благ и накопительства. Защищает от краж и финансовых потерь. Придает уверенности в себе и избавляет от лени.<br>\r\nПожалуй самый семейный камень - помогает сохранить и укрепить семью, брак. Одиноким встретить свою вторую половину.<br>\r\nПомогает зачать ребенка. Кельтский узор защищает семью владельца камня.', '', NULL),
(3, '3.jpg', '2020-06-20 15:50:23.197570', '2020-06-20 15:50:59.333995', 3, 1, NULL, '', 'Авантюрин красный', '', '', 'шт', NULL, NULL, '4500.00', '', '', '<div>Отлично подойдет людям скованным, которые боятся проявлять эмоции.</div><div>Тем, у кого все по полочкам и по расписанию - камень придаст легкость восприятия и свежие эмоции. Камень очень обостряет интуицию, считается, что притягивает удачу. Камень выделяет своего владельца среди прочих, придает легкость в общении , кокетство. Противоположный пол воспринимает владельца камней как блестящую вкусность - сильнейший любовный талисман. Камень способен буквально вырвать из лап депрессии и привнести в жизнь красок. Отличный помощник в делах, связанных с торговлей и ценными бумагами. Камень - воронка для новых положительных эмоций, возможностей и перспектив. <br><br>Противопоказан неуравновешенным и азартным людям.</div>', '', NULL),
(4, '4.jpg', '2020-06-20 16:01:44.315706', '2020-06-20 16:02:31.870779', 4, 1, NULL, '', 'Авантюрин синий', '', '', 'шт', NULL, NULL, '4500.00', '', '', 'Камень - природный щит, отводит любую физическую опасность от владельца, начиная от случайной драки и заканчивая авиакатастрофой. Делает человека сфокусированным и обостряет внимание. Издревле считается камнем магов - помогает легко входить в нужное состояние и транслировать его людям. Обращает внимание на своего хозяина так, что люди начинают к нему прислушиваться. Сильно обостряет скрытые способности, дарует виденье. Камень помогает при лечении заболеваний кожи, волос, дыхательных путей. Способствует очищению крови, придает организму силу и бодрость духа.<br><br>Противопоказан людям с растройством психики.', '', NULL),
(5, '5.jpg', '2020-06-20 16:03:55.973289', '2020-06-20 16:04:30.405278', 5, 1, NULL, '', 'Агат белый', '', 'Привезен из Монголии', 'шт', NULL, NULL, '4200.00', '', '', 'Агат белый защищает от любого воздействия, от психологических атак. Помогает справляться с фобиями и тревожными состояниями, дарит владельцу вдохновение, радость бытия. Помогает укрепить и сохранить брак. Обладательница белого агата становиться более притягательна для мужчин. Мужчины становятся более красноречивы.', '', NULL),
(6, '6.jpg', '2020-06-20 16:08:07.092258', '2020-06-20 16:08:37.516507', 6, 1, NULL, '', 'Агат черный', '', 'Привезен из Индии', 'шт', NULL, NULL, '4500.00', '', '', 'Это камень щит - он не пропускает ничего, что могло бы навредить человеку, никакие манипуляции и никакое воздействие. Нейтрализует сглаз, негатив и зависть, направленные на владельца камня. Он сохраняет у человека критический фактор, усиливает лидерские черты владельца. При этом камень любит детей и старается создать семью владельцу. Уравновешивает мысли и эмоции', '', NULL),
(7, '7.jpg', '2020-06-20 16:11:09.834647', '2020-06-20 16:16:37.860811', 7, 1, NULL, '', 'Аквамарин (большой, бусина серебро)', '', 'Привезены из Бразилии', '', NULL, NULL, '5400.00', '', '', 'Камень отношений, поддерживает дружбу и притягивает надежных единомышленников. Выводит злоумышленников на чистую воду, способствует восстановлению справедливости по отношению к своему владельцу. Камень обостряет зрение и физическое, и энергетическое, помогает видеть людей насквозь. Помогает избавится от вредных привычек, избежать проверок, сдать экзамены и любую отчетность.', '', NULL),
(8, '8.jpg', '2020-06-20 16:14:03.122052', '2020-06-20 16:16:05.883628', 8, 1, NULL, '', 'Аквамарин (средний, бусина серебро)', '', 'Привезен из Бразилии', 'шт', NULL, NULL, '4300.00', '', '', 'Камень отношений, поддерживает дружбу и притягивает надежных единомышленников. Выводит злоумышленников на чистую воду, способствует восстановлению справедливости по отношению к своему владельцу. Камень обостряет зрение и физическое, и энергетическое, помогает видеть людей насквозь. Помогает избавится от вредных привычек, избежать проверок, сдать экзамены и любую отчетность.<br>', '', NULL),
(9, '9.jpg', '2020-06-20 16:15:22.349789', '2020-06-20 16:22:36.440947', 9, 1, NULL, '', 'Аквамарин (маленький, бусина позолота)', '', 'Привезен из Бразилии', 'шт', NULL, NULL, '3700.00', '', '', 'Камень отношений, поддерживает дружбу и притягивает надежных единомышленников. Выводит злоумышленников на чистую воду, способствует восстановлению справедливости по отношению к своему владельцу. Камень обостряет зрение и физическое, и энергетическое, помогает видеть людей насквозь. Помогает избавится от вредных привычек, избежать проверок, сдать экзамены и любую отчетность.', '', NULL),
(10, '10.jpg', '2020-06-20 16:20:16.752822', '2020-06-20 16:22:13.594305', 10, 1, NULL, '', 'Амазонит', '', 'Привезен из Перу', '', NULL, NULL, '4700.00', '', '', '<div>Шаманский камень. Обостряет чувства и способствует открытию ясновидения. Подстраивается под настроение владельца, обнуляет негативные мысли. Он как бы стремится удовлетворить любые потребности владельца, будь то деньги или еще что-то. Поддерживает страсть между супругами, избавляет от скандалов, приносит уют и душевное тепло в дом владельца. Способствует развитию магических способностей, интуиции, дара предвиденья. Владельца этого камня практически невозможно обмануть.</div>', '', NULL),
(11, '11.jpg', '2020-06-20 16:23:28.044788', '2020-06-20 16:23:48.389464', 11, 1, NULL, '', 'Амазонит (бусина серебро)', '', '', '', NULL, NULL, '4300.00', '', '', '<div>Шаманский камень. Обостряет чувства и способствует открытию ясновидения. Подстраивается под настроение владельца, обнуляет негативные мысли. Он как бы стремится удовлетворить любые потребности владельца, будь то деньги или еще что-то. Поддерживает страсть между супругами, избавляет от скандалов, приносит уют и душевное тепло в дом владельца. Способствует развитию магических способностей, интуиции, дара предвиденья. Владельца этого камня практически невозможно обмануть.</div>', '', NULL),
(12, '12.jpg', '2020-06-20 16:26:17.185389', '2020-06-20 16:27:23.796565', 12, 1, NULL, '', 'Гематит ограниченный сталью с добавлением перита', '', 'Привезен из Бразилии', 'шт', NULL, NULL, '4600.00', '', '', 'Гематит уравновешивает и раскрывает сверхспособности, но при этом блокирует их, переводя в русло поиска себя, своего дела. Сочетания этих камней отводит от дурных мыслей и необдуманных поступков. Делает человека более целостным. На фото мой браслет, камешек посередине точно таким же не будет', '', NULL),
(13, '13.jpg', '2020-06-20 16:28:47.659459', '2020-06-20 16:29:56.106457', 13, 1, NULL, '', 'Дюмортьерит (бусина черненое серебро 925 пробы)', '', 'Привезен из Перу', 'шт', NULL, NULL, '4300.00', '', '', 'Камень призывает родовых духов на защиту и помощь являясь природным проводником. Подростки, носящие минерал проявляют больше любознательности к учебе. Помогает найти выход из любой сложной ситуации. Охраняет от любого магического воздействия. Камень способствует накоплению благ, притягивает 2 половинку, и укрепляет уже созданную семью.', '', NULL),
(14, '14.jpg', '2020-06-20 16:31:52.647270', '2020-06-20 16:32:14.911522', 14, 1, NULL, '', 'Кварц (бусина золото)', '', 'Привезен с Алтая', 'шт', NULL, NULL, '3900.00', '', '', 'Магический камень, он создает защитную воронку вокруг владельца. Способствует снижению веса и разглаживает кожу. Он нормализует все процессы в теле и жизни владельца, улучшает настроение и притягивает разные приятности. Приносит новые идеи и увеличивает уверенность в своих силах.', '', NULL),
(15, '15.jpg', '2020-06-20 16:45:41.667035', '2020-06-20 16:46:03.068669', 15, 1, NULL, '', 'Розовый коралл (бусина металл)', '', 'Привезен из Австрии', '', NULL, NULL, '2900.00', '', '', 'Способствует нормализации обмена веществ и регенерации в целом - это камень здоровья. Помогает отвадить врагов, сохраняет и умножает финансы. Камень способствует четко видеть свой путь и не сбиться с него. Помогает в любом управлении, как компанией, отделом, так и управлением транспорта. Он ограждает от искушений. Помогает найти партнера и создать семью.', '', NULL),
(16, '16.jpg', '2020-06-20 16:47:38.457322', '2020-06-20 16:48:04.119432', 16, 1, NULL, '', 'Лабрадор (бусина черненное серебро 925 пробы)', '', 'Привезен из Якутии', 'шт', NULL, NULL, '4300.00', '', '', '<div>Лабрадор - камень медиумов и магов, он усиливает дар предвидения, обостряет интуицию. Но поможет он только тому, кто осознаёт наличие у себя этого дара и может им управлять. Дарует владельцу красноречие и дар убеждения. Защищает от любого проявления «нечести», раз в месяц нужно оставлять на ночь на лунном свете (на подоконнике).</div>', '', NULL),
(17, '17.jpg', '2020-06-20 16:49:33.854486', '2020-06-20 16:50:09.611581', 17, 1, NULL, '', 'Лава вулканическая, пирит (бусина сталь)', '', 'Привезен из Испании ', '', NULL, NULL, '3700.00', '', '', 'Лава - камень знаний, если вы что-то изучаете постигаете, если ищите свое предназначение. Камень помогает справится с любыми жизненными ситуациями, раскрывает таланты и скрытые способности. Обостряет интуицию, привезен из Южной Америки. Пирит - это мощный энергетический камень. Его еще называют золото Инков. Благодаря магическим свойствам, камень действует как настоящий допинг, подпитывая истощенный организм энергией, «разжигая» в нем жизнь. Буквально притягивает любовь и разжигает ее в находящихся рядом. Один из магнитов для денег.', '', NULL),
(18, '18.jpg', '2020-06-20 16:51:10.594389', '2020-06-20 17:19:33.392380', 18, 1, NULL, '', 'Лазурит (бусина позолота)', '', 'Привезен из Афганистана', '', NULL, NULL, '4100.00', '', '', 'Всю свою историю лазурит использовался людьми в магических целях. Индейцы им очищались от негатива и плохих воспоминаний. Талисманы из лазурита применялись для исполнения желаний. Очищает от прошлых воспоминаний, защищает от причинения вреда. Приносит удачу в самых неожиданных ситуациях. Наполнят жизнь любовью и радостью. Проводник к общению с Божественным скрытом в каждом.', '', 2),
(19, '19.jpg', '2020-06-20 16:52:39.773560', '2020-06-20 17:19:54.320523', 19, 1, NULL, '', 'Лунный категории А', '', '', '', NULL, NULL, '6900.00', '', '', 'Он способен помогать в азартных играх и любых других делах, где требуется удача. Например, бизнес. Но одновременно с этим он притягивает и любовную удачу, обеспечивая внимание противоположного пола, хотя обычно любовь и удача не соседствуют.', '', NULL),
(20, '20.jpg', '2020-06-20 16:53:47.555525', '2020-06-20 17:20:33.020748', 20, 1, NULL, '', 'Лунный категории А (мелкий)', '', '', '', NULL, NULL, '4100.00', '', '', 'Он способен помогать в азартных играх и любых других делах, где требуется удача. Например, бизнес. Но одновременно с этим он притягивает и любовную удачу, обеспечивая внимание противоположного пола, хотя обычно любовь и удача не соседствуют.', '', NULL),
(21, '21.jpg', '2020-06-20 17:15:09.941141', '2020-06-20 17:15:41.492323', 21, 1, NULL, '', 'Нефрит (металл с покрытием)', '', 'Привезет из Бурятии', '', NULL, NULL, '3400.00', '', '', '<div>Нефрит считается камнем бессмертия. Обладает ранозаживительным эффектом, восстанавливает поврежденные клетки и ткани. Лечит бесплодие. Притягивает счастливые перемены. Щит от любой магии, причем с отдачей обидчику. Отгоняет депрессии.</div>', '', NULL),
(22, '22.jpg', '2020-06-20 17:24:00.315860', '2020-06-20 17:24:45.074243', 22, 1, NULL, '', 'Пирит (бусина серебро)', '', 'Привезен из Испании', '', NULL, NULL, '3900.00', '', '', 'Пирит это мощный энергетический камень. Его еще называют золотом Инков. Благодаря магическим свойствам, камень действует как настоящий допинг, подпитывая истощенный организм энергией, «разжигая» в нем жизнь. Буквально притягивая любовь и разжигая ее в находящихся рядом. Один из магнитов для денег. Носить можно первый месяц не более 3х дней подряд. Так как камень очень мощный, использую его маленький размер', '', NULL),
(23, '23.jpg', '2020-06-20 17:27:58.905725', '2020-06-20 17:28:25.291753', 23, 1, NULL, '', 'Родонит (бусина позолота с кельтским защитным узором, позолота или серебро)', '', 'Привезен из Австрии', '', NULL, NULL, '4300.00', '', '', '<div>Камень является магнитом для материальных благ и накопительства. Защищает от краж и финансовых потерь. Придает уверенности в себе и избавляет от лени. Пожалуй, самый семейный камень - помогает сохранить и укрепить семью, брак. Одиноким встретить вторую половину. Помогает зачать ребенка. Кельтский узор защищает семью владельца камня.</div>', '', NULL),
(24, '24.jpg', '2020-06-20 18:37:07.611897', '2020-06-20 18:37:23.779734', 24, 1, NULL, '', 'Родохрозит (бусины позолота)', '', 'Привезен из Перу', '', NULL, NULL, '5600.00', '', '', '<div>Семейный женский камень. Это природный резервуар, он питает силой обладательницу. Считается, что он отводит любое негативное воздействие, приносит удачу и действительно выстраивает отношения с противоположным полом. Но это тактильный камень, его нужно носить постоянно. Он выделяет своего обладателя среди любых конкурентов, особенно хорош при заключении договоров. Этот камень излучает любовь и умягчает сердца людей по отношению к вам. Так же он снижает уровень стресса и успокаивает нервную систему. Глобально - камень для налаживания отношений как внутренних, так и внешних. Абсолютно любые отношения, но камень любит чтоб у обладательницы был муж, или человек, которого вы будете воспринимать как мужа. Отлично подойдёт, если хотелось бы отношений. Также нормализует давление и вообще поддерживает сердечно- сосудистую систему</div>', '', NULL),
(25, '25.jpg', '2020-06-20 18:38:35.872320', '2020-06-20 18:38:49.911074', 25, 1, NULL, '', 'Родохрозит (средний, бусина позолота)', '', 'Привезен из Перу', '', NULL, NULL, '4900.00', '', '', '<div>Семейный женский камень. Это природный резервуар, он питает силой обладательницу. Считается, что он отводит любое негативное воздействие, приносит удачу и действительно выстраивает отношения с противоположным полом. Но это тактильный камень, его нужно носить постоянно. Он выделяет своего обладателя среди любых конкурентов, особенно хорош при заключении договоров. Этот камень излучает любовь и умягчает сердца людей по отношению к вам. Так же он снижает уровень стресса и успокаивает нервную систему. Глобально - камень для налаживания отношений как внутренних, так и внешних. Абсолютно любые отношения, но камень любит чтоб у обладательницы был муж, или человек, которого вы будете воспринимать как мужа. Отлично подойдёт, если хотелось бы отношений. Также нормализует давление и вообще поддерживает сердечно- сосудистую систему</div>', '', NULL),
(26, '26.jpg', '2020-06-20 18:39:52.338223', '2020-06-20 18:40:06.962537', 26, 1, NULL, '', 'Родохрозит (маленький, бусина позолота)', '', 'Привезен из Перу', '', NULL, NULL, '4700.00', '', '', '<div>Семейный женский камень. Это природный резервуар, он питает силой обладательницу. Считается, что он отводит любое негативное воздействие, приносит удачу и действительно выстраивает отношения с противоположным полом. Но это тактильный камень, его нужно носить постоянно. Он выделяет своего обладателя среди любых конкурентов, особенно хорош при заключении договоров. Этот камень излучает любовь и умягчает сердца людей по отношению к вам. Так же он снижает уровень стресса и успокаивает нервную систему. Глобально - камень для налаживания отношений как внутренних, так и внешних. Абсолютно любые отношения, но камень любит чтоб у обладательницы был муж, или человек, которого вы будете воспринимать как мужа. Отлично подойдёт, если хотелось бы отношений. Также нормализует давление и вообще поддерживает сердечно- сосудистую систему</div>', '', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `products_productscats`
--

DROP TABLE IF EXISTS `products_productscats`;
CREATE TABLE IF NOT EXISTS `products_productscats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_id` int(11) DEFAULT NULL,
  `product_id` int(11) NOT NULL,
  `container_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_productscat_product_id_6cc6463e_fk_products_` (`product_id`),
  KEY `products_productscats_cat_id_71130549_fk_flatcontent_blocks_id` (`cat_id`),
  KEY `products_productscat_container_id_2151481b_fk_flatconte` (`container_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `products_productsphotos`
--

DROP TABLE IF EXISTS `products_productsphotos`;
CREATE TABLE IF NOT EXISTS `products_productsphotos` (
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
  KEY `products_productsphotos_name_f19259af` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `products_productsphotos`
--

INSERT INTO `products_productsphotos` (`id`, `img`, `created`, `updated`, `position`, `is_active`, `state`, `parents`, `name`, `product_id`) VALUES
(1, '1.jpg', '2020-06-20 16:21:09.754867', '2020-06-20 16:21:09.754911', 1, 1, NULL, NULL, NULL, 10);

-- --------------------------------------------------------

--
-- Table structure for table `products_productsproperties`
--

DROP TABLE IF EXISTS `products_productsproperties`;
CREATE TABLE IF NOT EXISTS `products_productsproperties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `prop_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_productspro_product_id_50131a5d_fk_products_` (`product_id`),
  KEY `products_productspro_prop_id_4d9b9492_fk_products_` (`prop_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `products_propertiesvalues`
--

DROP TABLE IF EXISTS `products_propertiesvalues`;
CREATE TABLE IF NOT EXISTS `products_propertiesvalues` (
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
  KEY `products_propertiesvalues_digit_value_98cb8771` (`digit_value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `products_property`
--

DROP TABLE IF EXISTS `products_property`;
CREATE TABLE IF NOT EXISTS `products_property` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `shop_orders`
--

DROP TABLE IF EXISTS `shop_orders`;
CREATE TABLE IF NOT EXISTS `shop_orders` (
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
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `shop_orders_user_id_9abd760d_fk_personal_shopper_id` (`user_id`),
  KEY `shop_orders_img_89a0f42d` (`img`),
  KEY `shop_orders_created_f4f7ad2a` (`created`),
  KEY `shop_orders_updated_c63e3f75` (`updated`),
  KEY `shop_orders_position_93545035` (`position`),
  KEY `shop_orders_is_active_2cacc96e` (`is_active`),
  KEY `shop_orders_state_c02d2396` (`state`),
  KEY `shop_orders_parents_907e9242` (`parents`),
  KEY `shop_orders_number_6fd689bc` (`number`),
  KEY `shop_orders_comments_4a9b55e1` (`comments`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `shop_purchases`
--

DROP TABLE IF EXISTS `shop_purchases`;
CREATE TABLE IF NOT EXISTS `shop_purchases` (
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
  `user_id` int(11) DEFAULT NULL,
  `discount_info` varchar(255) DEFAULT NULL,
  `product_manufacturer` varchar(255) DEFAULT NULL,
  `product_measure` varchar(255) DEFAULT NULL,
  `product_price` decimal(13,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `shop_purchases_order_id_7309c2ce_fk_shop_orders_id` (`order_id`),
  KEY `shop_purchases_user_id_0cfce7b0_fk_personal_shopper_id` (`user_id`),
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
  KEY `shop_purchases_product_measure_44500ae1` (`product_measure`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `shop_wishlist`
--

DROP TABLE IF EXISTS `shop_wishlist`;
CREATE TABLE IF NOT EXISTS `shop_wishlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `shop_wishlist_product_id_0fc70568_fk_products_products_id` (`product_id`),
  KEY `shop_wishlist_user_id_131c4a81_fk_personal_shopper_id` (`user_id`),
  KEY `shop_wishlist_img_9cc8d6b2` (`img`),
  KEY `shop_wishlist_created_5afac261` (`created`),
  KEY `shop_wishlist_updated_562383b8` (`updated`),
  KEY `shop_wishlist_position_d20beef8` (`position`),
  KEY `shop_wishlist_is_active_32b112fb` (`is_active`),
  KEY `shop_wishlist_state_d78b0872` (`state`),
  KEY `shop_wishlist_parents_e51e38bc` (`parents`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `flatcontent_blocks`
--
ALTER TABLE `flatcontent_blocks`
  ADD CONSTRAINT `flatcontent_blocks_container_id_5864baa1_fk_flatconte` FOREIGN KEY (`container_id`) REFERENCES `flatcontent_containers` (`id`);

--
-- Constraints for table `flatcontent_linkcontainer`
--
ALTER TABLE `flatcontent_linkcontainer`
  ADD CONSTRAINT `flatcontent_linkcont_block_id_95a742ab_fk_flatconte` FOREIGN KEY (`block_id`) REFERENCES `flatcontent_blocks` (`id`),
  ADD CONSTRAINT `flatcontent_linkcont_container_id_9d707d07_fk_flatconte` FOREIGN KEY (`container_id`) REFERENCES `flatcontent_containers` (`id`);

--
-- Constraints for table `login_customuser`
--
ALTER TABLE `login_customuser`
  ADD CONSTRAINT `login_customuser_user_id_70d7d409_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `products_productscats`
--
ALTER TABLE `products_productscats`
  ADD CONSTRAINT `products_productscat_container_id_2151481b_fk_flatconte` FOREIGN KEY (`container_id`) REFERENCES `flatcontent_containers` (`id`),
  ADD CONSTRAINT `products_productscat_product_id_6cc6463e_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_products` (`id`),
  ADD CONSTRAINT `products_productscats_cat_id_71130549_fk_flatcontent_blocks_id` FOREIGN KEY (`cat_id`) REFERENCES `flatcontent_blocks` (`id`);

--
-- Constraints for table `products_productsphotos`
--
ALTER TABLE `products_productsphotos`
  ADD CONSTRAINT `products_productspho_product_id_1dd25946_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_products` (`id`);

--
-- Constraints for table `products_productsproperties`
--
ALTER TABLE `products_productsproperties`
  ADD CONSTRAINT `products_productspro_product_id_50131a5d_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_products` (`id`),
  ADD CONSTRAINT `products_productspro_prop_id_4d9b9492_fk_products_` FOREIGN KEY (`prop_id`) REFERENCES `products_propertiesvalues` (`id`);

--
-- Constraints for table `products_propertiesvalues`
--
ALTER TABLE `products_propertiesvalues`
  ADD CONSTRAINT `products_propertiesv_prop_id_45598b2c_fk_products_` FOREIGN KEY (`prop_id`) REFERENCES `products_property` (`id`);

--
-- Constraints for table `shop_orders`
--
ALTER TABLE `shop_orders`
  ADD CONSTRAINT `shop_orders_user_id_9abd760d_fk_personal_shopper_id` FOREIGN KEY (`user_id`) REFERENCES `personal_shopper` (`id`);

--
-- Constraints for table `shop_purchases`
--
ALTER TABLE `shop_purchases`
  ADD CONSTRAINT `shop_purchases_order_id_7309c2ce_fk_shop_orders_id` FOREIGN KEY (`order_id`) REFERENCES `shop_orders` (`id`),
  ADD CONSTRAINT `shop_purchases_user_id_0cfce7b0_fk_personal_shopper_id` FOREIGN KEY (`user_id`) REFERENCES `personal_shopper` (`id`);

--
-- Constraints for table `shop_wishlist`
--
ALTER TABLE `shop_wishlist`
  ADD CONSTRAINT `shop_wishlist_product_id_0fc70568_fk_products_products_id` FOREIGN KEY (`product_id`) REFERENCES `products_products` (`id`),
  ADD CONSTRAINT `shop_wishlist_user_id_131c4a81_fk_personal_shopper_id` FOREIGN KEY (`user_id`) REFERENCES `personal_shopper` (`id`);
SET FOREIGN_KEY_CHECKS=1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
