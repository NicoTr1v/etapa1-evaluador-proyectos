# Librerias
import sys
import osmnx as ox
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Funciones tratamiento de inputs

def cargar_datos(geojson_path, excel_path, crs='EPSG:4326'):
    '''Carga y procesa los archivos de la zonificación y normativa'''
    try:
        # Cargar los datos geoespaciales y de normativa
        area = gpd.read_file(geojson_path).merge(pd.read_excel(excel_path), on='cod').to_crs(crs)
    except FileNotFoundError as e:
        print(f"Error al cargar archivos: {e}")
        # Si no se encuentran los archivos, se termina el programa
        sys.exit(1)
    return area

def obtener_geometria():
    '''Obtiene un GeoDataFrame geometría Point según la elección del usuario (dirección o coordenadas)'''
    while True:
        # Pregunta al usuario si tiene una dirección o coordenadas
        try:
            ubicacion = int(input('¿Tienes una dirección o coordenadas? (1: dirección / 2: coordenadas): '))
            if ubicacion not in [1, 2]:
                raise ValueError
            break
        # Solicita que se ingrese un valor válido
        except ValueError:
            print("Entrada no válida. Por favor ingrese 1 para dirección o 2 para coordenadas.")
    
    # Pide la dirección y obtiene la geometría
    if ubicacion == 1:
        direccion = input('Ingrese la dirección: ')
        location = ox.geocode(direccion)
        lon, lat = location[1], location[0]

    # Pide las coordenadas y obtiene la geometría
    else:
        while True:
            try:
                lon = float(input('Ingrese la longitud: '))
                lat = float(input('Ingrese la latitud: '))
                break
            except ValueError:
                print("Entrada no válida. Por favor ingrese valores numéricos para longitud y latitud.")
    
    return gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs='EPSG:4326')

# Funciones de procesamiento 
def procesar_zona(area, point):
    '''Realiza la intersección del punto con la zona y muestra la normativa correspondiente'''
    # zona_prc es el GeoDataFrame de la zona en la que se encuentra el punto
    zona_prc = area[area.intersects(point.geometry.iloc[0])]

    # Si no se encuentra la zona, se termina el programa
    if zona_prc.empty:
        print("El terreno no se ubica en la comuna.")
        sys.exit(1)
    
    # Si se encuentra la zona, se muestra la información base de la zona
    else:
        zona_info = zona_prc.iloc[0]
        print(f'El terreno se emplaza en:') 
        print(f'- Uso Suelo: {zona_info["uso_zona"]}')
        print(f'- Zona Edificación: {zona_info["zona"]}')
        print(f'- Nombre: {zona_info["nombre"]} ')

        # Si la zona no permite edificación se termina el programa
        if zona_info['normativa_edificacion'] in ['Unica', 'Areas Verdes']:
            print("La zona no permite edificación.")
            sys.exit(1)
        return zona_prc

def elige_normativa(zona_prc):
    '''Permite al usuario elegir una normativa entre las opciones residenciales'''
    # Se filtran las opciones de normativa residencial (este proceso se puede modificar para incluir otras normativas)
    norms_residenciales = ['Residencial', 'Densificación Residencial']
    opciones = zona_prc[zona_prc['normativa_edificacion'].isin(norms_residenciales)].copy()
    
    # Se crea una columna con el número de opción por si existen más de una residencial o densificación
    opciones['opcion'] = range(1, len(opciones) + 1)
    
    # Se genera un DataFrame con las opciones pero con las columnas renombradas para que el usuario pueda entenderlas
    opciones_out = opciones.rename(columns={
        'opcion': 'Opción',
        'normativa_edificacion': 'Normativa',
        'subdivision_predial_minima': 'Subdivisión Predial Min',
        'densidad_bruta_maxima': 'Densidad Bruta Max (hab/ha)',
        'constructibilidad': 'Coef. Constructibilidad',
        'ocupacion_1er_piso': 'Coef. Ocupación 1er Piso',
        'altura_maxima_pisos': 'Altura Max (pisos)'})
    
    #Los valores 9999 indican que la normativa en esa temática es Libre, reemplaza los 9999 por 'Libre'
    opciones_out.replace(9999, 'Libre', inplace=True)
    
    # Se muestra un DataFrame con las opciones de normativa residencial
    print("Las posibles combinaciones de normativa residencial a aplicar en la zona en la que se emplaza el terreno son las siguientes:")
    print(opciones_out[['Opción', 'Normativa', 'Subdivisión Predial Min', 'Densidad Bruta Max (hab/ha)', 
                            'Coef. Constructibilidad', 'Coef. Ocupación 1er Piso', 'Altura Max (pisos)']].to_string(index=False))
    
    # Se muestra una observación adicional sobre la zona en la que se encuentra el terreno
    print('Además considere lo siguiente:')
    print(opciones_out['observacion'].iloc[0])

    # Se pide al usuario que elija una de las opciones para aplicar la normativa al terreno que tiene
    while True:
        try:
            eleccion = int(input("Ingrese el número de la normativa que desea aplicar al terreno: "))
            if eleccion in opciones['opcion'].values:
                return opciones[opciones['opcion'] == eleccion]
            else:
                print("Número inválido. Intente poner un número válido.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número válido.")

def ingresar_superficie():
    '''Pide al usuario que ingrese la superficie del terreno'''
    # Se pide al usuario que ingrese la superficie del terreno
    while True:
        try:
            superficie = float(input('Ingrese la superficie del terreno (m2): '))
            break
        except ValueError:
            print("Entrada no válida. Por favor ingrese un valor numérico para la superficie.")
    return superficie

def calcular_restricciones(superficie, normativa_elegida):
    '''Calcula las restricciones de la normativa según la superficie del terreno'''
    # Se calculan las restricciones según la normativa y la superficie del terreno
    # Se calcula la cantidad máxima de viviendas permitidas
    if normativa_elegida['densidad_bruta_maxima'].iloc[0] == 9999:
        max_vi = 'Libre'
    else:
        max_vi = ((normativa_elegida['densidad_bruta_maxima'].iloc[0] * (superficie/10000)) // 4)

    # Calcula la superficie máxima permitida a construir
    max_surf = round(superficie * normativa_elegida['constructibilidad'].iloc[0], 3)

    # Calcula la superficie mácima permitia a construir en el 1er piso
    max_oc = round(superficie * normativa_elegida['ocupacion_1er_piso'].iloc[0], 3)

    # Se muestran las restricciones calculadas
    print(f'La superficie máxima construible es de {max_surf} m2.')
    print(f'La ocupación máxima del suelo en el 1er piso es de {max_oc} m2.')
    print(f'La cantidad máxima de viviendas permitidas son {max_vi}.')

def main():
    # Cargar los datos geoespaciales y de normativa
    area = cargar_datos('capas/zonas_geom.geojson', 'capas/normativa_residencial.xlsx')
    # Obtener la ubicación del usuario (por dirección o coordenadas)
    point = obtener_geometria()
    # Procesar la zona en función del punto
    zona_prc = procesar_zona(area, point)
    # Elegir la normativa que se va a aplicar
    normativa_elegida = elige_normativa(zona_prc)
    # Ingresar la superficie del terreno
    superficie = ingresar_superficie()
    # Calcular y mostrar las restricciones según la normativa y superficie
    calcular_restricciones(superficie, normativa_elegida)

# Ejecutar el programa
if __name__ == "__main__":
    main()

# CASO TINSA: -33.40890, -70.55164
#avenida tomas moro 20, las condes, chile
#av: 70,5699767°W 33,4279546°S 