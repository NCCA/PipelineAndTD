#include "MyThread.h"
#include <QDebug>

MyThread::MyThread(QObject *parent, int _v) :
  QThread(parent)
{
  data=_v;
}


void MyThread::run()
{
  while(1)
  {
    data++;
    qDebug()<<"running thread "<<data;
    sleep(2);
  }
}
