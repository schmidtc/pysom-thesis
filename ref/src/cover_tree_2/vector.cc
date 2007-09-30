#include "vector.h"
#include<stdio.h>
#include<math.h>
#include <string.h>

const int batch = 120;//must be a multiple of 8

int point_len = 0;

//Assumption: points are a multiples of 8 long
float distance(vector p1, vector p2, float upper_bound)
{
  float sum = 0.;
  float *end = p1 + point_len;
  upper_bound *= upper_bound;
  for (float *batch_end = p1 + batch; batch_end <= end; batch_end += batch)
    {
      for (; p1 != batch_end; p1+=2, p2+=2)
	{
	  float d1 = *p1 - *p2;
	  float d2 = *(p1+1) - *(p2+1);
	  d1 *= d1;
	  d2 *= d2;
	  sum = sum + d1 + d2;
	}
      if (sum > upper_bound)
	return sqrt(sum);
    }
  for (; p1 != end; p1+=2, p2+=2)
	{
	  float d1 = *p1 - *p2;
	  float d2 = *(p1+1) - *(p2+1);
	  d1 *= d1;
	  d2 *= d2;
	  sum = sum + d1 + d2;
	}
  return sqrt(sum);
}

v_array<vector> parse_points(char *filename)
{
  FILE *input = fopen(filename,"r");
  v_array<vector > parsed;
  char c;
  v_array<float> p;

  while ( (c = getc(input)) != EOF )
    {
      ungetc(c,input);
      
      while ((c = getc(input)) != '\n' )
	{
	  while (c != '0' && c != '1' && c != '2' && c != '3' 
		 && c != '4' && c != '5' && c != '6' && c != '7' 
		 && c != '8' && c != '9' && c != '\n' && c != EOF && c != '-')
	    c = getc(input);
	  if (c != '\n' && c != EOF) {
	    ungetc(c,input);
	    float f;
	    fscanf(input, "%f",&f);
	    push(p,f);
	  }
	  else 
	    if (c == '\n') 
	      ungetc(c,input);
	}

      if (p.index %8 > 0)
	for (int i = 8 - p.index %8; i> 0; i--)
	  push(p,(float) 0.);
      float *new_p;
      posix_memalign((void **)&new_p, 16, p.index*sizeof(float));

      memcpy(new_p,p.elements,sizeof(float)*p.index);

      if (point_len > 0 && point_len != p.index)
	{
	  printf("Can't handle vectors of differing length, bailing\n");
	  exit(0);
	}      

      point_len = p.index;
      p.index = 0;
      push(parsed,new_p);
      
      // If the index of the first point is F, then 
      // &(parsed[parsed.index-1])-&(parsed[0])  is the index of the current point
    }
  return parsed;
}

void print(vector &p)
{
  for (int i = 0; i<point_len; i++)
    printf("%f ",p[i]);
  printf("\n");
}
