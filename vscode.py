# #CIV 102 Bridge Project
import numpy as np
# #import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import math

# Defining INITAL BRIDGE PARAMETERS
# Beam geometry
L = 1200
# position, magnitude



# loads_base_case = [[172, -66.6], [348, -66.6], [512, -66.6], [688, -66.6], [852, -66.6], [1028, -66.6]] # position, magnutide

loads_in_terms_of_p = [[172, -66.6], [348, -66.6], [512, -66.6], [688, -66.6], [852, -66.6], [1028, -66.6]] # position, magnutide in terms of p
# total train weight == 400

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

def min_p():
   global diaphragm_dimension, Qmat, loads_in_terms_of_p
   p1 = bending_stress(I_value, ybar, max_mom)[0]
   p2 = bending_stress(I_value, ybar, max_mom)[1]
   p3 = max_shear_stress_matboard(loads_in_terms_of_p, Qmat, I_value)[0]
   p4 = max_shear_stress_glue(max_shear, Qglue, I_value)[0]
   p5 = case_1()[0]
   p6 = case_2()[0]
   p7 = case_3()[0]
   p8 = case_4(diaphragm_dimension, Qmat, loads_in_terms_of_p)[0]

   minp = min(p1, p2, p3, p4, p5, p6, p7, p8)
   print('min p: ', minp)
   return minp

# # Calculating Reaction Forecs
# def reaction_force(loads):
#    rf1 = ((loads[5][0]*(-6.67)) + (loads[4][0]*(-6.67)) + (loads[3][0]*(-6.67)) + (loads[2][0]*(-6.67)) + (loads[1][0]*(-9.00)) + (loads[0][0]*(-9.00)))
#    rf1 /= -1200
#    return rf1

# # Calculating Reaction Forecs
# def reaction_force2(loads):
#     rf2 = 0
#     for i in range(len(loads)):
#         rf2 += loads[i][0] * loads[i][1]
#     rf2 /= -1200
#     return rf2

# def reaction_force1(loads):
#    rf2 = reaction_force_2
#    rf1 = 400 - rf2
#    return rf1

# Calculating Total area
def total_area(list):
   matboard = 813 * 1016
   print(f'total area of matboard is {matboard} mm^2')
   top = list[0][0] * (list[0][1]/1.27) # width of top flange
   mid = list[1][1] * (list[1][0]/1.27) # height of side web
   gluetab = list[2][0] # width of glue tab
   bottom = list[3][0] # width of bottom flange
   diaphram = list[4][0] * list[4][1] * list[4][2] # area of diaphram

   total = 1200*(top + 2*mid + 2*gluetab + bottom) + (diaphram)
   print(f"total area of suggested cut peices is {total} mm^2")
   return total

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
  reaction_force_1 = reaction_force_1

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

def calculate_shear_force_for_sfd(position, loads):
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
    sfd.append(shear_force)

  return sfd
#   return shear_force



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
    for i in range(0, 1201, 1):  # Adjust the range to ensure you reach 1200
        sfd.append(calculate_shear_force(i, loads))
    plt.plot(sfd)
    plt.xlabel('Position along the beam (mm)')
    plt.ylabel('Shear Force (N)') 
    plt.title('Shear Force Diagram (SFD)')
    plt.grid(True)
    plt.show()


def plot_bmd(loads):
   bmd = []
   for i in range(0, 1201, 1):
      bmd.append(calculate_moment(i, loads))
    
   plt.plot(bmd)
   plt.xlabel('Position along the beam (mm)')
   plt.ylabel('Bending Moment (N)') 
   plt.title('Bending Moment Diagram (BMD)')
   plt.grid(True)
   plt.show()




# Plotting sfd.
# if __name__ == "__main__":
# #    print(calculate_shear_force(100, loads_in_terms_of_p))
#     plot_sfd(loads_in_terms_of_p)
#     plot_bmd(loads_in_terms_of_p)

# TESTS

# # Testing ybar and I
# if __name__ == "__main__":
#     pass
#     ybar = y_bar(cross_sectional_areas)
#     I = I(cross_sectional_areas)
#     print("ybar value is", ybar, "mm")
#     print("I value is", I/10**3, 'x10^3 mm^4')
#     # print(sfd)

