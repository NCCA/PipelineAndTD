#include "Sphere.h"


Sphere::Sphere() :  m_name(_name),
                    m_x(_x),
                    m_y(_y),
                    m_z(_z),
                    m_radius(_rad)
                    {;}


std::ostream & operator<<(std::ostream &_os, const Sphere &_s )
{
  return _os<<"Sphere "<<_s.m_name<<'\n'
         <<"Position "<<_s.m_x<<" "<<_s.m_y<<' '
         <<_s.m_z<<'\n'
         <<"Radius "<<_s.m_radius<<'\n';
}

