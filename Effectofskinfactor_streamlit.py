import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title('Effect of Formation Damage on Pressure Profile')
st.sidebar.title('Inputs')

A = st.sidebar.number_input('Reservoir Area (acres)', min_value=1.0, value=100.0)
re = np.sqrt(43560 * A / 3.14)
rw = st.sidebar.number_input('Wellbore Radius (ft)', min_value=0.1, value=1.0)
pe = st.sidebar.number_input('Pressure at Reservoir Boundary (psi)', min_value=0.0, value=3000.0)
Bo = st.sidebar.number_input('Oil Formation Volume Factor', min_value=0.1, value=1.0)
q = st.sidebar.number_input('Oil Flowrate (STB/Day)', min_value=0.0, value=1000.0)
k = st.sidebar.number_input('Permeability (mD)', min_value=0.1, value=100.0)
h = st.sidebar.number_input('Payzone Thickness (ft)', min_value=1.0, value=10.0)
mu = st.sidebar.number_input('Oil Viscosity (cP)', min_value=0.1, value=1.0)

r = np.linspace(rw, 50, 500)
p = []
for i in r:
    a = pe - (141.2 * q * mu * Bo * (np.log(re / i)) / k / h)
    p.append(a)
Pressures_Ideal = np.array(p).T
Radius = r.reshape(500, 1)


def calculate_pressure_profile(skin):
    rskin = np.linspace(rw, 3, 500)
    P = []
    for i in rskin:
        a = pe - (141.2 * q * mu * Bo * (np.log(re / i) + skin) / k / h)
        P.append(a)
    A = np.array(P)
    rSkin = np.append(rskin, 10)
    Pressure_Skin = np.append(A, pe - (141.2 * q * mu * Bo * (np.log(re / 10)) / k / h))
    return rSkin, Pressure_Skin


skin = st.slider('Formation Damage (Skin)', min_value=0.5, max_value=5.0, value=1.0)
rSkin, Pressure_Skin = calculate_pressure_profile(skin)

plt.style.use('fivethirtyeight')
plt.figure(figsize=(14, 8))
plt.plot(rSkin, Pressure_Skin, label="Damaged (Skin) Pressure Profile")
plt.plot(Radius, Pressures_Ideal, label="Ideal Pressure Profile")
plt.xlim(rw + 0.5, 50)  # To show the line attached to Y Axis
plt.ylim(900, 3100)
plt.axvspan(0, 10, alpha=0.2, label='Damaged Zone', color='yellow')
plt.axvspan(10, 50, alpha=0, label='Undamaged Zone')
plt.xlabel('Distance from center of well "r" (ft)')
plt.ylabel('Pressure at distance "r" P(r), psi')
plt.title('Effect of Formation Damage (Skin) on Pressure Profile near Wellbore')
plt.legend(loc='best')
plt.grid(True)

st.pyplot(plt)
