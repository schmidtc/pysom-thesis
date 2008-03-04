program main

!*******************************************************************************
!
!! MAIN is the main program for SXY_VORONOI.
!
!  Discussion:
!
!    SXYZ_VORONOI determines the Voronoi diagram of points on the sphere in 3D.
!
!    The user supplies an XYZ file containing points on the unit sphere.
!    This routine reads that file and calls the appropriate STRIPACK
!    routines to compute and plot the Delaunay triangulation and the
!    Voronoi diagram.  These plots are stored as PostScript files.
!
!  Modified:
!
!    14 June 2002
!
!  Author:
!
!    John Burkardt
!
  implicit none

  integer arg_num
  integer iarg
  integer iargc
  integer :: ierror = 0
  integer ilen
  integer ios
  integer ipxfargc
  integer lens
  character ( len = 256 ) :: xyz_file_name = ' '

  call timestamp ( )

  write ( *, '(a)' ) ' '
  write ( *, '(a)' ) 'SXYZ_VORONOI'
  write ( *, '(a)' ) '  Given a set of XYZ points on the sphere,'
  write ( *, '(a)' ) '  compute the Voronoi diagram.'
!
!  Get the number of command line arguments.
!
!  Old style:
!
  arg_num = iargc ( )
!
!  New style:
!
! arg_num = ipxfargc ( )
!
!  If at least one command line argument, it's the input file name.
!
  if ( arg_num < 1 ) then

    write ( *, '(a)' ) ' '
    write ( *, '(a)' ) 'Enter the input XYZ file name:'
    read ( *, '(a)', iostat = ios ) xyz_file_name

    if ( ios /= 0 ) then
      write ( *, '(a)' ) ' '
      write ( *, '(a)' ) 'SXYZ_VORONOI - Fatal error!'
      write ( *, '(a)' ) '  Unexpected read error!'
      stop
    end if

  else

    iarg = 1
!
!  Old style:
!
    call getarg ( iarg, xyz_file_name )
!
!  New style:
!
!   call pxfgetarg ( iarg, xyz_file_name, ilen, ierror )
!
!   if ( ierror /= 0 ) then
!     write ( *, '(a)' ) ' '
!     write ( *, '(a)' ) 'SXYZ_VORONOI - Fatal error!'
!     write ( *, '(a)' ) '  Could not read command line argument.'
!     stop
!   end if

  end if

  call stripack_interface ( xyz_file_name )

  write ( *, '(a)' ) ' '
  write ( *, '(a)' ) 'SXYZ_VORONOI'
  write ( *, '(a)' ) '  Normal end of execution.'

  write ( *, '(a)' ) ' '
  call timestamp ( )

  stop
end
subroutine stripack_interface ( xyz_file_name )

!*******************************************************************************
!
!! STRIPACK_INTERFACE calls STRIPACK routines.
!
!  Discussion:
!
!    10 June 2002: Changed this routine so that it can handle any size
!    problem, by making all arrays allocatable.
!
!  Modified:
!
!    10 June 2002
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Input, character ( len = * ) XYZ_FILE_NAME, the name of the input file.
!
  implicit none

  real ( kind = 8 ) a
  real ( kind = 8 ), allocatable, dimension ( : ) :: ds
  real ( kind = 8 ) elat
  real ( kind = 8 ) elon
  integer i
  integer ierror
  integer iunit
  integer, allocatable, dimension ( : ) :: iwk
  integer k
  integer kt
  integer, allocatable, dimension ( :, : ) :: lbtri
  integer, allocatable, dimension ( : ) :: lend
  integer, allocatable, dimension ( : ) :: list
  integer, allocatable, dimension ( : ) :: listc
  integer lnew
  integer lp
  integer lpl
  integer, allocatable, dimension ( : ) :: lptr
  integer, allocatable, dimension ( :, : ) :: ltri
  integer n
  integer na
  integer nb
  integer nn
  real ( kind = 8 ) norm
  integer nt
  integer ntemp
  logical numbr
  integer nv
  real ( kind = 8 ), parameter :: pltsiz = 7.5D+00
  real ( kind = 8 ), allocatable, dimension ( : ) :: rc
  character ( len = 80 ) trplot_file_name
  character ( len = 80 ) trplot_title
  real ( kind = 8 ) vlat
  real ( kind = 8 ) vlon
  character ( len = 80 ) vrplot_file_name
  character ( len = 80 ) vrplot_title
  real ( kind = 8 ), allocatable, dimension ( : ) :: x
  real ( kind = 8 ), allocatable, dimension ( : ) :: xc
  character ( len = * ) xyz_file_name
  real ( kind = 8 ), allocatable, dimension ( : ) :: y
  real ( kind = 8 ), allocatable, dimension ( : ) :: yc
  real ( kind = 8 ), allocatable, dimension ( : ) :: z
  real ( kind = 8 ), allocatable, dimension ( : ) :: zc
