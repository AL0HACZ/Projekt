-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 04, 2025 at 08:28 PM
-- Server version: 10.5.25-MariaDB
-- PHP Version: 8.2.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `vyuka39`
--

-- --------------------------------------------------------

--
-- Table structure for table `wiki_brands`
--

CREATE TABLE `wiki_brands` (
  `brand_id` int(11) NOT NULL,
  `brand_name` varchar(255) NOT NULL,
  `brand_country` varchar(255) NOT NULL,
  `brand_post` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;

-- --------------------------------------------------------

--
-- Table structure for table `wiki_cars`
--

CREATE TABLE `wiki_cars` (
  `car_id` int(11) NOT NULL,
  `car_brand` int(11) NOT NULL,
  `car_post` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;

-- --------------------------------------------------------

--
-- Table structure for table `wiki_categories`
--

CREATE TABLE `wiki_categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(255) NOT NULL,
  `category_description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;

-- --------------------------------------------------------

--
-- Table structure for table `wiki_category_assignments`
--

CREATE TABLE `wiki_category_assignments` (
  `assignment_category` int(11) NOT NULL,
  `assignment_car` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;

-- --------------------------------------------------------

--
-- Table structure for table `wiki_posts`
--

CREATE TABLE `wiki_posts` (
  `post_id` int(11) NOT NULL,
  `post_title` varchar(255) NOT NULL,
  `post_created` datetime NOT NULL DEFAULT current_timestamp(),
  `post_published` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;

-- --------------------------------------------------------

--
-- Table structure for table `wiki_revisions`
--

CREATE TABLE `wiki_revisions` (
  `revision_id` int(11) NOT NULL,
  `revision_post` int(11) NOT NULL,
  `revision_author` int(11) DEFAULT NULL,
  `revision_content` text NOT NULL,
  `revision_created` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;

-- --------------------------------------------------------

--
-- Table structure for table `wiki_sessions`
--

CREATE TABLE `wiki_sessions` (
  `session_id` int(11) NOT NULL,
  `session_user` int(11) NOT NULL,
  `session_time` datetime NOT NULL DEFAULT current_timestamp(),
  `session_ip` varchar(255) NOT NULL,
  `session_token` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;

-- --------------------------------------------------------

--
-- Table structure for table `wiki_users`
--

CREATE TABLE `wiki_users` (
  `user_id` int(11) NOT NULL,
  `user_username` varchar(50) NOT NULL,
  `user_displayname` varchar(50) NOT NULL,
  `user_root` tinyint(1) NOT NULL DEFAULT 0,
  `user_created` datetime NOT NULL DEFAULT current_timestamp(),
  `user_password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_czech_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `wiki_brands`
--
ALTER TABLE `wiki_brands`
  ADD PRIMARY KEY (`brand_id`),
  ADD KEY `wiki_brands_ibfk_post` (`brand_post`);

--
-- Indexes for table `wiki_cars`
--
ALTER TABLE `wiki_cars`
  ADD PRIMARY KEY (`car_id`),
  ADD KEY `wiki_cars_ibfk_post` (`car_post`);

--
-- Indexes for table `wiki_categories`
--
ALTER TABLE `wiki_categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `wiki_category_assignments`
--
ALTER TABLE `wiki_category_assignments`
  ADD PRIMARY KEY (`assignment_category`,`assignment_car`),
  ADD KEY `wiki_category_assignments_ibfk_car` (`assignment_car`);

--
-- Indexes for table `wiki_posts`
--
ALTER TABLE `wiki_posts`
  ADD PRIMARY KEY (`post_id`);

--
-- Indexes for table `wiki_revisions`
--
ALTER TABLE `wiki_revisions`
  ADD PRIMARY KEY (`revision_id`),
  ADD KEY `wiki_revisions_ibfk_post` (`revision_post`),
  ADD KEY `wiki_revisions_ibfk_author` (`revision_author`);

--
-- Indexes for table `wiki_sessions`
--
ALTER TABLE `wiki_sessions`
  ADD PRIMARY KEY (`session_id`),
  ADD KEY `wiki_sessions_ibfk_user` (`session_user`);

--
-- Indexes for table `wiki_users`
--
ALTER TABLE `wiki_users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_username` (`user_username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `wiki_brands`
--
ALTER TABLE `wiki_brands`
  MODIFY `brand_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `wiki_cars`
--
ALTER TABLE `wiki_cars`
  MODIFY `car_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `wiki_categories`
--
ALTER TABLE `wiki_categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `wiki_posts`
--
ALTER TABLE `wiki_posts`
  MODIFY `post_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `wiki_revisions`
--
ALTER TABLE `wiki_revisions`
  MODIFY `revision_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `wiki_sessions`
--
ALTER TABLE `wiki_sessions`
  MODIFY `session_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `wiki_users`
--
ALTER TABLE `wiki_users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `wiki_brands`
--
ALTER TABLE `wiki_brands`
  ADD CONSTRAINT `wiki_brands_ibfk_post` FOREIGN KEY (`brand_post`) REFERENCES `wiki_posts` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `wiki_cars`
--
ALTER TABLE `wiki_cars`
  ADD CONSTRAINT `wiki_cars_ibfk_post` FOREIGN KEY (`car_post`) REFERENCES `wiki_posts` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `wiki_category_assignments`
--
ALTER TABLE `wiki_category_assignments`
  ADD CONSTRAINT `wiki_category_assignments_ibfk_car` FOREIGN KEY (`assignment_car`) REFERENCES `wiki_cars` (`car_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `wiki_category_assignments_ibfk_category` FOREIGN KEY (`assignment_category`) REFERENCES `wiki_categories` (`category_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `wiki_revisions`
--
ALTER TABLE `wiki_revisions`
  ADD CONSTRAINT `wiki_revisions_ibfk_author` FOREIGN KEY (`revision_author`) REFERENCES `wiki_users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `wiki_revisions_ibfk_post` FOREIGN KEY (`revision_post`) REFERENCES `wiki_posts` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `wiki_sessions`
--
ALTER TABLE `wiki_sessions`
  ADD CONSTRAINT `wiki_sessions_ibfk_user` FOREIGN KEY (`session_user`) REFERENCES `wiki_users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
