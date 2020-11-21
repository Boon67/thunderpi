SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `environmental`
--
SET @DBNAME= 'env';
SET @DBLOGIN= 'environment_logger';
SET @DBPASSWORD='password';

SET @query = CONCAT('DROP DATABASE `', @DBNAME, '`');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @query = CONCAT('CREATE DATABASE `', @DBNAME, '`');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-----------------------------------------------------------
SET @query = CONCAT('DROP USER "',@DBLOGIN,'"@"localhost" ');
PREPARE stmt FROM @query; 
EXECUTE stmt; 
DEALLOCATE PREPARE stmt;

SET @query = CONCAT('CREATE USER "',@DBLOGIN,'"@"localhost" IDENTIFIED BY "',@DBPASSWORD,'" ');
PREPARE stmt FROM @query; 
EXECUTE stmt; 
DEALLOCATE PREPARE stmt;

SET @query = CONCAT('
    GRANT ALL PRIVILEGES ON ',@DBNAME, '.* TO "',@DBLOGIN,'"@"localhost" IDENTIFIED BY "',@DBPASSWORD,'" ');
        
    /*WITH
          MAX_QUERIES_PER_HOUR 120 MAX_CONNECTIONS_PER_HOUR 60 MAX_UPDATES_PER_HOUR 60 
          MAX_USER_CONNECTIONS 2' */
PREPARE stmt FROM @query; 
EXECUTE stmt; 
DEALLOCATE PREPARE stmt;

USE env
--
-- Table structure for table `assets`
--

CREATE TABLE `assets` (
  `asset_id` int(11) NOT NULL,
  `asset_name` varchar(255) NOT NULL,
  `asset_description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `records`
--

CREATE TABLE `records` (
  `record_id` int(11) NOT NULL,
  `record` text NOT NULL,
  `ts` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `sites`
--

CREATE TABLE `sites` (
  `site_id` int(11) NOT NULL,
  `site_name` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sub_assets`
--

CREATE TABLE `sub_assets` (
  `sub_asset` int(11) NOT NULL,
  `sub_asset_name` varchar(255) NOT NULL,
  `sub_asset_description` text DEFAULT NULL,
  `asset_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `assets`
--
ALTER TABLE `assets`
  ADD PRIMARY KEY (`asset_id`);

--
-- Indexes for table `records`
--
ALTER TABLE `records`
  ADD PRIMARY KEY (`record_id`);

--
-- Indexes for table `sites`
--
ALTER TABLE `sites`
  ADD PRIMARY KEY (`site_id`);

--
-- Indexes for table `sub_assets`
--
ALTER TABLE `sub_assets`
  ADD PRIMARY KEY (`sub_asset`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `assets`
--
ALTER TABLE `assets`
  MODIFY `asset_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `records`
--
ALTER TABLE `records`
  MODIFY `record_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=195;
--
-- AUTO_INCREMENT for table `sites`
--
ALTER TABLE `sites`
  MODIFY `site_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `sub_assets`
--
ALTER TABLE `sub_assets`
  MODIFY `sub_asset` int(11) NOT NULL AUTO_INCREMENT;