!
!  Count the number of lines of (X,Y,Z) data.
!
  call file_row_count ( xyz_file_name, n )

  if ( n <= 0 ) then
    write ( *, '(a)' ) ' '
    write ( *, '(a)' ) 'STRIPACK_INTERFACE - Fatal error!'
    write ( *, '(a)' ) '  The input file has no data.'
    return
  end if
!
!  Allocate everything.
!
  allocate ( ds(1:n) )
  allocate ( iwk(1:2*n) )
  allocate ( lbtri(1:6,1:n) )
  allocate ( lend(1:n) )
  allocate ( list(1:6*(n-2)) )
  allocate ( listc(1:6*(n-2)) )
  allocate ( lptr(1:6*(n-2)) )
  allocate ( ltri(1:9,1:2*(n-2)) )
  allocate ( rc(1:2*(n-2)) )
  allocate ( x(1:n) )
  allocate ( xc(1:2*(n-2)) )
  allocate ( y(1:n) )
  allocate ( yc(1:2*(n-2)) )
  allocate ( z(1:n) )
  allocate ( zc(1:2*(n-2)) )
!
!  Read the (X,Y,Z) data from a file.
!
  call xyz_read ( xyz_file_name, n, x, y, z, ierror )
!
!  Make sure the data is on the unit sphere.
!
  do i = 1, n
    norm = sqrt ( x(i)**2 + y(i)**2 + z(i)**2 )
    x(i) = x(i) / norm
    y(i) = y(i) / norm
    z(i) = z(i) / norm
  end do
!
!  Create the triangulation.
!
  call trmesh ( n, x, y, z, list, lptr, lend, lnew, iwk, iwk(n+1), ds, ierror )

  if ( ierror == -2 ) then
    write ( *, '(a)' ) ' '
    write ( *, '(a)' ) 'STRIPACK_INTERFACE - Fatal error!'
    write ( *, '(a)' ) '  Error in TRMESH.'
    write ( *, '(a)' ) '  The first 3 nodes are collinear.'
    stop
  end if

  if ( 0 < ierror ) then
    write ( *, '(a)' ) ' '
    write ( *, '(a)' ) 'STRIPACK_INTERFACE - Fatal error!'
    write ( *, '(a)' ) '  Error in TRMESH.'
    write ( *, '(a)' ) '  Duplicate nodes encountered.'
    stop
  end if
!
!  Create a triangle list.
!
  call trlist ( n, list, lptr, lend, 9, nt, ltri, ierror )

  if ( ierror /= 0 ) then
    write ( *, '(a)' ) ' '
    write ( *, '(a)' ) 'STRIPACK_INTERFACE - Fatal error!'
    write ( *, '(a)' ) '  Error in TRLIST.'
    stop
  end if
!
!  Plot the portion of the triangulation contained 
!  in the hemisphere centered at E = (ELAT,ELON), where ELAT and ELON
!  are taken to be the center of the range of
!  the nodal latitudes and longitudes.
!
  elat = 50.0D+00
  elon = 0.0D+00
  a = 90.0D+00
  numbr = ( n <= 200 )

  trplot_title = '(Triangulation created by STRIPACK)'

  trplot_file_name = 'delaunay.eps'

  call get_unit ( iunit )

  open ( unit = iunit, file = trplot_file_name )

  call trplot ( iunit, pltsiz, elat, elon, a, n, x, y, z, list, &
    lptr, lend, trplot_title, numbr, ierror )

  close ( unit = iunit )

  if ( ierror /= 0 ) then
    write ( *, '(a)' ) ' '
    write ( *, '(a)' ) 'STRIPACK_INTERFACE - Warning!'
    write ( *, '(a,i6)' ) '  TRPLOT returned error code ', ierror
    stop
  end if

  write ( *, '(a)' ) ' '
  write ( *, '(a)' ) 'TRPLOT created the triangulation plot file: ' // &
    trim ( trplot_file_name )
!
!  Write the XYZ file that includes Delaunay information.
!
  call tr_to_xyz ( n, x, y, z, list, lptr, lend )
!
!  Construct the Voronoi diagram.
!
!  Note that the triangulation data structure is altered if NB > 0.
!
  call crlist ( n, n, x, y, z, list, lend, lptr, lnew, &
    lbtri, listc, nb, xc, yc, zc, rc, ierror )

  if ( ierror /= 0 ) then
    write ( *, '(a)' ) ' '
    write ( *, '(a)' ) 'STRIPACK_INTERFACE - Fatal error!'
    write ( *, '(a)' ) '  Error in CRLIST.'
    write ( *, '(a,i6)' ) '  IERROR = ', ierror
    stop
  end if
!
!  Count the number of polygons of each size.
!
  call poly_count ( n, lend, lptr, listc )
!
!  Plot the Voronoi diagram.
!
  nt = 2 * n - 4

  vrplot_file_name = 'voronoi.eps'

  vrplot_title = '(Voronoi diagram created by STRIPACK)'

  call get_unit ( iunit )

  open ( unit = iunit, file = vrplot_file_name )

  call vrplot ( iunit, pltsiz, elat, elon, a, n, x, y, z, nt, listc, &
    lptr, lend, xc, yc, zc, vrplot_title, numbr, ierror )

  close ( unit = iunit )

  if ( ierror /= 0 ) then
    write ( *, '(a)' ) ' '
    write ( *, '(a)' ) 'STRIPACK_INTERFACE - Warning!'
    write ( *, '(a,i6)' ) '  VRPLOT returned error code ', ierror
    stop
  end if

  write ( *, '(a)' ) ' '
  write ( *, '(a)' ) 'VRPLOT created the Voronoi plot file: ' // &
    trim ( vrplot_file_name )
