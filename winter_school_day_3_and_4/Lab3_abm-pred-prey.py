import numpy as np
import matplotlib.pyplot as plt
import copy as cp


#################################
#####  PARAMETERS   #####
#################################

carrying_cap = 500.0    # carrying capacity of rabbits

rabbits_init = 100  # initial rabbit population
moveradius_r = 0.03     # magnitude of movement of rabbits
death_r = 1.0      # death rate of rabbits when it faces foxes 
repro_r = 0.1      # reproduction rate of rabbits

foxes_init = 30   # initial fox population
moveradius_f = 0.07     # magnitude of movement of foxes
death_f = 0.1     # 0.1 death rate of foxes when there is no food
repro_f = 0.5      # reproduction rate of foxes

hunt_radius = 0.04     # radius for collision detection

# OUTCOME VARIABLES
# lists to store the rabbit/fox population over time
rabbit_pop = []
fox_pop = []



#################################
#####  AGENT CLASS   #####
#################################

class agent:
    pass

def initialize():
    global agents
    agents = []
    # initialize the rabbits
    for i in range(rabbits_init):
       ag = agent()
       ag.type = 'rabbit'
       ag.x = np.random.random()
       ag.y = np.random.random()
       agents.append(ag)

    # initialize the foxes
    for i in range(foxes_init):
       ag = agent()
       ag.type = 'fox'
       ag.x = np.random.random()
       ag.y = np.random.random()
       agents.append(ag)
    return 


#################################
#####  UPDATING   #####
#################################

def update_one_agent():
    global agents

    if agents == []:
       return

    # choose a random agent
    ag = agents[np.random.randint(len(agents))]

    # simulating random movement
    move_radius = moveradius_r if ag.type == 'r' else moveradius_f
    ag.x = ag.x + np.random.uniform(-move_radius, move_radius)
    ag.y = ag.y + np.random.uniform(-move_radius, move_radius)
    
    # ensure that agents do not leave the environment.
    ag.x = np.clip(ag.x, 0, 1)
    ag.y = np.clip(ag.y, 0, 1)
    # detecting collision and simulating death or birth
    
    neighbors = []
    for ag2 in agents:
        if (ag2.type != ag.type) and ((ag.x - ag2.x)**2 + (ag.y - ag2.y)**2 < hunt_radius**2):
            neighbors.append(ag2)

    if ag.type == 'rabbit':
        if len(neighbors) > 0: # if there are foxes nearby, die with probability death_r
           if np.random.random() < death_r:
              agents.remove(ag)
              return
        # logistic growth
        rabbit_pop = len([ag for ag in agents if ag.type=="rabbit"])
        if np.random.random() < repro_r*(1 - rabbit_pop/carrying_cap):
           agents.append(cp.copy(ag))
    else:
        if len(neighbors) == 0: # if there are no rabbits nearby, die with probability death_f
           if np.random.random() < death_f:
              agents.remove(ag)
              return
        else: # if there are rabbits nearby, reproduce
           if np.random.random() < repro_f:
              agents.append(cp.copy(ag))
    return 
                

def updaet_one_time_step():
    global agents
    for i in range(len(agents)):
        update_one_agent()



#################################
#####  OBSERVING   #####
#################################

def observe():
    global agents, rabbit_pop, fox_pop

    # count foxes at current time t
    foxes = [ag for ag in agents if ag.type == 'fox']
    fox_pop.append(len(foxes))

    # count rabbits at current time t
    rabbits = [ag for ag in agents if ag.type == 'rabbit']
    rabbit_pop.append(len(rabbits))

    fig, axs = plt.subplots(2,1)

    axs[0].set_title('Time ' + str(t), fontsize=16)
    
    # 1. plot foxes and rabbits as dots on our map
    # Plot the rabbits 
    if len(rabbits) > 0:
       x = [ag.x for ag in rabbits]
       y = [ag.y for ag in rabbits]
       axs[0].plot(x, y, '.', color="blue")

    # Plot the foxes
    if len(foxes) > 0:
        x = [ag.x for ag in foxes]
        y = [ag.y for ag in foxes]
        axs[0].plot(x, y, 'o', color="red")
    axs[0].set_xlim(0,1)
    axs[0].set_ylim(0,1)
    axs[0].set_aspect("equal") # this ensures that x and y axis have the same units

    # 2. plot the number of foxes and rabbits over time (from time 0 to t)
    axs[1].plot(range(t+1), fox_pop, color="r", label="foxes")
    axs[1].plot(range(t+1), rabbit_pop, color="b", label="rabbits")
    axs[1].legend(loc="upper right")
    axs[1].set_xlim(0, T)
    axs[1].set_ylim(0,550)

    plt.savefig('figs/' + str(t) + '.png', bbox_inches='tight', pad_inches=0)
    plt.close()
    return 


#################################
#####  SIMULATE   #####
#################################
t=0
T = 501

np.random.seed(2025)
initialize()
observe()

for t in range(1, T):
    print(t)
    updaet_one_time_step()
    observe()
