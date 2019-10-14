#include "LampardClocks.h"

int main()
{
    char *in[3][4] = {
        {"a", "s1", "r3", "b"},
        {"c", "r2", "s3", NULL},
        {"r1", "d", "s2", "e"},
    };
    calculate(3, 4, in);

    return 0;
}