!
!  Write the XYZ file that includes Voronoi information.
!
  call vr_to_xyz ( n, xc, yc, zc, listc, lptr, lend, x, y, z )
!
!  Deallocate.
!
  deallocate ( ds )
  deallocate ( iwk )
  deallocate ( lbtri )
  deallocate ( lend )
  deallocate ( list )
  deallocate ( listc )
  deallocate ( lptr )
  deallocate ( ltri )
  deallocate ( rc )
  deallocate ( x )
  deallocate ( xc )
  deallocate ( y )
  deallocate ( yc )
  deallocate ( z )
  deallocate ( zc )

  return
end
subroutine ch_cap ( c )

!*******************************************************************************
!
!! CH_CAP capitalizes a single character.
!
!  Modified:
!
!    19 July 1998
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Input/output, character C, the character to capitalize.
!
  implicit none

  character c
  integer itemp

  itemp = ichar ( c )

  if ( 97 <= itemp .and. itemp <= 122 ) then
    c = char ( itemp - 32 )
  end if

  return
end
function ch_eqi ( c1, c2 )

!*******************************************************************************
!
!! CH_EQI is a case insensitive comparison of two characters for equality.
!
!  Examples:
!
!    CH_EQI ( 'A', 'a' ) is .TRUE.
!
!  Modified:
!
!    28 July 2000
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Input, character C1, C2, the characters to compare.
!
!    Output, logical CH_EQI, the result of the comparison.
!
  implicit none

  character c1
  character c1_cap
  character c2
  character c2_cap
  logical ch_eqi

  c1_cap = c1
  c2_cap = c2

  call ch_cap ( c1_cap )
  call ch_cap ( c2_cap )

  if ( c1_cap == c2_cap ) then
    ch_eqi = .true.
  else
    ch_eqi = .false.
  end if

  return
end
subroutine ch_to_digit ( c, digit )

!*******************************************************************************
!
!! CH_TO_DIGIT returns the integer value of a base 10 digit.
!
!  Example:
!
!     C   DIGIT
!    ---  -----
!    '0'    0
!    '1'    1
!    ...  ...
!    '9'    9
!    ' '    0
!    'X'   -1
!
!  Modified:
!
!    04 August 1999
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Input, character C, the decimal digit, '0' through '9' or blank
!    are legal.
!
!    Output, integer DIGIT, the corresponding integer value.  If C was
!    'illegal', then DIGIT is -1.
!
  implicit none

  character c
  integer digit

  if ( lge ( c, '0' ) .and. lle ( c, '9' ) ) then

    digit = ichar ( c ) - 48

  else if ( c == ' ' ) then

    digit = 0

  else

    digit = -1

  end if

  return
end
subroutine file_row_count ( file_name, nline )

!*******************************************************************************
!
!! FILE_ROW_COUNT counts the number of rows in a file.
!
!  Discussion:
!
!    The file is assumed to be a simple text file.
!
!    Blank lines and comment lines, which begin with '#', are not counted.
!
!  Modified:
!
!    21 June 2001
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Input, character ( len = * ) FILE_NAME, the name of the file.
!
!    Output, integer NLINE, the number of lines found in the file.
!    If the file could not be opened, then NLINE is returned as -1.
!
  implicit none

  character ( len = * ) file_name
  integer ios
  integer iunit
  character ( len = 256 ) line
  integer nline
  logical, parameter :: verbose = .false.

  nline = 0
!
!  Open the file.
!
  call get_unit ( iunit )

  open ( unit = iunit, file = file_name, status = 'old', form = 'formatted', &
    access = 'sequential', iostat = ios )

  if ( ios /= 0 ) then

    nline = -1

    if ( verbose ) then
      write ( *, '(a)' ) ' '
      write ( *, '(a)' ) 'FILE_ROW_COUNT - Fatal error!'
      write ( *, '(a)' ) '  Could not open the file:'
      write ( *, '(4x,a)' ) '"' // trim ( file_name ) // '".'
    end if

    return

  end if
!
!  Count the lines.
!
  do

    read ( iunit, '(a)', iostat = ios ) line

    if ( ios /= 0 ) then
      exit
    end if

    if ( len_trim ( line ) == 0 ) then
      cycle
    end if

    if ( line(1:1) == '#' ) then
      cycle
    end if

    nline = nline + 1

  end do

  close ( unit = iunit )

  return
end
subroutine get_unit ( iunit )

