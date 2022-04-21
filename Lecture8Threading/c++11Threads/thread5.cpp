#include <thread>
#include <iostream>
#include <assert.h>
#include <chrono>
#include <future>
#include "Logger.h"

void threadFunction(std::future<void> futureObj)
{
  Logger::info("Thread Start");
  // check every so often for the exit signal
  while (futureObj.wait_for(std::chrono::milliseconds(1)) == std::future_status::timeout)
  {
    Logger::warning("Thread Working");
    std::this_thread::sleep_for(std::chrono::seconds(1));
  }
  Logger::critical("Thread End");
}
int main()
{
  // Create a std::promise to signal our exit
  std::promise<void> exitSignal;
  // grab the future and pass to thread when starting
  std::future<void> futureObj = exitSignal.get_future();
  //
  std::thread t(&threadFunction, std::move(futureObj));

  Logger::info("Press enter to stop");
  std::getchar();
  // Set the value in promise
  exitSignal.set_value();
  // we can join or detach here to release the thread
  // if we don't we get an abort
  t.detach();

  // Wait for thread to join
  Logger::info("Exiting Main Function");
  return EXIT_SUCCESS;
}