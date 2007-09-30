#include "sparse_vector.h"
#define NDEBUG
#include<assert.h>
#include<math.h>
#include <string.h>
#include <iostream>
#include <fstream>

/* Created by Omid Madani Omid.Madani@overture.com
   Modified by John Langford jl@hunch.net
 */

using namespace std;


double dot_product(single_node* x1, single_node* x2);
double l2_norm(single_node* x);
double euclidean_distance(single_node* x1, single_node* x2, double upper_bound);
void print_features_of(single_node* x);

single_node** read_file (char *file_name, int & size);

void random_permute(single_node** xx, int size);

#define MAX_CHARS 160
#define MAXLINESIZE 600000
#define loop(i,n) for(int i=0; i < n; i++)
// use stringization to output the expression, then corresponding value
#define pr2(x,y) cout << #x  << ":  " << (y) << endl;

/************ file errors **************/

inline
void open_file_error(char* file_name)
{
  pr2("file opening failed.. exiting: ", file_name);
  exit(0);
}

/**********/

// return a random int between 0 and n-1, inclusive
int randomInt(int n);

double randomUniform(double lb=0 );


/**********/

template <class Type>
void swap(Type* a, int i, int j)
{
  Type x=a[i];
  a[i]=a[j];
  a[j]=x;
}

inline
void out_of_memory_error(char* line)
{
  cout << "Out of memory.. \"" << line << "\"" << endl;
  exit(0);
}


/*********** array stuff (allocation, size increase and decrease/fit)  *********/


template <class Type>
void allocate_array(Type* & a, int  desired_size)
{

  //  ps(# in allocate);
  
  a = new Type[desired_size];
  if (a==NULL)
    out_of_memory_error("out of memory, while allocating array!");
}

template <class Type>
void allocate_array(Type* & a, int  desired_size,  const Type & def_value)
{

  a = new Type[desired_size];
  if (a==NULL)
    out_of_memory_error("out of memory, while allocating array!");
  loop(i, desired_size)
    a[i] = def_value;

}

template <class Type>
void  expand_array(Type* & a, int & current_size, int desired_capacity, const Type & def_value) 
{
  int old_size = current_size;
  current_size = desired_capacity;
  Type* b;
  allocate_array(b, current_size);

  //Type* b = new Type[current_size];
  //if (b==NULL)
  //out_of_memory_error("out of memory, while expanding array size!");
  
  loop(i, old_size)
    b[i] =  a[i];
  loop(i, current_size-old_size)
    b[i+old_size] =   def_value;

  if (a != NULL && old_size > 0)
    delete [] a;
  
  a = b;

  
}

template <class Type>
void  expand_array(Type* & a, int & current_size, int desired_capacity) 
{
  int old_size = current_size;
  current_size = desired_capacity;
  Type* b;
  allocate_array(b, current_size);

  //Type* b = new Type[current_size];
  //if (b==NULL)
  //out_of_memory_error("out of memory, while expanding array size!");
  
  loop(i, old_size)
    b[i] =  a[i];
  delete [] a;
  a = b;
}


template <class Type>
void fit_array_to_size(Type* & a, int desired_size)
{
  Type* b;
  allocate_array(b, desired_size);
  
  //  Type* b = new Type[desired_size];
  // if (b==NULL)
  // out_of_memory_error("out of memory, while fitting to desired size!");
  
  loop(i, desired_size)
    b[i] =  a[i];
  
  delete [] a;
  a = b;
}

int randomInt(int n)
{
  int k;
  do 
    k=(int) (randomUniform()*n);
  while (k==n);
  
  return k;
}

// return a number in [0,1] uniformly at random
double randomUniform(double lb)
{
  return (double(random()) / RAND_MAX)*(1-lb) +  lb;
}

//Assumption: points are a multiples of 8 long
float distance(sparse_vector  p1, sparse_vector p2, float upper_bound)
{
  return (float) euclidean_distance((single_node*) p1, (single_node*) p2, upper_bound );
}

v_array<sparse_vector > parse_points(char *file_name)
{
  v_array<sparse_vector > parsed;
  
  //  learning_problem->l2_normalize();


  int size;
  single_node** xx = read_file (file_name, size);

  random_permute(xx, size );


  for(int i=0; i < size; i++)
    push(parsed, xx[i]);

  return parsed;
}


void random_permute(single_node** xx, int size)
{
  for (int i=size-1; i > 0; i--)
  {
    int j = randomInt(i+1);
    if ( i!=j )
      swap(xx, i, j);
  }
}

void print(const sparse_vector &p)
{

  print_features_of( (single_node *) p);
  cout << endl;
}

void print_features_of(single_node* x)
{
  
  int i=0;
  do {
    if (x[i].index == -1)
      break;
    cout << x[i].index << ":" <<x[i].value << " ";
    i++;
    
  } while (1);
}