!*******************************************************************************
!
!! GET_UNIT returns a free FORTRAN unit number.
!
!  Discussion:
!
!    A "free" FORTRAN unit number is an integer between 1 and 99 which
!    is not currently associated with an I/O device.  A free FORTRAN unit
!    number is needed in order to open a file with the OPEN command.
!
!    If IUNIT = 0, then no free FORTRAN unit could be found, although
!    all 99 units were checked (except for units 5, 6 and 9, which
!    are commonly reserved for console I/O).
!
!    Otherwise, IUNIT is an integer between 1 and 99, representing a
!    free FORTRAN unit.  Note that GET_UNIT assumes that units 5 and 6
!    are special, and will never return those values.
!
!  Modified:
!
!    18 September 2005
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Output, integer IUNIT, the free unit number.
!
  implicit none

  integer i
  integer ios
  integer iunit
  logical lopen
 
  iunit = 0
 
  do i = 1, 99
 
    if ( i /= 5 .and. i /= 6 .and. i /= 9 ) then

      inquire ( unit = i, opened = lopen, iostat = ios )
 
      if ( ios == 0 ) then
        if ( .not. lopen ) then
          iunit = i
          return
        end if
      end if

    end if
 
  end do

  return
end
subroutine poly_count ( n, lend, lptr, listc )

!*******************************************************************************
!
!! POLY_COUNT counts the number of polygons of each size in the diagram.
!
!  Modified:
!
!    06 June 2002
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Input, integer N, the number of Voronoi polygons.
!
!    Input, integer LEND(N), some kind of pointer.
!
!    Input, integer LPTR(6*(N-2)), some other kind of pointer.
!
!    Input, integer LISTC(6*(N-2)), some other kind of pointer.
!
  implicit none

  integer n
  integer, parameter :: side_max = 20

  integer count(side_max)
  integer edges
  integer i
  integer kv
  integer lend(n)
  integer listc(6*(n-2))
  integer lp
  integer lpl
  integer lptr(6*(n-2))
  integer n0
  integer sides
  integer vertices
!
  count(1:side_max) = 0

  edges = 0
  vertices = 0

  do n0 = 1, n

    lpl = lend(n0)

    lp = lpl

    sides = 0

    do

      lp = lptr(lp)
      kv = listc(lp)

      vertices = max ( vertices, kv )
      sides = sides + 1
      edges = edges + 1

      if ( lp == lpl ) then
        exit
      end if

    end do

    if ( 0 < sides .and. sides < side_max ) then
      count(sides) = count(sides) + 1
    else
      count(side_max) = count(side_max) + 1
    end if

  end do

  edges = edges / 2

  write ( *, '(a)' ) ' '
  write ( *, '(a)' ) 'POLY_COUNT'
  write ( *, '(a)' ) '  Number of polygons of each shape.'
  write ( *, '(a)' ) ' '
  write ( *, '(a,i6)' ) '  Faces =    ', n
  write ( *, '(a,i6)' ) '  Vertices = ', vertices
  write ( *, '(a,i6)' ) '  Edges =    ', edges
  write ( *, '(a)' ) ' '
  write ( *, '(a,i6)' ) '  F+V-E-2 =  ', n + vertices - edges - 2
  write ( *, '(a)' ) ' '
  write ( *, '(a)' ) ' Sides  Number'
  write ( *, '(a)' ) ' '

  do i = 1, side_max - 1
    if ( count(i) /= 0 ) then
      write ( *, '(i6,i6)' ) i, count(i)
    end if
  end do

  if ( count(side_max) /= 0 ) then
    write ( *, '(i6,i6)' ) side_max, count(side_max)
  end if

  return
end
subroutine s_to_r8 ( s, r, ierror, lchar )

!*******************************************************************************
!
!! S_TO_R8 reads an R8 from a string.
!
!  Discussion:
!
!    This routine will read as many characters as possible until it reaches
!    the end of the string, or encounters a character which cannot be
!    part of the real number.
!
!    Legal input is:
!
!       1 blanks,
!       2 '+' or '-' sign,
!       2.5 spaces
!       3 integer part,
!       4 decimal point,
!       5 fraction part,
!       6 'E' or 'e' or 'D' or 'd', exponent marker,
!       7 exponent sign,
!       8 exponent integer part,
!       9 exponent decimal point,
!      10 exponent fraction part,
!      11 blanks,
!      12 final comma or semicolon.
!
!    with most quantities optional.
!
!  Examples:
!
!    S                 R
!
!    '1'               1.0
!    '     1   '       1.0
!    '1A'              1.0
!    '12,34,56'        12.0
!    '  34 7'          34.0
!    '-1E2ABCD'        -100.0
!    '-1X2ABCD'        -1.0
!    ' 2E-1'           0.2
!    '23.45'           23.45
!    '-4.2E+2'         -420.0
!    '17d2'            1700.0
!    '-14e-2'         -0.14
!    'e2'              100.0
!    '-12.73e-9.23'   -12.73 * 10.0**(-9.23)
!
!  Modified:
!
!    12 February 2001
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Input, character ( len = * ) S, the string containing the
!    data to be read.  Reading will begin at position 1 and
!    terminate at the end of the string, or when no more
!    characters can be read to form a legal real.  Blanks,
!    commas, or other nonnumeric data will, in particular,
!    cause the conversion to halt.
!
!    Output, real ( kind = 8 ) R, the real value that was read from the string.
!
!    Output, integer IERROR, error flag.
!
!    0, no errors occurred.
!
!    1, 2, 6 or 7, the input number was garbled.  The
!    value of IERROR is the last type of input successfully
!    read.  For instance, 1 means initial blanks, 2 means
!    a plus or minus sign, and so on.
!
!    Output, integer LCHAR, the number of characters read from
!    the string to form the number, including any terminating
!    characters such as a trailing comma or blanks.
!
  implicit none

  character c
  logical ch_eqi
  integer ierror
  integer ihave
  integer isgn
  integer iterm
  integer jbot
  integer jsgn
  integer jtop
  integer lchar
  integer nchar
  integer ndig
  real ( kind = 8 ) r
  real ( kind = 8 ) rbot
  real ( kind = 8 ) rexp
  real ( kind = 8 ) rtop
  character ( len = * ) s
  character, parameter :: TAB = char ( 9 )

  nchar = len_trim ( s )
  ierror = 0
  r = 0.0D+00
  lchar = - 1
  isgn = 1
  rtop = 0.0D+00
  rbot = 1.0D+00
  jsgn = 1
  jtop = 0
  jbot = 1
  ihave = 1
  iterm = 0

  do

    lchar = lchar + 1
    c = s(lchar+1:lchar+1)
