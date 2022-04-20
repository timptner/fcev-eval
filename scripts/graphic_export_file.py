import scipy.io
import matplotlib.pyplot as plt
import numpy as np
from typing import Union, Tuple

#data load
Data_WLTP_Bat_SOC50 = scipy.io.loadmat(r"C:\Users\Maximus\Desktop\MPA\Matlab\FCEV_Simulation_FINAL\FCEV_Simulation_20220203T1421\DATA_WLTP_BAT_SOC50.mat")
Data_WLTP_Bat = Data_WLTP_Bat_SOC50['Data_WLTP_Bat']

Data_WLTP_SC_SOC50 = scipy.io.loadmat(r"C:\Users\Maximus\Desktop\MPA\Matlab\FCEV_Simulation_FINAL\FCEV_Simulation_20220203T1421\DATA_WLTP_SC_SOC50.mat")
Data_WLTP_SC = Data_WLTP_SC_SOC50['Data_WLTP_SC']


#print(mat)
#time load
Time_WLTP_Bat_SOC50 = scipy.io.loadmat(r"C:\Users\Maximus\Desktop\MPA\Matlab\FCEV_Simulation_FINAL\FCEV_Simulation_20220203T1421\TIME_WLTP_BAT_SOC50.mat")
Time_WLTP_Bat = Time_WLTP_Bat_SOC50['Time_WLTP_Bat']

Time_WLTP_SC_SOC50 = scipy.io.loadmat(r"C:\Users\Maximus\Desktop\MPA\Matlab\FCEV_Simulation_FINAL\FCEV_Simulation_20220203T1421\TIME_WLTP_SC_SOC50.mat")
Time_WLTP_SC = Time_WLTP_SC_SOC50['Time_WLTP_SC']

Time = [Time_WLTP_Bat, Time_WLTP_SC]
# variable name load
# f = open(r"C:\Users\Maximus\Desktop\MPA\Matlab\FCEV_Simulation_FINAL\FCEV_Simulation_20220203T1421\Var_List.txt",'r')
# Var_List = f.readlines()
# print("Variable 1 ist {}".format(Var_List[1]))
Var_List =["Sollbremsmoment [N]", "Sollgeneratormoment [N]", "Sollgeneratorleistung [W]", "Bremsmoment [N]",
           "Motormoment [N]", "elektr. Motorleistung [W]", "mechanische Motorleistung [W]", "Generatormoment [N]",
           "Sollmotormoment [N]", "max. Motorleistung [W]", "Sollmotorleistung [W]", "elektr. Motorengrenzleistung [W]",
           "Nebenverbrauchsleistung [W]", "opt. elektr. Brennstoffzellleistung [W]", "Sollstromstärke der FC [A]",
           "Stromstärkegradient FC [A/s]", "Stromstärke FC [A]", "chem. Leistung FC [W]", "elektr. Leistung FC [W]",
           "max. elektr. Leistung FC [W]", "Spannung FC [V]", "Wirkungsgrad FC [-]",
           "max. Boardnetzleistung [W]", "elektr. Gesamtleistung [W]", "SOC [-]", "Spannung Speichers [V]",
           "Stromstärke Speicher [A]", "Wasserstofftankniveau [-]", "Wasserstoffmassenstrom [kg/s]", "Wasserstoffmenge [kg]",
           "Sollgeschwindigkeit [m/s]", "Sollleistung der FC [W]", "Sollstrategie [-]", "Strategie [-]",
           "SOC-Richtwert [-]", "Weg [m]", "Geschwindigkeit [m/s]"]

Var_List_SC =["Sollbremsmoment [N]", "Sollgeneratormoment [N]", "Sollgeneratorleistung [W]", "Bremsmoment [N]",
           "Motormoment [N]", "elektr. Motorleistung [W]", "mechanische Motorleistung [W]", "Generatormoment [N]", "omega [rad/s]",
           "Sollmotormoment [N]", "max. Motorleistung [W]", "Sollmotorleistung [W]", "elektr. Motorengrenzleistung [W]",
           "Nebenverbrauchsleistung [W]", "opt. elektr. Brennstoffzellleistung [W]", "Sollstromstärke der FC [A]",
           "Stromstärkegradient FC [A/s]", "Stromstärke FC [A]", "chem. Leistung FC [W]", "elektr. Leistung FC [W]",
           "max. elektr. Leistung FC [W]", "Spannung FC [V]", "Wirkungsgrad FC [-]",
           "max. Boardnetzleistung [W]", "elektr. Gesamtleistung [W]", "SOC [-]", "Spannung Speichers [V]",
           "Stromstärke Speicher [A]", "Wasserstofftankniveau [-]", "Wasserstoffmassenstrom [kg/s]", "Wasserstoffmenge [kg]",
           "Sollgeschwindigkeit [m/s]", "Sollleistung der FC [W]", "Sollstrategie [-]", "Strategie [-]",
           "SOC-Richtwert [-]", "Weg [m]", "Geschwindigkeit [m/s]"]

