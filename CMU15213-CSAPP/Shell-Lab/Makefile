# Makefile for the CS:APP Shell Lab

CC = gcc
CFLAGS = -Wall -O2

all: tsh

tsh: tsh.c csapp.o
	$(CC) $(CFLAGS) -o tsh tsh.c csapp.o

csapp.o: csapp.c csapp.h
	$(CC) $(CFLAGS) -c csapp.c


# clean up
clean:
	rm -f *.o
	rm -f *.out
	rm -f tsh