!
!  Blank or TAB character.
!
    if ( c == ' ' .or. c == TAB ) then

      if ( ihave == 2 ) then

      else if ( ihave == 6 .or. ihave == 7 ) then
        iterm = 1
      else if ( ihave > 1 ) then
        ihave = 11
      end if
!
!  Comma.
!
    else if ( c == ',' .or. c == ';' ) then

      if ( ihave /= 1 ) then
        iterm = 1
        ihave = 12
        lchar = lchar + 1
      end if
!
!  Minus sign.
!
    else if ( c == '-' ) then

      if ( ihave == 1 ) then
        ihave = 2
        isgn = - 1
      else if ( ihave == 6 ) then
        ihave = 7
        jsgn = - 1
      else
        iterm = 1
      end if
!
!  Plus sign.
!
    else if ( c == '+' ) then

      if ( ihave == 1 ) then
        ihave = 2
      else if ( ihave == 6 ) then
        ihave = 7
      else
        iterm = 1
      end if
!
!  Decimal point.
!
    else if ( c == '.' ) then

      if ( ihave < 4 ) then
        ihave = 4
      else if ( ihave >= 6 .and. ihave <= 8 ) then
        ihave = 9
      else
        iterm = 1
      end if
!
!  Exponent marker.
!
    else if ( ch_eqi ( c, 'E' ) .or. ch_eqi ( c, 'D' ) ) then

      if ( ihave < 6 ) then
        ihave = 6
      else
        iterm = 1
      end if
!
!  Digit.
!
    else if ( ihave < 11 .and. lge ( c, '0' ) .and. lle ( c, '9' ) ) then

      if ( ihave <= 2 ) then
        ihave = 3
      else if ( ihave == 4 ) then
        ihave = 5
      else if ( ihave == 6 .or. ihave == 7 ) then
        ihave = 8
      else if ( ihave == 9 ) then
        ihave = 10
      end if

      call ch_to_digit ( c, ndig )

      if ( ihave == 3 ) then
        rtop = 10.0D+00 * rtop + real ( ndig, kind = 8 )
      else if ( ihave == 5 ) then
        rtop = 10.0D+00 * rtop + real ( ndig, kind = 8 )
        rbot = 10.0D+00 * rbot
      else if ( ihave == 8 ) then
        jtop = 10 * jtop + ndig
      else if ( ihave == 10 ) then
        jtop = 10 * jtop + ndig
        jbot = 10 * jbot
      end if
!
!  Anything else is regarded as a terminator.
!
    else
      iterm = 1
    end if
!
!  If we haven't seen a terminator, and we haven't examined the
!  entire string, go get the next character.
!
    if ( iterm == 1 .or. lchar+1 >= nchar ) then
      exit
    end if

  end do
!
!  If we haven't seen a terminator, and we have examined the
!  entire string, then we're done, and LCHAR is equal to NCHAR.
!
  if ( iterm /= 1 .and. lchar+1 == nchar ) then
    lchar = nchar
  end if
!
!  Number seems to have terminated.  Have we got a legal number?
!  Not if we terminated in states 1, 2, 6 or 7!
!
  if ( ihave == 1 .or. ihave == 2 .or. ihave == 6 .or. ihave == 7 ) then

    ierror = ihave

    return
  end if
!
!  Number seems OK.  Form it.
!
  if ( jtop == 0 ) then
    rexp = 1.0D+00
  else

    if ( jbot == 1 ) then
      rexp = 10.0D+00**( jsgn * jtop )
    else
      rexp = jsgn * jtop
      rexp = rexp / jbot
      rexp = 10.0D+00**rexp
    end if

  end if

  r = isgn * rexp * rtop / rbot

  return
