#!/bin/csh
#
set echo
#
f90 -c -g sxyz_voronoi.f90 >& compiler.out
if ( $status != 0 ) then
  echo "Errors compiling sxyz_voronoi.f90"
  exit
endif
rm compiler.out
#
f90 sxyz_voronoi.o -L$HOME/lib/$ARCH -lstripack
if ( $status != 0 ) then
  echo "Errors linking and loading sxyz_voronoi.o"
  exit
endif
rm sxyz_voronoi.o
#
mv a.out ~/bin/$ARCH/sxyz_voronoi
#
echo "The sxyz_voronoi executable has been created."
