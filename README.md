## Parte 1: Restricciones para Edificación

# Descripción

Para que un proyecto de edificación sea aprobado, debe pasar por diversas etapas, una de las cuales es la revisión de las normativas aplicables en la zona donde se ubica el terreno. Aunque existen diferentes Instrumentos de Planificación Territorial (IPT), el instrumento que detalla los coeficientes que limitan las características físicas, como la superficie máxima de edificación, es la Ordenanza Local de cada comuna.

De esta manera revisión detallada de la ordenanza local y las normativas aplicables permite identificar de manera temprana posibles obstáculos y ajustar el proyecto a las regulaciones establecidas, garantizando así su viabilidad y cumplimiento legal.

Para agilizar esta etapa de un proyecto inmobiliario, se ha desarrollado este prototipo aplicado en la comuna de Las Condes, que está diseñado para que, mediante la interacción con el script, el usuario pueda obtener rápidamente las restricciones de superficie.

El script permite al usuario ingresar una dirección o coordenadas para ubicar un punto dentro de la comuna. Luego, consulta la normativa correspondiente para esa zona, mostrando detalles como la densidad máxima permitida, coeficientes de constructibilidad y ocupación, altura máxima, entre otros. Además, calcula restricciones basadas en la superficie del terreno ingresada, como la superficie máxima construible y la ocupación máxima del suelo, según las normas establecidas en la tabla de normativa seleccionada por el usuario.

---

# Requisitos

- Python 3.x
- pip
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

# Archivos requeridos

El script requiere de dos arcihvos e

## Archivo GeoJSON Zonificación Comuna

## Excel de Normativa de cada Zona

---

# Descripción General de las Funciones

A continuación, se indican las principales funciones utilizadas en el código junto a una breve descripción, entradas y salidas.

### 1. **`cargar_datos(geojson_path, excel_path, crs='EPSG:4326')`**

- **Descripción**: Carga un archivo geográfico de las zonas de edificación de la comuna (GeoJSON) y las normativas asociadas a cada una de ellas(Excel), fusionándolos en un `GeoDataFrame`. Convierte el sistema de referencia espacial a `EPSG:4326`.
- **Entrada**:
    - `geojson_path`: Ruta al archivo GeoJSON que contiene las zonas.
    - `excel_path`: Ruta al archivo Excel con las normativas.
    - `crs`: Sistema de referencia espacial (por defecto 'EPSG:4326').
- **Salida**:
    - `area`: Un `GeoDataFrame` que contiene la zonificación geográfica combinada con la normativa, transformado al CRS especificado.

---

### 2. **`obtener_geometria()`**

- **Descripción**: Solicita al usuario una dirección o coordenadas. Luego convierte esa entrada en un `GeoDataFrame` que representa la ubicación como un punto (`Point`).
- **Entrada**:
    - No recibe argumentos, pero solicita al usuario:
        - Si elige `1`, se solicita una dirección para convertirla a coordenadas.
        - Si elige `2`, se piden coordenadas de longitud (`lon`) y latitud (`lat`).
- **Salida**:
    - Un `GeoDataFrame` con una geometría de tipo `Point` que representa la ubicación proporcionada por el usuario.

---

### 3. **`procesar_zona(area, point)`**

- **Descripción**: Interseca el punto geográfico ingresado por el usuario con el área de zonificación. Muestra la información de uso de suelo y la normativa correspondiente si la zona permite edificación.
- **Entrada**:
    - `area`: Un `GeoDataFrame` con la zona de edificación y sus normativas.
    - `point`: Un `GeoDataFrame` con la geometría del punto de la ubicación ingresada por el usuario.
- **Salida**:
    - `zona_prc`: Un `GeoDataFrame` que contiene la zona donde se ubica el punto. Si la zona no permite edificación, el programa termina.

---

### 4. **`elige_normativa(zona_prc)`**