end
subroutine timestamp ( )

!*******************************************************************************
!
!! TIMESTAMP prints the current YMDHMS date as a time stamp.
!
!  Example:
!
!    May 31 2001   9:45:54.872 AM
!
!  Modified:
!
!    15 March 2003
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    None
!
  implicit none

  character ( len = 40 ) string

  call timestring ( string )

  write ( *, '(a)' ) trim ( string )

  return
end
subroutine timestring ( string )

!*******************************************************************************
!
!! TIMESTRING writes the current YMDHMS date into a string.
!
!  Example:
!
!    STRING = 'May 31 2001   9:45:54.872 AM'
!
!  Modified:
!
!    15 March 2003
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Output, character ( len = * ) STRING, contains the date information.
!    A character length of 40 should always be sufficient.
!
  implicit none

  character ( len = 8 ) ampm
  integer d
  character ( len = 8 ) date
  integer h
  integer m
  integer mm
  character ( len = 9 ), parameter, dimension(12) :: month = (/ &
    'January  ', 'February ', 'March    ', 'April    ', &
    'May      ', 'June     ', 'July     ', 'August   ', &
    'September', 'October  ', 'November ', 'December ' /)
  integer n
  integer s
  character ( len = * ) string
  character ( len = 10 ) time
  integer values(8)
  integer y
  character ( len = 5 ) zone

  call date_and_time ( date, time, zone, values )

  y = values(1)
  m = values(2)
  d = values(3)
  h = values(5)
  n = values(6)
  s = values(7)
  mm = values(8)

  if ( h < 12 ) then
    ampm = 'AM'
  else if ( h == 12 ) then
    if ( n == 0 .and. s == 0 ) then
      ampm = 'Noon'
    else
      ampm = 'PM'
    end if
  else
    h = h - 12
    if ( h < 12 ) then
      ampm = 'PM'
    else if ( h == 12 ) then
      if ( n == 0 .and. s == 0 ) then
        ampm = 'Midnight'
      else
        ampm = 'AM'
      end if
    end if
  end if

  write ( string, '(a,1x,i2,1x,i4,2x,i2,a1,i2.2,a1,i2.2,a1,i3.3,1x,a)' ) &
    trim ( month(m) ), d, y, h, ':', n, ':', s, '.', mm, trim ( ampm )

  return
end
subroutine tr_to_xyz ( n, x, y, z, list, lptr, lend )

!*******************************************************************************
!
!! TR_TO_XYZ makes an XYZ file of Delaunay triangulation data.
!
!  Modified:
!
!    14 June 2002
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Input, integer N, the number of nodes.
!
!    Input, real ( kind = 8 ) X(N), Y(N), Z(N), the coordinates of the nodes.
!
!    Input, integer LIST(6*(N-2)), LPTR(6*(N-2)), LEND(N), information
!    defining the triangulation, created by TRMESH.
!
  implicit none

  integer n

  character ( len = 80 ) :: filename = 'delaunay.xyz'
  integer iunit
  integer lend(n)
  integer list(6*(n-2))
  integer lp
  integer lpl
  integer lptr(6*(n-2))
  integer node1
  integer node2
  real ( kind = 8 ) x(n)
  real ( kind = 8 ) y(n)
  real ( kind = 8 ) z(n)

  call get_unit ( iunit )

  open ( unit = iunit, file = filename )
!
!  Write header.
!
  write ( iunit, '(a)' ) '# ' // trim ( filename )
  write ( iunit, '(a)' ) '#'
  write ( iunit, '(a)' ) '#  XYZ file containing Delaunay triangle information.'
  write ( iunit, '(a)' ) '#'
!
!  List all the point coordinates.
!
  do node1 = 1, n
    write ( iunit, '(a)' ) ' '
    write ( iunit, '(3f8.4)' ) x(node1), y(node1), z(node1)
  end do
!
!  List all the line segments that emanate from a point.
!  (Will this involve listing segments twice?)
!
  do node1 = 1, n

    lpl = lend(node1)
    lp = lpl

    do

      lp = lptr(lp)
      node2 = abs ( list(lp) )

      write ( iunit, '(a)' ) ' '
      write ( iunit, '(3f8.4)' ) x(node1), y(node1), z(node1)
      write ( iunit, '(3f8.4)' ) x(node2), y(node2), z(node2)

      if ( lp == lpl ) then
        exit
      end if

    end do

  end do

  close ( unit = iunit )

  write ( *, '(a)' ) ' '
  write ( *, '(a)' ) 'TR_TO_XYZ:'
  write ( *, '(a)' ) '  Wrote the Delaunay XYZ file: ' // trim ( filename )

  return
end
subroutine vr_to_xyz ( n, xc, yc, zc, listc, lptr, lend, x, y, z )

