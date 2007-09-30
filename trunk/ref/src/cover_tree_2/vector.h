#ifndef VECTOR_H
#define VECTOR_H

/* First written by John Langford jl@hunch.net
   Templatization by Dinoj Surendran dinojs@gmail.com
*/

#include "stack.h"

typedef float* vector;

float distance(vector v1, vector v2, float upper_bound);
v_array<vector > parse_points(char *filename);
void print(vector &p);

#endif