double dot_product(single_node* x1, single_node* x2)
{

  if (x1 == NULL || x2 == NULL)
    return 0;
  
  int i =0;
  int j =0;
  
  double s=0;

  while (x1[i].index != -1 && x2[j].index != -1)
  {
    if (    x1[i].index == x2[j].index )
      s += x1[i++].value * x2[j++].value;
    else
      if (  x1[i].index < x2[j].index  )
        i++;
      else
        j++;
  } 
  
  return s;
  
}

double l2_norm(single_node* x)
{
  if (x == NULL)
    return 0;
  return sqrt(dot_product(x,x));
 
}

double euclidean_distance(single_node* x1, single_node* x2, double upper_bound)
{
  if (x1 == NULL)
    return l2_norm(x2);

  if ( x2 == NULL)
    return l2_norm(x1);
    
  int i =0;
  int j =0;
  
  double s=0;

  upper_bound *= upper_bound;
  
  
  while (x1[i].index != -1 && x2[j].index != -1)
  {
    if (    x1[i].index == x2[j].index )
    {
      s += ((x1[i].value - x2[j].value)*(x1[i].value - x2[j].value));
      i++;
      j++;
    }
    else
      if (  x1[i].index < x2[j].index  )
      {
        s += x1[i].value * x1[i].value;
        i++;
      }
      else
      {
        s += x2[j].value * x2[j].value;
        j++;
      }

    if (upper_bound != 0 && s > upper_bound)
       return sqrt(s);
  } 

  while (x1[i].index != -1 )
  {
    s += (x1[i].value * x1[i].value);
    if (upper_bound != 0 && s > upper_bound)
      return sqrt(s);
    i++;
  }

  
  while (x2[j].index != -1 )
  {
    s += (x2[j].value * x2[j].value);
    if (upper_bound != 0 && s > upper_bound)
       return sqrt(s);
    j++;
  }
  
  return sqrt(s);
}

int appears(char c, char* s)
{
  int found = 0;
  int i=0;
  while (s[i] != '\0' && !found)
  {
    if (c==s[i])
      found  = 1;
    else
      i++;
  }

  return found;
}

void skip_separated_fields(char* line, int n, int& pointer, char* chars_to_skip)
{
  //  cout << "\"" << chars_to_skip << "\"" << endl;
  //pr(n);
  
  loop(i, n)
    {
      // first skip non blank characters
      while (line[pointer] != '\0' && !appears(line[pointer], chars_to_skip) )
        pointer++;

      //  pr(pointer);
      
      // now skip blank characters
      while (line[pointer] != '\0' && appears(line[pointer], chars_to_skip) )
        pointer++;

      //pr(pointer);

      if (line[pointer]=='\0')
        break;
    }
  
}

int extract_vector(char* line, single_node*& x);

// return whether c occurs in s
// NOTE returns true if c is end of string \0
int occurs(char c, char* s)
{
  int appears = 0;

  for (int i=0; !appears; i++)
  {
    if (s[i]=='\0' && c != '\0' )
      return 0;
    else
      if (s[i]==c)
        appears = 1;
    
  }
  
  return appears;
  
}

int is_blank(char* line, char* white_space=" \t")
{
  int white = 1;

  for (int i=0; white; i++)
    if (line[i]=='\0')
      break;
    else
      if (!occurs(line[i], white_space))
        white = 0;

  return white;
  
}

