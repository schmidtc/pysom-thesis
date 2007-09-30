#!/bin/csh
#
echo "Split the file."
#
mkdir temp
cd temp
rm *
f90split ../stripack.f90
#
echo "Compile the routines."
#
foreach FILE (`ls -1 *.f90`)
  f90 -c $FILE >& compiler.out
  if ( $status != 0 ) then
   echo "Errors while compiling " $FILE
    exit
  endif
  rm compiler.out
end
rm *.f90
#
echo "Create the archive."
ar qc libstripack.a *.o
rm *.o
#
echo "Store the archive."
mv libstripack.a ~/lib/$ARCH
if ( $status != 0 ) then
  exit
endif
cd ..
rmdir temp
#
echo "A new version of stripack has been created."
