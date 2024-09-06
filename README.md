# Etapa 1 Evaluador Proyectos

# Descripción

Para que un proyecto de edificación sea aprobado, debe pasar por diversas etapas, una de las cuales es la revisión de las normativas aplicables en la zona donde se ubica el terreno. Aunque existen diferentes Instrumentos de Planificación Territorial (IPT), el instrumento que detalla los coeficientes que limitan las características físicas, como la superficie máxima de edificación, es la Ordenanza Local de cada comuna.

De esta manera revisión detallada de la ordenanza local y las normativas aplicables permite identificar de manera temprana posibles obstáculos y ajustar el proyecto a las regulaciones establecidas, garantizando así su viabilidad y cumplimiento legal.

Para agilizar esta etapa de un proyecto inmobiliario, se ha desarrollado este prototipo aplicado en la comuna de Las Condes, que está diseñado para que, mediante la interacción con el script, el usuario pueda obtener rápidamente las restricciones de superficie.

El script permite al usuario ingresar una dirección o coordenadas para ubicar un punto dentro de la comuna. Luego, consulta la normativa correspondiente para esa zona, mostrando detalles como la densidad máxima permitida, coeficientes de constructibilidad y ocupación, altura máxima, entre otros. Además, calcula restricciones basadas en la superficie del terreno ingresada, como la superficie máxima construible y la ocupación máxima del suelo, según las normas establecidas en la tabla de normativa seleccionada por el usuario.

---

# Antecedentes