# max_mom = max_moment(loads_in_terms_of_p)
max_mom = 68600
#function that returns p's

def bending_stress(I_value, ybar, max_mom):
    global top_flange, side_web, bottom_flange
    max_ss_comp = 6
    max_ss_tens = 30
    # M > 0, compression on top
    ytop = (top_flange[1] + side_web[1] + bottom_flange[1]) - ybar
    ybot = ybar
    app_s_comp = (max_mom*ytop)/(I_value)
    app_s_tens = (max_mom*ybot)/(I_value)
    p1 = (max_ss_comp*I_value)/(ybot*max_mom)
    p2 = (max_ss_tens*I_value)/(ytop*max_mom)
    FOS_sigma_comp = 6/((app_s_comp))
    FOS_sigma_tens = 30/((app_s_tens))
    print("applied comp stress:", app_s_comp)
    print("applied tens stress:", app_s_tens)
    print("FOS comp:", FOS_sigma_comp)
    print("FOS tens:", FOS_sigma_tens)
    print("p1,p2 =", p1, p2)
    return p1, p2, app_s_comp, app_s_tens, FOS_sigma_comp, FOS_sigma_tens

def Q_matboard(ybar):
    global Qmat
    global side_web, bottom_flange, glue_tab
    if ybar <= side_web[1] + bottom_flange[1]-glue_tab[1]:
       Qmat = 2*(bottom_flange[0]*bottom_flange[1]*(ybar - (bottom_flange[1]/2)) +  (ybar - bottom_flange[1]*bottom_flange[0]*(ybar - bottom_flange[1] - (side_web[1]/2))))
       print("Qmat =", Qmat)
    else:
        Qmat = 0
        print("Calculate new Q")
    return Qmat

def Q_glue(ybar):
    global side_web, bottom_flange, glue_tab, Qglue
    Qglue = 2*(top_flange[0]*top_flange[1])*((bottom_flange[1] + side_web[1] + top_flange[1]) - ybar -(top_flange[1]/2))
    print("Qglue =", Qglue)
    return Qglue

def max_shear_stress_matboard(loads, Qmat, I_value):
    global bottom_flange
    matboard_shear = 4
    maxshear = max_shear(loads)
    #case dependent(change base if there is no bottom!!!!!)
    app_tao_matb = (maxshear * Qmat) / (int(I_value) * (bottom_flange[0]))
    FOS_tao_matb = ((app_tao_matb)*10) / (4)
    p3 = (matboard_shear * I_value * bottom_flange[0]) / (Qmat * maxshear)
    print("applied tau matboard:", app_tao_matb)
    print("FOS shear matboard:", FOS_tao_matb)
    print("p3 =", p3)
    return p3, app_tao_matb, FOS_tao_matb

def max_shear_stress_glue(loads, Qglue, I_value):
    global glue_tab
    maxshear = max_shear(loads_in_terms_of_p)
    glue_shear = 2
    app_tao_glue = (maxshear * Qglue) / (I_value * bottom_flange[0])
    FOS_tao_glue = ((app_tao_glue)*10)/(2)
    p4 = (glue_shear*I_value*2*glue_tab[0])/(Qglue*maxshear)
    print("FOS shear glue:", FOS_tao_glue)
    print("p4 =", p4)
    return p4, app_tao_glue, FOS_tao_glue

#buckling of thin plates

#case 1 - restrained on 4 sides
def case_1():
    k = 4
    t = top_flange[1]
    b = bottom_flange[0] - 2*(side_web[0])
    ytop = (bottom_flange[1] + side_web[1] + top_flange[1]) - ybar

    sigma_crit_1 = ((k * math.pi**2 * E) / (12*(1-mu**2)) ) * (t/b)**2

    if sigma_crit_1 < 6:
        print("will buckle in case 1")

    p5 = (sigma_crit_1*I_value)//(ytop*max_mom)

    FOS_case1 = (sigma_crit_1*10)/ 6

    print("p5 =", p5)
    print("FOS buck 1:", FOS_case1)

    return p5, FOS_case1

