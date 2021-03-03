-- MySQL dump 10.13  Distrib 5.7.31, for osx10.12 (x86_64)
--
-- Host: localhost    Database: white_siberia
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
-- Table structure for table `addresses_address`
--

DROP TABLE IF EXISTS `addresses_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `addresses_address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `postalCode` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `county` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  `subdistrict` varchar(255) DEFAULT NULL,
  `street` varchar(255) DEFAULT NULL,
  `houseNumber` varchar(255) DEFAULT NULL,
  `addressLines` varchar(255) DEFAULT NULL,
  `additionalData` varchar(255) DEFAULT NULL,
  `latitude` decimal(30,25) DEFAULT NULL,
  `longitude` decimal(30,25) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `addresses_address_img_d97c8404` (`img`),
  KEY `addresses_address_created_c5f21648` (`created`),
  KEY `addresses_address_updated_267c29b8` (`updated`),
  KEY `addresses_address_position_cc9d8a12` (`position`),
  KEY `addresses_address_is_active_5781cfbc` (`is_active`),
  KEY `addresses_address_parents_0d3365ce` (`parents`),
  KEY `addresses_address_postalCode_958f100a` (`postalCode`),
  KEY `addresses_address_country_37f18fba` (`country`),
  KEY `addresses_address_state_d77aca34` (`state`),
  KEY `addresses_address_county_25761896` (`county`),
  KEY `addresses_address_city_f178f038` (`city`),
  KEY `addresses_address_district_32ade1ac` (`district`),
  KEY `addresses_address_subdistrict_f4357340` (`subdistrict`),
  KEY `addresses_address_street_57aa04d4` (`street`),
  KEY `addresses_address_houseNumber_b3d8f726` (`houseNumber`),
  KEY `addresses_address_addressLines_4c7151ff` (`addressLines`),
  KEY `addresses_address_additionalData_ba86b71c` (`additionalData`),
  KEY `addresses_address_latitude_4b3e2a1a` (`latitude`),
  KEY `addresses_address_longitude_f87f3196` (`longitude`),
  KEY `addresses_address_place_bff2abae` (`place`)
) ENGINE=InnoDB AUTO_INCREMENT=441 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses_address`
--

LOCK TABLES `addresses_address` WRITE;
/*!40000 ALTER TABLE `addresses_address` DISABLE KEYS */;
INSERT INTO `addresses_address` VALUES (380,NULL,'2021-02-05 01:31:06.278798','2021-02-05 01:31:06.278830',1,1,NULL,'127015','Россия','Москва',NULL,'Москва',NULL,NULL,'Вятская улица','49с2','ул. Вятская, д. 49, стр.2',NULL,55.8044860000000000000000000,37.5803460000000000000000000,'Electro town'),(381,NULL,'2021-02-05 01:31:06.293383','2021-02-05 01:31:06.293408',2,1,NULL,'117312','Россия','Москва',NULL,'Москва',NULL,NULL,'улица Вавилова','9Ас5','ул. Вавилова, д. 9а, стр.5',NULL,55.7010390000000000000000000,37.5890600000000000000000000,'LuxVelo'),(382,NULL,'2021-02-05 01:31:06.307374','2021-02-09 23:36:33.121530',3,1,'','','Россия','Москва','','Москва','','','Волгоградский проспект','32к8','Волгоградский проспект д. 32 к. 8. ТЦ ТехноХолл 2-й этаж павильон АВ-40','',55.7238910000000000000000000,37.6885570000000000000000000,'Electro-skuter'),(383,NULL,'2021-02-05 01:31:06.310295','2021-02-05 01:31:06.310312',4,1,NULL,'119331','Россия','Москва',NULL,'Москва',NULL,NULL,'улица Марии Ульяновой','16','ул. Марии Ульяновой д. 16',NULL,55.6831120000000000000000000,37.5218030000000000000000000,'Electro-skuter'),(384,NULL,'2021-02-05 01:31:06.312895','2021-02-05 01:31:06.312911',5,1,NULL,'129164','Россия','Москва',NULL,'Москва',NULL,NULL,'проспект Мира','124к2','Проспект мира 124 к2',NULL,55.8163530000000000000000000,37.6399850000000000000000000,'Giroskutershop.ru'),(385,NULL,'2021-02-05 01:31:06.315612','2021-02-05 01:31:06.315629',6,1,NULL,'123022','Россия','Москва',NULL,'Москва',NULL,NULL,'Большая Декабрьская улица','3с1','ул. Большая декабрьская 3 стр1',NULL,55.7650880000000000000000000,37.5575470000000000000000000,'Giroskutershop.ru'),(386,NULL,'2021-02-05 01:31:06.318316','2021-02-05 01:31:06.318334',7,1,NULL,'125284','Россия','Москва',NULL,'Москва',NULL,NULL,'улица Поликарпова','27','ул. Поликарпова, д. 27',NULL,55.7813120000000000000000000,37.5436770000000000000000000,'Girobay'),(387,NULL,'2021-02-05 01:31:06.321100','2021-02-05 01:31:06.321117',8,1,NULL,'105077','Россия','Москва',NULL,'Москва',NULL,NULL,'Средняя Первомайская улица','3','ул. Средняя Первомайская, д. 3',NULL,55.7957670000000000000000000,37.8037570000000000000000000,'Eko-Bike'),(388,NULL,'2021-02-05 01:31:06.323692','2021-02-05 01:31:06.323709',9,1,NULL,NULL,'Россия','Москва',NULL,'Москва',NULL,NULL,'МКАД, 27-й километр',NULL,'27 км МКАД (внешняя) ТЦ «Формула Х»',NULL,55.5787720000000000000000000,37.6960760000000000000000000,'ELECTRON motors'),(389,NULL,'2021-02-05 01:31:06.326259','2021-02-05 01:31:06.326276',10,1,NULL,'109382','Россия','Москва',NULL,'Москва',NULL,NULL,'улица Нижние Поля','27с2','ул. Нижние поля д. 27 ст1',NULL,55.6588040000000000000000000,37.7357550000000000000000000,'Гиротрейд.рф'),(390,NULL,'2021-02-05 01:31:06.328831','2021-02-05 01:31:06.328849',11,1,NULL,'111020','Россия','Москва',NULL,'Москва',NULL,NULL,'Юрьевский переулок','16А','Юрьевский переулок 16А',NULL,55.7651440000000000000000000,37.7174110000000000000000000,'ЦИМ'),(391,NULL,'2021-02-05 01:31:06.331530','2021-02-05 01:31:06.331548',12,1,NULL,'119270','Россия','Москва',NULL,'Москва',NULL,NULL,'Лужнецкая набережная','2/4с71','Лужнецкая набережная д. 2/4 стр. 71',NULL,55.7135420000000000000000000,37.5714800000000000000000000,'ElectroStreet'),(392,NULL,'2021-02-05 01:31:06.334174','2021-02-05 01:31:06.334190',13,1,NULL,'117535','Россия','Москва',NULL,'Москва',NULL,NULL,'Россошанский проезд','3','Россошанский проезд, д. 3',NULL,55.6009180000000000000000000,37.6092720000000000000000000,'GreenWheel'),(393,NULL,'2021-02-05 01:31:06.336888','2021-02-05 01:31:06.336905',14,1,NULL,'109316','Россия','Москва',NULL,'Москва',NULL,NULL,'Волгоградский проспект','35','Волгоградский проспект д. 35 оф. 106',NULL,55.7234150000000000000000000,37.6960490000000000000000000,'Sigvey.ru'),(394,NULL,'2021-02-05 01:31:06.339469','2021-02-05 01:31:06.339486',15,1,NULL,'117593','Россия','Москва',NULL,'Москва',NULL,NULL,'Соловьиный проезд','18А','Соловьиный проезд дом 18А оф.1',NULL,55.6052410000000000000000000,37.5560740000000000000000000,'Luxwheel'),(395,NULL,'2021-02-05 01:31:06.342063','2021-02-09 22:26:39.266925',16,1,'','','Россия','Москва','','Москва','','','улица Миклухо-Маклая','8','ул. Миклухо-Маклая владение д. 8 ст. 3 заезд с улицы Саморы Машела','',55.6508760000000000000000000,37.5036750000000000000000000,'Raptor-tv'),(396,NULL,'2021-02-05 01:31:06.344713','2021-02-05 01:31:06.344733',17,1,NULL,'111402','Россия','Москва',NULL,'Москва',NULL,NULL,'Кетчерская улица','13с2','ул. Кетчерская, д. 13, стр. 2',NULL,55.7462230000000000000000000,37.8383600000000000000000000,'Zoty'),(397,NULL,'2021-02-05 01:31:06.347809','2021-02-05 01:31:06.347826',18,1,NULL,'121596','Россия','Москва',NULL,'Москва',NULL,NULL,'улица Горбунова','12к2с5','ул. Горбунова д. 12 к. 2 стр. 5',NULL,55.7268720000000000000000000,37.3811630000000000000000000,'Simargl Elektro'),(398,NULL,'2021-02-05 01:31:06.350522','2021-02-05 01:31:06.350539',19,1,NULL,'115088','Россия','Москва',NULL,'Москва',NULL,NULL,'2-я улица Машиностроения','17с1','2-ая ул. Машиностроения д. 17 стр. 1',NULL,55.7160420000000000000000000,37.6822060000000000000000000,'Электросамокаты в России'),(399,NULL,'2021-02-05 01:31:06.353291','2021-02-05 01:31:06.353308',20,1,NULL,'111538','Россия','Москва',NULL,'Москва',NULL,NULL,'Вешняковская улица','18','Вешняковская 18 ТЦ Вешняки 3 этаж',NULL,55.7241240000000000000000000,37.8251550000000000000000000,'Girosmart'),(400,NULL,'2021-02-05 01:31:06.355861','2021-02-05 01:31:06.355878',21,1,NULL,'424028','Россия','Республика Марий Эл','городской округ Йошкар-Ола','Йошкар-Ола',NULL,NULL,'улица Строителей','19','ул. Строителей д. 19 кв. 8',NULL,56.6354710000000000000000000,47.8378940000000000000000000,'Lux velo'),(401,NULL,'2021-02-05 01:31:06.358451','2021-02-05 01:31:06.358468',22,1,NULL,NULL,'Франция','Прованс-Альпы-Лазурный Берег',NULL,NULL,NULL,NULL,NULL,NULL,'Проспект Ленина 12а, сек.111',NULL,44.0894640000000000000000000,5.4909970000000000000000000,'ElectroStreet'),(402,NULL,'2021-02-05 01:31:06.361302','2021-02-05 01:31:06.361327',23,1,NULL,NULL,'Киргизия','город республиканского подчинения Бишкек',NULL,'Бишкек',NULL,NULL,'Байкальский переулок','12','Байкальский переулок, 12',NULL,42.9217320000000000000000000,74.6136810000000000000000000,'Electro town'),(403,NULL,'2021-02-05 01:31:06.364223','2021-02-05 01:31:06.364244',24,1,NULL,'644046','Россия','Омская область','городской округ Омск','Омск',NULL,NULL,'улица Декабристов','114/1','Декабристов, 114/1',NULL,54.9666180000000000000000000,73.3943710000000000000000000,'ElectroSamokaty'),(404,NULL,'2021-02-05 01:31:06.366945','2021-02-05 01:31:06.366961',25,1,NULL,'420088','Россия','Республика Татарстан','городской округ Казань','Казань',NULL,NULL,'проспект Победы','206','проспект Победы, д. 206, БЦ ВИЗИТ',NULL,55.8031100000000000000000000,49.2103760000000000000000000,'Elektro-mall.ru'),(405,NULL,'2021-02-05 01:31:06.369623','2021-02-05 01:31:06.369641',26,1,NULL,'420132','Россия','Республика Татарстан','городской округ Казань','Казань',NULL,NULL,'улица Адоратского','63','ул. Адоратского д. 63',NULL,55.8447130000000000000000000,49.1461910000000000000000000,'Electrotexas'),(406,NULL,'2021-02-05 01:31:06.372279','2021-02-05 01:31:06.372296',27,1,NULL,'420097','Россия','Республика Татарстан','городской округ Казань','Казань',NULL,NULL,'улица Зинина','9/23','ул. Зинина, д. 9/23',NULL,55.7896540000000000000000000,49.1561090000000000000000000,'Electro town'),(407,NULL,'2021-02-05 01:31:06.374959','2021-02-05 01:31:06.374975',28,1,NULL,'190000','Россия','Санкт-Петербург',NULL,'Санкт-Петербург',NULL,NULL,'Казанская улица','45','. ул. Казанская 45. Вход со двора.',NULL,59.9280540000000000000000000,30.3073610000000000000000000,'Электросамокаты в России'),(408,NULL,'2021-02-05 01:31:06.378264','2021-02-05 01:31:06.378288',29,1,NULL,'197110','Россия','Санкт-Петербург',NULL,'Санкт-Петербург',NULL,NULL,'Левашовский проспект','15','Левашовский проспект, д.15',NULL,59.9667460000000000000000000,30.2847060000000000000000000,'Zoty'),(409,NULL,'2021-02-05 01:31:06.381089','2021-02-05 01:31:06.381106',30,1,NULL,'190013','Россия','Санкт-Петербург',NULL,'Санкт-Петербург',NULL,NULL,'Серпуховская улица','23','ул. Серпуховская д. 23',NULL,59.9145470000000000000000000,30.3237460000000000000000000,'Electro-skuter'),(410,NULL,'2021-02-05 01:31:06.383739','2021-02-05 01:31:06.383756',31,1,NULL,'194354','Россия','Санкт-Петербург',NULL,'Санкт-Петербург',NULL,NULL,'проспект Энгельса','113к2','пр-т Энгельса 113\\2',NULL,60.0376700000000000000000000,30.3265760000000000000000000,'Smart-техники'),(411,NULL,'2021-02-05 01:31:06.386603','2021-02-05 01:31:06.386621',32,1,NULL,'193232','Россия','Санкт-Петербург',NULL,'Санкт-Петербург',NULL,NULL,'улица Дыбенко','23к1','ул. Дыбенко 23\\1',NULL,59.9041890000000000000000000,30.4740790000000000000000000,'Smart-техники'),(412,NULL,'2021-02-05 01:31:06.389203','2021-02-05 01:31:06.389220',33,1,NULL,'196158','Россия','Санкт-Петербург',NULL,'Санкт-Петербург',NULL,NULL,'улица Ленсовета','81','ул. Ленсовета 81',NULL,59.8377930000000000000000000,30.3392510000000000000000000,'Smart-техники'),(413,NULL,'2021-02-05 01:31:06.391803','2021-02-05 01:31:06.391821',34,1,NULL,'190068','Россия','Санкт-Петербург',NULL,'Санкт-Петербург',NULL,NULL,'Вознесенский проспект','34Г','Вознесенский проспект 34 литера Г',NULL,59.9250830000000000000000000,30.3084210000000000000000000,'Sky run'),(414,NULL,'2021-02-05 01:31:06.394475','2021-02-05 01:31:06.394492',35,1,NULL,'191119','Россия','Санкт-Петербург',NULL,'Санкт-Петербург',NULL,NULL,'улица Достоевского','29/18','улица Достоевского д. 29/18',NULL,59.9221560000000000000000000,30.3440660000000000000000000,'Electro town'),(415,NULL,'2021-02-05 01:31:06.397095','2021-02-09 23:37:25.549517',36,1,'','','Россия','Краснодарский край','городской округ Сочи','Сочи','','','жилой район Адлер','','Адлерский район, ул. Куйбышева, 36 «Мадагаскар»','',43.4328370000000000000000000,39.9169000000000000000000000,'Scooters-Zone'),(416,NULL,'2021-02-05 01:31:06.399757','2021-02-05 01:31:06.399774',37,1,NULL,NULL,'Россия','Краснодарский край','городской округ Сочи',NULL,NULL,NULL,'Центральный район',NULL,'ул. Конституции СССР, 46. Торговый центр ЛЕВЫЙ БЕРЕГ, 2й подъезд.',NULL,43.6101500000000000000000000,39.7364380000000000000000000,'Scooters-Zone'),(417,NULL,'2021-02-05 01:31:06.402406','2021-02-05 01:31:06.402425',38,1,NULL,NULL,'Россия','Белгородская область','муниципальное образование Город Белгород','Белгород',NULL,NULL,'проспект Богдана Хмельницкого','131','Проспект Богдана Хмельницкого д. 131 этаж 1',NULL,50.6130620000000000000000000,36.5776200000000000000000000,'King Toys'),(418,NULL,'2021-02-05 01:31:06.406713','2021-02-05 01:31:06.406739',39,1,NULL,NULL,'Казахстан','Алматы',NULL,'Алматы',NULL,NULL,'улица Герцена','83','ул. Герцена, д. 83',NULL,43.2927280000000000000000000,76.9564430000000000000000000,'Гироскутер 43'),(419,NULL,'2021-02-05 01:31:06.409677','2021-02-05 01:31:06.409694',40,1,NULL,'610002','Россия','Кировская область','городской округ Город Киров','Киров',NULL,NULL,'улица Горбачёва','30','ул. Горбачева, д.30',NULL,58.5990750000000000000000000,49.6798890000000000000000000,'Energy Shop'),(420,NULL,'2021-02-05 01:31:06.412702','2021-02-05 01:31:06.412719',41,1,NULL,'620075','Россия','Свердловская область','муниципальное образование Город Екатеринбург','Екатеринбург',NULL,NULL,'улица Луначарского','77','ул. Луначарского, д. 77',NULL,56.8482020000000000000000000,60.6178930000000000000000000,'Zoty'),(421,NULL,'2021-02-05 01:31:06.415313','2021-02-05 01:31:06.415330',42,1,NULL,'610020','Россия','Кировская область','городской округ Город Киров','Киров',NULL,NULL,'Московская улица','11','ул. Московская, 11',NULL,58.6039560000000000000000000,49.6791440000000000000000000,'Electro town'),(422,NULL,'2021-02-05 01:31:06.418163','2021-02-05 01:31:06.418183',43,1,NULL,'614068','Россия','Пермский край','городской округ Пермь','Пермь',NULL,NULL,'улица Луначарского','101','ул. Луначарского, д. 101',NULL,58.0029880000000000000000000,56.2195800000000000000000000,'Gyroperm'),(423,NULL,'2021-02-05 01:31:06.420881','2021-02-05 01:31:06.420897',44,1,NULL,NULL,'Киргизия','Нарынская область',NULL,'Нарын',NULL,NULL,'улица Ленина','92','ул. Ленина 92',NULL,41.4282760000000000000000000,75.9912480000000000000000000,'Rocket'),(424,NULL,'2021-02-05 01:31:06.423457','2021-02-05 01:31:06.423474',45,1,NULL,'302043','Россия','Орловская область','городской округ Орёл','Орёл',NULL,NULL,'Маслозаводской переулок','2','Маслозаводской переулок, дом 2',NULL,52.9390570000000000000000000,36.0506590000000000000000000,'Wiseshop'),(425,NULL,'2021-02-05 01:31:06.426090','2021-02-05 01:31:06.426107',46,1,NULL,'644050','Россия','Омская область','городской округ Омск','Омск',NULL,NULL,'проспект Мира','28/1','Проспект Мира д. 28 к. 1',NULL,55.0256990000000000000000000,73.2950980000000000000000000,'Sky run'),(426,NULL,'2021-02-05 01:31:06.428683','2021-02-05 01:31:06.428700',47,1,NULL,NULL,'Россия','Красноярский край','городской округ Красноярск','Красноярск',NULL,NULL,'Регатная улица','4','ул. Регатная, д. 4, пом. 322',NULL,55.9991380000000000000000000,92.9055000000000000000000000,'Sky run'),(427,NULL,'2021-02-05 01:31:06.431298','2021-02-05 01:31:06.431315',48,1,NULL,NULL,'Россия','Ставропольский край','городской округ Ставрополь','Ставрополь',NULL,NULL,'проспект Кулакова','27А','Проспект Кулакова 27А',NULL,45.0611660000000000000000000,41.9225600000000000000000000,'Smart Gifts'),(428,NULL,'2021-02-05 01:31:06.433962','2021-02-05 01:31:06.433979',49,1,NULL,NULL,'Россия','Ставропольский край','городской округ Ставрополь','Ставрополь',NULL,NULL,'проспект Карла Маркса','47','Проспект Карла Маркса 47-49',NULL,45.0504180000000000000000000,41.9860350000000000000000000,'Smart Gifts'),(429,NULL,'2021-02-05 01:31:06.436697','2021-02-05 01:31:06.436714',50,1,NULL,'300041','Россия','Тульская область','муниципальное образование Тула','Тула',NULL,NULL,'улица Каминского','24В','ул. Каминского 24в, ТРЦ Тройка: 1 этаж, бутик 1',NULL,54.1915370000000000000000000,37.6134130000000000000000000,'Технологии Будущего'),(430,NULL,'2021-02-05 01:31:06.439437','2021-02-05 01:31:06.439454',51,1,NULL,'109386','Россия','Москва',NULL,'Москва',NULL,NULL,'Новороссийская улица','3','ул. Новороссийская, д.3',NULL,55.6806360000000000000000000,37.7610960000000000000000000,'Dindi'),(431,NULL,'2021-02-05 01:31:06.443651','2021-02-05 01:31:06.443668',52,1,NULL,NULL,'Армения','Ереван',NULL,'Ереван',NULL,NULL,'Севастопольская улица','20/1','ул. Севастопольская, 20\\1',NULL,40.1959200000000000000000000,44.4870610000000000000000000,'Dindi'),(432,NULL,'2021-02-05 01:31:06.446260','2021-02-05 01:31:06.446277',53,1,NULL,'450006','Россия','Республика Башкортостан','городской округ Уфа','Уфа',NULL,NULL,'улица Цюрупы','149','ул. Цюрупы, 149',NULL,54.7428760000000000000000000,55.9605420000000000000000000,'Electro town'),(433,NULL,'2021-02-05 01:31:06.448812','2021-02-05 01:31:06.448829',54,1,NULL,NULL,'Россия','Тюменская область','городской округ Тюмень','Тюмень',NULL,NULL,'микрорайон Парфёново',NULL,'ул. Комиссаржевской, 15',NULL,57.1922110000000000000000000,65.5694160000000000000000000,'Electro town'),(434,NULL,'2021-02-05 01:31:06.451504','2021-02-05 01:31:06.451524',55,1,NULL,'640003','Россия','Курганская область','городской округ Курган','Курган',NULL,NULL,'улица Тимофея Невежина','3с10','ул. Невежина 3 с 10',NULL,55.4283470000000000000000000,65.2980620000000000000000000,'Eco drive 45'),(435,NULL,'2021-02-05 01:31:06.454197','2021-02-05 01:31:06.454214',56,1,NULL,'610033','Россия','Кировская область','городской округ Город Киров','Киров',NULL,NULL,'Московская улица','118к1','Московская улица, 118, к.1',NULL,58.6017250000000000000000000,49.6204930000000000000000000,'ElectroTown'),(436,NULL,'2021-02-05 01:31:06.456751','2021-02-05 01:31:06.456767',57,1,NULL,NULL,'Россия','Алтайский край',NULL,NULL,NULL,NULL,'Особая экономическая зона туристско-рекреационного типа Бирюзовая Катунь',NULL,'ул. Бирюзовая, д. 1',NULL,51.7882930000000000000000000,85.7373310000000000000000000,'Zoty'),(437,NULL,'2021-02-05 01:31:06.459301','2021-02-05 01:31:06.459317',58,1,NULL,NULL,'Россия','Нижегородская область','городской округ Нижний Новгород','Нижний Новгород',NULL,'жилой район Верхние Печёры','Нижегородский район',NULL,'ул. Композитора Касьянова, д.6Гк1',NULL,56.2885210000000000000000000,44.0578730000000000000000000,'ELECTROCART'),(438,NULL,'2021-02-05 01:31:06.462044','2021-02-05 01:31:06.462062',59,1,NULL,NULL,'Беларусь','Минск',NULL,'Минск',NULL,NULL,'улица Тимирязева','9','ул. Тимирязева 9, 3 этаж',NULL,53.9071110000000000000000000,27.5315400000000000000000000,'Mashinki-nn'),(439,NULL,'2021-02-05 01:31:06.464682','2021-02-05 01:31:06.464699',60,1,NULL,NULL,'Беларусь','Минская область','Минский район','деревня Копище',NULL,NULL,'Авиационная улица','10','Беларусь, Минск, Новая Боровая, улица Авиационная10',NULL,53.9608990000000000000000000,27.6628650000000000000000000,'WHITE SIBERIA'),(440,NULL,'2021-02-05 01:31:06.467479','2021-02-05 01:48:54.632166',61,1,'','','Казахстан','Карагандинская область','городской акимат Караганда','Караганда','','','улица Крылова','101','Казахстан г. Караганда, ул. Крылова, д. 101','',49.7955560000000000000000000,73.0600180000000000000000000,'WHITE SIBERIA');
/*!40000 ALTER TABLE `addresses_address` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add user',3,'add_user'),(10,'Can change user',3,'change_user'),(11,'Can delete user',3,'delete_user'),(12,'Can view user',3,'view_user'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Админка - Настрока',6,'add_config'),(22,'Can change Админка - Настрока',6,'change_config'),(23,'Can delete Админка - Настрока',6,'delete_config'),(24,'Can view Админка - Настрока',6,'view_config'),(25,'Can add Админка - Задача',7,'add_tasks'),(26,'Can change Админка - Задача',7,'change_tasks'),(27,'Can delete Админка - Задача',7,'delete_tasks'),(28,'Can view Админка - Задача',7,'view_tasks'),(29,'Can add custom user',11,'add_customuser'),(30,'Can change custom user',11,'change_customuser'),(31,'Can delete custom user',11,'delete_customuser'),(32,'Can view custom user',11,'view_customuser'),(33,'Can add Стат.контет - Файл',12,'add_files'),(34,'Can change Стат.контет - Файл',12,'change_files'),(35,'Can delete Стат.контет - Файл',12,'delete_files'),(36,'Can view Стат.контет - Файл',12,'view_files'),(37,'Can add Стат.контент - Блоки',13,'add_blocks'),(38,'Can change Стат.контент - Блоки',13,'change_blocks'),(39,'Can delete Стат.контент - Блоки',13,'delete_blocks'),(40,'Can view Стат.контент - Блоки',13,'view_blocks'),(41,'Can add Стат.контент - Контейнеры',14,'add_containers'),(42,'Can change Стат.контент - Контейнеры',14,'change_containers'),(43,'Can delete Стат.контент - Контейнеры',14,'delete_containers'),(44,'Can view Стат.контент - Контейнеры',14,'view_containers'),(45,'Can add Стат.контент - Линковка меню к контейнерам',15,'add_linkcontainer'),(46,'Can change Стат.контент - Линковка меню к контейнерам',15,'change_linkcontainer'),(47,'Can delete Стат.контент - Линковка меню к контейнерам',15,'delete_linkcontainer'),(48,'Can view Стат.контент - Линковка меню к контейнерам',15,'view_linkcontainer'),(49,'Can add Товары - товар/услуга',16,'add_products'),(50,'Can change Товары - товар/услуга',16,'change_products'),(51,'Can delete Товары - товар/услуга',16,'delete_products'),(52,'Can view Товары - товар/услуга',16,'view_products'),(53,'Can add products cats',17,'add_productscats'),(54,'Can change products cats',17,'change_productscats'),(55,'Can delete products cats',17,'delete_productscats'),(56,'Can view products cats',17,'view_productscats'),(57,'Can add products photos',18,'add_productsphotos'),(58,'Can change products photos',18,'change_productsphotos'),(59,'Can delete products photos',18,'delete_productsphotos'),(60,'Can view products photos',18,'view_productsphotos'),(61,'Can add property',19,'add_property'),(62,'Can change property',19,'change_property'),(63,'Can delete property',19,'delete_property'),(64,'Can view property',19,'view_property'),(65,'Can add properties values',20,'add_propertiesvalues'),(66,'Can change properties values',20,'change_propertiesvalues'),(67,'Can delete properties values',20,'delete_propertiesvalues'),(68,'Can view properties values',20,'view_propertiesvalues'),(69,'Can add products properties',21,'add_productsproperties'),(70,'Can change products properties',21,'change_productsproperties'),(71,'Can delete products properties',21,'delete_productsproperties'),(72,'Can view products properties',21,'view_productsproperties'),(73,'Can add costs types',22,'add_coststypes'),(74,'Can change costs types',22,'change_coststypes'),(75,'Can delete costs types',22,'delete_coststypes'),(76,'Can view costs types',22,'view_coststypes'),(77,'Can add costs',23,'add_costs'),(78,'Can change costs',23,'change_costs'),(79,'Can delete costs',23,'delete_costs'),(80,'Can view costs',23,'view_costs'),(81,'Can add Пользователи - пользователь',24,'add_shopper'),(82,'Can change Пользователи - пользователь',24,'change_shopper'),(83,'Can delete Пользователи - пользователь',24,'delete_shopper'),(84,'Can view Пользователи - пользователь',24,'view_shopper'),(85,'Can add Магазин - Заказ',25,'add_orders'),(86,'Can change Магазин - Заказ',25,'change_orders'),(87,'Can delete Магазин - Заказ',25,'delete_orders'),(88,'Can view Магазин - Заказ',25,'view_orders'),(89,'Can add Магазин - Покупки',27,'add_purchases'),(90,'Can change Магазин - Покупки',27,'change_purchases'),(91,'Can delete Магазин - Покупки',27,'delete_purchases'),(92,'Can view Магазин - Покупки',27,'view_purchases'),(93,'Can add Магазин - Транзакция',28,'add_transactions'),(94,'Can change Магазин - Транзакция',28,'change_transactions'),(95,'Can delete Магазин - Транзакция',28,'delete_transactions'),(96,'Can view Магазин - Транзакция',28,'view_transactions'),(97,'Can add Магазин - Промокод',29,'add_promocodes'),(98,'Can change Магазин - Промокод',29,'change_promocodes'),(99,'Can delete Магазин - Промокод',29,'delete_promocodes'),(100,'Can view Магазин - Промокод',29,'view_promocodes'),(101,'Can add Адреса - адрес объекта',30,'add_address'),(102,'Can change Адреса - адрес объекта',30,'change_address'),(103,'Can delete Адреса - адрес объекта',30,'delete_address'),(104,'Can view Адреса - адрес объекта',30,'view_address'),(105,'Can add Дилеры - Дилер',31,'add_dealer'),(106,'Can change Дилеры - Дилер',31,'change_dealer'),(107,'Can delete Дилеры - Дилер',31,'delete_dealer'),(108,'Can view Дилеры - Дилер',31,'view_dealer');
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$z2Mb2Ah4Y28R$kOOnJSTXh1bKX8A7yKFwEgO/3GE+9cmyCXd1SSnK9tc=','2021-02-13 11:21:50.999485',1,'jocker','','','dkramorov@mail.ru',1,1,'2021-02-02 21:42:08.061384'),(2,'pbkdf2_sha256$150000$m8qHktIFhtyy$d6FeWJYi3mMumHCERr1fuEj1kQJdnAVtmWNc1pBAsxI=',NULL,1,'phil','Ромка','Обухов','',1,1,'2021-02-03 00:08:41.461176');
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
-- Table structure for table `dealers_dealer`
--

DROP TABLE IF EXISTS `dealers_dealer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealers_dealer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img` varchar(255) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `position` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `state` int(11) DEFAULT NULL,
  `parents` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `worktime` varchar(255) DEFAULT NULL,
  `site` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `address_id` int(11) DEFAULT NULL,
  `city` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dealers_dealer_address_id_a1f3a527_fk_addresses_address_id` (`address_id`),
  KEY `dealers_dealer_img_32a1fb21` (`img`),
  KEY `dealers_dealer_created_51d1a8ed` (`created`),
  KEY `dealers_dealer_updated_bb977c54` (`updated`),
  KEY `dealers_dealer_position_5e84a91a` (`position`),
  KEY `dealers_dealer_is_active_d07a0805` (`is_active`),
  KEY `dealers_dealer_state_9398ac52` (`state`),
  KEY `dealers_dealer_parents_01bde26f` (`parents`),
  KEY `dealers_dealer_name_5972c3c2` (`name`),
  KEY `dealers_dealer_worktime_f8b12134` (`worktime`),
  KEY `dealers_dealer_site_58fa6443` (`site`),
  KEY `dealers_dealer_phone_c4860455` (`phone`),
  KEY `dealers_dealer_city_6a84f42d` (`city`),
  CONSTRAINT `dealers_dealer_address_id_a1f3a527_fk_addresses_address_id` FOREIGN KEY (`address_id`) REFERENCES `addresses_address` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=308 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dealers_dealer`
--

LOCK TABLES `dealers_dealer` WRITE;
/*!40000 ALTER TABLE `dealers_dealer` DISABLE KEYS */;
INSERT INTO `dealers_dealer` VALUES (247,NULL,'2021-02-05 01:31:06.285945','2021-02-05 01:31:06.285968',1,1,NULL,NULL,'Electro town','9:00 - 21:00<br>','https://electrotown.ru/<br>','+7 (499) 408-80-88<br>',380,1),(248,NULL,'2021-02-05 01:31:06.301117','2021-02-05 01:31:06.301141',2,1,NULL,NULL,'LuxVelo','с 10:00 до 21:00<br>','luxvelo.ru<br>','+7 (495) 00-44-717<br>',381,1),(249,NULL,'2021-02-05 01:31:06.308910','2021-02-05 01:31:06.308928',3,1,NULL,NULL,'Electro-skuter','09:00 - 20:00<br>','https://electro-skuter.ru/<br>','+7 (495) 481-40-39<br>',382,1),(250,NULL,'2021-02-05 01:31:06.311641','2021-02-05 01:31:06.311658',4,1,NULL,NULL,'Electro-skuter','10:00 - 20:00<br>','https://electro-skuter.ru/<br>','+7 (495) 481-40-39<br>',383,1),(251,NULL,'2021-02-05 01:31:06.314325','2021-02-05 01:31:06.314343',5,1,NULL,NULL,'Giroskutershop.ru','с 10:00 до 21:00<br>','giroskutershop.ru<br>','+7 (495) 795-43-44<br>+7 (977) 653-83 13<br>',384,1),(252,NULL,'2021-02-05 01:31:06.316926','2021-02-05 01:31:06.316943',6,1,NULL,NULL,'Giroskutershop.ru','с 10 до 19<br>','giroskutershop.ru<br>','+7 (495) 795-43-44<br>+7 (977) 653-83-13<br>',385,1),(253,NULL,'2021-02-05 01:31:06.319757','2021-02-05 01:31:06.319774',7,1,NULL,NULL,'Girobay','Пн. – Пт. 9:00–20:00, Сб. – Вс. 11:00–20:00<br>','https://girobay.ru/<br>','+7 (925) 026-44-22<br>+7 (495) 532-69-44<br>',386,1),(254,NULL,'2021-02-05 01:31:06.322432','2021-02-05 01:31:06.322449',8,1,NULL,NULL,'Eko-Bike','Пн.– Пт. 09:00–20:00 Сб. – Вс. 10:00–19:00<br>','https://eko-bike.ru/<br>','+7 (499) 877-13-85<br>',387,1),(255,NULL,'2021-02-05 01:31:06.325006','2021-02-05 01:31:06.325022',9,1,NULL,NULL,'ELECTRON motors','10:00 - 19:00<br>','https://electronmotors.ru/<br>','+7 (968) 870-77-88<br>',388,1),(256,NULL,'2021-02-05 01:31:06.327575','2021-02-05 01:31:06.327593',10,1,NULL,NULL,'Гиротрейд.рф','10:00 - 20:00<br>','https://гиротрейд.рф/<br>','+7 (982) 966-54-60<br>',389,1),(257,NULL,'2021-02-05 01:31:06.330196','2021-02-05 01:31:06.330213',11,1,NULL,NULL,'ЦИМ','10:30 - 19:30<br>','https://cim-pro.ru/<br>','+7 (495) 260-96-20<br>',390,1),(258,NULL,'2021-02-05 01:31:06.332872','2021-02-05 01:31:06.332889',12,1,NULL,NULL,'ElectroStreet','10:00 - 20:00<br>','https://electrostreet.ru/<br>','+7 (968) 570-07-24<br>+7 (495) 215-51-08<br>',391,1),(259,NULL,'2021-02-05 01:31:06.335580','2021-02-05 01:31:06.335597',13,1,NULL,NULL,'GreenWheel','с 10:00 до 20:00<br>','green-wheel.me<br>','8 (499) 113-15-53<br>',392,1),(260,NULL,'2021-02-05 01:31:06.338211','2021-02-05 01:31:06.338228',14,1,NULL,NULL,'Sigvey.ru','09:00 - 19:00<br>','https://sigvey.ru/<br>','+7 (495) 182-12-82<br>',393,1),(261,NULL,'2021-02-05 01:31:06.340749','2021-02-05 01:31:06.340766',15,1,NULL,NULL,'Luxwheel','Пн. – Пт. 9:00–18:00, Сб. – Вс. 12:00–18:00<br>','https://luxwheel.ru/<br>','+7 (985) 226-56-20<br>+7 (499) 455-12-75<br>',394,1),(262,NULL,'2021-02-05 01:31:06.343427','2021-02-05 01:31:06.343444',16,1,NULL,NULL,'Raptor-tv','10:00 - 20:00<br>','https://raptor-tv.ru/<br>','+7 (495) 222-27-33<br>+7 (915) 422-22-27<br>',395,1),(263,NULL,'2021-02-05 01:31:06.346470','2021-02-05 01:31:06.346488',17,1,NULL,NULL,'Zoty','10:00 - 19:00<br>','https://zoty.ru/<br>','+7 (800) 511-36-20<br>+7 (919) 999-88-88<br>',396,1),(264,NULL,'2021-02-05 01:31:06.349174','2021-02-05 01:31:06.349191',18,1,NULL,NULL,'Simargl Elektro','10:00 – 20:00, выходные: 11:00 – 19:00<br>','https://simargl-elektro.ru/<br>','+7 (800) 500-69-96<br>',397,1),(265,NULL,'2021-02-05 01:31:06.351972','2021-02-05 01:31:06.351991',19,1,NULL,NULL,'Электросамокаты в России','09:00 - 21:00<br>','https://electrosamokat-russia.ru/<br>','+7 (495) 021-65-56<br>',398,1),(266,NULL,'2021-02-05 01:31:06.354626','2021-02-05 01:31:06.354643',20,1,NULL,NULL,'Girosmart','10:00 - 21:00<br>','https://Girosmart.ru/<br>','+7(495)150-11-10<br>',399,1),(267,NULL,'2021-02-05 01:31:06.357186','2021-02-05 01:31:06.357204',21,1,NULL,NULL,'Lux velo','10:00 - 21:00 (будни), 11:00 - 19:00 (выходные)<br>','https://luxvelo.ru/<br>','+7 (495) 004-47-17<br>',400,1),(268,NULL,'2021-02-05 01:31:06.359758','2021-02-05 01:31:06.359776',22,1,NULL,NULL,'ElectroStreet','10:00 - 20:00<br>','samara.electrostreet.ru<br>','+7 (846) 955-00-09<br>+7 (927) 006-45-99<br>',401,2),(269,NULL,'2021-02-05 01:31:06.362874','2021-02-05 01:31:06.362892',23,1,NULL,NULL,'Electro town','9:00 - 20:00<br>','https://samara.electrotown.ru/<br>','+7 (846) 215-08-89<br>',402,2),(270,NULL,'2021-02-05 01:31:06.365670','2021-02-05 01:31:06.365687',24,1,NULL,NULL,'ElectroSamokaty','10:00 - 20:00<br>','https://es-omsk.ru<br>','+7(913)633‒26‒70<br>',403,3),(271,NULL,'2021-02-05 01:31:06.368255','2021-02-05 01:31:06.368272',25,1,NULL,NULL,'Elektro-mall.ru','10:00 - 20:00<br>','https://elektro-mall.ru/<br>','+7 (843) 292-57-18<br>',404,4),(272,NULL,'2021-02-05 01:31:06.371000','2021-02-05 01:31:06.371018',26,1,NULL,NULL,'Electrotexas','10:00 - 20:00<br>','https://electrotexas.ru/<br>','+7 (917) 252-35-77<br>',405,4),(273,NULL,'2021-02-05 01:31:06.373686','2021-02-05 01:31:06.373703',27,1,NULL,NULL,'Electro town','9:00 - 20:00<br>','https://kazan.electrotown.ru/<br>','+7 (8432) 168-420<br>',406,4),(274,NULL,'2021-02-05 01:31:06.376568','2021-02-05 01:31:06.376590',28,1,NULL,NULL,'Электросамокаты в России','09:00 - 21:00<br>','https://spb.electrosamokat-russia.ru/<br>','+7 (812) 413-99-39<br>',407,5),(275,NULL,'2021-02-05 01:31:06.379802','2021-02-05 01:31:06.379819',29,1,NULL,NULL,'Zoty','10:00 - 19:00<br>','https://zoty.ru/<br>','+7 (800) 511-36-20<br>+7 (919) 999-88-88<br>',408,5),(276,NULL,'2021-02-05 01:31:06.382416','2021-02-05 01:31:06.382434',30,1,NULL,NULL,'Electro-skuter','10:00 - 20:00<br>','https://electro-skuter.ru/<br>','+7 (812) 200-49-87<br>',409,5),(277,NULL,'2021-02-05 01:31:06.385219','2021-02-05 01:31:06.385238',31,1,NULL,NULL,'Smart-техники','с 10:00 до 21:00<br>','смарт-техника.рф<br>','8 (812) 509-23-43<br>8 (812) 602-74-02<br>8 (812) 603-77-08<br>',410,5),(278,NULL,'2021-02-05 01:31:06.387931','2021-02-05 01:31:06.387948',32,1,NULL,NULL,'Smart-техники','с 10:00 до 21:00<br>','смарт-техника.рф<br>','8 (812) 509-23-43<br>8 (812) 602-74-02<br>8 (812) 603-77-08<br>',411,5),(279,NULL,'2021-02-05 01:31:06.390529','2021-02-05 01:31:06.390546',33,1,NULL,NULL,'Smart-техники','с 10:00 до 21:00<br>','смарт-техника.рф<br>','8 (812) 509-23-43<br>8 (812) 602-74-02<br>8 (812) 603-77-08<br>',412,5),(280,NULL,'2021-02-05 01:31:06.393177','2021-02-05 01:31:06.393194',34,1,NULL,NULL,'Sky run','10:00 - 21:00<br>','https://electrogroup24.ru/<br>','8 (800) 301-58-71<br>',413,5),(281,NULL,'2021-02-05 01:31:06.395829','2021-02-05 01:31:06.395847',35,1,NULL,NULL,'Electro town','10:00 - 21:00<br>','https://spb.electrotown.ru/<br>','+7 (812) 429-70-20<br>',414,5),(282,NULL,'2021-02-05 01:31:06.398477','2021-02-05 01:31:06.398494',36,1,NULL,NULL,'Scooters-Zone','10:00 - 22:00<br>','https://scooters-zone.ru/<br>','+7 (862) 259-20-10<br>+7 (918) 600-35-00<br>',415,6),(283,NULL,'2021-02-05 01:31:06.401076','2021-02-05 01:31:06.401093',37,1,NULL,NULL,'Scooters-Zone','10:00 - 22:00<br>','https://scooters-zone.ru/<br>','+7 (862) 259-20-10<br>+7 (918) 600-35-00<br>',416,6),(284,NULL,'2021-02-05 01:31:06.405175','2021-02-05 01:31:06.405193',38,1,NULL,NULL,'King Toys','09:00 - 19:00<br>','https://kingtoys31.ru/<br>','+7 (915) 565-00-01<br>+7 (4722) 411-579<br>',417,7),(285,NULL,'2021-02-05 01:31:06.408363','2021-02-05 01:31:06.408381',39,1,NULL,NULL,'Гироскутер 43','12:00 - 19:00, Вс. вых.<br>','https://techno43.ru/<br>','+7 (922) 950-43-43<br>',418,8),(286,NULL,'2021-02-05 01:31:06.411286','2021-02-05 01:31:06.411309',40,1,NULL,NULL,'Energy Shop','10:00 - 18:00<br>','https://energy-shop43.ru/<br>','+7 (996) 896-42-74<br>',419,8),(287,NULL,'2021-02-05 01:31:06.414028','2021-02-05 01:31:06.414045',41,1,NULL,NULL,'Zoty','10:00 - 19:00<br>','https://zoty.ru/<br>','+7 (800) 511-36-20<br>+7 (919) 999-88-88<br>',420,9),(288,NULL,'2021-02-05 01:31:06.416617','2021-02-05 01:31:06.416634',42,1,NULL,NULL,'Electro town','9:00 - 20:00<br>','https://ekb.electrotown.ru/<br>','+7 (343) 339-46-80<br>',421,9),(289,NULL,'2021-02-05 01:31:06.419592','2021-02-05 01:31:06.419609',43,1,NULL,NULL,'Gyroperm','Пн. – Пт. 10:30–20:00, Сб. – Вс. 11:00–19:00<br>','https://gyroperm.ru/<br>','+7 (342) 204-77-99<br>',422,10),(290,NULL,'2021-02-05 01:31:06.422192','2021-02-05 01:31:06.422209',44,1,NULL,NULL,'Rocket','с 10:00 до 20:00<br>','rocket24.ru<br>','+7 (342) 277-27-44<br>',423,10),(291,NULL,'2021-02-05 01:31:06.424786','2021-02-05 01:31:06.424803',45,1,NULL,NULL,'Wiseshop','10:00 - 20:00<br>','https://wiseshop.ru/<br>','+7 (915) 500-20-00<br>',424,11),(292,NULL,'2021-02-05 01:31:06.427407','2021-02-05 01:31:06.427424',46,1,NULL,NULL,'Sky run','10:00 - 21:00<br>','https://vn.sky-run.ru/<br>','+7(8162) 68-13-99<br>',425,12),(293,NULL,'2021-02-05 01:31:06.430045','2021-02-05 01:31:06.430062',47,1,NULL,NULL,'Sky run','10:00 - 21:00<br>','https://krsk.sky-run.ru/<br>','+7 (391) 989-77-00<br>',426,13),(294,NULL,'2021-02-05 01:31:06.432669','2021-02-05 01:31:06.432686',48,1,NULL,NULL,'Smart Gifts','с 09:00 до 22:00<br>','smart-gifts.ru<br>','8 (968) 266-65-06<br>',427,14),(295,NULL,'2021-02-05 01:31:06.435390','2021-02-05 01:31:06.435408',49,1,NULL,NULL,'Smart Gifts','с 09:00 до 22:00<br>','smart-gifts.ru<br>','8 (968) 266-65-08<br>',428,14),(296,NULL,'2021-02-05 01:31:06.438147','2021-02-05 01:31:06.438164',50,1,NULL,NULL,'Технологии Будущего','10:00 - 20:00<br>','https://tbrussia.ru/<br>','+7 (953) 194-57-57<br>',429,15),(297,NULL,'2021-02-05 01:31:06.442365','2021-02-05 01:31:06.442383',51,1,NULL,NULL,'Dindi','10:00 - 19:30<br>','https://dindi.ru/<br>','+7 (978) 737-78-89<br>',430,16),(298,NULL,'2021-02-05 01:31:06.445019','2021-02-05 01:31:06.445036',52,1,NULL,NULL,'Dindi','10:00 - 19:30<br>','https://dindi.ru/<br>','+7 (978) 80-55-600<br>',431,17),(299,NULL,'2021-02-05 01:31:06.447568','2021-02-05 01:31:06.447585',53,1,NULL,NULL,'Electro town','9:00 - 20:00<br>','https://www.ufa.electrotown.ru/<br>','+7 (347) 258-89-18<br>',432,18),(300,NULL,'2021-02-05 01:31:06.450154','2021-02-05 01:31:06.450172',54,1,NULL,NULL,'Electro town','10:00 - 21:00<br>','https://voronezh.electrotown.ru/<br>','+7 (473) 200-67-93<br>',433,19),(301,NULL,'2021-02-05 01:31:06.452928','2021-02-05 01:31:06.452945',55,1,NULL,NULL,'Eco drive 45','10:00 - 19:00<br>','http://ecodrive45.ru/<br>','+7 (996) 557-14-99<br>',434,20),(302,NULL,'2021-02-05 01:31:06.455496','2021-02-05 01:31:06.455512',56,1,NULL,NULL,'ElectroTown','10:00 - 21:00<br>','krasnodar.electrotown.ru<br>','+7 (861) 204-07-35<br>',435,21),(303,NULL,'2021-02-05 01:31:06.458054','2021-02-05 01:31:06.458070',57,1,NULL,NULL,'Zoty','10:00 - 19:00<br>','https://zoty.ru/<br>','+7 (800) 511-36-20<br>+7 (919) 999-88-88<br>',436,21),(304,NULL,'2021-02-05 01:31:06.460684','2021-02-05 01:31:06.460702',58,1,NULL,NULL,'ELECTROCART','с 10:00 до 18:00<br>','Electrocart.ru<br>','+7 (910) 790-99-68<br>',437,22),(305,NULL,'2021-02-05 01:31:06.463423','2021-02-05 01:31:06.463440',59,1,NULL,NULL,'Mashinki-nn','с 10:00 до 20:00<br>','mashinki-nn.ru<br>','+7 (831) 266-45-37<br>',438,22),(306,NULL,'2021-02-05 01:31:06.466064','2021-02-05 01:31:06.466081',60,1,NULL,NULL,'WHITE SIBERIA','вт. – сб. 11.00-19.00<br>','https://white-siberia.by/<br>','+375 33 340-15-41<br>',439,23),(307,NULL,'2021-02-05 01:31:06.469184','2021-02-05 01:31:06.469204',61,1,NULL,NULL,'WHITE SIBERIA','10:00 - 18:00<br>','save.satu.kz<br>','+7 771 129-02-02<br>',440,24);
/*!40000 ALTER TABLE `dealers_dealer` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (30,'addresses','address'),(2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(31,'dealers','dealer'),(12,'files','files'),(13,'flatcontent','blocks'),(14,'flatcontent','containers'),(15,'flatcontent','linkcontainer'),(11,'login','customuser'),(8,'login','extrafields'),(10,'login','extrainfo'),(9,'login','extravalues'),(6,'main_functions','config'),(7,'main_functions','tasks'),(24,'personal','shopper'),(23,'products','costs'),(22,'products','coststypes'),(16,'products','products'),(17,'products','productscats'),(18,'products','productsphotos'),(21,'products','productsproperties'),(20,'products','propertiesvalues'),(19,'products','property'),(5,'sessions','session'),(25,'shop','orders'),(29,'shop','promocodes'),(27,'shop','purchases'),(28,'shop','transactions'),(26,'shop','wishlist');
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
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'addresses','0001_initial','2021-02-02 21:42:06.546179'),(2,'contenttypes','0001_initial','2021-02-02 21:42:06.723776'),(3,'contenttypes','0002_remove_content_type_name','2021-02-02 21:42:06.747621'),(4,'auth','0001_initial','2021-02-02 21:42:06.902199'),(5,'auth','0002_alter_permission_name_max_length','2021-02-02 21:42:07.028154'),(6,'auth','0003_alter_user_email_max_length','2021-02-02 21:42:07.044614'),(7,'auth','0004_alter_user_username_opts','2021-02-02 21:42:07.052265'),(8,'auth','0005_alter_user_last_login_null','2021-02-02 21:42:07.068615'),(9,'auth','0006_require_contenttypes_0002','2021-02-02 21:42:07.070152'),(10,'auth','0007_alter_validators_add_error_messages','2021-02-02 21:42:07.076854'),(11,'auth','0008_alter_user_username_max_length','2021-02-02 21:42:07.091060'),(12,'auth','0009_alter_user_last_name_max_length','2021-02-02 21:42:07.108636'),(13,'auth','0010_alter_group_name_max_length','2021-02-02 21:42:07.124736'),(14,'auth','0011_update_proxy_permissions','2021-02-02 21:42:07.135305'),(15,'files','0001_initial','2021-02-02 21:42:07.169746'),(16,'files','0002_auto_20191203_2054','2021-02-02 21:42:07.224251'),(17,'files','0003_auto_20200112_1717','2021-02-02 21:42:07.232450'),(18,'files','0004_auto_20200402_2127','2021-02-02 21:42:07.250965'),(19,'files','0005_auto_20200809_1025','2021-02-02 21:42:07.254217'),(20,'flatcontent','0001_initial','2021-02-02 21:42:07.334373'),(21,'flatcontent','0002_auto_20190825_1730','2021-02-02 21:42:07.621871'),(22,'flatcontent','0003_auto_20191203_2054','2021-02-02 21:42:07.657373'),(23,'flatcontent','0004_blocks_html','2021-02-02 21:42:07.680409'),(24,'flatcontent','0005_auto_20200112_1717','2021-02-02 21:42:07.712638'),(25,'flatcontent','0006_auto_20200314_1638','2021-02-02 21:42:07.718359'),(26,'flatcontent','0007_auto_20200402_2127','2021-02-02 21:42:07.828224'),(27,'flatcontent','0008_containers_class_name','2021-02-02 21:42:07.853686'),(28,'flatcontent','0009_blocks_class_name','2021-02-02 21:42:07.887062'),(29,'login','0001_initial','2021-02-02 21:42:08.183102'),(30,'login','0002_auto_20200925_1007','2021-02-02 21:42:08.455578'),(31,'main_functions','0001_initial','2021-02-02 21:42:08.498706'),(32,'main_functions','0002_auto_20191203_2052','2021-02-02 21:42:08.518601'),(33,'main_functions','0003_auto_20200407_1845','2021-02-02 21:42:08.717077'),(34,'personal','0001_initial','2021-02-02 21:42:08.826358'),(35,'personal','0002_auto_20200528_1642','2021-02-02 21:42:08.952591'),(36,'personal','0003_auto_20200616_1707','2021-02-02 21:42:08.963582'),(37,'personal','0004_shopper_ip','2021-02-02 21:42:08.983990'),(38,'products','0001_initial','2021-02-02 21:42:09.030250'),(39,'products','0002_productsphotos','2021-02-02 21:42:09.196016'),(40,'products','0003_auto_20200315_2217','2021-02-02 21:42:09.271435'),(41,'products','0004_auto_20200316_2329','2021-02-02 21:42:09.319810'),(42,'products','0005_auto_20200402_2127','2021-02-02 21:42:09.416795'),(43,'products','0006_auto_20200402_2351','2021-02-02 21:42:09.561939'),(44,'products','0007_property_ptype','2021-02-02 21:42:09.583732'),(45,'products','0008_property_code','2021-02-02 21:42:09.606768'),(46,'products','0009_property_measure','2021-02-02 21:42:09.630178'),(47,'products','0010_auto_20200623_1629','2021-02-02 21:42:09.676209'),(48,'products','0011_auto_20200627_1353','2021-02-02 21:42:09.828781'),(49,'products','0012_auto_20201212_1449','2021-02-02 21:42:09.887747'),(50,'products','0013_property_search_facet','2021-02-02 21:42:09.920243'),(51,'sessions','0001_initial','2021-02-02 21:42:09.941779'),(52,'shop','0001_initial','2021-02-02 21:42:10.033638'),(53,'shop','0002_auto_20200618_0000','2021-02-02 21:42:10.367387'),(54,'shop','0003_auto_20200621_1346','2021-02-02 21:42:10.610522'),(55,'shop','0004_purchases_cost_type','2021-02-02 21:42:10.676439'),(56,'shop','0005_transactions','2021-02-02 21:42:10.728498'),(57,'shop','0006_auto_20200719_0003','2021-02-02 21:42:10.905211'),(58,'shop','0007_auto_20200719_0146','2021-02-02 21:42:11.052724'),(59,'shop','0008_auto_20201026_1359','2021-02-02 21:42:11.097401'),(60,'shop','0009_auto_20201212_1539','2021-02-02 21:42:11.163598'),(61,'main_functions','0004_config_user','2021-02-03 17:50:45.148299'),(62,'dealers','0001_initial','2021-02-04 00:33:09.710881'),(63,'dealers','0002_dealer_city','2021-02-04 00:41:07.879869'),(64,'shop','0010_auto_20210208_1858','2021-02-09 18:17:35.385678'),(65,'shop','0011_orders_external_number','2021-02-09 18:17:35.510928');
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
INSERT INTO `django_session` VALUES ('13uoj013kpdbzllan4pctpzkyhor4whe','NjFjMjNjYTAyNmE5NjU0MTc3ODkyMWNlN2ViM2MwM2RmZjIxYTgyYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjQ2NjFlNThkMTdlMGYzZjRhOWQ2ZjA1NDBmZmJlZGJjOTgzOTA5ZjgifQ==','2021-02-27 11:21:51.008550'),('fsk57ydat7qhg9ovhposxzesljtdtsn1','NjFjMjNjYTAyNmE5NjU0MTc3ODkyMWNlN2ViM2MwM2RmZjIxYTgyYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjQ2NjFlNThkMTdlMGYzZjRhOWQ2ZjA1NDBmZmJlZGJjOTgzOTA5ZjgifQ==','2021-02-16 22:11:32.378706'),('grb1gj545hkmhbsb1nnp632jni6rmmko','NjFjMjNjYTAyNmE5NjU0MTc3ODkyMWNlN2ViM2MwM2RmZjIxYTgyYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjQ2NjFlNThkMTdlMGYzZjRhOWQ2ZjA1NDBmZmJlZGJjOTgzOTA5ZjgifQ==','2021-02-18 16:18:16.555537'),('p8pu6iet4odvryhvvquccq05d5vhbm0y','NjFjMjNjYTAyNmE5NjU0MTc3ODkyMWNlN2ViM2MwM2RmZjIxYTgyYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjQ2NjFlNThkMTdlMGYzZjRhOWQ2ZjA1NDBmZmJlZGJjOTgzOTA5ZjgifQ==','2021-02-17 18:01:51.669853'),('vq0iuiu2lrf86fn3w8wpuwi5kqsfis8e','NjFjMjNjYTAyNmE5NjU0MTc3ODkyMWNlN2ViM2MwM2RmZjIxYTgyYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjQ2NjFlNThkMTdlMGYzZjRhOWQ2ZjA1NDBmZmJlZGJjOTgzOTA5ZjgifQ==','2021-02-23 18:18:02.188229'),('z3tsc01o7iw5hnz9lny5l3l8tgxaguv1','NjFjMjNjYTAyNmE5NjU0MTc3ODkyMWNlN2ViM2MwM2RmZjIxYTgyYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYXBwcy5sb2dpbi5iYWNrZW5kLk15QmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjQ2NjFlNThkMTdlMGYzZjRhOWQ2ZjA1NDBmZmJlZGJjOTgzOTA5ZjgifQ==','2021-02-19 18:50:20.257795');
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
) ENGINE=InnoDB AUTO_INCREMENT=429 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_blocks`
--

