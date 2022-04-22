#include <thread>
#include <iostream>
#include "Logger.h"
#include <fmt/format.h>
#include <fmt/ostream.h>
#include <chrono>

int main()
{
  auto endTime=std::chrono::steady_clock::now() + std::chrono::seconds(3);
  int counter=0;
  Logger::warning(fmt::format("Counter is {}", counter));

  std::thread t([&]()
                {
                   Logger::info(fmt::format("In thread {}", std::this_thread::get_id()));
                   while(std::chrono::steady_clock::now()<endTime)
                    std::cout<<"from thread "<<counter++<<'\n';
                });
 
  while(std::chrono::steady_clock::now()<endTime)
        std::cout<<"main "<<counter++<<'\n';
  t.join();
  Logger::info(fmt::format("counter is {}", counter));
}