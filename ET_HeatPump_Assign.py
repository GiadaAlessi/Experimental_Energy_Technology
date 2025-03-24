#Practice on Air to Water Heat Pump

from CoolProp.CoolProp import *
import numpy as np
import matplotlib.pyplot as plt

#### Input Data ####

ref='R134a'

# Tests
# Experimental data of the primary (refrigerant) circuit
Tcomp_out=np.array([68.57, 73.74, 83.83, 93.87, 108.10])
Tcond_in=np.array([65.29, 72.41, 77.60, 82.91, 89.72])
Tcond_out=np.array([26.77, 36.65, 45.96, 54.88, 65.37])
Texp_in=np.array([25.87, 38.06, 47.92, 56.30, 65.07])
Texp_out=np.array([2.35, 4.15, 6.09, 7.65, 8.89])
Tevap_in=np.array([2.30, 3.79, 5.54, 6.94, 8.13])
Tevap_out=np.array([8.01, 10.06, 12.93, 15.63, 17.43])
Tcomp_in=np.array([9.04, 10.99, 13.78, 16.36, 18.21])        #°C
pcomp_out=np.array([9.441, 11.606, 14.188, 16.950, 20.445])
pcomp_in=np.array([2.920, 3.097, 3.314, 3.499, 3.664])       #bar
mref=np.array([34.77, 35.07, 34.92, 34.15, 32.18])           #kg/h
We=np.array([531.8, 589.0, 652.4, 727.5, 813.0])             #W
# Experimental data from secondary (coolant and air) circuits
Tcool_in=np.array([20.55, 30.86, 40.67, 49.91, 59.96])
Tcool_out=np.array([27.18, 37.05, 46.58, 55.42, 64.77])
Tair_in=np.array([20.10, 20.05, 20.10, 19.99, 20.00])
Tair_out=np.array([6.63, 7.7, 8.85, 9.72, 11.17])         #°C
HRair_in=np.array([32.60, 33.64, 35.33, 35.43, 34.92])     #%
HRair_out= np.array([76.00, 72.93, 68.77, 65.54, 59.31])      #%
mcool=np.array([0.080, 0.079, 0.078, 0.077, 0.076])         #kg/s
mair=np.array([0.122, 0.121, 0.121, 0.120, 0.119])         #kg/s
Wf=91                                               #W
cpcool=np.array([3702, 3735, 3768, 3801, 3834])          #J/kgK

# Evaluation of Hentalpies

h1=np.zeros(5)
h2=np.zeros(5)
h3=np.zeros(5)
h4=np.zeros(5)
h5=np.zeros(5)
h6=np.zeros(5)
h7=np.zeros(5)
h8=np.zeros(5)

p1=np.zeros(5)
p2=np.zeros(5)
p3=np.zeros(5)
p4=np.zeros(5)
p5=np.zeros(5)
p6=np.zeros(5)
p7=np.zeros(5)
p8=np.zeros(5)

for i in range (0,5,1):
    Tsat_cond= PropsSI('T', 'P', pcomp_out[i]*1e5, 'Q', 1, ref)  # Saturation temperature at pcomp_out[i]
    Tsat_evap = PropsSI('T', 'P', pcomp_in[i]*1e5, 'Q', 1, ref)   # Saturation temperature at pcomp_in[i]
    print(Tsat_cond-273.15, Tsat_evap-273.15)

    h1[i]=PropsSI('H', 'P', pcomp_in[i]*1e5,'T', Tcomp_in[i]+273.15, ref)
    h2[i]=PropsSI('H', 'P', pcomp_out[i]*1e5,'T', Tcomp_out[i]+273.15, ref)
    h3[i]=PropsSI('H', 'P', pcomp_out[i]*1e5,'T', Tcond_in[i]+273.15, ref)
    h4[i]=PropsSI('H', 'P', pcomp_out[i]*1e5,'T', Tcond_out[i]+273.15, ref)
    h5[i]=PropsSI('H', 'P', pcomp_out[i]*1e5,'T', Texp_in[i]+273.15, ref)
    h6[i]=PropsSI('H', 'P', pcomp_in[i]*1e5,'T', Texp_out[i]+273.15, ref)
    h7[i]=PropsSI('H', 'P', pcomp_in[i]*1e5,'T', Tevap_in[i]+273.15, ref)
    h8[i]=PropsSI('H', 'P', pcomp_in[i]*1e5,'T', Tevap_out[i]+273.15, ref)

    h6[i]=h5[i]

    p1[i]=pcomp_in[i]*1e5
    p2[i]=pcomp_out[i]*1e5
    p3[i]=pcomp_out[i]*1e5
    p4[i]=pcomp_out[i]*1e5
    p5[i]=pcomp_out[i]*1e5
    p6[i]=pcomp_in[i]*1e5
    p7[i]=pcomp_in[i]*1e5
    p8[i]=pcomp_in[i]*1e5