El principal obstáculo que enfrenta la automatización de este proceso es la disponibilidad y formatos de los Instrumentos de Planificación Territorial requeridos. Cada comuna tiene distintas Ordenanzas Locales donde especifican los coeficientes en distintas formas, ya sea tablas, párrafos de texto, etc. Por otro lado, la capa espacial que permite hacer el proceso terreno-normativa suele estar contenida en algún visor de la misma comuna o en el [servicio de mapas del Ministerio de Vivienda y Urbanismo.](https://geoide.minvu.cl/server/rest/services/IPT/PRC_Metropolitana/FeatureServer)

A continuación se muestra el formato en que vienen los archivos en bruto antes de ser tratados y como se espera que esté disponible para la ejecución correcta del script.

## Normativa de cada zona

Como se menciona, la normativa específica de cada zona está explicada en distinto formatos, en este caso se muestra como viene en la [Ordenanza Plan Regulador Comunal de Las Condes](https://archivos.lascondes.cl/descargas/plano-regulador/2021_11_10_Texto_Refundido_Ordenanza_PRC_Exposicion_vf_exp.pdf). En la Imagen 1 se muestra un ejemplo para una zona específica dentro de la comuna, se muestran 2 posibles combinaciones de normativas, dadas por la *Tabla A) Base* y la *Tabla B) Proyectos de Densificación de Viviendas en Edificaciones Colectivas* 

![image](https://github.com/user-attachments/assets/a59402eb-4bed-49ee-97ab-22ad904134cc)

*Imagen 1: Tablas con distintas combinaciones de normativas aplicables a una zona.*

### Forma esperada para el funcionamiento del script

Para que el script sea funcional es necesario que la información de cada normativa sea tabulada en un Excel.

![image](https://github.com/user-attachments/assets/601a32bf-7f6d-480c-b365-dd4d1d043562)

*Imagen 2: Formato esperado para las distintas combinaciones de normativa (filtrado para zona E-Ab1).*

La Imagen 2 muestra el formato esperado para las combinaciones de normativas disponibles en una zona. Esta tabla se compone de varias columnas con información, sin embargo, las relevantes para este script son:

- cod: (*str*) código que se compone de siglas uso de suelo/siglas zona edificación, este código no es único, ya que es un código que permite unir después a cada zona en la capa geográfica con todas las combinaciones de normativas disponibles y cada zona como bien muestra la Imagen 1, se tienen distintas combinaciones de normativa para cada cod.
- uso_zona: (*str*) siglas asociadas al uso de suelo de la zona.
- zona: (*str*) siglas de la zona.
- nombre: (*str*) nombre y significado de las siglas de la zona.
- obervacion:  (*str*)observación importante sobre la normativa de la zona.
- normativa_edificacion: (*str*) tipo de normativa aplicable, puede ser: Residencial, Equipamiento, Densificación Residencial, Densificación no Residencial, Áreas verdes y Única. Para estas últimas está prohibido la edificación (el script lo explicita). También el script funciona solo para aplicación de tipo de normativa Residencial y Densificación Residencial.
- densidad_bruta_maxima: (float) Densidad Bruta Máxima en la zona, en habitantes/hectáreas, se considera 4 habitantes por vivienda (O.G.U.C).
- constructibilidad:  (*float*) Coeficiente de Constructibilidad, valor que multiplicado la superficie del terreno entrega la superficie máxima a construir sobre el terreno.
- ocupacion_1er_piso:  (*float*) Coeficiente de Ocupación en el 1er Piso, valor que multiplicado la superficie del terreno entrega la superficie máxima a construir en el primer piso.
- altura_maxima_pisos: (*int*) altura máxima permitida en pisos, la O.G.U.C permite considerar hasta 3,5 metros por piso, sin embargo, en el mercado se suele usar 2,5 metros.
- altura_maxima_mts: (*float*) altura máxima permitida en metros, aplicado con 3,5 metros por piso. En algunos casos se específica solo en pisos por lo que se hace el calculo con los valores ya mencionados, en otros específica ambos valores.

### A considerar: 

La tabla Excel que se utiliza trae más columnas, que dependiendo la escalabilidad, serán de importancia, estasson:

- uso_prohibido:  (*str*)nuso prohibido en la zona.
- uso_permitido: (*str*) uso permitido en la zona.
- subdivision_predial_minima: (float) Subdivisión predial mínima admitida en la zona.
- subdivision_predial_maxima: (*float*) Subdivisión predial máxima admitida en la zona.
- ocupacion_2do_piso: (*float*) Coeficiente de Ocupación en el 2do Piso, valor que multiplicado la superficie del terreno entrega la superficie máxima a construir en el segundo piso.
- ocupacion_3er_piso: (*float*) Coeficiente de Ocupación en el 3er Piso, valor que multiplicado la superficie del terreno entrega la superficie máxima a construir en el tercer piso.
- ocupacion_pisos_superiores: (*float*) Coeficiente de Ocupación en los pisos superiores.
- rasante: (*str*) Rasante de la edificación en grados.
- agrupamiento: (*str*) Sistema de Agrupamiento de las edificaciones permitido.
- antejardin: (*float*) espacio entre línea oficial de la vía y la edificación a dejar como Antejardín en metros.

- **Los coeficientes de ocupación varían en cada comuna, en algunos se específica hasta el del 3er piso, otros solo 1er piso y superiores. Para el caso de Las Condes, solo se específica el coeficiente para el primer piso, lo que indica que la ocupación es pisos superiores está dada por lo restante entre lo que determina el coeficiente de constructibilidad.**
- **Donde no hay valores se reemplazó con un “-”, además, si hay columnas que no tienen valores, significa que la comuna de Las Condes no los informa, sin embargo otras si, por lo que si se quiere hacer escalable a la Región Metropolitana se mantienen.**

## Capa geográfica de la zonificación de la comuna

El otro archivo requerido es la capa geográfica que permite hacer la intersección entre la ubicación del terreno de interés y la zona en la que se emplaza. En el link asociado al MINVU (mencionado al principio de antecedentes) se ve como es el formato en el que viene este archivo, sin embargo, se espera que la capa geográfica para este script sea un GeoJSON con los campos de código (*cod*), comuna y el campo de geometría requerido para posteriormente.

![image](https://github.com/user-attachments/assets/a1f67c1d-416d-45fe-8241-8e85e32ef171)

*Imagen 3: Formato esperado para capa geográfica (GeoJSON).*

La Imagen 3 muestra como es la capa, cada zona tiene el código (*cod*), el cual no está hecho para una visualización atractiva, solo para entender como se compone la capa, en este caso la geometría es `MultiPolygon`, ya que se tienen distintos polígonos que representan una misma zona en distintas partes de la comuna.

# Requisitos

- Python 3.x
- pip
	- Librerías: (también están en requirements.txt)
		- geopandas==0.14.4
		- osmnx==1.9.4
		- pandas==2.2.2
		- numpy==1.26.4
		- shapely==2.0.6
		- openpyxl==3.1.5
- git

# Configuración del Entorno

Para configurar el entorno de ejecución y ejecutar el algoritmo se deben seguir los siguientes pasos:

## 1. Clonar el repositorio

En primer lugar se debe clonar el repositorio dentro de la máquina local utilizando Git:

```bash
git clone https://github.com/NicoTr1v/etapa1-evaluador-proyectos.git
cd etapa1-evaluador-proyectos
```

## 2. **Crear y Activar un Entorno Virtual**

Para evitar conflictos de dependencias, se crea un entorno virtual dentro del directorio del proyecto

```bash
python -m venv venv
```

Luego, se debe activar el entorno virtual generado:

- En Windows:

```bash
.\venv\Scripts\activate
```

- En macOS/Linux:

```bash
source venv/bin/activate
```

## 3. Instalación de dependencias

Ya con el entorno virtual activado, se deben instalar las dependencias necesarias para que el código se ejecute sin problemas:

```bash
pip install -r requirements.txt
```

# Ejecución del script

Una vez configurado el entorno de ejecución, dentro del directorio raíz se ejecuta el siguiente comando:

```bash
python etapa_1_recomendador.py 
```

# Salida del script

La salida final del script es una visualización de las restricciones a para las características del terreno.

---

# Diagrama de Abstracción de Procesos

A continuación se detalla el flujo del script en un diagrama de abstracción:

![image](https://github.com/user-attachments/assets/a9995b65-f6a1-45ac-b0ac-499a427be05c)


*Imagen 4: Diagrama de abstracción para el script.*

---

# Descripción General de las Funciones

A continuación, se indican las principales funciones utilizadas en el código junto a una breve descripción, entradas y salidas.

### 1. **`cargar_datos(geojson_path, excel_path, crs='EPSG:4326')`**

- **Descripción**: Carga los datos geoespaciales (GeoJSON) y las normativas (Excel), fusionándolos en un `GeoDataFrame`. Transforma los datos al sistema de referencia espacial `EPSG:4326`.
- **Entrada**:
    - `geojson_path`: Ruta al archivo GeoJSON con los datos de zonificación.
    - `excel_path`: Ruta al archivo Excel con las normativas.
    - `crs`: Sistema de referencia espacial (por defecto 'EPSG:4326').
- **Salida**:
    - `zonificacion`: Un `GeoDataFrame` que combina la zonificación geográfica y las normativas, transformado al CRS especificado.

---

### 2. **`obtener_geometria()`**

- **Descripción**: Solicita al usuario una dirección o coordenadas, y convierte esa entrada en un `GeoDataFrame` con un punto (`Point`) geoespacial que representa la ubicación.
- **Entrada**:
    - No recibe argumentos, pero solicita al usuario:
        - Dirección (si selecciona `1`).
        - Coordenadas de longitud (`lon`) y latitud (`lat`) (si selecciona `2`).
- **Salida**:
    - `point`: Un `GeoDataFrame` con una geometría `Point` que representa la ubicación ingresada por el usuario.

---

### 3. **`procesar_zona(zonificacion, point)`**

- **Descripción**: Realiza la intersección del punto ingresado con la zonificación. Si el punto está en una zona permitida, muestra información sobre el uso del suelo, la normativa de edificación y el nombre de la zona.
- **Entrada**:
    - `zonificacion`: Un `GeoDataFrame` que contiene la zonificación geográfica y normativas.
    - `point`: Un `GeoDataFrame` que contiene la geometría del punto de la ubicación ingresada.
- **Salida**:
    - `zona_prc`: Un `GeoDataFrame` que contiene la zona donde se encuentra el punto. Si la zona no permite edificación, el programa se cierra.

---

### 4. **`elige_normativa(zona_prc)`**

- **Descripción**: Filtra las normativas residenciales disponibles en la zona, imprime las opciones y permite al usuario seleccionar una normativa aplicable.
- **Entrada**:
    - `zona_prc`: Un `GeoDataFrame` que contiene las normativas disponibles para la zona en la que se ubica el terreno.
- **Salida**:
    - Un `GeoDataFrame` que contiene la normativa seleccionada por el usuario.

---

### 5. **`calcular_restricciones(normativa_elegida)`**

- **Descripción**: Calcula las restricciones de construcción basadas en la normativa seleccionada por el usuario y la superficie del terreno ingresada. Muestra:
    - Superficie máxima construible.
    - Ocupación máxima del suelo en el primer piso.
    - Cantidad máxima de viviendas permitidas.
    - Altura máxima permitida (en pisos).
- **Entrada**:
    - `normativa_elegida`: El `GeoDataFrame` con la normativa seleccionada por el usuario.
- **Salida**:
    - No tiene una salida directa, pero imprime los cálculos de restricciones.

---

### 6. **`main()`**

- **Descripción**: Es la función principal que coordina todo el flujo del programa:
    - Carga los datos geoespaciales y normativos.
    - Solicita la ubicación del usuario (dirección o coordenadas).
    - Procesa la zonificación para obtener la normativa aplicable.
    - Permite al usuario elegir una normativa residencial.
    - Calcula y muestra las restricciones de edificación basadas en la normativa y la superficie del terreno.
- **Entrada**:
    - No recibe argumentos.
- **Salida**:
    - No tiene una salida directa, pero coordina la ejecución de las funciones.

---

# A considerar:

- Si el input será una dirección considere la forma: *vía numeración, comuna, país*
    - Ej: avenida tomas moro 20, las condes, chile

- Si ingresa una dirección que si es de la comuna y el programa le dice que no, considere utilizar la opción por coordenadas.
    - Al escoger coordenadas, el programa solicitará primero longitud y luego latitud, considere sistema de referencia geodésico para las coordenadas (mismas que entrega Google Maps), para Chile ambos negativos y con un punto para los decimales.
        - Ej:
	- longitud: -70.55164
        - latitud: -33.40890
        

# Ejemplo Uso

Interacción (ingresa dirección):

```
¿Tienes una dirección o coordenadas? (1: dirección / 2: coordenadas): 1
Ingrese la dirección: avenida tomas moro 20, las condes, chile
```

Interacción (ingresa coordenadas):

```
¿Tienes una dirección o coordenadas? (1: dirección / 2: coordenadas): 2
Ingrese la longitud: -70.55164
Ingrese la latitud: -33.40890
```

Retorno:

```
El terreno se emplaza en:
- Uso Suelo: UC1
- Zona Edificación: EAm1p
- Nombre: UC1/EAm1p Zona de Uso de Comercio N°1 e Instituciones Comunal/ Edificación Aislada Media N°1 Prima
Las posibles combinaciones de normativa residencial a aplicar en la zona en la que se emplaza el terreno son las siguientes:
 Opción             Normativa      Subdivisión Predial Min      Densidad Bruta Max (hab/ha)    Coef. Constructibilidad       Coef. Ocupación 1er Piso    Altura Max (pisos)
      1               Residencial           2500                        20                                0.6                         0.4                      3
      2   Densificación Residencial         1500                       Libre                              2.5                         0.3                      7
Además considere lo siguiente:
En todos los casos, la edificación podrá acogerse sólo a una de las tablas precedentes y, en el deslinde de contrafrente, deberá cumplir un distanciamiento mínimo 
de 18 metros con los predios que pertenezcan parcialmente al área de edificación E-Ab1 y de 12 metros con predios que pertenezcan parcialmente al área de edificación 
E-Ab2, E-Ab3, distancia que será medida desde el eje del deslinde y en toda su longitud. Para efectos de calificar si el predio pertenece a las áreas de edificación 
E-Ab1, E-Ab2 o E-Ab3, se considerará cualquier predio que contenga total o parcialmente alguna de estas áreas.
```

Interacción:

```
Ingrese el número de la opción de normativa que desea aplicar al terreno: 2
Ingrese la superficie del terreno (m2): 1450
```

Retorno

```
La superficie máxima construible es de 3625.0 m2.
La ocupación máxima del suelo en el 1er piso es de 435.0 m2.
La cantidad máxima de viviendas permitidas son Libre.   
```
