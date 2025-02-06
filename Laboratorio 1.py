import wfdb
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.stats import gaussian_kde

# Cargar la información
senal = wfdb.rdrecord("emg_myopathy")

# Obtener los valores de la señal
informacion = senal.p_signal[:, 0]  # Solo el primer canal

# Número total de muestras
tamano = senal.sig_len

# Definir el fragmento que se ampliará 
inicio = 20000
fin = 25000
datos_ampliados = informacion[inicio:fin]

# Graficar la señal completa
plt.figure(figsize=(12, 5))
plt.plot(informacion, label="Señal completa", color='b')
plt.title('Señal EMG de Myopatía')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [mV]')
plt.legend()
plt.show()

# Graficar la señal ampliada
plt.figure(figsize=(12, 5))
plt.plot(range(inicio, fin), datos_ampliados, label="Fragmento ampliado", color='r')
plt.title('Fragmento ampliado de la señal EMG')
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [mV]')
plt.legend()
plt.show()


# MEDIA DE LA SEÑAL:
# Calculo la media de la señal sin función
suma_informacion = 0 #Comenzamos con la suma en 0.
for valor_informacion in datos_ampliados:  # Recorremos cada valor de los datos
    suma_informacion += valor_informacion  # Sumar cada valor a la suma total
num_informacion = len(datos_ampliados)   #  cuántos valores hay
media = suma_informacion / num_informacion
print(f"Media de la señal (Sin función): {media}")

# Calculo la media de la señal con función
media_numpy = np.mean(datos_ampliados)
print(f"Media de la señal (Con función): {media_numpy}")

# DESVIACIÓN ESTÁNDAR:
# Calculo la desviación de la señal sin función
# 1. Calcular la media 
suma_informacion = 0
for valor_informacion in datos_ampliados:  # Recorremos cada valor de los datos
    suma_informacion += valor_informacion  # Sumar cada valor a la suma total
num_informacion = len(datos_ampliados)
media = suma_informacion / num_informacion

# 2. Calcular la suma de las diferencias al cuadrado
diferencia_al_cuadrado = 0  # Inicializamos la variable para almacenar la suma de las diferencias al cuadrado
for valor_informacion in datos_ampliados:  # Recorremos cada valor de los datos
    diferencia = valor_informacion - media  # Calculamos la diferencia entre el valor y la media
    diferencia_al_cuadrado += diferencia ** 2  # Sumamos el cuadrado de esa diferencia

# 3. Dividir por el número de valores
varianza = diferencia_al_cuadrado / num_informacion

# 4. Calcular la raíz cuadrada de la varianza (desviación estándar)
desviacion_estandar = math.sqrt(varianza)
print(f"Desviación estándar de la señal (Sin función): {desviacion_estandar}")

# Calculo la desviación estándar de la señal usando la función
desviacion_estandar_numpy = np.std(datos_ampliados)
print(f"Desviación estándar de la señal (Con función): {desviacion_estandar_numpy}")

# COEFICIENTE DE VARIACIÓN
# Calculo el coeficiente de variación de la señal sin función
coeficiente_variacion = (desviacion_estandar / media) * 100
print(f"Coeficiente de variación de la señal (Sin función): {coeficiente_variacion}%")

# Calculo el coeficiente de variación de la señal usando la función
coeficiente_variacion_numpy = (desviacion_estandar_numpy / media_numpy) * 100
print(f"Coeficiente de variación de la señal (Con función): {coeficiente_variacion_numpy}%")

# HISTOGRAMA Y FUNCIÓN DE PROBABILIDAD 
num_datos = len(datos_ampliados)  # Número total de datos
k = int(1 + 3.322 * np.log10(num_datos))  # Calcular número de bins (Regla de Sturges)

# Definir los límites de los bins
valor_min = np.min(datos_ampliados)  # Mínimo valor
valor_max = np.max(datos_ampliados)  # Máximo valor

# Calculo del tamaño de cada bin (ancho de los bins)
ancho_bin = (valor_max - valor_min) / k

# Límites de cada bin
bins = np.linspace(valor_min, valor_max, k + 1)

# Conteo cuántos valores caen en cada bin
conteo_histograma = np.zeros(k)  # Inicializamos el contador de cada bin

# Conteo de cuántos valores caen en cada bin
for valor in datos_ampliados:
    for i in range(k):
        if bins[i] <= valor < bins[i + 1]:
            conteo_histograma[i] += 1
            break

# Calculo de las marcas de clase
centros_bins = bins[:-1]

# Estimación de la función de probabilidad con KDE
kde = gaussian_kde(datos_ampliados)  # Estimador de densidad por Kernel
valores_x = np.linspace(valor_min, valor_max, 1000)  # Rango de valores para la estimación
valores_y = kde(valores_x)  # Estimación de la PDF

# Graficar el histograma manualmente
plt.figure(figsize=(12, 5))