#### Plot p-h Diagram ####

for i in range (0,5,1):
    plt.figure(figsize=(10, 6))
    plt.plot([h1[i], h2[i]], [p1[i], p2[i]], label='Compression', color='red', marker='o')
    plt.plot([h2[i], h3[i]], [p2[i], p3[i]], color='black', marker='o')
    plt.plot([h3[i], h4[i]], [p3[i], p4[i]], label='Condensation', color='orange', marker='o')
    plt.plot([h4[i], h5[i]], [p4[i], p5[i]], color='black', marker='o')
    plt.plot([h5[i], h6[i]], [p5[i], p6[i]], label='Expansion', color='green', marker='o')
    plt.plot([h6[i], h8[i]], [p6[i], p8[i]], label='Evaporation', color='blue', marker='o')
    plt.plot([h8[i], h1[i]], [p8[i], p1[i]], color='black', marker='o')
    
    pressure_saturation = np.linspace(1e5, 1e7, 500)
    h_saturation_liquid = PropsSI('H', 'P', pressure_saturation, 'Q', 0, ref)
    h_saturation_vapor = PropsSI('H', 'P', pressure_saturation, 'Q', 1, ref)
    plt.plot(h_saturation_liquid, pressure_saturation, 'k--', label='Saturation Line')
    plt.plot(h_saturation_vapor, pressure_saturation, 'k--')
    plt.title(f'Air to Water Heat Pump P-h Diagram - Test {i+1}')
    plt.xlabel('Enthalpy (J/kg)')
    plt.ylabel('Pressure (Pa)')
    plt.grid()
    plt.legend()
    plt.show()

colors = ['blue', 'green', 'red', 'purple', 'orange']
plt.figure(figsize=(10, 6))
for i in range(5):
    plt.plot([h1[i], h2[i]], [p1[i], p2[i]], label=f'Test {i+1}', color=colors[i], marker='o')
    plt.plot([h2[i], h5[i]], [p2[i], p5[i]], color=colors[i], marker='o')
    plt.plot([h5[i], h6[i]], [p5[i], p6[i]], color=colors[i], marker='o')
    plt.plot([h6[i], h1[i]], [p6[i], p1[i]], color=colors[i], marker='o')

pressure_saturation = np.linspace(1e5, 1e7, 500)
h_saturation_liquid = PropsSI('H', 'P', pressure_saturation, 'Q', 0, ref)
h_saturation_vapor = PropsSI('H', 'P', pressure_saturation, 'Q', 1, ref)
plt.plot(h_saturation_liquid, pressure_saturation, 'k--', label='Saturation Line')
plt.plot(h_saturation_vapor, pressure_saturation, 'k--')

plt.xlabel('Enthalpy (J/kg)')
plt.ylabel('Pressure (Pa)')
plt.title('p-h Diagram for All Test Cycles')
plt.grid()
plt.legend()
plt.show()

#### Compression Work ####

Wc=np.zeros(5)

for i in range (0,5,1):
    Wc[i]= mref[i]*(h2[i]-h1[i])/3600
    print(Wc[i])

plt.figure(figsize=(10, 6))
plt.plot(Tcool_in, Wc, 'o-', label='Compressor Work', color='blue')
plt.plot(Tcool_in, We, 's-', label='Electrical Consumption', color='red')
plt.xlabel('Secondary Inlet Temperature of the Condenser (°C)')
plt.ylabel('Power (W)')
plt.title('Compressor Work vs Electrical Consumption')
plt.legend()
plt.grid()
plt.show()

#### Qc vs Qh and COP ####

Qc=np.zeros(5)
Qh=np.zeros(5)
COP=np.zeros(5)

for i in range (0,5,1):
    Qc[i]=mref[i]*(h3[i]-h4[i])/3600
    Qh[i]=mcool[i]*cpcool[i]*(Tcool_out[i]-Tcool_in[i])
    COP[i]= Qc[i]/(Wc[i]+Wf)

    print(Qc[i])
    print(Qh[i])
    print(COP[i])



plt.figure(figsize=(10, 6))
plt.plot(Tcool_in, Qc, 'o-', label='Heating Power for Refrigerant', color='blue')
plt.plot(Tcool_in, Qh, 's-', label='Heating Power for Coolant', color='red')
plt.xlabel('Secondary Inlet Temperature of the Condenser (°C)')
plt.ylabel('Heating Power (W)')
plt.title('Heating Power for Refrigerant vs Coolant')
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(Tcool_in, COP, 'x-', label='COP', color='green')
plt.xlabel('Secondary Inlet Temperature of the Condenser (°C)')
plt.ylabel('COP')
plt.title('Coefficient of Performance vs Secondary Inlet Temperature')
plt.legend()
plt.grid()
plt.show()
