#include <cstdlib>
#include <iostream>
#include <unistd.h>


void error()
{
	std::cout<<"Error \n";
}

void child()
{
	std::cout<<"In child\n";
}

void parent()
{
	std::cout<<"In Parent\n";
}

int main()
{

std::cout<<"Started main about to fork\n";

pid_t pid = fork();

switch (pid)
{
  case -1:
    /* an error occurred, i.e. no child process created */
    error();
  case 0:
    /* a return value of 0 means we're in the child process */
    child();
    break;  // or _exit()
  default:
    /* we're in the parent; pid is the child's process id */
    parent();
}


	std::cout<<"Exit program pid is "<<pid<<"\n";

	return EXIT_SUCCESS;
}