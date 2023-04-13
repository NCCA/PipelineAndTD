#include <iostream>
#include <cstdlib>
#include <fstream>
#include "Sphere.h"

int main()
{
  std::cout<<"creating object\n";
  Sphere s1("Sphere1 test 1 2",0.0f,2.4f,0.4f,2.3l);
  std::cout<<s1<<"\n\n";
  std::ofstream ofs("Sphere.txt");
   // save data to archive
   {
   boost::archive::text_oarchive oa(ofs);
   // write class instance to archive
   oa << s1;
   // archive and stream closed when destructors are called
   }
   Sphere s2;
   std::cout<<"created Empty object \n";
   std::cout<<s2<<"\n\n";
   {
     // create and open an archive for input
     std::ifstream ifs("Sphere.txt");
     boost::archive::text_iarchive ia(ifs);
     // read class state from archive
     ia >> s2;
     // archive and stream closed when destructors are called
    }
   std::cout<<s2<<"\n\n";
  return EXIT_SUCCESS;
}

