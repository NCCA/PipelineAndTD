#include <thread>
#include <atomic>
#include <cassert>
#include <string>
#include <iostream>
#include <random>
std::atomic<std::string*> ptr;
std::default_random_engine rng;
constexpr size_t size=20;

std::uniform_int_distribution<int> range(1,size);
std::unique_ptr<std::string> p ;
void producer()
{
  while(true)
  {
   p  = std::make_unique<std::string>(range(rng),'*');
    ptr.store(p.get(), std::memory_order_release);
    std::this_thread::sleep_for(std::chrono::milliseconds(40));
  }
}
void consumer()
{
    std::string clear(size,' ');
    std::string* str;
    while(true)
    {
      while (!(str = ptr.load(std::memory_order_consume))) ;
     
      std::cout<<clear<<'\r';
      std::cout<<*str<<'\r';
      std::cout.flush();
      
      std::this_thread::sleep_for(std::chrono::milliseconds(40));
    }
}
 
int main()
{
    std::thread produce(producer);
    std::thread consume(consumer);
    produce.join(); 
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    consume.join();
}