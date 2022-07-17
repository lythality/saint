#include <stdbool.h>

typedef struct _A {
    int             a: 1;
    signed int      b: 2;
    unsigned int    c: 3;
    bool            d: 1;
} A;

typedef unsigned int UINT_16;
typedef UINT_16 DEEP_UINT_16;

struct s {
    unsigned int    b1:2;
    int             b2:2;
    UINT_16         b3:2;
    signed long     b4:2;
    DEEP_UINT_16    b5:2;
};

int main() {
    return c;
}