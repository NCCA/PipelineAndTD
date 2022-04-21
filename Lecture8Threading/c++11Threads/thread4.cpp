#include <iostream>
#include <thread>
#include <cstdlib>
#include "Logger.h"
#include <vector>
#include <fmt/format.h>
#include <fmt/ostream.h>

void func()
{
  while (true)
  {
    Logger::info("Thread function");
    std::this_thread::sleep_for(std::chrono::seconds(1));
  }
}

int main()
{
  std::thread t(func);
  t.detach();
  while (true)
  {
    Logger::warning("In Main");
    std::this_thread::sleep_for(std::chrono::seconds(2));
  }

  return EXIT_SUCCESS;
}