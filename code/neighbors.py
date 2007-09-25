class graph:
    def __init__(self):
        self.W = {} # This is the sparse first order weights matrix
    def addLink(self,i,j):
        """ Add a link from i to j """
        if not i in self.W:
            self.W[i] = []
        else:
            self.W[i].append(j)

