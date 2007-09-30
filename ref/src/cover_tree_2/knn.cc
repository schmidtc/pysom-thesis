#include "cover_tree.h"
#include "vector.h"

// Compute the k nearest neighbors

int main(int argc, char *argv[])
{
  int k = atoi(argv[1]);
  v_array<vector> set_of_points = parse_points(argv[2]);
  v_array<vector> set_of_queries = parse_points(argv[3]);

  node<vector> top = batch_create(set_of_points);
  node<vector> top_query = batch_create(set_of_queries);
  
  v_array<v_array<vector> > res;
  k_nearest_neighbor(top,top_query,res,k);
  
  printf("Printing results\n");
  for (int i = 0; i < res.index; i++)
    {
      for (int j = 0; j<res[i].index; j++)
	print(res[i][j]);
      printf("\n");
    }
    printf("results printed\n");
}
