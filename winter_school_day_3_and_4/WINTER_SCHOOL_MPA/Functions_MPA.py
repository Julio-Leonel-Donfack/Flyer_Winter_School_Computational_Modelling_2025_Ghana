#!/usr/bin/env python3
# -*- coding: utf-8 -*-



#---------------------------------------------------------------------------

# An agent-based model (ABM) representative of the Senegalese sardine artisanal fishery 
# to untangle the combined effects of fishery collective behaviour (characterized by 
# cooperative trait and associated fishing effort) and design of no-take fishery 
# area (size, distance of between network of areas and age MPA)

# By : OWUSU, Kwabena Afriyie
# Date : 16th April, 2019

#----------------------------------------------------------------------------
###########################################################################################################

class agent:  # create an empty class
    pass     
    
def initialize():
    
    global time1, time2, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen, fishermen_data1,  fishermen_data2, fishermen_data3 
    time1 = 0. # time
    time2 =[time1]
    agents = []  # list containing fishes and fishermen
    fish_data = [init_fish]  # list containing number of fishes
    total_hav_data = {} # dictionary containing total catch of fishermen according to cooperative-trait 
    current_hav_data  = {} # dictionary containing current catch of fishermen according to cooperative-trait 
    fishermen_data1 = [0] # list containing total catch of fishermen 
    fishermen_data2 = [0] # list containing current catch of fishermen 

#----------------------------------------------------------------------------------------------------------    
    # Attributes of agents (fishermen and fish) #
    for j in range(num_fishers + init_fish):    
        ag = agent()
        ag.type = 'fishers' if j < num_fishers else 'fish'  # set first (num_fishers)-th as fishermen and remaining as fishes
        
        if ag.type == 'fishers':
            ag.harvest = 0 # initialise harvest as zero for all fishermen
            
            if j < (fully_noncoop): # set first (fully_noncoop)-th fishermen agents as fully_noncooperators
                ag.effort = 1.0    # predefined effort corresponding to fully_noncooperators
                ag.trait = 'fully_noncoop' # set their cooperative-trait
                ag.num = 'fully_noncoop%d'% (1 + j) # to set fully_noncooperators as "fully_noncooperators1, fully_noncooperators2, etc." 
               
            elif (fully_noncoop) <= j < (fully_noncoop + fully_coop): # set second (fully_coop)-th fishermen agents as fully_cooperators
                ag.effort = 0.2
                ag.trait = 'fully_coop'
                ag.num = 'fully_coop%d'% ((1 + j) - fully_noncoop)
                        
            total_hav_data[ag.num]  = [ag.harvest]  # initialise total catch of fishermen according to cooperative trait
            current_hav_data [ag.num]  = [ag.harvest] # initialise current catch according to cooperative trait

#----------------------------------------------------------------------------------------------------------                     
            if (MPA == 'no') : # only no MPA 
                # randomly assign spatial_position to fishermen 
                ag.x = rd.uniform(-Half_Length_Area, Half_Length_Area)
                ag.y = rd.uniform(-Half_Length_Area, Half_Length_Area)
                
            
            elif (MPA == 'yes' and Type_MPA == 'single'): # only single MPA
                while True: # randomly assign spatial_position to fishermen
                    ag.x = rd.uniform(-Half_Length_Area, Half_Length_Area)
                    ag.y = rd.uniform(-Half_Length_Area, Half_Length_Area)
                    if not((Xa <= ag.x <= Xb) and (Ya <= ag.y <= Yb)) : # keep looping until spatial_position falls outside the MPA
                        break
                        
            elif (MPA == 'yes' and Type_MPA == 'spaced'): # only spaced MPA
                while True: # randomly assign spatial_position to fishermen 
                    ag.x = rd.uniform(-Half_Length_Area, Half_Length_Area)
                    ag.y = rd.uniform(-Half_Length_Area, Half_Length_Area)
                    if all([not((Xm <= ag.x <= Xn) and (Ym <= ag.y <= Yn)), 
                        not((Xp <= ag.x <= Xq) and (Yp <= ag.y <= Yq))]): # keep looping until spatial_position falls outside the MPA
                            break
        else: # if a fish
            ag.x = rd.uniform(-Half_Length_Area, Half_Length_Area)
            ag.y = rd.uniform(-Half_Length_Area, Half_Length_Area)

        agents.append(ag) # put all agents 
        
