#include <cstdlib>
#include <unistd.h>
#include <signal.h>
#include <iostream>
#include <cmath>

int g_count = 0;
void sig_handler(int signum)
{
  std::cout << "Got Signal " << signum << '\n';
  if (signum == SIGHUP)
  {
    std::cout << "here is my number" << g_count << '\n';
    exit(EXIT_SUCCESS);
  }
  else if (signum == SIGINT)
  {
    std::cout << "stop interupting!\n";
  }
}
int main()
{
  signal(SIGHUP, sig_handler); // Register signal handler
  signal(SIGINT, sig_handler); // Register signal handler

  while (true)
  {
    std::cout << "Process id is " << getpid() << '\n';
    // do some work so it shows in top
    g_count++;
    sleep(10);
  }
  return EXIT_SUCCESS;
}