- **Descripción**: Filtra las normativas residenciales disponibles en la zona e imprime las opciones. Luego, permite al usuario seleccionar una normativa aplicable.
- **Entrada**:
    - `zona_prc`: Un `GeoDataFrame` que contiene las normativas de la zona donde se ubica el terreno.
- **Salida**:
    - Un `GeoDataFrame` con la normativa seleccionada por el usuario.

---

### 5. **`ingresar_superficie()`**

- **Descripción**: Solicita al usuario que ingrese la superficie del terreno en metros cuadrados.
- **Entrada**:
    - No recibe argumentos.
- **Salida**:
    - Un número que representa la superficie ingresada por el usuario en metros cuadrados.

---

### 6. **`calcular_restricciones(superficie, normativa_elegida)`**

- **Descripción**: Calcula las restricciones de construcción basadas en la normativa seleccionada y la superficie del terreno. Muestra la superficie máxima construible, la ocupación del suelo en el primer piso, y la cantidad máxima de viviendas permitidas.
- **Entrada**:
    - `superficie`: La superficie del terreno en metros cuadrados.
    - `normativa_elegida`: El `GeoDataFrame` con la normativa seleccionada por el usuario.
- **Salida**:
    - No tiene una salida directa, pero imprime:
        - Superficie máxima construible.
        - Ocupación máxima en el primer piso.
        - Número máximo de viviendas permitidas.

---

### 7. **`main()`**

- **Descripción**: Coordina el flujo del programa:
    - Carga los datos geoespaciales y normativos.
    - Solicita la ubicación del usuario y procesa la zona.
    - Permite seleccionar la normativa aplicable.
    - Pide la superficie del terreno.
    - Calcula las restricciones basadas en la normativa seleccionada.
- **Entrada**:
    - No recibe argumentos.
- **Salida**:
    - No tiene salida directa, coordina la ejecución de las funciones.

# Ejemplo Uso

Parámetros de Entrada:

```json
{
    "parametros_entrada": {

        "tipo_propiedad": "DEPARTAMENTO",
        "tasa_prom": 2.64,
        "vel_prom": 7.69,
        "uso_habitacional_mixto": "HABITACIONAL",
        "viviendas": 724,
        "dist_metro": 528.62,
        "cc": 32,
        "tasa_interes": 1.9,
        "comuna": "SANTIAGO",
        "area_terreno": 2406.48,
        "costo_terreno": 50,
        "limite_superficie_construida": 18000
    },

    "parametros_ag": {

        "NUM_CROMOSOMAS" : 10,  
        "NUM_GENERACIONES" : 60,  
        "NUM_TIPOLOGIAS" : 10  
    },

    "log_path" : "./log"
}
```

Retorno:

```python
Mejor cromosoma encontrado: 
[153, 0.11958100571401273, 0.09196688831173332, 0.16579238837191398, 0.013014441599349957, 0.09196688831173332, 0.03122844241325229, 0.2208641957095921, 0.16563061636333495, 0.07710081003826087, 0.02285432316681647] 
con un VPN de 839235.3544256077 y un Precio Predicho de 10812.253664998163

{'Mejor VPN': 839235.3544256077, 
'Mejor Precio Predicho': 10812.253664998163, 
'Mejor Cromosoma': 
[153, 0.11958100571401273, 0.09196688831173332, 0.16579238837191398, 0.013014441599349957, 0.09196688831173332, 0.03122844241325229, 0.2208641957095921, 0.16563061636333495, 0.07710081003826087, 0.02285432316681647], 
'Configuración': {
		'n_unidades': 153, 
		'Porcentajes de Tipologías': [0.11958100571401273, 0.09196688831173332, 0.16579238837191398, 0.013014441599349957, 0.09196688831173332, 0.03122844241325229, 0.2208641957095921, 0.16563061636333495, 0.07710081003826087, 0.02285432316681647]}, 
		'Superficie Construida': 17815.366117228492}
```
