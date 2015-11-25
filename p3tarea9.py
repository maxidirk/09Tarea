##############################################################################
##############################################################################
'''
Metodos Numericos para la Ciencia e Ingenieria
FI3104-1
Tarea 9
Maximiliano Dirk Vega Aguilera
18.451.231-9
'''
##############################################################################
##############################################################################

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import os
np.random.seed(25)

##############################################################################
##############################################################################
# funciones


def llamar_archivo(nombre):
    '''
    Lee los datos
    '''
    cur_dir = os.getcwd()
    arch = np.loadtxt(os.path.join(cur_dir, 'data', nombre),
                      usecols=(80, 81, 82, 83))
    w = arch[:, 0]
    x = arch[:, 1]
    y = arch[:, 2]
    z = arch[:, 3]
    return w, x, y, z

def lineal(x, b, a):
    '''
    y=a+bx considerando a y b distintos de cero
    '''
    return a + b * x

def crear_muestra_sintetica(x, y, error_x, error_y):
    '''
    crea muestra sintetica a partir de la muestra original x,y y sus errores
    mediante el metodo de simulacion de Monte Carlo
    '''
    N = len(x)
    xs = np.zeros(N)
    ys = np.zeros(N)
    for i in range(N):
        xs[i] = np.random.normal(loc=x[i], scale=error_x[i])
        ys[i] = np.random.normal(loc=y[i], scale=error_y[i])
    return xs, ys


##############################################################################
##############################################################################
banda_i, error_i, banda_z, error_z = llamar_archivo('DR9Q.dat')

banda_i = banda_i / 3.631  # se transforman a unidades de microJy
error_i = error_i / 3.631  # se transforman a unidades de microJy
banda_z = banda_z / 3.631  # se transforman a unidades de microJy
error_z = error_z / 3.631  # se transforman a unidades de microJy

N = len(banda_i)  # largo de la muestra
Nb = int(N*np.log(N)**2)   # numero de muestras sinteticas a tomar

b = np.zeros(Nb)  # arreglo para guardar los b de cada muestra sintetica
a = np.zeros(Nb)  # arreglo para guardar los a de cada muestra sintetica
for i in range(Nb):
    bis, bzs = crear_muestra_sintetica(banda_i, banda_z, error_i, error_z)
    b1, a1 = np.polyfit(bis, bzs, 1)  # paremetros del ajuste lineal
    b[i] = b1
    a[i] = a1

b_values = np.sort(b)
limite_bajo_b = b_values[int(Nb * 0.025)]
limite_alto_b = b_values[int(Nb * 0.975)]
print "El intervalo de confianza al 95% para \
       b es: [{}:{}]".format(limite_bajo_b, limite_alto_b)

a_values = np.sort(a)
limite_bajo_a = a_values[int(Nb * 0.025)]
limite_alto_a = a_values[int(Nb * 0.975)]
print "El intervalo de confianza al 95% para \
       a es: [{}:{}]".format(limite_bajo_a, limite_alto_a)

bdato, adato = np.polyfit(banda_i, banda_z, 1)
print 'b y a del ajuste de los datos: b=', bdato,' a= ', adato


plt.plot(banda_i, lineal(banda_i, limite_bajo_b, limite_bajo_a), 'g--')
plt.plot(banda_i, lineal(banda_i, limite_alto_b, limite_alto_a), 'r--')
plt.plot(banda_i, lineal(banda_i, bdato, adato), 'b-')
plt.errorbar(banda_i, banda_z, xerr=error_i, yerr=error_z, fmt='^')
plt.axis([0., 35., 0., 35.])
plt.title('Banda i vs Banda z')
plt.xlabel('Banda i [$\mu Jy$]')
plt.ylabel('Banda z [$\mu Jy$]')
plt.show()