print(Var_List[34])
# figure creating

#mm 2 inch
def mm2inch(value: Union[int, Tuple[int]]) -> Union[int]:
    def calc(val):
        return round(val / 25.4, 2)

    if type(value) == tuple:
        return tuple([calc(i) for i in value])
    elif type(value) == int:
        return calc(value)
    else:
        raise ValueError("Only integers or tuple of integers are allowed.")


#fig parameters

figsize = mm2inch((80, 50))
dpi = 300.0
linewidth = 0.5
fontsize = 6
color_vec = ['b', 'g', 'r']
color_vec = len(Var_List_SC) * color_vec

num_variables = np.shape(Var_List)
#num_fig = range(int(num_variables[0]))
#FC_on_time =
index_FC_on = int(np.where(Time_WLTP_Bat==1550)[0])
index_FC_off = int(np.shape(Time_WLTP_Bat)[0])
index_marker_FC = np.where(Data_WLTP_Bat[:,33]==6)[0]
index_marker_FC = 28636

index_EM_on = int(np.where(Time_WLTP_Bat==740)[0])
index_EM_off = int(np.where(Time_WLTP_Bat==840)[0])

index_Bat_on = index_EM_on
index_Bat_off = index_EM_off
index_Reg_Brake_on = np.where(Data_WLTP_Bat[index_Bat_on:index_Bat_off,33]==1)[0][0]

index_SC_on = int(np.where(Time[1]==1290)[0])
index_SC_off = int(np.where(Time[1]==1340)[0])
index_Marker_SC = np.where(Data_WLTP_SC[index_SC_on:index_SC_off,34]==3)[0][0]
#plotting FC on data
FC_comp = [33, 16, 20, 18, 17, 21, 12, 28, 27] #stratmode, IFC, UFC PFCel, PFchem, etaFC, PFCaux, m_dot, H2-Level
EM_comp = [33, 5, 4, 8, 7, 1] #startmode, PMel , MM, MMset, MG, MGset
Bat_comp = [33, 23, 18, 12, 5, 25, 26, 24] #stratmode, Pel, PFCel, PFCaux, PMel  U, I, SOC
SC_comp = [34, 24, 19, 13, 5, 26, 27, 25] #stratmode, Pel, PFCel, PFCaux, PMel  U, I, SOC
all_comp = range(num_variables[0])

# print("Es werden {} Grafiken erstellt, deren Verlauf das Verhalten der Fuel Cell darstellen.".format(len(FC_comp)))
# print("Es werden {} Grafiken erstellt, deren Verlauf das Verhalten des E-Motors darstellen.".format(len(EM_comp)))
# print("Es werden {} Grafiken erstellt, deren Verlauf das Verhalten der Batterie darstellen.".format(len(Bat_comp)))
# print("Es werden {} Grafiken erstellt, deren Verlauf das Gesamtverhalten des FCEV darstellen.".format(len(all_comp)))
# print("Insgesamt wurden: {} Grafiken erstellt.".format(len(all_comp)+len(FC_comp)+len(EM_comp)+len(Bat_comp)))



num_fig_FC = range(len(FC_comp))
num_fig_EM = range(len(EM_comp))
num_fig_Bat = range(len(Bat_comp))
num_fig_SC = range(len(SC_comp))
num_fig_all = range(len(all_comp))