#----------------------------------------------------------------------------------------------------------
    # Initialise the number of fishes in an MPA 
    if (MPA == 'no') :
        fish_data_MPA = [0] #  a zero because no mpa is available
        
    elif (MPA == 'yes' and Type_MPA == 'single'): # only single MPA
        fish_data_MPA = [sum([1 for j in agents if j.type == 'fish' and  ((Xa <= j.x <= Xb) and (Ya <= j.y <= Yb))])]
        
    elif (MPA == 'yes' and Type_MPA == 'spaced'):
        fish_data_MPA = [sum([1 for j in agents if j.type == 'fish' and any([((Xm <= j.x <= Xn) and (Ym <= j.y <= Yn)), ((Xp <= j.x <= Xq) and (Yp <= j.y <= Yq))])])]
    
    fishermen_data3 = [fish_data[-1] - fish_data_MPA[-1]] # initialise number of fishes outside MPA
    

###########################################################################################################


def observe():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen , fishermen_data1,  fishermen_data2, fishermen_data3    
    plt.clf()  # clear figure
    plt.subplot(111, facecolor='white') # background color
    
    fishermen = [ag for ag in agents if ag.type == 'fishers']  # fisherman
    if len(fishermen) > 0:
        X_fully_noncoop = [ag.x for ag in fishermen if ag.trait == 'fully_noncoop'] # x-axis
        Y_fully_noncoop = [ag.y for ag in fishermen if ag.trait == 'fully_noncoop'] # y-axis
        
        X_fully_coop = [ag.x for ag in fishermen if ag.trait == 'fully_coop']
        Y_fully_coop  = [ag.y for ag in fishermen if ag.trait == 'fully_coop']
        
        # Set five different color of reds  
        colors = np.linspace(0, 1, 2) ; mymap = plt.get_cmap("Greys") ; my_colors = mymap(colors) 
         
        # plot fisherman-agents
        plt.plot(X_fully_coop, Y_fully_coop, 'o', color = my_colors[1], markersize=7.5, label='fully_coop',markeredgecolor='black')
        plt.plot(X_fully_noncoop, Y_fully_noncoop, 'o', color = my_colors[0], markersize=7.5, label='fully_noncoop',markeredgecolor='black')
        
#----------------------------------------------------------------------------------------------------------             
    fish = [ag for ag in agents if ag.type == 'fish']  #  fish-agents
    if len(fish) > 0:
        X_fish = [ag.x for ag in fish]
        Y_fish = [ag.y for ag in fish]
        #plt.plot(X_fish, Y_fish, '^', color='darkgreen', markersize=3, label='fish') #  plot  fish-agents
        plt.plot(X_fish, Y_fish, '.',markersize=3, label='fish',markerfacecolor="none",markeredgecolor='black') #  plot  fish-agents
    
    if (MPA == 'yes' and Type_MPA == 'single'):
        #Lines enclosing single MPA
        plt.vlines(Xa, Ya, Yb, lw=2, color='k') # (x1,y1,y2) 
        plt.vlines(Xb, Ya, Yb, lw=2, color='k') # (x2,y1,y2)
        plt.hlines(Ya, Xa, Xb, lw=2, color='k') # (y1,x1,x2)
        plt.hlines(Yb, Xa, Xb, lw=2, color='k') # (y2, x1,x2)
        
    elif (MPA == 'yes' and Type_MPA == 'spaced'):
        # Lines enclosing the first spaced MPA
        plt.vlines(Xm, Ym, Yn, lw=2, color='k') # (x1,y1,y2) 
        plt.vlines(Xn, Ym, Yn, lw=2, color='k') # (x2,y1,y2)
        plt.hlines(Ym, Xm, Xn, lw=2, color='k') # (y1,x1,x2)
        plt.hlines(Yn, Xm, Xn, lw=2, color='k') # (y2, x1,x2)
         # Lines enclosing the second spaced MPA
        plt.vlines(Xp, Yp, Yq, lw=2, color='k') # (x1,y1,y2) 
        plt.vlines(Xq, Yp, Yq, lw=2, color='k') # (x2,y1,y2)
        plt.hlines(Yp, Xp, Xq, lw=2, color='k') # (y1,x1,x2)
        plt.hlines(Yq, Xp, Xq, lw=2, color='k') # (y2, x1,x2)
    
    axis('image') ; axis([-Half_Length_Area, Half_Length_Area,-Half_Length_Area, Half_Length_Area]) ; plt.grid(False) ; plt.xticks([], []) ; plt.yticks([], [])  # plt.axis('off') axis , grid and axis-ticks
    plt.title('year =' + str(int(time1))) # title
    plt.legend(numpoints=1, loc= 'center', bbox_to_anchor=(0.5, -0.072), ncol=3, prop={'size':11}, facecolor='white')
    plt.savefig('year_%04d.png' % time1, bbox_inches='tight', pad_inches=0 ,dpi=200) # save-figures to frames folder , dpi=1000
       

