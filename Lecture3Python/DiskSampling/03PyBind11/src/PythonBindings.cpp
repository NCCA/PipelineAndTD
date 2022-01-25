#include "PoissonDisk.h"
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <pybind11/cast.h>
#include <pybind11/stl_bind.h>
#include <pybind11/pytypes.h>
#include <pybind11/complex.h>

namespace py = pybind11;

PYBIND11_MAKE_OPAQUE(std::vector<Point2>);

PYBIND11_MODULE(PoissonDisk,m)
{
  m.doc()="pyngl module to use NGL in python";

  py::class_<Point2>(m,"Point2")
      .def(py::init<>())
       .def("__repr__",
        [](const Point2 &p) {
                      return "("+std::to_string(p.x)+","+
                          std::to_string(p.y)+"]";})
          .def_readwrite("x", &Point2::x)
          .def_readwrite("y", &Point2::y)
          .def("__getitem__",py::overload_cast<const size_t &>( &Point2::operator[]))

      ;
  py::class_<PoissonDisk>(m, "PoissonDisk")
      .def(py::init<int, int, float , int , int >(),
      py::arg("_width") = 50,
      py::arg("_height") = 50,
      py::arg("_r") = 1.0f,
      py::arg("_k") = 30,
      py::arg("_seed") = 1234
      )

      .def("reset",&PoissonDisk::reset)
      .def("sample",&PoissonDisk::sample)
  ;

  py::bind_vector<std::vector<Point2>>(m,"VectorPoint2")
  .def("__iter__", [](std::vector<Point2> &v) 
  {
    return py::make_iterator(std::begin(v),std::end(v));
  }, py::keep_alive<0, 1>()) /* Keep vector alive while iterator is used */
    ;

}