#plotting all data
#FC Data
# for i in num_fig_FC:
#     fig, ax = plt.subplots(figsize=figsize, dpi=dpi, constrained_layout=True)
#
#     ax.set_xlabel("Zeit [s]",fontdict={'fontsize':fontsize+1})
#     plt.xticks(fontsize=fontsize)
#     ax.set_ylabel(Var_List[FC_comp[i]].replace('\n', ''),fontdict={'fontsize':fontsize+1})
#     plt.yticks(fontsize=fontsize)
#
#     if i == 0:
#             #ax.set_title('Verhalten der Brennstoffzellkomponenten',fontdict={'fontsize':fontsize})
#         ax.set(ylim=(0, 6.5))
#     ax.grid(True)
#     ax.plot(Time_WLTP_Bat[index_FC_on:index_FC_off], Data_WLTP_Bat[index_FC_on:index_FC_off,FC_comp[i]],color_vec[i],linewidth=linewidth)
#     plt.axvline(Time_WLTP_Bat[index_marker_FC], color='k', linestyle='--', linewidth=linewidth+0.5)
#
#     #plt.show()
#     #plt.savefig('WLTP FC Plausibility {}.png'.format(Var_List[FC_comp[i]].replace('\n', '').replace('\n', '').replace("/","").replace("-",""))) #working
#
# #####################################################################################################################
# ##EM Data
# for i in num_fig_EM:
#     fig, ax = plt.subplots(figsize=figsize, dpi=dpi, constrained_layout=True)
#
#     ax.set_xlabel("Zeit [s]",fontdict={'fontsize':fontsize+1})
#     plt.xticks(fontsize=fontsize)
#     ax.set_ylabel(Var_List[EM_comp[i]].replace('\n', ''),fontdict={'fontsize':fontsize+1})
#     plt.yticks(fontsize=fontsize)
#
#     if i == 0:
#         #ax.set_title('Verhalten der Brennstoffzellkomponenten',fontdict={'fontsize':fontsize})
#         ax.set(ylim=(0, 6.5))
#     ax.grid(True)
#     ax.plot(Time_WLTP_Bat[index_EM_on:index_EM_off], Data_WLTP_Bat[index_EM_on:index_EM_off,EM_comp[i]],color_vec[i],linewidth=linewidth)
#     plt.axvline(Time_WLTP_Bat[(index_Bat_on + index_Reg_Brake_on)], color='k', linestyle='--', linewidth=linewidth+0.5)
# #    plt.show()
    #plt.savefig('WLTP EM Plausibility {}.png'.format(Var_List[EM_comp[i]].replace('\n', '').replace('\n', '').replace("/","").replace("-",""))) #working
#####################################################################################################################
# Bat Data
# for i in num_fig_Bat:
#      fig, ax = plt.subplots(figsize=figsize, dpi=dpi, constrained_layout=True)
#
#      ax.set_xlabel("Zeit [s]",fontdict={'fontsize':fontsize+1})
#      plt.xticks(fontsize=fontsize)
#      ax.set_ylabel(Var_List[Bat_comp[i]].replace('\n', ''),fontdict={'fontsize':fontsize+1})
#      plt.yticks(fontsize=fontsize)
#
#      if i == 0:
#          #ax.set_title('Verhalten der Brennstoffzellkomponenten',fontdict={'fontsize':fontsize})
#          ax.set(ylim=(0, 6.5))
#      ax.grid(True)
#      ax.plot(Time_WLTP_Bat[index_Bat_on:index_Bat_off], Data_WLTP_Bat[index_Bat_on:index_Bat_off,Bat_comp[i]], color_vec[i],linewidth=linewidth)
#      plt.axvline(Time_WLTP_Bat[index_Bat_on + index_Reg_Brake_on], color='k', linestyle='--', linewidth=linewidth+0.5)
#      #plt.show()
#      #plt.savefig('WLTP Bat Plausibility {}.png'.format(Var_List[Bat_comp[i]].replace('\n', '').replace('\n', '').replace("/","").replace("-",""))) #working

