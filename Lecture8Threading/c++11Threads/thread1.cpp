#include <thread>
#include <iostream>

void threadFunc()
{
	std::cout << "ID " << std::this_thread::get_id() << '\n';
}

int main()
{
	std::cout << "Parent " << std::this_thread::get_id() << '\n';
	std::thread t1(threadFunc);
	t1.join();
}