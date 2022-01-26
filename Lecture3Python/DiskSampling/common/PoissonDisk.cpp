#include "PoissonDisk.h"
#include <random>
#include <cmath>
#include <limits>
#include <array>
#include <iostream>
#include <algorithm>

std::random_device g_rd;
std::seed_seq g_seed{g_rd(), g_rd(), g_rd(), g_rd(), g_rd(), g_rd(), g_rd(), g_rd()};

std::mt19937 g_generator(g_seed);



Index Index::operator+(const Index &_rhs)const 
{
  return Index(x+_rhs.x,y+_rhs.y);
}

int PoissonDisk::getIndex(Index _i)
{
  return (m_nx*_i.y)+_i.x;
}


PoissonDisk::PoissonDisk(int _width, int _height, float _r, int _k, int _seed)
{

  m_width=_width;
  m_height=_height;
  m_r=_r;
  m_k=_k;
  m_a= m_r/sqrtf(2.0f);
  m_nx=int(m_width/m_a)+1;
  m_ny=int(m_height / m_a) + 1;
  g_generator.seed(time(nullptr)); 
  reset();

}


void PoissonDisk::reset(bool _reseed)
{
  m_cells.resize(m_nx*m_ny);
  for(auto &c : m_cells)
    c=-1; 
}
std::vector<Point2> PoissonDisk::sample()
{
  // """Poisson disc random sampling in 2D.
  // Draw random samples on the domain width x height such that no two
  // samples are closer than r apart. The parameter k determines the
  // maximum number of candidate points to be chosen around each reference
  // point before removing it from the "active" list.
  // """

  ///# Pick a random point to start with.
  auto wDist=std::uniform_real_distribution<float>(0.0f,m_width);
  auto hDist=std::uniform_real_distribution<float>(0.0f,m_height);

  Point2 pt {wDist(g_generator),hDist(g_generator)};
  m_samples.push_back(pt);
  // Our first sample is indexed at 0 in the samples list...
  auto cell=getCellCoords(pt);
  m_cells[getIndex(cell)] = 0;
  // and it is active, in the sense that we're going to look for more
  // points in its neighborhood.
  std::vector<int>active={0};
  //# As long as there are points in the active list, keep looking for
  //# samples.
  while( !active.empty())
  {
      // choose a random "reference" point from the active list.
      auto choice=std::uniform_int_distribution<>(0,active.size()-1);
      size_t index=choice(g_generator);
      int idx = active[index];
      Point2 refpt = m_samples[idx];
      //# Try to pick a new point relative to the reference point.
      Point2 pt;
      bool found = getPoint(refpt,pt);
      if (found)
      {
        //# Point pt is valid: add it to samples list and mark as active
        m_samples.push_back(pt);
        auto nsamples =m_samples.size() - 1;
        active.push_back(nsamples);
        auto c=getCellCoords(pt);
        m_cells[getIndex(c)] = nsamples;
      }
      else
      {
        // remove it from the list of "active" points.
      active.erase(std::remove(active.begin(), active.end(), idx), active.end());
  
      }
  }

  return m_samples;
}

Index PoissonDisk::getCellCoords(Point2 _xy)
{
  // Get the coordinates of the cell that pt = (x,y) falls in.
  int x=floor(_xy.x/m_a);
  int y=floor(_xy.y/m_a);
  return Index(x,y);
}

std::vector<int> PoissonDisk::getNeighbours(Index _cords)
{
  
static  std::array<Index,21> dxdy = { Index(-1,-2),Index(0,-2),Index(1,-2),Index(-2,-1),
    Index(-1,-1),Index(0,-1),Index(1,-1),Index(2,-1),Index(-2,0),Index(-1,0),Index(1,0),Index(2,0),Index(-2,1),Index(-1,1),Index(0,1),Index(1,1),Index(2,1),Index(-1,2),Index(0,2),Index(1,2),Index(0,0)
  };
std::vector<int> neighbours;
for (auto i : dxdy)
{
  Index current=_cords+i;
  //std::cout<<"dxdy "<<i.x<<' '<<i.y<<'\n';
//  if not (0 <= neighbour_coords[0] < self.nx and
//                    0 <= neighbour_coords[1] < self.ny)
  if( !((current.x >= 0) && (current.x < m_nx) && (current.y >= 0) && (current.y < m_ny)))
  //if( !( ( current.x<=0 || current.x < m_nx) && (current.y<=0 || current.y <m_ny)))  
  {
    // off grid skip
    continue;
  }
  int cell=m_cells[getIndex(current)];
  if( cell >=0)
  {
    //std::cout<<"Index values "<<getIndex(current)<<' '<<current.x<<' '<<current.x<<" nx ny "<<m_nx<<' '<<m_ny<<'\n';
    //std::cout<<"Cell value being added "<<cell<<'\n';
    neighbours.push_back(cell);
  }
}
//std::cout<<"found ne "<<neighbours.size()<<'\n';
return neighbours;

}

bool PoissonDisk::pointValid(Point2 _pt)
{
/*
 """Is pt a valid point to emit as a sample?
        It must be no closer than r from any other point: check the cells in
        its immediate neighbourhood.
        """
*/
  auto cell_coords = getCellCoords(_pt);
  auto neighbourhood=getNeighbours(cell_coords);
  for(auto idx : neighbourhood)
  {
      auto nearby_pt = m_samples[idx];
      //  Squared distance between candidate point, pt, and this nearby_pt.
      auto distance2 = ((nearby_pt.x-_pt.x)*(nearby_pt.x-_pt.x)) + ((nearby_pt.y-_pt.y)*(nearby_pt.y-_pt.y));
      if (distance2 < m_r*m_r)
      {
      //  # The points are too close, so pt is not a candidate.
        return false;
      }
  }
  return true;
}
bool PoissonDisk::getPoint(Point2 _pt, Point2 &o_found)
{
 /*   """Try to find a candidate point near refpt to emit in the sample.
        We draw up to k points from the annulus of inner radius r, outer radius
        2r around the reference point, refpt. If none of them are suitable
        (because they're too close to existing points in the sample), return
        False. Otherwise, return the pt.
        """
*/
  int i = 0;
  auto rhoDist=std::uniform_real_distribution<float>(m_r,2.0f*m_r);
  auto thetaDist=std::uniform_real_distribution<float>(0.0f,2.0f*M_PI);

  while (i < m_k)
  {
    float rho = rhoDist(g_generator);
    float theta =thetaDist(g_generator); 
    float ptX = _pt.x + rho*cosf(theta);
    float ptY =  _pt.y + rho*sinf(theta);
    if( (ptX <=0 || ptX >m_width) || (ptY<=0 || ptY >m_height))
    {
      //# This point falls outside the domain, so try again.
      continue;
    }
    if (pointValid({ptX,ptY}))
    {
      o_found.x=ptX;
      o_found.y=ptY;
      return true;
    }
    ++i;
  }
  //# We failed to find a suitable point in the vicinity of refpt.
  return false;
}
