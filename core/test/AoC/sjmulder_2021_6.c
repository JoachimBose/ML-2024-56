#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <inttypes.h>

int
main()
{
	uint64_t ages[9]={0}, p1=0,p2=0;
	int age,day,i;

	while (scanf("%d,", &age) == 1)
		ages[age]++;

	for (day=0; day<80; day++)
		ages[(day+7)%9] += ages[day%9];
	for (i=0; i<9; i++)
		p1 += ages[i];
	for (; day<256; day++)
		ages[(day+7)%9] += ages[day%9];
	for (i=0; i<9; i++)
		p2 += ages[i];

	printf("06: %" PRIu64 " %" PRIu64 "\n", p1, p2);
	return 0;
}
