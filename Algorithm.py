import random
from math import *
from Gen2Airfoil import *
from xfoil_dat import *
import sys
import os


filelist = [ f for f in os.listdir(".") if f.endswith(".dat") ]
for f in filelist:
    os.remove(f)
#    print f   
filelist = [ f for f in os.listdir(".") if f.endswith(".log") ]
for f in filelist:
    os.remove(f)


# Airfoil is defined by
#  LEU = Leading edge up            LED = Leading edge down      
#  C25 = Camber at 25%              T25 = Camber at 25%
#  C50 = Camber at 50%              T50 = Camber at 50%
#  C75 = Camber at 75%              T75 = Camber at 75%

nsubjects = 20
nbest     = 10
name = "testfoil"

niterations = 15
Re = 1000000
Ncrit = 9.0


#              LEU   LED     C25   C50    C75      T25   T50   T75
genmaxs = [    0.2,  0.2,    0.2,  0.2,   0.2,     0.2,  0.2,  0.2   ]
genmins = [    -0.01,  0.0,    -0.01,  0.0,   -0.01,     -0.01,  0.0,  0.0   ]

ngen= len (genmaxs)

foilnum = 0



def newborn(gen):
    global foilnum
    foilnum+=1
    return [0,gen,'%06d' %foilnum]

def check_range(gen):
    for i in range(0,ngen):
        gen[i]=bound_value(gen[i],genmins[i],genmaxs[i])

def breed_random():
    child = [0]*ngen
    for i in range(0,ngen):
        child[i] = random.uniform(genmins[i],genmaxs[i])
        check_range(child)
    return newborn(child)


def bound_value(v,min_v,max_v):
	return min(max(min_v,v),max_v)

def breed_crossover_mutate(mother,father,mutation_probability=0.1,effect=0.5):
	child = [0]*ngen
	for i in range(0,ngen):
		child[i]=random.uniform(min(mother[i],father[i]),max(mother[i],father[i]))
		if random.random() < mutation_probability:
			min_v=min(genmins)
			max_v=max(genmaxs)
			v=child[i]
			rv=random.choice([-1,1]) * random.uniform(0,effect*(max_v - min_v))
			new_v_gauss=bound_value(random.gauss(v,(max_v - min_v) * effect),min_v, max_v)
			new_v = bound_value(v+rv,min_v,max_v)
			child[i]=new_v
	check_range(child)
	return newborn(child)


def gen2log(gen,logfile):
    logfile.write (gen[2])
    logfile.write (' {0:10.2f}       '.format(gen[0]))
    for i in range(0,ngen):
        logfile.write(" %1.4f " %gen[1][i])
    logfile.write("\n")

#              LEU   LED     C25   C50    C75      T25   T50   C75
testgen = [    0.5,  0.1,    0.1,  0.1,   0.3,     0.5,  0.6,  0.7   ]





logfile = open("logfile.log","w")



def populate():
	population = [[0,[],""] for i in range(0,nsubjects)]
	for i in range (0,nsubjects):
		#foilnum++
		population[i] = breed_random()
		#name = '%06d' %foilnum
		gen2airfoil(population[i][1],population[i][2]) # generate Airfoil shape by Bezier interpolation
		Xfoil(population[i][2],Ncrit,Re)                   # compute fittness in Xfoil
		population[i][0] = getLDmax(population[i][2])      # set fittness = LD
		print (i,population[i][2],population[i][0])
		gen2log(population[i],logfile)
	return population 

def eval_fitness(population):
    for i in range (0,nsubjects):          # evaluate fitness
        gen2airfoil(population[i][1],population[i][2]) # generate Airfoil shape by Bezier interpolation
        Xfoil(population[i][2],Ncrit,Re)                   # compute fittness in Xfoil
        population[i][0] = getLDmax(population[i][2])      # set fittness = LD
        print (i,population[i][0])
        gen2log(population[i],logfile)

def tournament(population):
	sample=random.sample(population,5)
	return max(sample,key=lambda x: x[0])

def selection(population,pairs):
	pool=[]
	while len(pool) < pairs: # no. of pairs of parents selected for breeding
		# Generate a pair for mating
		p1=tournament(population)
		a=[x for x in population if x not in p1]
		p2=tournament(a)
		pool.append((p1,p2))
	return pool


def evolve(pool,population,sz):
	offspring=[[0,[],""] for i in range(0,20)]
	cnt=0
	for p1,p2 in pool:
		offspring[cnt]=breed_crossover_mutate(p1[1],p2[1])
		cnt=cnt+1
	for i in range(0,sz):
		population[i]=offspring[i]
	return population


print (" ===== iteration: 0")
population=populate()
for i in range (1,niterations):
	print (" ===== iteration: ",i)
	eval_fitness(population)
	population.sort(reverse=True)
	population1=[[0,[],""] for i in range(0,20)]
	for i in range(0,10):
		population1[i]=population[i]
	pool=selection(population,10)
	population2=evolve(pool,population,10)
	for i in range(10,20):
		population1[i]=population2[i-10]
	for i in range(0,20):
		population[i]=population1[i]
logfile.close()