!*******************************************************************************
!
!! VR_TO_XYZ makes an XYZ file of Voronoi diagram data.
!
!  Modified:
!
!    14 June 2002
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Input, integer N, the number of nodes.
!
!    Input, real ( kind = 8 ) XC(2*(N-2)), YC(2*(N-2)), ZC(2*(N-2)),
!    the coordinates  of the Voronoi vertices.
!
!    Input, integer LISTC(6*(N-2)), LPTR(6*(N-2)), LEND(N), information
!    defining the triangulation, created by TRMESH.
!
  implicit none

  integer n

  character ( len = 80 ) :: filename = 'voronoi.xyz'
  integer i
  integer iunit
  integer kv1
  integer kv2
  integer lend(n)
  integer listc(6*(n-2))
  integer lp
  integer lpl
  integer lptr(6*(n-2))
  integer node1
  integer node2
  real ( kind = 8 ) xc(2*(n-2))
  real ( kind = 8 ) yc(2*(n-2))
  real ( kind = 8 ) zc(2*(n-2))
  real ( kind = 8 ) x(2*(n-2))
  real ( kind = 8 ) y(2*(n-2))
  real ( kind = 8 ) z(2*(n-2))

  call get_unit ( iunit )

  open ( unit = iunit, file = filename )
!
!  Write header.
!
  write ( iunit, '(a)' ) '# ' // trim ( filename )
  write ( iunit, '(a)' ) '#'
  write ( iunit, '(a)' ) '#  XYZ file containing Voronoi diagram information.'
  write ( iunit, '(a)' ) '#'
!
!  List the vertex coordinates.
!
!  do i = 1, 2 * ( n - 2 )
!    write ( iunit, '(a)' ) ' '
!    write ( iunit, '(3f8.4)' ) xc(i), yc(i), zc(i)
!  end do
!
!  Loop on nodes (Voronoi centers) N0.
!  LPL indexes the last neighbor of N0.
!
  do i = 1, n

    lpl = lend(i)
!
!  Set KV2 to the first (and last) vertex index.
!
    kv2 = listc(lpl) 
!
!  Loop on neighbors of node.  For each triangulation edge
!  there is a corresponding Voronoi edge.
!
    lp = lpl

    write ( iunit, '(a)' ) ' center'
    write ( iunit, '(3f8.4)' ) x(i), y(i), z(i)
    write ( iunit, '(a)' ) ' polygon'
    do

      lp = lptr(lp)

      kv1 = kv2
      kv2 = listc(lp)
!
!  Add edge KV1-KV2 to the path if KV1 < KV2.
!
      if ( 1==1 ) then
!      if ( kv1 < kv2 ) then
        write ( iunit, '(3f8.4)' ) xc(kv1), yc(kv1), zc(kv1)
!        write ( iunit, '(3f8.4)' ) xc(kv2), yc(kv2), zc(kv2)
      end if

      if ( lp == lpl ) then
        exit
      end if

    end do

  end do

  close ( unit = iunit )

  write ( *, '(a)' ) ' '
  write ( *, '(a)' ) 'VR_TO_XYZ:'
  write ( *, '(a)' ) '  Wrote the Voronoi XYZ file: ' // trim ( filename )

  return
end
subroutine word_next_read ( s, word, done )

!*******************************************************************************
!
!! WORD_NEXT_READ "reads" words from a string, one at a time.
!
!  Special cases:
!
!    The following characters are considered to be a single word,
!    whether surrounded by spaces or not:
!
!      " ( ) { } [ ]
!
!    Also, if there is a trailing comma on the word, it is stripped off.
!    This is to facilitate the reading of lists.
!
!  Modified:
!
!    23 May 2001
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Input, character ( len = * ) S, a string, presumably containing words
!    separated by spaces.
!
!    Output, character ( len = * ) WORD.
!
!    If DONE is FALSE, then WORD contains the "next" word read.
!    If DONE is TRUE, then WORD is blank, because there was no more to read.
!
!    Input/output, logical DONE.
!
!    On input with a fresh string, set DONE to TRUE.
!
!    On output, the routine sets DONE:
!      FALSE if another word was read,
!      TRUE if no more words could be read.
!
  implicit none

  logical done
  integer ilo
  integer, save :: lenc = 0
  integer, save :: next = 1
  character ( len = * ) s
  character, parameter :: TAB = char ( 9 )
  character ( len = * ) word
!
!  We "remember" LENC and NEXT from the previous call.
!
!  An input value of DONE = TRUE signals a new line of text to examine.
!
  if ( done ) then

    next = 1
    done = .false.
    lenc = len_trim ( s )

    if ( lenc <= 0 ) then
      done = .true.
      word = ' '
      return
    end if

  end if
!
!  Beginning at index NEXT, search the string for the next nonblank,
!  which signals the beginning of a word.
!
  ilo = next
!
!  ...S(NEXT:) is blank.  Return with WORD = ' ' and DONE = TRUE.
!
  do

    if ( ilo > lenc ) then
      word = ' '
      done = .true.
      next = lenc + 1
      return
    end if
!
!  If the current character is blank, skip to the next one.
!
    if ( s(ilo:ilo) /= ' ' .and. s(ilo:ilo) /= TAB ) then
      exit
    end if

    ilo = ilo + 1

  end do
