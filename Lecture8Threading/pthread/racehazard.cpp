#include <iostream>
#include <cstdlib>
#include <memory>
#include <array>
#include <unistd.h>
#include <pthread.h>

std::unique_ptr<char []>sharedMem;
constexpr int SIZE=20;

void *starFillerThread(void *arg)
{
	while(1)
	{
	printf("Star Filler\n");
	for(int i=0; i<SIZE; ++i)
		sharedMem[i]='*';
	sleep(1);
	}
}

void *hashFillerThread(void *arg)
{
	while(1)
	{
	printf("hash filler\n");
	for(int i=0; i<SIZE; ++i)
		sharedMem[i]='#';
	sleep(2);
	}
}


void *consumerThread(void *arg)
{
		while(1)
		{
		printf("Consumer\n");
		for(int i=0; i<SIZE; ++i)
			printf("%c",sharedMem[i]);
		printf("\n");
		sleep(2);
		}
}

int main()
{
	sharedMem= std::make_unique<char []>(SIZE);//    .reset(new char[SIZE]);
	std::array<pthread_t,3> threadID;

	pthread_create(&threadID[0],0,starFillerThread,0);
	pthread_create(&threadID[1],0,hashFillerThread,0);
	pthread_create(&threadID[2],0,consumerThread,0);

	for(auto &t : threadID)
		pthread_join(t,0);

}