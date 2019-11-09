CC = gcc

CFLAGS = -Wall -O1 -m64

all: ec es

ec: echoclient.c csapp.o
	$(CC) $(CFLAGS) -o echoclient echoclient.c csapp.o

es: echoserveri.c csapp.o echo.o
	$(CC) $(CFLAGS) -o echoserveri echoserveri.c csapp.o echo.o

echo.o: echo.c csapp.h
	$(CC) $(CFLAGS) -c -o echo.o echo.c

csapp.o: csapp.c csapp.h
	$(CC) $(CFLAGS) -c -o csapp.o csapp.c


clean:
	rm -f *.o
	rm -f *.out
	rm -f echoclient
	rm -r echoserveri

