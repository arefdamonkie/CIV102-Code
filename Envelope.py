
import numpy as np
import matplotlib.pyplot as plt

# Loads
loads_in_terms_of_p = [[172, -6.66], [348, -6.66], [512, -6.66], [688, -6.66], [852, -6.66], [1028, -6.66]]
initial_loads = [[0, -6.67], [176, -6.67], [340, -6.67], [516, -6.67], [680, -9], [856, -9]]
final_loads = [[344, -6.67], [520, -6.67], [684, -6.67], [860, -6.67], [1024, -9], [1200, -9]]

# Calculating Reaction Forecs
def reaction_force2(loads):
    rf2 = 0
    for i in range(len(loads)):
        rf2 += loads[i][0] * loads[i][1]
    rf2 /= -1200
    return rf2
def reaction_force1(loads):
   rf2 = reaction_force2(loads)
   rf1 = 44.6 - rf2
   return rf1

def max_shear(loads):
   rf2 = reaction_force2(loads)
   rf1 = 44.6 - rf2
   return max(rf1, rf2)
   

# Calculating shear force (values only)
def calculate_shear_force(position, loads):
  '''shear force calculation, inputs: position, loads
  outputs: shear force at position
  Last updated by Aref on Nov 23 @ 4pm'''
    # Initialize the initial reaction force
  global reaction_force_1
  reaction_force_1 = reaction_force1(loads_in_terms_of_p)
  
  shear_force = reaction_force_1

  sfd = [shear_force]
    # Iterate through the loads
  for j in range(len(loads)):
      if loads[j][0] >= position:
        break
      shear_force += loads[j][1]
    #   sfd.append(shear_force)
  
#   return sfd
  return shear_force



def calculate_moment(position, loads):
  '''calculates moment at position due to loads
  this seems to be working now - aref on nov 22 at 12:27'''
  moment = 0
  for i in range(0, position, 1):
      moment += calculate_shear_force(i, loads) * 1
      # moment /= 1000
  return moment



def max_moment(loads):
  '''calculate the max moment across length of beam
  this seems to be working now - aref on nov 22 at 12:27'''
  max_moment = 0
  for i in range(0, 1201, 1):
      moment = calculate_moment(i, loads)
      if moment > max_moment:
          max_moment = moment
  return max_moment



def reset_loads_to_start(loads):
  '''resets the loads to zero
  this seems to be working now - aref on nov 22 at 12:27'''
  for i in range(len(loads)):
      loads[i][0] -= 172
  return loads

# def envelope_values(loads):
#   '''Loop through positions of loads at every centimeter of the bridge and calculate the max moment.
#   Store in an array that will then be graphed.
#   Assume the length is 1250, and the train is loaded according to the base case (172 cm on either side)
#   DOES NOT WORK DUE TO WRONG REACTION FORCES'''
#   array = []

#   # set loads to initial position
#   loads = reset_loads_to_start(loads)
#   max_moment_value = max_moment(loads)
#   array.append(max_moment_value)

#   # iterating through every point on the bridge
#   for j in range(43):
#     for i in range(len(loads)):
#         loads[i][0] += 8
#     max_moment_value = max_moment(loads)
#     array.append(max_moment_value)

#   return array
def envelope_values_shear(initial_loads):
   shear = []

    # setup loads to initial position
   loads = reset_loads_to_start(initial_loads)
   max_shear_value = max_shear(loads)
   shear.append(max_shear_value)

   # iterate through every point on the bridge
   for j in range(43):
        loads_copy = loads.copy()  # Work with a copy of the loads
        for i in range(len(loads_copy)):
            loads_copy[i][0] += 8
        max_shear_value = max_shear(loads_copy)
        shear.append(max_shear_value)

   return shear


def envelope_values(initial_loads):
    '''Loop through positions of loads at every centimeter of the bridge and calculate the max moment.
    Store in an array that will then be graphed.
    Assume the length is 1250, and the train is loaded according to the base case (172 cm on either side)
    DOES NOT WORK DUE TO WRONG REACTION FORCES'''
    array = []

    # set loads to initial position
    loads = reset_loads_to_start(initial_loads)
    max_moment_value = max_moment(loads)
    array.append(max_moment_value)

    # iterating through every point on the bridge
    for j in range(43):
        loads_copy = loads.copy()  # Work with a copy of the loads
        for i in range(len(loads_copy)):
            loads_copy[i][0] += 8
        max_moment_value = max_moment(loads_copy)
        array.append(max_moment_value)

    return array


  # end
#   for i in range(len(loads)):
#      loads[i][0] += 172
#   max_moment_value = max_moment(loads)
#   array.append(max_moment_value)



def plot_shear_envelope(loads):
  '''Plot the envelope'''
  envelope = envelope_values_shear(loads)
  x_values = [i * 8 for i in range(len(envelope))]
  plt.plot(x_values, envelope)
  plt.xlabel('Position of train along the bridge (mm)')
  plt.ylabel('Maximum Shear in terms of P (N)')
  plt.title('Envelope of Maximum Shear')
  plt.show()

def plot_envelope(loads):
  '''Plot the envelope'''
  envelope = envelope_values(loads)
  x_values = [i * 8 for i in range(len(envelope))]
  plt.plot(x_values, envelope)
  plt.xlabel('Position of train along the bridge (mm)')
  plt.ylabel('Maximum Moment in terms of P (Nm)')
  plt.title('Envelope of Maximum Moment')
  plt.show()




if __name__ == "__main__":
    position = 1200
  #   this is now working - aref on nov 26 at 2 pm
#   print(reaction_force1(loads_in_terms_of_p))
#   print(calculate_shear_force(position, loads_in_terms_of_p))
    # print(envelope_values(loads_in_terms_of_p))
    # plot_envelope(loads_in_terms_of_p)
    plot_shear_envelope(loads_in_terms_of_p)