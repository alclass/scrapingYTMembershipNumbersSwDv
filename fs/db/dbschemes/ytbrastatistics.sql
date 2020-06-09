-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Tempo de geração: 08-Jun-2020 às 20:17
-- Versão do servidor: 5.7.30-0ubuntu0.18.04.1
-- versão do PHP: 7.2.24-0ubuntu0.18.04.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `ytbrastatistics`
--
CREATE DATABASE IF NOT EXISTS `ytbrastatistics` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `ytbrastatistics`;

-- --------------------------------------------------------

--
-- Estrutura da tabela `channels`
--

DROP TABLE IF EXISTS `channels`;
CREATE TABLE IF NOT EXISTS `channels` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `ytchannelid` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nname` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `obs` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ytchannelid_idx` (`ytchannelid`),
  UNIQUE KEY `nname_idx` (`nname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='You Channels or Users';

-- --------------------------------------------------------

--
-- Estrutura da tabela `dailychannelsubscribernumbers`
--

DROP TABLE IF EXISTS `dailychannelsubscribernumbers`;
CREATE TABLE IF NOT EXISTS `dailychannelsubscribernumbers` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `ytchannelid` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subscribers` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `infodate` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ytchannelid_subs_fk` (`ytchannelid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Table to register daily number of ytchannel subscribers';

-- --------------------------------------------------------

--
-- Estrutura da tabela `individualvideostats`
--

DROP TABLE IF EXISTS `individualvideostats`;
CREATE TABLE IF NOT EXISTS `individualvideostats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ytvideoid` char(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `duration_in_sec` int(11) DEFAULT NULL,
  `publishdate` date DEFAULT NULL,
  `published_time_ago` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `infodate` date DEFAULT NULL,
  `changelog` text COLLATE utf8mb4_unicode_ci,
  `ytchannelid` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ytvideoid` (`ytvideoid`),
  KEY `ytchannelid_fk` (`ytchannelid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='individual yt [bra] video statistics';

-- --------------------------------------------------------

--
-- Estrutura da tabela `videosviews`
--

DROP TABLE IF EXISTS `videosviews`;
CREATE TABLE IF NOT EXISTS `videosviews` (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `views` int(10) UNSIGNED NOT NULL,
  `infodate` date NOT NULL,
  `ytvideoid` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ytvideoid_fk` (`ytvideoid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `dailychannelsubscribernumbers`
--
ALTER TABLE `dailychannelsubscribernumbers`
  ADD CONSTRAINT `ytchannelid_subs_fk` FOREIGN KEY (`ytchannelid`) REFERENCES `channels` (`ytchannelid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limitadores para a tabela `individualvideostats`
--
ALTER TABLE `individualvideostats`
  ADD CONSTRAINT `ytchannelid_fk` FOREIGN KEY (`ytchannelid`) REFERENCES `channels` (`ytchannelid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Limitadores para a tabela `videosviews`
--
ALTER TABLE `videosviews`
  ADD CONSTRAINT `ytvideoid_fk` FOREIGN KEY (`ytvideoid`) REFERENCES `individualvideostats` (`ytvideoid`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
