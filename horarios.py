import json
from typing import Callable, Dict, List


def _hora_a_minutos(hora: str) -> int:
    """Convierte una hora con formato HH:MM en minutos desde medianoche."""
    horas, minutos = hora.split(":")
    return int(horas) * 60 + int(minutos)


def _cargar_materias() -> List[Dict]:
    """Lee y devuelve la lista de materias desde el archivo JSON."""
    with open("Horario_PrimerAño.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        materias = data["materias"]
    return materias


def _filtrar_horarios_por_turno(materias: List[Dict], criterio_turno: Callable[[int], bool]) -> Dict[str, Dict]:
    """
    Devuelve un diccionario con las materias que tienen horarios que cumplen el criterio de turno.

    La clave es el código de la materia y el valor contiene nombre y lista de horarios filtrados.
    """
    materias_filtradas: Dict[str, Dict] = {}
    for materia in materias:
        horarios_turno = []
        for horario in materia.get("horarios", []):
            inicio_minutos = _hora_a_minutos(horario["inicio"])
            if criterio_turno(inicio_minutos):
                horarios_turno.append(horario)

        if horarios_turno:
            materias_filtradas[materia["codigo"]] = {
                "nombre": materia["nombre"],
                "horarios": horarios_turno,
            }
    return materias_filtradas


def _imprimir_horarios(materias_filtradas: Dict[str, Dict], encabezado: str) -> None:
    print(encabezado)
    for codigo, info in materias_filtradas.items():
        print(f"[{codigo}] {info['nombre']}")
        for horario in info["horarios"]:
            modalidad = "Virtual" if horario.get("virtual", False) else "Presencial"
            dia_formateado = f"{horario['dia']:<10}"  # padding para alinear días
            inicio = horario["inicio"]
            fin = horario["fin"]
            codigo_original = horario.get("codigo_original", "")
            tipo_clase = horario.get("tipo_clase", "")
            print(
                f"  - {dia_formateado} {inicio}–{fin} | {modalidad:<11} | {codigo_original} | {tipo_clase}"
            )


def mostrar_horarios_manana() -> None:
    materias = _cargar_materias()
    materias_filtradas = _filtrar_horarios_por_turno(
        materias, lambda inicio: inicio < _hora_a_minutos("13:00")
    )
    _imprimir_horarios(materias_filtradas, "[HORARIOS - MATERIAS A LA MAÑANA]")


def mostrar_horarios_tarde() -> None:
    materias = _cargar_materias()
    materias_filtradas = _filtrar_horarios_por_turno(
        materias,
        lambda inicio: _hora_a_minutos("13:00") <= inicio < _hora_a_minutos("18:00"),
    )
    _imprimir_horarios(materias_filtradas, "[HORARIOS - MATERIAS A LA TARDE]")


def mostrar_horarios_noche() -> None:
    materias = _cargar_materias()
    materias_filtradas = _filtrar_horarios_por_turno(
        materias, lambda inicio: inicio >= _hora_a_minutos("18:00")
    )
    _imprimir_horarios(materias_filtradas, "[HORARIOS - MATERIAS A LA NOCHE]")


if __name__ == "__main__":
    mostrar_horarios_manana()
    print()
    mostrar_horarios_tarde()
    print()
    mostrar_horarios_noche()
