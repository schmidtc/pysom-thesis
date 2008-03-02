#!/bin/csh
#
set echo
#
f90 -c f90split.f90 >& compiler.out
if ( $status != 0 ) then
  echo "Errors compiling f90split.f90"
  exit
endif
rm compiler.out
#
f90 f90split.o
if ( $status != 0 ) then
  echo "Errors linking and loading f90split.o"
  exit
endif
rm f90split.o
#
chmod ugo+x a.out
mv a.out ~/bin/f90split
#
echo "A new version of f90split has been created."
