#include "LampardClocks.h"

int main()
{
    char *in[3][4] = {
        {"1", "2", "8", "9"},
        {"1", "6", "7", "0"},
        {"3", "4", "5", "6"},
    };
    verify(3, 4, in);

    return 0;
}