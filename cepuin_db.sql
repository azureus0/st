-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 06, 2025 at 09:05 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cepuin_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `mode` varchar(50) NOT NULL,
  `file_path` varchar(500) DEFAULT NULL,
  `image_path` varchar(500) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`id`, `username`, `subject`, `description`, `mode`, `file_path`, `image_path`, `timestamp`) VALUES
(12, 'Anonymous', 'Pencurian PC Kantor', 'gAAAAABpDFGWVy5i_2NuKM3pqpNShWMQCRCaZTJinV6NURvC6LqpAGgB2bL0DWRtfEzxumAamrdojTvCWPXnu32fHhi1xeIOrXodZRinwuHaHdAGBG_Sie7L0TdDkIz-gQjikvV4XVKVG-ZwupD8SajD4oFMZpvNNg==', 'biasa', 'uploads\\files\\83b3fca3f5244e34aa091bd0080a7c4d_budi_nyuri.jpg.enc', NULL, '2025-11-06 07:43:18'),
(13, 'Anonymous', 'Korupsi', 'gAAAAABpDFH8BCNdGPV5H8IkGNjfdR2B7gLmDoLEhFtH_f7npkh2UsuCncfW_y9h1H5QtWU41ps04l4sUfZ9i5jCGTcFU3iPDw==', 'steganografi', NULL, 'uploads\\images\\stego_72a7f6e4463a45858b3ea0de18e66527_robot.png', '2025-11-06 07:45:00'),
(14, 'Anonymous', 'Gratifikasi', 'gAAAAABpDFURVyth10MnWCMXO68481KaGVrf4jUG2YpHPOT9qW7jZ355c1AYLdLP9N-4kvdXUciZjKy-cwBuGiMlfc9VgPNfiSii0--iEzs0VlBlIr_x5Rc=', 'steganografi', NULL, 'uploads\\images\\stego_b41a589105c641968e45c31cd9f9189b_39gagsflzec71.png', '2025-11-06 07:58:09');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `salt` varchar(32) NOT NULL,
  `role` varchar(50) DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `salt`, `role`) VALUES
(0, 'admin', '689e241e7a6d47d40191eb57f2da41c79c74a7de5bc287e302fe1a05dfb15a83dcb4b3f7c38e35d264ffca451e003a36ffd82968ba448969a4a2dea1be15d0e3', '56080c7b0217c23d9d903244f76cfaa6', 'admin'),
(1, 'wadaw', 'b343ed47968bdf1233879fc1191a85c5b4a4938f319369c0f9d26e14ebba756d6e90654007e60b30baddcf16f1a6edce110af3636ba4b9eda0b22cf41944c186', 'efefa7aaa73cd30f2d2da3625ff991a5', 'user'),
(2, 'mamamia', '07fb654ab01708942715011ec25b57faffaa73cb80b69d44dcaaa4688990102b4419a9272d89482a2460441aa6ca8cf3310db546c1835acc38de22ec3bc3a93c', 'e37ade444458d1350eaf2f5908bbbc76', 'user'),
(3, 'yedi', '1d5359dbeada304baef89af67d7622ff09705c18aeef05988ff98c95cfdbf97548da9445de2fd4caedf3f5014807fbb57ec6f70829e1bd79e7bb804c140e014d', '86abae23ecfe1462c728945170946bcf', 'user'),
(4, 'y', '54c21e9ea3c9a5ad33f20cfe75861936059cf05bbca20a9aac4241cf8d55ca1397be8a3feb91588fc8841ded067d65d97eb1b67d77d63ec5e42a509a90c11f07', 'c42856de88f3475a1296450306726d53', 'user'),
(5, 'yooo', '4cb65bd33181d254dfc5f8cf4429c64599b5a63815379bb0b21cff7a3de56616f6c32269695705ab06296d5fc868a53ae4689ee8b1aadecd8b76151914ec8b65', 'de1dd53b9196427ef8656dc199316046', 'user'),
(6, 'e', 'c2a8b7b2afb7fc44fafdf442e55c666b77bf06bcad138236eb1bc667af389ee0674f2acbe1629b069a9ef8da0c376304560c8f8af0eaba896a9e7bee5fd57967', '47f328128c06d5695f0b8475ca744690', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
