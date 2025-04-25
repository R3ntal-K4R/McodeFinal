
import argparse
from functions import *
from readConstants import read_constants
from interactionUpdateLoop import run_simulation

def main():
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Run spring collision simulation for a single projectile MASS.")
    # --vy and --mass --constants as arguments
    parser.add_argument('--vy', type=float, required=True,
                        help='Initial vy(m/s) for the projectile (kg).')
    parser.add_argument('--mass', type=float, required=True,
                        help='Initial mass (M) for the projectile (kg).')
    parser.add_argument('--constants', type=str, default='constants.txt',
                        help='Path to the constants file (default: constants.txt).')
    args = parser.parse_args()
    # --- End Argument Parsing ---

    constants = read_constants(args.constants)
    # Get the single mass value from command line
    mass_val = args.mass
    vy_val = args.vy
    # Run simulation for the single mass provided
    energy_loss = run_simulation(constants, mass_val,vy_val) # Pass mass to simulation

    # Output *only* the energy loss
    print(f"{energy_loss}")
  
    # Optional status message to stderr
    # print(f"Sim Mass={mass_val:.4e} kg -> E_loss={energy_loss:.6e}", file=sys.stderr)


if __name__ == "__main__":
    main()