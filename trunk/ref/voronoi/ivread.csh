#!/bin/csh
#
set echo
#
f90 -c ivread.f90 >& compiler.out
if ( $status != 0 ) then
  echo "Errors compiling ivread.f90"
  exit
endif
rm compiler.out
#
f90 ivread.o
if ( $status != 0 ) then
  echo "Errors linking and loading ivread.o"
  exit
endif
#
rm ivread.o
#
chmod ugo+x a.out
mv a.out ~/bin/$ARCH/ivread
#
echo "A new version of ivread has been created."
