#include <iostream>
#include <fstream>
#include <string>
#include "scene.pb.h"

// iterate scene and print
void printScene(const NCCA::Scene& _scene) 
{
  for(auto & asset : _scene.assets())
  {
    //auto asset=_scene.assets(i);
    std::cout<<"Name "<<asset.name()<<"\n";
    std::cout<<"id "<<asset.id()<<"\n";
    std::cout<<"description "<<asset.description()<<"\n";
    for(auto & mesh : asset.meshes()) 
    {
      std::cout<<"location "<<mesh.location()<<"\n";
      std::cout<<"type "<<mesh.type()<<"\n";      
    }
  }
}

// Main function:  Reads the entire address book from a file and prints all
//   the information inside.
int main(int argc, char* argv[])
{
  // Verify that the version of the library that we linked against is
  // compatible with the version of the headers we compiled against.
  GOOGLE_PROTOBUF_VERIFY_VERSION;

  if (argc != 2) 
  {
    std::cerr << "Usage:  " << argv[0] << " scene file\n" ;
    return EXIT_FAILURE;
  }

  NCCA::Scene scene;

  {
    // Read the existing scene
    std::fstream input(argv[1], std::ios::in | std::ios::binary);
    if (!scene.ParseFromIstream(&input)) 
    {
      std::cerr << "Failed to parse address book.\n";
      return EXIT_FAILURE;
    }
  }

  printScene(scene);

  // Optional:  Delete all global objects allocated by libprotobuf.
  google::protobuf::ShutdownProtobufLibrary();

  return EXIT_SUCCESS;
}
