// g++ embed.cpp `python-config --cflags --ldflags --libs --embed`
// from https://docs.python.org/3/extending/embedding.html
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <cstdlib>
#include <iostream>

int main(int argc, char **argv)
{
  wchar_t *program = Py_DecodeLocale(argv[0], NULL);
  if (program == NULL) 
  {
    std::cerr<<"Fatal error: cannot decode argv[0]\n";
    exit(EXIT_FAILURE);
  }

  Py_SetProgramName(program);  /* optional but recommended */
  Py_Initialize();
  PyRun_SimpleString("from time import time,ctime\n"
                      "print('Today is', ctime(time()))\n");
  if (Py_FinalizeEx() < 0) 
  {
    std::cerr<<"Failed to exit python\n";
    // 120 is used by python examples not sure why!
    exit(120);
  }
  PyMem_RawFree(program);
  return EXIT_SUCCESS;
}