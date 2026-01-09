CREATE TABLE `Scores` (
  `highScore` INT NULL DEFAULT 0,
  `FirstName` VARCHAR(45) NOT NULL,
  `LastName` VARCHAR(45) NOT NULL,
  `UserID` INTEGER PRIMARY KEY); 
INSERT INTO `Scores` (`highScore`, `FirstName`, `LastName`) VALUES ('12312', 'Jon', 'Macey');
INSERT INTO `Scores` (`highScore`, `FirstName`, `LastName`) VALUES ('234', 'Jane', 'Doe');
INSERT INTO `Scores` (`highScore`, `FirstName`, `LastName`) VALUES ('324', 'anon', 'anon');