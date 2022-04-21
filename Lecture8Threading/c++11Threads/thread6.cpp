#include <thread>
#include <iostream>
#include <vector>
#include <memory>
#include <cstdlib>
#include <string>
#include <functional>
#include <fmt/format.h>
#include <fmt/ostream.h>

#include "Logger.h"

class Task
{
public:
  Task(int id) : m_id(id) {}
  void task(const std::string &a, const std::string &b)
  {
    while (true)
    {
      Logger::info(fmt::format("task(str,str) {} ID {} value {} {}", m_id, std::this_thread::get_id(), a, b));
    }
  }
  void task(int a)
  {
    while (true)
    {
      Logger::warning(fmt::format("task(int) {} ID {} value {}", m_id, std::this_thread::get_id(), a));
    }
  }
  void task(double a)
  {
    while (true)
    {
      Logger::error(fmt::format("task(double) {} ID {} value {}", m_id, std::this_thread::get_id(), a));
    }
  }

private:
  int m_id;
};

int main()
{
  std::vector<std::thread> threads;
  threads.reserve(6);
  std::shared_ptr<Task> pTask(new Task(10));
  Task b(20);

  auto funca = std::bind(static_cast<void (Task::*)(int)>(&Task::task), b, 2);
  threads.emplace_back(funca);

  auto funcb = std::bind(static_cast<void (Task::*)(int)>(&Task::task), pTask.get(), 99);
  threads.emplace_back(funcb);

  auto funcc = std::bind(static_cast<void (Task::*)(double)>(&Task::task), b, 2.23);
  threads.emplace_back(funcc);

  auto funcd = std::bind(static_cast<void (Task::*)(double)>(&Task::task), pTask, 9.9);
  threads.emplace_back(funcd);

  std::string sa = "hello";
  std::string sb = " c++ 11 threads";
  auto funce = std::bind(static_cast<void (Task::*)(const std::string &, const std::string &)>(&Task::task), b, sa, sb);
  threads.emplace_back(funce);
  auto funcf = std::bind(static_cast<void (Task::*)(const std::string &, const std::string &)>(&Task::task), pTask.get(), sa, sb);
  threads.emplace_back(funcf);

  std::for_each(std::begin(threads), std::end(threads), std::mem_fn(&std::thread::join));

  return EXIT_SUCCESS;
}