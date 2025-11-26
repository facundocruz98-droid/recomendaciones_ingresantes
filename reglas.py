# reglas.py
# Requiere: pip install experta
from experta import KnowledgeEngine, Fact, Rule, AND

class SBC_Engine(KnowledgeEngine):
    # Reglas (las tuyas, copiadas tal cual)
    @Rule(AND(Fact(code='AB'), Fact(code='AG')))
    def r_ab_ag_a(self):
        self.declare(Fact(code='A'))

    @Rule(Fact(code='AB'))
    def r_ab_ff(self):
        self.declare(Fact(code='FF'))

    @Rule(Fact(code='FF'))
    def r_ff_e_v(self):
        self.declare(Fact(code='E'))
        self.declare(Fact(code='V'))

    @Rule(Fact(code='AG'))
    def r_ag_b_c_d_aa(self):
        self.declare(Fact(code='B'))
        self.declare(Fact(code='C'))
        self.declare(Fact(code='D'))
        self.declare(Fact(code='AA'))

    @Rule(Fact(code='AH'))
    def r_ah_i_k(self):
        self.declare(Fact(code='I'))
        self.declare(Fact(code='K'))

    @Rule(Fact(code='K'))
    def r_k_x(self):
        self.declare(Fact(code='X'))

    @Rule(Fact(code='AF'))
    def r_af_f_t_u_ll(self):
        self.declare(Fact(code='F'))
        self.declare(Fact(code='T'))
        self.declare(Fact(code='U'))
        self.declare(Fact(code='LL'))

    @Rule(Fact(code='AD'))
    def r_ad_l_m(self):
        self.declare(Fact(code='L'))
        self.declare(Fact(code='M'))

    @Rule(Fact(code='AC'))
    def r_ac_m_n(self):
        self.declare(Fact(code='M'))
        self.declare(Fact(code='N'))

    @Rule(Fact(code='O'))
    def r_o_s_r(self):
        self.declare(Fact(code='S'))
        self.declare(Fact(code='R'))

    @Rule(Fact(code='AI'))
    def r_ai_aa_dd(self):
        self.declare(Fact(code='AA'))
        self.declare(Fact(code='DD'))

    @Rule(AND(Fact(code='AI'), Fact(code='AG')))
    def r_ai_ag_gg(self):
        self.declare(Fact(code='GG'))

    @Rule(Fact(code='DD'))
    def r_dd_ee(self):
        self.declare(Fact(code='EE'))

    @Rule(AND(Fact(code='AB'), Fact(code='AF'), Fact(code='AI')))
    def r_ab_af_ai_bb(self):
        self.declare(Fact(code='BB'))

    @Rule(Fact(code='BB'))
    def r_bb_cc(self):
        self.declare(Fact(code='CC'))

    @Rule(AND(Fact(code='AE'), Fact(code='AG')))
    def r_ae_ag_kk_gg(self):
        self.declare(Fact(code='KK'))
        self.declare(Fact(code='GG'))

    @Rule(Fact(code='GG'))
    def r_gg_hh_k_ii(self):
        self.declare(Fact(code='HH'))
        self.declare(Fact(code='K'))
        self.declare(Fact(code='II'))

    @Rule(Fact(code='HH'))
    def r_hh_jj_m_n(self):
        self.declare(Fact(code='JJ'))
        self.declare(Fact(code='M'))
        self.declare(Fact(code='N'))

    @Rule(AND(Fact(code='AI'), Fact(code='AH')))
    def r_ai_ah_ll_mm(self):
        self.declare(Fact(code='LL'))
        self.declare(Fact(code='MM'))

    @Rule(AND(Fact(code='AI'), Fact(code='GG')))
    def r_ai_gg_nn(self):
        self.declare(Fact(code='NN'))

    @Rule(Fact(code='LL'))
    def r_ll_oo(self):
        self.declare(Fact(code='OO'))

    @Rule(Fact(code='MM'))
    def r_mm_a(self):
        self.declare(Fact(code='A'))

    @Rule(AND(Fact(code='AE'), Fact(code='AF')))
    def r_ae_af_bb(self):
        self.declare(Fact(code='BB'))

    @Rule(Fact(code='BB'))
    def r_bb_hh_rr(self):
        self.declare(Fact(code='HH'))
        self.declare(Fact(code='RR'))

    @Rule(Fact(code='HH'))
    def r_hh_n_m(self):
        self.declare(Fact(code='N'))
        self.declare(Fact(code='M'))

    @Rule(AND(Fact(code='AF'), Fact(code='AC'), Fact(code='AD')))
    def r_af_ac_ad_qq(self):
        self.declare(Fact(code='QQ'))

    @Rule(Fact(code='QQ'))
    def r_qq_g(self):
        self.declare(Fact(code='G'))

    @Rule(AND(Fact(code='AC'), Fact(code='AE')))
    def r_ac_ae_qq(self):
        self.declare(Fact(code='QQ'))


def ejecutar_motor(hechos):
    """
    Recibe 'hechos' (dict). Declara en el motor los keys boolean True
    y ejecuta las reglas. Devuelve lista ordenada de códigos activos.
    """
    engine = SBC_Engine()
    engine.reset()

    for k, v in hechos.items():
        # declaramos solo claves booleanas relevantes
        if isinstance(v, bool) and v:
            engine.declare(Fact(code=k))

    engine.run()

    codes = set()
    for fid, fact in engine.facts.items():
        try:
            c = fact['code']
            if isinstance(c, str):
                codes.add(c)
        except Exception:
            pass

    return sorted(codes)
