# File: functions.py
# Description: Defines classes and functions for the spring-projectile simulation.
# Note: Corrected physics implementation.

import numpy as np
import math

# =======================================================
# Classes
# =======================================================

class Projectile:
    def __init__(self, Mass, V_x, V_y, x, y, R):
        self.M = Mass
        self.V_X = V_x
        self.V_Y = V_y
        self.X = x
        self.Y = y
        self.R = R

    def getSpeed(self):
        """Calculates the magnitude of the projectile's velocity."""
        return np.sqrt(self.V_X**2 + self.V_Y**2)

    def getEnergy(self):
        """Calculates the kinetic energy of the projectile. Corrected formula."""
        # Kinetic Energy = 0.5 * mass * speed^2
        return 0.5 * self.M * self.getSpeed()**2 # Corrected formula

    def update(self, F_X, F_Y, dt):
        """Updates the velocity and position based on net force using Verlet-like integration."""
        # Update position first using current velocity and previous acceleration
        # Note: The 0.5*a*dt^2 term implicitly uses acceleration from the *start* of dt
        acc_X_prev = F_X / self.M
        acc_Y_prev = F_Y / self.M
        self.X += self.V_X * dt + 0.5 * acc_X_prev * dt**2
        self.Y += self.V_Y * dt + 0.5 * acc_Y_prev * dt**2

        # Update velocity using the force (effectively using acceleration at the start of the step)
        # A more accurate Verlet would average accelerations, but this is common.
        self.V_X += acc_X_prev * dt
        self.V_Y += acc_Y_prev * dt


    def Y_pos_at_X(self, x_coord):
        """
        Returns the Y-coordinate of the lowest point of the projectile sphere
        at a given horizontal coordinate x_coord.
        Returns float('inf') if x_coord is outside the horizontal span of the projectile.
        """
        horizontal_dist_sq = (x_coord - self.X)**2
        radius_sq = self.R**2
        if horizontal_dist_sq > radius_sq:
            # The vertical line at x_coord does not intersect the projectile
            return float('inf')
        else:
            # Calculate the vertical distance from center to the bottom point at x_coord
            vertical_offset = np.sqrt(radius_sq - horizontal_dist_sq)
            return self.Y - vertical_offset

class Spring:
    def __init__(self, x, y, k, m) -> None:
        self.X = x           # Current X position
        self.Y = y           # Current Y position
        self.k = k           # Spring constant
        self.X_Equ = x       # Equilibrium X position
        self.Y_Equ = y       # Equilibrium Y position (initially 0)
        self.V_X = 0         # Initial X velocity
        self.V_Y = 0         # Initial Y velocity
        self.m = m           # Mass of the spring top (if considering inertia)

    def get_F_Y(self):
        """Calculates the internal restoring force in Y direction."""
        # Force = -k * displacement_from_equilibrium
        return -self.k * (self.Y - self.Y_Equ) # Corrected: Positive force when below Equ

    def get_F_X(self):
        """Calculates the internal restoring force in X direction."""
        # Force = -k * displacement_from_equilibrium
        return -self.k * (self.X - self.X_Equ)

    def update(self, F_net_X, F_net_Y, dt):
        """
        Updates the spring's velocity and position based on the NET force
        applied to it (external + internal restoring) using Verlet-like integration.
        """
        # Calculate acceleration based on NET force
        acc_X = F_net_X / self.m
        acc_Y = F_net_Y / self.m

        # Update position first
        self.X += self.V_X * dt + 0.5 * acc_X * dt**2
        self.Y += self.V_Y * dt + 0.5 * acc_Y * dt**2

        # Update velocity
        self.V_X += acc_X * dt
        self.V_Y += acc_Y * dt

# =======================================================
# Functions
# =======================================================

def init_springs(N_springs, dx, k, m):
    """Initializes a list of Spring objects along the x-axis."""
    springs = []
    start_x = 0 # Or adjust if springs shouldn't start at x=0
    for i in range(N_springs):
        # Place springs at intervals dx, with Y=0 equilibrium
        springs.append(Spring(start_x + i * dx, 0, k, m))
    return springs

def is_touching(spring, projectile, epsilon):
    """
    Checks if the projectile is touching or overlapping with the top of the spring.
    Revised logic for sphere hitting a point/surface.
    """
    # Check if the spring's X position is horizontally underneath the projectile
    if abs(spring.X - projectile.X) > projectile.R:
        return False # Spring is not under the projectile

    # Calculate the lowest point of the projectile directly above the spring's X
    proj_bottom_y_at_spring_x = projectile.Y_pos_at_X(spring.X)

    # Check if the projectile's bottom is at or below the spring's current top position
    # Add epsilon for floating point comparison robustness
    return proj_bottom_y_at_spring_x <= spring.Y + epsilon

# Note: add_forces and push_outside are removed.
# Force calculation is now integrated into the main simulation loop.