# #####################################################################################################################
# SC Data
for i in num_fig_SC:
     fig, ax = plt.subplots(figsize=figsize, dpi=dpi, constrained_layout=True)

     ax.set_xlabel("Zeit [s]",fontdict={'fontsize':fontsize+1})
     plt.xticks(fontsize=fontsize)
     ax.set_ylabel(Var_List_SC[SC_comp[i]].replace('\n', ''),fontdict={'fontsize':fontsize+1})
     plt.yticks(fontsize=fontsize)

     if i == 0:
        ax.set(ylim=(0, 6.5))
        ax.set_ylabel(Var_List_SC[SC_comp[i]].replace('\n', ''), fontdict={'fontsize': fontsize + 1})

        ax.grid(True)
        ax.plot(Time_WLTP_SC[index_SC_on:index_SC_off], Data_WLTP_SC[index_SC_on:index_SC_off,SC_comp[i]], color_vec[i],linewidth=linewidth)
        plt.axvline(Time_WLTP_SC[index_SC_on + index_Marker_SC], color='k', linestyle='--', linewidth=linewidth+0.5)
        #plt.savefig('WLTP SC Plausibility {}.png'.format(Var_List_SC[SC_comp[i]].replace('\n', '').replace('\n', '').replace("/","").replace("-",""))) #working

     elif i == 1:
         ax.set_ylabel("Leistungsverläufe SC [W]", fontdict={'fontsize': fontsize + 1})
         ax.grid(True)
         plot1 = ax.plot(Time[1][index_SC_on:index_SC_off], Data_WLTP_SC[index_SC_on:index_SC_off,SC_comp[i]], 'y', linewidth=linewidth + 0.5,
                         label='elektr. Gesamtleistung')
         plot2 = ax.plot(Time[1][index_SC_on:index_SC_off], Data_WLTP_SC[index_SC_on:index_SC_off, SC_comp[i+1]], 'b', linewidth=linewidth, label='elektr. Leistung FC')
         plot3 = ax.plot(Time[1][index_SC_on:index_SC_off], Data_WLTP_SC[index_SC_on:index_SC_off, SC_comp[i+2]], 'r', linewidth=linewidth, label='Leistung NV', linestyle='--')
         plot4 = ax.plot(Time[1][index_SC_on:index_SC_off], Data_WLTP_SC[index_SC_on:index_SC_off, SC_comp[i+3]], 'g', linewidth=linewidth, label='elektr. Motorleistung', linestyle=':')
         plt.axvline(Time_WLTP_SC[index_SC_on + index_Marker_SC], color='k', linestyle='--', linewidth=linewidth + 0.5)
         ax.legend(loc='upper right', fontsize=fontsize)
         plt.show()
         #plt.savefig('WLTP SC Plausibility {}.png'.format(Var_List_SC[SC_comp[i]].replace('\n', '').replace('\n', '').replace("/", "").replace("-", "")))  # working

     #plt.show()
     else:
         ax.grid(True)
         ax.set_ylabel(Var_List_SC[SC_comp[i]].replace('\n', ''), fontdict={'fontsize': fontsize + 1})
         ax.plot(Time_WLTP_SC[index_SC_on:index_SC_off], Data_WLTP_SC[index_SC_on:index_SC_off, SC_comp[i]], color_vec[i],
         linewidth=linewidth)
         plt.axvline(Time_WLTP_SC[index_SC_on + index_Marker_SC], color='k', linestyle='--', linewidth=linewidth + 0.5)
         plt.show()

     plt.savefig('WLTP SC Plausibility {}.png'.format(Var_List_SC[SC_comp[i]].replace('\n', '').replace('\n', '').replace("/","").replace("-",""))) #working

# #####################################################################################################################

 #whole data
# for i in num_fig_all:
#     fig, ax = plt.subplots(figsize=figsize, dpi=dpi, constrained_layout=True)
#
#     ax.set_xlabel("Zeit [s]",fontdict={'fontsize':fontsize+1})
#     plt.xticks(fontsize=fontsize)
#     ax.set_ylabel(Var_List[all_comp[i]].replace('\n', ''),fontdict={'fontsize':fontsize+1})
#     plt.yticks(fontsize=fontsize)
#     ax.grid(True)
#     ax.set(xlim=(0, Time_WLTP_Bat[-1]))
#     if i == 33:
#         #ax.set_title('Verhalten der Brennstoffzellkomponenten',fontdict={'fontsize':fontsize})
#         ax.set(ylim=(0, 6.5))
#
#     if i == 30:
#         ax.set_ylabel("Soll- und Istgeschwindigkeit" , fontdict={'fontsize': fontsize + 1})
#         plot1 = ax.plot(Time_WLTP_Bat[:], Data_WLTP_Bat[:,30],'b',linewidth=linewidth+0.5, linestyle='--', label='Sollgeschw.')
#         plot2 = ax.plot(Time_WLTP_Bat[:], Data_WLTP_Bat[:, 36], 'r', linewidth=linewidth, label='Istgeschw.')
#         ax.legend()
#         #plt.show()
#     elif i != 36:
#         ax.set_ylabel(Var_List[all_comp[i]].replace('\n', ''), fontdict={'fontsize': fontsize + 1})
#         ax.plot(Time_WLTP_Bat[:], Data_WLTP_Bat[:,i], color_vec[i],linewidth=linewidth)
#     else:
#         pass
    #plt.savefig('WLTP Bat SOC50 {}.png'.format(Var_List[all_comp[i]].replace('\n', '').replace("/","").replace("-",""))) #working

#plt.show()