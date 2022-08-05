#include <stdbool.h>

typedef struct _A {
    unsigned int    a: 2;
} A;

struct _B {
    signed int    a: 2;
};

struct _B {
    unsigned int    a: 2;
};

typedef enum _C {
    sunday=1, monday, tuesday, wednesday=3, thursday, friday, saturday
} C;

enum _D {
    ONE, TWO, THREE=3, FOUR, FIVE, SIX, SAME_THREE=3
};

enum _E {
    sunday=77, monday, tuesday, wednesday, thursday, friday, saturday
};

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
    struct _A {
        unsigned int    a: 2;
        unsigned int    b: 2;
        unsigned int    c: 2;
    }

    struct _A decl1;
    union _A decl2;
}

int main() {
    int d, e, f;
    static int g;
    int C;
    return c;
}
