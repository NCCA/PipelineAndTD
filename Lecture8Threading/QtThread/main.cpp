#include <QApplication>
#include "MyThread.h"
int main(int argc, char **argv)
{
QApplication a(argc, argv);
MyThread t;
t.start();
MyThread v(NULL,99);
v.start();
return a.exec();
}