!
!  ILO is the index of the next nonblank character in the string.
!
!  If this initial nonblank is a special character,
!  then that's the whole word as far as we're concerned,
!  so return immediately.
!
  if ( s(ilo:ilo) == '"' .or. &
       s(ilo:ilo) == '(' .or. &
       s(ilo:ilo) == ')' .or. &
       s(ilo:ilo) == '{' .or. &
       s(ilo:ilo) == '}' .or. &
       s(ilo:ilo) == '[' .or. &
       s(ilo:ilo) == ']' ) then

    word = s(ilo:ilo)
    next = ilo + 1
    return

  end if
!
!  Now search for the last contiguous character that is not a
!  blank, TAB, or special character.
!
  next = ilo + 1

  do while ( next <= lenc )

    if ( s(next:next) == ' ' ) then
      exit
    else if ( s(next:next) == TAB ) then
      exit
    else if ( s(next:next) == '"' ) then
      exit
    else if ( s(next:next) == '(' ) then
      exit
    else if ( s(next:next) == ')' ) then
      exit
    else if ( s(next:next) == '{' ) then
      exit
    else if ( s(next:next) == '}' ) then
      exit
    else if ( s(next:next) == '[' ) then
      exit
    else if ( s(next:next) == ']' ) then
      exit
    end if

    next = next + 1

  end do
!
!  Ignore a trailing comma.
!
  if ( s(next-1:next-1) == ',' ) then
    word = s(ilo:next-2)
  else
    word = s(ilo:next-1)
  end if

  return
end
subroutine xyz_read ( xyz_file_name, n, x, y, z, ierror )

!*******************************************************************************
!
!! XYZ_READ reads graphics information from an XYZ file.
!
!  Discussion:
!
!    Comment lines begin with '#";
!    The XYZ coordinates of a point are written on a single line.
!
!  Example:
!
!     # cube.xyz
!     #
!     0 0 0
!     0 0 1
!     0 1 0
!     0 1 1
!     1 0 0
!     1 0 1
!     1 1 0
!     1 1 1
!
!  Modified:
!
!    05 June 2002
!
!  Author:
!
!    John Burkardt
!
!  Parameters:
!
!    Input, character ( len = * ) XYZ_FILE_NAME, the name of the input file.
!
!    Input, integer N, the number of points.
!
!    Output, real ( kind = 8 ) X(N), Y(N), Z(N), the point coordinates.
!
!    Output, integer IERROR, error flag.
!    0, no error occurred.
!    nonzero, an error occurred.
!
  implicit none

  integer n

  logical done
  integer i
  integer ierror
  integer ios
  integer iunit
  integer lchar
  character ( len = 256 ) line
  integer n2
  real ( kind = 8 ) temp(3)
  integer text_num
  character ( len = 100 ) word
  real ( kind = 8 ) x(n)
  character ( len = * ) xyz_file_name
  real ( kind = 8 ) y(n)
  real ( kind = 8 ) z(n)

  n2 = 0
  ierror = 0
  word = ' '
  text_num = 0

  call get_unit ( iunit )

  open ( unit = iunit, file = xyz_file_name, status = 'old', iostat = ios )

  if ( ios /= 0 ) then
    write ( *, '(a)' ) ' '
    write ( *, '(a)' ) 'XYZ_READ - Fatal error!'
    write ( *, '(a)' ) '  Could not open the input file.'
    ierror = 1
    stop
  end if
!
!  Read a line of text from the file.
!
  do

    read ( iunit, '(a)', iostat = ios ) line

    if ( ios /= 0 ) then
      exit
    end if

    text_num = text_num + 1
!
!  If this line begins with '#' , then it's a comment.  Read a new line.
!
    if ( line(1:1) == '#' ) then
      cycle
    end if
!
!  If this line is blank, then record that information.
!
    if ( len_trim ( line ) == 0 ) then
      cycle
    end if
!
!  This line records a node's coordinates.
!
    n2 = n2 + 1

    if ( n2 <= n ) then

      done = .true.

      do i = 1, 3

        call word_next_read ( line, word, done )

        call s_to_r8 ( word, temp(i), ierror, lchar )

        if ( ierror /= 0 ) then
          write ( *, '(a)' ) ' '
          write ( *, '(a)' ) 'XYZ_READ - Fatal error!'
          write ( *, '(a,i6)' ) '  S_TO_R8 returned IERROR = ', ierror
          write ( *, '(a,i6)' ) '  Reading (X,Y,Z) component ', i
          exit
        end if

      end do

      if ( ierror /= 0 ) then
        exit
      end if

      x(n2) = temp(1)
      y(n2) = temp(2)
      z(n2) = temp(3)

    end if

  end do

  close ( unit = iunit )
!
!  Report.
!
  write ( *, '(a)' ) ' '
  write ( *, '(a,i6,a)' ) 'XYZ_READ:'
  write ( *, '(a,i6,a)' ) '  Read ', text_num, ' text lines from ' &
    // trim ( xyz_file_name )
  write ( *, '(a,i6,a)' ) '  Read ', n2, ' sets of (X,Y,Z) coordinates.'


  return
end
