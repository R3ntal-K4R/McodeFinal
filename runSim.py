import numpy as np
import matplotlib.pyplot as plt
from singleSimulation import run_single_simulation
from plotters.plotter import plotter
from plotters.threeDplotter import threeDPlotter 
import os
import argparse
#also argrunsim in here
from getTemp import getTemp, readSpecificHeat
from readConstants import read_constants

def read_params(fileName):
    constants = {}
    with open(fileName, 'r') as file:
        for line in file:
            # Remove comments
            line = line.split('#')[0].strip()
            if not line:
                continue
            # Parse key and value
            key, value = map(str.strip, line.split('='))
            try:
                value = float(value) if '.' in value or 'e' in value.lower() else int(value)
            except ValueError:
                pass  # Leave as string if it's not a number
            constants[key] = value
    return constants

def main():
    parser = argparse.ArgumentParser(description="Run the simulation with a constants file.")
    parser.add_argument('-mc', type=str, required = True, help='Path to the material constants file')

    args = parser.parse_args()
    print(args)
    # --- Configuration ---
    simulation_script_name = 'ArgsRunSimulation.py'
    constants_file_name = args.mc
    params_files_name = 'MVTparams.txt'


    # read params
    params = read_params(params_files_name)
    print(params)
    mass_start = params['mass_start'] # kg
    mass_end = params['mass_end']     # kg
    num_points = params['num_points']      # Number of simulation runs
    vy_start = params['vy_start']  #m/s
    vy_end = params['vy_end']  # m/s 
    

    vy_value_to_test = np.linspace(vy_start, vy_end, num_points) # spacer
    mass_values_to_test = np.linspace(mass_start, mass_end, num_points) # Use linspace for linear scale
    


    # --- Run Simulations & Collect Data ---
    results_mass = []
    results_vy = []
    results_energy_loss_raw = []
    results_max_displacement_raw = []
    results_temp_change_raw = []

    print(f"Starting simulations using '{simulation_script_name}'...")
    print(f"Testing {num_points} Mass values from {mass_start:.2e} to {mass_end:.2e} kg (Linear Scale).\n"
          f"Vy_value from {vy_start} to {vy_end}") # Updated message
    # print(f"Ensure '{constants_file_name}' contains a fixed 'V_Y_initial'.")
    constants = read_constants(constants_file_name)
    material_name = constants['material_name']
    material_specific_heat = readSpecificHeat(material_name)

    for vy in vy_value_to_test:

        for mass in mass_values_to_test:
            energy_loss,max_displacement = run_single_simulation(mass, vy, constants_file_name, simulation_script_name)

            if energy_loss or max_displacement is not None:
                results_mass.append(mass)
                results_vy.append(vy)
                results_energy_loss_raw.append(energy_loss)
                results_max_displacement_raw.append(max_displacement)
                results_temp_change_raw.append(getTemp(material_specific_heat, mass, energy_loss))

            else:
                print(f"  Skipping Mass = {mass:.4e} V_y = {vy:.4e} due to simulation error.")

    # --- Data Processing for Plotting ---
    results_mass_np = np.array(results_mass)
    results_v_y_np = np.array(results_vy)
    print(results_v_y_np)
    results_energy_loss_raw_np = np.array(results_energy_loss_raw)
    results_energy_loss_magnitude = np.abs(results_energy_loss_raw_np)
    results_max_displacement = np.abs(np.array(results_max_displacement_raw))
    results_temp_change = np.abs(np.array(results_temp_change_raw))

    # --- Data Saving ----
    

    # --- Plotting ---
    if not results_mass_np.size:
        print("\nNo simulation results collected successfully. Cannot generate plot.")
        return
    else:
        print(f"\nCollected {len(results_mass_np)}, {len(results_v_y_np)} results. Generating CSV...")
        points = np.column_stack((results_mass_np,results_v_y_np,results_energy_loss_magnitude,results_max_displacement,results_temp_change))
        title = (f"Vy[{vy_start:.2e}-{vy_start:.2e}]|M[{mass_start:.2e}-{mass_start:.2e}]|num[{num_points}]")
        np.savetxt(f"./OutputData/{title}.csv", points, delimiter=",", header="mass,v_y,Eloss,Dmax,dT", comments='')
        print(f"\nCollected {len(results_mass_np)}, {len(results_v_y_np)} results. Generating plot...")
        # plotter(results_mass_np,results_energy_loss_magnitude)
        print(len(results_mass_np),len(results_v_y_np), len(results_energy_loss_magnitude),len(results_max_displacement))
        threeDPlotter(results_mass_np,results_v_y_np,results_energy_loss_magnitude)
        threeDPlotter(results_mass_np,results_v_y_np,results_max_displacement)



if __name__ == "__main__":
    main()