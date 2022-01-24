#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>

int main(int argc, char *argv[])
{
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;
    int i;

    if (argc < 3) 
    {
        std::cerr<<"Usage: call pythonfile funcname [args]\n";
        return EXIT_FAILURE;
    }

    Py_Initialize();
    pName = PyUnicode_DecodeFSDefault(argv[1]);
    /* Error checking of pName left out */

    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (pModule != NULL) 
    {
        pFunc = PyObject_GetAttrString(pModule, argv[2]);
        /* pFunc is a new reference */

        if (pFunc && PyCallable_Check(pFunc)) 
        {
            pArgs = PyTuple_New(argc - 3);
            for (i = 0; i < argc - 3; ++i) 
            {
                pValue = PyLong_FromLong(atoi(argv[i + 3]));
                if (!pValue) 
                {
                    Py_DECREF(pArgs);
                    Py_DECREF(pModule);
                    std::cerr<<"Cannot convert argument\n";
                    return EXIT_FAILURE;
                }
                /* pValue reference stolen here: */
                PyTuple_SetItem(pArgs, i, pValue);
            }
            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);
            if (pValue != NULL) 
            {
                std::cout<<"Result of call: "<< PyLong_AsLong(pValue)<<'\n';
                Py_DECREF(pValue);
            }
            else 
            {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                PyErr_Print();
                std::cerr<<"Call failed\n";
                return EXIT_FAILURE;
            }
        }
        else 
        {
            if (PyErr_Occurred())
                PyErr_Print();
            std::cerr<<"Cannot find function "<<argv[2]<<'\n';
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else 
    {
        PyErr_Print();
        std::cerr<<"Failed to load"<<argv[1]<<'\n';
        return EXIT_FAILURE;
    }
    if (Py_FinalizeEx() < 0) 
    {

        return 120;
    }
    return EXIT_SUCCESS;
}