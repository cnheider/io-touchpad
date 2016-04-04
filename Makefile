CC=gcc
CFLAGS=-c -fPIC
LDFLAGS=-shared

all: lib/touchpadlib.so

lib/touchpadlib.so: touchpadlib.o
	mkdir lib
	$(CC) $(LDFLAGS) -Wl,-soname,touchpadlib.so -o lib/touchpadlib.so touchpadlib.o

touchpadlib.o: touchpadlib/touchpadlib.c touchpadlib/touchpadlib.h
	$(CC) $(CFLAGS) -o touchpadlib.o touchpadlib/touchpadlib.c

clean:
	-@rm -f *.o lib/touchpadlib.so 2>/dev/null || true
	-@rmdir lib 2>/dev/null || true
