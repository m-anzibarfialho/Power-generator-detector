# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 15:43:31 2023

@author: manzibar
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

plt.close('all')

#FIGURA 1

from scipy.io import wavfile
from scipy.fft import fft
samplerate, data = wavfile.read('./generador_foreground.wav') #path for the file containing the on-site generator recording

#------- FFT ---------

L = len(data)
print('Duración del audio en segundos:')
print(L/samplerate)

def promedio_espectros(data,samplerate,N): #N: the amount of intervals in which the signal is splited
    L=len(data)
    count = 0
    L_intervalo = round(L // N)
    FFT_inter = []

    for ii in range(N):
        vect = data[count * L_intervalo : (count + 1) * L_intervalo]
        VECT = fft(vect)
        P2 = abs(VECT/len(vect));
        P1 = P2[:len(vect)//2+1];
        FFT_inter.append(P1)
               
        count += 1

    FFT = np.mean(FFT_inter, axis=0)
    FFT = 20*np.log10(FFT/max(FFT)) #20dB porque es voltaje
    FREC = (samplerate/L_intervalo)*np.arange(0,L_intervalo/2+1)
    
    # plt.figure()
    # plt.xlim((0,500))
    # plt.ylim((-50,0))
    # plt.xlabel('Frecuencia (Hz)')
    # plt.ylabel('dB')
    # plt.title('Espectro promediado')
    # plt.plot(FREC,FFT)
    
    return [FFT, FREC]


[FFT,FREC] = promedio_espectros(data,samplerate,100)

print('The frequency resolution is: ')
print(np.diff(FREC)[0])


fig,ax = plt.subplots(figsize=(10,7))
plt.rcParams.update({'font.size': 15})

ax.plot(FREC,FFT,color='black')
ax.set_xlabel('Frequency (Hz)',fontsize=20)
ax.set_ylabel('Amplitude(dB)',fontsize=20)
ax.set_ylim((-75,5))
ax.set_xlim((0,5000))
plt.savefig('espectro_dB.png', format='png', dpi=600)

ax_zoom = fig.add_subplot()
ax_zoom.plot(FREC,FFT,color='black')
ax_zoom.set_ylim((-50,5))
ax_zoom.set_xlim((0,500))
ax_zoom.set_position([0.45,0.5,0.4,0.3])
# ax_zoom.set_edgecolor('r')
ax_zoom.spines['bottom'].set_color('red')
ax_zoom.spines['top'].set_color('red')
ax_zoom.spines['left'].set_color('red')
ax_zoom.spines['right'].set_color('red')
# change all spines
for axis in ['top','bottom','left','right'] :
    ax_zoom.spines[axis].set_linewidth(2)

ax_zoom.plot(75,0, '.', color='Blue', markersize=15)
ax_zoom.text(0.25, 0.9, '75Hz', horizontalalignment='center', verticalalignment='center', transform=ax_zoom.transAxes, fontsize=13)

#--
rectangulo = plt.Rectangle(xy=(0.001,0.4), width=0.2, height=0.55, facecolor='white', edgecolor='Red', linewidth = 2, transform=ax.transAxes)
ax.add_patch(rectangulo)

# plt.savefig('./generator_spectrum.png',dpi=1000) # save image

#%% Spectrograma

frec_espect, t_espect, Sxx = signal.spectrogram(data, samplerate,nperseg=2**16)
Sxx_dB = 10*np.log10(Sxx/np.max(Sxx)) # paso espectrograma a dB

fig2, ax2 = plt.subplots(figsize=(15,8))
sp = ax2.pcolormesh(t_espect, frec_espect, Sxx_dB, shading='gouraud',vmin=-60, vmax=0, cmap='gray')
ax2.set_ylabel('Frequency (Hz)',fontsize=20)
ax2.set_xlabel('Time (sec)',fontsize=20)
ax2.set_ylim((0,500))
c = plt.colorbar(sp, ax=ax2)
c.set_label('Intensity (dB)',fontsize=20)

rectangulo_spectro = plt.Rectangle(xy=(0.001,0.165), width=1.3, height=0.05, facecolor=(0,0,0,0), edgecolor='Red', linestyle='--', linewidth = 2, transform=ax.transAxes)
ax2.add_patch(rectangulo_spectro)

# plt.savefig('C:/Users/Maximiliano/Desktop/Antártida PAPER/generador_espectrograma.png',dpi=1000)
#%% FIND MAX FREQUENCY

print('El valor máximo de frequencia se da en:')
Frec_max = FREC[np.where(FFT==0)[0][0]]
print(Frec_max)



#relación con el primer armónico
armonico_1 = np.round(Frec_max*2)
print('1er armónico:')
print(armonico_1)


difference_array = np.absolute(FREC-armonico_1)
index = difference_array.argmin()
armonico_1_dB = FFT[index]
print('Amplitud 1er armónico:', armonico_1_dB)

#relación con el segundo armónico
armonico_2 = np.round(Frec_max*3)
print('2do armónico:')
print(armonico_2)

difference_array = np.absolute(FREC-armonico_2)
index = difference_array.argmin()
armonico_2_dB = FFT[index]
print('Amplitud 2do armónico:', armonico_2_dB)


def entorno_frecuencia(espectro,frecuencias,l,L,TARGET): #2*l y 2*L are the total length (points) of small and big intervals respectively
    frec_round = np.round(frecuencias)
    indice = np.where(frec_round==TARGET)
    indice = indice[0][0]
    
    entorno_chico = espectro[indice-l:indice+l]
    dB_entorno_chico = np.max(entorno_chico)    
    entorno_grande = espectro[indice-L:indice+L]
    dB_entorno_grande = np.mean(entorno_grande)
    
    print('dB_entorno_chico:', dB_entorno_chico)
    print('dB_entorno_grande:', dB_entorno_grande)
    
    plt.figure()
    plt.plot(frecuencias,espectro)
    plt.xlim((0,500))
    plt.plot(frecuencias[indice-L:indice+L],entorno_grande,'r')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('dB')
    
    diferencia = abs(abs(dB_entorno_chico) - abs(dB_entorno_grande)) 
    
    return diferencia


DIF = entorno_frecuencia(FFT,FREC,3,50,75)
print('Dif 1er armónico:  ', DIF)


#%% 
plt.figure(10, figsize=(10,7))
plt.plot(FREC,FFT,color='black')
plt.set_ylim((-50,5))
plt.set_xlim((0,500))
plt.plot(75,0, '.', color='Blue', markersize=15)
plt.text(0.25, 0.9, '75Hz', horizontalalignment='center', verticalalignment='center', transform=ax_zoom.transAxes, fontsize=13)