###########################################################################################################

def update_fish():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen , fishermen_data1,  fishermen_data2, fishermen_data3    
    fish_ag = rd.sample([j for j in agents if j.type == 'fish'],1)[-1] #randomly select a fish 
    
    repulsion = [nb for nb in agents if nb.type == 'fish' and nb != fish_ag and ((fish_ag.x - nb.x)**2 + (fish_ag.y - nb.y)**2) < rad_repulsion_sqr] # fishes within the repulsion zone
    alignment = [nb for nb in agents if nb.type == 'fish' and nb != fish_ag and rad_repulsion_sqr < ((fish_ag.x - nb.x)**2 + (fish_ag.y - nb.y)**2) < rad_orientation_sqr ] # fishes within the parallel-orientation zone
    attraction =[nb for nb in agents if nb.type == 'fish' and nb != fish_ag and rad_orientation_sqr < ((fish_ag.x - nb.x)**2 + (fish_ag.y - nb.y)**2) < rad_attraction_sqr ] # fishes within the attraction zone
    
    if len(repulsion) > 0: # if fishes within repulsion zone, move away from the spot that would be the center of mass (midpoint) of all  fish within repulsion zone
        repulsion_x = mean([j.x for j in repulsion])
        repulsion_y = mean([j.y for j in repulsion])
        repulsion_1 = (math.atan2((repulsion_y - fish_ag.y), (repulsion_x - fish_ag.x)) + math.pi ) % (2 * math.pi) # if greater than  (2 * math.pi) then compute with a minus
        theta = repulsion_1
        fish_ag.x +=  move_fish*math.cos(theta)     # moves 'move_fish' step    
        fish_ag.y +=  move_fish*math.sin(theta) 
        fish_ag.x = (fish_ag.x % -Half_Length_Area) if fish_ag.x > Half_Length_Area else (fish_ag.x % Half_Length_Area) if fish_ag.x < -Half_Length_Area else fish_ag.x  # ( When fish-agent approach a border of the landscape, 
        fish_ag.y = (fish_ag.y % -Half_Length_Area) if fish_ag.y > Half_Length_Area else (fish_ag.y % Half_Length_Area) if fish_ag.y < -Half_Length_Area else fish_ag.y  # they re-enter the system at the opposite border )
    
    elif all([len(repulsion) == 0, len(alignment) > 0]):   # if fishes within parallel-orientation zone, change direction to match the average direction of all the other fish  within parallel-orientation zone     
        alignment_1 = mean([math.atan2((j.y - fish_ag.y),(j.x - fish_ag.x)) for j in alignment])
        theta = alignment_1
        fish_ag.x +=   move_fish*math.cos(theta)     # moves 'move_fish' step,  move_fish*math.cos(theta)
        fish_ag.y +=   move_fish*math.sin(theta)  
        fish_ag.x = (fish_ag.x % -Half_Length_Area) if fish_ag.x > Half_Length_Area else (fish_ag.x % Half_Length_Area) if fish_ag.x < -Half_Length_Area else fish_ag.x  # ( When fish-agent approach a border of the landscape, 
        fish_ag.y = (fish_ag.y % -Half_Length_Area) if fish_ag.y > Half_Length_Area else (fish_ag.y % Half_Length_Area) if fish_ag.y < -Half_Length_Area else fish_ag.y  # they re-enter the system at the opposite border )

    elif all([len(repulsion) == 0, len(alignment) == 0, len(attraction) > 0]): # if fishes within only the attraction zone, head towards the middle (midpoint) of the fishes in zone of attraction.   
        attraction_x = mean([j.x for j in attraction ])
        attraction_y = mean([j.y for j in attraction])
        attraction_1 = math.atan2((attraction_y - fish_ag.y), (attraction_x - fish_ag.x))
        theta = attraction_1
        fish_ag.x +=  move_fish*math.cos(theta)     # moves 'move_fish' step      
        fish_ag.y +=  move_fish*math.sin(theta) 
        fish_ag.x = (fish_ag.x % -Half_Length_Area) if fish_ag.x > Half_Length_Area else (fish_ag.x % Half_Length_Area) if fish_ag.x < -Half_Length_Area else fish_ag.x  # ( When fish-agent approach a border of the landscape, 
        fish_ag.y = (fish_ag.y % -Half_Length_Area) if fish_ag.y > Half_Length_Area else (fish_ag.y % Half_Length_Area) if fish_ag.y < -Half_Length_Area else fish_ag.y  # they re-enter the system at the opposite border )

    elif all([len(repulsion) == 0, len(alignment) == 0, len(attraction) == 0]): # if no fishes in all the zone, move in a random direction  
        theta = 2*math.pi*rd.random()  
        fish_ag.x +=  move_fish*math.cos(theta)     # moves 'move_fish' step     
        fish_ag.y +=  move_fish*math.sin(theta) 
        fish_ag.x = (fish_ag.x % -Half_Length_Area) if fish_ag.x > Half_Length_Area else (fish_ag.x % Half_Length_Area) if fish_ag.x < -Half_Length_Area else fish_ag.x  # ( When fish-agent approach a border of the landscape, 
        fish_ag.y = (fish_ag.y % -Half_Length_Area) if fish_ag.y > Half_Length_Area else (fish_ag.y % Half_Length_Area) if fish_ag.y < -Half_Length_Area else fish_ag.y  # they re-enter the system at the opposite border )
                                       
    if rd.random() < growth_prob * (1-sum([1 for j in agents if j.type == 'fish'])/float(K)):  # logistic growth of fishes
        agents.append(cp.copy(fish_ag)) # add-copy of fish agent  


