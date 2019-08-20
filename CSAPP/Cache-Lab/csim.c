/*
 * CMU 15-213 Cache-Lab
 * Simulator of a cache memory
 * Keep track of hits, misses and evictions from valgrind-generated traces
 * xu-zhang@sjtu.edu.cn
 */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>
#include <getopt.h>
#include "cachelab.h"

const char *usage_msg =
    "Usage: ./csim -s <num> -E <num> -b <num> -t <file>\n"
    "Options:\n"
    "  -s <num>:\tNumber of set index bits (S = 2^s is the number of sets)\n"
    "  -E <num>:\tAssociativity (number of lines per set)\n"
    "  -b <num>:\tNumber of block bits (B = 2^b is the block size\n"
    "  -t <file>:\tName of the valgrind trace to replay\n";

typedef struct {
    bool valid;
    unsigned tag;
} cache_head;


int main(int argc, char *argv[])
{
    int opt;
    int s, E, b;
    FILE *tf = NULL;
    while ((opt = getopt(argc, argv, "hs:E:b:t:")) != -1) {
        switch (opt) {
        case 'h':
            printf("%s", usage_msg);
            exit(EXIT_SUCCESS);            
        case 's':
            s = atoi(optarg);
            break;
        case 'E':
            E = atoi(optarg);
            break;
        case 'b':
            b = atoi(optarg);
            break;
        case 't':
            tf = fopen(optarg, "r");
            break;
        default:
            fprintf(stderr, "%s", usage_msg);
            exit(EXIT_FAILURE);
        }
    }

    /* allocate a two-dimensional array to represent 2^s sets each with E lines */
    cache_head **pool = (cache_head**)malloc((1 << s) * sizeof(cache_head*));
    for (int i = 0; i < (1 << s); i++) {
        *(pool + i) = (cache_head*)malloc(E * sizeof(cache_head));
        memset(pool[i], 0, E * sizeof(cache_head));
    }


    printf("%d\n", pool[2][2].tag);
    /* free the dynamic memory allocated */
    for (int i = 0; i < (1 << s); i++) {
        free(*(pool + i));
    }
    free(pool);

    printf("%d,%d,%d\n", s, E, b);
    fclose(tf);

    printSummary(0, 0, 0);
    return 0;
}
