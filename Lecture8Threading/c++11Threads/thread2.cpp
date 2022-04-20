#include <iostream>
#include <thread>
#include <cstdlib>
#include "Logger.h"
#include <vector>
#include <fmt/format.h>
#include <fmt/ostream.h>

void hello(int _which)
{
	auto this_id = std::this_thread::get_id();
	for (int i = 0; i < 400; ++i)
	{
		switch (_which)
		{
		case 0:
			Logger::info(fmt::format("{} hello from thread {}", this_id, i), false);
			break;
		case 1:
			Logger::warning(fmt::format("{} hello from thread {}", this_id, i), false);
			break;
		case 2:
			Logger::error(fmt::format("{} hello from thread {}", this_id, i), false);
			break;
		case 3:
			Logger::debug(fmt::format("{} hello from thread {}", this_id, i), false);
			break;
		}
	}
}
int main()
{
	auto nThreads = std::thread::hardware_concurrency();
	std::cout << "num threads " << nThreads << '\n';
	std::vector<std::thread> pool(nThreads);
	int i = 0;
	for (auto &t : pool)
		t = std::thread(hello, ++i);
	for (auto &t : pool)
		t.join();

	return EXIT_SUCCESS;
}