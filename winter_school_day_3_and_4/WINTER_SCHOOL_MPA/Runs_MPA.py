#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------
## Import relevent libraries ##
from pylab import *
import copy as cp
import random as rd
import math
import numpy as np
import  matplotlib.pyplot as plt
import csv 
from statistics import mean
import pandas as pd

##----------------------------------------------------------------------------
    
## Parameters ##

# Fishing environment #
K = 600 # carrying capacity of fishing ground (must be greater than initial number of fish)
n = 150 # number of simulation  years

# Fish characteristics #
growth_prob =  0.35 # maximum intrinsic growth rate
init_fish = 400 # initial total number of fishes
move_fish = 0.2 # speed of fish 
rad_repulsion = 0.025 # radius of repulsion zone
rad_orientation = 0.06 # radius of orientation zone 
rad_attraction =  0.1 # radius of attraction zone 
rad_repulsion_sqr = rad_repulsion ** 2 # radius of repulsion zone squared
rad_orientation_sqr = rad_orientation ** 2 # radius of orientation zone squared
rad_attraction_sqr = rad_attraction ** 2 # radius of attraction zone squared

# Fishing unit characteristics
num_fishers = 20 # number of pirogues
move_fishers = 0.3 # speed of a pirogue 
q = 0.6 # catchability coefficient
r = 0.2 # neighbourhood radius 
r_sqr = r ** 2 # neighbourhood radius squared

# Cooperation level (total of num_fishers)
fully_noncoop = 10 # number of fully_noncooperative pirogues
fully_coop = 10 # number of fully_cooperative pirogues

# Design of the MPA simulation (size, distance and age MPA) 
MPA = 'no'  # run with-only-MPA simulation? (A 'yes' implies only-with-MPA and 'no' implies only-without-MPA)
Type_MPA = 'none' # If MPA  = 'yes', which spatial configuration do you want? (A 'spaced' implies two MPAs and 'single' implies only one MPA)
Dist_MPA = 0.2 # If Type_MPA = 'spaced', What should be the distance between the two MPAs ?
Frac_MPA = 0.2  # If MPA  = 'yes', What fraction of the fishing environments should be set as MPA?

##----------------------------------------------------------------------------

# Coordinates of the fishing ground 
Area = 2.0000 
Length_Area = math.sqrt(Area)
Half_Length_Area = Length_Area / 2

# Coordinates of the MPA
Half_Length = (math.sqrt(Frac_MPA* Area)) / 2 # compute half the length  of MPA 

# Coordinates for a single MPA
Xa = - Half_Length 
Xb =   Half_Length 
Ya = - Half_Length 
Yb =   Half_Length

# Coordinates of first spaced MPA
Xm = - Half_Length - (Dist_MPA / 2)
Xn = -(Dist_MPA / 2) 
Ym = - Half_Length 
Yn =   Half_Length 

# Coordinates of second spaced MPA #
Xp = (Dist_MPA / 2) 
Xq =  Half_Length + (Dist_MPA / 2)
Yp = -Half_Length 
Yq =  Half_Length

#----------------------------------------------------------------------------
with open("Functions_MPA.py") as file: # read the file containing the functions representing the proceses
    exec(file.read())
    
#----------------------------------------------------------------------------
 ## Create a subfolder to keep all plot files and data
import shutil, os
subdir = 'simulation_output' # subfolder name for plot files
if os.path.isdir(subdir): # does the subfolder already exist?
    shutil.rmtree(subdir) # delete the whole folder
os.mkdir(subdir) # make new subfolder
os.chdir(subdir) # move to subfolder

#---------------------------------------------------------------------------------------------------    
initialize()  
observe()
    
for j in range(1, n):  
    update_one_unit_time()
    observe()
#os.system("ffmpeg -v quiet -r 5 -i year_%04d.png -vcodec mpeg4  -y -s:v 1920x1080 simulation_movie.mp4") # convert files to a movie
os.chdir(os.pardir) # optional: move up to parent folder

#---------------------------------------------------------------------------------------------------
# Plot the simualtion outputs
sim_dat = 'simulation_output/simulation_data.csv'  # read average all subject data 
sim_dat = pd.read_csv(sim_dat, header=0)
column_names=list(sim_dat.columns[-4:]) # all but the first element (which is time)

fig = plt.figure(figsize=(12, 7))
fig.suptitle('nr. noncoperators = ' + str(fully_noncoop) + ',' + ' ' + 'nr. cooperators = ' + str(fully_coop) + ',' + ' ' + 'MPA =' + str(MPA) + ',' + ' ' + ('Type MPA =' + str(Type_MPA) if MPA == "yes" else 'Type MPA =' + str('none')), fontsize=18)
fig.subplots_adjust(hspace=0.3, wspace=0.1) # horizontal and vertical space 

j = 1
for i in column_names:
    # j == 1
    ax = fig.add_subplot(2, 2, j) # fig positioning
    ax.plot(sim_dat.loc[:,'time'], sim_dat.loc[:,i], color='black', lw=1.6) 
    #ax.text(0, 0,  sum(sim_dat.loc[:,i]))
    ax.set_ylabel(i, fontsize=20)

    if any([j == 3, j == 4]):
        ax.set_xlabel("Time steps", fontsize=20)   
    j +=1
plt.tight_layout() 
plt.savefig("output_dynamics_0.pdf", bbox_inches='tight', pad_inches=0.1, dpi=300) 
#---------------------------------------------------------------------------------------------------