single_node** read_file (char* f, int& size)
{
  
  ifstream ifile(f, ios::in);
  if (!ifile)
    open_file_error(f);

  char line[MAXLINESIZE];

  //   allocate a large array, and later reduce or expand it
  //   if needed

  int current_max_size = 50000;
  
  single_node** xx;
  allocate_array (xx, current_max_size, (single_node*) NULL);
  cout << "# reading instances from " <<  f << " ..\n";

  int i = 0;

  do
  {

    int eof = !(ifile.getline(line, MAXLINESIZE));

    if (eof)
      break;

    if (is_blank(line)) // skip blank lines
      continue;
    if ( line[0] =='#' ) // skip comments
      continue;
    
    int success = extract_vector(line, xx[i]);
    if (!success)
      continue;
    
    i++;
    if ( i >= current_max_size-1 )
      expand_array(xx, current_max_size , 2 * current_max_size, (single_node*)NULL);

  } while ( 1 );

  // i should equal to number of instances read and kept
  cout << "# number of instances read and kept is: " << i << endl;

  fit_array_to_size(xx, i);
  size = i;
  
  ifile.close();
  pr2(# done reading.. size,  size );

  return xx;  
}

int is_digit(char c)
{
  return (c >= '0' && c <='9');
}

int begins_a_number(char* c)
{
  return ( is_digit(c[0]) || (  (c[0] == '+' || c[0] == '-' || c[0] == '.')&& is_digit(c[1])  ) );  
}

int part_of_a_number(char c)
{
  return ( (c >= '0' && c <='9') || c == '+' || c == '-' || c == '.' || c == 'e' || c == 'E' );  
}

// assumes s represents a positive wbole number (without fractional part)
// (used along with convert_to_integer to handle larger numbers)
double convert_to_whole_number(char* s)
{
  int i=0;
  double sum = 0;
  while (s[i] != '\0' && s[i] != '.')
  {
    //cout << "s_i: " << s[i] << endl;
    
    int j = ( s[i] - '0' );
    sum = sum * 10. + j;
    
    i++;
  }
  
  return sum;
}

// s represents a number possibly with a sign and decimal point (bot not 'e')
double extract_number_no_e(char* s)
{
  double first=0;

  int sign = 1;
  if (s[0]=='-')
    sign = -1;

  if (s[0]=='+' || s[0]=='-')
    s[0]='0';
  
  if (s[0]<='9' && s[0]>='0')
    first = convert_to_whole_number(s);

  //  cout << "first half = " << first << endl;
  
  int i=0;
  while (s[i] != '.' && s[i] != '\0')
    i++;

  if (s[i]== '\0') return (first * sign);

  double fraction = 0;
  if (s[i]=='.')
  {
    i++;
    double sum=0;
    double pow=1;
    while (s[i]!='\0' && s[i]!='e')
    {
      int j = (s[i]- '0');
      sum = sum * 10 + j;
      pow*=10;
      i++;

    }
    
    fraction = (double) sum/pow;

  }

  //  cout << "second half = " << fraction << endl;
  
  return ( sign * (first + fraction) );
  
}

// s represents a number possibly with exponentiation and sign and decimal point (and no extra stuff!)
double convert_to_number(char* s)
{

  int i=0;
  while (s[i] != 'e' && s[i] != '\0')
    i++;

  if (s[i]=='\0')
    return extract_number_no_e(s);

  s[i]='\0';
  double first = extract_number_no_e (s);
  double second = extract_number_no_e (&(s[i+1]));

  return first * exp( second* log(10.0) );
  
}

// start your search at pointer and return the next value appearing in the line
// success flags whether a number was found
// pointer will point to the following character after the number was found

// note the numbers  may not be bigger than a the integer size
double get_next_number(char* line, int& pointer, int & success )
{
  static  char temp[MAX_CHARS + 1];

  success = 1;
  
  while (line[pointer] != '\0' && !begins_a_number(&line[pointer]))
    pointer++;// point to first letter of the number

  // if no number found
  if (line[pointer]=='\0')
  {
    pointer = -1;
    success = 0;
    return 0;
  }
  
  // get the number (delimit it in temp)
  int i=0;
  for (; part_of_a_number(line[i+pointer]); i++)
    temp[i]=line[i+pointer];  
  temp[i]='\0';

  pointer = pointer + i; // update pointer

  return convert_to_number(temp);
}

void number_expected_error(char* line)
{
  cout << "Number expected in: \"" << line << "\"" << endl;
  exit(0);
}

// same as above, without the success indicator
double get_next_number(char* line, int & pointer)
{

  int success;
  double s = get_next_number(line, pointer, success);  

  //ps(next number called);
  // pr(pointer);
  
  if (!success)
    number_expected_error(line);
  
  return s;
  
}

int extract_vector(char* line, single_node*& x)
{
  int i=0;
  int pointer = 0;
  int read_success;

  skip_separated_fields(line, 1,  pointer, " \t");
  //  line = &(line[pointer]);
  
  //cout << line << endl;
  //cout << "pointer=" << pointer << endl;
  
  int old_id=-2;
  int not_sorted = 0;

  if (x != NULL)
    delete [] x;

  static  int max_size = 200;
  allocate_array(x, max_size);
  
  for (i=0;  ; i++)
  {
    
    if ( i >= max_size ) // expand
      expand_array(x, max_size, max_size*2);
    
    x[i].index = (int) get_next_number(line, pointer, read_success);

    //cout << "index=" << x[i].index << endl;
    
    //  cout << "fid= " << ( feature_ids[i]  ) << endl;
    
    if ( !read_success ) break;

    if ( !( x[i].index > old_id) )
      not_sorted = 1;
    else
      old_id = x[i].index;
    
    x[i].value = get_next_number(line, pointer, read_success);

    if( !read_success)
    {
      cout << "expected a number for the value of the feature in line:\n";
      cout << line << endl;
      cout << "pointer = " << pointer << endl;
      
      exit(0);
    }
  }

  x[i].index=-1;
  //if (not_sorted)
  //  sort_vector_features(x);

  fit_array_to_size(x, i+1 );

  return 1;
}

