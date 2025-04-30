# config.py
#This is where all global variables will be stored, access these variables by importing this file at the top of your code, and using config.(variable_name) to access the variable.

# Dictionary to store PV data (name, capacity, lifespan, efficiency, module type, cost)
pv_data_dict = {
    
}  

# Dictionary to store Generic PV data (name, capacity, lifespan, efficiency, module type, cost)
pv_data_existing_configurations = {
    0: ["LONGi-Hi-MO-6", 435, 25, 22, "Monocrystalline", 550], 
    1: ["First-Solar-Series-7", 510, 30, 18, "Thin-Film", 450],
    2: ["Canadian-Solar-HiKu-7", 665, 25, 21.4, "Monocrystalline", 450]
} 

pv_lifespan = 15  # Lifespan of PV modules in years
pv_counter = 1 # Counter for PV modules

# Dictionary to store Wind data (name, capacity, lifespan, efficiency, hub height, rotor diameter, cost)
wind_data_dict = {
    
}  

# Dictionary to store Genertic Wind data (name, capacity, lifespan, efficiency, hub height, rotor diameter, cost)
wind_data_existing_configurations = {
    0: ["GE-2.8-127", 2800, 27, 45, 100, 127, 1600],
    1: ["Siemens-Gamesa-SG-6.6-55", 6600, 25, 50, 100, 155, 1400],
    2: ["Vestas-V150-4.2", 4200, 28, 47, 100, 150, 1500]
}

wind_counter = 1 # Counter for Wind turbines
wind_lifespan = 20  # Lifespan of wind turbines in years

battery_data_dict = {}  # Dictionary to store Battery data

# Initialize an empty list to store configurations
project_name = "Default_project"  # Default project name
timestamped_folder = None


# load demand array (jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec)
#load_demand = [10000, 12000, 20000, 25000, 32000, 38000, 40000, 35000, 28000, 14000, 12000, 11000 ]  # Large scale load demand in kWh
load_demand = [1500, 2200, 3000, 3800, 4300, 5200, 6700, 7300, 6400, 5800, 4600, 3100 ] # Small scale load demand in kWh
#load_demand = [4000, 5500, 7000, 9000, 11000, 12500, 14000, 11000, 7500, 6800, 5700, 3600]
#load_demand = {}
grid_rate = 0.01  # Default grid rate


# DER Maximums
turbine_max = 4 # Default maximum number of wind turbines
PV_max = 1000 # Default maximum number of PV modules

# Objective Weights
cost_weight = 50
renewable_weight = 50

# Dictionary to store the transfer of data between pages
dictionary_transfer = {} 