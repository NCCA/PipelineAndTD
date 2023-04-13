#include <iostream>
#include <fstream>
#include <string>
#include "scene.pb.h"


void addToScene(NCCA::Asset *_asset)
{
  std::cout<<"Enter Asset Name\n";
  getline(std::cin, *_asset->mutable_name());
  std::cout << "Enter ID number: \n";
  int id;
  std::cin >> id;
  _asset->set_id(id);
  std::cin.ignore(256, '\n');
  std::cout << "Enter description (blank for none)\n";
  std::string desc;
  getline(std::cin, desc);
  if (!desc.empty()) 
  {
     _asset->set_description(desc);
  }
  



  auto *mesh=_asset->add_meshes(); 
  
  while (true) 
  {
    std::cout<<"Enter Mesh location (blank to exit)\n";
    std::string location;
    getline(std::cin,location);
    
    if (location.empty()) 
    {
      break;
    }
    mesh->set_location(location);
  }
}



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
    // Read the existing scnee if it exists.
    std::fstream input(argv[1], std::ios::in | std::ios::binary);
    if (!input) 
    {
      std::cout << argv[1] << ": File not found.  Creating a new file. \n";
    } 
    else if (!scene.ParseFromIstream(&input)) 
    {
      std::cerr << "Failed to parse scene.\n";
      return EXIT_FAILURE;
    }
  }

  // Add to scene
  addToScene(scene.add_assets());

  {
    // Write the new scene back to disk.
    std::fstream output(argv[1], std::ios::out | std::ios::trunc | std::ios::binary);
    if (!scene.SerializeToOstream(&output)) 
    {
      std::cerr << "Failed to write address book.\n";
      return EXIT_SUCCESS;
    }
  }

  // Optional:  Delete all global objects allocated by libprotobuf.
  google::protobuf::ShutdownProtobufLibrary();

  return EXIT_SUCCESS;
}
