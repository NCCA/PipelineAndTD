#include <cstdlib>
#include <unistd.h>
#include <iostream>
int main()
{
  std::cout << "Process id is " << getpid() << '\n';
  std::cout << "User ID " << getuid() << '\n';
  std::cout << "Group ID " << getgid() << '\n';
  return EXIT_SUCCESS;
}