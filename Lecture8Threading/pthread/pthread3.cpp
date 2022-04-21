#include <iostream>
#include <cstdlib>
#include <array>
#include <pthread.h>


struct argStruct
{
	int arg1;
	char arg2;
};


void *threadFunc(void *arg)
{
	struct argStruct *args = (argStruct *)arg;
	for(int i=0; i<10; ++i)
		printf("thread function %d %c \n",args->arg1,args->arg2);
return 0;
}


int main()
{
	std::array<pthread_t,4> threadID;
	std::array<struct argStruct,4> args;

	for(int i=0; i<4; ++i)
	{
		args[i].arg1=i;
		args[i].arg2='a'+i;
		pthread_create(&threadID[i],0,threadFunc,(void *)&args[i]);
	}
	// now join

	for(auto &t : threadID)
	{
		pthread_join(t,0);
	}
}