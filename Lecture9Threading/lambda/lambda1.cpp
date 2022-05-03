#include <thread>
#include <iostream>
#include "Logger.h"
#include <fmt/format.h>
#include <fmt/ostream.h>

int main()
{
  Logger::warning(fmt::format("Parent id {}", std::this_thread::get_id()));
  std::thread t1([]()
                 { Logger::info(fmt::format("In thread {}", std::this_thread::get_id())); });
  t1.join();
}