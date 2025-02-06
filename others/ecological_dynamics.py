# Ecological Dynamics Simulation: Algae, Corals, and Herbivores
#
# This script simulates the interactions between algae, corals, and herbivores in a marine ecosystem using a system of ODEs.
# It models the dynamics of these populations over time based on growth and mortality rates, herbivore pressure on algae, 
# and the influence of algae on coral health.

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# Model parameters
G_algae = 0.1  # Algae growth rate
C_herbivores = 0.05  # Algae consumption coefficient by herbivores
R_corals = 0.1  # Coral growth rate
r_herbivores = 0.1  # Herbivore growth rate
d_herbivores = 0.05  # Herbivore mortality rate

def model(y, t, G_algae, C_herbivores, R_corals, r_herbivores, d_herbivores):
    A, S_corals, P_herbivores = y
    # Rate of change of algae abundance
    dA_dt = G_algae - C_herbivores * P_herbivores * A
    # Herbivore pressure on corals
    herbivore_pressure = 0.05 * P_herbivores
    # Rate of change of coral health
    dS_corals_dt = R_corals * A - herbivore_pressure
    # Rate of change of herbivore population
    dP_herbivores_dt = r_herbivores * P_herbivores * A - d_herbivores * P_herbivores
    return [dA_dt, dS_corals_dt, dP_herbivores_dt]

# Initial conditions: algae (A), coral health (S), herbivore population (P)
A0, S0, P0 = 0.5, 1.0, 50
y0 = [A0, S0, P0]

# Simulation time (100 time units, with 1001 points)
t = np.linspace(0, 100, 1001)

# Parameters to pass to the function
params = (G_algae, C_herbivores, R_corals, r_herbivores, d_herbivores)

# Solve the system of ODEs
solution = odeint(model, y0, t, args=params)

# Extract results for each population
A, S_corals, P_herbivores = solution[:, 0], solution[:, 1], solution[:, 2]

# Plot the results
plt.figure(figsize=(15, 6))

# Subplot for algae abundance
plt.subplot(1, 3, 1)
plt.plot(t, A, color='green',label='Algae Abundance', linewidth=4)
plt.xlabel('Time [days]', fontweight='bold')
plt.ylabel('Algae Abundance A', fontweight='bold')

plt.xlim([0,100])
# plt.title('Algae Dynamics')
plt.legend()
plt.grid(True)

# Subplot for coral health
plt.subplot(1, 3, 2)
plt.plot(t, S_corals, color='blue',label='Coral Health Evolution', linewidth=4)
plt.xlabel('Time [days]', fontweight='bold')
plt.ylabel('Coral Health S', fontweight='bold')
plt.xlim([0,100])
# plt.title('Coral Health Evolution')
plt.legend()
plt.grid(True)

# Subplot for herbivore population
plt.subplot(1, 3, 3)
plt.plot(t, P_herbivores, color='orange',label='Herbivore Population', linewidth=4)
plt.xlabel('Time [days]', fontweight='bold')
plt.ylabel('Herbivore Population P' , fontweight='bold')
plt.xlim([0,100])
# plt.title('Herbivore Dynamics')
plt.legend()
plt.grid(True)

# Save and Show the plot
plt.savefig('ecological_dynamics_plot.png')
plt.show()

