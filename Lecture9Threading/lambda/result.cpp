#include <thread>
#include <iostream>
#include "Logger.h"
#include <fmt/format.h>
#include <fmt/ostream.h>

int main()
{
  int sum = 0;

  Logger::warning(fmt::format("Sum is {}", sum));

  std::thread t([&]()
                {
                   Logger::info(fmt::format("In thread {}", std::this_thread::get_id()));
                   for (int i = 0; i < 100; ++i)
                     sum += i; 
                });
  t.join();
  Logger::info(fmt::format("Sum is {}", sum));
}