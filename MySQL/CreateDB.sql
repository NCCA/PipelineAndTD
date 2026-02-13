create database computer_store;
use computer_store;

CREATE TABLE Manufacturers (
                            Code INTEGER PRIMARY KEY NOT NULL,
                            Name TEXT NOT NULL
                            );
CREATE TABLE Products ( Code INTEGER PRIMARY KEY NOT NULL,
                        Name TEXT NOT NULL ,
                        Price REAL NOT NULL ,
                        Manufacturer INTEGER NOT NULL
                        );

INSERT INTO Manufacturers(Code, Name)
VALUES(1, 'Sony'),
       (2, 'Creative Labs'),
       (3, 'Hewlett-Packard'),
       (4, 'Iomega'),
       (5, 'Fujitsu'),
       (6, 'Winchester');

INSERT INTO Products(Code, Name, Price, Manufacturer)
VALUES(1, 'Hard drive', 240, 5),
       (2, 'Memory', 120, 6),
       (3, 'ZIP drive', 150, 4),
       (4, 'Floppy disk', 5, 3),
       (5, 'Monitor', 240, 1),
       (6, 'DVD drive', 180, 2),
       (7, 'CD drive', 90, 2),
       (8, 'Printer', 270, 3),
       (9, 'Toner cartridge', 66, 3),
       (10, 'DVD burner', 180, 2);
