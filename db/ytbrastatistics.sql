-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Tempo de geração: 24-Maio-2020 às 22:32
-- Versão do servidor: 5.7.30-0ubuntu0.18.04.1
-- versão do PHP: 7.2.24-0ubuntu0.18.04.4

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
  `obs` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
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
  `date` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Table to register daily number of ytchannel subscribers';

-- --------------------------------------------------------

--
-- Estrutura da tabela `individualvideostats`
--

CREATE TABLE `individualvideostats` (
  `id` int(11) NOT NULL,
  `ytchannelid` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ytvideoid` char(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `videoname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `duration_in_sec` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `views` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='individual yt [bra] video statistics';

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
  ADD PRIMARY KEY (`id`);

--
-- Índices para tabela `individualvideostats`
--
ALTER TABLE `individualvideostats`
  ADD PRIMARY KEY (`id`);

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
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
