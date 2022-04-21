#include <thread>
#include <iostream>
#include <vector>
#include <cstdlib>
#include <string>
#include <algorithm>
#include <chrono>
#include <functional>
#include <fmt/format.h>
#include <fmt/ostream.h>

#include "Logger.h"

void threadFunc(const std::string &a, const std::string &b)
{
  while (true)
  {
    Logger::info(fmt::format("threadFunc(str,str) ID {} value {}  {}", std::this_thread::get_id(), a, b));
    std::this_thread::sleep_for(std::chrono::seconds(2));
  }
}
void threadFunc(int a)
{
  while (true)
  {
    Logger::warning(fmt::format("threadFunc(int) ID {} value {} \n", std::this_thread::get_id(), a));
    std::this_thread::sleep_for(std::chrono::seconds(3));
  }
}

void threadFunc(double a)
{
  while (true)
  {

    Logger::error(fmt::format("threadFunc(double) ID {} value {} ", std::this_thread::get_id(), a));
    std::this_thread::sleep_for(std::chrono::seconds(6));
  }
}

int main()
{
  std::vector<std::thread> threads;
  threads.reserve(4);

  auto funca = std::bind<void(int)>(threadFunc, 1);
  threads.emplace_back(funca);

  auto funcb = std::bind<void(double)>(threadFunc, 0.002);
  threads.emplace_back(funcb);

  std::string a = "hello";
  std::string b = " c++ 11 threads";
  auto funcs = std::bind<void(const std::string &, const std::string &)>(threadFunc, a, b);
  threads.emplace_back(funcs);

  using namespace std::placeholders; // for _1, _2, _3...
  auto funcs2 = std::bind<void(const std::string &, const std::string &)>(threadFunc, _1, _2);
  threads.emplace_back(funcs2, "placeholders", "are cool");
  std::for_each(std::begin(threads), std::end(threads), std::mem_fn(&std::thread::join));
  return EXIT_SUCCESS;
}