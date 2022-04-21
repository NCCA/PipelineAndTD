#include <iostream>
#include <cstdlib>
#include <pthread.h>
#include <array>

struct argStruct
{
	int arg1;
	char arg2;
};


void *threadFunc(void *arg)
{
	struct argStruct *args = (argStruct *)arg;
/*	std::cout<<"thread func \n";
	std::cout<<"Arg 1 "<<args->arg1<<'\n';
	std::cout<<"Arg 2 "<<args->arg2<<'\n';
	*/
	printf("thread function %d %c \n",args->arg1,args->arg2);
	return 0;
}


int main()
{
	std::array<pthread_t,14> threadID;
	struct argStruct args;

	for(int i=0; i<14; ++i)
	{
		args.arg1=i;
		args.arg2='a'+i;
		pthread_create(&threadID[i],0,threadFunc,(void *)&args);
	}
	// now join

	for(auto &t : threadID)
	{
		pthread_join(t,0);
	}
}