from experta import *
import constantes as c
import mensajes as m

class RecomendadorEstudios(KnowledgeEngine):
    
    # --- REGLA GENERAL DE IMPRESIÓN ---
    # Esta regla se activa para cualquier hecho (A, B, CC, etc.) que sea declarado
    # y busca si tiene un mensaje asociado en el diccionario.
    @Rule(AS.hecho << Fact())
    def mostrar_recomendacion(self, hecho):
        # Extraemos el código del hecho (ej: "A", "B", "FF")
        codigo_hecho = hecho.get(0)
        # Buscamos si ese código tiene un mensaje asociado.
        if codigo_hecho and codigo_hecho in m.RECOMENDACIONES:
            print(f" > [CONSEJO]: {m.RECOMENDACIONES[codigo_hecho]}")

    # --- TUS REGLAS LÓGICAS ---

    # Si AB, AG entonces A
    @Rule(Fact(c.SOLO_ESTUDIA), Fact(c.CURSA_TODAS))
    def regla_1(self):
        self.declare(Fact("A"))

    # Si AB entonces FF
    @Rule(Fact(c.SOLO_ESTUDIA))
    def regla_2(self):
        self.declare(Fact("FF"))

    # Si FF entonces E, V
    @Rule(Fact("FF"))
    def regla_3(self):
        self.declare(Fact("E"))
        self.declare(Fact("V"))

    # Si AG entonces B, C, D, AA
    @Rule(Fact(c.CURSA_TODAS))
    def regla_4(self):
        self.declare(Fact("B"))
        self.declare(Fact("C"))
        self.declare(Fact("D"))
        self.declare(Fact("AA"))

    # Si AH entonces I, K
    @Rule(Fact(c.RETOMA_ESTUDIO))
    def regla_5(self):
        self.declare(Fact("I"))
        self.declare(Fact("K"))

    # Si K entonces X
    @Rule(Fact("K"))
    def regla_6(self):
        self.declare(Fact("X"))

    # Si AF entonces F, T, U, LL
    @Rule(Fact(c.CURSA_ALGUNAS))
    def regla_7(self):
        self.declare(Fact("F"))
        self.declare(Fact("T"))
        self.declare(Fact("U"))
        self.declare(Fact("LL"))

    # Si AD entonces L, M (Trabaja Tarde -> Horarios Mañana y Virtual)
    @Rule(Fact(c.TRABAJA_TARDE))
    def regla_8(self):
        self.declare(Fact("L"))
        self.declare(Fact("M"))

    # Si AC entonces M, N (Trabaja Mañana -> Virtual y Horarios Tarde)
    @Rule(Fact(c.TRABAJA_MANANA))
    def regla_9(self):
        self.declare(Fact("M"))
        self.declare(Fact("N"))

    # Si O entonces S, R
    @Rule(Fact("O"))
    def regla_10(self):
        self.declare(Fact("S"))
        self.declare(Fact("R"))

    # Si AI entonces AA, DD
    @Rule(Fact(c.DOS_CARRERAS))
    def regla_11(self):
        self.declare(Fact("AA"))
        self.declare(Fact("DD"))

    # Si AI, AG entonces GG
    @Rule(Fact(c.DOS_CARRERAS), Fact(c.CURSA_TODAS))
    def regla_12(self):
        self.declare(Fact("GG"))

    # Si DD entonces EE
    @Rule(Fact("DD"))
    def regla_13(self):
        self.declare(Fact("EE"))

    # Si AB, AF, AI entonces BB
    @Rule(Fact(c.SOLO_ESTUDIA), Fact(c.CURSA_ALGUNAS), Fact(c.DOS_CARRERAS))
    def regla_14(self):
        self.declare(Fact("BB"))

    # Si BB entonces CC
    @Rule(Fact("BB"))
    def regla_15(self):
        self.declare(Fact("CC"))

    # Si AE, AG entonces KK, GG (Trabaja Noche y Cursa Todo)
    @Rule(Fact(c.TRABAJA_NOCHE), Fact(c.CURSA_TODAS))
    def regla_16(self):
        self.declare(Fact("KK"))
        self.declare(Fact("GG"))

    # Si GG entonces HH, K, II
    @Rule(Fact("GG"))
    def regla_17(self):
        self.declare(Fact("HH"))
        self.declare(Fact("K"))
        self.declare(Fact("II"))

    # Si HH entonces JJ, M, N
    @Rule(Fact("HH"))
    def regla_18(self):
        self.declare(Fact("JJ"))
        self.declare(Fact("M"))
        self.declare(Fact("N"))

    # Si AI, AH entonces LL, MM
    @Rule(Fact(c.DOS_CARRERAS), Fact(c.RETOMA_ESTUDIO))
    def regla_19(self):
        self.declare(Fact("LL"))
        self.declare(Fact("MM"))

    # Si AI, GG entonces NN
    @Rule(Fact(c.DOS_CARRERAS), Fact("GG"))
    def regla_20(self):
        self.declare(Fact("NN"))

    # Si LL entonces OO
    @Rule(Fact("LL"))
    def regla_21(self):
        self.declare(Fact("OO"))

    # Si MM entonces A
    @Rule(Fact("MM"))
    def regla_22(self):
        self.declare(Fact("A"))

    # Si AE, AF entonces BB
    @Rule(Fact(c.TRABAJA_NOCHE), Fact(c.CURSA_ALGUNAS))
    def regla_23(self):
        self.declare(Fact("BB"))

    # Si BB entonces HH, RR (Nota: BB ya tenía otra regla arriba, se suman las consecuencias)
    @Rule(Fact("BB"))
    def regla_24(self):
        self.declare(Fact("HH"))
        self.declare(Fact("RR"))

    # Si HH entonces N, M (Nota: HH ya tenía otra regla arriba, se suman)
    @Rule(Fact("HH"))
    def regla_25(self):
        self.declare(Fact("N"))
        self.declare(Fact("M"))

    # Si AF, AC, AD entonces QQ (Algunas, Mañana y Tarde)
    @Rule(Fact(c.CURSA_ALGUNAS), Fact(c.TRABAJA_MANANA), Fact(c.TRABAJA_TARDE))
    def regla_26(self):
        self.declare(Fact("QQ"))

    # Si QQ entonces G
    @Rule(Fact("QQ"))
    def regla_27(self):
        self.declare(Fact("G"))

    # Si AC, AE entonces QQ (Mañana y Noche)
    @Rule(Fact(c.TRABAJA_MANANA), Fact(c.TRABAJA_NOCHE))
    def regla_28(self):
        self.declare(Fact("QQ"))

def ejecutar_motor(hechos_iniciales):
    """
    Recibe un SET de hechos iniciales (ej: {'AB', 'AG'})
    e inicia el motor de inferencia.
    """
    engine = RecomendadorEstudios()
    engine.reset()
    
    print("\n--- ANALIZANDO PERFIL DEL ESTUDIANTE ---\n")
    
    # Cargar los hechos capturados en el main
    for codigo in hechos_iniciales:
        engine.declare(Fact(codigo))
        
    engine.run()