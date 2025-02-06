Laboratorio 1: Análisis estadístico de la señal

Este proyecto analiza una señal de electromiografía (EMG) de una persona con miopatía. Se realizan visualizaciones de la señal, cálculos estadísticos y una ampliación de un segmento específico para un análisis más detallado.

El código carga una señal EMG desde un archivo, la visualiza y cálcula estadísticas importantes como la media, desviación estándar y coeficiente de variación. Se usa un fragmento de la señal para análisis detallado. 

- Requisitos para utilizar el spyder: Asegurarse de tener bien instaladas las siguientes librerias en tu programa:
  * Wfdb (Para leer archivos de señales fisiológicas)
  * Matplotlib (Para visualizar la señal)
  * Numpy (Para cálculos numéricos)
  * Scipy (Para estadísticas avanzadas)
 
- Instalación:
  Si no tienes alguna de las anteriores librerias mencionadas, puedes hacerlo manualmente de la siguiente manera:
  
  Ej: pip install wfdb

- Uso:
  1. Descarga el archivo de la señal: Asegurate de tener el archivo "emg_myophaty" en la misma carpeta donde está el script.
  2. Ejecuta el script: Guarda el código en un archivo Python, por ejemplo, *analisis_emg.py*
     
     Luego, ejecuta el script con: python analisis_emg.py
  3. Interpreta los resultados: Se generarán dos gráficos
     * La señal completa de EMG.
     * Un fragmento ampliado para análisis detallado.

