# #CIV 102 Bridge Project
import numpy as np
# #import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import math

# Defining INITAL BRIDGE PARAMETERS
# Beam geometry
L = 1200
# position, magnitude



loads_base_case = [[172, -66.6], [348, -66.6], [512, -66.6], [688, -66.6], [852, -66.6], [1028, -66.6]] # position, magnutide

loads_in_terms_of_p = [[172, -66.6], [348, -66.6], [512, -66.6], [688, -66.6], [852, -66.6], [1028, -66.6]] # position, magnutide in terms of p
# total train weight == 44.6 P

# loads_in_terms_of_p = loads_base_case

# Reaction forces
reaction_force_1 = 200
reaction_force_2 = 200

sig_tens = 0
sig_comp = 0


# defining CROSS SECITIONS
top_flange = [100, 1.27, 75.635] # [base, height, distance of centriod from bottom]
side_web = [1.270, 75-1.27, 37.5]
glue_tab = [5, 1.270, 74.365]
bottom_flange = [80, 1.27, 0.635]
diaphram = [bottom_flange[0] - (1.27*2), side_web[1] - 1.27, 5] #base, height


cross_sectional_areas = [top_flange, side_web, glue_tab, bottom_flange, diaphram] # [[top flange], [side flange], [bottom flange]]


#buckling of thin plates
diaphragm_dimension = 1200 / diaphram[2]
E = 4000
mu = 0.2

# Calculating y_bar
def y_bar(L):
    num = (L[0][0] * L[0][1] * L[0][2]) + (2 * (L[1][0] * L[1][1] * L[1][2])) + (2 * (L[2][0] * L[2][1] * L[2][2])) + (L[3][0] * L[3][1] * L[3][2])
    denom = (L[0][0] * L[0][1]) + (2 * (L[1][0] * L[1][1])) + (2 * (L[2][0] * L[2][1])) + (L[3][0] * L[3][1])
    ybar = num / denom
    return ybar

# Calculating I
def I(L):
    global ybar
    I_value = ((L[0][0] * (L[0][1])**3)/12) + (2 * ((L[1][0] * (L[1][1])**3)/12)) + (2 * ((L[2][0] * (L[2][1])**3)/12)) + ((L[3][0] * (L[3][1])**3)/12)
    I_value += ((L[0][0] * L[0][1]) * (L[0][2] - ybar)**2) + 2 * ((L[1][0] * L[1][1]) * (L[1][2] - ybar)**2) + 2 * ((L[2][0] * L[2][1]) * (L[2][2] - ybar)**2) + ((L[3][0] * L[3][1]) * (L[3][2] - ybar)**2)
    return I_value


# # Calculating Reaction Forecs
# def reaction_force(loads):
#    rf1 = ((loads[5][0]*(-6.67)) + (loads[4][0]*(-6.67)) + (loads[3][0]*(-6.67)) + (loads[2][0]*(-6.67)) + (loads[1][0]*(-9.00)) + (loads[0][0]*(-9.00)))
#    rf1 /= -1200
#    return rf1

# Calculating Reaction Forecs
# def reaction_force2(loads):
#     rf2 = 0
#     for i in range(len(loads)):
#         rf2 += loads[i][0] * loads[i][1]
#     rf2 /= -1200
#     return rf2

# def reaction_force1(loads):
#    rf2 = reaction_force2(loads)
#    rf1 = 44.6 - rf2
#    return rf1

# Calculating Total area
# def total_area(list):
#    matboard = 813 * 1016
#    print(f'total area of matboard is {matboard} mm^2')
#    top = list[0][0] * (list[0][1]/1.27) # width of top flange
#    mid = list[1][1] * (list[1][0]/1.27) # height of side web
#    gluetab = list[2][0] # width of glue tab
#    bottom = list[3][0] # width of bottom flange
#    diaphram = list[4][0] * list[4][1] * list[4][2] # area of diaphram

#    total = 1200*(top + 2*mid + 2*gluetab + bottom) + (diaphram)
#    print(f"total area of suggested cut peices is {total} mm^2")
#    return total

