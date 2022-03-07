#include <iostream>
#include <cstdlib>
#include <string>

int main(int arc, char **argv, char **environ)
{
  std::cout << "Program starting \n";
  int i = 0;
  while (environ[i] != nullptr)
  {
    std::cout << environ[i++] << '\n';
  }

  return EXIT_SUCCESS;
}