###########################################################################################################

def no_mpa():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen, fishermen_data1,  fishermen_data2, fishermen_data3 
    fisherman_ag = rd.sample([j for j in agents if j.type == 'fishers'],1)[-1] # randomly sample a fisherman 
    
    fish_neighbors = [nb for nb in agents if nb.type == 'fish' and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr ] # detecting fishes in neighbourhood
    num_fish_harvest = int(round(q * fisherman_ag.effort * len(fish_neighbors))) # number of fish to be harvested based on (q*E*x), where x is number of fishes in neighborhood 
    sample_fish_harvest= rd.sample(fish_neighbors, num_fish_harvest) # randomly sampled "num_fish_harvest"  fish  in neighbourhood radius 
    for j in sample_fish_harvest:
        agents.remove(j)  # remove catch  
        fisherman_ag.harvest += 1  # add to catch of a fisherman
    
    fishers_neighbors = [[nb.harvest, nb] for nb in agents if nb.type == 'fishers' and nb != fisherman_ag and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr] # detecting fishermen in neighbourhood 
    fishers_neighbors_harvest = sorted(fishers_neighbors, key=lambda HAV: HAV[0]) # sort fishermen in neighborhood according to catch
    
    if len(fishers_neighbors_harvest) == 0: # if there exist no fisherman in neighbourhood
        theta_1 = 2*math.pi*rd.random()
        fisherman_ag.x +=  move_fishers*math.cos(theta_1) # move  'move_fishers' step in a random direction
        fisherman_ag.y +=  move_fishers*math.sin(theta_1) 
        fisherman_ag.x = -Half_Length_Area if fisherman_ag.x > Half_Length_Area else  Half_Length_Area if fisherman_ag.x < -Half_Length_Area else fisherman_ag.x
        fisherman_ag.y = -Half_Length_Area if fisherman_ag.y > Half_Length_Area else  Half_Length_Area if fisherman_ag.y < -Half_Length_Area else fisherman_ag.y
    
    elif all([len(fishers_neighbors_harvest) > 0, fishers_neighbors_harvest[-1][0] > fisherman_ag.harvest]) : # if there exist fisherman with greater catch than focal fisherman 
            deltax = fishers_neighbors_harvest[-1][-1].x - fisherman_ag.x   #move in the direction of one with greater catch than focal fisherman 
            deltay = fishers_neighbors_harvest[-1][-1].y - fisherman_ag.y 
            theta_2 = math.atan2(deltay,deltax) 
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) # move 'move_fishers' in the direction of neighbour fishermen with greatest catch
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) 
            fisherman_ag.x = -Half_Length_Area if fisherman_ag.x > Half_Length_Area else  Half_Length_Area if fisherman_ag.x < -Half_Length_Area else fisherman_ag.x
            fisherman_ag.y = -Half_Length_Area if fisherman_ag.y > Half_Length_Area else  Half_Length_Area if fisherman_ag.y < -Half_Length_Area else fisherman_ag.y
    
    else: # if all fisherman have less or equal catch relativelly  to focal fisherman
            theta_2 = 2*math.pi*rd.random()
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) # move  'move_fishers' step in a random direction
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) 
            fisherman_ag.x = -Half_Length_Area if fisherman_ag.x > Half_Length_Area else  Half_Length_Area if fisherman_ag.x < -Half_Length_Area else fisherman_ag.x
            fisherman_ag.y = -Half_Length_Area if fisherman_ag.y > Half_Length_Area else  Half_Length_Area if fisherman_ag.y < -Half_Length_Area else fisherman_ag.y
  

