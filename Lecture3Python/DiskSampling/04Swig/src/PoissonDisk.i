%module PoissonDisk

%{
#define SWIG_FILE_WITH_INIT
#include "PoissonDisk.h"
%}

%include "std_vector.i"
namespace std {
    %template(VectorPoint2)  std::vector<Point2>;
}


// Include the header file with above prototypes
%include "PoissonDisk.h"
