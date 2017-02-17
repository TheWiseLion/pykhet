#include <Python.h>
#include <stdio.h>
#include "minmax.h"
#define PyInt_AsLong PyLong_AsLong
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

void initkhetsearch(void)
{
    Py_InitModule3("khetsearch", khetsearch_funcs, "Extension module example!");
}