###########################################################################################################

def single_mpa():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen, fishermen_data1,  fishermen_data2, fishermen_data3   
    fisherman_ag = rd.sample([j for j in agents if j.type == 'fishers'],1)[-1]   #randomly select a fisherman
    
    fish_neighbors = [nb for nb in agents if nb.type == 'fish' and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr 
        and not((Xa <= nb.x <= Xb) and (Ya <= nb.y <= Yb))] # detecting fishes in neighbourhood and outside MPA
    num_fish_harvest = int(round(q * fisherman_ag.effort * len(fish_neighbors))) # number of fish catch based on (q*E*x), where x is fishes in neighborhood  and outside MPA
    sample_fish_harvest= rd.sample(fish_neighbors, num_fish_harvest) # randomly sampled "num_fish_harvest"  fishes in neighbourhood radius 
    for j in sample_fish_harvest:
        agents.remove(j)  # remove fish catch
        fisherman_ag.harvest += 1  # add to catch of fisherman
    
    fishers_neighbors = [[nb.harvest, nb] for nb in agents if nb.type =='fishers' and nb != fisherman_ag  and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr] # detecting fishermen in neighbourhood 
    fishers_neighbors_harvest = sorted(fishers_neighbors, key=lambda HAV: HAV[0]) # sort fishermen in neighborhood according to catch
    
    if len(fishers_neighbors_harvest) == 0 : # if there exist no fisherman in neighbourhood:
        theta_empt1 = 0 ; theta_empt2 = 0
        while True: 
            theta_1 = 2*math.pi*rd.random()
            fisherman_ag.x +=  move_fishers*math.cos(theta_1) - theta_empt1  # move  'move_fishers' step in a random direction
            fisherman_ag.y +=  move_fishers*math.sin(theta_1) - theta_empt2 
            theta_empt1 = move_fishers*math.cos(theta_1) ; theta_empt2 = move_fishers*math.sin(theta_1)
            if not((Xa <= fisherman_ag.x <= Xb) and (Ya <= fisherman_ag.y <= Yb)):
                fisherman_ag.x = -Half_Length_Area if fisherman_ag.x > Half_Length_Area else  Half_Length_Area if fisherman_ag.x < -Half_Length_Area else fisherman_ag.x
                fisherman_ag.y = -Half_Length_Area if fisherman_ag.y > Half_Length_Area else  Half_Length_Area if fisherman_ag.y < -Half_Length_Area else fisherman_ag.y
                break
    
    elif all([len(fishers_neighbors_harvest) > 0, fishers_neighbors_harvest[-1][0] > fisherman_ag.harvest])  : # if there exist a fisherman in neighbourhood with greatest catch than focal fisherman
        deltax = fishers_neighbors_harvest[-1][-1].x - fisherman_ag.x   #move in the direction of one with greatest catch
        deltay = fishers_neighbors_harvest[-1][-1].y - fisherman_ag.y 
        theta_2 = math.atan2(deltay,deltax) 
        if not((Xa <= (fisherman_ag.x + move_fishers*math.cos(theta_2)) <= Xb) and (Ya <= (fisherman_ag.y + move_fishers*math.sin(theta_2)) <= Yb)):  # if updating  movement does not fall in MPA
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) # move 'move_fishers' in the direction of neighbour fishermen with greatest catch 
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) 
            fisherman_ag.x = -Half_Length_Area if fisherman_ag.x > Half_Length_Area else  Half_Length_Area if fisherman_ag.x < -Half_Length_Area else fisherman_ag.x
            fisherman_ag.y = -Half_Length_Area if fisherman_ag.y > Half_Length_Area else  Half_Length_Area if fisherman_ag.y < -Half_Length_Area else fisherman_ag.y
        else:  # in case moving in this direction lands you on an MPA, move in a random direction
            theta_empt1 = 0 ; theta_empt2 = 0
            while True: 
                theta_2 = 2*math.pi*rd.random()
                fisherman_ag.x +=  move_fishers*math.cos(theta_2) - theta_empt1  # move  'move_fishers' step in a random direction
                fisherman_ag.y +=  move_fishers*math.sin(theta_2) - theta_empt2 
                theta_empt1 = move_fishers*math.cos(theta_2) ; theta_empt2 = move_fishers*math.sin(theta_2)
                if not((Xa <= fisherman_ag.x <= Xb) and (Ya <= fisherman_ag.y <= Yb)):
                    fisherman_ag.x = -Half_Length_Area if fisherman_ag.x > Half_Length_Area else  Half_Length_Area if fisherman_ag.x < -Half_Length_Area else fisherman_ag.x
                    fisherman_ag.y = -Half_Length_Area if fisherman_ag.y > Half_Length_Area else  Half_Length_Area if fisherman_ag.y < -Half_Length_Area else fisherman_ag.y
                    break
    
    else:  # if all fisherman in neighbourhood have less or equal catch compared to focal fisherman
        theta_empt1 = 0 ; theta_empt2 = 0
        while True: 
            theta_2 = 2*math.pi*rd.random()
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) - theta_empt1  # move  'move_fishers' step in a random direction
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) - theta_empt2 
            theta_empt1 = move_fishers*math.cos(theta_2) ; theta_empt2 = move_fishers*math.sin(theta_2)
            if not((Xa <= fisherman_ag.x <= Xb) and (Ya <= fisherman_ag.y <= Yb)):
                fisherman_ag.x = -Half_Length_Area if fisherman_ag.x > Half_Length_Area else  Half_Length_Area if fisherman_ag.x < -Half_Length_Area else fisherman_ag.x
                fisherman_ag.y = -Half_Length_Area if fisherman_ag.y > Half_Length_Area else  Half_Length_Area if fisherman_ag.y < -Half_Length_Area else fisherman_ag.y
                break
                            