# Graficar el histograma con barras y agregar el label
histograma_barras = plt.bar(bins[:-1], conteo_histograma, width=ancho_bin, color='yellow', edgecolor='black', alpha=0.6)
# Asignar el label directamente a la barra


# Graficar las marcas de clase sobre el histograma y agregar el label
marcas_clase = plt.scatter(centros_bins, conteo_histograma, color='red', zorder=5, marker='o')


# Conectar las marcas de clase con una línea y agregar el label
linea_conexion = plt.plot(centros_bins, conteo_histograma, color='blue', linewidth=2)
# Asignamos label a la línea de conexión


# Graficar la función de probabilidad sobre el histograma y agregar el label
funcion_probabilidad = plt.plot(valores_x, valores_y, color='orange', linewidth=2)

# Etiquetas en el eje horizontal (rango de los bins)
plt.xticks(bins, rotation=45)

# Títulos y etiquetas
plt.title('Histograma y Función de Probabilidad de la señal EMG')
plt.xlabel('Voltaje [mV]')
plt.ylabel('Frecuencia / Densidad de Probabilidad')
plt.grid(True)

plt.legend()

# Mostrar la gráfica
plt.show()







# HISTOGRAMA CON FUNCIÓN (plt.hist())
plt.figure(figsize=(12, 5))

# Graficar el histograma
plt.hist(datos_ampliados, bins=k, color='yellow', edgecolor='black', density=True, alpha=0.6)

# Obtener los límites de los bins y centros
bordes_bins = np.histogram(datos_ampliados, bins=k)[1]
ancho_bin = bordes_bins[1] - bordes_bins[0]
centros_bins = bordes_bins[:-1] + ancho_bin / 2

# Función de densidad de probabilidad a partir del histograma
conteo_histograma, _ = np.histogram(datos_ampliados, bins=bordes_bins, density=True)

# Graficar la función de probabilidad sobre el histograma
plt.plot(centros_bins, conteo_histograma, color='orange', linewidth=2)

# Puntos de clase (rojos) sobre la función de probabilidad
plt.scatter(centros_bins, conteo_histograma, color='red', zorder=5, marker='o')

# Título y etiquetas
plt.title('Histograma de la señal EMG (Fragmento) - Con Función')
plt.xlabel('Voltaje [mV]')
plt.ylabel('Frecuencia / Densidad de Probabilidad')
plt.grid(True)

# Mostrar leyenda
plt.legend()

# Mostrar la gráfica
plt.show()





# Función para calcular SNR correctamente
def calcular_snr(signal, ruido):
    # Calcular la potencia de la señal y del ruido
    potencia_signal = np.mean(signal**2)
    potencia_ruido = np.mean(ruido**2)
    
    # Asegurarse de que no haya división por cero (evitar valores infinitos)
    if potencia_ruido == 0:
        return np.nan  # Retornar NaN si la potencia del ruido es cero
    
    # Calcular el SNR en dB
    snr = 10 * np.log10(potencia_signal / potencia_ruido)
    return snr

# CONTAMINACIÓN CON DIFERENTES TIPOS DE RUIDO
ruidos = {
    "Ruido Gaussiano Bajo": np.random.normal(0, np.std(datos_ampliados) * 0.5, len(datos_ampliados)),
    "Ruido Gaussiano Alto": np.random.normal(0, np.std(datos_ampliados) * 2, len(datos_ampliados)),
    "Ruido Impulsivo Bajo": (np.random.rand(len(datos_ampliados)) < 0.01) * np.max(np.abs(datos_ampliados)) * 2 * (2 * np.random.randint(0, 2, len(datos_ampliados)) - 1),
    "Ruido Impulsivo Alto": (np.random.rand(len(datos_ampliados)) < 0.02) * np.max(np.abs(datos_ampliados)) * 5 * (2 * np.random.randint(0, 2, len(datos_ampliados)) - 1),
    "Ruido Artefacto Bajo": np.max(np.abs(datos_ampliados)) * 0.5 * np.sin(2 * np.pi * 0.1 * np.arange(len(datos_ampliados))),
    "Ruido Artefacto Alto": np.max(np.abs(datos_ampliados)) * 2 * np.sin(2 * np.pi * 0.1 * np.arange(len(datos_ampliados))),
}

for ruido_tipo, ruido in ruidos.items():
    valores_contaminados = datos_ampliados + ruido
    
    # Calcular el SNR con la nueva función
    snr = calcular_snr(datos_ampliados, ruido)
    
    # Imprimir el valor de SNR
    print(f"{ruido_tipo}: SNR = {snr:.2f} dB")
    
    # Grafica la señal contaminada
    plt.figure(figsize=(12, 5))
    plt.plot(valores_contaminados, label=f"{ruido_tipo}", color=np.random.rand(3,))
    plt.title(f'Señal Contaminada con {ruido_tipo}')
    plt.xlabel('Tiempo(s)')
    plt.ylabel('Voltaje [mV]')
    plt.legend()
    plt.show()