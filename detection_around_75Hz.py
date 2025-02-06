# -*- coding: utf-8 -*-
"""
Created by Maximiliano Anzibar Fialho - 2024

Running this script will compute the prominance of 75Hz amplitud in the spectrum regarding a mean value of an interval around 75Hz.



@author: manzibar
"""

import numpy as np
from scipy.fft import fft
from scipy import signal
import time
from scipy.io import wavfile
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True #para que interprete Latex
plt.close('all')


# Implement low pass filter
def filtro_pasabajo(data,samplerate,orden,frec_corte):
    
    b, a = signal.butter(orden,frec_corte,'low',fs=samplerate)
    data_filt = signal.lfilter(b, a, data)
    return data_filt
    
# Take the mean spectrum of different intervals of the signal
def promedio_espectros(data,samplerate,N): #N is the amount of interval into which the signal is cut
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
    
    return [FFT, FREC]

# Compute the prominance of 75Hz frequency amplitude
def entorno_75Hz(espectro,frecuencias,l,L): #2*l y 2*L es el largo total (en puntos) de los intervalos chicos y grandes respectivamente
    frec_round = np.round(frecuencias)
    indice = np.where(frec_round==150)
    indice = indice[0][0]
    
    entorno_chico = espectro[indice-l:indice+l]
    dB_entorno_chico = np.mean(entorno_chico)    
    entorno_grande = espectro[indice-L:indice+L]
    dB_entorno_grande = np.mean(entorno_grande)
        
    diferencia = abs(abs(dB_entorno_chico) - abs(dB_entorno_grande)) 
    
    return diferencia
    
    
    
    
#%% ******* MAIN LOOP *****
# Loop through the files to compute the desired magnitud 

import os
directorio_locacion = 'D:/Antartida/CAV 2022-2023/Compu Pasteur/2022-2023/Faro/Enero/Base de datos' # Put here the directory with the audio files
fechas = os.listdir(directorio_locacion)

MAT_DIF = np.zeros((len(fechas),24))


for KK in range(len(fechas)):
    horas = os.listdir(directorio_locacion + '/' + fechas[KK])
    
    for JJ in range(len(horas)):
        hora = horas[JJ]
        samplerate, data = wavfile.read(directorio_locacion + '/' + fechas[KK] + '/' + hora)
        
        data_filt = filtro_pasabajo(data,samplerate,10,1000)
        [FFT,FREC] = promedio_espectros(data_filt,samplerate,100)
        plt.close()
        MAT_DIF[KK,JJ] = entorno_75Hz(FFT,FREC,3,50)
        plt.close()
    
    print(fechas[KK])

# ------- PLOT ------
vect_horas = np.linspace(0,23,24)
plt.figure(figsize=(15,8))
plt.rcParams.update({'font.size': 18})
plt.pcolor(vect_horas,np.arange(0,len(fechas)),MAT_DIF)
plt.yticks(np.arange(len(fechas)), fechas)
plt.xticks(vect_horas)
cbar = plt.colorbar()
cbar.set_label(r'$<I_{small75}>-<I_{big75}>$', rotation=270, labelpad=25)
plt.clim(0,20)
plt.xlabel('UTC Time')
plt.ylabel('Dates')
# plt.title('Entorno de 75Hz')
ax = plt.gca()
ax.invert_yaxis()
   

#%% SAVE

list_save = []
list_save.append(MAT_DIF)
list_save.append(np.arange(0,24))
list_save.append(fechas)

# Save the data in a numpy array
#np.save('D:/CAV/2022-2023/Faro/Enero/FARO_ENERO.npy', np.array(list_save, dtype=object), allow_pickle=True)



    
    