#ifndef SPARSE_VECTOR_H
#define SPARSE_VECTOR_H

/* Created by Omid Madani */

#include "stack.h"

struct single_node
{
  int index;
  double value;

  // omid has added these so he can use quicksorting
  // sorting is designed to be done based on the index..
  // in increasing order of index..
  int operator<( const single_node & b)
  {
    return index < b.index;
  }
  int operator>( const single_node & b)
  {
    return index > b.index;
  }
  int operator==( const single_node & b)
  {
    return index == b.index;
  }
};

typedef single_node* sparse_vector;

float complete_distance(sparse_vector v1, sparse_vector v2);

float distance(sparse_vector v1, sparse_vector v2, float upper_bound);

v_array<sparse_vector > parse_points(char *input);

void print(const sparse_vector & p);

#endif
