#include <iostream>
#include <cstdlib>
#include <array>
#include <pthread.h>

void *threadFunc(void *arg)
{
	for(int i=0; i<3; ++i)
	{
		std::cout<<"thread func "<<i<<' ';
	//	std::cout.flush();
	}
std::cout<<'\n';
return 0;
}


int main()
{
	std::array<pthread_t,8> threadID;
	for(auto &t : threadID)
	{
		pthread_create(&t,0,threadFunc,0);
	}

	// now join
	for(auto &t : threadID)
	{
		std::cout<<"*************************\n";
		pthread_join(t,0);
	}
	std::cout<<"###########################\n";
}








