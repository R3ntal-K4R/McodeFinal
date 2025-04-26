# MISSFIT mechnical Simulation


## Plotters
they don't work

## Simulation Paramaters and Constants
1.Constants.txt
2.MVTParams.txt

so we are simulating a wall of springs for a given material and a pojectile, hitting the wall hard, 

1. constants.txt
this is the material constants, the one you need to make more of, this one is default steel, but you need add another one based off of the calculations of the equation given by Dr. Petritris

material_name = Steel
m=0.0000000058875 # Mass per spring element (kg)
k=175.0           # Spring constant per element (N/m) - CORRECTED based on calculation

there are the only constants that you need to change

2. MVTParams.txt
I'm bad at naming so at this point I don't know why I named like this. 
this is the Paramers of the entire simulation, for ranges of Mass and Velocity and how many data points that you want to collect. 

the data point should be a squre 

3. materialSummary.csv
Material,Young's Modulus,Melting Point,Specific Heat
it's a table of contents



## Simulation scripts
we have the following 3 scripts that handles the simulation
1. ArgsRunSimulation.py
2. singleSimulation.py
3. runSim.py

I know these names are very similar and it can be confusing, I'm bad at naming and sleep deprvation doesn't help, let me explain:

### ArgsRunSimulation.py
this file provides the entirity for one single impact simulation, and enclased with argument paramter flags to run the program with such as "--vy", "--mass" and "--constants". 

### singleSimulation.py
this file calles ArgsRunSimulation with input flag constants values, and runs the simulation once, also has the time decotor on it to record time for each simulation.
very unnecessary code

### runSim.py
the most important one, and this is the one you will be directly interface with this scipt calls singleSimulation.py with given paramers and run it a lot of times, to run it use
`python3 runSim.py -mc <material_constant.txt>`
the `-mc` flag stands for material constants, and when you put in the file name don't type the brackets
at the end outputs a csv contains 3D infomation, containing all possible combaintaions of given mass and v_y 


## OutputData
outputed data in format
you need to plot this


