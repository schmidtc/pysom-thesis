import sys
sys.path.insert(0,'/Users/cschmidt/Documents/repos/pysom/trunk')
import pysom

#create an instance of the Observation File class.
# 3d-7c-no1_rs.dat, is a generated data file containing 7 clusters in 3 dimensions.
f = pysom.data.ObsFile("3d-7c-no1_rs.dat")

#create a networkX graph using provided utility functions
rows = 20
cols = 20
hex = pysom.utils.topology.hexGraph(rows,cols)

# Initialize the SOM object
S = pysom.som.GraphTopology(hex)
# Set the training Parameters
S.Dims = 3 #The number of dimmensions in the training data
S.maxN = 0.5 #The percent of the network to include in the first training step
S.tSteps = 100000 #The number training steps to perform
S.tSteps = 100
S.alpha0 = 0.04 #The initial learning rate

#Randomly Initialize the reference vectors.
S.randInit()

# Save the initial State (optional)
S.save("output/", "initial_state")


#Train the som
S.run(f)
#Save the trained SOM and the Map
S.save("output/","phase1")

#Adjust training parameters for phase Two training,
S.maxN = 0.333
S.tSteps = 1000000
S.tSteps = 1000
S.alpha0 = 0.03

#Reset the observation file
f.reset()
#Start training
S.run(f)
#Map the observation onto the SOM (optional)
f.reset()
S.map(f)
#Save
S.save("output/","phase2")

