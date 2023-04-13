#include "Sphere.h"

std::ostream & operator<<(
                          std::ostream &_os,
                          const Sphere &_s
                         )
{

  return _os<<"Sphere "<<_s.m_name<<std::endl
         <<"Position "<<_s.m_x<<" "<<_s.m_y<<" "
         <<_s.m_z<<std::endl
         <<"Radius "<<_s.m_radius<<std::endl;
}

