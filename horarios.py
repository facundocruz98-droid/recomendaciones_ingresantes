# horarios.py
import json

def cargar_horarios():
    """Carga los horarios desde el archivo JSON."""
    try:
        with open('Horario_PrimerAño.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(" > [ERROR]: No se encontró el archivo 'Horario_PrimerAño.json'.")
        return None
    except json.JSONDecodeError:
        print(" > [ERROR]: El archivo 'Horario_PrimerAño.json' tiene un formato incorrecto.")
        return None

def obtener_horarios_por_franja(franja):
    """
    Obtiene y formatea los horarios para una franja específica (mañana, tarde, noche).
    """
    datos = cargar_horarios()
    if not datos or 'subjects' not in datos:
        return "No se pudo cargar la información de horarios."

    horarios_encontrados = []
    
    for materia in datos['subjects']:
        for sesion in materia['sessions']:
            hora_inicio = int(sesion['start'].split(':')[0])
            
            if franja == 'manana' and hora_inicio < 12:
                horarios_encontrados.append((materia, sesion))
            elif franja == 'tarde' and 12 <= hora_inicio < 19:
                horarios_encontrados.append((materia, sesion))
            elif franja == 'noche' and hora_inicio >= 19:
                horarios_encontrados.append((materia, sesion))

    if not horarios_encontrados:
        return f"No hay materias disponibles en el turno {franja}."

    # Usamos un diccionario para agrupar las sesiones por materia y no repetir el nombre
    materias_formateadas = {}
    for materia, sesion in horarios_encontrados:
        nombre_materia = materia['name']
        if nombre_materia not in materias_formateadas:
            materias_formateadas[nombre_materia] = []
        
        modalidad = "Virtual" if sesion.get('virtual', False) else "Presencial"
        detalle_sesion = (
            f"    - {sesion['day']} de {sesion['start']} a {sesion['end']} "
            f"({sesion['class_type']}, Modalidad: {modalidad})"
        )
        materias_formateadas[nombre_materia].append(detalle_sesion)

    # Creamos el texto final
    texto_final = f"Materias disponibles en el turno {franja.upper()}:\n"
    for nombre_materia, detalles in materias_formateadas.items():
        texto_final += f"  > {nombre_materia}:\n"
        for detalle in detalles:
            texto_final += f"{detalle}\n"
            
    return texto_final

if __name__ == '__main__':
    # Pruebas para verificar que las funciones operan correctamente
    print("--- PRUEBA TURNO MAÑANA ---")
    print(obtener_horarios_por_franja('manana'))
    print("\n--- PRUEBA TURNO TARDE ---")
    print(obtener_horarios_por_franja('tarde'))
    print("\n--- PRUEBA TURNO NOCHE ---")
    print(obtener_horarios_por_franja('noche'))
