def scaler(data_file_name,out_file_name,delim=None,minList=None,maxList=None):
	"""
	scaler scales all the values in a text file using the giving minList and maxList, if both min and max lists are not given they are generated.  Values will be scaled from 0 to 1 by default.

	The first line in the text file must be a single integer, specify the number of dimmensions to scale.  The first n dims will be scaled.

	Example datafile:
	3
	50 0 100 Label 1
	0 100 50 Label 2
	100 50 0 Label 3

	outfile:
	3
	0.5 0.0 1.0 Label 1
	0.0 1.0 0.5 Label 2
	1.0 0.5 0.0 Label 3


	An optional deliminater can be specified. Otherwise python's default is used (' ')
	Returns: (minList,maxList)
	"""
	data = open(data_file_name,'r')
	outf = open(out_file_name,'w')

	dim = int(data.readline().strip('\n'))

	if not minList or not maxList:
		line = data.readline()
		line = line.strip('\n')
		line = line.split(delim)
		minList = [float(line[n]) for n in xrange(dim)]
		maxList = [float(line[n]) for n in xrange(dim)]
		line = data.readline()
		while line:
			line = line.strip('\n')
			line = line.split(delim)
			for n in xrange(dim):
				val = float(line[n])
				if val < minList[n]:
					minList[n] = val
				if val > maxList[n]:
					maxList[n] = val
			line = data.readline()

	data.seek(0)
	outf.write(data.readline())
	line = data.readline()
	while line:
		line = line.strip('\n')
		line = line.split(delim)
		for n in xrange(dim):
			line[n] = str((float(line[n])-minList[n]) / (maxList[n] - minList[n]))
		line = ' '.join(line) + '\n'
		outf.write(line)
		line = data.readline()
	outf.close()
	data.close()
	return minList,maxList
if __name__=="__main__":
	from sys import argv
	infname = argv[1]
	outfname = argv[2]
	print scaler(infname,outfname)
