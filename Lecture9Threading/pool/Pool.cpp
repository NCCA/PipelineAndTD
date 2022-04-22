#include <vector>
#include <thread>
#include <iostream>
#include "Logger.h"
#include <fmt/format.h>
#include <fmt/ostream.h>
#include <chrono>
#include <mutex>
#include <condition_variable>
#include <numeric>
#include <random>

struct Pool
{
  Pool(size_t _size)
  {
    things.resize(_size);
    std::iota(std::begin(things),std::end(things),0);
  }
  int getThing()
  {
    std::unique_lock<std::mutex> lock(mutex);
    while(things.empty())
    {
        Logger::debug("Waiting Lock");
        cv.wait(lock);
    }
    auto r=std::move(things.back()); // I know it's an int
    things.pop_back();
    return r;
  }

  void returnThing(int _t)
  {
    std::unique_lock<std::mutex> lock(mutex);
    things.push_back(_t);
    lock.unlock();
    Logger::error("calling Notify");
    cv.notify_one();
    //cv.notify_all();
    
  }
  std::vector<int> things;
  std::mutex mutex;
  std::condition_variable cv;
};

int main()
{
  std::default_random_engine rng;
  std::uniform_int_distribution<int> sleep_for(500,1550);

  Pool pool(4);
  auto nThreads = std::thread::hardware_concurrency();
  Logger::info(fmt::format("Have {} threads",nThreads));
	std::vector<std::thread> workers(nThreads);
  int readableID=0;
  for(auto &t : workers)
  {

    t=std::thread([&](){
      thread_local int localID=readableID;
      while(true)  
      {
        // grab thing from pool
        auto thing=pool.getThing();
        Logger::warning(fmt::format("Thread {} has thing {}",localID,thing));
        // simulate work
        std::this_thread::sleep_for(std::chrono::milliseconds(sleep_for(rng)));
        // return when done
        pool.returnThing(thing);
      }
    });
    ++readableID;
  }
  for(auto &t : workers)
    t.join();
}