# Calculating maximum shear force
def max_shear(loads):
   rf1 = reaction_force_1
   rf2 = 400 - rf1
   maxshear = max(rf1, rf2)
   return maxshear



# Calculating shear force (values only)
def calculate_shear_force(position, loads):
  '''shear force calculation, inputs: position, loads
  outputs: shear force at position
  Last updated by Aref on Nov 23 @ 4pm'''
    # Initialize the initial reaction force
  global reaction_force_1

  shear_force = reaction_force_1

  sfd = [shear_force]
    # Iterate through the loads
  for j in range(len(loads)):
    if loads[j][0] >= position:
      break
    shear_force += loads[j][1]
    # sfd.append(shear_force)

  # return sfd
  return shear_force

# def calculate_shear_force_for_sfd(position, loads):
#   '''shear force calculation, inputs: position, loads
#   outputs: shear force at position
#   Last updated by Aref on Nov 23 @ 4pm'''
#     # Initialize the initial reaction force
#   global reaction_force_1
#   reaction_force_1 = reaction_force1(loads_in_terms_of_p)

#   shear_force = reaction_force_1

#   sfd = [shear_force]
#     # Iterate through the loads
#   for j in range(len(loads)):
#     if loads[j][0] >= position:
#       break
#     shear_force += loads[j][1]
#     sfd.append(shear_force)

#   return sfd
# #   return shear_force



def calculate_moment(position, loads):
  '''calculates moment at position due to loads
  this seems to be working now - aref on nov 22 at 12:27'''
  moment = 0
  for i in range(0, position, 1):
      moment += calculate_shear_force(i, loads) * 1
      # moment /= 1000
  return moment




# Calculates max moment
def max_moment(loads):
  '''calculate the max moment across length of beam
  this seems to be working now - aref on nov 22 at 12:27'''
  max_mom = 0
  for i in range(0, 1200, 1):
      moment = calculate_moment(i, loads)
      if moment > max_mom:
          max_mom = moment
  return max_mom






# def envelope_values(loads):
#   '''Loop through positions of loads at every centimeter of the bridge and calculate the max moment.
#   Store in an array that will then be graphed.
#   Assume the length is 1250, and the train is loaded according to the base case (172 cm on either side)'''
#   array = []
#   loads = reset_loads_to_start(loads)
#   for _ in range(0, 172, 2):
#     for i in range(len(loads)):
#         loads[i][0] += 2
#     max_moment_value = max_moment(loads)
#     array.append(max_moment_value)
#   return array





# def plot_envelope(loads):
#   '''Plot the envelope'''
#   envelope = envelope_values(loads)
#   plt.plot(envelope)
#   plt.xlabel('Position along the bridge (cm)')
#   plt.ylabel('Maximum Moment (kNm)')
#   plt.title('Envelope of Maximum Moment')
#   plt.show()

def plot_sfd(loads):
    sfd = []
    for i in range(0, 1201, 1):  # iterates through every point and appends the value of the shear at that position to an array
        sfd.append(calculate_shear_force(i, loads))
    plt.plot(sfd)
    plt.xlabel('Position along the beam (mm)')
    plt.ylabel('Shear Force (N)') 
    plt.title('Shear Force Diagram (SFD)')
    plt.grid(True)
    plt.show()


def plot_bmd(loads):
   bmd = []
   for i in range(0, 1201, 1): # iterates through every point and appends the value of the moment to an array
      bmd.append(calculate_moment(i, loads))
    
   plt.plot(bmd)
   plt.xlabel('Position along the beam (mm)')
   plt.ylabel('Bending Moment (N)') 
   plt.title('Bending Moment Diagram (BMD)')
   plt.grid(True) # provides grid
   plt.show()




# Plotting sfd.
if __name__ == "__main__":
#    print(calculate_shear_force(100, loads_in_terms_of_p))

    plot_sfd(loads_in_terms_of_p)
    plot_bmd(loads_in_terms_of_p)