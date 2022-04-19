#ifndef MYTHREAD_H
#define MYTHREAD_H

#include <QtCore/QThread>

class MyThread : public QThread
{
  Q_OBJECT
public:
  explicit MyThread(QObject *parent = 0,int _v=0);

protected :
  void run();
  int data;
  
signals:
  
public slots:
  
};

#endif // MYTHREAD_H
