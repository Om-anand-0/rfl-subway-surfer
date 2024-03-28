#include<stdio.h>

int main()
{
    int a;
    printf("enter the no : \n");
    scanf("%d", &a);
    if(a % 97 == 0){
    printf("\nthe number is divisible by 97\n");
    }
    else{
    printf("\nthe number is not divisible by 97\n");
    }
    return 0;
}