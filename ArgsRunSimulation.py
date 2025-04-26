
import argparse
from functions import *
from readConstants import read_constants

def run_simulation(constants, M, V_y): # Takes Mass as argument
    """Runs a single simulation for a given  Mass, initial v_y, returns energy loss.
        """
    # Extract constants
    N_springs = constants['N_springs']
    dx = constants['dx']
    m = constants['m']
    k = constants['k']
    V_X = 0 
    X = constants['X_projectile_start']
    Y = constants['Y_projectile_start']
    R = constants['R']
    dt = constants['dt']
    timesteps = constants['timesteps']
    epsilon = constants['epsilon']


    # Initialize simulation components
    springs = init_springs(N_springs, dx, k, m)
    # Use M_initial for the projectile mass
    projectile = Projectile(M, V_X, V_y, X, Y, R)

    # Calculate initial energy
    initial_energy = projectile.getEnergy()

    # --- Simulation Loop  ---
    for i in range(timesteps):
        total_force_on_projectile = np.array([0.0, 0.0])
        forces_on_springs = [np.array([0.0, 0.0]) for _ in springs]

        for idx, spring in enumerate(springs):
            if is_touching(spring, projectile, epsilon):
                proj_bottom_y = projectile.Y_pos_at_X(spring.X)
                if proj_bottom_y != float('inf'):
                    compression_depth = spring.Y - proj_bottom_y
                    if compression_depth >= -epsilon:
                        force_y_on_proj = spring.k * max(0, compression_depth)
                        force_x_on_proj = 0.0
                        force_spring_on_proj = np.array([force_x_on_proj, force_y_on_proj])
                        total_force_on_projectile += force_spring_on_proj
                        forces_on_springs[idx] = -force_spring_on_proj

        projectile.update(total_force_on_projectile[0], total_force_on_projectile[1], dt)

        for idx, spring in enumerate(springs):
            internal_force_y = spring.get_F_Y()
            internal_force_x = spring.get_F_X()
            external_force = forces_on_springs[idx]
            net_force_x = internal_force_x + external_force[0]
            net_force_y = internal_force_y + external_force[1]
            spring.update(net_force_x, net_force_y, dt)
    # --- End Simulation Loop ---

    final_energy = projectile.getEnergy()
    energy_loss = initial_energy - final_energy

    return energy_loss

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