###########################################################################################################

def spaced_mpa():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen , fishermen_data1,  fishermen_data2, fishermen_data3   
    fisherman_ag = rd.sample([j for j in agents if j.type == 'fishers'],1)[-1]    #randomly select an fisherman agent
    
    fish_neighbors = [nb for nb in agents if nb.type == 'fish' and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr and  all([not((Xm <= nb.x <= Xn) and (Ym <= nb.y <= Yn)), not((Xp <= nb.x <= Xq) and (Yp <= nb.y <= Yq))])] # detecting fishes in neighbourhood
    num_fish_harvest = int(round(q * fisherman_ag.effort * len(fish_neighbors))) # number of fish catch based on (q*E*x), where x is number of fishes in neighborhood 
    sample_fish_harvest= rd.sample(fish_neighbors, num_fish_harvest) # randomly sampled "num_fish_harvest"  fish in neighbourhood radius 
    for j in sample_fish_harvest:
        agents.remove(j)  # remove fish catch
        fisherman_ag.harvest += 1  # add to fish catch
    
    fishers_neighbors = [[nb.harvest, nb] for nb in agents if nb.type == 'fishers' and nb != fisherman_ag and ((fisherman_ag.x - nb.x)**2 + (fisherman_ag.y - nb.y)**2) < r_sqr] # detecting fishermen in neighbourhood 
    fishers_neighbors_harvest = sorted(fishers_neighbors, key=lambda HAV: HAV[0]) # sort fishermen in neighborhood according to catch
    
    if len(fishers_neighbors_harvest) == 0 : # if there are no fisherman in neighbourhood 
        theta_empt1 = 0 ; theta_empt2 = 0
        while True: 
            theta_1 = 2*math.pi*rd.random()
            fisherman_ag.x +=  move_fishers*math.cos(theta_1) - theta_empt1  # move  'move_fishers' step in a random direction
            fisherman_ag.y +=  move_fishers*math.sin(theta_1) - theta_empt2 
            theta_empt1 = move_fishers*math.cos(theta_1) ; theta_empt2 = move_fishers*math.sin(theta_1)
            if all([not((Xm <= fisherman_ag.x <= Xn) and (Ym <= fisherman_ag.y <= Yn)), not((Xp <= fisherman_ag.x <= Xq) and (Yp <= fisherman_ag.y <= Yq))]):
                    fisherman_ag.x = -Half_Length_Area if fisherman_ag.x > Half_Length_Area else  Half_Length_Area if fisherman_ag.x < -Half_Length_Area else fisherman_ag.x
                    fisherman_ag.y = -Half_Length_Area if fisherman_ag.y > Half_Length_Area else  Half_Length_Area if fisherman_ag.y < -Half_Length_Area else fisherman_ag.y
                    break
    
    elif all([len(fishers_neighbors_harvest) > 0, fishers_neighbors_harvest[-1][0] > fisherman_ag.harvest]) : # if there exist fisherman in neighbourhood with greatest catch than focal fisherman 
        deltax = fishers_neighbors_harvest[-1][-1].x - fisherman_ag.x   # move in the direction of the fisherman with greatest catch 
        deltay = fishers_neighbors_harvest[-1][-1].y - fisherman_ag.y 
        theta_2 = math.atan2(deltay,deltax) 
        if all([not((Xm <= (fisherman_ag.x + move_fishers*math.cos(theta_2)) <= Xn) and (Ym <= (fisherman_ag.y + move_fishers*math.sin(theta_2)) <= Yn)), not((Xp <= (fisherman_ag.x + move_fishers*math.cos(theta_2) <= Xq)) and (Yp <= (fisherman_ag.y + move_fishers*math.sin(theta_2)) <= Yq))]):
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) # move 'move_fishers' in the direction of neighbour fishermen with greater harvest 
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) 
            fisherman_ag.x = -Half_Length_Area if fisherman_ag.x > Half_Length_Area else  Half_Length_Area if fisherman_ag.x < -Half_Length_Area else fisherman_ag.x
            fisherman_ag.y = -Half_Length_Area if fisherman_ag.y > Half_Length_Area else  Half_Length_Area if fisherman_ag.y < -Half_Length_Area else fisherman_ag.y
        else:  # in the case this paths lands you on an MPA, move in a random direction
            theta_empt1 = 0 ; theta_empt2 = 0
            while True: 
                theta_2 = 2*math.pi*rd.random()
                fisherman_ag.x +=  move_fishers*math.cos(theta_2) - theta_empt1  # move  'move_fishers' step in a random direction
                fisherman_ag.y +=  move_fishers*math.sin(theta_2) - theta_empt2 
                theta_empt1 = move_fishers*math.cos(theta_2) ; theta_empt2 = move_fishers*math.sin(theta_2)
                if all([not((Xm <= fisherman_ag.x <= Xn) and (Ym <= fisherman_ag.y <= Yn)), not((Xp <= fisherman_ag.x <= Xq) and (Yp <= fisherman_ag.y <= Yq))]):
                    fisherman_ag.x = -Half_Length_Area if fisherman_ag.x > Half_Length_Area else  Half_Length_Area if fisherman_ag.x < -Half_Length_Area else fisherman_ag.x
                    fisherman_ag.y = -Half_Length_Area if fisherman_ag.y > Half_Length_Area else  Half_Length_Area if fisherman_ag.y < -Half_Length_Area else fisherman_ag.y
                    break
    else:  # if there exist fisherman in neighbourhood with less or equal catch compared to focal fisherman 
        theta_empt1 = 0 ; theta_empt2 = 0
        while True: 
            theta_2 = 2*math.pi*rd.random()
            fisherman_ag.x +=  move_fishers*math.cos(theta_2) - theta_empt1  # move  'move_fishers' step in a random direction
            fisherman_ag.y +=  move_fishers*math.sin(theta_2) - theta_empt2 
            theta_empt1 = move_fishers*math.cos(theta_2) ; theta_empt2 = move_fishers*math.sin(theta_2)
            if all([not((Xm <= fisherman_ag.x <= Xn) and (Ym <= fisherman_ag.y <= Yn)), not((Xp <= fisherman_ag.x <= Xq) and (Yp <= fisherman_ag.y <= Yq))]):
                fisherman_ag.x = -Half_Length_Area if fisherman_ag.x > Half_Length_Area else  Half_Length_Area if fisherman_ag.x < -Half_Length_Area else fisherman_ag.x
                fisherman_ag.y = -Half_Length_Area if fisherman_ag.y > Half_Length_Area else  Half_Length_Area if fisherman_ag.y < -Half_Length_Area else fisherman_ag.y
                break
   
