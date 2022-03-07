#include <cstdlib>
#include <unistd.h>
#include <iostream>
#include <cmath>
int main()
{
  while (true)
  {
    std::cout << "Process id is " << getpid() << '\n';
    // do some work so it shows in top
    int sum;
    for (size_t i = 1; i < 100000; ++i)
      sum += sqrt(i);
    sleep(10);
  }
  return EXIT_SUCCESS;
}