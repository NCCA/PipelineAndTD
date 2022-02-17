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
    std::string query;
    std::getline (std::cin,query);
    std::cout<<query;
    sqlite::database db("Scores.db");
      db << query.c_str() 
            
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