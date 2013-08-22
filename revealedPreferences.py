#!/usr/bin/python
import sys
import copy
verbose = False

#This script takes, as input, the preference lists of all elements of A and
#the preference lists of all elements of B. It uses the Extended Gale-Shapley 
#Algorithm for One-One Matching to produce the unique A-optimal stable matching.

#Verbose print function
if verbose:
    def vprint(*args):
        # Print each argument separately so caller doesn't need to
        # stuff everything to be printed into a single string
        for arg in args:
           print arg,
        print
else:   
    vprint = lambda *a: None      # do-nothing function

#Check if alpha_n is satisfied with matching M, GS-list G
def satisfied(n,M,G):
	if M[n] != None or G[n] == M[n]:
		return True
	else:
		return False

def generateG_A(inpt):
	#Assign elements of input to variables
	sizeA = len(inpt[-1])
	sizeB = len(inpt[0])
	alphaPreferences = copy.deepcopy(inpt[0:sizeA])
	betaPreferences = copy.deepcopy(inpt[sizeA:])

	vprint("Input:")
	vprint(alphaPreferences)
	vprint(betaPreferences)

	#Check for bad input
	if sizeA+sizeB != len(inpt):
		print "Improper Data Formatting 1"
		sys.exit()
	for alpha in alphaPreferences:
		if set(alpha) != set(range(sizeB)):
			print "Improper Data Formatting 2: "+str(alpha)
			sys.exit()
	for beta in betaPreferences:
		if set(beta) != set(range(sizeA)):
			print "Improper Data Formatting 3: "+str(beta)
			sys.exit()

	#Initialize M and G
	M=[]
	for i in range(sizeA):
		M.append(None)
	G = alphaPreferences

	vprint("M=", str(M))
	vprint("G=", str(G))

	#The algorithm begins!
	unsatisfiedList = range(sizeA)
	vprint("Unsatisfied alphas:", str(unsatisfiedList))
	while unsatisfiedList != []:	#Execute until all alphas are satisfied
		vprint("\n")
		n = unsatisfiedList[0]	#Select an unsatisfied alpha, alpha_n
		betaJ = G[n][0]	#Take alpha_n's favorite available beta, beta_j
		#Step 1: Unmatch beta_j from its previous partner, in M
		for k in [k for k in range(sizeA) if M[k] == betaJ]:
			M[k]= None
		M[n]=betaJ	#Match alpha_n to beta_j
		#Step 2: Remove partners less preferable to beta_j, in G
		for k in range(sizeA):
			if (betaPreferences[betaJ].index(k)>betaPreferences[betaJ].index(n) and 
				betaJ in G[k]):
				G[k].remove(betaJ)
		#Check which alphas are still dissatisfied
		unsatisfiedList = [n for n in range(sizeA) if not satisfied(n,M,G)]
		vprint("M=", str(M))
		vprint("G=", str(G))
		vprint("Unsatisfied alphas:" + str(unsatisfiedList))
	return G

def generateG_B(inpt):
	sizeA=len(inpt[-1])
	sizeB=len(inpt[0])
	return generateG_A(inpt[-sizeB:]+inpt[:sizeA])

#Main function begins here
#Translate input into list array of integers
x=sys.stdin.read()
x=x.splitlines()
for i in range(len(x)):
	x[i] = x[i].split()
	for j in range(len(x[i])):
		x[i][j]=int(x[i][j])

#Finds row-domination free nodes, and column-domination free nodes
GA = generateG_A(x)
##print str(GA)
GB = generateG_B(x)
##print str(GB)

#Format as sets of pairs, and get intersection
GA_set = set()
GB_set = set()
for i in range(len(GA)):
	for j in GA[i]:
		GA_set.add((i,j))
for i in range(len(GB)):
	for j in GB[i]:
		GB_set.add((j,i))
G_set = (GA_set & GB_set)

for pair in G_set:
	vprint( str(pair))

#Reinterpret intersection, to better pipe to graphviz
GA_restricted = copy.deepcopy(GA)
for i in range(len(GA)):
	for j in GA[i]:
		if (i,j) not in G_set:
			GA_restricted[i].remove(j)

##print GA_restricted

GB_restricted = copy.deepcopy(GB)
for j in range(len(GB)):
	for i in GB[j]:
		if (i,j) not in G_set:
			GB_restricted[j].remove(i)

##print GB_restricted

output = """graph G {\n"""
for i in range(len(GA)):
	output = output + """\tA%d [ pos = "-1,%d!", shape = none];\n""" % (i,i)
for i in range(len(GB)):
	output = output + """\tB%d [ pos = "%d,-1!", shape = none];\n""" % (i,i)

for pair in (GA_set & GB_set):
	output = output + """\tn%d_%d [ pos = "%d,%d!", label ="", shape = point ];\n""" % (pair[0],pair[1],pair[1],pair[0])

for i in range(len(GA)):
	for index in range(len(GA_restricted[i])-1):
		output = output +"""\tn%d_%d -- n%d_%d [ dir = back ];\n""" % (i,GA_restricted[i][index],i,GA_restricted[i][index+1])

for j in range(len(GB)):
	for index in range(len(GB_restricted[j])-1):
		output = output +"""\tn%d_%d -- n%d_%d [ dir = back ];\n""" % (GB_restricted[j][index],j,GB_restricted[j][index+1],j)
output = output + """\t}"""
print output


command="neato -T jpeg -Gsplines=true neato_test2 > neato_test2.jpg"

