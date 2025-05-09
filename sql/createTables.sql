DROP SCHEMA IF EXISTS `MovieTvDatabase` ;

CREATE SCHEMA `MovieTvDatabase` DEFAULT CHARACTER SET utf8mb4 ;

USE `MovieTvDatabase` ;

CREATE TABLE `MovieTvDatabase`.`MoviesAndShows` (
  `id` VARCHAR(12) NOT NULL,
  `Title` VARCHAR(200) NOT NULL,
  `StartYear` SMALLINT NULL,
  `EndYear` SMALLINT NULL,
  `Runtime` SMALLINT NULL,
  `Type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `MovieTvDatabase`.`People` (
  `id` VARCHAR(12) NOT NULL,
  `Name` VARCHAR(100) NOT NULL,
  `BirthYear` SMALLINT NULL,
  `DeathYear` SMALLINT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `Professions` (
  `type` varchar(45) NOT NULL,
  `PeopleId` varchar(12) NOT NULL,
  PRIMARY KEY (`type`,`PeopleId`),
  KEY `PeopleId_idx` (`PeopleId`),
  CONSTRAINT `PeopleId` FOREIGN KEY (`PeopleId`) REFERENCES `People` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `MovieTvDatabase`.`Ratings` (
  `movShowId` VARCHAR(12) NOT NULL,
  `avgRating` DOUBLE NOT NULL,
  `numVotes` INT NOT NULL,
  PRIMARY KEY (`movShowId`),
  CONSTRAINT `movShowId`
    FOREIGN KEY (`movShowId`)
    REFERENCES `MovieTvDatabase`.`MoviesAndShows` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `Roles` (
  `movShowId` varchar(12) NOT NULL,
  `peopleId` varchar(12) NOT NULL,
  `category` varchar(45) NOT NULL,
  `character` varchar(200) DEFAULT NULL,
  `ordering` int NOT NULL,
  PRIMARY KEY (`movShowId`,`ordering`),
  KEY `rolesPersonId_idx` (`peopleId`),
  CONSTRAINT `rolesMovShowId` FOREIGN KEY (`movShowId`) REFERENCES `MoviesAndShows` (`id`),
  CONSTRAINT `rolesPersonId` FOREIGN KEY (`peopleId`) REFERENCES `People` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `MovieTvDatabase`.`KnownFor` (
  `peopleId` VARCHAR(12) NOT NULL,
  `movShowId` VARCHAR(12) NOT NULL,
  PRIMARY KEY (`peopleId`, `movShowId`),
  INDEX `movShowId_idx` (`movShowId` ASC) VISIBLE,
  CONSTRAINT `knownPersonId`
    FOREIGN KEY (`peopleId`)
    REFERENCES `MovieTvDatabase`.`People` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `knownForId`
    FOREIGN KEY (`movShowId`)
    REFERENCES `MovieTvDatabase`.`MoviesAndShows` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

