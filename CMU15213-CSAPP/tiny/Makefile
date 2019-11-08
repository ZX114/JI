CC = gcc

CFLAGS = -O1 -m64

all: tiny

tiny: tiny.c csapp.o
	$(CC) $(CFLAGS) -o tiny tiny.c csapp.o

csapp.o: csapp.c csapp.h
	$(CC) $(CFLAGS) -c -o csapp.o csapp.c

clean:
	rm -f *.o
	rm -f *.out
	rm -f tiny