#case 2 - restrained on 3 sides
def case_2():
    k = 0.425
    t = top_flange[1]
    b = top_flange[0] - bottom_flange[0]
    ytop = (bottom_flange[1] + side_web[1] + top_flange[1]) - ybar
    sigma_crit_2 = ((k * math.pi**2 * E) / (12*(1-mu**2)) ) * (t/b)**2

    if sigma_crit_2 < 6:
        print("will buckle in case 2")

    p6 = (sigma_crit_2*I_value)//(ytop*max_mom)
    FOS_case2 = (sigma_crit_2*10) / 6
    print("p6 =", p6)
    print("FOS buck 2:", FOS_case2)
    return p6, FOS_case2

#case 3 - linear stress profile
def case_3():
    k = 6
    t = (bottom_flange[1] + side_web[1]) - ybar
    b = 2*(side_web[0])
    ytop = (bottom_flange[1] + side_web[1] + top_flange[1]) - ybar
    sigma_crit_3 = ((k * math.pi**2 * E) / (12*(1-mu**2)) ) * (b/t)**2

    p7 = (sigma_crit_3*I_value)//(ytop*max_mom)

    FOS_case3 = (sigma_crit_3*10) / 6
    print("p7 =", p7)
    print("FOS buck 3:", FOS_case3)
    return p7, FOS_case3

#case 4 - shear
def case_4(diaphragm_dimension, Qmat, loads):
    global I_value
    maxshear = max_shear(loads)
    a = diaphragm_dimension
    h = bottom_flange[1] + side_web[1]
    b = side_web[0]
    ytop = (bottom_flange[1] + side_web[1] + top_flange[1]) - ybar
    crit_4 = ((5 * math.pi**2 * E) / (12*(1 - mu**2))) * ((b/h)**2 + (b/a)**2)

    p8 = ((2*I_value*b)*(crit_4))/(Qmat*maxshear)

    FOS_case4 = crit_4 / 4
    print("p8 =", p8)
    print("FOS shear.buck:", FOS_case4)
    return p8, FOS_case4



if __name__ == "__main__":
    ybar = y_bar(cross_sectional_areas)
    I_value = I(cross_sectional_areas)
    print("ybar value is", ybar, "mm")
    print("I value is", I_value/10 )
    # reaction_force_result = reaction_force(loads_in_terms_of_p)
    max_shear_result = max_shear(loads_in_terms_of_p)
    max_mom = max_moment(loads_in_terms_of_p)
    print("MOMENT IN CENTER", calculate_moment(1200//2, loads_in_terms_of_p))
    print("max moment is", max_moment(loads_in_terms_of_p))
    bending_stress_result = bending_stress(I_value, ybar, max_mom)
    Q_matboard_result = Q_matboard(ybar)
    Q_glue_result = Q_glue(ybar)
    max_shear_stress_matboard_result = max_shear_stress_matboard(loads_in_terms_of_p, Q_matboard_result, I_value)

    print(calculate_moment(600, loads_in_terms_of_p))


    max_shear_stress_glue_result = max_shear_stress_glue(loads_in_terms_of_p, Q_glue_result, I_value)

    case_1_result = case_1()
    case_2_result = case_2()
    case_3_result = case_3()
    case_4_result = case_4(diaphragm_dimension, Qmat, loads_in_terms_of_p)

    print(min_p())
    total_area(cross_sectional_areas)
## TESTING SHEAR, MOMENT, MAXMOMENT, AND ENVELOPE.
# if __name__ == "__main__":
    # loads = [(172, -66.7), (348, -66.7), (512, -66.7), (688, -66.7), (852, -90), (1028, -90)] # Format: (position, magnitude)
    # position_on_beam = 625
    # length = 1250

    # print(f"Moment at point {position_on_beam} is {calculate_moment(position_on_beam, loads_in_terms_of_p)}")


    # resulting_shear_force = calculate_shear_force(position_on_beam, loads_in_terms_of_p)
    # print(f"Shear force at position {position_on_beam} is {resulting_shear_force}")

    # print("Max moment is ", max_moment(loads_in_terms_of_p))

    # print(reset_loads_to_start(loads_in_terms_of_p))
    # print(plot_envelope(loads_in_terms_of_p))