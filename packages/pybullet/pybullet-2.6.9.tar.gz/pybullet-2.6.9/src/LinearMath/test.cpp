#include <stdio.h>
#include <math.h>
#include <float.h>

int main(int argc, char* argv[])
{
  float d = DBL_EPSILON;
  while (1)
{
d/=2.0;
printf("d=%.64f\n", d);
  float s = sqrt(d);
printf("s=%.64f\n", s);
float t = 1.0 / s;
printf("t = %.64f\n", t);
}
}
