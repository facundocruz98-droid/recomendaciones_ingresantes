import datetime
import motor # Importamos el archivo motor.py que acabamos de crear
from datetime import datetime
# Importamos los códigos del archivo que acabamos de crear
import constantes as c

# --- TUS FUNCIONES DE UTILIDAD (YA DEFINIDAS) ---

def obtener_saludo():
    h = datetime.now().hour
    if 6 <= h < 12:
        return "¡Buen día! ☀️"
    elif 12 <= h < 18:
        return "¡Buenas tardes! 🌤️"
    elif 18 <= h < 24:
        return "¡Buenas noches! 🌙"
    else:
        return "Wow, estás conectado a la madrugada 😴 — ¡sos un/a crack!"

def imprimir_info_inicial():
    print(obtener_saludo())
    print("Soy tu asistente de la Facultad de Ingeniería (UNJu).")
    print("Voy a hacerte unas preguntas rápidas para armar tu perfil y poder darte recomendaciones de estudio que realmente te sirvan. 🤝\n")

def preguntar_si_no(prompt):
    while True:
        r = input(prompt + " (sí / no): ").strip().lower()
        if r in ("si", "sí", "s"):
            return True
        if r in ("no", "n"):
            return False
        print("No te entendí — por favor respondé 'sí' o 'no'.")

def preguntar_turnos_trabajo():
    """Devuelve un set con los códigos de turno (AC, AD, AE)"""
    opciones_map = {"1": c.TRABAJA_MANANA, "2": c.TRABAJA_TARDE, "3": c.TRABAJA_NOCHE}
    texto = (
        "\nContame en qué turno trabajás. Podés elegir una o dos opciones:\n"
        "  1) Mañana\n"
        "  2) Tarde\n"
        "  3) Noche\n"
        "Escribí el número o los números separados por coma (ej.: 1 o 1,3). \nRespuesta: "
    )
    while True:
        r = input(texto).strip()
        if not r:
            print("Está bien si no estás seguro/a — por favor ingresá al menos una opción.")
            continue
        parts = [p.strip() for p in r.split(",") if p.strip()]
        
        # Validación
        if any(p not in ("1", "2", "3") for p in parts):
            print("Ups — solo podés elegir 1, 2 y/o 3. Probá de nuevo.")
            continue
        if len(parts) > 2:
            print("Tranquilo/a — solo permitimos hasta 2 turnos. Elegí una o dos opciones.")
            continue
            
        perfiles = set(opciones_map[p] for p in parts)
        return perfiles

def pedir_nombre():
    nombre = input("1) ¿Cuál es tu nombre completo? (podés poner apodo): ").strip()
    if not nombre:
        print("No hay problema si preferís no decirlo ahora. Te llamaré '(sin nombre)'.")
        return "Estudiante"
    return nombre

# --- NUEVA FUNCIÓN PARA COMPLETAR LA CAPTURA ---

def preguntar_cantidad_materias():
    """Pregunta si cursa todas o algunas y devuelve el código correspondiente."""
    print("\n¿Tenés pensado cursar todas las materias del año o solo algunas?")
    while True:
        r = input("Escribí 'todas' o 'algunas': ").strip().lower()
        if "todas" in r or "todo" in r:
            return c.CURSA_TODAS # AG
        if "algunas" in r or "pocas" in r or "par" in r:
            return c.CURSA_ALGUNAS # AF
        print("Por favor, escribí 'todas' o 'algunas'.")

def capturar_datos_estudiante():
    """
    Función principal que orquesta las preguntas con lógica condicional.
    Devuelve: (nombre, set_de_hechos)
    """
    hechos_usuario = set() # Aquí guardaremos códigos como 'AB', 'AC', etc.
    
    imprimir_info_inicial()
    
    # 1. Nombre
    nombre = pedir_nombre()
    
    # 2. Trabajo (Lógica condicional estricta)
    trabaja = preguntar_si_no("\n2) ¿Trabajás actualmente además de estudiar?")
    
    if not trabaja:
        # Si NO trabaja, asignamos AB y NO preguntamos turnos.
        hechos_usuario.add(c.SOLO_ESTUDIA)
    else:
        # Si SÍ trabaja, NO asignamos AB. Preguntamos turnos.
        turnos = preguntar_turnos_trabajo()
        hechos_usuario.update(turnos) # Agrega AC, AD o AE según corresponda
    
    # 3. Cursada (Todas vs Algunas)
    codigo_cursada = preguntar_cantidad_materias()
    hechos_usuario.add(codigo_cursada)
    
    # 4. Retoma estudios (AH)
    if preguntar_si_no("\n4) ¿Estás retomando los estudios después de haber dejado un tiempo?"):
        hechos_usuario.add(c.RETOMA_ESTUDIO)
        
    # 5. Dos carreras (AI)
    if preguntar_si_no("\n5) ¿Estás estudiando otra carrera simultáneamente?"):
        hechos_usuario.add(c.DOS_CARRERAS)
        
    return nombre, hechos_usuario

# --- BLOQUE PRINCIPAL PARA PROBAR ---

""" 
# if __name__ == "__main__":
    nombre_alumno, perfil_detectado = capturar_datos_estudiante()
    print("-" * 50)
    print(f"PERFIL GENERADO PARA: {nombre_alumno}")
    print(f"Códigos detectados (Hechos): {perfil_detectado}")
    print("-" * 50)
    print("Listo para enviar al motor de inferencia...") 
    
    """
    
if __name__ == "__main__":
    nombre_alumno, perfil_detectado = capturar_datos_estudiante()
    
    print("-" * 50)
    
    print(f"PERFIL GENERADO PARA: {nombre_alumno}")
    
    print(f"Códigos detectados (Hechos): {perfil_detectado}")
    
    # print(f"Códigos detectados: {perfil_detectado}") # Debug
    print("-" * 50)
    
    # EJECUTAMOS EL MOTOR CON LOS DATOS OBTENIDOS
   
    motor.ejecutar_motor(perfil_detectado)