- Explicación del código:
  1. Cargar la señal EMG:
     - Aquí se lee el archivo y se selecciona el primer canal de la señal.
       
     signal = wfdb.rdrecord("emg_myopathy")
     
     info = signal.p_signal[:, 0]
  2. Para graficar la señal completa.
     - Esto dibuja la señal completa en un gráfico para su fácil visualización
       
     plt.figure(figsize=(12, 5))
     
     plt.plot(info, label="Señal completa", color='b')
     
     plt.title('Señal EMG de Myopatía')
     
     plt.xlabel('Tiempo [s]')
     
     plt.ylabel('Voltaje [mV]')
     
     plt.legend()
     
     plt.show()
  
  3. Para ampliar el fragmento de la señal:
     - Se selecciona un fragmento de la señal entre los rangos de 20.000 y 25.000 (Esto es a elección).
       
       inicio = 20000
       
       fin = 25000
       
       datos_ampliados = info[inicio:fin]
       
  4. Para calcular estadísticas:
     
     - Media (Promedio): Es importante porque permite resumir un conjunto de datos en un solo valor, lo que facilita el análisis de la información. Ambas fromas calculan el promedio de la señal
     
        * Sin función:
     
        suma_info = 0
     
        for valor in datos_ampliados:
     
        suma_info += valor
     
        media = suma_info / len(datos_ampliados)

        * Con función de Numpy:
          
        media_numpy = np.mean(datos_ampliados)
       
     - Desviación estandar: Es una medida que indica la dispersión de un conjunto de datos. Es importante calcularla porque ayuda a entender cómo se distribuyen los datos y mide la dispesión de los valores. 
     
        * Sin función:
          
        diferencia_al_cuadrado = 0
       
        for valor in datos_ampliados:
       
        diferencia_al_cuadrado += (valor - media) ** 2
       
        varianza = diferencia_al_cuadrado / len(datos_ampliados)
       
        desviacion_estandar = math.sqrt(varianza)

        * Con función de Numpy:
          
        desviacion_estandar_numpy = np.std(datos_ampliados)

      - Coeficiente de variación: Es útil para comparar la variabilidad entre diferentes conjuntos de datos.
     
        * Sin función:
          
        coeficiente_variacion = (desviacion_estandar / media) * 100

        * Con función de Numpy:
          
        coeficiente_variacion_numpy = (desviacion_estandar_numpy / media_numpy) * 100

      - Resultados: Después de ejecutar el código, verás algo como esto en la consola:
        
        ![Imagen de WhatsApp 2025-02-05 a las 23 06 20_c476f9be](https://github.com/user-attachments/assets/387f0fd8-94b3-4b9c-b923-880713c04341)   

        Fig 1. Pantallazo de la consola con los valores

    Y se mostrarán dos gráficos:

    - Grafico 1: Toda la señal EMG
      
  ![Imagen de WhatsApp 2025-02-05 a las 22 18 41_b43309b8](https://github.com/user-attachments/assets/87a64d7e-0996-4366-8180-6409888e09cd)
   
    Fig 2. Señal EMG de Myopatia

    - Grafico 2: Un segmento ampliado de la señal
      
  ![Imagen de WhatsApp 2025-02-05 a las 22 19 08_540374a2](https://github.com/user-attachments/assets/a1734bc4-04a3-47cd-abe4-eb60ceca6a8d)
   
    Fig 3. Fragmento ampliado de la señal EMG

  5. Histograma y Función de Probabilidad
     - Se aplica la Regla de Sturges para determinar el número de bins:
       
       k = int(1 + 3.322 * np.log10(len(datos_ampliados)))

     - Después, se calculan los bins, las marcas de clase y la función de densidad de probabilidad con Kernel Density Estimation (KDE).

       kde = gaussian_kde(datos_ampliados)
       
       valores_x = np.linspace(np.min(datos_ampliados), np.max(datos_ampliados), 1000)
       
       valores_y = kde(valores_x)

     - Finalmente, se grafica el histograma y la función de probabilidad.
    
       plt.figure(figsize=(12, 5))
       
       plt.bar(bins[:-1], conteo_histograma, width=ancho_bin,       color='yellow', edgecolor='black', alpha=0.6)
       
       plt.plot(valores_x, valores_y, color='orange', linewidth=2)
       
       plt.title('Histograma y Función de Probabilidad de la señal EMG')
       
       plt.xlabel('Voltaje [mV]')
       
       plt.ylabel('Frecuencia / Densidad de Probabilidad')
       
       plt.grid(True)
       
       plt.show()

  6. Ruido y Relación Señal-Ruido (SNR)
     - Se define una función para calcular la relación señal-ruido en decibeles.

       def calcular_snr(signal, ruido):
       
       potencia_signal = np.mean(signal**2)
       
       potencia_ruido = np.mean(ruido**2)
       
       if potencia_ruido == 0:
       
       return np.nan
       
       return 10 * np.log10(potencia_signal / potencia_ruido)

Luego, se contamina la señal con diferentes tipos de ruido y se calcula el SNR.

  * Ruido Gaussiano:
     
     "Ruido Gaussiano Bajo": np.random.normal(0, np.std(datos_ampliados) * 0.5, len(datos_ampliados)),
     
     "Ruido Gaussiano Alto": np.random.normal(0, np.std(datos_ampliados) * 2, len(datos_ampliados)),
     
  * Ruido Impulsivo:

     "Ruido Impulsivo Bajo": (np.random.rand(len(datos_ampliados)) < 0.01) * np.max(np.abs(datos_ampliados)) * 2,
     
     "Ruido Impulsivo Alto": (np.random.rand(len(datos_ampliados)) < 0.02) * np.max(np.abs(datos_ampliados)) * 5,
     
  * Ruido de Artefactos:

     "Ruido Artefacto Bajo": np.max(np.abs(datos_ampliados)) * 0.5 * np.sin(2 * np.pi * 0.1 * np.arange(len(datos_ampliados))),
     
     "Ruido Artefacto Alto": np.max(np.abs(datos_ampliados)) * 2 * np.sin(2 * np.pi * 0.1 * np.arange(len(datos_ampliados))),
    

   - Para cada tipo de ruido, se calcula el SNR e imprime en consola:

   for ruido_tipo, ruido in ruidos.items():
    
   valores_contaminados = datos_ampliados + ruido
    
   snr = calcular_snr(datos_ampliados, ruido)
    
   print(f"{ruido_tipo}: SNR = {snr:.2f} dB")
   

   - Finalmente, se grafican las señales contaminadas con ruido:

   plt.figure(figsize=(12, 5))
    
   plt.plot(valores_contaminados, label=f"{ruido_tipo}", color=np.random.rand(3,))
    
   plt.title(f'Señal Contaminada con {ruido_tipo}')
    
   plt.xlabel('Tiempo(s)')
    
   plt.ylabel('Voltaje [mV]')
    
   plt.legend()
    
   plt.show()


   - Resultados:

     * Histogramas y función de densidad de la probabilidad:
       
       ![Imagen de WhatsApp 2025-02-05 a las 22 29 35_928330ce](https://github.com/user-attachments/assets/62caf9ab-4b56-4294-bece-180df73ddcc8)

       Fig 4. Histograma y función de probabilidad de la señal EMG
       

       ![Imagen de WhatsApp 2025-02-05 a las 22 29 50_20d71359](https://github.com/user-attachments/assets/18818aba-4a24-4867-a9ee-b52e7d030aab)

        Fig 5. Histograma de la señal EMG (Fragmento)-con función
       

     * Señales contaminadas con diferentes tipos de ruido:

       ![Imagen de WhatsApp 2025-02-05 a las 22 30 06_a10d38ed](https://github.com/user-attachments/assets/af33a108-7edf-48f6-b6e0-fdd884a2b2ed)

        Fig 6. Señal contaminada con Ruido Gaussiano Bajo
       

       ![Imagen de WhatsApp 2025-02-05 a las 22 30 25_1a9b9d5e](https://github.com/user-attachments/assets/2403272a-299e-4681-bd31-83242b9d1d2b)

        Fig 7. Señal contaminada con Ruido Gaussiano Alto
       

       ![Imagen de WhatsApp 2025-02-05 a las 22 30 43_8a377666](https://github.com/user-attachments/assets/26db8143-79ef-4710-8691-ce9e5a912458)

        Fig 8. Señal contaminada con Ruido Gaussiano Impulsivo Bajo
       

       ![Imagen de WhatsApp 2025-02-05 a las 22 31 19_0b0eda35](https://github.com/user-attachments/assets/f1eb8aaa-2b5f-4cfc-a2a6-056cda33306a)

        Fig 9. Señal contaminada con Ruido Gaussiano Impulsivo Alto
       

       ![Imagen de WhatsApp 2025-02-05 a las 22 31 42_b71a9aa6](https://github.com/user-attachments/assets/ce0169f6-ef34-40fa-acdc-37fc9b4f985d)

        Fig 10. Señal Contaminada con Ruido Artefacto Bajo
       

       ![Imagen de WhatsApp 2025-02-05 a las 22 32 00_8bb78765](https://github.com/user-attachments/assets/f9606ac8-262a-4820-bbd4-a0a2f9880cf3)

        Fig 11. Señal Contaminada con Ruido Artefacto Alto
       
     
     * Relación señal-ruido (SNR) en la consola de valores:

       ![Imagen de WhatsApp 2025-02-05 a las 23 48 36_7549cdec](https://github.com/user-attachments/assets/4dde5683-4b43-45ae-b17f-7efdaded04ca)

       Fig 12. Valores del ruido en la consola





















         
        
     
