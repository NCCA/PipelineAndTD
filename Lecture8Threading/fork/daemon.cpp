#include <iostream>
#include <cstdlib>
#include <unistd.h>


int daemonInit()
{
// initialise the daemon using the standard fork
// for a good example see Advanced Programming
// in the UNIX Environment by Stevens
  pid_t pid;
  if ((pid = fork()) < 0)
  {
    return -1;
  }
  else if (pid != 0)
  {
    exit(EXIT_SUCCESS);
  }
	// create a new session
  setsid();

  return 0;
}

int main()
{
	daemonInit();
	while(1)
	{
		std::cout<<"ping\n";
    sleep(2);
	}
}





