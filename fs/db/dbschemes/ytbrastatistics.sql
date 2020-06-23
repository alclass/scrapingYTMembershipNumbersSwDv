-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Tempo de geração: 22-Jun-2020 às 21:28
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

-- --------------------------------------------------------

--
-- Estrutura da tabela `channels`
--

CREATE TABLE `channels` (
  `id` int(10) UNSIGNED NOT NULL,
  `ytchannelid` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nname` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category_id` smallint(5) UNSIGNED DEFAULT NULL,
  `each_n_days_for_dld` tinyint(4) NOT NULL DEFAULT '1',
  `scrapedate` date DEFAULT NULL,
  `obs` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='You Channels or Users';

-- --------------------------------------------------------

--
-- Estrutura da tabela `dailychannelsubscribernumbers`
--

CREATE TABLE `dailychannelsubscribernumbers` (
  `id` int(10) UNSIGNED NOT NULL,
  `ytchannelid` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subscribers` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `infodate` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Table to register daily number of ytchannel subscribers';

-- --------------------------------------------------------

--
-- Estrutura da tabela `individualvideostats`
--

CREATE TABLE `individualvideostats` (
  `id` int(11) NOT NULL,
  `ytvideoid` char(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `duration_in_sec` int(11) DEFAULT NULL,
  `publishdate` date DEFAULT NULL,
  `published_time_ago` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `infodate` date DEFAULT NULL,
  `changelog` text COLLATE utf8mb4_unicode_ci,
  `ytchannelid` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='individual yt [bra] video statistics';

-- --------------------------------------------------------

--
-- Estrutura da tabela `newsarticles`
--

CREATE TABLE `newsarticles` (
  `id` int(10) UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `filename` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `publisher_id` int(10) UNSIGNED DEFAULT NULL,
  `publishdate` date NOT NULL,
  `cat_id` smallint(5) UNSIGNED DEFAULT NULL,
  `reldir_id` int(10) UNSIGNED DEFAULT NULL,
  `is_read` tinyint(1) NOT NULL DEFAULT '0',
  `personal_rank` tinyint(4) NOT NULL DEFAULT '0',
  `comment` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='newsarticles to help write the book on the Brazilian 2018 El';

-- --------------------------------------------------------

--
-- Estrutura da tabela `nw_categories`
--

CREATE TABLE `nw_categories` (
  `id` smallint(5) UNSIGNED NOT NULL,
  `category_id` int(10) UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='nw_categories self-referential';

-- --------------------------------------------------------

--
-- Estrutura da tabela `nw_relativefolders`
--

CREATE TABLE `nw_relativefolders` (
  `id` int(10) UNSIGNED NOT NULL,
  `parent_id` int(10) UNSIGNED NOT NULL,
  `foldername` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='relativefolders self-referential';

-- --------------------------------------------------------

--
-- Estrutura da tabela `videosviews`
--

CREATE TABLE `videosviews` (
  `id` int(10) UNSIGNED NOT NULL,
  `views` int(10) UNSIGNED NOT NULL,
  `infodate` date NOT NULL,
  `ytvideoid` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `channels`
--
ALTER TABLE `channels`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ytchannelid_idx` (`ytchannelid`),
  ADD UNIQUE KEY `nname_idx` (`nname`);

--
-- Índices para tabela `dailychannelsubscribernumbers`
--
ALTER TABLE `dailychannelsubscribernumbers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ytchannelid_subs_fk` (`ytchannelid`);

--
-- Índices para tabela `individualvideostats`
--
ALTER TABLE `individualvideostats`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ytvideoid` (`ytvideoid`),
  ADD KEY `ytchannelid_fk` (`ytchannelid`);

--
-- Índices para tabela `newsarticles`
--
ALTER TABLE `newsarticles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `publishdate_idx` (`publishdate`);

--
-- Índices para tabela `nw_categories`
--
ALTER TABLE `nw_categories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id_idx` (`category_id`);

--
-- Índices para tabela `nw_relativefolders`
--
ALTER TABLE `nw_relativefolders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pid_idx` (`parent_id`);

--
-- Índices para tabela `videosviews`
--
ALTER TABLE `videosviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ytvideoid_fk` (`ytvideoid`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `channels`
--
ALTER TABLE `channels`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `dailychannelsubscribernumbers`
--
ALTER TABLE `dailychannelsubscribernumbers`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `individualvideostats`
--
ALTER TABLE `individualvideostats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `newsarticles`
--
ALTER TABLE `newsarticles`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `nw_categories`
--
ALTER TABLE `nw_categories`
  MODIFY `id` smallint(5) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `nw_relativefolders`
--
ALTER TABLE `nw_relativefolders`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `videosviews`
--
ALTER TABLE `videosviews`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

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