###########################################################################################################

def update_one_unit_time():
    
    global time1, agents, fish, fish_data, fish_data_MPA, total_hav_data, current_hav_data, fishermen, fishermen_data1,  fishermen_data2, fishermen_data3  
    time1 += 1  # update time
    time2.append(time1)
    
    t = 0.
    while t < 1. and sum([1 for j in agents if j.type == 'fish']) > 0:
        t += 1. / len(fish)  # we assume a 1 / (number of fishes) time passes by per time. 
        update_fish()       # thus on-average each fish agent is updated once per time.
        
    
    if (MPA == 'no'): # no MPA is required throughout entire simulation
        t = 0.
        while t < 1. :   
            t += 1. / len(fishermen)  # we assume a 1 / (number of fishermen) time passes by per time
            no_mpa()        # thus on-average each fish agent is updated once per time.
        fish_data_MPA.append(0) # append a zero since no MPA is required
       
    
    elif (MPA == 'yes') : #  MPA is required throughout entire simulation
        if Type_MPA == 'single' :
            t = 0.
            while t < 1. :  
                t += 1. / len(fishermen)  # we assume a 1 / (number of fishermen) time passes by per time
                single_mpa()        # thus on-average each fish agent is updated once per time.
            fish_data_MPA.append(sum([1 for j in agents if j.type == 'fish' and ((Xa <= j.x <= Xb) and (Ya <= j.y <= Yb))])) #  fishes in MPA
        
        elif Type_MPA == 'spaced' :
            t = 0.
            while t < 1. :   
                t += 1. / len(fishermen)  # we assume a 1 / (number of fishermen) time passes by per time
                spaced_mpa()        # thus on-average each fish agent is updated once per time.
            fish_data_MPA.append(sum([1 for j in agents if j.type == 'fish' and any([((Xm <= j.x <= Xn) and (Ym <= j.y <= Yn)), ((Xp <= j.x <= Xq) and (Yp <= j.y <= Yq))])])) #  fish biomass in MPA

            
    # Preparation of data
    fish_data.append(sum([1 for j in agents if j.type == 'fish']))   # total fishes
    all_fishers = [[j.num, j.harvest] for j in agents if j.type =='fishers'] # fishermen 
    for j in all_fishers:
        total_hav_data[j[0]].append(j[-1])  # append each fishermans total catch to dictionary 'total_hav_data' based on its cooperative-trait
        current_hav_data[j[0]].append(total_hav_data[j[0]][-1] - total_hav_data[j[0]][-2])  # append each fishermans current catch to dictionary 'current_hav_data'
    
    fishermen_data1.append(sum([j.harvest for j in agents if j.type == 'fishers']))   # total  catch 
    fishermen_data2.append(fishermen_data1[-1] - fishermen_data1[-2])   # current catch 
    fishermen_data3.append(fish_data[-1] - fish_data_MPA[-1]) # fishes outside MPA
   
    csvfile = "simulation_data.csv"   # a csv-file output 
    #header = [key for key in sorted(current_hav_data)]
    header= []
    header.append('time')
    header.append('total_catch')  
    header.append('total_biomass') 
    header.append('biomass_inside_MPA') 
    header.append('biomass_outside_MPA')
    
    #main_data = [current_hav_data[key] for key in sorted(current_hav_data)]
    main_data = []
    main_data.append(time2)
    main_data.append(fishermen_data2) 
    main_data.append(fish_data) 
    main_data.append(fish_data_MPA) 
    main_data.append(fishermen_data3)
    with open(csvfile, "w") as output:
        writer = csv.writer(output) 
        writer.writerow(header)
        writer.writerows(zip(*main_data))

###########################################################################################################





