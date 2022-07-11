CREATE DATABASE IF NOT EXISTS `seteam32`;

USE `seteam32`;

DROP TABLE IF EXISTS `Visitor`;

CREATE TABLE `Visitor` (
  `citizen_id` INT NOT NULL,
  `visitor_name` varchar(200) NOT NULL,
  `address` varchar(200) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `email` varchar(200) NOT NULL,
  `device_id` varchar(20) NOT NULL UNIQUE,
  `infected` boolean NOT NULL DEFAULT false,
  PRIMARY KEY (`citizen_id`)
);

DROP TABLE IF EXISTS `Visitor_to_places`;

CREATE TABLE `Visitor_to_places` (
  `QRcode` varchar(20) NOT NULL,
  `device_id` varchar(20) NOT NULL,
  `entry_date` date NOT NULL,
  `entry_time` time NOT NULL,
  `exit_date` date NOT NULL DEFAULT "1900-01-01",
  `exit_time` time NOT NULL DEFAULT "00:00:00.000",
  PRIMARY KEY (
    `QRcode`,
    `device_id`,
    `entry_date`,
    `entry_time`
  )
);

DROP TABLE IF EXISTS `Places`;

CREATE TABLE `Places` (
  `place_id` INT NOT NULL,
  `place_name` varchar(200) NOT NULL,
  `address` varchar(200) NOT NULL,
  `QRcode` varchar(20) NOT NULL UNIQUE,
  PRIMARY KEY (`place_id`)
);

DROP TABLE IF EXISTS `Agent`;

CREATE TABLE `Agent` (
  `agent_id` INT NOT NULL,
  `username` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  PRIMARY KEY (`agent_id`)
);

DROP TABLE IF EXISTS `Hospital`;

CREATE TABLE `Hospital` (
  `hospital_id` INT NOT NULL,
  `username` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  `approved` BOOLEAN NOT NULL DEFAULT false,
  PRIMARY KEY (`hospital_id`)
);

-- USE `seteam34`;
DROP TABLE IF EXISTS `Hospital_Requests`;

CREATE TABLE `Hospital_Requests` (
  `username` varchar(200) NOT NULL,
  `request_id` INT(6) ZEROFILL NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`request_id`)
);

INSERT INTO Agent(agent_id, username, password)
VALUES (1234567890, 'agent@gmail.com', 'hello@12');

INSERT INTO Hospital(hospital_id, username, password)
VALUES (1234567890, 'legithospital@gmail.com', 'hello@12');