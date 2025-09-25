import matplotlib.pyplot as plt
import datetime
import sys 

def plotter(x,y, xlabel=None, ylabel = None,  title = None):
    if xlabel is None:
        xlabel = "x"
    if ylabel is None:
        ylabel = "y"
    if zlabel is None:
        zlabel = "z"
    if title is None:
        title = f"{xlabel} vs. {ylabel} Linear Scale"

    plt.figure(figsize=(10, 6))

    plt.plot(x, y, marker='o', linestyle='-', color='green', label='Simulation Results')

    

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title) 

    # --- MODIFICATION: REMOVED log scale setting ---
    # plt.xscale('log') # Removed this line

    # --- MODIFICATION: Adjusted grid for linear scale ---
    plt.grid(True, which='major', linestyle='--', alpha=0.6) # Changed 'both' to 'major'

    plt.legend()

    now = datetime.datetime.now().strftime("%H:%M:%S")

    #more testing, because git is important
    plot_filename = f'{title}_{now}.png' # Updated filename
    try:
        plt.savefig(plot_filename)
        print(f"Plot successfully saved to '{plot_filename}' at {now}")
    except Exception as e:
        print(f"Error saving plot to '{plot_filename}': {e}", file=sys.stderr)

    plt.show()