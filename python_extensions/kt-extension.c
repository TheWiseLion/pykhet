#include <Python.h>
#include <stdio.h>
#include "minmax.h"
#include "search.h"

/// Python 3 uses different api -_- ///
#if PY_MAJOR_VERSION >= 3
  #define PyIntObject                  PyLongObject
  #define PyInt_Type                   PyLong_Type
  #define PyInt_Check(op)              PyLong_Check(op)
  #define PyInt_CheckExact(op)         PyLong_CheckExact(op)
  #define PyInt_FromString             PyLong_FromString
  #define PyInt_FromUnicode            PyLong_FromUnicode
  #define PyInt_FromLong               PyLong_FromLong
  #define PyInt_FromSize_t             PyLong_FromSize_t
  #define PyInt_FromSsize_t            PyLong_FromSsize_t
  #define PyInt_AsLong                 PyLong_AsLong
  #define PyInt_AS_LONG                PyLong_AS_LONG
  #define PyInt_AsSsize_t              PyLong_AsSsize_t
  #define PyInt_AsUnsignedLongMask     PyLong_AsUnsignedLongMask
  #define PyInt_AsUnsignedLongLongMask PyLong_AsUnsignedLongLongMask
#endif
/// Only tears my friends ///



/***
*
* Color (byte), Board State (80 bytes), Min depth, # Iterations (2 bytes)
*/
static PyObject * khetsearch(PyObject* self, PyObject *args){
    PyObject *l;
    const char * board;
    int boardSize;
    int minDepth;
    int iterations;
    char color;
    int len = 0;
    int i = 0;
    struct MoveResults mr;
    struct MoveRating r;
    char actualBoard[80];
    long tmp;
    PyObject * listObj;
    if (!PyArg_ParseTuple(args, "bOii", &color, &listObj, &minDepth, &iterations)){
        return NULL;
    }


    for(i=0;i<80;i++){
        tmp = (char)PyInt_AsLong(PyList_GetItem(listObj, i));
        actualBoard[i] = tmp;
    }

    mr = getMoveRatings(color, actualBoard,minDepth,iterations);

    l = PyList_New(mr.numMoves*2);// {Move, Move Rating}

    i=0;
    while (i<mr.numMoves){
        r = mr.moves[i];
        PyList_SET_ITEM(l, i*2, PyInt_FromLong((long)r.moveValue));
        PyList_SET_ITEM(l, i*2 + 1, PyFloat_FromDouble(r.moveRating));
        i++;
    }
    free(mr.moves);
    return l;
}

static char khetsearch_docs[] =
    "Pass character array as board representation and number of iteration(int)\n";

static PyMethodDef khetsearch_funcs[] = {
    {"khetsearch", (PyCFunction)khetsearch,
     METH_VARARGS, khetsearch_docs},
    {NULL}
};


/// Python 3 different initialization -_- ///
#if PY_MAJOR_VERSION >= 3
    static struct PyModuleDef khetModule = {
       PyModuleDef_HEAD_INIT,
       "khetsearch",   /* name of module */
       khetsearch_docs, /* module documentation, may be NULL */
       -1,       /* size of per-interpreter state of the module,
                    or -1 if the module keeps state in global variables. */
       khetsearch_funcs
    };

    PyMODINIT_FUNC PyInit_khetsearch(void)
    {
        return PyModule_Create(&khetModule);
    }


#else

void initkhetsearch(void)
{
    Py_InitModule3("khetsearch", khetsearch_funcs, "Extension module example!");
}

#endif
/// Only tears my friends ///