LOCK TABLES `flatcontent_blocks` WRITE;
/*!40000 ALTER TABLE `flatcontent_blocks` DISABLE KEYS */;
INSERT INTO `flatcontent_blocks` VALUES (1,NULL,'2021-02-02 22:12:05.730236','2021-02-02 22:12:05.730260',1,1,3,'','Логотип','Добро пожаловать, на наш сайт','/','logo',1,0,NULL,NULL,NULL,NULL,NULL),(2,NULL,'2021-02-02 22:12:05.744248','2021-02-02 22:26:04.728646',2,1,1,'','Телефон','','tel:79628848888','phone',1,0,'','','','+7 962 884-88-88',''),(3,NULL,'2021-02-02 22:12:05.747325','2021-02-02 22:12:05.747349',3,1,3,'','Адрес',NULL,NULL,'address',1,0,NULL,NULL,NULL,'г. Иркутск ул. Советская 32а офис 5',NULL),(4,NULL,'2021-02-02 22:12:05.750143','2021-02-02 22:12:05.750166',4,1,3,'','Email',NULL,NULL,'email',1,0,NULL,NULL,NULL,'test@test.ru',NULL),(5,NULL,'2021-02-02 22:12:05.752986','2021-02-02 22:12:05.753010',5,1,3,'','Режим работы',NULL,NULL,'worktime',1,0,NULL,NULL,NULL,'пн-пт 9:00 - 18:00<br>сб-вс 10:00 - 17:00',NULL),(6,NULL,'2021-02-02 22:12:05.755982','2021-02-10 22:07:26.125112',6,1,1,'','Copyright','','','copyright',1,0,'','','','<p>© 2014 - 2021 White Siberia, Все права защищены</p>',''),(7,NULL,'2021-02-02 22:12:05.758769','2021-02-02 22:12:05.758790',7,1,3,'','Сообщества',NULL,NULL,'social',1,0,NULL,NULL,NULL,NULL,NULL),(11,NULL,'2021-02-02 22:12:05.770619','2021-02-09 19:36:58.706376',11,1,1,'_7','whatsapp','','https://wa.me/79628848888','whatsapp',1,1,'','','','',''),(30,NULL,'2021-02-02 22:13:02.421267','2021-02-03 20:08:53.662068',29,1,4,'','О компании','','/o-kompanii/','',2,0,'','','','',''),(31,NULL,'2021-02-02 22:13:05.262591','2021-02-06 18:21:08.544148',30,1,4,'','Каталог','','/cat/','',2,0,'','','','',''),(32,NULL,'2021-02-02 22:13:08.830635','2021-02-05 12:19:04.861507',31,1,4,'','Дилеры','','/dilery/','',2,0,'','','','',''),(33,NULL,'2021-02-02 22:13:12.263029','2021-02-03 21:21:00.666403',32,1,4,'','Контакты','','/kontakty/','',2,0,'','','','',''),(34,NULL,'2021-02-02 22:13:26.425471','2021-02-03 20:04:33.185734',33,1,4,'','Стать дилером','','/stat-dilerom/','',2,0,'','','','',''),(40,'40.jpg','2021-02-02 22:52:37.836663','2021-02-02 23:29:43.418574',38,1,1,'','WS-PRO 2WD','','/','',4,0,'','','','60v 4000w',''),(41,'41.jpg','2021-02-02 22:54:10.814872','2021-02-02 23:29:40.222533',39,1,1,'','WS-PRO MAX+','','/','',4,0,'','','','60v 3000w',''),(42,'42.png','2021-02-02 22:54:24.785591','2021-02-02 23:29:36.576233',40,1,1,'','WS-TAIGA','','/','',4,0,'','','','48v 800w',''),(43,'40.jpg','2021-02-02 23:48:34.793658','2021-02-02 23:48:34.793680',38,1,1,'','WS-PRO 2WD','','/','',5,0,'','','','60v 4000w',''),(44,'41.jpg','2021-02-02 23:48:34.797028','2021-02-02 23:48:34.797047',39,1,1,'','WS-PRO MAX+','','/','',5,0,'','','','60v 3000w',''),(45,'42.png','2021-02-02 23:48:34.804901','2021-02-02 23:48:34.804921',40,1,1,'','WS-TAIGA','','/','',5,0,'','','','48v 800w',''),(46,NULL,'2021-02-03 00:03:46.181225','2021-02-03 00:03:46.181245',41,1,4,'','О компании',NULL,'/o-kompanii/',NULL,3,0,NULL,NULL,NULL,NULL,NULL),(47,NULL,'2021-02-03 00:03:55.070642','2021-02-12 16:18:35.841643',42,1,4,'','Каталог','','/cat/','',3,0,'','','','',''),(48,NULL,'2021-02-03 00:03:58.825663','2021-02-03 00:03:58.825681',43,1,4,'','Дилеры',NULL,'/dilery/',NULL,3,0,NULL,NULL,NULL,NULL,NULL),(49,NULL,'2021-02-03 00:04:02.270327','2021-02-03 00:04:02.270348',44,1,4,'','Контакты',NULL,'/kontakty/',NULL,3,0,NULL,NULL,NULL,NULL,NULL),(50,NULL,'2021-02-03 00:04:15.996343','2021-02-03 00:04:15.996362',45,1,4,'','Стать дилером',NULL,'/stat-dilerom/',NULL,3,0,NULL,NULL,NULL,NULL,NULL),(51,NULL,'2021-02-03 18:02:09.348591','2021-02-03 18:28:56.461054',46,1,1,'','2020 год','Смотреть все','/','',6,0,'','','','<p><b>Расширение дилерской сети и производственных мощностей. </b></p>\r\n<p>По итогам 2020 года компания WHITE SIBERIA продала на рынке КНР свыше\r\n 3500 единиц электротранспорта, а на рынке стран СНГ - свыше 10 000. </p>\r\n<p>В странах СНГ компанию представляют 26 дилеров. В 2020 году состоялся выход на рынки Казахстана и Украины.</p>\r\n<p>Количество сборочных линий на производстве электротранспорта было увеличено до 4.</p>',''),(52,NULL,'2021-02-03 18:02:10.256503','2021-02-03 18:03:13.925089',47,1,1,'','2019 год','','','',6,0,'','','','<p><b>Масштабирование компании, повышение спроса и завоевание новых рынков сбыта. </b></p>\r\n<p>За 2019 год на территории КНР было продано свыше 3000 единиц \r\nэлектротранспорта. Это позволило компании масштабироваться и выйти на \r\nновые рынки сбыта. В начале года был открыт офис в Сочи, а буквально \r\nчерез 6 месяцев - в Москве и Минске.</p>',''),(53,NULL,'2021-02-03 18:02:11.020554','2021-02-03 18:03:40.766257',48,1,1,'','2018 год','','','',6,0,'','','','<p><b>Мощный рывок в развитии компании и выход в топ.</b></p>\r\n<p>В начале 2018 года состоялось открытие первого офиса и магазина \r\nэлектротранспорта в Шанхае, а к концу года WHITE SIBERIA вошла в топ \r\nкомпаний по продажам электротранспорта иностранцам, проживающим на \r\nтерритории КНР.</p>',''),(54,NULL,'2021-02-03 18:02:12.311947','2021-02-03 18:09:12.249788',49,1,1,'','2014 год','','','',6,0,'','','','<p><b>Год основания компании WHITE SIBERIA.</b></p>\r\n<p>В 2014 году в Шанхае была основана компания, которая до 2017 года \r\nзанималась продажей запчастей и комплектующих для коммерческого \r\nтранспорта.</p>',''),(55,NULL,'2021-02-03 18:29:41.968655','2021-02-03 18:29:41.968674',46,1,1,'','2020 год','Смотреть все','/','',7,0,'','','','<p><b>Расширение дилерской сети и производственных мощностей. </b></p>\r\n<p>По итогам 2020 года компания WHITE SIBERIA продала на рынке КНР свыше\r\n 3500 единиц электротранспорта, а на рынке стран СНГ - свыше 10 000. </p>\r\n<p>В странах СНГ компанию представляют 26 дилеров. В 2020 году состоялся выход на рынки Казахстана и Украины.</p>\r\n<p>Количество сборочных линий на производстве электротранспорта было увеличено до 4.</p>',''),(56,NULL,'2021-02-03 18:29:41.969609','2021-02-03 18:29:41.969625',47,1,1,'','2019 год','','','',7,0,'','','','<p><b>Масштабирование компании, повышение спроса и завоевание новых рынков сбыта. </b></p>\r\n<p>За 2019 год на территории КНР было продано свыше 3000 единиц \r\nэлектротранспорта. Это позволило компании масштабироваться и выйти на \r\nновые рынки сбыта. В начале года был открыт офис в Сочи, а буквально \r\nчерез 6 месяцев - в Москве и Минске.</p>',''),(57,NULL,'2021-02-03 18:29:41.971010','2021-02-03 18:29:41.971028',48,1,1,'','2018 год','','','',7,0,'','','','<p><b>Мощный рывок в развитии компании и выход в топ.</b></p>\r\n<p>В начале 2018 года состоялось открытие первого офиса и магазина \r\nэлектротранспорта в Шанхае, а к концу года WHITE SIBERIA вошла в топ \r\nкомпаний по продажам электротранспорта иностранцам, проживающим на \r\nтерритории КНР.</p>',''),(58,NULL,'2021-02-03 18:29:41.971891','2021-02-03 18:29:41.971908',49,1,1,'','2014 год','','','',7,0,'','','','<p><b>Год основания компании WHITE SIBERIA.</b></p>\r\n<p>В 2014 году в Шанхае была основана компания, которая до 2017 года \r\nзанималась продажей запчастей и комплектующих для коммерческого \r\nтранспорта.</p>',''),(59,'banner.png','2021-02-03 18:58:57.644976','2021-02-10 19:00:26.236080',50,1,1,'','В семью!','Подробнее','/','',8,0,'','','','<p>Электротранспорт под брендом WHITE SIBERIA – это качество, \r\nнадежность, стильный дизайн и приемлемая цена. Именно поэтому наша \r\nдилерская сеть стремительно растет, а ассортимент техники на витринах \r\nмагазинов в России и странах СНГ – расширяется.</p>\r\n						<p>Если Вы хотите стать участником нашей дилерской сети и \r\nприсоединиться к выполнению нашей миссии – заполните форму, и мы \r\nобязательно свяжемся с Вами.</p>',''),(60,'banner.png','2021-02-03 19:33:12.375995','2021-02-10 19:00:35.548845',50,1,1,'','В семью!','Подробнее','/','',9,0,'','','','<p>Электротранспорт под брендом WHITE SIBERIA – это качество, \r\nнадежность, стильный дизайн и приемлемая цена. Именно поэтому наша \r\nдилерская сеть стремительно растет, а ассортимент техники на витринах \r\nмагазинов в России и странах СНГ – расширяется.</p>\r\n						<p>Если Вы хотите стать участником нашей дилерской сети и \r\nприсоединиться к выполнению нашей миссии – заполните форму, и мы \r\nобязательно свяжемся с Вами.</p>',''),(61,NULL,'2021-02-03 19:48:18.050345','2021-02-03 19:48:30.152546',51,1,1,'','Описание','','','',10,0,'','','','<p>Если Вы хотите стать участником нашей дилерской сети и \r\nпопуляризировать электротранспорт вместе с нами – заполните форму, и мы \r\nобязательно свяжемся с Вами в ближайшее время. </p>\r\n<p>В графе «Дополнительные сведения» просим Вас указать следующую информацию: </p>\r\n<p>Есть ли у Вас опыт продаж или обслуживания электротранспорта?</p>\r\n<p>Вы планируете продажи онлайн или оффлайн? </p>\r\n<p>Есть ли у Вас розничная точка продаж? </p>\r\n<p>Укажите Ваш сайт (если есть).</p>\r\n<p>Будем рады поработать вместе с Вами!</p>',''),(62,NULL,'2021-02-03 19:55:42.089195','2021-02-03 19:56:50.248257',52,1,1,'','Политика в отношении обработки персональных данных','','','',11,0,'','','','<h3>1. Общие положения</h3>\r\n<p>Настоящая политика обработки персональных данных составлена в \r\nсоответствии с требованиями Федерального закона от 27.07.2006. №152-ФЗ \r\n«О персональных данных» и определяет порядок обработки персональных \r\nданных и меры по обеспечению безопасности персональных данных, \r\nпредпринимаемые ИП Соболев И.П. (далее – Оператор).</p>\r\n<ul><li>1.1. Оператор ставит своей важнейшей целью и условием осуществления\r\n своей деятельности соблюдение прав и свобод человека и гражданина при \r\nобработке его персональных данных, в том числе защиты прав на \r\nнеприкосновенность частной жизни, личную и семейную тайну.</li><li>1.2. Настоящая политика Оператора в отношении обработки \r\nперсональных данных (далее – Политика) применяется ко всей информации, \r\nкоторую Оператор может получить о посетителях <a href=\"https://white-siberia.com/\">веб-сайта</a>.</li></ul>\r\n<h3>2. Основные понятия, используемые в Политике</h3>\r\n<ul><li>2.1. Автоматизированная обработка персональных данных – обработка персональных данных с помощью средств вычислительной техники;</li><li>2.2. Блокирование персональных данных – временное прекращение \r\nобработки персональных данных (за исключением случаев, если обработка \r\nнеобходима для уточнения персональных данных);</li><li>2.3. Веб-сайт – совокупность графических и информационных \r\nматериалов, а также программ для ЭВМ и баз данных, обеспечивающих их \r\nдоступность в сети интернет по сетевому адресу <a href=\"https://white-siberia.com/\">https://www.white-siberia.com/</a>;</li><li>2.4. Информационная система персональных данных — совокупность \r\nсодержащихся в базах данных персональных данных, и обеспечивающих их \r\nобработку информационных технологий и технических средств;</li><li>2.5. Обезличивание персональных данных — действия, в результате \r\nкоторых невозможно определить без использования дополнительной \r\nинформации принадлежность персональных данных конкретному Пользователю \r\nили иному субъекту персональных данных;</li><li>2.6. Обработка персональных данных – любое действие (операция) или \r\nсовокупность действий (операций), совершаемых с использованием средств \r\nавтоматизации или без использования таких средств с персональными \r\nданными, включая сбор, запись, систематизацию, накопление, хранение, \r\nуточнение (обновление, изменение), извлечение, использование, передачу \r\n(распространение, предоставление, доступ), обезличивание, блокирование, \r\nудаление, уничтожение персональных данных;</li><li>2.7. Оператор – государственный орган, муниципальный орган, \r\nюридическое или физическое лицо, самостоятельно или совместно с другими \r\nлицами организующие и (или) осуществляющие обработку персональных \r\nданных, а также определяющие цели обработки персональных данных, состав \r\nперсональных данных, подлежащих обработке, действия (операции), \r\nсовершаемые с персональными данными;</li><li>2.8. Персональные данные – любая информация, относящаяся прямо или косвенно к определенному или определяемому Пользователю <a href=\"https://white-siberia.com/\">веб-сайта</a>;</li><li>2.9. Пользователь – любой посетитель <a href=\"https://white-siberia.com/\">веб-сайта</a>;</li><li>2.10. Предоставление персональных данных – действия, направленные \r\nна раскрытие персональных данных определенному лицу или определенному \r\nкругу лиц;</li><li>2.11. Распространение персональных данных – любые действия, \r\nнаправленные на раскрытие персональных данных неопределенному кругу лиц \r\n(передача персональных данных) или на ознакомление с персональными \r\nданными неограниченного круга лиц, в том числе обнародование \r\nперсональных данных в средствах массовой информации, размещение в \r\nинформационно-телекоммуникационных сетях или предоставление доступа к \r\nперсональным данным каким-либо иным способом;</li><li>2.12. Трансграничная передача персональных данных – передача \r\nперсональных данных на территорию иностранного государства органу власти\r\n иностранного государства, иностранному физическому или иностранному \r\nюридическому лицу;</li><li>2.13. Уничтожение персональных данных – любые действия, в \r\nрезультате которых персональные данные уничтожаются безвозвратно с \r\nневозможностью дальнейшего восстановления содержания персональных данных\r\n в информационной системе персональных данных и (или) уничтожаются \r\nматериальные носители персональных данных.</li></ul>\r\n<h3>3. Оператор может обрабатывать следующие персональные данные Пользователя</h3>\r\n<ul><li>3.1. Фамилия, имя, отчество;</li><li>3.2. Электронный адрес;</li><li>3.3. Номера телефонов;</li><li>3.4. Название организации;</li><li>3.5. Также на сайте происходит сбор и обработка обезличенных данных\r\n о посетителях (в т.ч. файлов «cookie») с помощью сервисов \r\nинтернет-статистики (Яндекс Метрика и Гугл Аналитика и других).</li><li>3.6. Вышеперечисленные данные далее по тексту Политики объединены общим понятием Персональные данные.</li></ul>\r\n<h3>4. Цели обработки персональных данных</h3>\r\n<ul><li>4.1. Цель обработки персональных данных Пользователя — заключение, \r\nисполнение и прекращение гражданско-правовых договоров; предоставление \r\nдоступа Пользователю к сервисам, информации и/или материалам, \r\nсодержащимся на веб-сайте.</li><li>4.2. Также Оператор имеет право направлять Пользователю уведомления\r\n о новых продуктах и услугах, специальных предложениях и различных \r\nсобытиях. Пользователь всегда может отказаться от получения \r\nинформационных сообщений, направив Оператору письмо на адрес электронной\r\n почты <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a> с пометкой «Отказ от уведомлений о новых продуктах и услугах и специальных предложениях».</li><li>4.3. Обезличенные данные Пользователей, собираемые с помощью \r\nсервисов интернет-статистики, служат для сбора информации о действиях \r\nПользователей на сайте, улучшения качества сайта и его содержания.</li></ul>\r\n<h3>5. Правовые основания обработки персональных данных</h3>\r\n<ul><li>5.1. Оператор обрабатывает персональные данные Пользователя только в\r\n случае их заполнения и/или отправки Пользователем самостоятельно через \r\nспециальные формы, расположенные на <a href=\"https://white-siberia.com/\">сайте</a>.\r\n Заполняя соответствующие формы и/или отправляя свои персональные данные\r\n Оператору, Пользователь выражает свое согласие с данной Политикой.</li><li>5.2. Оператор обрабатывает обезличенные данные о Пользователе в \r\nслучае, если это разрешено в настройках браузера Пользователя (включено \r\nсохранение файлов «cookie» и использование технологии JavaScript).</li></ul>\r\n<h3>6. Порядок сбора, хранения, передачи и других видов обработки персональных данных</h3>\r\n<p>Безопасность персональных данных, которые обрабатываются Оператором, \r\nобеспечивается путем реализации правовых, организационных и технических \r\nмер, необходимых для выполнения в полном объеме требований действующего \r\nзаконодательства в области защиты персональных данных.</p>\r\n<ul><li>6.1. Оператор обеспечивает сохранность персональных данных и \r\nпринимает все возможные меры, исключающие доступ к персональным данным \r\nнеуполномоченных лиц.</li><li>6.2. Персональные данные Пользователя никогда, ни при каких \r\nусловиях не будут переданы третьим лицам, за исключением случаев, \r\nсвязанных с исполнением действующего законодательства.</li><li>6.3. В случае выявления неточностей в персональных данных, \r\nПользователь может актуализировать их самостоятельно, путем направления \r\nОператору уведомление на адрес электронной почты Оператора <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a> с пометкой «Актуализация персональных данных».</li><li>6.4. Срок обработки персональных данных является неограниченным. \r\nПользователь может в любой момент отозвать свое согласие на обработку \r\nперсональных данных, направив Оператору уведомление посредством \r\nэлектронной почты на электронный адрес Оператора <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a> с пометкой «Отзыв согласия на обработку персональных данных».</li></ul>\r\n<h3>7. Трансграничная передача персональных данных</h3>\r\n<ul><li>7.1. Оператор до начала осуществления трансграничной передачи \r\nперсональных данных обязан убедиться в том, что иностранным \r\nгосударством, на территорию которого предполагается осуществлять \r\nпередачу персональных данных, обеспечивается надежная защита прав \r\nсубъектов персональных данных.</li><li>7.2. Трансграничная передача персональных данных на территории \r\nиностранных государств, не отвечающих вышеуказанным требованиям, может \r\nосуществляться только в случае наличия согласия в письменной форме \r\nсубъекта персональных данных на трансграничную передачу его персональных\r\n данных и/или исполнения договора, стороной которого является субъект \r\nперсональных данных.</li></ul>\r\n<h3>8. Заключительные положения</h3>\r\n<ul><li>8.1. Пользователь может получить любые разъяснения по интересующим \r\nвопросам, касающимся обработки его персональных данных, обратившись к \r\nОператору с помощью электронной почты <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a>.</li><li>8.2. В данном документе будут отражены любые изменения политики \r\nобработки персональных данных Оператором. Политика действует бессрочно \r\nдо замены ее новой версией.</li><li>8.3. Актуальная версия Политики в свободном доступе расположена в сети Интернет на <a href=\"https://white-siberia.com/privacy/\">этой странице</a>.</li></ul>',''),(63,NULL,'2021-02-03 20:00:53.480653','2021-02-03 20:00:53.480671',52,1,1,'','Политика в отношении обработки персональных данных','','','',12,0,'','','','<h3>1. Общие положения</h3>\r\n<p>Настоящая политика обработки персональных данных составлена в \r\nсоответствии с требованиями Федерального закона от 27.07.2006. №152-ФЗ \r\n«О персональных данных» и определяет порядок обработки персональных \r\nданных и меры по обеспечению безопасности персональных данных, \r\nпредпринимаемые ИП Соболев И.П. (далее – Оператор).</p>\r\n<ul><li>1.1. Оператор ставит своей важнейшей целью и условием осуществления\r\n своей деятельности соблюдение прав и свобод человека и гражданина при \r\nобработке его персональных данных, в том числе защиты прав на \r\nнеприкосновенность частной жизни, личную и семейную тайну.</li><li>1.2. Настоящая политика Оператора в отношении обработки \r\nперсональных данных (далее – Политика) применяется ко всей информации, \r\nкоторую Оператор может получить о посетителях <a href=\"https://white-siberia.com/\">веб-сайта</a>.</li></ul>\r\n<h3>2. Основные понятия, используемые в Политике</h3>\r\n<ul><li>2.1. Автоматизированная обработка персональных данных – обработка персональных данных с помощью средств вычислительной техники;</li><li>2.2. Блокирование персональных данных – временное прекращение \r\nобработки персональных данных (за исключением случаев, если обработка \r\nнеобходима для уточнения персональных данных);</li><li>2.3. Веб-сайт – совокупность графических и информационных \r\nматериалов, а также программ для ЭВМ и баз данных, обеспечивающих их \r\nдоступность в сети интернет по сетевому адресу <a href=\"https://white-siberia.com/\">https://www.white-siberia.com/</a>;</li><li>2.4. Информационная система персональных данных — совокупность \r\nсодержащихся в базах данных персональных данных, и обеспечивающих их \r\nобработку информационных технологий и технических средств;</li><li>2.5. Обезличивание персональных данных — действия, в результате \r\nкоторых невозможно определить без использования дополнительной \r\nинформации принадлежность персональных данных конкретному Пользователю \r\nили иному субъекту персональных данных;</li><li>2.6. Обработка персональных данных – любое действие (операция) или \r\nсовокупность действий (операций), совершаемых с использованием средств \r\nавтоматизации или без использования таких средств с персональными \r\nданными, включая сбор, запись, систематизацию, накопление, хранение, \r\nуточнение (обновление, изменение), извлечение, использование, передачу \r\n(распространение, предоставление, доступ), обезличивание, блокирование, \r\nудаление, уничтожение персональных данных;</li><li>2.7. Оператор – государственный орган, муниципальный орган, \r\nюридическое или физическое лицо, самостоятельно или совместно с другими \r\nлицами организующие и (или) осуществляющие обработку персональных \r\nданных, а также определяющие цели обработки персональных данных, состав \r\nперсональных данных, подлежащих обработке, действия (операции), \r\nсовершаемые с персональными данными;</li><li>2.8. Персональные данные – любая информация, относящаяся прямо или косвенно к определенному или определяемому Пользователю <a href=\"https://white-siberia.com/\">веб-сайта</a>;</li><li>2.9. Пользователь – любой посетитель <a href=\"https://white-siberia.com/\">веб-сайта</a>;</li><li>2.10. Предоставление персональных данных – действия, направленные \r\nна раскрытие персональных данных определенному лицу или определенному \r\nкругу лиц;</li><li>2.11. Распространение персональных данных – любые действия, \r\nнаправленные на раскрытие персональных данных неопределенному кругу лиц \r\n(передача персональных данных) или на ознакомление с персональными \r\nданными неограниченного круга лиц, в том числе обнародование \r\nперсональных данных в средствах массовой информации, размещение в \r\nинформационно-телекоммуникационных сетях или предоставление доступа к \r\nперсональным данным каким-либо иным способом;</li><li>2.12. Трансграничная передача персональных данных – передача \r\nперсональных данных на территорию иностранного государства органу власти\r\n иностранного государства, иностранному физическому или иностранному \r\nюридическому лицу;</li><li>2.13. Уничтожение персональных данных – любые действия, в \r\nрезультате которых персональные данные уничтожаются безвозвратно с \r\nневозможностью дальнейшего восстановления содержания персональных данных\r\n в информационной системе персональных данных и (или) уничтожаются \r\nматериальные носители персональных данных.</li></ul>\r\n<h3>3. Оператор может обрабатывать следующие персональные данные Пользователя</h3>\r\n<ul><li>3.1. Фамилия, имя, отчество;</li><li>3.2. Электронный адрес;</li><li>3.3. Номера телефонов;</li><li>3.4. Название организации;</li><li>3.5. Также на сайте происходит сбор и обработка обезличенных данных\r\n о посетителях (в т.ч. файлов «cookie») с помощью сервисов \r\nинтернет-статистики (Яндекс Метрика и Гугл Аналитика и других).</li><li>3.6. Вышеперечисленные данные далее по тексту Политики объединены общим понятием Персональные данные.</li></ul>\r\n<h3>4. Цели обработки персональных данных</h3>\r\n<ul><li>4.1. Цель обработки персональных данных Пользователя — заключение, \r\nисполнение и прекращение гражданско-правовых договоров; предоставление \r\nдоступа Пользователю к сервисам, информации и/или материалам, \r\nсодержащимся на веб-сайте.</li><li>4.2. Также Оператор имеет право направлять Пользователю уведомления\r\n о новых продуктах и услугах, специальных предложениях и различных \r\nсобытиях. Пользователь всегда может отказаться от получения \r\nинформационных сообщений, направив Оператору письмо на адрес электронной\r\n почты <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a> с пометкой «Отказ от уведомлений о новых продуктах и услугах и специальных предложениях».</li><li>4.3. Обезличенные данные Пользователей, собираемые с помощью \r\nсервисов интернет-статистики, служат для сбора информации о действиях \r\nПользователей на сайте, улучшения качества сайта и его содержания.</li></ul>\r\n<h3>5. Правовые основания обработки персональных данных</h3>\r\n<ul><li>5.1. Оператор обрабатывает персональные данные Пользователя только в\r\n случае их заполнения и/или отправки Пользователем самостоятельно через \r\nспециальные формы, расположенные на <a href=\"https://white-siberia.com/\">сайте</a>.\r\n Заполняя соответствующие формы и/или отправляя свои персональные данные\r\n Оператору, Пользователь выражает свое согласие с данной Политикой.</li><li>5.2. Оператор обрабатывает обезличенные данные о Пользователе в \r\nслучае, если это разрешено в настройках браузера Пользователя (включено \r\nсохранение файлов «cookie» и использование технологии JavaScript).</li></ul>\r\n<h3>6. Порядок сбора, хранения, передачи и других видов обработки персональных данных</h3>\r\n<p>Безопасность персональных данных, которые обрабатываются Оператором, \r\nобеспечивается путем реализации правовых, организационных и технических \r\nмер, необходимых для выполнения в полном объеме требований действующего \r\nзаконодательства в области защиты персональных данных.</p>\r\n<ul><li>6.1. Оператор обеспечивает сохранность персональных данных и \r\nпринимает все возможные меры, исключающие доступ к персональным данным \r\nнеуполномоченных лиц.</li><li>6.2. Персональные данные Пользователя никогда, ни при каких \r\nусловиях не будут переданы третьим лицам, за исключением случаев, \r\nсвязанных с исполнением действующего законодательства.</li><li>6.3. В случае выявления неточностей в персональных данных, \r\nПользователь может актуализировать их самостоятельно, путем направления \r\nОператору уведомление на адрес электронной почты Оператора <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a> с пометкой «Актуализация персональных данных».</li><li>6.4. Срок обработки персональных данных является неограниченным. \r\nПользователь может в любой момент отозвать свое согласие на обработку \r\nперсональных данных, направив Оператору уведомление посредством \r\nэлектронной почты на электронный адрес Оператора <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a> с пометкой «Отзыв согласия на обработку персональных данных».</li></ul>\r\n<h3>7. Трансграничная передача персональных данных</h3>\r\n<ul><li>7.1. Оператор до начала осуществления трансграничной передачи \r\nперсональных данных обязан убедиться в том, что иностранным \r\nгосударством, на территорию которого предполагается осуществлять \r\nпередачу персональных данных, обеспечивается надежная защита прав \r\nсубъектов персональных данных.</li><li>7.2. Трансграничная передача персональных данных на территории \r\nиностранных государств, не отвечающих вышеуказанным требованиям, может \r\nосуществляться только в случае наличия согласия в письменной форме \r\nсубъекта персональных данных на трансграничную передачу его персональных\r\n данных и/или исполнения договора, стороной которого является субъект \r\nперсональных данных.</li></ul>\r\n<h3>8. Заключительные положения</h3>\r\n<ul><li>8.1. Пользователь может получить любые разъяснения по интересующим \r\nвопросам, касающимся обработки его персональных данных, обратившись к \r\nОператору с помощью электронной почты <a href=\"mailto:info@white-siberia.com\">info@white-siberia.com</a>.</li><li>8.2. В данном документе будут отражены любые изменения политики \r\nобработки персональных данных Оператором. Политика действует бессрочно \r\nдо замены ее новой версией.</li><li>8.3. Актуальная версия Политики в свободном доступе расположена в сети Интернет на <a href=\"https://white-siberia.com/privacy/\">этой странице</a>.</li></ul>',''),(64,NULL,'2021-02-03 20:01:20.733348','2021-02-03 20:02:14.974730',2,1,4,'','Политика в отношении обработки персональных данных','','/privacy/','',13,0,'','','','',''),(65,NULL,'2021-02-03 20:04:23.367314','2021-02-03 20:04:23.367333',51,1,1,'','Описание','','','',14,0,'','','','<p>Если Вы хотите стать участником нашей дилерской сети и \r\nпопуляризировать электротранспорт вместе с нами – заполните форму, и мы \r\nобязательно свяжемся с Вами в ближайшее время. </p>\r\n<p>В графе «Дополнительные сведения» просим Вас указать следующую информацию: </p>\r\n<p>Есть ли у Вас опыт продаж или обслуживания электротранспорта?</p>\r\n<p>Вы планируете продажи онлайн или оффлайн? </p>\r\n<p>Есть ли у Вас розничная точка продаж? </p>\r\n<p>Укажите Ваш сайт (если есть).</p>\r\n<p>Будем рады поработать вместе с Вами!</p>',''),(66,'about.jpg','2021-02-03 20:07:40.028622','2021-02-03 20:08:22.179506',52,1,1,'','Наша миссия','','','',15,0,'','','','<p>Компания WHITE SIBERIA была основана в 2014 году, и с тех пор наша\r\n цель остается неизменной: сделать комфортный и надежный \r\nэлектротранспорт доступным для каждого жителя России и стран СНГ. </p>\r\n<p>История  WHITE SIBERIA берет свое начало в Шанхае, одном из \r\nкрупнейших городов Китая. Жители Китая  – страны с динамичным развитием \r\nнауки и техники – не мыслят своего существования без электротранспорта: \r\nэлектробайки, электросамокаты и велогибриды уже давно стали неотъемлемой\r\n частью их жизни.   </p>\r\n<p>Миссия компании WHITE SIBERIA – популяризировать электротранспорт на \r\nтерритории России и стран СНГ, раскрыть потенциал этого удобного и \r\nдолговечного транспорта, который прекрасно адаптируется к любым дорогам и\r\n климатическим условиям. </p>\r\n<p>Мы гордимся высоким статусом нашего бренда и доверием многочисленных \r\nпокупателей. Секрет успеха прост: вся наша техника универсальна, \r\nобладает комфортным управлением и стильным дизайном, а дополняет все это\r\n справедливая цена! </p>\r\n<p>Компания WHITE SIBERIA – номер один по продажам электротранспорта в странах СНГ и один из лидеров среди конкурентов в Шанхае. </p>\r\n<p>Выбирая технику WHITE SIBERIA, Вы выбираете надежность, новые возможности, яркие эмоции и безграничную свободу. </p>\r\n<p><b>WHITE SIBERIA. Доступность. Комфорт. Стиль.</b></p>',''),(67,NULL,'2021-02-03 20:52:16.246367','2021-02-03 20:52:38.490298',54,1,1,'','Россия','','','',16,0,'','','','',''),(68,NULL,'2021-02-03 20:52:42.875101','2021-02-03 20:52:42.875123',55,1,1,'','Беларусь',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(69,NULL,'2021-02-03 20:52:45.964422','2021-02-03 20:52:45.964455',56,1,1,'','Китай',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(70,NULL,'2021-02-03 20:52:50.610710','2021-02-03 20:52:50.610730',57,1,1,'','Казахстан',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(71,NULL,'2021-02-03 20:52:59.642162','2021-02-03 21:03:16.062594',58,1,1,'_67','Адреса','','','',16,0,'','','','',''),(72,NULL,'2021-02-03 20:53:08.904377','2021-02-03 20:53:08.904396',59,1,1,'_68','Адреса',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(73,NULL,'2021-02-03 20:53:11.050341','2021-02-03 20:53:11.050360',60,1,1,'_69','Адреса',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(75,NULL,'2021-02-03 20:53:30.974737','2021-02-03 20:53:30.974755',61,1,1,'_70','Адреса',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(76,NULL,'2021-02-03 20:53:45.767420','2021-02-03 20:53:45.767442',62,1,1,'_67','Оптовый отдел',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(77,NULL,'2021-02-03 20:53:48.114919','2021-02-03 20:53:48.114949',63,1,1,'_68','Оптовый отдел',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(78,NULL,'2021-02-03 20:53:50.852793','2021-02-03 20:53:50.852823',64,1,1,'_69','Оптовый отдел',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(79,NULL,'2021-02-03 20:53:52.989677','2021-02-03 20:53:52.989698',65,1,1,'_70','Оптовый отдел',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(80,NULL,'2021-02-03 20:54:03.126550','2021-02-03 20:54:03.126569',66,1,1,'_67','Розничный отдел',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(81,NULL,'2021-02-03 20:54:11.956483','2021-02-03 20:54:11.956505',67,1,1,'_67','Гарантийный отдел',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(82,NULL,'2021-02-03 20:54:30.049241','2021-02-03 20:54:30.049267',68,1,1,'_69','WeChat ID',NULL,NULL,NULL,16,0,NULL,NULL,NULL,NULL,NULL),(83,NULL,'2021-02-03 21:03:27.414773','2021-02-03 21:04:14.337374',69,1,1,'_67_71','Адрес1','','','',16,0,'map-marker','','','г. Москва, дер. Марушкино, ул. Северная\r\n<br>',''),(84,NULL,'2021-02-03 21:03:28.745255','2021-02-03 21:04:17.858913',70,1,1,'_67_71','Адрес2','','','',16,0,'map-marker','','','г. Сочи, Адлерский р-н, ул. Садовая 48',''),(85,NULL,'2021-02-03 21:04:34.217207','2021-02-03 21:04:44.210976',71,1,1,'_68_72','Адрес1','','','',16,0,'map-marker','','','г. Минск Новая Боровая, Авиационная 10',''),(86,NULL,'2021-02-03 21:04:57.606323','2021-02-03 21:05:07.597920',72,1,1,'_69_73','Адрес1','','','',16,0,'map-marker','','','Shanghai Channing district Channing street 398',''),(87,NULL,'2021-02-03 21:05:19.655024','2021-02-03 21:05:34.123970',73,1,1,'_69_73','Адрес2','','','',16,0,'map-marker','','','Shanghai Jiading district JiaSongbei street 6855',''),(88,NULL,'2021-02-03 21:05:50.965278','2021-02-03 21:06:01.821064',74,1,1,'_70_75','Адрес1','','','',16,0,'map-marker','','','г. Караганда, ул. Крылова, д. 101',''),(89,NULL,'2021-02-03 21:12:12.614288','2021-02-03 21:12:33.955364',75,1,1,'_67_76','Телефон','','','',16,0,'phone','','','<a href=\"tel:+79384704147\">+7 938 470 41 47</a>',''),(90,NULL,'2021-02-03 21:12:50.957777','2021-02-03 21:13:36.584360',76,1,1,'_67_76','WhatsApp','','','',16,0,'phone-square','','','+7 938 470 41 47',''),(91,NULL,'2021-02-03 21:13:47.900546','2021-02-03 21:13:58.183112',77,1,1,'_67_76','Email','','','',16,0,'envelope-o','','','opt@white-siberia.com',''),(92,NULL,'2021-02-03 21:14:25.899340','2021-02-03 21:14:45.096690',78,1,1,'_67_80','Телефон','','','',16,0,'phone','','','+7 988 169 16 39',''),(93,NULL,'2021-02-03 21:14:51.618277','2021-02-03 21:15:00.072004',79,1,1,'_67_80','WhatsApp','','','',16,0,'phone-square','','','+7 988 403 85 43',''),(94,NULL,'2021-02-03 21:15:17.367987','2021-02-03 21:15:25.014295',80,1,1,'_67_80','Email','','','',16,0,'envelope-o','','','roznica@white-siberia.com',''),(95,NULL,'2021-02-03 21:15:44.244407','2021-02-03 21:15:53.068776',81,1,1,'_67_81','Телефон','','','',16,0,'phone','','','+7 989 085 87 45',''),(96,NULL,'2021-02-03 21:16:04.148488','2021-02-03 21:16:13.061510',82,1,1,'_67_81','WhatsApp','','','',16,0,'phone-square','','','+7 989 085 87 45',''),(97,NULL,'2021-02-03 21:16:23.294549','2021-02-03 21:16:32.702984',83,1,1,'_67_81','Email','','','',16,0,'envelope-o','','','guarantee@white-siberia.com',''),(98,NULL,'2021-02-03 21:16:53.360211','2021-02-03 21:17:04.005939',84,1,1,'_68_77','Телефон','','','',16,0,'phone','','','<a href=\"tel:+375333274526\">+375 33 327 45 26</a>',''),(99,NULL,'2021-02-03 21:17:16.441848','2021-02-03 21:17:24.378744',85,1,1,'_68_77','WhatsApp','','','',16,0,'phone-square','','','<a href=\"https://wa.me/375333274526\">+375 33 327 45 26</a>',''),(100,NULL,'2021-02-03 21:17:33.642760','2021-02-03 21:17:43.320158',86,1,1,'_68_77','Email','','','',16,0,'envelope-o','','','<a href=\"mailto:opt@white-siberia.com\">opt@white-siberia.com</a>',''),(101,NULL,'2021-02-03 21:18:08.439227','2021-02-03 21:18:16.769648',87,1,1,'_69_78','Телефон','','','',16,0,'phone','','','<a href=\"tel:+8613167039323\">+86 131 6703 9323</a>',''),(102,NULL,'2021-02-03 21:18:27.227153','2021-02-03 21:18:35.388535',88,1,1,'_69_78','WhatsApp','','','',16,0,'phone-square','','','<a href=\"https://wa.me/8613167039323\">+86 131 6703 9323</a>',''),(103,NULL,'2021-02-03 21:18:44.552515','2021-02-03 21:18:50.283525',89,1,1,'_69_78','Email','','','',16,0,'envelope-o','','','<a href=\"mailto:opt@white-siberia.com\">opt@white-siberia.com</a>',''),(104,NULL,'2021-02-03 21:19:03.220580','2021-02-03 21:19:20.296041',90,1,1,'_69_82','Без названия','','','',16,0,'wechat','','','motobike-shanghai',''),(105,NULL,'2021-02-03 21:19:35.232804','2021-02-03 21:19:46.689851',91,1,1,'_70_79','Телефон','','','',16,0,'phone','','','<a href=\"tel:+77711290202\">+7 771 129 02 02</a>',''),(106,NULL,'2021-02-03 21:20:00.241759','2021-02-03 21:20:11.280790',92,1,1,'_70_79','WhatsApp','','','',16,0,'phone-square','','','<a href=\"https://wa.me/77711290202\">+7 771 129 02 02</a>',''),(107,NULL,'2021-02-03 21:20:21.390743','2021-02-03 21:20:31.663001',93,1,1,'_70_79','Email','','','',16,0,'envelope-o','','','<a href=\"mailto:opt@white-siberia.com\">opt@white-siberia.com</a>',''),(108,NULL,'2021-02-03 21:20:50.351157','2021-02-03 21:20:50.351177',54,1,1,'','Россия','','','',17,0,'','','','',''),(109,NULL,'2021-02-03 21:20:50.351989','2021-02-03 21:20:50.352005',58,1,1,'_108','Адреса','','','',17,0,'','','','',''),(110,NULL,'2021-02-03 21:20:50.352727','2021-02-03 21:20:50.352742',69,1,1,'_108_109','Адрес1','','','',17,0,'map-marker','','','г. Москва, дер. Марушкино, ул. Северная\r\n<br>',''),(111,NULL,'2021-02-03 21:20:50.353504','2021-02-03 21:20:50.353521',70,1,1,'_108_109','Адрес2','','','',17,0,'map-marker','','','г. Сочи, Адлерский р-н, ул. Садовая 48',''),(112,NULL,'2021-02-03 21:20:50.354356','2021-02-03 21:20:50.354374',62,1,1,'_108','Оптовый отдел',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(113,NULL,'2021-02-03 21:20:50.355154','2021-02-03 21:20:50.355171',75,1,1,'_108_112','Телефон','','','',17,0,'phone','','','<a href=\"tel:+79384704147\">+7 938 470 41 47</a>',''),(114,NULL,'2021-02-03 21:20:50.358068','2021-02-03 21:20:50.358094',76,1,1,'_108_112','WhatsApp','','','',17,0,'phone-square','','','+7 938 470 41 47',''),(115,NULL,'2021-02-03 21:20:50.359075','2021-02-03 21:20:50.359094',77,1,1,'_108_112','Email','','','',17,0,'envelope-o','','','opt@white-siberia.com',''),(116,NULL,'2021-02-03 21:20:50.359845','2021-02-03 21:20:50.359860',66,1,1,'_108','Розничный отдел',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(117,NULL,'2021-02-03 21:20:50.360603','2021-02-03 21:20:50.360619',78,1,1,'_108_116','Телефон','','','',17,0,'phone','','','+7 988 169 16 39',''),(118,NULL,'2021-02-03 21:20:50.361358','2021-02-03 21:20:50.361374',79,1,1,'_108_116','WhatsApp','','','',17,0,'phone-square','','','+7 988 403 85 43',''),(119,NULL,'2021-02-03 21:20:50.362529','2021-02-03 21:20:50.362545',80,1,1,'_108_116','Email','','','',17,0,'envelope-o','','','roznica@white-siberia.com',''),(120,NULL,'2021-02-03 21:20:50.363303','2021-02-03 21:20:50.363319',67,1,1,'_108','Гарантийный отдел',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(121,NULL,'2021-02-03 21:20:50.364103','2021-02-03 21:20:50.364129',81,1,1,'_108_120','Телефон','','','',17,0,'phone','','','+7 989 085 87 45',''),(122,NULL,'2021-02-03 21:20:50.365417','2021-02-03 21:20:50.365438',82,1,1,'_108_120','WhatsApp','','','',17,0,'phone-square','','','+7 989 085 87 45',''),(123,NULL,'2021-02-03 21:20:50.366338','2021-02-03 21:20:50.366357',83,1,1,'_108_120','Email','','','',17,0,'envelope-o','','','guarantee@white-siberia.com',''),(124,NULL,'2021-02-03 21:20:50.367212','2021-02-03 21:20:50.367229',55,1,1,'','Беларусь',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(125,NULL,'2021-02-03 21:20:50.368091','2021-02-03 21:20:50.368108',59,1,1,'_124','Адреса',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(126,NULL,'2021-02-03 21:20:50.368905','2021-02-03 21:20:50.368922',71,1,1,'_124_125','Адрес1','','','',17,0,'map-marker','','','г. Минск Новая Боровая, Авиационная 10',''),(127,NULL,'2021-02-03 21:20:50.369777','2021-02-03 21:20:50.369794',63,1,1,'_124','Оптовый отдел',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(128,NULL,'2021-02-03 21:20:50.370593','2021-02-03 21:20:50.370618',84,1,1,'_124_127','Телефон','','','',17,0,'phone','','','<a href=\"tel:+375333274526\">+375 33 327 45 26</a>',''),(129,NULL,'2021-02-03 21:20:50.371438','2021-02-03 21:20:50.371455',85,1,1,'_124_127','WhatsApp','','','',17,0,'phone-square','','','<a href=\"https://wa.me/375333274526\">+375 33 327 45 26</a>',''),(130,NULL,'2021-02-03 21:20:50.372288','2021-02-03 21:20:50.372305',86,1,1,'_124_127','Email','','','',17,0,'envelope-o','','','<a href=\"mailto:opt@white-siberia.com\">opt@white-siberia.com</a>',''),(131,NULL,'2021-02-03 21:20:50.373150','2021-02-03 21:20:50.373169',56,1,1,'','Китай',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(132,NULL,'2021-02-03 21:20:50.374012','2021-02-03 21:20:50.374029',60,1,1,'_131','Адреса',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(133,NULL,'2021-02-03 21:20:50.375007','2021-02-03 21:20:50.375028',72,1,1,'_131_132','Адрес1','','','',17,0,'map-marker','','','Shanghai Channing district Channing street 398',''),(134,NULL,'2021-02-03 21:20:50.375925','2021-02-03 21:20:50.375953',73,1,1,'_131_132','Адрес2','','','',17,0,'map-marker','','','Shanghai Jiading district JiaSongbei street 6855',''),(135,NULL,'2021-02-03 21:20:50.376774','2021-02-03 21:20:50.376791',64,1,1,'_131','Оптовый отдел',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(136,NULL,'2021-02-03 21:20:50.377584','2021-02-03 21:20:50.377602',87,1,1,'_131_135','Телефон','','','',17,0,'phone','','','<a href=\"tel:+8613167039323\">+86 131 6703 9323</a>',''),(137,NULL,'2021-02-03 21:20:50.378404','2021-02-03 21:20:50.378421',88,1,1,'_131_135','WhatsApp','','','',17,0,'phone-square','','','<a href=\"https://wa.me/8613167039323\">+86 131 6703 9323</a>',''),(138,NULL,'2021-02-03 21:20:50.379390','2021-02-03 21:20:50.379408',89,1,1,'_131_135','Email','','','',17,0,'envelope-o','','','<a href=\"mailto:opt@white-siberia.com\">opt@white-siberia.com</a>',''),(139,NULL,'2021-02-03 21:20:50.380205','2021-02-03 21:20:50.380221',68,1,1,'_131','WeChat ID',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(140,NULL,'2021-02-03 21:20:50.380983','2021-02-03 21:20:50.380999',90,1,1,'_131_139','Без названия','','','',17,0,'wechat','','','motobike-shanghai',''),(141,NULL,'2021-02-03 21:20:50.381766','2021-02-03 21:20:50.381782',57,1,1,'','Казахстан',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(142,NULL,'2021-02-03 21:20:50.382526','2021-02-03 21:20:50.382542',61,1,1,'_141','Адреса',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(143,NULL,'2021-02-03 21:20:50.383333','2021-02-03 21:20:50.383348',74,1,1,'_141_142','Адрес1','','','',17,0,'map-marker','','','г. Караганда, ул. Крылова, д. 101',''),(144,NULL,'2021-02-03 21:20:50.384145','2021-02-03 21:20:50.384161',65,1,1,'_141','Оптовый отдел',NULL,NULL,NULL,17,0,NULL,NULL,NULL,NULL,NULL),(145,NULL,'2021-02-03 21:20:50.384907','2021-02-03 21:20:50.384923',91,1,1,'_141_144','Телефон','','','',17,0,'phone','','','<a href=\"tel:+77711290202\">+7 771 129 02 02</a>',''),(146,NULL,'2021-02-03 21:20:50.387127','2021-02-03 21:20:50.387144',92,1,1,'_141_144','WhatsApp','','','',17,0,'phone-square','','','<a href=\"https://wa.me/77711290202\">+7 771 129 02 02</a>',''),(147,NULL,'2021-02-03 21:20:50.387914','2021-02-03 21:20:50.387929',93,1,1,'_141_144','Email','','','',17,0,'envelope-o','','','<a href=\"mailto:opt@white-siberia.com\">opt@white-siberia.com</a>',''),(148,'prod.png','2021-02-05 18:04:57.874822','2021-02-06 14:26:38.046908',94,1,4,'','Продукция','','/cat/produkciya/','',21,0,'','','','',''),(149,'katalog_2.png','2021-02-05 18:05:23.294734','2021-02-06 14:27:04.319139',95,1,4,'','Аксессуары','','/cat/bez-nazvaniya/','',21,0,'','','','',''),(150,'parts.png','2021-02-05 18:05:36.912926','2021-02-13 11:24:11.985404',96,1,4,'','Запчасти','','https://yadi.sk/d/vWcN4R4zCw-kKQ?w=1','',21,1,'external-link','','','',''),(151,NULL,'2021-02-05 18:06:34.780657','2021-02-12 16:32:53.111607',97,1,4,'','WS-PRO TRIKE+ 3000W','','/product/ws-pro-trike-3000w-1/','product_1',22,0,NULL,'','',NULL,NULL),(152,'surron-logo.png','2021-02-06 16:26:50.702093','2021-02-06 16:32:21.325193',98,1,1,'','SUR-RON','Перейти на сайт','https://surronrussia.ru/','',25,1,'','','','Мы являемся<br>официальными представителями<br>техники SUR-RON',''),(153,'surron-logo.png','2021-02-06 16:40:04.257625','2021-02-06 16:40:04.257647',98,1,1,'','SUR-RON','Перейти на сайт','https://surronrussia.ru/','',26,1,'','','','Мы являемся<br>официальными представителями<br>техники SUR-RON',''),(154,NULL,'2021-02-06 17:21:31.686759','2021-02-10 19:16:01.025122',99,1,1,'','video1','Перейти на YouTube','https://www.youtube.com/channel/UCLMxls9urKSgQdE7setOt9w','',27,1,'youtube-play','','','<iframe src=\"https://www.youtube.com/embed/u8Tx7XC5q8k\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" width=\"398\" height=\"199\" frameborder=\"0\"></iframe>',''),(155,NULL,'2021-02-06 17:22:01.784443','2021-02-06 17:22:07.776280',100,1,1,'','video2','','','',27,0,'','','','<iframe width=\"398\" height=\"199\" src=\"https://www.youtube.com/embed/L8OU9xwCUXE\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>',''),(156,NULL,'2021-02-06 17:22:18.719858','2021-02-06 17:22:25.024811',101,1,1,'','video3','','','',27,0,'','','','<iframe width=\"398\" height=\"199\" src=\"https://www.youtube.com/embed/t_l9If6U_J4\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>',''),(157,NULL,'2021-02-06 17:22:44.156291','2021-02-06 17:24:20.781470',102,1,1,'','video4','','','',27,0,'','','','<iframe src=\"https://www.youtube.com/embed/lfSkjl0Qu68\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" width=\"398\" height=\"199\" frameborder=\"0\"></iframe>',''),(158,NULL,'2021-02-06 17:34:12.538147','2021-02-06 17:44:54.598215',99,1,1,'','video1','Перейти на YouTube','https://www.youtube.com/channel/UCLMxls9urKSgQdE7setOt9w','',28,1,'','','','<iframe src=\"https://www.youtube.com/embed/u8Tx7XC5q8k\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" width=\"398\" height=\"199\" frameborder=\"0\"></iframe>',''),(159,NULL,'2021-02-06 17:34:12.541346','2021-02-06 17:34:12.541366',100,1,1,'','video2','','','',28,0,'','','','<iframe width=\"398\" height=\"199\" src=\"https://www.youtube.com/embed/L8OU9xwCUXE\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>',''),(160,NULL,'2021-02-06 17:34:12.542266','2021-02-06 17:34:12.542282',101,1,1,'','video3','','','',28,0,'','','','<iframe width=\"398\" height=\"199\" src=\"https://www.youtube.com/embed/t_l9If6U_J4\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>',''),(161,NULL,'2021-02-06 17:34:12.549777','2021-02-06 17:34:12.549798',102,1,1,'','video4','','','',28,0,'','','','<iframe src=\"https://www.youtube.com/embed/lfSkjl0Qu68\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" width=\"398\" height=\"199\" frameborder=\"0\"></iframe>',''),(162,NULL,'2021-02-06 18:30:25.177266','2021-02-07 22:17:25.347075',103,1,4,'','WS-PRO MAX+ 3000W','','/product/ws-pro-max-3000w-2/','product_2',22,0,NULL,'','',NULL,NULL),(163,NULL,'2021-02-07 11:39:18.998662','2021-02-07 22:22:03.528488',104,1,4,'','WS-PRO 2WD 4000W','','/product/ws-pro-2wd-4000w-3/','product_3',22,0,NULL,'','',NULL,NULL),(164,NULL,'2021-02-07 11:56:00.215654','2021-02-07 22:29:19.052098',105,1,4,'','WS-WILD WHEEL 3000W','','/product/ws-wild-wheel-3000w-4/','product_4',22,0,NULL,'','',NULL,NULL),(165,NULL,'2021-02-07 12:24:33.880146','2021-02-07 22:33:39.099211',106,1,4,'','WS-PRO+ 2500W','','/product/ws-pro-2500w-5/','product_5',22,0,NULL,'','',NULL,NULL),(166,NULL,'2021-02-07 13:06:54.226523','2021-02-07 22:38:24.705418',107,1,4,'','WS-PRO LIGHT 2000W','','/product/ws-pro-light-2000w-6/','product_6',22,0,NULL,'','',NULL,NULL),(167,NULL,'2021-02-07 13:15:30.240030','2021-02-07 22:41:53.466058',108,1,4,'','WS-MINI R 1200W','','/product/ws-mini-r-1200w-7/','product_7',22,0,NULL,'','',NULL,NULL),(168,NULL,'2021-02-07 13:19:30.089724','2021-02-07 22:45:44.781754',109,1,4,'','WS-SOCHI 1300W','','/product/ws-sochi-1300w-8/','product_8',22,0,NULL,'','',NULL,NULL),(169,NULL,'2021-02-07 13:24:42.336250','2021-02-07 22:48:23.292806',110,1,4,'','WS-TAIGA 800W','','/product/ws-taiga-800w-9/','product_9',22,0,NULL,'','',NULL,NULL),(170,NULL,'2021-02-07 16:10:41.064522','2021-02-07 23:04:47.555965',111,1,4,'','LOCKER 1.0','','/product/locker-10-10/','product_10',22,0,NULL,'','',NULL,NULL),(171,NULL,'2021-02-07 16:14:06.606984','2021-02-07 23:29:45.153602',112,1,4,'','LOCKER 2.0','','/product/locker-20-11/','product_11',22,0,NULL,'','',NULL,NULL),(172,NULL,'2021-02-07 16:16:52.065389','2021-02-07 23:31:43.822479',113,1,4,'','WS-PHONE HOLDER 1.0','','/product/ws-phone-holder-10-12/','product_12',22,0,NULL,'','',NULL,NULL),(173,NULL,'2021-02-07 16:19:27.126971','2021-02-07 23:33:32.790762',114,1,4,'','WS-PHONE HOLDER 2.0','','/product/ws-phone-holder-20-13/','product_13',22,0,NULL,'','',NULL,NULL),(174,NULL,'2021-02-07 16:22:34.861766','2021-02-07 23:35:49.982378',115,1,4,'','WS-URBAN 3L','','/product/ws-urban-3l-14/','product_14',22,0,NULL,'','',NULL,NULL),(175,NULL,'2021-02-07 16:25:05.331159','2021-02-07 23:37:45.811887',116,1,4,'','WS-URBAN 5L','','/product/ws-urban-5l-15/','product_15',22,0,NULL,'','',NULL,NULL),(176,NULL,'2021-02-07 16:28:20.089969','2021-02-07 23:40:17.257647',117,1,4,'','WS-FAST CHARGER 5A','','/product/ws-fast-charger-5a-16/','product_16',22,0,NULL,'','',NULL,NULL),(177,NULL,'2021-02-07 16:30:39.938983','2021-02-07 23:42:11.075886',118,1,4,'','WS-KIDS HOLDER','','/product/ws-kids-holder-17/','product_17',22,0,NULL,'','',NULL,NULL),(178,NULL,'2021-02-07 16:36:57.288670','2021-02-07 23:50:56.609833',119,1,4,'','WS-RAIN COVER','','/product/ws-rain-cover-18/','product_18',22,0,NULL,'','',NULL,NULL),(179,NULL,'2021-02-07 16:39:41.976649','2021-02-07 23:57:33.481494',120,1,4,'','WS-OFFROAD EVOLUTION','','/product/ws-offroad-evolution-19/','product_19',22,0,NULL,'','',NULL,NULL),(180,NULL,'2021-02-07 16:42:34.922558','2021-02-07 23:59:18.963381',121,1,4,'','EVA-коврик','','/product/eva-kovrik-20/','product_20',22,0,NULL,'','',NULL,NULL),(181,'ower-2.png','2021-02-07 20:04:52.207665','2021-02-07 20:06:02.451685',122,1,1,'','Надежность, функциональность и мощь','','','',29,0,'','','','<div>\r\n											<ul><li>Грузоподъемность до 260 кг</li><li>Мотор тягового типа мощностью 3000 Вт</li><li>Возможность всесезонной эксплуатации</li><li>Шикарная комплектация: бокс, сетка-багажник, держатель для телефона, удобная спинка</li></ul>\r\n										</div>',''),(182,'ower-3.png','2021-02-07 20:12:23.346350','2021-02-07 20:12:46.645738',123,1,1,'','Максимальный комфорт даже на бездорожье','','','',29,0,'','','','<div>\r\n											<ul><li>Комфортная и динамичная езда благодаря 10–дюймовым колёсам</li><li>Большое и мягкое сиденье </li><li>Настраиваемая подвеска</li></ul>\r\n										</div>',''),(183,'ower-1.png','2021-02-07 20:13:12.227690','2021-02-07 20:13:31.002868',124,1,1,'','Безопасное передвижение в темное время суток','','','',29,0,'','','','<div>\r\n											<ul><li>1 мощная фара + 2 стробоскопа (вспомогательный свет)</li><li>Яркие задние ходовые огни, сертифицированные ECC</li><li>Поворотники LED с ярким свечением </li></ul>\r\n										</div>',''),(184,'ower-4.png','2021-02-07 20:13:43.484705','2021-02-07 20:13:59.599583',125,1,1,'','Уверенность в каждом километре','','','',29,0,'','','','<div>\r\n											<ul><li>Максимальная скорость до 45 км/ч</li><li>Тормозная система нового вида с возможностью регулировки</li><li>Обновленная тормозная система с возможностью регулировки</li><li>Масляные амортизаторы с возможностью регулировки</li><li>Плавность старта и торможения</li></ul>\r\n										</div>',''),(185,'ower-5.png','2021-02-07 20:14:08.676699','2021-02-07 20:14:23.600603',126,1,1,'','Инновационный LI-ION аккумулятор','','','',29,0,'','','','<div>\r\n											<ul><li>Пробег до 60 км на одном заряде</li><li>Быстросъёмный аккумулятор с балансировочной платой</li><li>Возможность установить вторую батарею и проезжать до 100 км</li><li>Производство TAIWAN</li></ul>\r\n										</div>',''),(186,'ower-6.png','2021-02-07 20:14:34.280452','2021-02-07 20:14:50.404258',127,1,1,'','Удобство и простота использования','','','',29,0,'','','','<div>\r\n											<ul><li>Большие, интуитивно понятные кнопки управления</li><li>Бортовой компьютер с LED-дисплеем</li><li>Большие зеркала без искажения</li><li>Держатель телефона с USB</li><li>Вместительный бокс и сетка-багажник</li><li>Кнопка Start-Stop</li><li>Сигнализация</li></ul>\r\n										</div>',''),(187,'ower-2.png','2021-02-07 20:16:37.449623','2021-02-07 20:16:37.449647',122,1,1,'','Надежность, функциональность и мощь','','','',30,0,'','','','<div>\r\n											<ul><li>Грузоподъемность до 260 кг</li><li>Мотор тягового типа мощностью 3000 Вт</li><li>Возможность всесезонной эксплуатации</li><li>Шикарная комплектация: бокс, сетка-багажник, держатель для телефона, удобная спинка</li></ul>\r\n										</div>',''),(188,'ower-3.png','2021-02-07 20:16:37.451426','2021-02-07 20:16:37.451444',123,1,1,'','Максимальный комфорт даже на бездорожье','','','',30,0,'','','','<div>\r\n											<ul><li>Комфортная и динамичная езда благодаря 10–дюймовым колёсам</li><li>Большое и мягкое сиденье </li><li>Настраиваемая подвеска</li></ul>\r\n										</div>',''),(189,'ower-1.png','2021-02-07 20:16:37.459797','2021-02-07 20:16:37.459824',124,1,1,'','Безопасное передвижение в темное время суток','','','',30,0,'','','','<div>\r\n											<ul><li>1 мощная фара + 2 стробоскопа (вспомогательный свет)</li><li>Яркие задние ходовые огни, сертифицированные ECC</li><li>Поворотники LED с ярким свечением </li></ul>\r\n										</div>',''),(190,'ower-4.png','2021-02-07 20:16:37.471184','2021-02-07 20:16:37.471211',125,1,1,'','Уверенность в каждом километре','','','',30,0,'','','','<div>\r\n											<ul><li>Максимальная скорость до 45 км/ч</li><li>Тормозная система нового вида с возможностью регулировки</li><li>Обновленная тормозная система с возможностью регулировки</li><li>Масляные амортизаторы с возможностью регулировки</li><li>Плавность старта и торможения</li></ul>\r\n										</div>',''),(191,'ower-5.png','2021-02-07 20:16:37.493510','2021-02-07 20:16:37.493535',126,1,1,'','Инновационный LI-ION аккумулятор','','','',30,0,'','','','<div>\r\n											<ul><li>Пробег до 60 км на одном заряде</li><li>Быстросъёмный аккумулятор с балансировочной платой</li><li>Возможность установить вторую батарею и проезжать до 100 км</li><li>Производство TAIWAN</li></ul>\r\n										</div>',''),(192,'ower-6.png','2021-02-07 20:16:37.502127','2021-02-07 20:16:37.502152',127,1,1,'','Удобство и простота использования','','','',30,0,'','','','<div>\r\n											<ul><li>Большие, интуитивно понятные кнопки управления</li><li>Бортовой компьютер с LED-дисплеем</li><li>Большие зеркала без искажения</li><li>Держатель телефона с USB</li><li>Вместительный бокс и сетка-багажник</li><li>Кнопка Start-Stop</li><li>Сигнализация</li></ul>\r\n										</div>',''),(193,'ower-4.png','2021-02-07 22:13:53.102252','2021-02-07 22:14:25.551188',122,1,1,'','Непревзойденная динамика и маневренность','','','',31,0,'','','','<div>\r\n											<ul><li>Максимальная скорость - до 71 км/ч</li><li>Мотор-колесо мощностью 3000 Вт, созданный специально для динамичной езды</li><li>Прекрасная маневренность на любых скоростях благодаря правильному распределению центра тяжести</li><li>Шикарная комплектация: бокс, держатель для телефона, спинка </li></ul>\r\n										</div>',''),(199,'ower-3.png','2021-02-07 22:14:35.433831','2021-02-07 22:14:57.533453',128,1,1,'','Максимальный комфорт при скоростной езде','','','',31,0,'','','','<div>\r\n											<ul><li>12-дюймовые колеса с низким профилем резины для отличного сцепления с дорожным покрытием</li><li>Мягкое и большое сиденье </li><li>Настраиваемая подвеска</li></ul>\r\n										</div>',''),(200,'ower-1.png','2021-02-07 22:15:04.981551','2021-02-07 22:15:41.638998',129,1,1,'','Безопасное передвижение в темное время суток','','','',31,0,'','','','<div>\r\n											<ul><li>1 мощная фара + 2 стробоскопа (вспомогательный свет)</li><li>Яркие задние ходовые огни, сертифицированные ECC</li><li>Поворотники LED с ярким свечением</li></ul>\r\n										</div>',''),(201,'ower-2.png','2021-02-07 22:15:52.313229','2021-02-07 22:16:12.156573',130,1,1,'','Уверенность в каждом километре','','','',31,0,'','','','<div>\r\n											<ul><li>Динамичность старта и быстрота торможения</li><li>Обновленная тормозная система с возможностью регулировки</li><li>Масляные амортизаторы с возможностью регулировки</li></ul>\r\n										</div>',''),(202,'ower-5.png','2021-02-07 22:16:21.777837','2021-02-07 22:16:36.263045',131,1,1,'','Инновационный LI-ION аккумулятор','','','',31,0,'','','','<div>\r\n											<ul><li>Пробег до 60 км на одном заряде</li><li>Быстросъёмный аккумулятор с балансировочной платой</li><li>Возможность установить вторую батарею и проезжать до 100 км</li><li>Производство TAIWAN</li></ul>\r\n										</div>',''),(203,'ower-6.png','2021-02-07 22:16:45.649266','2021-02-07 22:17:01.234809',132,1,1,'','Удобство и простота использования','','','',31,0,'','','','<div>\r\n											<ul><li>Большие, интуитивно понятные кнопки управления</li><li>Бортовой компьютер с LED-дисплеем</li><li>Большие зеркала без искажения</li><li>Держатель телефона с USB</li><li>Вместительный бокс и бардачок, встроенный в сиденье</li><li>Кнопка Start-Stop</li><li>Сигнализация</li></ul>\r\n										</div>',''),(204,'ower-2.png','2021-02-07 22:18:52.257694','2021-02-07 22:19:25.366066',122,1,1,'','Повышенная проходимость и функциональность','','','',32,0,'','','','<div>\r\n											<ul><li>Полный привод</li><li>Два мотор-колеса мощностью 2000 Вт каждое</li><li>Высокий клиренс</li><li>Богатая комплектация: бокс, держатель для телефона, спинка</li></ul>\r\n										</div>',''),(210,'ower-3.png','2021-02-07 22:19:37.215516','2021-02-07 22:19:50.539980',133,1,1,'','Максимальный комфорт даже на бездорожье','','','',32,0,'','','','<div>\r\n											<ul><li>Максимальный комфорт даже на серьезном бездорожье</li><li>Большое и мягкое сиденье</li><li>Настраиваемая подвеска</li></ul>\r\n										</div>',''),(211,'ower-1.png','2021-02-07 22:19:59.623616','2021-02-07 22:20:25.839572',134,1,1,'','Безопасное передвижение в темное время суток','','','',32,0,'','','','<div>\r\n											<ul><li>1 мощная фара + 2 стробоскопа (вспомогательный свет)</li><li>Яркие задние ходовые огни, сертифицированные ECC</li><li>Поворотники LED с ярким свечением</li></ul>\r\n										</div>',''),(212,'ower-4.png','2021-02-07 22:20:34.344653','2021-02-07 22:20:48.355639',135,1,1,'','Уверенность в каждом километре','','','',32,0,'','','','<div>\r\n											<ul><li>Максимальная скорость до 61 км/ч</li><li>Плавность старта и торможения</li><li>Обновленная тормозная система с возможностью регулировки</li><li>Масляные амортизаторы </li></ul>\r\n										</div>',''),(213,'ower-5.png','2021-02-07 22:20:59.051698','2021-02-07 22:21:12.772539',136,1,1,'','Инновационный LI-ION аккумулятор','','','',32,0,'','','','<div>\r\n											<ul><li>Пробег до 60 км на одном заряде</li><li>Быстросъёмный аккумулятор с балансировочной платой</li><li>Возможность установить вторую батарею и проезжать до 100 км</li><li>Производство TAIWAN</li></ul>\r\n										</div>',''),(214,'ower-6.png','2021-02-07 22:21:17.632915','2021-02-07 22:21:35.838447',137,1,1,'','Удобство и простота использования','','','',32,0,'','','','<div>\r\n											<ul><li>Большие, интуитивно понятные кнопки управления</li><li>Бортовой компьютер с LED-дисплеем</li><li>Большие зеркала без искажения</li><li>Держатель для телефона с USB</li><li>Вместительный бокс и бардачок, встроенный в сиденье</li><li>Кнопка Start-Stop</li><li>Сигнализация</li></ul>\r\n										</div>',''),(215,'ower-2.png','2021-02-07 22:26:00.392550','2021-02-07 22:26:40.470739',122,1,1,'','Лучшие качества круизера','','','',33,0,'','','','<div>\r\n											<ul><li>Пробег до 100 км на одном заряде АКБ</li><li>Никакой усталости благодаря удобной посадке</li><li>Три вместительных кофра и большой пластиковый бокс</li><li>Стильный дизайн, приковывающий взгляды</li></ul>\r\n										</div>',''),(221,'ower-3.png','2021-02-07 22:26:45.574101','2021-02-07 22:27:03.412438',138,1,1,'','Максимальный комфорт в длительных путешествиях','','','',33,0,'','','','<div>\r\n											<ul><li>Мотор-колесо мощностью 3000 Вт для динамичной езды</li><li>12-дюймовые колеса для преодоления бордюров и стабилизации байка при езде по неровным дорогам</li><li>Настраиваемая подвеска</li><li>Широкое заднее колесо для лучшего сцепления с дорогой</li></ul>\r\n										</div>',''),(222,'ower-1.png','2021-02-07 22:27:07.106249','2021-02-07 22:27:28.365158',139,1,1,'','Безопасное передвижение в темное время суток','','','',33,0,'','','','<div>\r\n											<ul><li>1 мощная фара с четкой световой границей</li><li>Яркие задние ходовые огни, сертифицированные ECC</li><li>Поворотники LED с ярким свечением </li></ul>\r\n										</div>',''),(223,'ower-4.png','2021-02-07 22:27:32.577761','2021-02-07 22:27:55.317299',140,1,1,'','Уверенность в каждом километре','','','',33,0,'','','','<div>\r\n											<ul><li>Максимальная скорость до 71 км/ч</li><li>Плавность старта и торможения</li><li>Обновленная тормозная система с возможностью регулировки</li><li>Масляные амортизаторы мотоциклетного типа с возможностью регулировки</li></ul>\r\n										</div>',''),(224,'ower-5.png','2021-02-07 22:28:04.190951','2021-02-07 22:28:18.164823',141,1,1,'','Инновационный LI-ION аккумулятор','','','',33,0,'','','','<div>\r\n											<ul><li>Пробег до 100 км на одном заряде 60V 31A</li><li>Быстросъёмный аккумулятор с балансировочной платой</li><li>Производство TAIWAN</li></ul>\r\n										</div>',''),(225,'ower-6.png','2021-02-07 22:28:35.427908','2021-02-07 22:28:48.405140',142,1,1,'','Удобство и простота использования','','','',33,0,'','','','<div>\r\n											<ul><li>Большие, интуитивно понятные кнопки управления</li><li>Бортовой компьютер с двумя LED-дисплеями</li><li>Большие зеркала без искажения</li><li>Держатель телефона с USB</li><li>Богатая комплектация с боксом и тремя кофрами</li><li>Сигнализация</li></ul>\r\n										</div>',''),(232,'232.png','2021-02-07 22:30:00.224710','2021-02-07 22:30:37.554303',143,1,1,'','Возможность установки трех АКБ, компактность и доступная цена','','','',34,0,'','','','<div>\r\n											<ul><li>Тяговитое мотор-колесо мощностью 2500W</li><li>Прекрасная проходимость по асфальту и бездорожью</li><li>Возможность проезжать до 150 км без дополнительной подзарядки</li><li>Мягкое анотомическое сиденье </li></ul>\r\n										</div>',''),(233,'233.png','2021-02-07 22:30:42.085487','2021-02-07 22:31:25.859430',144,1,1,'','Максимальный комфорт на любых дорогах','','','',34,0,'','','','<div>\r\n											<ul><li>10-дюймовые колеса с универсальным протектором резины для отличного сцепления с дорожным покрытием</li><li>Максимальная скорость - до 60 км/ч</li><li>Настраиваемая подвеска</li></ul>\r\n										</div>',''),(234,'ZXT_825811.png','2021-02-07 22:31:34.663023','2021-02-07 22:31:47.757042',145,1,1,'','Безопасность передвижения в темное время суток','','','',34,0,'','','','<div>\r\n											<ul><li>1 мощная фара + 2 стробоскопа (вспомогательный свет)</li><li>Яркие задние ходовые огни, сертифицированные ECC</li><li>Поворотники LED с ярким свечением</li></ul>\r\n										</div>',''),(235,'ZXT_825822.png','2021-02-07 22:31:56.943391','2021-02-07 22:32:13.213402',146,1,1,'','Уверенность в каждом километре','','','',34,0,'','','','<div>\r\n											<ul><li>Динамичность старта и быстрота торможения</li><li>Обновленная тормозная система с возможностью регулировки</li><li>Масляные амортизаторы с возможностью регулировки</li></ul>\r\n										</div>',''),(236,'ZXT_8258333.png','2021-02-07 22:32:21.927942','2021-02-07 22:32:43.273487',147,1,1,'','Инновационный LI-ION аккумулятор','','','',34,0,'','','','<div>\r\n											<ul><li>Пробег до 60 км на одном заряде</li><li>Быстросъёмный аккумулятор с балансировочной платой</li><li>Возможность установить дополнительно две батареи и проезжать до 150 км (в общем 3 АКБ в одном скутере)</li><li>Производство TAIWAN</li></ul>\r\n										</div>',''),(237,'ZXT_8258444.png','2021-02-07 22:32:51.796028','2021-02-07 22:33:04.141866',148,1,1,'','Удобство и простота использования','','','',34,0,'','','','<div>\r\n											<ul><li>Большие, интуитивно понятные кнопки управления</li><li>Бортовой компьютер с LED-дисплеем</li><li>Большие зеркала без искажения</li><li>Вместительный бокс </li><li>Кнопка Start-Stop</li><li>Сигнализация</li></ul>\r\n										</div>',''),(238,'ower-2.png','2021-02-07 22:35:40.018861','2021-02-07 22:36:10.122346',122,1,1,'','Динамика, практичность и универсальность','','','',35,0,'','','','<div>\r\n											<ul><li>Мощное мотор-колесо тягового типа</li><li>Небольшой вес: всего 70 кг!</li><li>Легкость маневрирования в потоке</li><li>Возможность установки зимней или грязевой резины для круглогодичной эксплуатации</li></ul></div>',''),(244,'ower-3.png','2021-02-07 22:36:18.688138','2021-02-07 22:36:32.359728',149,1,1,'','Максимальный комфорт на любых дорогах','','','',35,0,'','','','<div>\r\n											<ul><li>8-дюймовые колеса с высоким профилем для смягчения любых неровностей дороги</li><li>Большое и мягкое сиденье с мягкой спинкой</li><li>Настраиваемая подвеска</li></ul>\r\n										</div>',''),(245,'ower-1.png','2021-02-07 22:36:37.776789','2021-02-07 22:36:58.831727',150,1,1,'','Безопасное передвижение в темное время суток','','','',35,0,'','','','<div>\r\n											<ul><li>1 мощная фара + 2 стробоскопа (вспомогательный свет)</li><li>Яркие задние ходовые огни, сертифицированные ECC</li><li>Поворотники LED с ярким свечением</li></ul>\r\n										</div>',''),(246,'ower-4.png','2021-02-07 22:37:06.766000','2021-02-07 22:37:18.960580',151,1,1,'','Уверенность в каждом километре','','','',35,0,'','','','<div>\r\n											<ul><li>Максимальная скорость до 55 км/ч</li><li>Классическая гидравлическая тормозная система</li><li>Масляные амортизаторы</li></ul>\r\n										</div>',''),(247,'ower-5.png','2021-02-07 22:37:26.448388','2021-02-07 22:37:38.974802',152,1,1,'','Инновационный LI-ION аккумулятор','','','',35,0,'','','','<div>\r\n											<ul><li>Пробег до 60 км на одном заряде</li><li>Быстросъёмный аккумулятор с балансировочной платой</li><li>Производство TAIWAN</li></ul>\r\n										</div>',''),(248,'ower-6.png','2021-02-07 22:37:46.494531','2021-02-07 22:38:01.021757',153,1,1,'','Удобство и простота использования','','','',35,0,'','','','<div>\r\n											<ul><li>Большие, интуитивно понятные кнопки управления</li><li>Бортовой компьютер с  LED-дисплеем</li><li>Большие зеркала без искажения</li><li>Держатель телефона с USB</li><li>Кнопка START-STOP</li><li>Сигнализация</li></ul>\r\n										</div>',''),(249,'ower-4.png','2021-02-07 22:38:48.441754','2021-02-07 22:39:20.769369',122,1,1,'','Легкость, надежность и свобода выбора','','','',36,0,'','','','<div>\r\n											<ul><li>Двухместная модель весом всего 40 кг!</li><li>Сверхпрочная мотоциклетная трубчатая рама</li><li>Мотор тягового типа мощностью 1200 Вт</li><li>В комлекте второе сиденье с мягкой спинкой и корзина. Что устанавливать - решать только Вам!</li></ul>\r\n										</div>',''),(255,'ower-2.png','2021-02-07 22:39:28.319786','2021-02-07 22:39:42.220731',154,1,1,'','Максимальный комфорт на любых дорогах','','','',36,0,'','','','<div>\r\n											<ul><li>6,5-дюймовые колеса с высоким профилем для смягчения любых неровностей дороги</li><li>Полноразмерные крылья для защиты от брызг</li><li>Большое и мягкое сиденье</li><li>Настраиваемая подвеска</li></ul>\r\n										</div>',''),(256,'ower-1.png','2021-02-07 22:39:50.653167','2021-02-07 22:40:14.629114',155,1,1,'','Безопасное передвижение в темное время суток','','','',36,0,'','','','<div>\r\n											<ul><li>1 мощная фара + 2 стробоскопа (вспомогательный свет)</li><li>Яркие задние ходовые огни, сертифицированные ECC</li></ul>\r\n										</div>',''),(257,'ower-9.png','2021-02-07 22:40:22.646797','2021-02-07 22:40:33.179110',156,1,1,'','Уверенность в каждом километре','','','',36,0,'','','','<div>\r\n											<ul><li>Максимальная скорость до 45 км/ч</li><li>Дисковые тормоза с возможностью регулировки</li><li>Масляные амортизаторы с возможностью регулировки</li></ul>\r\n										</div>',''),(258,'ower-7.png','2021-02-07 22:40:41.175221','2021-02-07 22:40:54.128668',157,1,1,'','Инновационный LI-ION аккумулятор','','','',36,0,'','','','<div>\r\n											<ul><li>Пробег до 60 км на одном заряде</li><li>Быстросъёмный аккумулятор с балансировочной платой</li><li>Возможность установить вторую батарею и проезжать до 100 км</li><li>Производство TAIWAN</li></ul>\r\n										</div>',''),(259,'ower-5.png','2021-02-07 22:41:00.867149','2021-02-07 22:41:13.274137',158,1,1,'','Удобство и простота использования','','','',36,0,'','','','<div>\r\n											<ul><li>Большие, интуитивно понятные кнопки управления</li><li>Бортовой компьютер с  LED-дисплеем</li><li>Большие зеркала без искажения</li><li>Фирменный держатель телефона </li><li>Сигнализация</li></ul>\r\n										</div>',''),(260,'ower-10.png','2021-02-07 22:41:22.049532','2021-02-07 22:41:33.941307',159,1,1,'','Незаменимый в жизни','','','',36,0,'','','','<div>\r\n											<ul><li>Байк имеет втрое сиденье в комплекте</li><li>Байк имеет большую корзину в комплекте</li><li>Можно полностью подготовить под ваши нужды</li></ul>\r\n										</div>',''),(261,'ZXT_3046.png','2021-02-07 22:43:03.102203','2021-02-07 22:43:34.069233',122,1,1,'','Прочность и функциональность','','','',37,0,'','','','<div>\r\n											<ul><li>Мощный мотор тягового типа 1300w</li><li>Спидометр с указанием заряда батареи </li><li>Мотоциклетная трубчатая рама обладает сверх прочностью</li></ul>\r\n										</div>',''),(267,'ZXT_3027.png','2021-02-07 22:43:47.062174','2021-02-07 22:44:01.495784',160,1,1,'','Мягкость и комфорт во время езды','','','',37,0,'','','','<div>\r\n											<ul><li>Комфортная и динамичная езда, благодаря 10– дюймовым колёсам внедорожного типа</li><li>Мягкое и большое сиденье</li><li>Настраиваемая масляная подвеска</li></ul>\r\n										</div>',''),(268,'ZXT_3029.png','2021-02-07 22:44:08.915745','2021-02-07 22:44:22.761248',161,1,1,'','Безопасность передвижения в темное время суток','','','',37,0,'','','','1 мощная линзованная фара',''),(269,'ZXT_3030.png','2021-02-07 22:44:31.654193','2021-02-07 22:44:48.219545',162,1,1,'','Уверенность в каждом километре','','','',37,0,'','','','<div>\r\n											<ul><li>Максимальная скорость до 38 км/ч</li><li>Дисковые тормоза с возможностью регулировки</li><li>Правильное распределение веса байка</li></ul></div>',''),(270,'ZXT_3036.png','2021-02-07 22:44:52.741900','2021-02-07 22:45:11.034880',163,1,1,'','Инновационный аккумулятор','','','',37,0,'','','','<div>\r\n											<ul><li>Позволяет проехать до 50 км на одном заряде</li><li>Аккумулятор не боится воды и влаги</li><li>Емкость АКБ возможно увеличить</li></ul>\r\n										</div>',''),(271,'ZXT_3039.png','2021-02-07 22:45:18.140766','2021-02-07 22:45:29.070000',164,1,1,'','Удобство и простота использования','','','',37,0,'','','','<div>\r\n											<ul><li>Большие, интуитивно понятные кнопки управления</li><li>Удобное переключение скоростей</li><li>Шкала бензобака показвает уровень заряда АКБ </li><li>Сигнализация</li></ul>\r\n										</div>',''),(272,'ower-1.png','2021-02-07 22:46:15.891568','2021-02-07 22:46:44.428239',122,1,1,'','Надежность и функциональность','','','',38,0,'','','','<div>\r\n											<ul><li>Прочная алюминиевая рама, выдерживающая вес до 130 кг</li><li>Быстрая система складывания</li><li>Антилюфт складного механизма</li><li>Надежная заводская защита АКБ от влаги и внешних воздействий</li></ul>\r\n										</div>',''),(278,'ower-2.png','2021-02-07 22:46:52.577531','2021-02-07 22:47:08.409853',165,1,1,'','Потрясающая динамика и комфорт','','','',38,0,'','','','<div>\r\n											<ul><li>11-дюймовые колеса с хорошей проходимостью</li><li>Фирменное мотор-колесо мощностью 800 Вт</li><li>Низкочувствительная мягкая подвеска</li></ul>\r\n										</div>',''),(279,'ower-3.png','2021-02-07 22:47:15.867095','2021-02-07 22:47:25.947087',166,1,1,'','Уверенность в каждом километре','','','',38,0,'','','','<div>\r\n											<ul><li>Максимальная скорость до 45 км/ч</li><li>Два дисковых тормоза</li></ul>\r\n										</div>',''),(280,'ower-4.png','2021-02-07 22:47:34.223101','2021-02-07 22:47:48.109739',167,1,1,'','Инновационный LI-ION аккумулятор','','','',38,0,'','','','<div>\r\n											<ul><li>Пробег до 55 км на одном заряде</li><li>АКБ с балансировочной платой</li><li>Производство TAIWAN</li></ul>\r\n										</div>',''),(281,'ower-5.png','2021-02-07 22:47:54.453137','2021-02-07 22:48:05.984846',168,1,1,'','Стиль и качество в одном продукте','','','',38,0,'','','','<div>\r\n											<ul><li>Сертифицированный товар</li><li>Стильный футуристический дизайн</li><li>Две фары NANOLED</li></ul>\r\n										</div>',''),(282,NULL,'2021-02-07 22:55:42.705177','2021-02-09 18:18:21.915181',169,1,1,'','Название компании','','','company_name',1,0,'','','White Siberia','',''),(299,'ower-1.png','2021-02-07 22:58:35.398525','2021-02-07 22:59:04.665482',122,1,1,'','Удобство и мобильность','','','',39,0,'','','','<div>\r\n											<ul><li>Замок можно закрепить на руле и всегда возить с собой</li><li>Не нужно запоминать пароль, просто воспользуйтесь ключом</li></ul>\r\n										</div>',''),(305,'ower-2.png','2021-02-07 22:59:08.664280','2021-02-07 22:59:24.615250',186,1,1,'','Универсальность и надежность','','','',39,0,'','','','<div>\r\n											<ul><li>Легкость крепления техники благодаря длинному тросу (120 см)</li><li>Надежность конструкции: замок толщиной 12 мм</li></ul>\r\n										</div>',''),(306,'ower-3.png','2021-02-07 22:59:32.290084','2021-02-07 22:59:46.477295',187,1,1,'','Большой срок службы','','','',39,0,'','','','<div>\r\n											<ul><li>Металлический трос покрыт резиновой водонепроницаемой оболочкой</li><li>Внутренности замка сделаны из нержавеющей российской стали</li></ul>\r\n										</div>',''),(307,'ower-1.png','2021-02-07 23:05:12.704915','2021-02-07 23:05:43.930875',122,1,1,'','Удобство и мобильность','','','',40,0,'','','','<div>\r\n											<ul><li>Замок легко закрепить на руле и всегда возить с собой</li><li>Невозможно потерять ключ: вы просто запоминаете пароль</li></ul>\r\n										</div>',''),(313,'ower-2.png','2021-02-07 23:05:47.611852','2021-02-07 23:06:08.478149',188,1,1,'','Универсальность и стиль','','','',40,0,'','','','<div>\r\n											<ul><li>Легкость крепления техники благодаря длинному тросу (120 см) </li><li>Надежность конструкции: замок толщиной 12 мм</li></ul>\r\n										</div>',''),(314,'ower-3.png','2021-02-07 23:06:16.505005','2021-02-07 23:06:30.020185',189,1,1,'','Большой срок службы','','','',40,0,'','','','<div>\r\n											<ul><li>Металлический трос покрыт резиновой водонепроницаемой оболочкой</li><li>Внутренности замка сделаны из нержавеющей российской стали</li></ul>\r\n										</div>',''),(315,'ower-3.png','2021-02-07 23:30:08.494929','2021-02-07 23:30:37.726522',122,1,1,'','Удобство и мобильность','','','',41,0,'','','','<div>\r\n											<ul><li>Держатель легко устанавливается на руль самоката, скутера или велосипеда</li><li>Больше нет необходимости доставать телефон во время движения: он всегда перед Вами</li><li>Подходит для телефонов высотой от 95 до 185 мм</li></ul>\r\n										</div>',''),(321,'ower-2.png','2021-02-07 23:30:41.218801','2021-02-07 23:30:56.565561',190,1,1,'','Долгий срок службы','','','',41,0,'','','','<div>\r\n											<ul><li>Держатель изготовлен из крепкого пластика</li><li>Крепление держателя имеет дополнительные резиновые прослойки для надежной фиксации</li></ul>\r\n										</div>',''),(322,'ower-1.png','2021-02-07 23:31:01.375666','2021-02-07 23:31:19.155150',191,1,1,'','Ориентированность на клиента','','','',41,0,'','','','Вся продукция поставляется в фирменной упаковке с подробной инструкцией на русском языке',''),(323,'ower-1.png','2021-02-07 23:31:57.693885','2021-02-07 23:32:31.667843',122,1,1,'','Удобство и мобильность','','','',42,0,'','','','<div>\r\n											<ul><li>Держатель легко устанавливается на руль самоката, скутера или велосипеда</li><li>Больше нет необходимости доставать телефон во время движения: он всегда перед Вами</li><li>Подходит для телефонов высотой от 95 до 185 мм</li></ul>\r\n										</div>',''),(329,'ower-2.png','2021-02-07 23:32:39.821102','2021-02-07 23:32:52.871092',192,1,1,'','Долгий срок службы','','','',42,0,'','','','<div>\r\n											<ul><li>Держатель изготовлен из крепкого пластика</li><li>Крепление держателя – хомут, который фиксируется с помощью резьбовой закрутки</li></ul>\r\n										</div>',''),(330,'ower-3.png','2021-02-07 23:33:00.835137','2021-02-07 23:33:12.947206',193,1,1,'','Ориентированность на клиента','','','',42,0,'','','','Вся продукция поставляется в фирменной упаковке с подробной инструкцией на русском языке',''),(332,'ower-1.png','2021-02-07 23:34:14.855149','2021-02-07 23:34:45.304728',122,1,1,'','Универсальность и надежность','','','',43,0,'','','','<div>\r\n											<ul><li>Сумка подходит для самокатов и для скутеров</li><li>Изготовлена из водонепроницаемого материала</li><li>Снабжена прочными ремнями для надежности крепления</li></ul>\r\n										</div>',''),(338,'ower-3.png','2021-02-07 23:34:48.832898','2021-02-07 23:35:07.386156',194,1,1,'','Хорошая вместимость','','','',43,0,'','','','<div>\r\n											<ul><li>Продуманная конструкция позволяет использовать весь внутренний объем на 100%</li><li>Наличие внутренних карманов для распределения содержимого </li></ul>\r\n										</div>',''),(339,'ower-2.png','2021-02-07 23:35:14.710180','2021-02-07 23:35:28.176229',195,1,1,'','Длительный срок службы','','','',43,0,'','','','<div>\r\n											<ul><li>Прочный износостойкий материал с защитой от влаги</li><li>Все крепления пришиты крепкой нитью и имеют двойную строчку</li></ul>\r\n										</div>',''),(346,'ower-1.png','2021-02-07 23:36:23.050922','2021-02-07 23:36:43.223174',196,1,1,'','Универсальность и надежность','','','',44,0,'','','','<div>\r\n											<ul><li>Сумка подходит для самокатов и для скутеров</li><li>Изготовлена из водонепроницаемого материала</li><li>Снабжена прочными ремнями для надежности крепления</li></ul>\r\n										</div>',''),(347,'ower-3.png','2021-02-07 23:36:50.486253','2021-02-07 23:37:01.450712',197,1,1,'','Хорошая вместимость','','','',44,0,'','','','<div>\r\n											<ul><li>Продуманная конструкция позволяет использовать весь внутренний объем на 100%</li><li>Наличие большого количества внутренних карманов для распределения содержимого </li></ul>\r\n										</div>',''),(348,'ower-2.png','2021-02-07 23:37:08.425631','2021-02-07 23:37:20.843585',198,1,1,'','Длительный срок службы','','','',44,0,'','','','<div>\r\n											<ul><li>Прочный износостойкий материал с защитой от влаги</li><li>Все крепления пришиты крепкой нитью и имеют двойную строчку</li></ul>\r\n										</div>',''),(349,'ower-3.png','2021-02-07 23:38:06.986604','2021-02-07 23:38:34.541325',122,1,1,'','Удобство и универсальность','','','',45,0,'','','','<div>\r\n											<ul><li>Два варианта зарядных устройств: на 48V и на 60V</li><li>Наличие разнообразных переходников для различного вида электротранспорта. В комплекте – один на Ваш выбор</li><li>Компактный размер, который обусловлен дорогостоящей начинкой </li></ul>\r\n										</div>',''),(355,'ower-2.png','2021-02-07 23:38:41.807371','2021-02-07 23:38:55.969338',199,1,1,'','Высокая скорость зарядки','','','',45,0,'','','','<div>\r\n											<ul><li>Высокая скорость: зарядка в 3 раза быстрее, чем обычно!</li><li>Безопасность для Вашей АКБ</li><li>Подходит для зарядки АКБ емкостью свыше 11 А</li><li>Бесшумная работа</li></ul>\r\n										</div>',''),(356,'ower-1.png','2021-02-07 23:39:03.677396','2021-02-07 23:39:15.361418',200,1,1,'','Длительный срок службы','','','',45,0,'','','','<div>\r\n											<ul><li>Благодаря качественному наполнению З/У прослужит до 8 лет</li><li>Срок службы переходников - до 10 лет</li></ul>\r\n										</div>',''),(357,'ower-3.png','2021-02-07 23:40:40.142090','2021-02-07 23:41:10.214315',122,1,1,'','Универсальная ручка для самокатов','','','',46,0,'','','','<div>\r\n											<ul><li>Подходит на все модели самокатов</li><li>Универсальные скобы-крепления входят в комплект</li></ul>\r\n										</div>',''),(363,'ower-2.png','2021-02-07 23:41:18.379381','2021-02-07 23:41:33.940039',201,1,1,'','Качество и удобство','','','',46,0,'','','','<div>\r\n											<ul><li>Ручка сделана из прочного металла</li><li>Мягкие нескользящие грипсы выполнены из каучука</li><li>Стильный и лаконичный дизайн не испортит внешний вид Вашего самоката</li></ul>\r\n										</div>',''),(364,'ower-1.png','2021-02-07 23:41:41.238352','2021-02-07 23:41:52.612568',202,1,1,'','Долгий срок службы','','','',46,0,'','','','<div>\r\n											<ul><li>Металл имеет трехслойную покраску для защиты от коррозии</li><li>Толстые слои нанесения краски для предотвращения сколов</li></ul>\r\n										</div>',''),(371,'ower-1.png','2021-02-07 23:49:34.734661','2021-02-07 23:49:55.371457',203,1,1,'','Удобство и мобильность','','','',47,0,'','','','<div>\r\n											<ul><li>Чехол можно сложить в специальный мешочек</li><li>Чехол изготовлен из водонепроницаемого материала 210D, который в 4 раза толще ткани, используемой для производства зонтов</li></ul>\r\n										</div>',''),(372,'ower-2.png','2021-02-07 23:50:02.834186','2021-02-07 23:50:16.473030',204,1,1,'','Большая вместимость и компактность','','','',47,0,'','','','<div>\r\n											<ul><li>Чехлы представлены в двух размерах (ХХL и XXXL) и подойдут как для трайков, так и для двухколесной техники</li><li>Каждый чехол имеет стропы, с помощью которых Вы можете закрепить его на технике</li></ul>\r\n										</div>',''),(373,'ower-3.png','2021-02-07 23:50:20.924359','2021-02-07 23:50:38.921908',205,1,1,'','Длительный срок службы','','','',47,0,'','','','<div>\r\n											<ul><li>Чехол изготовлен из крепкой, водонепроницаемой ткани</li><li>Предусмотрено отверстие для замка, чтобы защитить технику от краж</li></ul>\r\n										</div>',''),(384,'ower-1.png','2021-02-07 23:54:15.419807','2021-02-07 23:54:29.814273',206,1,1,'','Удобство и универсальность','','','',48,0,'','','','<div>\r\n											<ul><li>Комплект колес подходит на любые трайки CityCoco</li><li>В комплект входят 3 колеса на внедорожной резине с высоким профилем. Одно переднее и два задних</li><li>Устанавливаются легко и быстро</li></ul>\r\n										</div>',''),(387,'ower-2.png','2021-02-07 23:55:20.961848','2021-02-07 23:55:33.174349',207,1,1,'','Удобство и компактный размер','','','',48,0,'','','','<div>\r\n											<ul><li>Комплект упакован в толстый картонный ящик. В нем вы сможете оставлять колеса на хранение</li><li>Установка колес не требует специальных навыков</li></ul>\r\n										</div>',''),(388,'ower-3.png','2021-02-07 23:55:40.795463','2021-02-07 23:55:59.645393',208,1,1,'','Длительный срок службы','','','',48,0,'','','','<div>\r\n											<ul><li>Резина произведена на крупной фабрике Faiben, которая занимается производством резины для рынка Тайваня</li><li>Покрышки с высоким профилем износостойкие, предназначены для поездок по бездорожью</li><li>Диск стальной, окрашен порошковой краской</li></ul>\r\n										</div>',''),(397,'ower-1.png','2021-02-07 23:58:04.089138','2021-02-07 23:58:16.208586',209,1,1,'','Легко и просто','','','',49,0,'','','','<div>\r\n											<ul><li>Коврик закрепляется на «липучки», которые надежно фиксируют его на скутере</li><li>Процесс снятия коврика занимает не более 3 секунд!</li><li>Удобный доступ ко второму отсеку батареи</li></ul>\r\n										</div>',''),(398,'ower-2.png','2021-02-07 23:58:23.571089','2021-02-07 23:58:34.604292',210,1,1,'','Удобство использования','','','',49,0,'','','','<div>\r\n											<ul><li>Коврики изготовлен из ячеистого материала EVA, который легко вытряхивается, сохраняя Вашу технику в чистоте</li><li>Материал коврика не боится точечных нагрузок и не меняет форму даже при постоянных нагрузках</li><li>Коврик подходят для любого скутера класса CityCoco</li></ul>\r\n										</div>',''),(399,'ower-3.png','2021-02-07 23:58:41.304274','2021-02-07 23:58:53.412083',211,1,1,'','Длительный срок службы','','','',49,0,'','','','<div>\r\n											<ul><li>Коврик изготовлен из инновационного материала EVA</li><li>Материал водонепроницаемый и износостойкий</li><li>Все канты прошиты крепкой нитью и имеют двойную строчку</li></ul>\r\n										</div>',''),(401,NULL,'2021-02-09 19:37:12.035840','2021-02-09 19:37:28.278307',212,1,1,'_7','telegram','','https://t.me/WSIB7','telegram',1,0,'','','','',''),(402,NULL,'2021-02-09 19:37:31.460826','2021-02-09 19:37:51.565424',213,1,1,'_7','viber','','viber://chat?number=+79628848888','viber',1,0,'','','','',''),(403,NULL,'2021-02-10 18:53:17.886672','2021-02-10 18:55:01.718717',214,1,4,'','Главная страничка','','/','',13,0,'','','','',''),(404,NULL,'2021-02-10 19:30:20.007910','2021-02-10 22:29:05.772130',215,1,1,'','Footer (Подвал)','','','footer',1,0,'','','','',''),(405,NULL,'2021-02-10 19:30:25.486486','2021-02-10 19:30:49.943449',216,1,1,'_404','Россия','','','',1,0,'','','','<div>г. Москва, дер. Марушкино, ул. Северная</div>\r\n<div>г. Сочи, Адлерский р-н, ул. Садовая 48</div>',''),(406,NULL,'2021-02-10 19:30:26.444298','2021-02-10 22:02:25.638699',217,1,1,'_404','Оптовый отдел','','','',1,0,'','','','',''),(407,NULL,'2021-02-10 19:30:28.363859','2021-02-10 22:04:38.274539',218,1,1,'_404','Розничный отдел','','','',1,0,'','','','',''),(408,NULL,'2021-02-10 19:30:30.007080','2021-02-10 22:05:43.985596',219,1,1,'_404','Гарантийный отдел','','','',1,0,'','','','',''),(409,NULL,'2021-02-10 22:02:32.500790','2021-02-10 22:02:47.790491',220,1,1,'_404_406','Телефон','','','phone',1,0,'','','','<a href=\"tel:+79384704147\">+7 938 470 41 47</a>',''),(410,NULL,'2021-02-10 22:03:09.773289','2021-02-10 22:03:59.023300',221,1,1,'_404_406','WhatsApp','','','whatsapp',1,0,'','','','<a href=\"https://wa.me/79384704147\">+7 938 470 41 47</a>',''),(411,NULL,'2021-02-10 22:04:05.887346','2021-02-10 22:04:15.785400',222,1,1,'_404_406','Email','','','envelope',1,0,'','','','<a href=\"mailto:opt@white-siberia.com\"> opt@white-siberia.com</a>',''),(412,NULL,'2021-02-10 22:04:30.356955','2021-02-10 22:04:49.962687',223,1,1,'_404_407','Телефон','','','phone',1,0,'','','','<a href=\"tel:+79881691639\">+7 988 169 16 39</a>',''),(413,NULL,'2021-02-10 22:04:31.531742','2021-02-10 22:05:10.482609',224,1,1,'_404_407','WhatsApp','','','whatsapp',1,0,'','','','<a href=\"https://wa.me/79884038543\">+7 988 403 85 43</a>',''),(414,NULL,'2021-02-10 22:04:32.528056','2021-02-10 22:05:25.278201',225,1,1,'_404_407','Email','','','envelope',1,0,'','','','<a href=\"mailto:roznica@white-siberia.com\">roznica@white-siberia.com</a>',''),(415,NULL,'2021-02-10 22:05:33.506007','2021-02-10 22:05:53.784245',226,1,1,'_404_408','Телефон','','','phone',1,0,'','','','<a href=\"tel:+79890858745\">+7 989 085 87 45</a>',''),(416,NULL,'2021-02-10 22:05:34.745175','2021-02-10 22:06:09.045981',227,1,1,'_404_408','WhatsApp','','','whatsapp',1,0,'','','','<a href=\"https://wa.me/79890858745\">+7 989 085 87 45</a>',''),(417,NULL,'2021-02-10 22:05:36.011216','2021-02-10 22:06:22.359226',228,1,1,'_404_408','Email','','','envelope',1,0,'','','','<a href=\"mailto:guarantee@white-siberia.com\">guarantee@white-siberia.com</a>',''),(419,NULL,'2021-02-10 22:08:56.826440','2021-02-10 22:09:03.843278',229,1,1,'','Сообщества (Подвал)','','','social_footer',1,0,'','','','',''),(420,NULL,'2021-02-10 22:09:06.319897','2021-02-10 22:09:44.978998',230,1,1,'_419','Instagram','','https://www.instagram.com/ws_electro/','',1,1,'instagram','','','',''),(421,NULL,'2021-02-10 22:09:07.360663','2021-02-10 22:10:09.790755',231,1,1,'_419','Вконтакте','','https://vk.com/ws_electro','',1,1,'vk','','','',''),(422,NULL,'2021-02-10 22:09:08.978976','2021-02-10 22:10:39.750100',232,1,1,'_419','YouTube','','https://www.youtube.com/channel/UCLMxls9urKSgQdE7setOt9w','',1,0,'youtube','','','',''),(423,NULL,'2021-02-12 16:32:24.961578','2021-02-12 16:32:24.961598',99,1,1,'','video1','Перейти на YouTube','https://www.youtube.com/channel/UCLMxls9urKSgQdE7setOt9w','',50,1,'youtube-play','','','<iframe src=\"https://www.youtube.com/embed/u8Tx7XC5q8k\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" width=\"398\" height=\"199\" frameborder=\"0\"></iframe>',''),(424,NULL,'2021-02-12 16:32:24.964399','2021-02-12 16:32:24.964417',100,1,1,'','video2','','','',50,0,'','','','<iframe width=\"398\" height=\"199\" src=\"https://www.youtube.com/embed/L8OU9xwCUXE\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>',''),(425,NULL,'2021-02-12 16:32:24.965211','2021-02-12 16:32:24.965228',101,1,1,'','video3','','','',50,0,'','','','<iframe width=\"398\" height=\"199\" src=\"https://www.youtube.com/embed/t_l9If6U_J4\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>',''),(426,NULL,'2021-02-12 16:32:24.965980','2021-02-12 16:32:24.965996',102,1,1,'','video4','','','',50,0,'','','','<iframe src=\"https://www.youtube.com/embed/lfSkjl0Qu68\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen=\"\" width=\"398\" height=\"199\" frameborder=\"0\"></iframe>',''),(427,NULL,'2021-02-13 11:53:33.823032','2021-02-13 11:53:33.823056',233,1,1,'','Favicon','','','',1,0,'','','','',''),(428,'427.jpg','2021-02-13 11:53:42.050273','2021-02-13 11:53:42.050291',233,1,1,'','Favicon','','','favicon',1,0,'','','','','');
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
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flatcontent_containers`
--

LOCK TABLES `flatcontent_containers` WRITE;
/*!40000 ALTER TABLE `flatcontent_containers` DISABLE KEYS */;
INSERT INTO `flatcontent_containers` VALUES (1,NULL,'2021-02-02 22:12:05.720368','2021-02-02 22:12:05.720449',1,1,2,NULL,'Контент для всех страничек','Создан автоматически, выводит блоки, которые должны показываться на всех страничках, например, телефон или счетчики','main',NULL,NULL),(2,NULL,'2021-02-02 22:12:05.772969','2021-02-09 19:50:29.585506',2,1,1,'','Главное меню','Создано автоматически, выводит главное меню','mainmenu','',''),(3,NULL,'2021-02-02 22:12:05.775389','2021-02-02 22:12:05.775409',3,1,1,NULL,'Нижнее меню','Создано автоматически, выводит нижнее меню','bottommenu',NULL,NULL),(4,NULL,'2021-02-02 22:51:43.645139','2021-02-02 22:51:43.645157',4,1,99,'','Слайдер','','slider','',''),(5,NULL,'2021-02-02 23:48:34.781174','2021-02-02 23:48:34.781192',5,1,3,'','Слайдер','','slider','',''),(6,NULL,'2021-02-03 18:02:05.035173','2021-02-03 18:57:38.021571',6,1,99,'','О нас','О компании<br>','about','',''),(7,NULL,'2021-02-03 18:29:41.959743','2021-02-03 18:57:49.493352',7,1,3,'','О компании','О компании','about','',''),(8,NULL,'2021-02-03 18:55:23.457178','2021-02-03 18:57:23.205094',8,1,99,'','Статья - Темный фон','Добро пожаловать','article_dark','',''),(9,NULL,'2021-02-03 19:33:12.351152','2021-02-03 19:33:12.369063',9,1,3,'','Статья - Темный фон','Добро пожаловать','article_dark','',''),(10,NULL,'2021-02-03 19:42:57.320896','2021-02-03 19:44:31.606935',10,1,99,'','Написать  нам','Стать дилером','feedback','',''),(11,NULL,'2021-02-03 19:55:37.037308','2021-02-03 19:55:37.037330',11,1,99,'','Простая статья','Приватность','article','',''),(12,NULL,'2021-02-03 20:00:53.469339','2021-02-03 20:00:53.477503',12,1,3,'','Политика в отношении обработки персональных данных','Приватность','article','',''),(13,NULL,'2021-02-03 20:01:13.247973','2021-02-03 20:01:13.247995',13,1,1,'','Скрытое меню','','','',''),(14,NULL,'2021-02-03 20:04:23.357301','2021-02-03 20:04:23.363852',14,1,3,'','Стать дилером','Стать дилером','feedback','',''),(15,NULL,'2021-02-03 20:07:40.020998','2021-02-03 20:10:08.974800',15,1,3,'','О компании','О компании','article','',''),(16,NULL,'2021-02-03 20:51:52.758722','2021-02-03 20:52:11.173989',16,1,99,'','Контакты','Контакты<br>','contacts','',''),(17,NULL,'2021-02-03 21:20:50.339640','2021-02-03 21:20:50.346422',17,1,3,'','Контакты','Контакты<br>','contacts','',''),(18,NULL,'2021-02-05 10:41:12.579944','2021-02-05 11:02:42.437728',18,1,99,'','Дилеры','Дилеры<br>','dealers','',''),(19,NULL,'2021-02-05 12:18:52.125623','2021-02-05 12:18:52.132598',19,1,3,'','Дилеры','Дилеры<br>','dealers','',''),(21,NULL,'2021-02-05 18:04:20.545205','2021-02-05 18:04:46.239730',21,1,7,'','Каталог товаров','','catalogue','',''),(22,NULL,'2021-02-05 18:06:34.776126','2021-02-05 18:06:34.776149',22,1,4,NULL,'Сео-тексты для товаров/услуг',NULL,'seo_for_products',NULL,NULL),(23,NULL,'2021-02-06 13:51:34.932110','2021-02-06 13:51:34.932129',23,1,99,'','Каталог','','catalogue','',''),(24,NULL,'2021-02-06 15:57:56.675752','2021-02-06 15:57:56.675773',24,1,3,'','Каталог','','catalogue','',''),(25,'surron.png','2021-02-06 16:26:11.829397','2021-02-06 16:29:01.420645',25,1,99,'','Заголовок','','call_to_action','',''),(26,'surron.png','2021-02-06 16:40:04.238357','2021-02-06 16:40:04.248517',26,1,3,'','SUR-RON','','call_to_action','',''),(27,NULL,'2021-02-06 17:21:24.672179','2021-02-06 17:34:39.813920',27,1,99,'','Видео','Обзоры техники','videos','',''),(28,NULL,'2021-02-06 17:34:12.520101','2021-02-06 17:34:28.898077',28,1,3,'','Обзоры техники','Обзоры техники','videos','',''),(29,NULL,'2021-02-07 19:57:06.145134','2021-02-07 19:57:06.145152',29,1,99,'','Статья (Вариант 2)','','article2','',''),(30,NULL,'2021-02-07 20:16:37.417855','2021-02-07 20:16:37.417873',30,1,3,'','Обзор на WS-PRO TRIKE+ 3000W','','article2','',''),(31,NULL,'2021-02-07 22:13:53.092830','2021-02-07 22:13:53.092848',31,1,3,'','Обзор на WS-PRO MAX+ 3000W','','article2','',''),(32,NULL,'2021-02-07 22:18:52.215860','2021-02-07 22:18:52.215878',32,1,3,'','Обзор на WS-PRO 2WD 4000W','','article2','',''),(33,NULL,'2021-02-07 22:26:00.383585','2021-02-07 22:26:00.383647',33,1,3,'','Обзор на WS-WILD WHEEL 3000W','','article2','',''),(34,NULL,'2021-02-07 22:29:44.226913','2021-02-07 22:29:48.989743',34,1,3,'','Обзор на WS-PRO+ 2500W','','article2','',''),(35,NULL,'2021-02-07 22:35:34.233813','2021-02-07 22:35:40.012430',35,1,3,'','Обзор на WS-PRO LIGHT 2000W','','article2','',''),(36,NULL,'2021-02-07 22:38:44.795829','2021-02-07 22:38:48.401390',36,1,3,'','Обзор на WS-MINI R 1200W','','article2','',''),(37,NULL,'2021-02-07 22:43:03.093874','2021-02-07 22:43:03.093894',37,1,3,'','Обзор на WS-SOCHI 1300W','','article2','',''),(38,NULL,'2021-02-07 22:46:11.308169','2021-02-07 22:46:15.872935',38,1,3,'','Обзор на WS-TAIGA 800W','','article2','',''),(39,NULL,'2021-02-07 22:58:35.364525','2021-02-07 22:58:35.364542',39,1,3,'','Обзор на LOCKER 1.0','','article2','',''),(40,NULL,'2021-02-07 23:05:12.660825','2021-02-07 23:05:12.660844',40,1,3,'','Обзор на LOCKER 2.0','','article2','',''),(41,NULL,'2021-02-07 23:30:02.712399','2021-02-07 23:30:08.484251',41,1,3,'','Обзор на WS-PHONE HOLDER 1.0','','article2','',''),(42,NULL,'2021-02-07 23:31:57.685787','2021-02-07 23:31:57.685805',42,1,3,'','WS-PHONE HOLDER 2.0','','article2','',''),(43,NULL,'2021-02-07 23:34:14.846701','2021-02-07 23:34:14.846717',43,1,3,'','Обзор на WS-URBAN 3L','','article2','',''),(44,NULL,'2021-02-07 23:36:10.218250','2021-02-07 23:36:10.218271',44,1,3,'','Обзор на WS-URBAN 5L','','article2','',''),(45,NULL,'2021-02-07 23:38:03.392190','2021-02-07 23:38:06.952994',45,1,3,'','Обзор на WS-FAST CHARGER 5A','','article2','',''),(46,NULL,'2021-02-07 23:40:35.034431','2021-02-07 23:40:40.133337',46,1,3,'','Обзор на WS-KIDS HOLDER','','article2','',''),(47,NULL,'2021-02-07 23:42:29.344801','2021-02-07 23:42:33.491395',47,1,3,'','Обзор на WS-RAIN COVER','','article2','',''),(48,NULL,'2021-02-07 23:51:14.144352','2021-02-07 23:51:18.070004',48,1,3,'','Обзор на WS-OFFROAD EVOLUTION','','article2','',''),(49,NULL,'2021-02-07 23:57:49.123578','2021-02-07 23:57:53.023037',49,1,3,'','Обзор на EVA-коврик','','article2','',''),(50,NULL,'2021-02-12 16:32:24.948624','2021-02-12 16:32:24.957979',50,1,3,'','Тест - привязка видео к товару','Обзоры техники','videos','','');
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
INSERT INTO `flatcontent_linkcontainer` VALUES (7,NULL,'2021-02-03 20:02:14.981433','2021-02-03 20:02:14.981463',4,1,NULL,NULL,64,12),(8,NULL,'2021-02-03 20:04:33.192381','2021-02-03 20:04:33.192401',5,1,NULL,NULL,34,14),(9,NULL,'2021-02-03 20:08:53.668792','2021-02-03 20:08:53.668812',6,1,NULL,NULL,30,15),(10,NULL,'2021-02-03 20:08:53.671529','2021-02-03 20:08:53.671549',7,1,NULL,NULL,30,7),(11,NULL,'2021-02-03 21:21:00.690884','2021-02-03 21:21:00.690906',8,1,NULL,NULL,33,17),(12,NULL,'2021-02-05 12:19:04.871726','2021-02-05 12:19:04.871746',9,1,NULL,NULL,32,19),(32,NULL,'2021-02-06 18:21:08.548157','2021-02-06 18:21:08.548176',16,1,NULL,NULL,31,24),(34,NULL,'2021-02-07 21:41:01.462903','2021-02-07 21:41:01.462921',0,1,NULL,NULL,151,30),(35,NULL,'2021-02-07 22:17:25.350831','2021-02-07 22:17:25.350850',18,1,NULL,NULL,162,31),(36,NULL,'2021-02-07 22:22:03.531551','2021-02-07 22:22:03.531567',19,1,NULL,NULL,163,32),(37,NULL,'2021-02-07 22:29:19.055767','2021-02-07 22:29:19.055789',20,1,NULL,NULL,164,33),(38,NULL,'2021-02-07 22:33:39.102434','2021-02-07 22:33:39.102454',21,1,NULL,NULL,165,34),(39,NULL,'2021-02-07 22:38:24.708796','2021-02-07 22:38:24.708817',22,1,NULL,NULL,166,35),(40,NULL,'2021-02-07 22:41:53.469322','2021-02-07 22:41:53.469339',23,1,NULL,NULL,167,36),(41,NULL,'2021-02-07 22:45:44.784865','2021-02-07 22:45:44.784881',24,1,NULL,NULL,168,37),(42,NULL,'2021-02-07 22:48:23.296326','2021-02-07 22:48:23.296346',25,1,NULL,NULL,169,38),(43,NULL,'2021-02-07 23:00:05.000094','2021-02-07 23:00:05.000113',0,1,NULL,NULL,170,39),(44,NULL,'2021-02-07 23:29:45.157180','2021-02-07 23:29:45.157197',26,1,NULL,NULL,171,40),(45,NULL,'2021-02-07 23:31:43.825928','2021-02-07 23:31:43.825949',27,1,NULL,NULL,172,41),(46,NULL,'2021-02-07 23:33:32.794417','2021-02-07 23:33:32.794438',28,1,NULL,NULL,173,42),(47,NULL,'2021-02-07 23:35:49.985573','2021-02-07 23:35:49.985603',29,1,NULL,NULL,174,43),(48,NULL,'2021-02-07 23:37:45.815132','2021-02-07 23:37:45.815151',30,1,NULL,NULL,175,44),(49,NULL,'2021-02-07 23:40:17.260807','2021-02-07 23:40:17.260823',31,1,NULL,NULL,176,45),(50,NULL,'2021-02-07 23:42:11.079408','2021-02-07 23:42:11.079426',32,1,NULL,NULL,177,46),(51,NULL,'2021-02-07 23:50:56.613062','2021-02-07 23:50:56.613079',33,1,NULL,NULL,178,47),(52,NULL,'2021-02-07 23:57:33.484525','2021-02-07 23:57:33.484541',34,1,NULL,NULL,179,48),(53,NULL,'2021-02-07 23:59:18.966813','2021-02-07 23:59:18.966832',35,1,NULL,NULL,180,49),(72,NULL,'2021-02-10 18:55:01.725147','2021-02-10 18:55:01.725168',36,1,NULL,NULL,403,5),(73,NULL,'2021-02-10 18:55:01.727771','2021-02-10 18:55:01.727789',37,1,NULL,NULL,403,7),(74,NULL,'2021-02-10 18:55:01.731607','2021-02-10 18:55:01.731629',38,1,NULL,NULL,403,9),(75,NULL,'2021-02-10 18:55:01.735301','2021-02-10 18:55:01.735320',39,1,NULL,NULL,403,24),(76,NULL,'2021-02-10 18:55:01.736713','2021-02-10 18:55:01.736762',40,1,NULL,NULL,403,26),(77,NULL,'2021-02-10 18:55:01.738292','2021-02-10 18:55:01.738311',41,1,NULL,NULL,403,28),(78,NULL,'2021-02-12 16:32:53.116097','2021-02-12 16:32:53.116122',1,1,NULL,NULL,151,50);
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
INSERT INTO `login_customuser` VALUES (1,NULL,'2021-02-02 21:42:08.154189','2021-02-13 11:21:51.006418',1,1,NULL,NULL,NULL,NULL,1),(2,NULL,'2021-02-03 00:08:37.610052','2021-02-03 00:08:41.475744',2,1,NULL,NULL,'','',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_products`
--

LOCK TABLES `products_products` WRITE;
/*!40000 ALTER TABLE `products_products` DISABLE KEYS */;
INSERT INTO `products_products` VALUES (1,'ZXT_5840.jpg','2021-02-05 18:06:34.719967','2021-02-12 16:32:53.076275',1,1,NULL,'','WS-PRO TRIKE+ 3000W','','','',NULL,NULL,109900.00,'','Лучший выбор загородной жизни','<div>\r\n					<h3>WS-PRO TRIKE+ 3000W</h3>\r\n<p>Самый мощный и комфортный трицикл на российском рынке. Безопасный и \r\nнадежный, он станет незаменимым помощником для людей, постоянно или \r\nсезонно проживающих за городом. Благодаря большой грузоподъемности (260 \r\nкг) и емкой АКБ, трицикл идеально подойдет для длительных поездок в \r\nмагазин, в лес за грибами или ягодами, на рыбалку или для любых приятных\r\n прогулок.</p>\r\n<p> \r\nПредустановленная АКБ WS-PRO TRIKE+ 3000W позволит Вам проехать до 60 км\r\n на одном заряде. Хотите увеличить дальность пробега? Легко! Просто \r\nустановите второй аккумулятор, и проезжайте до 100 км без дополнительной\r\n подзарядки.</p>\r\n<p>\r\nОбратите внимание на повышенную износостойкость данной модели: она \r\nпрекрасно адаптируется к любым дорогам и погодным условиям, а при \r\nустановке зимней резины трайк становится всесезонным.</p>\r\n<p>\r\nМодель «+» получила повышенный клиренс и новую настраиваемую подвеску, \r\nкоторые особенно порадуют тех, кто планирует передвигаться по грунтовым \r\nдорогам и серьезному бездорожью. \r\n</p>\r\n<h3>Редукторный мотор</h3>\r\n<p>На данной модели имеет мощность 3000 Вт и относится к тяговому типу \r\nдвигателей. Новая версия, в отличие от старой, имеет сертификат ECC \r\n(европейский стандарт) и относится к категории самых дорогих редукторных\r\n моторов, выпускаемых на данный момент. Максимальная скорость составляет\r\n 50 км/ч, в зависимости от веса райдера, рельефа и погодных условий.</p>\r\n<h3>Оптика</h3>\r\n<p>Состоит из светодиодных ламп. LED-оптика яркая, заметная и потребляет\r\n электричество экономно. Она обеспечивает отличное освещение и \r\nбезопасность при движении на дорогах. </p>\r\n<h3>Эргономика</h3>\r\n<p>Стоит обратить внимание на ручки газа, которые сделаны из алюминия с \r\nкаучуковой прослойкой. Ручки тормоза имеют возможность настройки \r\nфиксации в удобном для ваших пальцев положении. Кнопки переключения \r\nскоростей и света выполнены в классическом стиле.</p>\r\n<h3>Пробег</h3>\r\n<p>Скутер может проехать до 100 км на одном заряде при установке двух \r\nбатарей. В комплектации с предустановленной АКБ — до 60 км. Батарея \r\nсертифицирована и обладает умной BMS платой 40A, которая защищает АКБ от\r\n перезаряда и перегрузок, тем самым продлевая срок службы в циклах.</p>\r\n<h3>Посадка</h3>\r\n<p>Классическое сиденье, единое для всей линейки моделей WS. Оно мягкое,\r\n широкое, удобное и прекрасно подходит для длительных поездок. Верх \r\nсиденья отделан прочной и долговечной эко-кожей, которая устойчива к \r\nвоздействию влаги и ультрафиолета.</p>\r\n<h3>Бокс</h3>\r\n<p>Выполнен из прочного пластика. Держатель бокса рассчитан на нагрузку \r\nдо 50 кг., а верхняя крышка оснащена надежным фиксатором. В корпус \r\nвстроен катафот и предусмотрено место для установки дополнительного \r\nсвета. При желании, Вы можете демонтировать бокс и установить на его \r\nместо классическую спинку для второго пассажира, которая идет в \r\nкомплекте.</p>\r\n<h3>Бортовой компьютер</h3>\r\n<p>На модели установлен большой LED-дисплей, отображающий скорость, заряд батареи, индикатор света и пройденную дистанцию.</p>\r\n<h3>Колеса</h3>\r\n<p>10-дюймовые колеса с низким профилем выглядят стильно, а за счет \r\nширины и профиля покрышек отлично держат дорогу и уверенно останавливают\r\n электробайк. Отдельный плюс данной модели: Вы можете заменить штатную \r\nрезину на зимнюю или поставить комплект грязевой резины на 8-дюймовых \r\nдисках для передвижения осенью, зимой и ранней весной.</p>				</div>','1',NULL,109900.00,109900.00,NULL,NULL),(2,'20_1.jpg','2021-02-06 18:30:24.991768','2021-02-07 22:17:25.339648',2,1,NULL,'','WS-PRO MAX+ 3000W','','','',NULL,NULL,106900.00,'','Любитель скорости и новых впечатлений','<div>\r\n					<h3>WS-PRO MAX 3000W</h3>\r\n<p>Флагманская модель от компании WS-ELECTRO вышла на рынок стран СНГ в \r\nконце 2019 года и еще около полугода тщательно дорабатывалась инженерами\r\n компании WSE, чтобы стать поистине идеальным экземпляром в классе \r\nCityCoco. Маневренный и мощный электробайк способен развить скорость до \r\n71 км/ч, а особая настройка контроллера позволяет 3000-ваттному \r\nмотор-колесу при меньшем потреблении энергии выдавать результат \r\nдвигателей мощностью 4000 Вт. </p>\r\n<h3>Оптика</h3>\r\n<p>Состоит из светодиодных ламп. LED-оптика яркая, заметная и потребляет\r\n электричество экономно. Она обеспечивает отличное освещение и \r\nбезопасность при движении на дорогах.</p>\r\n<h3>Эргономика</h3>\r\n<p>Обратите внимание на ручки газа, которые выполнены из алюминия, \r\nстильно покрашенного в красный цвет, и имеют прослойку из каучука. \r\nНастраиваемые ручки тормоза позволят Вам подобрать идеально удобное \r\nположение. Интуитивно понятные кнопки переключения скоростей и света \r\nвыполнены в классическом стиле. </p>\r\n<h3>Пробег</h3>\r\n<p>Байк может проехать до 100 км на одном заряде при установке двух \r\nбатарей. В стандартной комплектации с одной АКБ — до 60 км. Батарея \r\nсертифицирована и обладает умной BMS платой 40A, которая защищает АКБ от\r\n перезаряда и перегрузки. </p>\r\n<h3>Посадка</h3>\r\n<p>Классическое сиденье, единое для всей линейки моделей WS. Оно мягкое,\r\n широкое, удобное и прекрасно подходит для длительных поездок. Верх \r\nсиденья отделан прочной и долговечной эко-кожей, которая устойчива к \r\nвоздействию влаги и ультрафиолета. </p>\r\n<h3>Бокс</h3>\r\n<p>Бокс выполнен из прочного пластика и снабжен дополнительным \r\nфиксатором верхней крышки. Усиленный держатель бокса способен выдержать \r\nнагрузку до 50 кг. В корпус встроен катафот и предусмотрено место для \r\nустановки дополнительного света. Вы можете демонтировать бокс и \r\nустановить на его место классическую спинку для второго пассажира, \r\nкоторая идет в комплекте.</p>\r\n<h3>Бортовой компьютер</h3>\r\n<p>На модели установлен большой LED-дисплей, отображающий скорость, заряд батареи, индикатор света и пройденную дистанцию. </p>\r\n<h3>Колеса</h3>\r\n<p>12-дюймовые колеса являются самыми большими для скутеров класса \r\nCityCoco. Они позволяют проезжать любые неровности на дорогах \r\nпрактически незаметно. На них установлена резина с низким профилем, \r\nкоторая идеально подходит для скоростной езды. </p>				</div>','2',NULL,106900.00,106900.00,NULL,NULL),(3,'6.jpg','2021-02-07 11:39:18.762354','2021-02-07 22:22:03.505865',3,1,NULL,'','WS-PRO 2WD 4000W','','','',NULL,NULL,104900.00,'','Покоритель бездорожья','<div>\r\n					<h3>WS-PRO 2WD 4000w</h3>\r\n<p>Первый полноприводный скутер класса CityCoco на рынке стран СНГ. Два \r\nмотор-колеса мощностью 2000 Вт (суммарная мощность 4000 Вт) в сочетании с\r\n полным приводом и 8-дюймовыми колесами позволят Вам преодолеть \r\nпересеченную местность без проблем и забот. Данная модель станет лучшим \r\nвыбором для охотников, рыболовов и любителей путешествий по бездорожью. В\r\n кофре Вы без проблем уместите габаритный груз, а в бардачок под \r\nсиденьем сможете положить документы, деньги и другие ценные вещи. Эта \r\nпрактичная и стильная модель непременно порадует Вас и подарит множество\r\n приятных поездок как в условиях города, так и за его пределами. </p>\r\n<h3>Оптика</h3>\r\n<p>Состоит из светодиодных ламп. LED-оптика яркая, заметная и потребляет\r\n электричество экономно. Она обеспечивает отличное освещение и \r\nбезопасность при движении на дорогах.</p>\r\n<h3>Эргономика</h3>\r\n<p>Ручки газа выполнены из алюминия с каучуковым покрытием, прочным и \r\nпрочным на ощупь. Настраиваемые ручки тормоза позволяют подобрать \r\nидеально удобное положение. Интуитивно понятные кнопки переключения \r\nскоростей и света выполнены в классическом стиле. </p>\r\n<h3>Пробег</h3>\r\n<p>Скутер может проехать до 80 км на одном заряде при комплектации двумя\r\n батареями. При классической комплектации одной батарей — до 50 км. \r\nБатарея сертифицирована и обладает умной BMS платой 40A, которая \r\nзащищает АКБ от перезаряда и перегрузки.</p>\r\n<h3>Посадка</h3>\r\n<p>Классическое сиденье, единое для всей линейки моделей WS. Оно мягкое,\r\n широкое, удобное и прекрасно подходит для длительных поездок. Верх \r\nсиденья отделан прочной и долговечной эко-кожей, которая устойчива к \r\nвоздействию влаги и ультрафиолета. </p>\r\n<h3>Бокс</h3>\r\n<p>Бокс выполнен из прочного пластика и снабжен дополнительным \r\nфиксатором верхней крышки. Усиленный держатель бокса способен выдержать \r\nнагрузку до 50 кг.<br>В корпус встроен катафот и предусмотрено место для\r\n установки дополнительного света. Вы можете демонтировать бокс и \r\nустановить на его место классическую спинку для второго пассажира, \r\nкоторая идет в комплекте.</p>\r\n<h3>Бортовой компьютер</h3>\r\n<p>На модели установлен большой LED-дисплей, отображающий скорость, заряд батареи, индикатор света и пройденную дистанцию. </p>\r\n<h3>Колеса</h3>\r\n<p>В стандартной комплектации поставляется на 8-дюймовых колесах с \r\nдорожной резиной. Для поездок по пересеченной местности и серьезного \r\nбездорожья рекомендуется установка комплекта грязевой резины. </p>\r\n				</div>','3',NULL,104900.00,104900.00,NULL,NULL),(4,'1r.jpg','2021-02-07 11:55:59.982738','2021-02-07 22:29:19.042615',4,1,NULL,'','WS-WILD WHEEL 3000W','','','',NULL,NULL,118900.00,'','Стильный путешественник','<div>\r\n					<h3>WS-WILD WHEEL 3000w</h3>\r\n<p>WS-WILD WHEEL 3000w — стильный электробайк, выполненный в духе \r\nклассических мотоциклов-круизеров. Его дизайн создан, чтобы притягивать \r\nвосхищенные взгляды окружающих! Отличительные черты данной модели: \r\nудобная посадка с низким расположением сиденья для комфорта в длительных\r\n путешествиях, хорошая динамика в потоке и внушительный пробег до 100 км\r\n без подзарядки. Обновленная тормозная система подарит Вам уверенность в\r\n каждом километре как на асфальтированной трассе, так и на грунтовых \r\nдорогах, а грузоподъемность до 220 кг, вместительный бокс и три кофра \r\nпозволят взять в путешествие все, что Вы запланируете. </p>\r\n<h3>Контроллер</h3>\r\n<p>На модели установлен контроллер 60V 3000W 50A. Особая настройка \r\nконтроллера позволяет 3000-ваттному мотор-колесу при меньшем потреблении\r\n энергии выдавать результат двигателей мощностью 4000 Вт. <br>Максимальная скорость — до 71 км/ч</p>\r\n<h3>Оптика</h3>\r\n<p>Светодиодная (LED) оптика отличается яркостью, делает скутер заметным\r\n на дороге в любое время суток и экономно потребляет электричество. Она \r\nобеспечивает отличное освещение даже при езде ночью. </p> \r\n<h3>Эргономика</h3>\r\n<p>Ручки газа сделаны из мягкого и прочного каучука. Ручки тормоза с \r\nвозможностью вариативных настроек позволяют подобрать идеально удобное \r\nположение для пальцев рук райдера. Кнопки управления — большие и \r\nинтуитивно понятные. </p>\r\n<h3>Пробег</h3>\r\n<p>Скутер может проехать до 100 км на одном заряде при установке двух \r\nбатарей. В комплектации с предустановленной АКБ — до 60 км. Батарея \r\nсертифицирована и обладает умной BMS платой 40A, которая защищает АКБ от\r\n перезаряда и перегрузки, тем самым продлевая срок службы в циклах.</p>\r\n<h3>Посадка</h3>\r\n<p>Благодаря удлиненному рулю и низкому расположению сиденья данная \r\nмодель имеет классическую посадку в стиле чопперов. Это позволяет \r\nвладельцу скутера преодолевать километр за километром без усталости. \r\nМягкое и широкое кресло из эко-кожи также способствует комфорту во время\r\n длительной езды. </p>\r\n<h3>Бортовой компьютер</h3>\r\n<p>WS-WILD WHEEL 3000w оснащен бортовым компьютером с двойным \r\nLED-дисплеем. Он отображает скорость, заряд батареи, индикатор света, а \r\nтакже общую дистанция и километраж последней поездки.</p>\r\n<h3>Колеса</h3>\r\n<p>12-дюймовые колеса отлично подходят для преодоления бордюров и \r\nстабилизации байка при езде по неровным дорогам. На модели установлено \r\nширокое заднее колесо для лучшего сцепления с дорогой. </p>\r\n				</div>','4',NULL,118900.00,118900.00,NULL,NULL),(5,'1b.jpg','2021-02-07 12:24:33.650528','2021-02-07 22:33:39.089246',5,1,NULL,'','WS-PRO+ 2500W','','','',NULL,NULL,89900.00,'','Выносливый и неприхотливый','<div>\r\n					<h3>WS-PRO+ 2500W</h3>\r\n<p>WS-PRO+ 2500 - стильный, маневренный и доступный электробайк, который\r\n станет незаменимым помощником как в городе, так и за его пределами. \r\nЭтот универсальный, легкий и крепкий байк готов проехать до 60 км без \r\nдополнительной подзарядки АКБ. Обратите внимание на возможность \r\nодновременной установки трех (!) АКБ, что даст Вам возможность проезжать\r\n до 150 км без дополнительной подзарядки АКБ. Путешествуйте и совершайте\r\n поездки на работу, учебу или по другим делам, не опасаясь израсходовать\r\n заряд. Фирменное мотор-колесо на 2500W обладает отличной тяговитостью и\r\n позволяет развивать скорость до 60 км\\ч. Из приятных дополнений: \r\nбольшое мягкое сидение, 10-дюймовые колеса повышенной проходимости с \r\nуниверсальным протектором,  вместительный бокс из прочного пластика с \r\nдополнительным фиксатором верхней крышки.</p>\r\n<h3>Оптика</h3>\r\n<p>Состоит из светодиодных ламп. LED-оптика яркая, заметная и потребляет\r\n электричество экономно. Она обеспечивает отличное освещение и \r\nбезопасность при движении на дорогах.\r\n</p>\r\n<h3>Эргономика</h3>\r\n<p>Каучуковые грипсы приятны на ощупь и препятствуют проскальзыванию. \r\nНастраиваемые ручки тормоза позволят Вам подобрать идеально удобное \r\nположение. Интуитивно понятные кнопки переключения скоростей и света \r\nвыполнены в классическом стиле.</p>\r\n<h3>Пробег</h3>\r\n<p>Байк может проехать до 150 км на одном заряде при установке трех \r\nбатарей. В стандартной комплектации с одной АКБ - до 60 км. Батарея \r\nсертифицирована и обладает умной BMS платой 40A, которая защищает АКБ от\r\n перезаряда и перегрузки.\r\n</p>\r\n<h3>Посадка</h3>\r\n<p>В этой моделе установлено новое анатомическе сиденье от компании WS. \r\nОно мягкое, широкое, удобное и прекрасно подходит для длительных \r\nпоездок. Верх сиденья отделан прочной и долговечной эко-кожей, которая \r\nустойчива к воздействию влаги и ультрафиолета. Большой плюс этого \r\nсиденья- оно повторяет анатомию вашего тела, что дает поездке \r\nдополнительный комфорт.</p>\r\n<h3>Бокс</h3>\r\n<p>Бокс выполнен из прочного пластика и снабжен дополнительным \r\nфиксатором верхней крышки. Держатель бокса с усилением. Он позволит \r\nвыдержать нагрузку до 30 кг.</p>\r\n<h3>Бортовой компьютер</h3>\r\n<p>ННа модели установлен большой LED-дисплей, отображающий скорость, \r\nзаряд батареи, индикатор света и пройденную дистанцию. Дисплей большой и\r\n с функцией антиблик.</p>\r\n<h3>Колеса</h3>\r\n<p>10-дюймовые колеса с универсальным протектором показывают отличную \r\nпроходимость за пределами городских дорог, а также демонстрируют \r\nотличные характеристики на асфальте, в том числе в дождливую погоду. </p>				</div>','5',NULL,89900.00,89900.00,NULL,NULL),(6,'6.jpg','2021-02-07 13:06:53.994597','2021-02-07 22:38:24.697110',6,1,NULL,'','WS-PRO LIGHT 2000W','','','',NULL,NULL,73900.00,'','Легкий и маневренный','<div>\r\n					<h3>WS-PRO LIGHT 2000W</h3>\r\n<p>Самая легкая модель класса CityCoco от компании WS-ELECTRO: он весит \r\nвсего 70 кг! Данный байк спроектирован инженерами WS для универсальной \r\nэксплуатации. Маленький вес делает его маневренным, наличие корзины — \r\nпрактичным, а возможность установки внедорожных колес — еще и \r\nуниверсальным транспортным средством. Отличный запас хода, надежность и \r\nнеприхотливость позволили WS-PRO LIGHT 2000W стать бестселлером в \r\nсегменте легких скутеров форм-фактора CityCoco. </p>\r\n<h3>Эргономика</h3>\r\n<p>Тормозные ручки имеют анатомическую форму. Ручка газа с мягкой \r\nгрипсой защищает от проскальзывания и делает поездку более безопасной. \r\nКнопки включения света и переключатели скоростей выполнены в \r\nклассическом, интуитивно понятном дизайне. </p>\r\n<h3>Пробег</h3>\r\n<p>Скутер может проехать до 60 км на одном заряде. Батарея \r\nсертифицирована и обладает умной BMS платой 40A, которая защищает \r\nэлементы питания от перезаряда и перегрузки. </p>\r\n<h3>Посадка</h3>\r\n<p>Классическое сиденье, единое для всей линейки моделей WS. Оно мягкое,\r\n широкое, удобное и прекрасно подходит для длительных поездок. Верх \r\nсиденья отделан прочной и долговечной эко-кожей, которая устойчива к \r\nвоздействию влаги и ультрафиолета. </p>\r\n<h3>Корзина</h3>\r\n<p>WS-PRO LIGHT 2000w на момент 2020 года — единственная модель в \r\nлинейке WS, которая оснащена передней корзиной. Благодаря \r\nвместительности и прочному каркасу в нее можно положить покупки или \r\nдругие полезные вещи весом не более 30 кг. </p>\r\n<h3>Бортовой компьютер</h3>\r\n<p>Данная модель укомплектована универсальным головным устройством. Узел\r\n сочетает в себе фару, замок зажигания и дисплей, на который выводится \r\nинформация о скорости, заряде батареи и пробеге. Активация байка \r\nпроизводится поворотом ключа на первое деление. При повороте на второе \r\nделение включается головной свет.</p>\r\n<h3>Колеса</h3>\r\n<p>8-дюймовые колеса с высоким профилем помогают смягчить любые \r\nнеровности дороги. При желании, Вы можете установить комплект зимней или\r\n грязевой резины и сделать эксплуатацию электробайка круглогодичной.</p>				</div>','6',NULL,73900.00,73900.00,NULL,NULL),(7,'1r.jpg','2021-02-07 13:15:30.049147','2021-02-07 22:41:53.218614',7,1,NULL,'','WS-MINI R 1200W','','','',NULL,NULL,46900.00,'','Компактный, но очень удобный','<div>\r\n					<h3>WS-MINI R 1200w</h3>\r\n<p>Компактная двухместная модель класса CityCoco весом всего 40 кг! Этот\r\n легкий и маневренный электробайк спроектирован инженерами WS для \r\nуниверсальной эксплуатации в городской среде и за ее пределами. \r\n6,5-дюймовые колеса с высоким профилем и настраиваемая подвеска \r\nпозволяют райдеру чувствовать себя комфортно на любых дорогах. \r\nМини-ситикоко можно модифицировать под Ваши потребности: скутер \r\nстандартно комплектуется сиденьем с мягкой спинкой для пассажира и \r\nвместительной корзиной. Что устанавливать — решать только Вам! Прямая \r\nпосадка и мягкое сиденье помогают преодолевать любые расстояния без \r\nусталости, а переносную батарею удобно брать с собой для подзарядки. </p>\r\n<h3>Эргономика</h3>\r\n<p>Тормозные ручки имеют анатомическую форму. Ручка газа с мягкой \r\nгрипсой защищает от проскальзывания и делает поездку более безопасной. \r\nКнопки включения света и переключатели скоростей выполнены в \r\nклассическом, интуитивно понятном дизайне. </p>\r\n<h3>Пробег</h3>\r\n<p>Скутер может проехать до 60 км на одном заряде. Батарея \r\nсертифицирована и обладает умной BMS платой 30A, которая защищает \r\nэлементы питания от перезаряда и перегрузки.</p>\r\n<h3>Посадка</h3>\r\n<p>Прямая посадка и классическое сиденье — мягкое, широкое и удобное — \r\nпрекрасно подходят для длительных поездок. Верх сиденья отделан прочной и\r\n долговечной эко-кожей, которая устойчива к воздействию влаги и \r\nультрафиолета.</p>\r\n<h3>Корзина</h3>\r\n<p>На данный момент модель WS-MINI R 1200w единственная укомплектована \r\nодновременно и корзиной, и дополнительным сиденьем с мягкой спинкой. \r\nКорзина выполнена из прочного пластика и имеет грузоподъемность 30 кг.</p>\r\n<h3>Оптика</h3>\r\n<p>Данная модель укомплектована одной мощной головной LED-фарой и двумя \r\nсветодиодными стробоскопами. Яркий свет оптики обеспечивает безопасность\r\n передвижения в любое время суток.</p>\r\n<h3>Колеса</h3>\r\n<p>Колеса диаметром 6,5 дюймов с высоким профилем отлично справляются с \r\nнеровностями на городских и загородных дорогах. А полноразмерные крылья \r\nпозволяют защитить водителя и пассажира от грязи и брызг во время \r\nдвижения.</p>				</div>','7',NULL,46900.00,46900.00,NULL,NULL),(8,'1o.jpg','2021-02-07 13:19:29.843982','2021-02-07 22:45:44.754749',8,1,NULL,'','WS-SOCHI 1300W','','','',NULL,NULL,61900.00,'','Идеальный выбор для юных мотоциклистов','<div>\r\n					<h3>WS-SOCHI 1300w</h3>\r\n<p>Модель WS-SOCHI мини-кросс 1300W подходит для детей и подростков в \r\nвозрасте от 5 до 14 лет. Этот компактный электрический мотоцикл \r\nоборудован мощным двигателем на 1300 Вт и создан специально для юных \r\nлюбителей мотокросса, которые с малых лет хотят быть на одной волне со \r\nсвоими родителями. На байке установлены 10-дюймовые спицованные колеса, \r\nкоторые позволяют с легкостью преодолевать любые трассы.</p>\r\n<p> \r\nЗа счёт мощного мотора байк не уступает бензиновым моделям аналогичного \r\nразмера, а в некоторых моментах даже превосходит.  Он очень удобен как \r\nдля городских жителей, так и для тех, кто живет за городом. \r\nЭлектромотоцикл не выделяет дыма, не пахнет бензином или маслом. Его \r\nлегко перевозить в багажнике авто, легко заряжать дома, легко хранить на\r\n балконе или в гараже. Во время прогулок в парках и скверах города Вы не\r\n столкнётесь с жалобами окружающих, ведь байк не шумит и не загрязняет \r\nвоздух.</p>\r\n<p>\r\nWS-SOCHI 1300w – самый простой способ влюбить ваших детей в мотоциклы.</p>\r\n<h3>Эргономика</h3>\r\n<p>Тормозные ручки имеют анатомическую форму. Ручка газа с мягкой \r\nгрипсой защищает от проскальзывания и делает поездку более безопасной. \r\nКнопки включения света и переключатели скоростей выполнены в \r\nклассическом интуитивно понятном дизайне. </p>\r\n<h3>Пробег</h3>\r\n<p>Скутер может проехать до 50 км на одном заряде аккумулятора, что \r\nсоответствует 2-3 часам активной езды. Батарея сертифицирована, имеет \r\nвлагозащиту и выдерживает температурные перепады.</p>\r\n<h3>Пластик</h3>\r\n<p>Пластиковые детали электробайка выполнены из мягкого и \r\nтравмобезопасного пластика с добавлением резины, за счет этого он хорошо\r\n гнется и не трескается.</p>\r\n<h3>Посадка</h3>\r\n<p>Прямая посадка и мягкое широкое сиденье позволяют райдеру проезжать \r\nмного километров без усталости. Форма сиденья не мешает при езде стоя, а\r\n верх отделан прочной и долговечной эко-кожей, которая устойчива к \r\nвоздействию влаги и ультрафиолета.</p>\r\n<h3>Оптика</h3>\r\n<p>Данная модель укомплектована одной мощной головной LED-фарой . Яркий \r\nсвет оптики обеспечивает безопасность передвижения в любое время суток.</p>\r\n<h3>Колеса</h3>\r\n<p>На 10-дюймовые колеса установлена резина с внедорожным протектором. \r\nПри этом байк стабилен не только на грунтовых дорогах, но и во время \r\nезды по асфальту.</p>\r\n<h3>Тормоза</h3>\r\n<p>На байке установлены классические легкообслуживаемые дисковые тормоза\r\n с тросиковым приводом. Им не страшна грязь, но даже если вы захотите их\r\n почистить, то сможете сделать это без каких-либо трудностей \r\nсамостоятельно.</p>				</div>','8',NULL,61900.00,61900.00,NULL,NULL),(9,'DSC_2424.jpg','2021-02-07 13:24:42.224770','2021-02-07 22:48:23.281888',9,1,NULL,'','WS-TAIGA 800W','','','',NULL,NULL,43900.00,'','Гость из будущего','<div>\r\n					<h3>WS-TAIGA 800W</h3>\r\n<p>Надежный, быстрый, стильный и мощный самокат от компании WS-ELECTRO, \r\nкоторый словно сошел с плаката о прекрасном будущем. При создании данной\r\n модели инженеры WS применили весь накопленный опыт в области \r\nэлектротранспорта. В WS-TAIGA 800W прекрасно все: прочная алюминиевая \r\nрама, отзывчивая подвеска, заводская аквазащита, футуристический дизайн,\r\n привлекающий внимание и вызывающий интерес, и отличные динамические \r\nхарактеристики. Самокат способен развивать скорость до 45 км/ч и готов \r\nпроехать до 50 км на одном заряде АКБ. </p>\r\n<h3>Оптика</h3>\r\n<p>Самокат оснащен двумя фарами NANOLED со сверхъяркими светодиодами \r\nCREE, которые отлично знакомы профессиональным покорителям бездорожья. \r\nЯркий и крупный стоп-сигнал электросамоката хорошо заметен в любое время\r\n суток, а полоса подсветки вдоль деки обеспечивает дополнительную \r\nбезопасность во время поездок в темноте. </p>\r\n<h3>Эргономика</h3>\r\n<p>Курок газа имеет анатомическую форму, поэтому Вы не почувствуете \r\nусталости даже во время длительных поездок. Кнопки управления бортовым \r\nкомпьютером, звонок и рычаг тормоза расположены слева, при этом \r\nторможение непременно порадует Вас своей предсказуемостью и \r\nэффективностью. </p>\r\n<h3>Пробег</h3>\r\n<p>На одном заряде АКБ самокат может проехать до 50 км в зависимости от \r\nпогодных условий, ландшафта и веса райдера. Батарея сертифицирована, \r\nснабжена балансировочной платой и обладает сверхнадежной гидроизоляцией.\r\n Конфигурация батареи — 48v16A, элементы от фирмы Lishen — крупного \r\nкитайского производителя аккумуляторных батарей. </p>\r\n<h3>Посадка</h3>\r\n<p>На модели предусмотрена установка сиденья, в базовой комплектации самокат идет без него.</p>\r\n<h3>Бортовой компьютер</h3>\r\n<p>Многофункциональный бортовой компьютер с функцией «антиблик» \r\nдемонстрирует скорость, уровень заряда батареи и пройденную дистанцию. </p>				</div>','9',NULL,43900.00,43900.00,NULL,NULL),(10,'DSC03861.png','2021-02-07 16:10:41.032127','2021-02-07 23:04:47.535391',10,1,NULL,'','LOCKER 1.0','','','',NULL,NULL,390.00,'','Припарковался, закрепил, техника под защитой','<div>\r\n					<p>Универсальный тросовый замок для вашего велосипеда, скутера или \r\nсамоката. Прочный металлический трос длиной 120 см позволит надежно \r\nзакрепить технику на парковке, у столба, ограждения или любого другого \r\nобъекта.  </p><p>Механизм блокировки представлен в виде ключевого замка 11-го уровня защиты.</p>				</div>','10',NULL,390.00,390.00,NULL,NULL),(11,'DSC03840.png','2021-02-07 16:14:06.448700','2021-02-07 23:29:45.140542',11,1,NULL,'','LOCKER 2.0','','','',NULL,NULL,449.00,'','Припарковался, закрепил, техника под защитой','<div>\r\n					<p>Универсальный тросовый замок для вашего велосипеда, скутера или \r\nсамоката. Прочный металлический трос длиной 120 см позволит надежно \r\nзакрепить технику на парковке, у столба, ограждения или любого другого \r\nобъекта.</p>\r\n<p>Механизм блокировки представлен в виде пятизначного кодового замка 11-го уровня защиты.</p>				</div>','11',NULL,449.00,449.00,NULL,NULL),(12,'DSC02601.jpg','2021-02-07 16:16:51.948843','2021-02-07 23:31:43.813557',12,1,NULL,'','WS-PHONE HOLDER 1.0','','','',NULL,NULL,390.00,'','Удобство передвижения','<div>\r\n					<p>Универсальный держатель для телефона от компании WS-ELECTRO. Он позволяет:</p>\r\n<ul><li>Держать смартфон на виду во время поездки, не переживая за его сохранность.</li><li>Отвечать на вызовы или пользоваться навигатором, не совершая лишних движений.</li></ul>\r\n<p>Держатель выполнен из крепкого пластика и имеет регулировку по \r\nвысоте, поэтому подойдет для большинства моделей современных телефонов. </p>				</div>','12',NULL,390.00,390.00,NULL,NULL),(13,'DSC04161.png','2021-02-07 16:19:27.030804','2021-02-07 23:33:32.781974',13,1,NULL,'','WS-PHONE HOLDER 2.0','','','',NULL,NULL,790.00,'','Удобство передвижения','<div>\r\n					<p>Универсальный держатель для телефона от компании WS-ELECTRO. Он позволяет:</p>\r\n<ul><li>Держать смартфон на виду во время поездки, не переживая за его сохранность.</li><li>Отвечать на вызовы или пользоваться навигатором, не совершая лишних движений.</li></ul>\r\n<p>Держатель выполнен из крепкого пластика и имеет обновленный механизм,\r\n который быстро, легко и надежно зажимает телефон. Путешествуйте с \r\nкомфортом и не переживайте за сохранность Вашего гаджета!</p>				</div>','13',NULL,790.00,790.00,NULL,NULL),(14,'DSC02619.jpg','2021-02-07 16:22:34.756251','2021-02-07 23:35:49.974177',14,1,NULL,'','WS-URBAN 3L','','','',NULL,NULL,1390.00,'','Удобство и практичность','Универсальные сумки для ручной клади от компании WS-ELECTRO. \r\nПредставлены в двух вариациях: объемом 3л и 5л. Крепление осуществляется\r\n с помощью прочных ремешков, поэтому сумку можно при необходимости \r\nотстегнуть и взять с собой. Износостойкий влагонепроницаемый материал, \r\nкачественная молния и крепкие нитки в двойных строчках гарантируют \r\nдолговечность сумки и сохранность ее содержимого.','14',NULL,1390.00,1390.00,NULL,NULL),(15,'DSC02607.jpg','2021-02-07 16:25:05.173346','2021-02-07 23:37:45.802397',15,1,NULL,'','WS-URBAN 5L','','','',NULL,NULL,1490.00,'','Удобство и практичность','Универсальные сумки для ручной клади от компании WS-ELECTRO. \r\nПредставлены в двух вариациях: объемом 3л и 5л. Крепление осуществляется\r\n с помощью прочных ремешков, поэтому сумку можно при необходимости \r\nотстегнуть и взять с собой. Износостойкий влагонепроницаемый материал, \r\nкачественная молния и крепкие нитки в двойных строчках гарантируют \r\nдолговечность сумки и сохранность ее содержимого.','15',NULL,1490.00,1490.00,NULL,NULL),(16,'DSC00895.jpg','2021-02-07 16:28:19.944569','2021-02-07 23:40:17.245693',16,1,NULL,'','WS-FAST CHARGER 5A','','','',NULL,NULL,2750.00,'','Зарядите транспорт в 3 раза быстрее','<div>\r\n					<p>Для ускорения скорости зарядки аккумуляторов инженеры WS-ELECTRO\r\n разработали зарядное устройство мощностью 5 А (стандартные З/У имеют \r\nмощность 2-3 А). </p>\r\n<p>WS-FAST CHARGER 5A имеет две вариации: на 48V и 60V. Наличие большого\r\n количества переходников под различные разъемы многочисленных моделей \r\nэлектротранспорта делает зарядное устройство универсальным. Также \r\nWS-FAST CHARGER 5A имеет функцию активации защитного режима при \r\nвнезапном коротком замыкании, вызванном внешними воздействиями, которая \r\nзащитит АКБ от повреждения.</p>\r\n				</div>','16',NULL,2750.00,2750.00,NULL,NULL),(17,'17.png','2021-02-07 16:30:39.888272','2021-02-07 23:42:11.051147',17,1,NULL,'','WS-KIDS HOLDER','','','',NULL,NULL,900.00,'','Передвигайтесь все семьей','<div>\r\n					<p>Для комфортной и безопасной езды с ребенком на самокате компания WS-ELECTRO создала универсальный детский держатель.</p>\r\n<p>Мягкие ручки удобны для детей и позволяют крепко держаться даже во \r\nвремя быстрой езды. В наборе присутствует 4 переходника для крепления к \r\nрулевой колонке электросамоката.</p>\r\n				</div>','17',NULL,900.00,900.00,NULL,NULL),(18,'ZXT_8242.jpg','2021-02-07 16:36:57.188140','2021-02-07 23:50:56.601096',18,1,NULL,'','WS-RAIN COVER','','','',NULL,NULL,3500.00,'','Ваша техника прослужит еще дольше','<div>\r\n					<p>Влага – агрессивная среда для электротранспорта. Чтобы защитить \r\nего во время хранения в условиях дождя или снега, компания WS-ELECTRO \r\nсоздала чехол от дождя WS-RAIN COVER. Чехол изготовлен из \r\nводонепроницаемого материала 210D, который в 4 раза толще ткани, \r\nиспользуемой для производства зонтов.</p>\r\n<p>В комплекте с чехлом идет мобильная сумка-переноска, которая позволяет брать его с собой или компактно хранить.</p>				</div>','18',NULL,3500.00,3500.00,NULL,NULL),(19,'DSC02471.jpg','2021-02-07 16:39:41.769071','2021-02-07 23:57:33.471034',19,1,NULL,'','WS-OFFROAD EVOLUTION','','','',NULL,NULL,15900.00,'','Передвигайтесь там, где другие не могут','Комплект 8-дюймовых колес в сборе с внедорожной резиной с высоким \r\nпрофилем. Разработана специально для WS-PRO + TRIKE 3000W, но подойдет \r\nдля любых трайков класса CityCoco. Установка колес происходит легко и \r\nбыстро в домашних условиях и не требует никаких особых навыков. \r\nРазболтовка задних колес – на 4 болта, переднее колесо крепится на ось','19',NULL,15900.00,15900.00,NULL,NULL),(20,'eva-1.jpg','2021-02-07 16:42:34.834551','2021-02-07 23:59:18.956227',20,1,NULL,'','EVA-коврик','','','',NULL,NULL,890.00,'','Ваша техника будет всегда чистой','<div>\r\n					<p>Для того, чтобы Ваша техника была всегда чистой, компания WHITE \r\nSIBERIA создала высокотехнологичный коврик EVA. Его легко закреплять и \r\nлегко снимать. </p>\r\n<p>Благодаря наличию ячеек коврик задерживает грязь и воду, при этом \r\nВаши ноги и техника остаются чистыми. Просто снимите коврик и вытряхните\r\n его – несколько секунд спустя он снова станет чистым! Износостойкий \r\nматериал коврика не боится влаги и не меняет свою форму даже при \r\nрегулярных точечных нагрузках. </p>\r\n<p>В комплекте коврик и две липучки.</p>\r\n				</div>','20',NULL,890.00,890.00,NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=330 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productscats`
--

LOCK TABLES `products_productscats` WRITE;
/*!40000 ALTER TABLE `products_productscats` DISABLE KEYS */;
INSERT INTO `products_productscats` VALUES (309,148,2,NULL),(310,148,3,NULL),(311,148,4,NULL),(312,148,5,NULL),(313,148,6,NULL),(314,148,7,NULL),(315,148,8,NULL),(316,148,9,NULL),(318,149,10,NULL),(319,149,11,NULL),(320,149,12,NULL),(321,149,13,NULL),(322,149,14,NULL),(323,149,15,NULL),(324,149,16,NULL),(325,149,17,NULL),(326,149,18,NULL),(327,149,19,NULL),(328,149,20,NULL),(329,148,1,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=440 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productsphotos`
--

LOCK TABLES `products_productsphotos` WRITE;
/*!40000 ALTER TABLE `products_productsphotos` DISABLE KEYS */;
INSERT INTO `products_productsphotos` VALUES (1,'ZXT_5855.jpg','2021-02-05 18:14:52.227257','2021-02-06 18:36:44.040691',1,1,NULL,NULL,'1',1),(2,'ZXT_5885.jpg','2021-02-05 18:15:47.736653','2021-02-06 18:36:56.915944',2,1,NULL,NULL,'1',1),(8,'8.jpg','2021-02-05 18:17:40.788497','2021-02-06 18:36:56.071126',8,1,NULL,NULL,'1',1),(9,'ZXT_5844.jpg','2021-02-05 18:18:00.036252','2021-02-06 18:37:12.168957',9,1,NULL,NULL,'1',1),(11,'ZXT_5840.jpg','2021-02-05 18:22:14.549039','2021-02-06 18:38:22.617458',10,1,NULL,NULL,'2',1),(12,'ZXT_5855.jpg','2021-02-05 18:22:43.705193','2021-02-06 18:37:24.901958',11,1,NULL,NULL,'2',1),(13,'ZXT_5885.jpg','2021-02-05 18:22:58.469939','2021-02-06 18:38:15.182311',12,1,NULL,NULL,'2',1),(15,'ZXT_5872.jpg','2021-02-05 18:23:18.956194','2021-02-06 18:38:12.113855',13,1,NULL,NULL,'2',1),(16,'ZXT_5844.jpg','2021-02-05 18:23:35.634693','2021-02-06 18:38:09.194019',14,1,NULL,NULL,'2',1),(36,'21.jpg','2021-02-06 18:32:46.198168','2021-02-07 11:34:02.654871',15,1,NULL,NULL,'1',2),(37,'23.jpg','2021-02-06 18:33:01.962888','2021-02-07 11:34:07.334646',16,1,NULL,NULL,'1',2),(38,'34.jpg','2021-02-06 18:33:17.619403','2021-02-07 11:34:13.880370',17,1,NULL,NULL,'1',2),(39,'32.jpg','2021-02-06 18:33:32.871134','2021-02-07 11:34:03.350487',18,1,NULL,NULL,'1',2),(40,'26.jpg','2021-02-06 18:33:45.696210','2021-02-07 11:34:10.567339',19,1,NULL,NULL,'1',2),(41,'27.jpg','2021-02-06 18:34:02.030638','2021-02-07 11:34:16.027054',20,1,NULL,NULL,'1',2),(42,'20.jpg','2021-02-06 18:34:42.008179','2021-02-07 11:34:20.089456',21,1,NULL,NULL,'2',2),(43,'34.jpg','2021-02-06 18:34:57.269082','2021-02-07 11:34:23.128073',22,1,NULL,NULL,'2',2),(44,'26.jpg','2021-02-06 18:35:10.288486','2021-02-07 11:34:26.548523',23,1,NULL,NULL,'2',2),(45,'27.jpg','2021-02-06 18:35:25.283057','2021-02-07 11:34:29.888063',24,1,NULL,NULL,'2',2),(46,'DSC01813.jpg','2021-02-06 18:39:11.517971','2021-02-06 18:45:30.119472',25,1,NULL,NULL,'3',1),(47,'DSC01819.jpg','2021-02-06 18:39:22.193912','2021-02-06 18:45:16.923338',26,1,NULL,NULL,'3',1),(48,'DSC03475.jpg','2021-02-06 18:43:50.244385','2021-02-06 18:45:19.409725',27,1,NULL,NULL,'3',1),(49,'DSC03496.jpg','2021-02-06 18:44:46.342682','2021-02-06 18:44:52.075604',28,1,NULL,NULL,'3',1),(50,'DSC03529.jpg','2021-02-06 18:45:05.018602','2021-02-06 18:45:22.795189',29,1,NULL,NULL,'3',1),(51,'DSC03545.jpg','2021-02-06 18:45:12.202125','2021-02-06 18:45:25.170874',30,1,NULL,NULL,'3',1),(53,'53.jpeg','2021-02-07 11:36:26.569400','2021-02-07 11:36:29.896654',31,1,NULL,NULL,'3',2),(55,'55.jpeg','2021-02-07 11:37:12.640338','2021-02-07 11:37:15.628192',32,1,NULL,NULL,'3',2),(56,'56.jpeg','2021-02-07 11:37:32.284818','2021-02-07 11:37:36.773455',33,1,NULL,NULL,'3',2),(58,'58.jpeg','2021-02-07 11:38:25.814916','2021-02-07 11:38:30.968388',34,1,NULL,NULL,'3',2),(74,'13.jpg','2021-02-07 11:52:55.062256','2021-02-07 11:54:19.539671',35,1,NULL,NULL,'4',3),(75,'2.jpg','2021-02-07 11:53:13.666090','2021-02-07 11:54:18.878748',36,1,NULL,NULL,'4',3),(76,'15.jpg','2021-02-07 11:53:26.781415','2021-02-07 11:54:20.235589',37,1,NULL,NULL,'4',3),(78,'10.jpg','2021-02-07 11:53:45.362651','2021-02-07 11:54:20.933253',38,1,NULL,NULL,'4',3),(79,'DSC03443.jpg','2021-02-07 11:54:32.972214','2021-02-07 11:54:39.607935',39,1,NULL,NULL,'3',3),(80,'DSC03448.jpg','2021-02-07 11:55:11.054429','2021-02-07 11:55:14.899990',40,1,NULL,NULL,'3',3),(81,'DSC03427.jpg','2021-02-07 11:55:23.356682','2021-02-07 11:55:26.553212',41,1,NULL,NULL,'3',3),(97,'2r.jpg','2021-02-07 11:57:54.253989','2021-02-07 11:58:46.048570',42,1,NULL,NULL,'1',4),(98,'3r.jpg','2021-02-07 11:58:09.827028','2021-02-07 11:58:46.623866',43,1,NULL,NULL,'1',4),(99,'4r.jpg','2021-02-07 11:58:22.983157','2021-02-07 11:58:47.748259',44,1,NULL,NULL,'1',4),(100,'5r.jpg','2021-02-07 11:58:36.084851','2021-02-07 11:58:48.470436',45,1,NULL,NULL,'1',4),(101,'1b.jpg','2021-02-07 11:59:22.848310','2021-02-07 12:00:29.763382',46,1,NULL,NULL,'2',4),(102,'2b.jpg','2021-02-07 11:59:37.286605','2021-02-07 12:00:31.980569',47,1,NULL,NULL,'2',4),(103,'3b.jpg','2021-02-07 11:59:49.804036','2021-02-07 12:00:28.718194',48,1,NULL,NULL,'2',4),(104,'4b.jpg','2021-02-07 12:00:03.443994','2021-02-07 12:00:40.442577',49,1,NULL,NULL,'2',4),(105,'5b.jpg','2021-02-07 12:00:15.022672','2021-02-07 12:00:31.124429',50,1,NULL,NULL,'2',4),(106,'DSC04043-2.jpg','2021-02-07 12:00:54.752003','2021-02-07 12:02:33.221538',51,1,NULL,NULL,'3',4),(107,'DSC04045.jpg','2021-02-07 12:01:02.232165','2021-02-07 12:02:24.325902',52,1,NULL,NULL,'3',4),(108,'DSC04048.jpg','2021-02-07 12:01:10.611132','2021-02-07 12:02:25.740872',53,1,NULL,NULL,'3',4),(109,'DSC04058.jpg','2021-02-07 12:01:19.573904','2021-02-07 12:02:27.236763',54,1,NULL,NULL,'3',4),(110,'DSC04074.jpg','2021-02-07 12:01:26.673468','2021-02-07 12:02:29.859670',55,1,NULL,NULL,'3',4),(111,'DSC04091.jpg','2021-02-07 12:01:34.840235','2021-02-07 12:02:31.704346',56,1,NULL,NULL,'3',4),(112,'DSC04097.jpg','2021-02-07 12:01:42.050157','2021-02-07 12:02:25.053658',57,1,NULL,NULL,'3',4),(113,'DSC04710.jpg','2021-02-07 12:01:47.990583','2021-02-07 12:02:26.528604',58,1,NULL,NULL,'3',4),(114,'DSC04676.jpg','2021-02-07 12:01:54.442566','2021-02-07 12:02:28.170878',59,1,NULL,NULL,'3',4),(115,'DSC04697.jpg','2021-02-07 12:02:01.376408','2021-02-07 12:02:30.817328',60,1,NULL,NULL,'3',4),(132,'1b.jpg','2021-02-07 13:01:36.218531','2021-02-07 13:03:52.840975',62,1,NULL,NULL,'1',5),(133,'1b.jpg','2021-02-07 13:01:48.816845','2021-02-07 13:03:49.767871',63,1,NULL,NULL,'1',5),(134,'1b.jpg','2021-02-07 13:02:00.831700','2021-02-07 13:03:49.275071',64,1,NULL,NULL,'1',5),(135,'1b.jpg','2021-02-07 13:02:11.575618','2021-02-07 13:03:53.684312',65,1,NULL,NULL,'1',5),(136,'1b.jpg','2021-02-07 13:02:23.350480','2021-02-07 13:03:50.591840',66,1,NULL,NULL,'1',5),(137,'1b.jpg','2021-02-07 13:02:36.144951','2021-02-07 13:03:48.465294',67,1,NULL,NULL,'1',5),(138,'1b.jpg','2021-02-07 13:02:47.006897','2021-02-07 13:03:54.493833',68,1,NULL,NULL,'1',5),(139,'1b.jpg','2021-02-07 13:02:58.556724','2021-02-07 13:03:51.150915',69,1,NULL,NULL,'1',5),(140,'1b.jpg','2021-02-07 13:03:11.886562','2021-02-07 13:03:47.599591',70,1,NULL,NULL,'1',5),(141,'1b.jpg','2021-02-07 13:03:22.476334','2021-02-07 13:03:55.439573',71,1,NULL,NULL,'1',5),(142,'1b.jpg','2021-02-07 13:04:07.668294','2021-02-07 13:06:26.010850',72,1,NULL,NULL,'2',5),(143,'1b.jpg','2021-02-07 13:04:19.412004','2021-02-07 13:06:20.385112',73,1,NULL,NULL,'2',5),(144,'1b.jpg','2021-02-07 13:04:31.329859','2021-02-07 13:06:15.379944',74,1,NULL,NULL,'2',5),(145,'1b.jpg','2021-02-07 13:04:42.886626','2021-02-07 13:06:12.544362',75,1,NULL,NULL,'2',5),(146,'1b.jpg','2021-02-07 13:04:55.990294','2021-02-07 13:06:03.160599',76,1,NULL,NULL,'2',5),(147,'1b.jpg','2021-02-07 13:05:07.622177','2021-02-07 13:06:28.328428',77,1,NULL,NULL,'2',5),(148,'1b.jpg','2021-02-07 13:05:25.184005','2021-02-07 13:06:22.588651',78,1,NULL,NULL,'2',5),(149,'1b.jpg','2021-02-07 13:05:36.377712','2021-02-07 13:06:17.785371',79,1,NULL,NULL,'2',5),(150,'ZXT_8242.jpg','2021-02-07 13:05:46.314819','2021-02-07 13:06:10.148447',80,1,NULL,NULL,'2',5),(151,'ZXT_8280.jpg','2021-02-07 13:05:57.211986','2021-02-07 13:06:05.476901',81,1,NULL,NULL,'2',5),(167,'ZXT_2516.jpg','2021-02-07 13:08:51.659145','2021-02-07 13:11:14.179515',82,1,NULL,NULL,'1',6),(169,'ZXT_2511.jpg','2021-02-07 13:09:15.616556','2021-02-07 13:11:14.844045',83,1,NULL,NULL,'1',6),(170,'ZXT_2529.jpg','2021-02-07 13:09:27.106186','2021-02-07 13:11:13.583227',84,1,NULL,NULL,'1',6),(171,'ZXT_2543.jpg','2021-02-07 13:09:39.308665','2021-02-07 13:11:12.944916',85,1,NULL,NULL,'1',6),(173,'173.jpg','2021-02-07 13:11:05.288079','2021-02-07 13:11:12.302233',86,1,NULL,NULL,'1',6),(174,'ZXT_2498.jpg','2021-02-07 13:11:38.989906','2021-02-07 13:13:04.822199',87,1,NULL,NULL,'2',6),(175,'ZXT_2516.jpg','2021-02-07 13:11:50.543543','2021-02-07 13:12:53.943821',88,1,NULL,NULL,'2',6),(176,'ZXT_2511.jpg','2021-02-07 13:12:03.011664','2021-02-07 13:13:00.224967',89,1,NULL,NULL,'2',6),(178,'ZXT_2529.jpg','2021-02-07 13:12:24.477387','2021-02-07 13:13:02.651459',90,1,NULL,NULL,'2',6),(179,'ZXT_2543.jpg','2021-02-07 13:12:37.183717','2021-02-07 13:12:55.621848',91,1,NULL,NULL,'2',6),(180,'ZXT_2518.jpg','2021-02-07 13:12:48.606824','2021-02-07 13:12:57.725318',92,1,NULL,NULL,'2',6),(196,'2r.jpg','2021-02-07 13:16:55.840070','2021-02-07 13:17:38.333825',93,1,NULL,NULL,'1',7),(197,'3r.jpg','2021-02-07 13:17:07.395379','2021-02-07 13:17:40.070214',94,1,NULL,NULL,'1',7),(198,'4r.jpg','2021-02-07 13:17:19.479224','2021-02-07 13:17:41.940932',95,1,NULL,NULL,'1',7),(199,'5r.jpg','2021-02-07 13:17:33.973716','2021-02-07 13:17:44.479122',96,1,NULL,NULL,'1',7),(200,'1b.jpg','2021-02-07 13:18:04.636702','2021-02-07 13:18:58.345263',97,1,NULL,NULL,'2',7),(201,'2b.jpg','2021-02-07 13:18:18.433915','2021-02-07 13:19:01.529158',98,1,NULL,NULL,'2',7),(202,'3b.jpg','2021-02-07 13:18:29.975573','2021-02-07 13:18:54.204070',99,1,NULL,NULL,'2',7),(203,'4b.jpg','2021-02-07 13:18:40.176278','2021-02-07 13:18:56.320961',100,1,NULL,NULL,'2',7),(204,'5b.jpg','2021-02-07 13:18:50.769103','2021-02-07 13:19:04.781966',101,1,NULL,NULL,'2',7),(220,'1o2.jpg','2021-02-07 13:22:17.270183','2021-02-07 13:24:01.043948',102,1,NULL,NULL,'5',8),(221,'1o3.png','2021-02-07 13:22:33.350361','2021-02-07 13:24:04.765391',103,1,NULL,NULL,'5',8),(222,'1o4.png','2021-02-07 13:22:49.630581','2021-02-07 13:24:01.695884',104,1,NULL,NULL,'5',8),(223,'1o5.png','2021-02-07 13:23:04.770243','2021-02-07 13:24:04.195776',105,1,NULL,NULL,'5',8),(224,'1b.jpg','2021-02-07 13:23:18.910736','2021-02-07 13:24:02.302791',106,1,NULL,NULL,'5',8),(225,'1b.jpg','2021-02-07 13:23:29.881848','2021-02-07 13:24:03.548716',107,1,NULL,NULL,'5',8),(226,'1b.jpg','2021-02-07 13:23:42.720260','2021-02-07 13:24:02.875363',108,1,NULL,NULL,'5',8),(236,'DSC_2416.jpg','2021-02-07 13:26:20.666975','2021-02-07 13:30:13.945645',109,1,NULL,NULL,'6',9),(239,'DSC_2498.jpg','2021-02-07 13:27:26.779864','2021-02-07 13:30:13.398599',110,1,NULL,NULL,'6',9),(240,'DSC_2529.jpg','2021-02-07 13:27:38.640040','2021-02-07 13:30:14.633113',111,1,NULL,NULL,'6',9),(241,'DSC_2532.jpg','2021-02-07 13:27:50.574437','2021-02-07 13:30:15.230021',112,1,NULL,NULL,'6',9),(242,'DSC_2418.jpg','2021-02-07 13:28:04.800800','2021-02-07 13:30:15.848583',113,1,NULL,NULL,'6',9),(243,'DSC_2495.jpg','2021-02-07 13:28:17.141216','2021-02-07 13:30:16.458800',114,1,NULL,NULL,'6',9),(244,'DSC_2419.jpg','2021-02-07 13:28:29.615385','2021-02-07 13:30:17.187535',115,1,NULL,NULL,'6',9),(245,'DSC_2398.jpg','2021-02-07 13:30:46.303612','2021-02-07 13:32:06.382442',116,1,NULL,NULL,'2',9),(246,'DSC_2399.jpg','2021-02-07 13:30:57.615810','2021-02-07 13:32:28.113245',117,1,NULL,NULL,'2',9),(247,'DSC_2521.jpg','2021-02-07 13:31:08.710528','2021-02-07 13:32:19.079659',118,1,NULL,NULL,'2',9),(248,'DSC_2401.jpg','2021-02-07 13:31:20.007906','2021-02-07 13:32:12.410343',119,1,NULL,NULL,'2',9),(249,'DSC_2512.jpg','2021-02-07 13:31:33.872769','2021-02-07 13:32:08.067754',120,1,NULL,NULL,'2',9),(250,'DSC_2400.jpg','2021-02-07 13:31:44.065527','2021-02-07 13:32:25.135292',121,1,NULL,NULL,'2',9),(251,'251.jpg','2021-02-07 13:32:00.952953','2021-02-07 13:32:22.198774',122,1,NULL,NULL,'2',9),(252,'DSC_2472.jpg','2021-02-07 13:32:59.935780','2021-02-07 13:35:25.149721',123,1,NULL,NULL,'7',9),(253,'DSC_2465.jpg','2021-02-07 13:33:11.071432','2021-02-07 13:35:27.781707',124,1,NULL,NULL,'7',9),(254,'DSC_2538.jpg','2021-02-07 13:33:20.964761','2021-02-07 13:35:30.525887',125,1,NULL,NULL,'7',9),(255,'DSC_2540.jpg','2021-02-07 13:33:29.974836','2021-02-07 13:35:32.965047',126,1,NULL,NULL,'7',9),(256,'DSC_2466.jpg','2021-02-07 13:33:39.267030','2021-02-07 13:39:15.800621',127,1,NULL,NULL,'8',9),(257,'DSC_2473.jpg','2021-02-07 13:33:51.468370','2021-02-07 13:35:20.772784',128,1,NULL,NULL,'7',9),(258,'DSC_2467.jpg','2021-02-07 13:34:01.130993','2021-02-07 13:35:23.045199',129,1,NULL,NULL,'7',9),(259,'DSC_2440.jpg','2021-02-07 13:35:56.524725','2021-02-07 13:39:26.169209',130,1,NULL,NULL,'8',9),(260,'DSC_2433.jpg','2021-02-07 13:36:07.037184','2021-02-07 13:39:29.062700',131,1,NULL,NULL,'8',9),(261,'DSC_2546.jpg','2021-02-07 13:36:27.448445','2021-02-07 13:39:32.140285',132,1,NULL,NULL,'8',9),(262,'DSC_2549.jpg','2021-02-07 13:36:37.542584','2021-02-07 13:39:07.461423',133,1,NULL,NULL,'8',9),(263,'DSC_2435.jpg','2021-02-07 13:36:47.969192','2021-02-07 13:39:10.194461',134,1,NULL,NULL,'8',9),(264,'DSC_2450.jpg','2021-02-07 13:37:02.452529','2021-02-07 13:39:13.839878',135,1,NULL,NULL,'8',9),(265,'DSC_2434.jpg','2021-02-07 13:37:13.445375','2021-02-07 13:39:19.438530',136,1,NULL,NULL,'8',9),(266,'DSC_2446.jpg','2021-02-07 13:37:26.437673','2021-02-07 13:39:22.827303',137,1,NULL,NULL,'8',9),(268,'268.jpeg','2021-02-07 13:40:16.457182','2021-02-07 13:45:23.179446',138,1,NULL,NULL,'3',9),(269,'269.jpeg','2021-02-07 13:40:55.086629','2021-02-07 13:46:03.542807',139,1,NULL,NULL,'3',9),(271,'271.jpeg','2021-02-07 13:41:33.933679','2021-02-07 13:45:59.450372',140,1,NULL,NULL,'3',9),(272,'272.jpeg','2021-02-07 13:41:51.991599','2021-02-07 13:45:56.132778',141,1,NULL,NULL,'3',9),(273,'273.jpeg','2021-02-07 13:42:12.163082','2021-02-07 13:45:53.012245',142,1,NULL,NULL,'3',9),(274,'DSC03385.jpg','2021-02-07 13:42:24.362303','2021-02-07 13:45:49.524132',143,1,NULL,NULL,'3',9),(275,'275.jpeg','2021-02-07 13:43:03.850196','2021-02-07 13:45:45.599158',144,1,NULL,NULL,'3',9),(276,'276.jpeg','2021-02-07 13:43:20.293056','2021-02-07 13:45:41.506902',145,1,NULL,NULL,'3',9),(277,'277.jpeg','2021-02-07 13:43:40.216123','2021-02-07 13:45:37.623085',146,1,NULL,NULL,'3',9),(278,'278.jpeg','2021-02-07 13:44:03.693481','2021-02-07 13:45:33.707353',147,1,NULL,NULL,'3',9),(279,'279.jpeg','2021-02-07 13:44:56.193419','2021-02-07 13:45:28.984888',148,1,NULL,NULL,'3',9),(280,'280.jpeg','2021-02-07 13:45:09.081052','2021-02-07 13:45:22.583172',149,1,NULL,NULL,'3',9),(281,'DSC03862.png','2021-02-07 16:11:29.413418','2021-02-07 16:11:29.413479',150,1,NULL,NULL,NULL,10),(282,'DSC03868.png','2021-02-07 16:11:41.732956','2021-02-07 16:11:41.732987',151,1,NULL,NULL,NULL,10),(283,'DSC03871.png','2021-02-07 16:11:54.227906','2021-02-07 16:11:54.227936',152,1,NULL,NULL,NULL,10),(284,'DSC03876.png','2021-02-07 16:12:07.079408','2021-02-07 16:12:07.079427',153,1,NULL,NULL,NULL,10),(285,'DSC03880.jpeg','2021-02-07 16:12:20.969821','2021-02-07 16:12:57.645491',154,1,NULL,NULL,'3',10),(286,'DSC03885.jpeg','2021-02-07 16:12:30.644169','2021-02-07 16:13:27.536568',155,1,NULL,NULL,'3',10),(287,'DSC03960.jpeg','2021-02-07 16:12:39.010758','2021-02-07 16:12:58.420872',156,1,NULL,NULL,'3',10),(288,'DSC03961.jpeg','2021-02-07 16:12:47.280848','2021-02-07 16:13:28.186016',157,1,NULL,NULL,'3',10),(297,'DSC03845.png','2021-02-07 16:15:29.527021','2021-02-07 16:15:29.527038',158,1,NULL,NULL,NULL,11),(298,'DSC03848.png','2021-02-07 16:15:42.623051','2021-02-07 16:15:42.623067',159,1,NULL,NULL,NULL,11),(299,'DSC03852.png','2021-02-07 16:15:53.367566','2021-02-07 16:15:53.367583',160,1,NULL,NULL,NULL,11),(300,'DSC03857.png','2021-02-07 16:16:03.510360','2021-02-07 16:16:03.510379',161,1,NULL,NULL,NULL,11),(301,'DSC03880.jpeg','2021-02-07 16:16:12.197052','2021-02-07 16:16:44.489073',162,1,NULL,NULL,'3',11),(302,'DSC03885.jpeg','2021-02-07 16:16:19.907757','2021-02-07 16:16:45.861674',163,1,NULL,NULL,'3',11),(303,'DSC03960.jpeg','2021-02-07 16:16:28.210906','2021-02-07 16:16:45.209991',164,1,NULL,NULL,'3',11),(304,'DSC03961.jpeg','2021-02-07 16:16:37.867311','2021-02-07 16:16:46.594255',165,1,NULL,NULL,'3',11),(313,'DSC02598.jpg','2021-02-07 16:18:24.542223','2021-02-07 16:18:24.542240',166,1,NULL,NULL,NULL,12),(314,'DSC02596.jpg','2021-02-07 16:18:36.600439','2021-02-07 16:18:36.600456',167,1,NULL,NULL,NULL,12),(315,'DSC04656.jpg','2021-02-07 16:18:47.867202','2021-02-07 16:19:12.585082',168,1,NULL,NULL,'3',12),(316,'DSC04654.jpg','2021-02-07 16:18:54.923686','2021-02-07 16:19:17.298547',169,1,NULL,NULL,'3',12),(317,'DSC04651.jpg','2021-02-07 16:19:02.170607','2021-02-07 16:19:15.257525',170,1,NULL,NULL,'3',12),(318,'DSC04653.jpg','2021-02-07 16:19:08.940590','2021-02-07 16:19:19.166552',171,1,NULL,NULL,'3',12),(325,'DSC04157.png','2021-02-07 16:20:44.715218','2021-02-07 16:20:44.715234',172,1,NULL,NULL,NULL,13),(327,'DSC04163.png','2021-02-07 16:21:02.837460','2021-02-07 16:21:02.837480',174,1,NULL,NULL,NULL,13),(328,'DSC04164.png','2021-02-07 16:21:21.494798','2021-02-07 16:21:21.494814',175,1,NULL,NULL,NULL,13),(329,'DSC04668.jpg','2021-02-07 16:21:35.327372','2021-02-07 16:22:08.096664',176,1,NULL,NULL,'3',13),(330,'DSC04663.jpg','2021-02-07 16:21:42.575186','2021-02-07 16:22:07.095908',177,1,NULL,NULL,'3',13),(331,'DSC04665.jpg','2021-02-07 16:21:49.486608','2021-02-07 16:22:09.198405',178,1,NULL,NULL,'3',13),(332,'DSC04666.jpg','2021-02-07 16:21:55.999492','2021-02-07 16:22:10.200912',179,1,NULL,NULL,'3',13),(340,'DSC02620.jpg','2021-02-07 16:23:52.605571','2021-02-07 16:23:52.605589',180,1,NULL,NULL,NULL,14),(341,'DSC02621.jpg','2021-02-07 16:24:05.341024','2021-02-07 16:24:05.341043',181,1,NULL,NULL,NULL,14),(342,'DSC04455.jpg','2021-02-07 16:24:15.374984','2021-02-07 16:24:57.432631',182,1,NULL,NULL,'3',14),(343,'DSC04460.jpg','2021-02-07 16:24:21.813783','2021-02-07 16:24:58.142341',183,1,NULL,NULL,'3',14),(344,'DSC04463.jpg','2021-02-07 16:24:27.799057','2021-02-07 16:24:58.951111',184,1,NULL,NULL,'3',14),(345,'DSC04488.jpg','2021-02-07 16:24:34.590690','2021-02-07 16:24:59.627179',185,1,NULL,NULL,'3',14),(346,'DSC04470.jpg','2021-02-07 16:24:40.042398','2021-02-07 16:25:00.311789',186,1,NULL,NULL,'3',14),(347,'DSC04452.jpg','2021-02-07 16:24:46.039632','2021-02-07 16:25:00.945602',187,1,NULL,NULL,'3',14),(356,'DSC02608.jpg','2021-02-07 16:26:21.950872','2021-02-07 16:26:21.950888',188,1,NULL,NULL,NULL,15),(358,'DSC02609.jpg','2021-02-07 16:26:35.991477','2021-02-07 16:26:35.991494',190,1,NULL,NULL,NULL,15),(359,'DSC02611.jpg','2021-02-07 16:26:49.332915','2021-02-07 16:26:49.332934',191,1,NULL,NULL,NULL,15),(360,'DSC02612.jpg','2021-02-07 16:27:01.974788','2021-02-07 16:27:01.974805',192,1,NULL,NULL,NULL,15),(361,'DSC02613.jpg','2021-02-07 16:27:13.383913','2021-02-07 16:27:13.383929',193,1,NULL,NULL,NULL,15),(362,'DSC04499.jpg','2021-02-07 16:27:24.659043','2021-02-07 16:28:12.198661',194,1,NULL,NULL,'3',15),(363,'DSC04508.jpg','2021-02-07 16:27:32.420326','2021-02-07 16:28:15.534409',195,1,NULL,NULL,'3',15),(364,'DSC04511.jpg','2021-02-07 16:27:38.885160','2021-02-07 16:28:13.465886',196,1,NULL,NULL,'3',15),(365,'DSC04524.jpg','2021-02-07 16:27:44.777167','2021-02-07 16:28:12.881931',197,1,NULL,NULL,'3',15),(366,'DSC04527.jpg','2021-02-07 16:27:51.540735','2021-02-07 16:28:14.737280',198,1,NULL,NULL,'3',15),(367,'DSC04535.jpg','2021-02-07 16:27:58.247612','2021-02-07 16:28:14.152602',199,1,NULL,NULL,'3',15),(379,'DSC01350.jpg','2021-02-07 16:29:46.097590','2021-02-07 16:29:46.097608',200,1,NULL,NULL,NULL,16),(380,'DSC01354.jpg','2021-02-07 16:29:58.925151','2021-02-07 16:29:58.925168',201,1,NULL,NULL,NULL,16),(382,'DSC01361.jpg','2021-02-07 16:30:13.597602','2021-02-07 16:30:13.597619',203,1,NULL,NULL,NULL,16),(386,'DSC_0086.png','2021-02-07 16:31:58.967882','2021-02-07 16:31:58.967902',204,1,NULL,NULL,NULL,17),(387,'DSC_0120.png','2021-02-07 16:32:15.717792','2021-02-07 16:32:15.717811',205,1,NULL,NULL,NULL,17),(388,'DSC04615.jpg','2021-02-07 16:32:23.675937','2021-02-07 16:33:02.908320',206,1,NULL,NULL,'3',17),(389,'DSC04626.jpg','2021-02-07 16:32:29.685342','2021-02-07 16:32:59.850026',207,1,NULL,NULL,'3',17),(390,'DSC04612.jpg','2021-02-07 16:32:35.874204','2021-02-07 16:33:01.747677',208,1,NULL,NULL,'3',17),(391,'DSC04619.jpg','2021-02-07 16:32:42.917522','2021-02-07 16:33:00.454299',209,1,NULL,NULL,'3',17),(392,'DSC04636.jpg','2021-02-07 16:32:50.200183','2021-02-07 16:33:01.050043',210,1,NULL,NULL,'3',17),(400,'ZXT_8238.jpg','2021-02-07 16:38:19.773004','2021-02-07 16:38:19.773020',211,1,NULL,NULL,NULL,18),(401,'ZXT_8245.jpg','2021-02-07 16:38:30.144127','2021-02-07 16:38:30.144142',212,1,NULL,NULL,NULL,18),(402,'ZXT_8239.jpg','2021-02-07 16:38:39.559482','2021-02-07 16:38:39.559498',213,1,NULL,NULL,NULL,18),(403,'ZXT_8243.jpg','2021-02-07 16:38:50.861607','2021-02-07 16:38:50.861623',214,1,NULL,NULL,NULL,18),(404,'DSC04354.jpg','2021-02-07 16:39:00.593175','2021-02-07 16:39:28.593249',215,1,NULL,NULL,'3',18),(405,'DSC04362.jpg','2021-02-07 16:39:07.906270','2021-02-07 16:39:28.064240',216,1,NULL,NULL,'3',18),(406,'DSC04398.jpg','2021-02-07 16:39:13.865988','2021-02-07 16:39:29.268042',217,1,NULL,NULL,'3',18),(407,'DSC04417.jpg','2021-02-07 16:39:19.786081','2021-02-07 16:39:27.468847',218,1,NULL,NULL,'3',18),(416,'DSC02475.jpg','2021-02-07 16:40:57.123960','2021-02-07 16:40:57.123979',219,1,NULL,NULL,NULL,19),(417,'DSC02472.jpg','2021-02-07 16:41:10.853800','2021-02-07 16:41:10.853820',220,1,NULL,NULL,NULL,19),(419,'DSC02474.jpg','2021-02-07 16:41:26.273977','2021-02-07 16:41:26.273992',221,1,NULL,NULL,NULL,19),(420,'420.png','2021-02-07 16:41:44.285114','2021-02-07 16:41:44.285144',222,1,NULL,NULL,NULL,19),(421,'DSC04540.jpg','2021-02-07 16:41:57.612999','2021-02-07 16:42:18.289206',223,1,NULL,NULL,'3',19),(422,'DSC04578.jpg','2021-02-07 16:42:03.812118','2021-02-07 16:42:17.715475',224,1,NULL,NULL,'3',19),(423,'DSC04599.jpg','2021-02-07 16:42:11.123898','2021-02-07 16:42:18.954554',225,1,NULL,NULL,'3',19),(431,'eva-2.jpg','2021-02-07 16:43:36.281352','2021-02-07 16:43:36.281368',226,1,NULL,NULL,NULL,20),(432,'eva-3.jpg','2021-02-07 16:43:45.592766','2021-02-07 16:43:45.592784',227,1,NULL,NULL,NULL,20),(433,'eva-4.jpg','2021-02-07 16:43:56.805360','2021-02-07 16:43:56.805377',228,1,NULL,NULL,NULL,20),(435,'eva-5.jpg','2021-02-07 16:44:12.945940','2021-02-07 16:44:12.945958',229,1,NULL,NULL,NULL,20),(436,'eva-6.jpg','2021-02-07 16:44:24.247965','2021-02-07 16:44:24.247982',230,1,NULL,NULL,NULL,20),(437,'DSC_0090.jpg','2021-02-07 16:44:33.748359','2021-02-07 16:44:59.199202',231,1,NULL,NULL,'3',20),(438,'DSC_0094.jpg','2021-02-07 16:44:43.012861','2021-02-07 16:44:57.805745',232,1,NULL,NULL,'3',20),(439,'DSC_0096.jpg','2021-02-07 16:44:50.549998','2021-02-07 16:44:58.547231',233,1,NULL,NULL,'3',20);
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
) ENGINE=InnoDB AUTO_INCREMENT=172 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productsproperties`
--

LOCK TABLES `products_productsproperties` WRITE;
/*!40000 ALTER TABLE `products_productsproperties` DISABLE KEYS */;
INSERT INTO `products_productsproperties` VALUES (19,1,11),(20,1,19),(21,1,2),(22,1,22),(23,1,31),(24,1,38),(25,1,42),(26,1,46),(27,1,53),(28,1,56),(29,1,63),(30,1,70),(31,1,79),(32,1,87),(33,1,90),(34,1,93),(35,1,96),(36,2,12),(37,2,19),(38,2,5),(39,2,23),(40,2,32),(41,2,38),(42,2,42),(43,2,47),(44,2,53),(45,2,56),(46,2,63),(47,2,71),(48,2,80),(49,2,87),(50,2,90),(51,2,93),(52,2,96),(53,3,11),(54,3,19),(55,3,4),(56,3,24),(57,3,33),(58,3,38),(59,3,42),(60,3,48),(61,3,53),(62,3,57),(63,3,64),(64,3,72),(65,3,81),(66,3,87),(67,3,90),(68,3,93),(69,3,96),(70,4,13),(71,4,19),(72,4,5),(73,4,25),(74,4,32),(75,4,39),(76,4,43),(77,4,47),(78,4,53),(79,4,58),(80,4,63),(81,4,72),(82,4,82),(83,4,88),(84,4,90),(85,4,93),(86,4,96),(87,5,14),(88,5,19),(89,5,6),(90,5,26),(91,5,34),(92,5,38),(93,5,42),(94,5,46),(95,5,53),(96,5,59),(97,5,65),(98,5,73),(99,5,83),(100,5,87),(101,5,90),(102,5,94),(103,5,96),(104,6,15),(105,6,19),(106,6,7),(107,6,27),(108,6,33),(109,6,38),(110,6,44),(111,6,48),(112,6,54),(113,6,56),(114,6,66),(115,6,75),(116,6,84),(117,6,87),(118,6,91),(119,6,94),(120,6,96),(121,7,12),(122,7,20),(123,7,2),(124,7,28),(125,7,35),(126,7,40),(127,7,42),(128,7,50),(129,7,53),(130,7,60),(131,7,67),(132,7,76),(133,7,85),(134,7,87),(135,7,90),(136,7,95),(137,7,97),(138,8,17),(139,8,21),(140,8,9),(141,8,29),(142,8,36),(143,8,40),(144,8,43),(145,8,51),(146,8,53),(147,8,61),(148,8,68),(149,8,77),(150,8,85),(151,8,87),(152,8,92),(153,8,95),(154,8,97),(155,9,18),(156,9,20),(157,9,2),(158,9,30),(159,9,37),(160,9,41),(161,9,45),(162,9,52),(163,9,55),(164,9,62),(165,9,69),(166,9,78),(167,9,86),(168,9,89),(169,9,90),(170,9,95),(171,9,98);
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
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_propertiesvalues`
--

LOCK TABLES `products_propertiesvalues` WRITE;
/*!40000 ALTER TABLE `products_propertiesvalues` DISABLE KEYS */;
INSERT INTO `products_propertiesvalues` VALUES (2,NULL,'2021-02-11 00:22:30.028854','2021-02-11 00:22:30.028878',1,0,NULL,NULL,'24-45',16,NULL),(4,NULL,'2021-02-11 00:22:41.914745','2021-02-11 00:22:41.914768',3,0,NULL,NULL,'24-60',16,NULL),(5,NULL,'2021-02-11 00:22:48.726144','2021-02-11 00:22:48.726165',4,0,NULL,NULL,'24-71',16,NULL),(6,NULL,'2021-02-11 00:22:55.630466','2021-02-11 00:22:55.630493',5,0,NULL,NULL,'24-61',16,NULL),(7,NULL,'2021-02-11 00:23:02.886717','2021-02-11 00:23:02.886740',6,0,NULL,NULL,'24-54',16,NULL),(9,NULL,'2021-02-11 00:23:17.808687','2021-02-11 00:23:17.808707',8,0,NULL,NULL,'24-38',16,NULL),(11,NULL,'2021-02-11 00:34:18.160998','2021-02-11 00:34:18.161020',9,0,NULL,NULL,'Lithium-ion 60V21A MADE IN TAIWAN Возможность установки второго АКБ',17,NULL),(12,NULL,'2021-02-11 00:34:25.953827','2021-02-11 00:34:25.953849',10,0,NULL,NULL,'Lithium-Ion 60V21A MADE IN TAIWAN + балансировочная плата. Возможность установки второго АКБ',17,NULL),(13,NULL,'2021-02-11 00:34:41.716678','2021-02-11 00:34:41.716704',11,0,NULL,NULL,'Lithium-Ion 60V31A MADE IN TAIWAN',17,NULL),(14,NULL,'2021-02-11 00:34:50.777625','2021-02-11 00:34:50.777652',12,0,NULL,NULL,'Lithium-Ion 60V21A MADE IN TAIWAN + балансировочная плата. Возможность установки трех АКБ',17,NULL),(15,NULL,'2021-02-11 00:34:56.634184','2021-02-11 00:34:56.634204',13,0,NULL,NULL,'Lithium-Ion 60V21A MADE IN TAIWAN ',17,NULL),(16,NULL,'2021-02-11 00:35:01.967183','2021-02-11 00:35:01.967204',14,0,NULL,NULL,'Lithium-Ion 48V15A MADE IN TAIWAN + балансировочная плата. Возможность установки второго АКБ',17,NULL),(17,NULL,'2021-02-11 00:35:13.229890','2021-02-11 00:35:13.229913',15,0,NULL,NULL,'36V12A. Возможность установки второго АКБ',17,NULL),(18,NULL,'2021-02-11 00:35:20.116163','2021-02-11 00:35:20.116197',16,0,NULL,NULL,'Lithium-ion 48V16A MADE IN TAIWAN+ балансировочная плата',17,NULL),(19,NULL,'2021-02-11 00:35:36.991242','2021-02-11 00:35:36.991267',17,0,NULL,NULL,'260',18,260.0000),(20,NULL,'2021-02-11 00:35:49.826728','2021-02-11 00:35:49.826747',18,0,NULL,NULL,'125',18,125.0000),(21,NULL,'2021-02-11 00:35:56.311732','2021-02-11 00:35:56.311756',19,0,NULL,NULL,'115',18,115.0000),(22,NULL,'2021-02-11 00:36:16.763554','2021-02-11 00:36:16.763575',20,0,NULL,NULL,'106',19,106.0000),(23,NULL,'2021-02-11 00:36:24.867510','2021-02-11 00:36:24.867532',21,0,NULL,NULL,'87',19,87.0000),(24,NULL,'2021-02-11 00:36:33.450714','2021-02-11 00:36:33.450738',22,0,NULL,NULL,'84.8',19,84.8000),(25,NULL,'2021-02-11 00:36:38.158888','2021-02-11 00:36:38.158909',23,0,NULL,NULL,'81',19,81.0000),(26,NULL,'2021-02-11 00:36:44.527362','2021-02-11 00:36:44.527382',24,0,NULL,NULL,'75,65',19,75.6500),(27,NULL,'2021-02-11 00:36:50.115563','2021-02-11 00:36:50.115582',25,0,NULL,NULL,'70.2 ',19,70.2000),(28,NULL,'2021-02-11 00:36:56.219971','2021-02-11 00:36:56.219992',26,0,NULL,NULL,'39.8',19,39.8000),(29,NULL,'2021-02-11 00:37:01.413339','2021-02-11 00:37:01.413362',27,0,NULL,NULL,'46',19,46.0000),(30,NULL,'2021-02-11 00:37:13.813810','2021-02-11 00:37:13.813831',28,0,NULL,NULL,'23.50 ',19,23.5000),(31,NULL,'2021-02-11 00:37:33.573533','2021-02-11 00:37:33.573622',29,0,NULL,NULL,'216 x 36 x 125',20,NULL),(32,NULL,'2021-02-11 00:37:38.564446','2021-02-11 00:37:38.564466',30,0,NULL,NULL,'215 x 37 x 125',20,NULL),(33,NULL,'2021-02-11 00:37:42.920346','2021-02-11 00:37:42.920367',31,0,NULL,NULL,'215 x 36 x 125',20,NULL),(34,NULL,'2021-02-11 00:37:58.984810','2021-02-11 00:37:58.984832',32,0,NULL,NULL,'210*34*78',20,NULL),(35,NULL,'2021-02-11 00:38:09.546675','2021-02-11 00:38:09.546697',33,0,NULL,NULL,'142*25*90',20,NULL),(36,NULL,'2021-02-11 00:38:16.434439','2021-02-11 00:38:16.434462',34,0,NULL,NULL,'140*65*87',20,NULL),(37,NULL,'2021-02-11 00:38:20.858411','2021-02-11 00:38:20.858429',35,0,NULL,NULL,'115 x 20 x 114',20,NULL),(38,NULL,'2021-02-11 00:38:35.558795','2021-02-11 00:38:35.558817',36,0,NULL,NULL,'7',21,7.0000),(39,NULL,'2021-02-11 00:38:44.419445','2021-02-11 00:38:44.419466',37,0,NULL,NULL,'9',21,9.0000),(40,NULL,'2021-02-11 00:38:59.701175','2021-02-11 00:38:59.701199',38,0,NULL,NULL,'5',21,5.0000),(41,NULL,'2021-02-11 00:39:10.043891','2021-02-11 00:39:10.043909',39,0,NULL,NULL,'8',21,8.0000),(42,NULL,'2021-02-11 00:39:25.644878','2021-02-11 00:39:25.644902',40,0,NULL,NULL,'Линзовая фара и стробоскопы',22,NULL),(43,NULL,'2021-02-11 00:39:38.350011','2021-02-11 00:39:49.357752',41,0,NULL,NULL,'Линзовая фара',22,NULL),(44,NULL,'2021-02-11 00:41:00.646318','2021-02-11 00:41:00.646341',42,0,NULL,NULL,'Диодная фара',22,NULL),(45,NULL,'2021-02-11 00:41:21.736317','2021-02-11 00:41:21.736337',43,0,NULL,NULL,'NANO LED',22,NULL),(46,NULL,'2021-02-11 00:41:36.885323','2021-02-11 00:42:42.456135',44,0,NULL,NULL,'10 дюймов',23,NULL),(47,NULL,'2021-02-11 00:41:46.453454','2021-02-11 00:42:43.569025',45,0,NULL,NULL,'12 дюймов',23,NULL),(48,NULL,'2021-02-11 00:42:13.722780','2021-02-11 00:42:44.975724',46,0,NULL,NULL,'8 дюймов',23,NULL),(49,NULL,'2021-02-11 00:42:37.205249','2021-02-11 00:42:37.205269',47,0,NULL,NULL,'10 дюймов (универсальный протектор)',23,NULL),(50,NULL,'2021-02-11 00:43:05.178775','2021-02-11 00:43:05.178797',48,0,NULL,NULL,'6.5 дюймов',23,NULL),(51,NULL,'2021-02-11 00:43:13.853174','2021-02-11 00:43:13.853198',49,0,NULL,NULL,'12 дюймов перед/ 10 дюймов зад',23,NULL),(52,NULL,'2021-02-11 00:43:20.523165','2021-02-11 00:43:20.523187',50,0,NULL,NULL,'11 дюймов',23,NULL),(53,NULL,'2021-02-11 00:43:35.627786','2021-02-11 00:43:35.627832',51,0,NULL,NULL,'Мотоциклетная, пружинно-масляного типа, настраиваемая',24,NULL),(54,NULL,'2021-02-11 00:43:55.037918','2021-02-11 00:43:55.037940',52,0,NULL,NULL,'Мотоциклетная, пружинного типа',24,NULL),(55,NULL,'2021-02-11 00:44:04.792012','2021-02-11 00:44:04.792032',53,0,NULL,NULL,'Многорычажная, пружинного типа',24,NULL),(56,NULL,'2021-02-11 00:44:19.370768','2021-02-11 00:44:19.370790',54,0,NULL,NULL,'50-60',25,NULL),(57,NULL,'2021-02-11 00:44:28.518682','2021-02-11 00:44:28.518702',55,0,NULL,NULL,'40-60',25,NULL),(58,NULL,'2021-02-11 00:44:36.612734','2021-02-11 00:44:36.612769',56,0,NULL,NULL,'60-80 км',25,NULL),(59,NULL,'2021-02-11 00:44:44.639582','2021-02-11 00:44:44.639606',57,0,NULL,NULL,'До 60',25,NULL),(60,NULL,'2021-02-11 00:44:56.513969','2021-02-11 00:44:56.513992',58,0,NULL,NULL,'60',25,60.0000),(61,NULL,'2021-02-11 00:45:02.586698','2021-02-11 00:45:02.586732',59,0,NULL,NULL,'40-50',25,NULL),(62,NULL,'2021-02-11 00:45:11.313196','2021-02-11 00:45:11.313221',60,0,NULL,NULL,'55',25,55.0000),(63,NULL,'2021-02-11 00:45:25.955449','2021-02-11 00:45:25.955472',61,0,NULL,NULL,'60v 3000w',26,NULL),(64,NULL,'2021-02-11 00:45:38.634987','2021-02-11 00:45:38.635078',62,0,NULL,NULL,'60v 2000w перед/зад суммарно 4000W',26,NULL),(65,NULL,'2021-02-11 00:45:45.481401','2021-02-11 00:45:45.481448',63,0,NULL,NULL,'60v 2500w',26,NULL),(66,NULL,'2021-02-11 00:45:52.122524','2021-02-11 00:45:52.122548',64,0,NULL,NULL,'60v 2000w',26,NULL),(67,NULL,'2021-02-11 00:45:56.976160','2021-02-11 00:45:56.976184',65,0,NULL,NULL,'48v 1200w',26,NULL),(68,NULL,'2021-02-11 00:46:04.797470','2021-02-11 00:46:04.797489',66,0,NULL,NULL,'48v 1300w',26,NULL),(69,NULL,'2021-02-11 00:46:14.298914','2021-02-11 00:46:14.298938',67,0,NULL,NULL,'48v 800w',26,NULL),(70,NULL,'2021-02-11 00:46:33.210915','2021-02-11 00:46:33.210935',68,0,NULL,NULL,'116.8',27,116.8000),(71,NULL,'2021-02-11 00:46:38.729127','2021-02-11 00:46:38.729149',69,0,NULL,NULL,'95',27,95.0000),(72,NULL,'2021-02-11 00:46:42.167435','2021-02-11 00:46:42.167461',70,0,NULL,NULL,'94.1',27,94.1000),(73,NULL,'2021-02-11 00:46:49.784870','2021-02-11 00:46:49.784892',71,0,NULL,NULL,'84,95',27,84.9500),(74,NULL,'2021-02-11 00:46:54.600263','2021-02-11 00:47:14.278310',72,0,NULL,NULL,'91.4',27,91.4000),(75,NULL,'2021-02-11 00:47:24.866200','2021-02-11 00:47:24.866222',73,0,NULL,NULL,'80',27,80.0000),(76,NULL,'2021-02-11 00:47:30.568064','2021-02-11 00:47:30.568089',74,0,NULL,NULL,'45.9',27,45.9000),(77,NULL,'2021-02-11 00:47:37.117284','2021-02-11 00:47:37.117308',75,0,NULL,NULL,'60.45',27,60.4500),(78,NULL,'2021-02-11 00:47:43.647639','2021-02-11 00:47:43.647661',76,0,NULL,NULL,'28.05',27,28.0500),(79,NULL,'2021-02-11 00:48:02.763554','2021-02-11 00:48:02.763577',77,0,NULL,NULL,'198/38/90',28,NULL),(80,NULL,'2021-02-11 00:48:07.635042','2021-02-11 00:48:07.635064',78,0,NULL,NULL,'198/36.5/85',28,NULL),(81,NULL,'2021-02-11 00:48:11.921114','2021-02-11 00:48:11.921137',79,0,NULL,NULL,'191/36.5/87',28,NULL),(82,NULL,'2021-02-11 00:48:16.949724','2021-02-11 00:48:16.949749',80,0,NULL,NULL,'191/36.5/90',28,NULL),(83,NULL,'2021-02-11 00:48:24.366909','2021-02-11 00:48:24.366934',81,0,NULL,NULL,'191*36,5*85',28,NULL),(84,NULL,'2021-02-11 00:48:28.693486','2021-02-11 00:48:28.693507',82,0,NULL,NULL,'191/38/90',28,NULL),(85,NULL,'2021-02-11 00:48:35.467214','2021-02-11 00:48:35.467235',83,0,NULL,NULL,'142/30/62',28,NULL),(86,NULL,'2021-02-11 00:48:46.909284','2021-02-11 00:48:46.909305',84,0,NULL,NULL,'118/22.5/52',28,NULL),(87,NULL,'2021-02-11 00:49:10.987872','2021-02-11 00:49:10.987892',85,0,NULL,NULL,'Положение руля, положение фары',29,NULL),(88,NULL,'2021-02-11 00:49:20.984500','2021-02-11 00:49:20.984536',86,0,NULL,NULL,'Положение руля',29,NULL),(89,NULL,'2021-02-11 00:49:45.391548','2021-02-11 00:49:45.391567',87,0,NULL,NULL,'Направление луча света',29,NULL),(90,NULL,'2021-02-11 00:50:08.273368','2021-02-11 00:50:08.273388',88,0,NULL,NULL,'Многофункциональный бортовой компьютер',30,NULL),(91,NULL,'2021-02-11 00:50:24.311810','2021-02-11 00:50:24.311837',89,0,NULL,NULL,'Информативный дисплей',30,NULL),(92,NULL,'2021-02-11 00:50:35.739525','2021-02-11 00:50:35.739549',90,0,NULL,NULL,'Шкала заряда батареи',30,NULL),(93,NULL,'2021-02-11 00:50:53.234805','2021-02-11 00:50:53.234829',91,0,NULL,NULL,'Дисковые, гидравлические настраиваемые',31,NULL),(94,NULL,'2021-02-11 00:51:06.463998','2021-02-11 00:51:06.464019',92,0,NULL,NULL,'Дисковые, гидравлические',31,NULL),(95,NULL,'2021-02-11 00:51:18.824089','2021-02-11 00:51:18.824112',93,0,NULL,NULL,'Дисковые, тросовые',31,NULL),(96,NULL,'2021-02-11 00:51:37.384361','2021-02-11 00:51:37.384383',94,0,NULL,NULL,'Сталь',32,NULL),(97,NULL,'2021-02-11 00:51:48.759001','2021-02-11 00:51:48.759026',95,0,NULL,NULL,'Металл',32,NULL),(98,NULL,'2021-02-11 00:51:58.591152','2021-02-11 00:51:58.591177',96,0,NULL,NULL,'Алюминий',32,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_property`
--

LOCK TABLES `products_property` WRITE;
/*!40000 ALTER TABLE `products_property` DISABLE KEYS */;
INSERT INTO `products_property` VALUES (16,NULL,'2021-02-10 23:57:44.448551','2021-02-10 23:57:44.448571',1,1,NULL,NULL,'Максимальная скорость (км/ч)',NULL,'maksimalnaya-skorost-kmch',NULL,0),(17,NULL,'2021-02-10 23:57:44.450539','2021-02-10 23:57:44.450556',2,1,NULL,NULL,'Аккумулятор',NULL,'akkumulyator',NULL,0),(18,NULL,'2021-02-10 23:57:44.452522','2021-02-10 23:57:44.452539',3,1,NULL,NULL,'Максимальная нагрузка (кг)',NULL,'maksimalnaya-nagruzka-kg',NULL,0),(19,NULL,'2021-02-10 23:58:13.705846','2021-02-10 23:58:13.705867',4,1,NULL,NULL,'Масса нетто (кг)',NULL,'massa-netto-kg',NULL,0),(20,NULL,'2021-02-10 23:58:13.710571','2021-02-10 23:58:13.710604',5,1,NULL,NULL,'Габаритные размеры в собранном состоянии (ДxШxВ) (см)',NULL,'gabaritnye-razmery-v-sobrannom-sostoyanii-dxshxv-sm',NULL,0),(21,NULL,'2021-02-10 23:58:13.714667','2021-02-10 23:58:13.714702',6,1,NULL,NULL,'Время зарядки (ч)',NULL,'vremya-zaryadki-ch',NULL,0),(22,NULL,'2021-02-11 00:00:07.593323','2021-02-11 00:00:07.593342',7,1,NULL,NULL,'Фара',NULL,'fara',NULL,0),(23,NULL,'2021-02-11 00:00:07.601831','2021-02-11 00:42:39.905882',8,1,NULL,'','Размер колес',NULL,'razmer-koles','',0),(24,NULL,'2021-02-11 00:00:07.607092','2021-02-11 00:00:07.607118',9,1,NULL,NULL,'Подвеска',NULL,'podveska',NULL,0),(25,NULL,'2021-02-11 00:00:07.610702','2021-02-11 00:00:07.610722',10,1,NULL,NULL,'Запас хода (км)',NULL,'zapas-hoda-km',NULL,0),(26,NULL,'2021-02-11 00:00:07.612683','2021-02-11 00:00:07.612700',11,1,NULL,NULL,'Электродвигатель',NULL,'elektrodvigatel',NULL,0),(27,NULL,'2021-02-11 00:00:07.614580','2021-02-11 00:00:07.614596',12,1,NULL,NULL,'Масса брутто (кг)',NULL,'massa-brutto-kg',NULL,0),(28,NULL,'2021-02-11 00:00:07.616928','2021-02-11 00:00:07.616947',13,1,NULL,NULL,'Габариты упаковки (см)',NULL,'gabarity-upakovki-sm',NULL,0),(29,NULL,'2021-02-11 00:00:07.618868','2021-02-11 00:00:07.618885',14,1,NULL,NULL,'Предварительные настройки',NULL,'predvaritelnye-nastroyki',NULL,0),(30,NULL,'2021-02-11 00:00:07.620891','2021-02-11 00:00:07.620910',15,1,NULL,NULL,'Панель управления',NULL,'panel-upravleniya',NULL,0),(31,NULL,'2021-02-11 00:00:07.622941','2021-02-11 00:00:07.622985',16,1,NULL,NULL,'Тормоза',NULL,'tormoza',NULL,0),(32,NULL,'2021-02-11 00:00:07.625388','2021-02-11 00:00:07.625407',17,1,NULL,NULL,'Материал рамы',NULL,'material-ramy',NULL,0);
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

-- Dump completed on 2021-02-13 11:54:46
