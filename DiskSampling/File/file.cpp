// g++ file.cpp `python-config --cflags --ldflags --libs --embed`
// from https://docs.python.org/3/extending/embedding.html
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <cstdlib>
#include <iostream>
#include <filesystem>
#include <vector>


int main(int argc, char **argv)
{


  if (argc == 1)
  {
    std::cout<<"Please pass file(s) to view on command line\n";
    exit(EXIT_FAILURE);
  }
  std::vector<std::string> files;
  namespace fs = std::filesystem;

  for(int i=1; i<argc; ++i)
  {
    if(fs::exists(argv[i]))
    {
      files.push_back(argv[i]);
    }
  }
  
  Py_Initialize();
  for(auto f : files)
  {
    std::cout<<"__________________________________________\n";
    std::cout<<"running "<<f<<'\n';
    auto fp = fopen(f.c_str(), "r");
    if (fp)
    {
        PyRun_SimpleFile(fp, f.c_str());
        fclose(fp);
    }
  }
  if (Py_FinalizeEx() < 0) 
  {
    std::cerr<<"Failed to exit python\n";
    // 120 is used by python examples not sure why!
    exit(120);
  }
  return EXIT_SUCCESS;
}