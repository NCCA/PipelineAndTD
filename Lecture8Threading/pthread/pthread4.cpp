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
	printf("thread function %d %c \n",args->arg1,args->arg2);
	int ret=args->arg1+10;
	pthread_exit(reinterpret_cast<void *>(ret));
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

  int ret;
	for(auto &t : threadID)
	{
		printf("join\n");
		pthread_join(t,(void **)&ret);
		printf("return %d\n",ret);
	}
}