#ifndef CSAPP_H
#define CSAPP_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <signal.h>
#include <errno.h>

void unix_error(char* msg);

/* Process control wrappers */
pid_t Fork(void);

unsigned int snooze(unsigned int);

typedef void handler_t(int);
handler_t* Signal(int, handler_t*);

/* sio (signal-safe IO) */
ssize_t sio_puts(char s[]);
void sio_error(char s[]);

#endif  // CSAPP_H
