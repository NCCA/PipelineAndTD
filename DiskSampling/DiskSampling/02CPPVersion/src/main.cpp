#include "PoissonDisk.h"
#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>

#include "cxxopts.h"
int main(int argc, char **argv)
{
  cxxopts::Options options("Poisson", "simple PoissonDisk sample demo");
options.add_options()
  ("w,width", "width of sim", cxxopts::value<int>()->default_value("50"))
  ("h,height", "height of sim", cxxopts::value<int>()->default_value("50"))
  ("r,radius", "radius", cxxopts::value<float>()->default_value("1.0"))
  ("k,simcount", "iterations for k", cxxopts::value<int>()->default_value("30"))
   ("s,seed", "seed", cxxopts::value<int>()->default_value("1234"))
   ;
  auto result = options.parse(argc, argv);
  auto width = result["width"].as<int>();
  auto height = result["height"].as<int>();
  auto r = result["radius"].as<float>();
  auto k = result["simcount"].as<int>();
  auto seed = result["seed"].as<int>();

  auto begin = std::chrono::steady_clock::now();
  auto scatter = PoissonDisk(width, height, r,k,seed);
  auto end = std::chrono::steady_clock::now();
  std::cout << "Construction took " << std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count() << "[ms]\n";
  begin = std::chrono::steady_clock::now();
  auto points=scatter.sample();
  end = std::chrono::steady_clock::now();
  std::cout << "sample took " << std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count() << "[ms]\n";
  std::cout<<"Number of Points "<<points.size()<<'\n';
std::ofstream fileOut;
fileOut.open("scatter.py");
fileOut<<"#!/usr/bin/env python\n";
fileOut<<"import matplotlib.pyplot as plt\n";
fileOut<<"points=[\n";
for(auto p : points)
{
  fileOut<<"("<<p.x<<','<<p.y<<"),\n";
}
fileOut<<"]\n";
fileOut<<"plt.title(\"Poisson disk sampling\")\n";
fileOut<<"plt.scatter(*zip(*points),s="<<r<<") \n";
fileOut<<"plt.show() \n";
fileOut.close();

}