#include<iostream>
#include <sqlite_modern_cpp.h>

int main()
{
  try
  {
    sqlite::database db("TheComputerStore.db");
    std::cout<<"Demo based on Computer Store code\n";
    std::cout<<"***************************************\n";
    std::cout<<"Select all products\n";
    std::cout<<"---------------------------------------\n";
    db << "select * from Products  ;"         
        >> [&](int code, std::string name, float price,int manufacturer) 
        {
          std::cout << code << ' '<<name<<' '<<price<<' '<<manufacturer<<'\n';
        };

    std::cout<<"***************************************\n";
    std::cout<<"Select the names of all the products in the store\n";
    std::cout<<"---------------------------------------\n";
    db << "SELECT Name FROM Products;"         
        >> [&](std::string name) 
        {
          std::cout <<name<<'\n';
        };
    
    std::cout<<"***************************************\n";
    std::cout<<" Select the name of the products with a price less than or equal to $200.\n";
    std::cout<<"---------------------------------------\n";
    db << "SELECT Name FROM Products WHERE Price <= 200;"         
        >> [&](std::string name) 
        {
          std::cout <<name<<'\n';
        };

    std::cout<<"***************************************\n";
    std::cout<<" Select all the products with a price between $60 and $120.\n";
    std::cout<<"---------------------------------------\n";
    db << "SELECT * FROM Products WHERE Price BETWEEN 60 AND 120;"         
        >> [&](int code, std::string name, float price,int manufacturer) 
        {
          std::cout << code << ' '<<name<<' '<<price<<' '<<manufacturer<<'\n';
        };

    std::cout<<"***************************************\n";
    std::cout<<" average price\n";
    std::cout<<"---------------------------------------\n";
    db << "SELECT AVG(Price) FROM Products WHERE Manufacturer=2;"         
        >> [&](float price) 
        {
          std::cout<<"Average price $" << price<<'\n';
        };
  
    std::cout<<"***************************************\n";
    std::cout<<" Select the names of manufacturer whose products have an average price larger than or equal to $150.\n";
    std::cout<<"---------------------------------------\n";
    
    db << "SELECT AVG(Price), Manufacturers.Name FROM Products INNER JOIN Manufacturers ON Products.Manufacturer = Manufacturers.Code GROUP BY Manufacturers.Name HAVING AVG(Price) >= 150;"         
        >> [&](float price,std::string name) 
        {
          std::cout << name<<' '<<price<<'\n';
        };
  
  
  
  }

  catch (std::exception& e) 
  {
   std::cout << e.what() <<'\n';
  }


}