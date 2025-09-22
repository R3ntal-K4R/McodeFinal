import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Not strictly needed in latest matplotlib, but safe to include


def threeDPlotter(x, y, z, xlab="X-axis", ylab="Y-axis", zlab="Z-axis"):
  """
    by triangulation of points
  """
  # Create a grid of X and Y values
  
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  # Create a triangulated surface
  surf = ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')

  ax.set_title("Triangulated 3D Surface from Scattered Data")
  ax.set_xlabel(xlab)
  ax.set_ylabel(ylab)
  ax.set_zlabel(zlab)
  plt.show()