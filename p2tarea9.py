##############################################################################
##############################################################################
'''
Metodos Numericos para la Ciencia e Ingenieria
FI3104-1
Tarea 9
Maximiliano Dirk Vega Aguilera
18.451.231-9
P2 datos de supernovas I
'''
##############################################################################
##############################################################################

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import os
np.random.seed(24)

##############################################################################
##############################################################################
# funciones


def llamar_archivo(nombre):
    '''
    Lee los datos
    '''
    cur_dir = os.getcwd()
    arch = np.loadtxt(os.path.join(cur_dir, 'data', nombre), usecols=(1, 2))
    x = arch[:, 0]
    y = arch[:, 1]
    return x, y


def s_ij(x, y=False):
    '''
    Calcula los S_ij para el ajuste lineal (S definidos en el informe)
    '''
    s = 0
    if y is False:
        for i in range(len(x)):
            s += x[i]
        return s
    for i in range(len(x)):
        s += x[i] * y[i]
    return s


def lineal(x, b):
    '''
    y=a+bx considerando a=0
    '''
    return b * x


def ajuste_manual(x, y):
    '''
    Calcula la pendiente b a partir de la minimizacion de chi**2
    '''
    b = s_ij(x, y) / s_ij(x, x)
    return b


def crear_muestra_sintetica(x,y):
    '''
    crea muestra sintetica a partir de la muestra original x,y
    '''
    N = len(x)
    xs = np.zeros(N)
    ys = np.zeros(N)
    for i in range(N):
        j = int(np.random.uniform(0,N-1))
        xs[i] = x[j]
        ys[i] = y[j]
    return xs, ys


def b_biseccion(b1,b2):
    '''
    calcula la pendiente de una recta entre las dos curvas de pendientes
    b1 y b2
    '''
    b = (b1 * b2 - 1 + np.sqrt((1 + b1**2) * (1 + b2**2))) / (b1 + b2)
    return b


##############################################################################
##############################################################################

y, x = llamar_archivo('SNIa.dat')

N = len(x)  # largo de la muestra
Nb = N**2   # numero de muestras sinteticas a tomar

b = np.zeros(Nb)  # arreglo para guardar los b_biseccion de cada muestra sintetica
for i in range(Nb):  # se desarrolla el metodo de Bootstap
    xs, ys = crear_muestra_sintetica(x,y)
    b1 = ajuste_manual(xs, ys)
    b2 = ajuste_manual(ys, xs)
    b2 = 1. / b2
    b[i] = b_biseccion(b1,b2)

# se calcula el intervalo de confianza al 95%
b_values = np.sort(b)
limite_bajo = b_values[int(Nb * 0.025)]
limite_alto = b_values[int(Nb * 0.975)]
print "El intervalo de confianza al 95% es: [{}:{}]".format(limite_bajo, limite_alto)

b1dato = ajuste_manual(x, y)
b2dato = ajuste_manual(y, x)
b2dato = 1. / b2
bdato = b_biseccion(b1,b2)

plt.plot(x, lineal(x, limite_bajo), 'g--')
plt.plot(x, lineal(x, limite_alto), 'r--')
plt.plot(x, lineal(x, bdato), 'b-')
plt.plot(x, y, '^')
plt.title('Velocidad de recesion a partir de la distancia')
plt.axis([50, 480, 2500, 35000])
plt.xlabel('Distancia [Mpc]')
plt.ylabel('Velocidad [km/s]')
plt.show()
