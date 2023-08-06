#define PY_SSIZE_T_CLEAN
#pragma once
#include <Python.h>
/*
 *************************************************
 * 
 * general basisu decompression
 * 
 ************************************************
*/

static PyObject *test(PyObject *self, PyObject *args)
{
    return NULL;
}


/*
 *************************************************
 * 
 * Python Connection
 * 
 ************************************************
*/

// Exported methods are collected in a table
static struct PyMethodDef method_table[] = {
    {"test",
     (PyCFunction)test,
     METH_VARARGS,
     ""},
 
    {NULL,
     NULL,
     0,
     NULL} // Sentinel value ending the table
};

// A struct contains the definition of a module
static PyModuleDef travis_test_module = {
    PyModuleDef_HEAD_INIT,
    "travis_test", // Module name
    "a texture decompression C++-extension for Python",
    -1, // Optional size of the module state memory
    method_table,
    NULL, // Optional slot definitions
    NULL, // Optional traversal function
    NULL, // Optional clear function
    NULL  // Optional module deallocation function
};

// The module init function
PyMODINIT_FUNC PyInit_travis_test(void)
{
    return PyModule_Create(&travis_test_module);
}