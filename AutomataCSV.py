import pandas as pd
# Autor: Jorge Alejandro Zamudio Cahuil
# Fecha: 2024-11-12
# Versión: 1.0
# Grupo: I7B

# Ruta al archivo CSV
# Modificar la ruta dependiendo de la ubicación del archivo CSV
file_path = r'C:/Users/alexc/Downloads/Rutas.csv'

# Función para cargar el archivo CSV y procesar el DFA
def cargar_dfa():
    try:
        df = pd.read_csv(file_path).drop(columns=['Unnamed: 4'], errors='ignore')
        print("Archivo CSV cargado correctamente. Aquí están las primeras filas:")
        print(df.head())
        
        # Construir el DFA
        dfa = {}
        initial_state = None
        final_states = set()

        for index, row in df.iterrows():
            state = row['Entidades']
            if row['Unnamed: 0'] == 'Inicio':
                initial_state = state
            if row['Unnamed: 0'] == 'Final':
                final_states.add(state)
            dfa[state] = {0: row.iloc[2], 1: row.iloc[3]}

        return df, dfa, initial_state, final_states

    except FileNotFoundError:
        print(f"Archivo no encontrado en la ruta: {file_path}")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

    return None, None, None, None

# Función para verificar una cadena en el DFA
def verificar_cadena(dfa, initial_state, final_states, cadena):
    current_state = initial_state
    for simbolo in cadena:
        simbolo = int(simbolo)
        if simbolo not in dfa[current_state]:
            return False
        current_state = dfa[current_state][simbolo]
    return current_state in final_states

# Función para modificar las rutas del DFA y actualizar el archivo CSV
def modificar_rutas(df):
    print("\n--- Modificar rutas del DFA ---")
    print("Estados disponibles:", df['Entidades'].tolist())
    
    estado = input("Introduce el estado que deseas modificar: ")
    if estado not in df['Entidades'].values:
        print("Estado no encontrado.")
        return

    # Obtener el índice del estado seleccionado
    index = df[df['Entidades'] == estado].index[0]

    # Solicitar nuevas transiciones para 0 y 1
    nuevaRuta0 = input(f"Introduce la nueva transición para el símbolo '0' desde el estado '{estado}': ")
    nuevaRuta1 = input(f"Introduce la nueva transición para el símbolo '1' desde el estado '{estado}': ")

    # Actualizar el DataFrame
    df.at[index, '0'] = nuevaRuta0
    df.at[index, '1'] = nuevaRuta1

    # Guardar los cambios en el archivo CSV
    df.to_csv(file_path, index=False)
    print(f"Rutas actualizadas para el estado '{estado}' y guardadas en el archivo CSV.")

# Menú principal
def main():
    df, dfa, initial_state, final_states = cargar_dfa()
    
    while True:
        print("\n    Menú Principal    ")
        print("1. Verificar una cadena")
        print("2. Modificar las rutas del DFA")
        print("3. Salir")
        
        opcion = input("Selecciona una opción (1, 2, 3): ")

        if opcion == '1':
            if dfa and initial_state and final_states:
                cadena = input("Introduce la cadena a verificar: ")
                es_valida = verificar_cadena(dfa, initial_state, final_states, cadena)
                print(f"La cadena '{cadena}' es {'válida' if es_valida else 'inválida'}.")
            else:
                print("DFA no cargado correctamente")

        elif opcion == '2':
            if df is not None:
                modificar_rutas(df)
                # Recargar el DFA después de la modificación
                df, dfa, initial_state, final_states = cargar_dfa()
            else:
                print("No se pudo cargar el archivo CSV para modificar las rutas.")

        elif opcion == '3':
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida")

# Ejecutar el menú principal
if __name__ == "__main__":
    main()
