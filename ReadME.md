#summary How to run pysom.

# Introduction #

PySOM is a topology independant implemenation of the Self-Organizing Maps
training algorithm, it is written in the Python Programming Language. To train a
SOM you must provide your own topology in the form a NetworkX undirected Graph.
Python functions are provided for created both hexagon and rectangular graphs.
Some support is provided for Geodesic and Spherical graphs.

The graph is supplied as an argument to the som.GraphTopology class.
After an instance of som.GraphToplogy has been created the following parameters
must be set:
Dims = The number of dimmensions in the data set.
maxN = The Initial neighborhood size, as a percentage of the entire graph (0 to 1)
tSteps = The number of training steps.
alpha0 = The initial learning rate (0 to 1).

You must also


# Details #

Add your content here.  Format your content with:
  * Text in **bold** or _italic_
  * Headings, paragraphs, and lists
  * Automatic links to other wiki pages