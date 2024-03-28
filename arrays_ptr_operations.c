#include<stdio.h>

int main()
{
    int  a = 10; 
    int  *p = &a;
    printf("Value of ptr 'a' is %u\n", p);

    int  b = 10; 
    int  *q = &b;
    printf("Value of ptr 'b' is %u\n", q);

    int c = (*p) * (*q);
    int *r = &c;
    printf("Value of ptr 'c' is %u\n", r);
    return 0;
}