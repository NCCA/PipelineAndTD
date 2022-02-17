#include<iostream>
#include <sqlite_modern_cpp.h>

int main()
{
  try
  {

    /*
CREATE TABLE `Scores` (
  `highScore` INT NULL DEFAULT 0,
  `FirstName` VARCHAR(45) NOT NULL,
  `LastName` VARCHAR(45) NOT NULL,
  `UserID` INTEGER PRIMARY KEY); 
    */
    sqlite::database db("Scores.db");
      db << "select highScore,FirstName,LastName,UserID from Scores  ;"
            
            >> [&](int highScore, std::string FirstName, std::string  LastName, int UserID) 
            {
            std::cout << UserID << ' ' << FirstName << ' ' << LastName<<' '<< highScore << '\n';
        };
  
  }

  catch (std::exception& e) 
  {
   std::cout << e.what() <<'\n';
  }


}