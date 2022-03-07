#include <iostream>
#include <cstdlib>
#include <string>

int main()
{
  std::cout << "Program starting \n";
  auto env = std::getenv("ENV_STARTUP");
  if (env == nullptr)
  {
    std::cout << "You need to set ENV_STARTUP\n";
    exit(EXIT_FAILURE);
  }
  else
  {
    std::cout << "Working dir is " << env << '\n';
  }
  return EXIT_SUCCESS;
}