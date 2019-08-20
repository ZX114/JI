/*
 * CMU 15-213 Cache-Lab
 * Simulator of a cache memory
 * Keep track of hits, misses and evictions from valgrind-generated traces
 * xu-zhang@sjtu.edu.cn
 */
#include <stdio.h>
#include <string.h>
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

typedef unsigned long ADDR_TYPE;  /* 64-bit address */

struct {
    int s;
    int E;
    int b;
} args = {-1, -1, -1};

typedef struct {
    int timestamp;
    ADDR_TYPE tag;
} Cache_head;

struct {
    int hit;
    int miss;
    int eviction;
} res = {0, 0, 0};

/*
 * visit the cache memory and record the timestamp for the use of
 * LRU (least-recently-used) replacement policy
 */
void visit_cache(ADDR_TYPE address, Cache_head **pool) {
    static int time = 0;
    /* determine the tag and set in this address */
    int taglen = sizeof(address)*8 - args.s - args.b;
    ADDR_TYPE tag = address  >> (args.s + args.b);
    int set = (address << taglen) >> (taglen + args.b);

    int minIdx = 0;
    for (int i = 0; i < args.E; i++) {
        if (pool[set][i].timestamp != 0 && pool[set][i].tag == tag) {
            pool[set][i].timestamp = ++time;
            res.hit++;
            return;
        } else if (pool[set][i].timestamp == 0) {
            pool[set][i].timestamp = ++time;
            pool[set][i].tag = tag;
            res.miss++;
            return;
        } else { /* timestamp != 0 && tag does not match */
            if (pool[set][i].timestamp < pool[set][minIdx].timestamp) {
                minIdx = i;
            }
        }
    }

    pool[set][minIdx].timestamp = ++time;
    pool[set][minIdx].tag = tag;
    res.miss++;
    res.eviction++;
}

int main(int argc, char *argv[])
{
    int opt;
    FILE *tf = NULL;
    while ((opt = getopt(argc, argv, "hs:E:b:t:")) != -1) {
        switch (opt) {
        case 'h':
            printf("%s", usage_msg);
            exit(EXIT_SUCCESS);            
        case 's':
            args.s = atoi(optarg);
            break;
        case 'E':
            args.E = atoi(optarg);
            break;
        case 'b':
            args.b = atoi(optarg);
            break;
        case 't':
            tf = fopen(optarg, "r");
            break;
        default:
            fprintf(stderr, "%s", usage_msg);
            exit(EXIT_FAILURE);
        }
    }

    /* allocate a two-dimensional array
     * to represent 2^s sets each with E lines */
    Cache_head **pool =
        (Cache_head**)malloc((1 << args.s) * sizeof(Cache_head*));
    for (int i = 0; i < (1 << args.s); i++) {
        *(pool + i) = (Cache_head*)malloc(args.E * sizeof(Cache_head));
        memset(pool[i], 0, args.E * sizeof(Cache_head));
    }

    /* read the tracefile */
    char id;
    ADDR_TYPE address;
    int size;
    while (fscanf(tf, " %c %lx,%d", &id, &address, &size) > 0) {
        switch (id) {
        case 'I': /* an instruction load */
            break;
        case 'L': /* a data load */
            visit_cache(address, pool);
            break;
        case 'S': /* a data store */
            visit_cache(address, pool);
            break;
        case 'M': /* a data modify */
            visit_cache(address, pool);
            res.hit++;
            break;
        }
    }

    /* free the dynamic memory allocated */
    for (int i = 0; i < (1 << args.s); i++) {
        free(*(pool + i));
    }
    free(pool);

    fclose(tf);

    printSummary(res.hit, res.miss, res.eviction);
    return 0;
}
