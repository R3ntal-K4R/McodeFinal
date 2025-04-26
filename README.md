# MISSFIT mechnical Simulation

## Simulation Paramaters and Constants
Constants.txt


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
