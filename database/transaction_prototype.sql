-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 28, 2019 at 11:10 AM
-- Server version: 10.3.15-MariaDB
-- PHP Version: 7.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `transaction_prototype`
--

-- --------------------------------------------------------

--
-- Table structure for table `master`
--

CREATE TABLE `master` (
  `id` int(10) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `balance` int(10) NOT NULL,
  `registration_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `master`
--

INSERT INTO `master` (`id`, `first_name`, `last_name`, `balance`, `registration_date`) VALUES
(1, 'Bernard', 'Lonaldo', 250, '2019-08-27 12:11:59'),
(2, 'Test', 'Test', 100, '2019-08-27 12:12:23'),
(3, 'Test02', 'Temp', 130, '2019-08-27 12:12:38'),
(8, 'Bernard', 'Bell', 420, '2019-08-27 14:26:45'),
(9, 'Well', 'Diamond', 200, '2019-08-27 14:28:06');

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `transaction_id` int(10) NOT NULL,
  `user_id` int(10) NOT NULL,
  `prev_amount` int(10) NOT NULL,
  `curr_amount` int(10) NOT NULL,
  `action_id` varchar(32) NOT NULL,
  `amount` int(10) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`transaction_id`, `user_id`, `prev_amount`, `curr_amount`, `action_id`, `amount`, `timestamp`) VALUES
(1, 3, 220, 230, '02', 10, '2019-08-28 03:30:20'),
(2, 3, 230, 130, '01', 100, '2019-08-28 03:31:13'),
(3, 8, 410, 420, '02', 10, '2019-08-28 03:46:14');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `master`
--
ALTER TABLE `master`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`transaction_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `master`
--
ALTER TABLE `master`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `transaction_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
