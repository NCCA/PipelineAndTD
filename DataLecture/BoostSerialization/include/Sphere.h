#ifndef SPHERE_H_
#define SPHERE_H_
#include <iostream>
#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/text_oarchive.hpp>

class Sphere
{
  /// @brief allow access to the serialization class
  friend class boost::serialization::access;

  public:
    /// @brief default ctor
    inline Sphere(){;}
    /// @brief user defined ctor
    /// @param _name the name of the sphere
    /// @param _x the x position
    /// @param _y the y position
    /// @param _z the z position
    /// @param _rad the radius
    Sphere(std::string _name, float _x,float _y, float _z, double _rad);
    /// @brief overload the insertion operator for printing
    /// @param _os the stream to output to
    /// @param _s the instanse of the class to output
    friend std::ostream & operator<<( std::ostream &_os,  const Sphere &_s );

  private :
    /// @brief the name of the sphere
    std::string m_name;
    /// @brief the x position
    float m_x;
    /// @brief the y position
    float m_y;
    /// @brief the z position
    float m_z;
    /// @brief the radius
    double m_radius;
    // @brief When the class Archive corresponds to an output archive, the
    // & operator is defined similar to <<.  Likewise, when the class Archive
    // is a type of input archive the & operator is defined similar to >>.
    template<class Archive>
    /// @brief the serialize method using boost::serialize
    /// @param the archive to output to

    void serialize(Archive & _ar, const unsigned int)
    {
        _ar & m_name;
        _ar & m_x;
        _ar & m_y;
        _ar & m_z;
        _ar & m_radius;
    }

};

#endif // SPHERE_H
