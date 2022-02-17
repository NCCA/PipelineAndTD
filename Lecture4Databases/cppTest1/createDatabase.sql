
# add tables
CREATE TABLE `Scores` (
  `highScore` INT NULL DEFAULT 0,
  `FirstName` VARCHAR(45) NOT NULL,
  `LastName` VARCHAR(45) NOT NULL,
  `UserID` INTEGER PRIMARY KEY);

# add data 
INSERT INTO Scores(highScore,FirstName,LastName) VALUES(100,"Jon","Macey");
INSERT INTO Scores(highScore,FirstName,LastName) VALUES(130,"Jon","Macey");
INSERT INTO Scores(highScore,FirstName,LastName) VALUES(120,"Jon","Macey");
INSERT INTO Scores(highScore,FirstName,LastName) VALUES(130,"Jon","Macey");
INSERT INTO Scores(highScore,FirstName,LastName) VALUES(12,"Jon","Macey");
INSERT INTO Scores(highScore,FirstName,LastName) VALUES(0,"Jon","Macey");


