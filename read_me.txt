Downloads for DER Optimizer Functionality

Step 1: Python Install
1.	Visit official Site:
-	https://www.python.org/downloads/
2.	Download the latest Python 13.x installer (Our Team used 3.12.3)
3.	Check the box that says “Add Python to PATH” during installation
Step 2: Set Up a Virtual Environment (Recommended)
1.	Open Command Prompt or Terminal and type:
-	python -m venv env
-	env\Scripts\activate
-	source env/bin/activate
Step 3: Install Required python packages
1.	Open Command Prompt or Terminal and type
-	pip install requests pandas numpy matplotlib
Step 4: Install and Set Up Gurobi Optimizer
1.	Create an account at:
-	https://www.gurobi.com
2.	Download and install Gurobi for your OS:
-	https://www.gurobi.com/downloads/
3.	Install the Python interface:
-	pip install gurobipy
-      grbgetkey <your-license-key>

All pip installations are copied below:
- pip install tkinter
- pip install csv
- pip install datetime
- pip install requests
- pip install matplotlib
- pip install pandas
- pip install gurobipy
- pip install numpy
- pip install time


File Descriptions:

GUI_Main: 
    This file is the main GUI program that needs to be ran to access the GUI.
    The program creates sections for each of the input boxes and seperates the 
    GUI into sectional frames.

Location_Input:
    This file is used to create the location section and creates the option for 
    the user to select between city entry and coordinate entry. The actual location
    API and logic are located in the Calculate function as the location isn't saved
    until the calculate button is pressed.

Load_Input:
    This file creates and populates the location frame, as well as saves the load data
    and grid rate the the config file to be used later in the optimization process.

Objectives:
    This file creates the weighted objective box for the renewable and cost objectives.
    The user is prompted to move the sliders to the weight they want, and then save the 
    values after changing the sliders. The default value is 50 for both sliders. The sliders
    have built in logic to always add up to 100 so the weight will never be off. 
    Once saved, the weighted objectives will be saved to the config file and used in the 
    optimization program.

DERs:
    This file first creates the input box where the user can select the desired 
    DERs to be used in the configuration. The user can also select a maximum amount of
    PVs and turbines. Once selected, the user pressses the confirm selection that is 
    included at the end of the show selected function, and the selected DERs will pop
    up on the right side of the GUI. Each DER has its own variable names used to calculate
    power and identify optimized results. The user can either choose from pre-exsiting 
    PVs or Wind Turbines, which will automatically save the configuration to the config file,
    or they can enter their own, with each desired configuration saved to the config file
    one the save button is pressed. 

config:
    This file acts as an active data dictionary to store all the user specified data
    to be accessed in each file within the program instead of sending the same values to 
    each function, the program will just pull from the config file by importing it in the 
    top of the program. The PV and wind data dict arrays store each configuration entered
    so that each configuration is stored in each section of the array. The pv and wind counters
    are then used to cycle through the data dictionary arrays so that when the configurations
    are used to calculate power, each individual DER will have its own data output, with
    the program looping for the number of times the counter has been increased. 
    The existing PV and turbine configurations are stored in a similiar format as the data 
    dictionaries, however they are only passed to the dictionaries if selected in the DER program.
    The load demand section stores each load in a 12 wide array for each corresponding month.
    The rest of the variables are set to default values that are updated if the program enters
    new values. The dictionary transfer is a very large array that is used at the end of the 
    optimization funtion to store the optimized values for the final output in the calculate page

Calculate:
    This file is the second largest program in the system, with a wide assortment of functions
    called after the calculate button from the GUI_main program is pressed. First, the location 
    API will be called if the city option is selected and save the corresponding coordinates to
    the config file. Next, the user will be prompted to enter a project name so the data outputs
    can be saved. If the user does not enter a name, the project will be saved under the default 
    project name in the config file. Regardless if a name is entered or not, the output data files
    will be saved to a timestamped folder in the designated location so that multiple outputs can be
    saved to the project. The program will then call the perform_calculations function, which will
    use the location data and DER configurations to call the wind and PV functions to calculate 
    the hourly power generated over a typical meteorological year. This data will be saved in individual 
    CSV files in the project folder for each DER configuration. Once each file is saved, the function will
    call the optimization function, which performs the actual optimization of the system, and will then
    receive the configurations saved to the dictionary_transfer array mentioned previously. 
    After the optimized configurations are saved, the open_results_window function is called 
    to display the optimized results. The frames are first configured, then the left side of the 
    results window is populated with the relevent data split into configuration, cost, and power data.
    The calculations to identify these values are performed in the optimization file.
    The right side of the screen is then populated with the monthly average power output graph, 
    which displays the annual power of the DERs and grid over a year. The user can then select 3 different graphs,
    with each graph using either the output CSV data for annual data or the average data passed by the 
    optimization function.

solar_PV_csv_save:
    This file takes the user PV data and calls the PV watts API to return the various hourly values
    the API is capable of calculating based on the location and solar irradiance. The API is called
    for each iteration and saves the files to the project folder.

Wind_csv_save
    This file uses the NASA LARC wind data API to first identify the wind power available in the
    entered location. After this data is returned, the program calculates the available hourly wind turbine
    power in kW-AC and adds a column to the API csv for each turbine configuration. The power is calculated
    through a typical turbine power calcualtion using the efficiency, wind speed, rotor diameter and air density.

gurobi_multi_objective:
    This file is the brains behind the GUI, using the Gurobi MILP optimizer with the DER configurations
    and calculated annual power with the weighted objectives to optimize the system. 
    The function first sets each variable used in the config file to be used easily in the function.
    After initialization, the individual DER power files are combined into a single file called power_data.
    The optimization model is the initialized with decision variables with data type specified as binary
    or integers. Logic is then applied to ensure that if a pv or turbine is selected, the program will only
    use one of the user configurations in the final output after optimizing the best configuration. 
    The program also makes sure that the number of pvs or turbines does not exceed the maximum.
    The constraint section is then used to identify the total available power from the hourly datasets
    for the optimized pv and turbine. The load balance constraint ensures that the load will only be supplied
    with DER power when power is available. This primarily was included for the pvs, as solar energy is only available
    for portions of the day. The objective function is then used to determine the hourly cost over a year for 
    each DER and grid used. The total cost and renewable production variables are then determined by adding
    the total levelized costs together and adding the DER power together. The program then 
    optimizes the model to identify the maximum and minimum total cost and total renewable power production.
    The values returned are then used in normalize cost and renewable functions, which set the normalized 
    value to be on the same scale between 1 and 0. After this is complete, the model can succesfuly optimize
    the final output by multiplying the objective weights with the normalized values and maximizing the model.
    The normalized renewable value is able to be maximized as the minimum value is subtracted from the 
    optimized renewable value, opposed to the cost where the optimized cost value is subtracted from the maximum
    cost. Once the model is solved, the data is saved to a final output CSV, with calculations for the 
    various values used in the output window. The program also has logic built in so that 
    only one DER can be selected and the model will still optimize based on the configurations.

