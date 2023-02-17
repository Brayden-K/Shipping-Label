/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 100425 (10.4.25-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : label

 Target Server Type    : MySQL
 Target Server Version : 100425 (10.4.25-MariaDB)
 File Encoding         : 65001

 Date: 17/02/2023 14:32:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for invoices
-- ----------------------------
DROP TABLE IF EXISTS `invoices`;
CREATE TABLE `invoices`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `ownerId` int NULL DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `amount` decimal(10, 2) NULL DEFAULT NULL,
  `currency` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `paid` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of invoices
-- ----------------------------
INSERT INTO `invoices` VALUES (6, NULL, 'LCXiBcR75e6znTxa6Yn5RL', 2500.00, 'new', NULL);
INSERT INTO `invoices` VALUES (8, NULL, 'RyVCYWkeNZ57zXckgX8DtH', 2500.00, 'new', NULL);
INSERT INTO `invoices` VALUES (9, NULL, 'VFBv1pPfJJrPVsFrPWWU3r', 2500.00, 'new', NULL);
INSERT INTO `invoices` VALUES (10, NULL, '3JYCpjCqgTkA9oNHBsgkGX', 2500.00, 'new', NULL);
INSERT INTO `invoices` VALUES (11, NULL, 'UvWmiDHdR5qcRQHtkRLhzU', 2500.00, 'new', NULL);
INSERT INTO `invoices` VALUES (12, NULL, 'WTyy8Q4UXDfGjPEqsWZCYR', 2500.00, 'new', NULL);
INSERT INTO `invoices` VALUES (13, NULL, 'D8RLJUJucZKipSPbuBj3hJ', 2500.00, 'new', NULL);
INSERT INTO `invoices` VALUES (14, NULL, 'LFiKBxz5288EZsLvZppqAM', 2500.00, 'new', NULL);
INSERT INTO `invoices` VALUES (15, NULL, 'XmhMSLQEoo5Wm2E6FAZEbf', 2500.00, 'new', NULL);
INSERT INTO `invoices` VALUES (16, NULL, 'YQKJBAUtxEq7m5H9cgmPEA', 2500.00, 'new', NULL);
INSERT INTO `invoices` VALUES (17, NULL, '8S2N48zz6VaxKNAgE5zyjN', 2500.00, 'new', NULL);
INSERT INTO `invoices` VALUES (18, NULL, 'EB7fbrQd3p893YWfyrkmEZ', 2500.00, 'complete', NULL);
INSERT INTO `invoices` VALUES (19, NULL, '964j2QESYe3aFE6pRxX4fj', 2500.00, 'complete', NULL);
INSERT INTO `invoices` VALUES (20, NULL, 'GraeZWEJWxKEf1MNCNED6p', 2500.00, 'complete', NULL);
INSERT INTO `invoices` VALUES (21, NULL, 'FwQ4ZgMg1HnJRD3sA28gcn', 2500.00, 'complete', NULL);

-- ----------------------------
-- Table structure for pricing
-- ----------------------------
DROP TABLE IF EXISTS `pricing`;
CREATE TABLE `pricing`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  `ca` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pricing
-- ----------------------------
INSERT INTO `pricing` VALUES (1, '1', 'FedEx Ground', NULL, 'fedex_ground', 9.99, NULL);
INSERT INTO `pricing` VALUES (2, '1', 'FedEx Overnight', NULL, 'fedex_overnight', 12.99, NULL);
INSERT INTO `pricing` VALUES (3, '3', 'USPS First Class', NULL, 'uspsv4_first_class', 12.99, NULL);
INSERT INTO `pricing` VALUES (4, '3', 'USPS Priority', NULL, 'uspsv4_priority', 12.99, NULL);
INSERT INTO `pricing` VALUES (5, '3', 'USPS Express', NULL, 'uspsv4_express', 13.99, NULL);
INSERT INTO `pricing` VALUES (6, '2', 'UPS Next Day Air Early', '1 Day', NULL, NULL, NULL);
INSERT INTO `pricing` VALUES (7, '2', 'UPS Next Day Air', '1 Day', NULL, NULL, NULL);
INSERT INTO `pricing` VALUES (8, '2', 'UPS 2nd Day Air', '2 Days', NULL, NULL, NULL);
INSERT INTO `pricing` VALUES (9, '2', 'UPS 3 Day Select', '3 Days', NULL, NULL, NULL);
INSERT INTO `pricing` VALUES (10, '2', 'UPS Ground', 'Min. 3 Days', NULL, NULL, NULL);
INSERT INTO `pricing` VALUES (11, '2', 'UPS Standard', 'Flexible', NULL, NULL, 1);
INSERT INTO `pricing` VALUES (12, '2', 'UPS Expedited', '2 Days', NULL, NULL, 1);
INSERT INTO `pricing` VALUES (13, '2', 'UPS Express Saver', '1 Day', NULL, NULL, 1);
INSERT INTO `pricing` VALUES (14, '2', 'UPS Express', '1 Day', NULL, NULL, 1);
INSERT INTO `pricing` VALUES (15, '2', 'UPS Express Early', '1 Day', NULL, NULL, 1);

-- ----------------------------
-- Table structure for providers
-- ----------------------------
DROP TABLE IF EXISTS `providers`;
CREATE TABLE `providers`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of providers
-- ----------------------------
INSERT INTO `providers` VALUES (1, 'fedex');
INSERT INTO `providers` VALUES (2, 'ups');
INSERT INTO `providers` VALUES (3, 'usps');

-- ----------------------------
-- Table structure for settings
-- ----------------------------
DROP TABLE IF EXISTS `settings`;
CREATE TABLE `settings`  (
  `siteName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `siteTitle` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `siteDescription` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `requireCaptcha` tinyint(1) NULL DEFAULT NULL,
  `captchaSiteKey` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `captchaSecret` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `underConstruction` tinyint(1) NULL DEFAULT NULL,
  `showDashboardMessage` tinyint(1) NULL DEFAULT NULL,
  `dashboardTitle` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `dashboardMessage` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `discordLink` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `telegramLink` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `coinbaseKey` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `coinbaseSigningSecret` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `emailSender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `emailSenderName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `emailUsername` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `emailPassword` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `emailHost` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `emailPort` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `upsApiKey` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `fedexApiKey` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `uspsApiKey` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `enableUps` tinyint(1) NULL DEFAULT NULL,
  `enableFedex` tinyint(1) NULL DEFAULT NULL,
  `enableUsps` tinyint(1) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of settings
-- ----------------------------
INSERT INTO `settings` VALUES ('CheapShip', 'Placeholder Tag', 'Super long description here', 0, '6LezZi8kAAAAAK0zr1Q37h3wDErCQ3Xe1OsCe_zG', '6LezZi8kAAAAACMBJmGtP3SRAxaVMWuYdqQZCo4k', 0, 1, 'This is a site-wide alert', 'Testing the site message', 'https://discord.gg/haksdjfhaksjhdf', 'https://t.me/@cheapship999', '48d4c6fc-cb82-4093-83b0-4a68d3395e33', '75167a1c-f302-483b-875a-904df13f46d1', 'admin@edgedev.io', 'Cheap Ship', 'AKIAXONBXLZ5ME6NIEGW', 'BEOjgt/CP1HCzb8Vt62okQn/TpMTrxc0ASkWktyb4Su1', 'email-smtp.us-west-1.amazonaws.com', '465', 'c99393e5-8959-11ed-8088-c2cbf658e5da', '630e80fb-1c0b-d772-8ad3-b09028642ef9', '630e80fb-1c0b-d772-8ad3-b09028642ef9', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for templates
-- ----------------------------
DROP TABLE IF EXISTS `templates`;
CREATE TABLE `templates`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `ownerId` int NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `address1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `address2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `address3` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `state` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `postalCode` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `companyName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `country` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of templates
-- ----------------------------
INSERT INTO `templates` VALUES (1, 1, 'from', 'Template One', '9385 hill rd s', '', '', 'PICKERINGTON', 'OH', '43147', 'John Doe', '0681669318', 'US');
INSERT INTO `templates` VALUES (2, 1, 'from', 'Template Two', '9385 hill rd s', '', '', 'PICKERINGTON', 'OH', '43147', 'John Doe', '0681669318', 'US');
INSERT INTO `templates` VALUES (3, 1, 'from', 'Template Three', '9385 hill rd s', '', '', 'PICKERINGTON', 'OH', '43147', 'John Doe', '0681669318', 'US');
INSERT INTO `templates` VALUES (4, 1, 'from', 'Template Four', '9385 hill rd s', '', '', 'PICKERINGTON', 'OH', '43147', 'John Doe', '0681669318', 'US');
INSERT INTO `templates` VALUES (8, 1, 'to', 'Template Three', '9385 hill rd s', '', '', 'PICKERINGTON', 'OH', '43147', 'John Doe', '0681669318', 'US');
INSERT INTO `templates` VALUES (9, 1, 'to', 'Template Four', '9385 hill rd s', '', '', 'PICKERINGTON', 'OH', '43147', 'John Doe', '0681669318', 'US');
INSERT INTO `templates` VALUES (10, 1, 'from', 'Template Five', '9385 hill rd s', '', '', 'PICKERINGTON', 'OH', '43147', 'John Doe', '0681669318', 'US');

-- ----------------------------
-- Table structure for tickets
-- ----------------------------
DROP TABLE IF EXISTS `tickets`;
CREATE TABLE `tickets`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `ownerId` int NULL DEFAULT NULL,
  `subject` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `priority` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `progress` int NULL DEFAULT NULL,
  `created` datetime NULL DEFAULT NULL,
  `complete` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tickets
-- ----------------------------
INSERT INTO `tickets` VALUES (1, 1, 'Help me please', 'thanks', 'low', 80, '2023-01-21 00:00:00', 1);
INSERT INTO `tickets` VALUES (2, 1, 'halp', 'thanks', 'low', 83, '2023-01-21 00:00:00', 0);
INSERT INTO `tickets` VALUES (3, 1, 'help', 'testtttt', 'low', 73, '2023-01-21 00:00:00', 1);
INSERT INTO `tickets` VALUES (4, 12, 'This is brok', 'I need help man', 'urgent', 100, '2023-01-22 00:00:00', 1);
INSERT INTO `tickets` VALUES (5, 2, 'asdf', 'This is broke', 'low', 100, '2023-01-22 00:00:00', 1);
INSERT INTO `tickets` VALUES (6, 12, 'TESTING THIS THING', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\r\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\r\nquis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\r\nconsequat. Duis aute irure dol', 'urgent', 100, '2023-01-24 00:00:00', 1);
INSERT INTO `tickets` VALUES (7, 1, 'asdf', 'asdf', 'low', 100, '2023-02-07 00:00:00', 1);
INSERT INTO `tickets` VALUES (8, 1, 'xxxxxNew Ticket', 'test', 'medium', 100, '2023-02-07 00:00:00', 1);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `notes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `admin` tinyint(1) NULL DEFAULT NULL,
  `balance` decimal(10, 2) NULL DEFAULT NULL,
  `banned` tinyint(1) NULL DEFAULT NULL,
  `joined` datetime NULL DEFAULT NULL,
  `telegram` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `discord` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'test@test.net', 'test', NULL, 1, 160.00, NULL, '2023-01-28 18:35:14', 'Edge', 'Edge#8686');
INSERT INTO `users` VALUES (2, 'test@testx.net', 'test', NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `users` VALUES (3, 'bbb@bbb.net', 'bbb', NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `users` VALUES (4, 'asdf@asdf.net', 'asdf', NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `users` VALUES (5, 'blahhhh@blah.net', 'x', NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `users` VALUES (6, 'test@test', 'test', NULL, NULL, NULL, NULL, NULL, NULL, NULL);

SET FOREIGN_KEY_CHECKS = 1;
