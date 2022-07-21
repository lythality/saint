
typedef int MY_INT;

int main() {
    int a, b, c;
    long d;

    a = 4;

    {
        int a,e;  // non-compliant
        a = 3;
    }
    return c;
}