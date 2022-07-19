#include <stdbool.h>

typedef struct _A {
    unsigned int    a: 2;
} A;

typedef struct UNIQUE {
    unsigned int    a: 2;
} UNIQUE;

int A = 3;
extern int B;
static int C = 5;
extern int D;
static int E;

int B = 4;

struct s {
    unsigned int    b1:2;
};

int f1() {
    int g;
    float B;
}

int main() {
    int d, e, f;
    static int g;
    int C;
    return c;
}
