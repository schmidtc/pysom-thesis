CFLAGS=-O3 -ffast-math -funroll-loops -static # -msse -march=athlon 

all:	test_nn knn

vector.o: vector.cc vector.h
	g++ -c -Wall $(CFLAGS) vector.cc

sparse_vector.o: sparse_vector.cc sparse_vector.h
	g++ -c -Wall $(CFLAGS) sparse_vector.cc

test_nn:	vector.o stack.h cover_tree.h vector.h test_nn.cc
	g++ -Wall $(CFLAGS) -o test_nn test_nn.cc vector.o 

knn:	vector.o sparse_vector.o stack.h sparse_vector.h vector.h cover_tree.h knn.cc
	g++ -Wall $(CFLAGS) -o knn knn.cc vector.o 

clean:
	rm *.o
