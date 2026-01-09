#SQLITE Simple Example

This demo uses a simple Scores table created using the following commands (however supplied)

```
/public/devel/bin/sqlite3 scores.db 
```

```
 CREATE TABLE `Scores` (
  `highScore` INT NULL DEFAULT 0,
  `FirstName` VARCHAR(45) NOT NULL,
  `LastName` VARCHAR(45) NOT NULL,
  `UserID` INTEGER PRIMARY KEY); 

```

With data inserted using the following command

```
INSERT INTO `Scores` (`highScore`, `FirstName`, `LastName`) VALUES ('12312', 'Jon', 'Macey');
INSERT INTO `Scores` (`highScore`, `FirstName`, `LastName`) VALUES ('234', 'Jane', 'Doe');
INSERT INTO `Scores` (`highScore`, `FirstName`, `LastName`) VALUES ('324', 'anon', 'anon');

```

In the University the sqlite3 lib is installed in /public/devel use the following flags for compilation

```
-I/public/devel/include/sqlite -L/public/devel/lib -lsqlite3
```


