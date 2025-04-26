import subprocess
import os
import sys
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def run_single_simulation(mass_value,vy_value,constants_file='constants.txt', simulation_script='SPsimulation_mass.py'):
    """
    Runs the simulation script SPsimulation_mass.py for a given projectile mass (M)
    and returns the calculated energy loss.
    """
    if not os.path.exists(simulation_script):
        print(f"Error: Simulation script '{simulation_script}' not found.", file=sys.stderr)
        return None
    if not os.path.exists(constants_file):
        print(f"Error: Constants file '{constants_file}' not found.", file=sys.stderr)
        return None

    python_executable = sys.executable
    command = [
        python_executable,
        simulation_script,
        '--vy', str(vy_value),
        '--mass', str(mass_value),
        '--constants', constants_file
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=300
        )
        energy_loss, max_displacement = map(float, result.stdout.strip().split(','))
        print(f"  Successfully ran for Mass = {mass_value:<10.4e}, Vy = {vy_value: <10.4e} -> Energy Loss = {energy_loss:.4e}, Max Displacement = {max_displacement:.4e}")
        return energy_loss, max_displacement

    except subprocess.CalledProcessError as e:
        print(f"Error running simulation for Mass = {mass_value},Vy = {vy_value} : Process failed.", file=sys.stderr)
        print(f"  Command : {' '.join(e.cmd)}", file=sys.stderr)
        print(f"  Exit Code: {e.returncode}", file=sys.stderr)
        if e.stderr: print(f"  Stderr  :\n{e.stderr.strip()}", file=sys.stderr)
        if e.stdout: print(f"  Stdout  :\n{e.stdout.strip()}", file=sys.stderr)
        return None
    except ValueError:
        print(f"Error parsing energy loss for Mass = {mass_value} or Vy = {vy_value}. Unexpected output.", file=sys.stderr)
        if 'result' in locals() and hasattr(result, 'stdout') and result.stdout:
             print(f"  Stdout received:\n{result.stdout.strip()}", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print(f"Error: Simulation timed out for Mass = {mass_value} Vy = {vy_value}(limit: 300s)", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred while running simulation for Mass = {mass_value} Vy = {vy_value}: {e}", file=sys.stderr)
        return None