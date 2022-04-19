#include <iostream>
#include <thread>
#include <cstdlib>
#include "Logger.h"
#include <vector>
#include <fmt/format.h>
#include <fmt/ostream.h>

void hello()
{
	std::thread::id this_id = std::this_thread::get_id();
	for (int i = 0; i < 10; ++i)
		Logger::info(fmt::format("{0} hello from thread {1}", this_id, i));
}

int main()
{
	auto nThreads = std::thread::hardware_concurrency();
	std::cout << "num threads " << nThreads << '\n';
	std::vector<std::thread> pool(nThreads);
	for (auto &t : pool)
		t = std::thread(hello);
	for (auto &t : pool)
		t.join();

	return EXIT_SUCCESS;
}