#include "csapp.h"

/*
 * unix_error - unix-style error routine
 */
void unix_error(char* msg)
{
    fprintf(stderr, "%s: %s\n", msg, strerror(errno));
    exit(0);
}

pid_t Fork(void)
{
    pid_t pid;

    if ((pid = fork()) < 0)
        unix_error("Fork error");
    return pid;
}

unsigned int snooze(unsigned int secs)
{
    unsigned int t = sleep(secs);
    fprintf(stdout, "Slept for %d of %d secs\n", secs - t, secs);
    return t;
}

/*
 * Signal - wrapper for the sigaction function
 */
handler_t *Signal(int signum, handler_t *handler) 
{
    struct sigaction action, old_action;

    action.sa_handler = handler;  
    sigemptyset(&action.sa_mask); /* block sigs of type being handled */
    action.sa_flags = SA_RESTART; /* restart syscalls if possible */

    if (sigaction(signum, &action, &old_action) < 0)
        unix_error("Signal error");
    return (old_action.sa_handler);
}

static size_t sio_strlen(char s[])
{
    int i = 0;

    while (s[i] != '\0')
        ++i;
    return i;
}

ssize_t sio_puts(char s[])
{
    return write(STDOUT_FILENO, s, sio_strlen(s));
}

void sio_error(char s[])
{
    sio_puts(s);
    _exit(1);
}
