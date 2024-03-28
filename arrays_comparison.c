#include <stdio.h>

int main()
{
	// declaring array
	int arr[5];

	// declaring pointer to array name
	int *p = &arr;
	// declaring pointer to first element
	int* q = &arr[0];

	if (p == q) {
		printf("Pointer to Array Name and First Element "
			"are Equal.");
	}
	else {
		printf("Pointer to Array Name and First Element "
			"are not Equal.");
	}

	return 0;
}
