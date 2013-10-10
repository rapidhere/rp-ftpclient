all: ftpparse.so

CC=gcc
FLAG=-fpic
PY_LIB=/usr/include/python2.7/

ftpparse.so: ftpparse.o ftpparse_wrap.o
	$(CC) -o $@ $^ $(FLAG) -shared

ftpparse.o: ftpparse.c
	$(CC) -c $^ $(FLAG) -o $@

ftpparse_wrap.o: ftpparse_wrap.c ftpparse.h
	$(CC) -I$(PY_LIB) -c ftpparse_wrap.c $(FLAG) -o $@

clean:
	rm -f *.o
