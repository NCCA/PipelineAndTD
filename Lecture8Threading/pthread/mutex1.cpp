#include <iostream>
#include <cstdlib>
#include <memory>
#include <array>
#include <unistd.h>
#include <pthread.h>

std::unique_ptr<char []>sharedMem;
constexpr int SIZE=20;


pthread_mutex_t mutex=PTHREAD_MUTEX_INITIALIZER;

void *starFillerThread(void *arg)
{

	while(1)
	{
	pthread_mutex_lock (&mutex);
	printf("Star Filler\n");
	for(int i=0; i<SIZE; ++i)
		sharedMem[i]='*';
	pthread_mutex_unlock(&mutex);
	sleep(2);
	}
}

void *hashFillerThread(void *arg)
{
	while(1)
	{
	pthread_mutex_lock (&mutex);
	printf("hash filler\n");
	for(int i=0; i<SIZE; ++i)
		sharedMem[i]='#';
	pthread_mutex_unlock (&mutex);
	sleep(2);
	}
}


void *consumerThread(void *arg)
{
		while(1)
		{
		pthread_mutex_lock (&mutex);
		printf("Consumer\n");
		for(int i=0; i<SIZE; ++i)
			printf("%c",sharedMem[i]);
		pthread_mutex_unlock (&mutex);
		printf("\n");
		sleep(2);
		}
}

int main()
{

	sharedMem.reset(  new char[SIZE]);
	std::array<pthread_t,3> threadID;

  pthread_mutex_init(&mutex, 0);
	pthread_create(&threadID[2],0,consumerThread,0);
	pthread_create(&threadID[0],0,starFillerThread,0);
	pthread_create(&threadID[1],0,hashFillerThread,0);

	for(auto &t : threadID)
		pthread_join(t,0);

}