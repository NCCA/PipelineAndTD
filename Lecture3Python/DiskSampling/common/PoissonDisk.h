#ifndef POSSIONDISK_H_
#define POSSIONDISK_H_

#include <vector>

struct Point2
{
  Point2(float _x, float _y) : x{_x},y{_y}{}
  Point2()=default;
  float x,y;
};

struct Index
{
    Index(int _x, int _y) : x{_x},y{_y}{}
    Index operator+(const Index &_rhs)const ;
    int x;
    int y; 
};

class PoissonDisk
{
  public :
    PoissonDisk(int _width=50, int _height=50, float _r=1.0, int _k=30, int _seed=1234);
    void reset(bool _reseed=true);
    std::vector<Point2> sample();

  private :
    Index getCellCoords(Point2 _xy);
    std::vector<int> getNeighbours(Index  _cords);
    bool pointValid(Point2 _pt);
    // return true if found and fill in o_found as the point
    bool getPoint(Point2 _pt, Point2 &o_found);
    int getIndex(Index _i);
    int m_width=50;
    int m_height=50;
    float m_r=1.0f;
    int m_k=30;
    float m_a=0.0f;
    std::vector<Point2> m_samples;    
    // cell index values, set to -1 for None
    std::vector<int> m_cells;
    // Number of cells in the x- and y-directions of the grid
    int m_nx;
    int m_ny;

};

#endif
