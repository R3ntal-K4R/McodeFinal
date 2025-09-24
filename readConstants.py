import sys

def read_constants(filename="constants.txt"):
    """Reads constants from a specified file, handling inline comments."""
    constants = {}
    #makes a dict
    try:
    #its try because the file might not exist
        with open(filename, 'r') as f:
            for line in f:
                line = line.split('#', 1)[0].strip() # Remove comments and strip
                #remove all comment lines
                if line and '=' in line:
                    try:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        try: constants[key] = int(value)
                        except ValueError:
                            try: constants[key] = float(value)
                            except ValueError: constants[key] = value
                    except ValueError:
                        print(f"Warning: Skipping malformed line in {filename}: {line}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: Constants file '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading constants file '{filename}': {e}", file=sys.stderr)
        sys.exit(1)

    # Define required keys FOR THIS SCRIPT (needs V_Y_initial, M is from args)
    required_keys = ['material_name','N_springs', 'dx', 'm', 'k', 'V_X_projectile',
                     'X_projectile_start', 'Y_projectile_start', 'R', 'dt',
                     'timesteps', 'epsilon'] # Added V_Y_initial
    missing_keys = [key for key in required_keys if key not in constants]
    if missing_keys:
        print(f"Error: Missing required constants in '{filename}': {', '.join(missing_keys)}", file=sys.stderr)
        print("Ensure 'V_Y_initial' is defined in constants.txt for this script.", file=sys.stderr)
        sys.exit(1)

    # Convert types explicitly after loading
    try:
        constants['material_name'] = str(constants['material_name'])
        constants['N_springs'] = int(constants['N_springs'])
        constants['dx'] = float(constants['dx'])
        constants['m'] = float(constants['m'])
        constants['k'] = float(constants['k'])
        # constants['V_X_projectile'] = float(constants['V_X_projectile'])
        constants['X_projectile_start'] = float(constants['X_projectile_start'])
        constants['Y_projectile_start'] = float(constants['Y_projectile_start'])
        # constants['V_Y_initial'] = float(constants['V_Y_initial']) # Ensure V_Y is float
        constants['R'] = float(constants['R'])
        constants['dt'] = float(constants['dt'])
        constants['timesteps'] = int(constants['timesteps'])
        constants['epsilon'] = float(constants['epsilon'])
    except ValueError as e:
        print(f"Error: Invalid numeric value for a constant: {e}", file=sys.stderr)
        sys.exit(1)

    return constants