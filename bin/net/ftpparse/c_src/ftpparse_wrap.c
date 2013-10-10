#include <Python.h>
#include "ftpparse.h"
#include <string.h>

PyObject * ftpparse_wrap(PyObject * self, PyObject * args);

static PyMethodDef _Methods[] = {
    {"ftp_list_parse", ftpparse_wrap, METH_VARARGS, 
        "Parse the information from a single ftp  LIST line"},
    {NULL, NULL}
};

void initftpparse() {
    PyObject * m = Py_InitModule("ftpparse", _Methods);

    PyModule_AddIntMacro(m, FTPPARSE_SIZE_UNKNOWN);
    PyModule_AddIntMacro(m, FTPPARSE_SIZE_BINARY);
    PyModule_AddIntMacro(m, FTPPARSE_SIZE_ASCII);
    
    PyModule_AddIntMacro(m, FTPPARSE_MTIME_UNKNOWN);
    PyModule_AddIntMacro(m, FTPPARSE_MTIME_LOCAL);
    PyModule_AddIntMacro(m, FTPPARSE_MTIME_REMOTEMINUTE);
    PyModule_AddIntMacro(m, FTPPARSE_MTIME_REMOTEDAY);

    PyModule_AddIntMacro(m, FTPPARSE_ID_UNKNOWN);
    PyModule_AddIntMacro(m, FTPPARSE_ID_FULL);
}

/********************************************************************************/
char _buffer[2048];
PyObject * ftpparse_wrap(PyObject * self, PyObject * args) {
    char * buffer;
    if(! PyArg_ParseTuple(args,"s",&buffer))
        return NULL;
    strcpy(_buffer,buffer);

    struct ftpparse ret;
    if(ftpparse(&ret, _buffer, strlen(_buffer)) == 0)
        return NULL;

    return Py_BuildValue("(s#iiililis#)",
        ret.name, ret.namelen,          //s#
        ret.flagtrycwd,                 //i
        ret.flagtryretr,                //i
        ret.sizetype,                   //i
        ret.size,                       //l
        ret.mtimetype,                  //i
        ret.mtime,                      //l = time_t
        ret.idtype,                     //i
        ret.id, ret.idlen               //s#
    );
}
