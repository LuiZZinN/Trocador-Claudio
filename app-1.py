import streamlit as st
import math

st.set_page_config(page_title="Simulador de Trocador de Calor", layout="wide")

Fluidos = [
    { "id": 1, "nome": "Acetona", "rho": 791, "mu": 0.0003, "k": 0.16, "cp": 2150, "Tref": 25, "a_rho": -7e-4, "a_mu": -2.0e-2, "a_k": 1.2e-3, "a_cp": 9e-4, "classe_fouling": 2, "Tsat": 56, "h_vap": 518000, "M": 0.05808 },
    { "id": 2, "nome": "Ácido cítrico 10%", "rho": 1045, "mu": 0.003, "k": 0.52, "cp": 3600, "Tref": 25, "a_rho": -3e-4, "a_mu": -2.5e-2, "a_k": 1.5e-3, "a_cp": 8e-4, "classe_fouling": 1, "Tsat": None, "h_vap": None, "M": None },
    { "id": 3, "nome": "Ácido sulfúrico 98%", "rho": 1840, "mu": 0.025, "k": 0.25, "cp": 1380, "Tref": 25, "a_rho": -3e-4, "a_mu": -2.8e-2, "a_k": 1.0e-3, "a_cp": 7e-4, "classe_fouling": 1, "Tsat": 337, "h_vap": 420000, "M": 0.09808 },
    { "id": 4, "nome": "Água", "rho": 997, "mu": 0.00089, "k": 0.606, "cp": 4182, "Tref": 25, "a_rho": -3e-4, "a_mu": -2.5e-2, "a_k": 1.5e-3, "a_cp": 8e-4, "classe_fouling": 1, "Tsat": 100, "h_vap": 2257000, "M": 0.018015 },
    { "id": 5, "nome": "Água salobra", "rho": 1015, "mu": 0.0012, "k": 0.58, "cp": 4000, "Tref": 25, "a_rho": -3e-4, "a_mu": -2.5e-2, "a_k": 1.5e-3, "a_cp": 8e-4, "classe_fouling": 1, "Tsat": 102, "h_vap": 2250000, "M": 0.018015 },
    { "id": 6, "nome": "Amônia (gás)", "rho": 0.73, "mu": 9.82e-6, "k": 0.024, "cp": 2090, "Tref": 25, "a_rho": -3e-3, "a_mu": 1.5e-2, "a_k": 1.7e-3, "a_cp": 3e-4, "classe_fouling": 6, "Tsat": None, "h_vap": None, "M": 0.01703 },
    { "id": 7, "nome": "Amônia líquida", "rho": 682, "mu": 0.00025, "k": 0.504, "cp": 4700, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.0e-2, "a_k": 1.0e-3, "a_cp": 9e-4, "classe_fouling": 7, "Tsat": -33, "h_vap": 1370000, "M": 0.01703 },
    { "id": 8, "nome": "Ar (gás)", "rho": 1.184, "mu": 1.85e-5, "k": 0.0262, "cp": 1005, "Tref": 25, "a_rho": -3e-3, "a_mu": 1.5e-2, "a_k": 1.7e-3, "a_cp": 3e-4, "classe_fouling": 6, "Tsat": None, "h_vap": None, "M": 0.02897 },
    { "id": 9, "nome": "Biodiesel", "rho": 880, "mu": 0.0045, "k": 0.17, "cp": 2000, "Tref": 25, "a_rho": -7e-4, "a_mu": -3.5e-2, "a_k": 1.2e-3, "a_cp": 1.0e-3, "classe_fouling": 3, "Tsat": 330, "h_vap": 250000, "M": 0.29200 },
    { "id": 10, "nome": "CO2 (gás)", "rho": 1.842, "mu": 1.48e-5, "k": 0.0166, "cp": 846, "Tref": 25, "a_rho": -3e-3, "a_mu": 1.4e-2, "a_k": 1.6e-3, "a_cp": 3e-4, "classe_fouling": 6, "Tsat": None, "h_vap": None, "M": 0.04401 },
    { "id": 11, "nome": "Creme de leite", "rho": 980, "mu": 0.005, "k": 0.5, "cp": 3700, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.5e-2, "a_k": 9e-4, "a_cp": 1.0e-3, "classe_fouling": 5, "Tsat": None, "h_vap": None, "M": None },
    { "id": 12, "nome": "Diesel", "rho": 830, "mu": 0.003, "k": 0.13, "cp": 2100, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.5e-2, "a_k": 8e-4, "a_cp": 1.1e-3, "classe_fouling": 3, "Tsat": 180, "h_vap": 250000, "M": 0.17000 },
    { "id": 13, "nome": "Etanol", "rho": 785.3, "mu": 0.00104, "k": 0.169, "cp": 2440, "Tref": 25, "a_rho": -7e-4, "a_mu": -2.0e-2, "a_k": 1.2e-3, "a_cp": 9e-4, "classe_fouling": 2, "Tsat": 78.3, "h_vap": 846000, "M": 0.04607 },
    { "id": 14, "nome": "Etileno glicol 30%", "rho": 1040, "mu": 0.004, "k": 0.38, "cp": 3500, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.0e-2, "a_k": 1.0e-3, "a_cp": 9e-4, "classe_fouling": 1, "Tsat": None, "h_vap": None, "M": None },
    { "id": 15, "nome": "Gasolina", "rho": 740, "mu": 0.0006, "k": 0.147, "cp": 2220, "Tref": 25, "a_rho": -6e-4, "a_mu": -2.5e-2, "a_k": 1.0e-3, "a_cp": 9e-4, "classe_fouling": 2, "Tsat": 95, "h_vap": 350000, "M": 0.11400 },
    { "id": 16, "nome": "Glicerina pura", "rho": 1260, "mu": 1.49, "k": 0.29, "cp": 2430, "Tref": 25, "a_rho": -6e-4, "a_mu": -4.0e-2, "a_k": 7e-4, "a_cp": 1.1e-3, "classe_fouling": 4, "Tsat": 290, "h_vap": 900000, "M": 0.09209 },
    { "id": 17, "nome": "Hidrogênio (gás)", "rho": 0.0837, "mu": 8.9e-6, "k": 0.18, "cp": 14300, "Tref": 25, "a_rho": -3e-3, "a_mu": 1.6e-2, "a_k": 2.0e-3, "a_cp": 3e-4, "classe_fouling": 6, "Tsat": None, "h_vap": None, "M": 0.002016 },
    { "id": 18, "nome": "Iogurte natural", "rho": 1040, "mu": 0.004, "k": 0.48, "cp": 3600, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.5e-2, "a_k": 9e-4, "a_cp": 1.0e-3, "classe_fouling": 5, "Tsat": None, "h_vap": None, "M": None },
    { "id": 19, "nome": "Leite integral", "rho": 1032, "mu": 0.003, "k": 0.53, "cp": 3900, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.0e-2, "a_k": 1.0e-3, "a_cp": 1.0e-3, "classe_fouling": 5, "Tsat": None, "h_vap": None, "M": None },
    { "id": 20, "nome": "Mel", "rho": 1420, "mu": 10, "k": 0.52, "cp": 2900, "Tref": 25, "a_rho": -6e-4, "a_mu": -4.0e-2, "a_k": 7e-4, "a_cp": 1.1e-3, "classe_fouling": 4, "Tsat": None, "h_vap": None, "M": None },
    { "id": 21, "nome": "Melado de açúcar", "rho": 1350, "mu": 5, "k": 0.5, "cp": 3100, "Tref": 25, "a_rho": -6e-4, "a_mu": -4.0e-2, "a_k": 7e-4, "a_cp": 1.1e-3, "classe_fouling": 4, "Tsat": None, "h_vap": None, "M": None },
    { "id": 22, "nome": "Metano (gás)", "rho": 0.656, "mu": 1.12e-5, "k": 0.034, "cp": 2220, "Tref": 25, "a_rho": -3e-3, "a_mu": 1.5e-2, "a_k": 1.7e-3, "a_cp": 3e-4, "classe_fouling": 6, "Tsat": None, "h_vap": None, "M": 0.01604 },
    { "id": 23, "nome": "Metanol", "rho": 792, "mu": 0.0006, "k": 0.2, "cp": 2510, "Tref": 25, "a_rho": -7e-4, "a_mu": -2.0e-2, "a_k": 1.2e-3, "a_cp": 9e-4, "classe_fouling": 2, "Tsat": 64.7, "h_vap": 1100000, "M": 0.03204 },
    { "id": 24, "nome": "Nafta", "rho": 680, "mu": 0.0005, "k": 0.12, "cp": 2300, "Tref": 25, "a_rho": -6e-4, "a_mu": -2.5e-2, "a_k": 1.0e-3, "a_cp": 9e-4, "classe_fouling": 2, "Tsat": 120, "h_vap": 320000, "M": 0.11000 },
    { "id": 25, "nome": "Óleo de soja", "rho": 922, "mu": 0.06, "k": 0.156, "cp": 1650, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.5e-2, "a_k": 8e-4, "a_cp": 1.1e-3, "classe_fouling": 3, "Tsat": 300, "h_vap": 300000, "M": 0.88000 },
    { "id": 26, "nome": "Óleo SAE 40", "rho": 890, "mu": 0.25, "k": 0.144, "cp": 1800, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.8e-2, "a_k": 8e-4, "a_cp": 1.1e-3, "classe_fouling": 4, "Tsat": 320, "h_vap": 300000, "M": 0.45000 },
    { "id": 27, "nome": "Oxigênio (gás)", "rho": 1.331, "mu": 2.07e-5, "k": 0.026, "cp": 918, "Tref": 25, "a_rho": -3e-3, "a_mu": 1.5e-2, "a_k": 1.7e-3, "a_cp": 3e-4, "classe_fouling": 6, "Tsat": None, "h_vap": None, "M": 0.03200 },
    { "id": 28, "nome": "Propileno glicol", "rho": 1036, "mu": 0.052, "k": 0.21, "cp": 2500, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.5e-2, "a_k": 9e-4, "a_cp": 1.0e-3, "classe_fouling": 3, "Tsat": 188, "h_vap": 700000, "M": 0.07609 },
    { "id": 29, "nome": "Propileno glicol 30%", "rho": 1030, "mu": 0.01, "k": 0.36, "cp": 3200, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.0e-2, "a_k": 1.0e-3, "a_cp": 9e-4, "classe_fouling": 1, "Tsat": None, "h_vap": None, "M": None },
    { "id": 30, "nome": "Querosene", "rho": 810, "mu": 0.0018, "k": 0.14, "cp": 2000, "Tref": 25, "a_rho": -6e-4, "a_mu": -2.8e-2, "a_k": 1.0e-3, "a_cp": 9e-4, "classe_fouling": 2, "Tsat": 175, "h_vap": 300000, "M": 0.17000 },
    { "id": 31, "nome": "R-134a (líquido)", "rho": 1206, "mu": 0.00021, "k": 0.081, "cp": 1420, "Tref": 25, "a_rho": -6e-4, "a_mu": -2.5e-2, "a_k": 1.2e-3, "a_cp": 8e-4, "classe_fouling": 7, "Tsat": -26.3, "h_vap": 216000, "M": 0.10203 },
    { "id": 32, "nome": "R22", "rho": 1191, "mu": 0.00019, "k": 0.083, "cp": 1380, "Tref": 25, "a_rho": -6e-4, "a_mu": -2.5e-2, "a_k": 1.2e-3, "a_cp": 8e-4, "classe_fouling": 7, "Tsat": -40.8, "h_vap": 233000, "M": 0.08647 },
    { "id": 33, "nome": "R404A", "rho": 1040, "mu": 0.00035, "k": 0.078, "cp": 1250, "Tref": 25, "a_rho": -6e-4, "a_mu": -2.6e-2, "a_k": 1.2e-3, "a_cp": 8e-4, "classe_fouling": 7, "Tsat": -46.5, "h_vap": 200000, "M": 0.09760 },
    { "id": 34, "nome": "R410A", "rho": 1040, "mu": 0.00025, "k": 0.087, "cp": 1500, "Tref": 25, "a_rho": -6e-4, "a_mu": -2.6e-2, "a_k": 1.2e-3, "a_cp": 8e-4, "classe_fouling": 7, "Tsat": -51.6, "h_vap": 240000, "M": 0.07258 },
    { "id": 35, "nome": "Soda cáustica 30%", "rho": 1280, "mu": 0.05, "k": 0.48, "cp": 3400, "Tref": 25, "a_rho": -3e-4, "a_mu": -3.0e-2, "a_k": 1.2e-3, "a_cp": 8e-4, "classe_fouling": 1, "Tsat": 105, "h_vap": 2200000, "M": 0.018015 },
    { "id": 36, "nome": "Solução salina 0.9%", "rho": 1005, "mu": 0.001, "k": 0.58, "cp": 4000, "Tref": 25, "a_rho": -3e-4, "a_mu": -2.5e-2, "a_k": 1.5e-3, "a_cp": 8e-4, "classe_fouling": 1, "Tsat": 100.5, "h_vap": 2250000, "M": 0.018015 },
    { "id": 37, "nome": "Solução salina 10%", "rho": 1030, "mu": 0.0012, "k": 0.6, "cp": 4000, "Tref": 25, "a_rho": -3e-4, "a_mu": -2.5e-2, "a_k": 1.5e-3, "a_cp": 8e-4, "classe_fouling": 1, "Tsat": 103, "h_vap": 2230000, "M": 0.018015 },
    { "id": 38, "nome": "Suco de abacaxi", "rho": 1025, "mu": 0.0014, "k": 0.52, "cp": 3850, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.0e-2, "a_k": 1.0e-3, "a_cp": 1.0e-3, "classe_fouling": 5, "Tsat": None, "h_vap": None, "M": None },
    { "id": 39, "nome": "Suco de laranja", "rho": 1040, "mu": 0.0015, "k": 0.5, "cp": 3800, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.0e-2, "a_k": 1.0e-3, "a_cp": 1.0e-3, "classe_fouling": 5, "Tsat": None, "h_vap": None, "M": None },
    { "id": 40, "nome": "Suco de maçã", "rho": 1030, "mu": 0.0012, "k": 0.48, "cp": 3700, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.0e-2, "a_k": 1.0e-3, "a_cp": 1.0e-3, "classe_fouling": 5, "Tsat": None, "h_vap": None, "M": None },
    { "id": 41, "nome": "Suco de tomate", "rho": 1080, "mu": 0.0035, "k": 0.4, "cp": 3500, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.2e-2, "a_k": 9e-4, "a_cp": 1.0e-3, "classe_fouling": 5, "Tsat": None, "h_vap": None, "M": None },
    { "id": 42, "nome": "Suco de uva", "rho": 1055, "mu": 0.0018, "k": 0.45, "cp": 3600, "Tref": 25, "a_rho": -6e-4, "a_mu": -3.0e-2, "a_k": 9e-4, "a_cp": 1.0e-3, "classe_fouling": 5, "Tsat": None, "h_vap": None, "M": None },
    { "id": 43, "nome": "Vapor d’água (100°C)", "rho": 0.598, "mu": 1.25e-5, "k": 0.025, "cp": 2010, "Tref": 100, "a_rho": -3e-3, "a_mu": 1.6e-2, "a_k": 1.7e-3, "a_cp": 3e-4, "classe_fouling": 6, "Tsat": 100, "h_vap": 2257000, "M": 0.018015 },
    { "id": 44, "nome": "Xarope de glicose", "rho": 1550, "mu": 1.5, "k": 0.4, "cp": 2500, "Tref": 25, "a_rho": -6e-4, "a_mu": -4.0e-2, "a_k": 7e-4, "a_cp": 1.1e-3, "classe_fouling": 4, "Tsat": None, "h_vap": None, "M": None },
    { "id": 45, "nome": "Xarope de milho", "rho": 1320, "mu": 5, "k": 0.45, "cp": 3100, "Tref": 25, "a_rho": -6e-4, "a_mu": -4.0e-2, "a_k": 7e-4, "a_cp": 1.1e-3, "classe_fouling": 4, "Tsat": None, "h_vap": None, "M": None }
]

Materiais = [
    { "id": 1, "nome": "Aço Carbono", "k": 45 },
    { "id": 2, "nome": "Aço Inox 304", "k": 16 },
    { "id": 3, "nome": "Aço Inox 316", "k": 14 },
    { "id": 4, "nome": "Cobre", "k": 385 },
    { "id": 5, "nome": "Latão", "k": 110 },
    { "id": 6, "nome": "Alumínio", "k": 205 },
    { "id": 7, "nome": "Titânio", "k": 22 },
    { "id": 8, "nome": "Monel", "k": 26 },
    { "id": 9, "nome": "Inconel", "k": 15 },
    { "id": 10, "nome": "Aço Duplex", "k": 19 }
]

def atualiza_propriedades_T(fluido, T):
    dT = T - fluido['Tref']
    return {
        **fluido,
        'rho': fluido['rho'] * (1 + fluido['a_rho'] * dT),
        'mu': fluido['mu'] * math.exp(fluido['a_mu'] * dT),
        'k': fluido['k'] * (1 + fluido['a_k'] * dT),
        'cp': fluido['cp'] * (1 + fluido['a_cp'] * dT)
    }

def calcula_h_monofasico(Dh, v, fluido):
    Re = (fluido['rho'] * v * Dh) / fluido['mu']
    Pr = (fluido['cp'] * fluido['mu']) / fluido['k']

    if Re < 2100:
        Nu = 3.66
    elif Re < 10000:
        f = (0.79 * math.log(Re) - 1.64)**(-2)
        Nu = ((f / 8) * (Re - 1000) * Pr) / (1 + 12.7 * math.sqrt(f / 8) * (Pr**(2 / 3) - 1))
    else:
        Nu = 0.023 * (Re**0.8) * (Pr**0.4)

    return (Nu * fluido['k']) / Dh

def calcula_h_condensacao(Dh, fluido):
    if fluido['Tsat'] is None or fluido['h_vap'] is None or fluido['M'] is None:
        return 1000
    rho_l = fluido['rho'] * (1 + fluido['a_rho'] * (fluido['Tsat'] - fluido['Tref']))
    R = 8.3144
    T_sat_K = fluido['Tsat'] + 273.15
    P_operacao = 1
    rho_v = (P_operacao * fluido['M']) / (R * T_sat_K)
    
    hfg = fluido['h_vap']
    g = 9.81
    DeltaT = 5

    h = 0.943 * (((rho_l * (rho_l - rho_v) * g * hfg * (fluido['k']**3)) / (fluido['mu'] * Dh * DeltaT))**(1/4))
    return h

def calcula_h_evaporacao(Dh, v, fluido):
    h_conv = calcula_h_monofasico(Dh, v, fluido)
    Re = (fluido['rho'] * v * Dh) / fluido['mu']

    S = 6
    if Re < 3000:
        S = 2.5
    elif Re < 10000:
        S = 4

    return S * h_conv

def identifica_fase(Tin, Tout, fluido):
    if fluido['Tsat'] is None:
        return 'monofasico'
    if Tin > fluido['Tsat'] and Tout <= fluido['Tsat']:
        return 'condensacao'
    if Tin < fluido['Tsat'] and Tout >= fluido['Tsat']:
        return 'evaporacao'
    return 'monofasico'

def calcula_h_geral(Dh, v, fluido, Tin, Tout):
    modo = identifica_fase(Tin, Tout, fluido)
    if modo == 'monofasico':
        return calcula_h_monofasico(Dh, v, fluido)
    if modo == 'condensacao':
        return calcula_h_condensacao(Dh, fluido)
    if modo == 'evaporacao':
        return calcula_h_evaporacao(Dh, v, fluido)
    return 0

def calcula_h_casco_Kern(D_casco, d_o, mdot, fluido, arranjo):
    p_t = 1.25 * d_o if arranjo == 1 else 1.33 * d_o
    B = 0.5 * D_casco
    A_s = (D_casco * B * (p_t - d_o)) / p_t
    v_s = mdot / (fluido['rho'] * A_s)
    D_hs = 4 * ((p_t**2) - (math.pi * (d_o**2) / 4)) / (math.pi * d_o)
    
    Re_s = abs(fluido['rho'] * v_s * D_hs) / fluido['mu']
    Pr = (fluido['cp'] * fluido['mu']) / fluido['k']
    Nu_s = 0.36 * (Re_s**0.55) * (Pr**(1/3))
    
    return (Nu_s * fluido['k']) / D_hs

def calcula_LMTD(Ti_in, Ti_out, Te_in, Te_out):
    DT1 = abs(Ti_in - Te_out)
    DT2 = abs(Ti_out - Te_in)
    if abs(DT1 - DT2) < 0.01:
        return DT1
    return (DT1 - DT2) / math.log(DT1 / DT2)

def calcula_Ds_selba(Nt, Pt, arranjo, n_passes):
    C, z = 0.29, 2.14
    if arranjo == 2:
        if n_passes == 1: C, z = 0.319, 2.142
        elif n_passes == 2: C, z = 0.249, 2.207
        elif n_passes == 4: C, z = 0.175, 2.285
        elif n_passes == 6: C, z = 0.0743, 2.499
        elif n_passes == 8: C, z = 0.0365, 2.675
    else:
        if n_passes == 1: C, z = 0.29, 2.14
        elif n_passes == 2: C, z = 0.23, 2.21
        elif n_passes == 4: C, z = 0.16, 2.28
        elif n_passes == 6: C, z = 0.068, 2.50
        elif n_passes == 8: C, z = 0.033, 2.68
    return Pt * ((Nt / C) ** (1 / z))

def calcula_taxa_fouling(fluido, Re, T_med):
    classe = fluido['classe_fouling']
    T_K = T_med + 273.15
    taxa = 0
    if classe == 1:
        K = 4e-5
        c = 0.006
        taxa = K * (Re**-0.8) * math.exp(c * T_med)
    elif classe == 2:
        K = 3e-5
        taxa = K * (Re**-0.5)
    elif classe == 3:
        K = 1.5e-3
        B = 1500
        taxa = K * math.exp(-B / T_K)
    elif classe == 4:
        K = 2.0e-8
        taxa = K * (T_med**2)
    elif classe == 5:
        K = 1.5e-6
        taxa = K * math.sqrt(max(0, T_med))
    elif classe == 6:
        taxa = 3e-8
    elif classe == 7:
        K = 2e-5
        taxa = K * (Re**-0.3)
    return taxa

def runSimulation(params, chosenPasses=None):
    id_i = params['id_i']
    id_e = params['id_e']
    id_mat = params['id_mat']
    D_tubo_mm = params['D_tubo_mm']
    espessura_mm = params['espessura_mm']
    L_tubo = params['L_tubo']
    arranjo = params['arranjo']
    mdot_i_kgh = params['mdot_i_kgh']
    mdot_e_kgh = params['mdot_e_kgh']
    Ti_in = params['Ti_in']
    Ti_out = params['Ti_out']
    Te_in = params['Te_in']
    usaBellDelaware = params['usaBellDelaware']
    Jc = params['Jc']
    Jl = params['Jl']
    Jb = params['Jb']
    Js = params['Js']
    Jr = params['Jr']
    T_saida_min_tubo = params.get('T_saida_min_tubo')
    T_saida_limite_casco = params.get('T_saida_limite_casco')

    fluido_i_base = next(f for f in Fluidos if f['id'] == id_i)
    fluido_e_base = next(f for f in Fluidos if f['id'] == id_e)
    mat = next(m for m in Materiais if m['id'] == id_mat)

    D_tubo = D_tubo_mm / 1000
    espessura = espessura_mm / 1000
    D_o = D_tubo + 2 * espessura
    k_tubo = mat['k']

    mdot_i = mdot_i_kgh / 3600
    mdot_e = mdot_e_kgh / 3600

    Tmed_i = (Ti_in + Ti_out) / 2
    fluido_i = atualiza_propriedades_T(fluido_i_base, Tmed_i)
    modo_i = identifica_fase(Ti_in, Ti_out, fluido_i)

    Qt = 0
    if modo_i == 'monofasico':
        Qt = mdot_i * fluido_i['cp'] * abs(Ti_out - Ti_in)
    elif fluido_i['h_vap']:
        Qt = mdot_i * fluido_i['h_vap']

    Te_out = 0
    deltaT_casco = Qt / (mdot_e * fluido_e_base['cp'])

    if Ti_in > Ti_out:
        Te_out = Te_in + deltaT_casco
    else:
        Te_out = Te_in - deltaT_casco

    Tmed_e = (Te_in + Te_out) / 2
    fluido_e = atualiza_propriedades_T(fluido_e_base, Tmed_e)
    modo_e = identifica_fase(Te_in, Te_out, fluido_e)

    Qc = 0
    if modo_e == 'monofasico':
        Qc = mdot_e * fluido_e['cp'] * abs(Te_out - Te_in)
    elif fluido_e['h_vap']:
        Qc = mdot_e * fluido_e['h_vap']

    DTlm = calcula_LMTD(Ti_in, Ti_out, Te_in, Te_out)
    
    R_val = (Ti_in - Ti_out) / (Te_out - Te_in) if (Te_out - Te_in) != 0 else 0
    S_val = (Te_out - Te_in) / (Ti_in - Te_in) if (Ti_in - Te_in) != 0 else 0
    DT1 = Ti_in - Te_out
    DT2 = Ti_out - Te_in

    F_base = -1
    if R_val > 0 and S_val > 0 and S_val < 1 and R_val * S_val < 1:
        raiz = math.sqrt(R_val * R_val + 1)
        termo1 = (1 - S_val) / (1 - R_val * S_val)
        termo2 = (2 - S_val * (R_val + 1 - raiz)) / (2 - S_val * (R_val + 1 + raiz))

        if termo1 > 0 and termo2 > 0:
            num = raiz * math.log(termo1)
            den = (R_val - 1) * math.log(termo2)
            if den != 0:
                F_temp = num / den
                if F_temp > 0 and F_temp <= 1:
                    F_base = F_temp

    possiveisConfigs = []
    eMonofasico = (modo_i == 'monofasico' and modo_e == 'monofasico')

    if eMonofasico:
        if DT1 * DT2 > 0:
            possiveisConfigs.append({"n_passes": 1, "F": 1.0, "config": "1-1 (Contracorrente)"})
        if F_base > 0:
            possiveisConfigs.append({"n_passes": 2, "F": F_base, "config": "1-2"})
            possiveisConfigs.append({"n_passes": 4, "F": min(1.0, F_base + 0.08), "config": "1-4"})
            possiveisConfigs.append({"n_passes": 6, "F": min(1.0, F_base + 0.13), "config": "1-6"})
            possiveisConfigs.append({"n_passes": 8, "F": min(1.0, F_base + 0.18), "config": "1-8"})
        else:
            if len(possiveisConfigs) == 0:
                possiveisConfigs.append({"n_passes": 1, "F": 1.0, "config": "1-1 (Forçado/Contracorrente)"})
    else:
        possiveisConfigs.append({"n_passes": 1, "F": 1.0, "config": "1-1 (Mudança de fase)"})
        possiveisConfigs.append({"n_passes": 2, "F": 1.0, "config": "1-2 (Mudança de fase)"})
        possiveisConfigs.append({"n_passes": 4, "F": 1.0, "config": "1-4 (Mudança de fase)"})
        possiveisConfigs.append({"n_passes": 6, "F": 1.0, "config": "1-6 (Mudança de fase)"})
        possiveisConfigs.append({"n_passes": 8, "F": 1.0, "config": "1-8 (Mudança de fase)"})

    J_total = Jc * Jl * Jb * Js * Jr if usaBellDelaware else 1
    Pt = 1.33 * D_o if arranjo == 2 else 1.25 * D_o
    R_parede = (D_o * math.log(D_o / D_tubo)) / (2 * k_tubo)

    v_min_tubo = 0.6
    v_max_tubo = 2.5
    h_i_min = calcula_h_geral(D_tubo, v_min_tubo, fluido_i, Ti_in, Ti_out)
    A_fluxo_tubo = math.pi * (D_tubo**2) / 4
    
    Nt_min = math.ceil(mdot_i / (fluido_i['rho'] * v_max_tubo * A_fluxo_tubo))
    if Nt_min < 1: Nt_min = 1

    def simulaConfig(p_passes, p_F, p_config):
        nonlocal Nt_min, mdot_i, mdot_e, Qt, DTlm, D_o, L_tubo, fluide_i, fluido_e, Ti_in, Ti_out, Te_in, Te_out
        D_casco_min = calcula_Ds_selba(Nt_min, Pt, arranjo, p_passes)
        h_e_min = calcula_h_casco_Kern(D_casco_min, D_o, mdot_e, fluido_e, arranjo) * J_total

        U_est = 1 / (1 / h_i_min + 1 / h_e_min + R_parede)
        A_proj = Qt / (U_est * p_F * DTlm)
        A_tubo = math.pi * D_o * L_tubo
        Nt_curr = math.ceil(A_proj / A_tubo)
        if Nt_curr < 1: Nt_curr = 1

        erro = 999
        iter_num = 0
        D_casco_curr = v_tubo_curr = v_casco_curr = h_i_curr = h_e_curr = U_curr = A_curr = Q_curr = 0

        while erro > 0.05 and iter_num < 50:
            iter_num += 1
            D_casco_curr = calcula_Ds_selba(Nt_curr, Pt, arranjo, p_passes)
            
            A_fluxo_curr_tubos = Nt_curr * A_fluxo_tubo / p_passes
            v_tubo_curr = mdot_i / (fluido_i['rho'] * A_fluxo_curr_tubos)

            B_val = 0.25 * D_casco_curr
            A_s_val = (D_casco_curr * B_val * (Pt - D_o)) / Pt
            v_casco_curr = mdot_e / (fluido_e['rho'] * A_s_val)

            h_i_curr = calcula_h_geral(D_tubo, v_tubo_curr, fluido_i, Ti_in, Ti_out)
            h_e_curr = calcula_h_casco_Kern(D_casco_curr, D_o, mdot_e, fluido_e, arranjo) * J_total

            U_curr = 1 / (1 / h_i_curr + 1 / h_e_curr + R_parede)
            A_curr = Nt_curr * math.pi * D_o * L_tubo
            Q_curr = U_curr * A_curr * p_F * DTlm

            erro = abs(Q_curr - Qt) / Qt

            if erro > 0.05:
                Nt_novo = math.ceil(Nt_curr * Qt / Q_curr)
                if Nt_novo == Nt_curr:
                    if Q_curr < Qt: Nt_curr += 1
                    else: Nt_curr = max(Nt_curr - 1, 1)
                else:
                    Nt_curr = Nt_novo

        L_eq = p_passes * L_tubo
        Re_t = (fluido_i['rho'] * v_tubo_curr * D_tubo) / fluido_i['mu']
        f_t = 64 / Re_t if Re_t < 2100 else 0.316 * (Re_t**-0.25)
        DeltaP_tubo = f_t * (L_eq / D_tubo) * (fluido_i['rho'] * (v_tubo_curr**2) / 2)

        B_esp = 0.25 * D_casco_curr
        Nb = L_tubo / B_esp
        A_s_casco = D_casco_curr * B_esp * ((Pt - D_o) / Pt)
        Gs = mdot_e / A_s_casco
        D_hs = 4 * ((Pt**2) - (math.pi * (D_o**2) / 4)) / (math.pi * D_o)
        Re_s = (D_hs * Gs) / fluido_e['mu']
        f_s = 1 if Re_s < 100 else 0.14 * (Re_s**-0.2)
        DeltaP_casco = f_s * ((Gs**2) / (2 * fluido_e['rho'])) * (D_casco_curr / D_hs) * Nb

        P_tubo = (mdot_i / fluido_i['rho']) * DeltaP_tubo
        P_casco = (mdot_e / fluido_e['rho']) * DeltaP_casco

        validationsList = [
            {
                "nome": "Fator de Correção LMTD (F >= 0.75)",
                "passou": p_F >= 0.75,
                "valor": f"{p_F:.3f}",
                "pontos": 2,
                "impacto": "Assegura eficiência de troca sob fluxo misto"
            },
            {
                "nome": "Turbulência nos Tubos (Re >= 3000)",
                "passou": Re_t >= 3000,
                "valor": f"Re = {round(Re_t)}",
                "pontos": 1,
                "impacto": "Evita regime laminar de baixa troca térmica"
            },
            {
                "nome": "Velocidade nos Tubos (0.6 - 2.5 m/s)",
                "passou": v_min_tubo <= v_tubo_curr <= v_max_tubo,
                "valor": f"{v_tubo_curr:.2f} m/s",
                "pontos": 2,
                "impacto": "Evita deposição (se baixa) e erosão rápida (se alta)"
            },
            {
                "nome": "Velocidade no Casco (0.3 - 1.2 m/s)",
                "passou": 0.3 <= v_casco_curr <= 1.2,
                "valor": f"{v_casco_curr:.2f} m/s",
                "pontos": 2,
                "impacto": "Evita má distribuição ou vibração excessiva dos tubos"
            },
            {
                "nome": "Coeficiente Global U (>= 500 W/m²K)",
                "passou": U_curr >= 500,
                "valor": f"{U_curr:.1f} W/m²K",
                "pontos": 1,
                "impacto": "Denota design térmico compacto e eficiente"
            },
            {
                "nome": "Perda de Carga nos Tubos (<= 50 kPa)",
                "passou": DeltaP_tubo <= 50000,
                "valor": f"{(DeltaP_tubo / 1000):.2f} kPa",
                "pontos": -2 if DeltaP_tubo > 50000 else 0,
                "impacto": "Garante baixas demandas do sistema de bombas"
            }
        ]

        p_score = 0
        for v in validationsList:
            if v["passou"]:
                if v["pontos"] > 0: p_score += v["pontos"]
            else:
                if v["pontos"] < 0: p_score += v["pontos"]

        return {
            "n_passes": p_passes,
            "config": p_config,
            "F": p_F,
            "Nt": Nt_curr,
            "D_casco": D_casco_curr,
            "v_tubo": v_tubo_curr,
            "v_casco": v_casco_curr,
            "h_i": h_i_curr,
            "h_e": h_e_curr,
            "U": U_curr,
            "A": A_curr,
            "Q": Q_curr,
            "Re_t": Re_t,
            "Re_s": Re_s,
            "DeltaP_tubo": DeltaP_tubo,
            "DeltaP_casco": DeltaP_casco,
            "P_tubo": P_tubo,
            "P_casco": P_casco,
            "score": p_score,
            "validations": validationsList,
            "aceitavel": p_score >= 3
        }

    alternativas = [simulaConfig(cfg["n_passes"], cfg["F"], cfg["config"]) for cfg in possiveisConfigs]

    bestIdx = -1
    if chosenPasses is not None:
        bestIdx = next((i for i, alt in enumerate(alternativas) if alt["n_passes"] == chosenPasses), -1)
    
    if bestIdx == -1:
        bestIdx = next((i for i, alt in enumerate(alternativas) if alt["F"] >= 0.75), -1)
        if bestIdx == -1:
            bestIdx = len(alternativas) - 1
    if bestIdx < 0: bestIdx = 0

    active = alternativas[bestIdx]

    def decomposeTime(tempo_meses):
        if tempo_meses <= 0 or math.isnan(tempo_meses) or math.isinf(tempo_meses):
            return {"anos": 0, "meses": 0, "dias": 0}
        total_dias = tempo_meses * 30.4375
        anos = math.floor(total_dias / 365.25)
        dias_restantes_ano = total_dias % 365.25
        meses = math.floor(dias_restantes_ano / 30.4375)
        dias = math.floor(dias_restantes_ano % 30.4375)
        return {"anos": anos, "meses": meses, "dias": dias}

    fouling_tubo = None
    if T_saida_min_tubo is not None and not math.isnan(T_saida_min_tubo):
        Q_limite = mdot_i * fluido_i['cp'] * abs(T_saida_min_tubo - Ti_in)
        if Ti_in > Ti_out:
            Te_out_lim = Te_in + Q_limite / (mdot_e * fluido_e['cp'])
        else:
            Te_out_lim = Te_in - Q_limite / (mdot_e * fluido_e['cp'])
        
        if Te_in > Ti_in:
            Th_in_L, Th_out_L, Tc_in_L, Tc_out_L = Te_in, Te_out_lim, Ti_in, T_saida_min_tubo
        else:
            Th_in_L, Th_out_L, Tc_in_L, Tc_out_L = Ti_in, T_saida_min_tubo, Te_in, Te_out_lim
        LMTD_lim = calcula_LMTD(Th_in_L, Th_out_L, Tc_in_L, Tc_out_L)
        
        U_sujo = abs(Q_limite) / (active['A'] * active['F'] * LMTD_lim)
        R_f_critico = (1 / U_sujo) - (1 / active['U'])
        taxa = calcula_taxa_fouling(fluido_i, active['Re_t'], Tmed_i)
        
        tempo_campanha = R_f_critico / taxa if R_f_critico > 0 else 0

        fouling_tubo = {
            "U_limpo": active['U'],
            "U_sujo": U_sujo,
            "R_f_critico": R_f_critico,
            "taxa": taxa,
            "tempo_campanha_meses": tempo_campanha,
            "decomposicao": decomposeTime(tempo_campanha)
        }

    fouling_casco = None
    if T_saida_limite_casco is not None and not math.isnan(T_saida_limite_casco):
        Q_limite = mdot_e * fluido_e['cp'] * abs(T_saida_limite_casco - Te_in)
        if Te_in > Te_out:
            Ti_out_lim = Ti_in + Q_limite / (mdot_i * fluido_i['cp'])
        else:
            Ti_out_lim = Ti_in - Q_limite / (mdot_i * fluido_i['cp'])
        
        if Te_in > Ti_in:
            Th_in_L, Th_out_L, Tc_in_L, Tc_out_L = Te_in, T_saida_limite_casco, Ti_in, Ti_out_lim
        else:
            Th_in_L, Th_out_L, Tc_in_L, Tc_out_L = Ti_in, Ti_out_lim, Te_in, T_saida_limite_casco
        LMTD_lim = calcula_LMTD(Th_in_L, Th_out_L, Tc_in_L, Tc_out_L)
        
        U_sujo = abs(Q_limite) / (active['A'] * active['F'] * LMTD_lim)
        R_f_critico = (1 / U_sujo) - (1 / active['U'])
        taxa = calcula_taxa_fouling(fluido_e, active['Re_s'], Tmed_e)
        
        tempo_campanha = R_f_critico / taxa if R_f_critico > 0 else 0

        fouling_casco = {
            "U_limpo": active['U'],
            "U_sujo": U_sujo,
            "R_f_critico": R_f_critico,
            "taxa": taxa,
            "tempo_campanha_meses": tempo_campanha,
            "decomposicao": decomposeTime(tempo_campanha)
        }

    return {
        "termico": {
            "Q": Qt,
            "Te_out": Te_out,
            "erro_Q_bal": abs(Qt - Qc)/Qt,
            "LMTD": DTlm,
            "F": active['F'],
            "configuracao": active['config'],
            "n_passes": active['n_passes'],
        },
        "envelope": {
            "U_min": h_i_min,
            "U_proj": active['U'],
            "U_max": active['U'],
            "A_proj": active['A'],
            "Nt_area": active['Nt']
        },
        "it_geo": {
            "Nt": active['Nt'],
            "D_casco": active['D_casco'],
            "v_tubo_real": active['v_tubo'],
            "v_casco_real": active['v_casco'],
            "h_i_real": active['h_i'],
            "h_e_real": active['h_e'],
            "U_real": active['U'],
            "A_real": active['A'],
            "Q_real": active['Q'],
            "erro_Q_real": abs(active['Q'] - Qt) / Qt
        },
        "hidraulico": {
            "Re_t": active['Re_t'],
            "DeltaP_tubo": active['DeltaP_tubo'],
            "DeltaP_casco": active['DeltaP_casco'],
            "P_tubo": active['P_tubo'],
            "P_casco": active['P_casco']
        },
        "status": {
            "score": active['score'],
            "aceitavel": active['aceitavel'],
            "validations": active['validations']
        },
        "alternativas": alternativas,
        "fouling": {
            "tubo": fouling_tubo,
            "casco": fouling_casco
        }
    }

# ----------------- STREAMLIT UI -----------------

st.title("Simulador de Trocador de Calor")
st.markdown("Casco-tubos - Otimização Térmica e Hidráulica")

if "chosen_passes" not in st.session_state:
    st.session_state.chosen_passes = None

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Parâmetros de Projeto")
    with st.form("simulation_form"):
        id_i = st.selectbox("Fluido Interno (Tubos)", options=[f["id"] for f in Fluidos], format_func=lambda x: next(f["nome"] for f in Fluidos if f["id"] == x), index=3)
        id_e = st.selectbox("Fluido Externo (Casco)", options=[f["id"] for f in Fluidos], format_func=lambda x: next(f["nome"] for f in Fluidos if f["id"] == x), index=3)
        
        col1_a, col1_b = st.columns(2)
        mdot_i_kgh = col1_a.number_input("Vazão Tubos (kg/h)", value=50000.0)
        mdot_e_kgh = col1_b.number_input("Vazão Casco (kg/h)", value=60000.0)
        
        col1_c, col1_d = st.columns(2)
        Ti_in = col1_c.number_input("T. Ent Tubo (°C)", value=80.0)
        Ti_out = col1_d.number_input("T. Sai Tubo (°C)", value=40.0)
        
        Te_in = st.number_input("T. Ent Casco (°C)", value=25.0)
        
        st.divider()
        id_mat = st.selectbox("Material do Tubo", options=[m["id"] for m in Materiais], format_func=lambda x: next(m["nome"] for m in Materiais if m["id"] == x), index=0)
        
        col1_e, col1_f = st.columns(2)
        D_tubo_mm = col1_e.number_input("Diâmetro Int (mm)", value=19.05, step=0.01)
        espessura_mm = col1_f.number_input("Espessura (mm)", value=2.11, step=0.01)
        
        col1_g, col1_h = st.columns(2)
        L_tubo = col1_g.number_input("Comprimento (m)", value=6.0, step=0.1)
        arranjo = col1_h.selectbox("Arranjo", options=[1, 2], format_func=lambda x: "Triangular (1)" if x == 1 else "Quadrado (2)")
        
        st.divider()
        usaBellDelaware = st.checkbox("Usar Método Bell-Delaware", value=False)
        if usaBellDelaware:
            b_cols = st.columns(5)
            Jc = b_cols[0].number_input("Jc", value=0.85, step=0.01)
            Jl = b_cols[1].number_input("Jl", value=0.80, step=0.01)
            Jb = b_cols[2].number_input("Jb", value=0.80, step=0.01)
            Js = b_cols[3].number_input("Js", value=0.90, step=0.01)
            Jr = b_cols[4].number_input("Jr", value=0.95, step=0.01)
        else:
            Jc = 0.85; Jl = 0.80; Jb = 0.80; Js = 0.90; Jr = 0.95
            
        st.divider()
        st.markdown("**Limites para Análise de Fouling**")
        col_f1, col_f2 = st.columns(2)
        T_saida_min_tubo = col_f1.number_input("T. Limite Tubo (°C)", value=40.0, step=0.1)
        T_saida_limite_casco = col_f2.number_input("T. Limite Casco (°C)", value=35.0, step=0.1)

        submitted = st.form_submit_button("Simular", type="primary")

if submitted:
    st.session_state.chosen_passes = None

params = {
    "id_i": id_i, "id_e": id_e, "D_tubo_mm": D_tubo_mm, "espessura_mm": espessura_mm,
    "L_tubo": L_tubo, "arranjo": arranjo, "id_mat": id_mat, "mdot_i_kgh": mdot_i_kgh,
    "mdot_e_kgh": mdot_e_kgh, "Ti_in": Ti_in, "Ti_out": Ti_out, "Te_in": Te_in,
    "usaBellDelaware": usaBellDelaware, "Jc": Jc, "Jl": Jl, "Jb": Jb, "Js": Js, "Jr": Jr,
    "T_saida_min_tubo": T_saida_min_tubo, "T_saida_limite_casco": T_saida_limite_casco
}

if submitted or st.session_state.chosen_passes is not None:
    result = runSimulation(params, st.session_state.chosen_passes)
    with col2:
        st.header("Resultados")
        
        r1, r2 = st.columns(2)
        with r1:
            st.subheader("Balanço Térmico")
            st.write(f"**Calor Trocado (Q):** {(result['termico']['Q'] / 1000):.2f} kW")
            st.write(f"**Temp. saída Casco calc.:** {result['termico']['Te_out']:.2f} °C")
            st.write(f"**LMTD:** {result['termico']['LMTD']:.2f} °C")
            st.write(f"**Configuração:** {result['termico']['configuracao']}")
            st.write(f"**Fator de Correção (F):** {result['termico']['F']:.3f}")
        
        with r2:
            st.subheader("Dimensões Finais")
            st.write(f"**Nº de Tubos (Nt):** {result['it_geo']['Nt']}")
            st.write(f"**Diâmetro Casco (Ds):** {(result['it_geo']['D_casco'] * 1000):.1f} mm")
            st.write(f"**Área de Troca (A):** {result['it_geo']['A_real']:.2f} m²")
            st.write(f"**Coef. Global (U):** {result['it_geo']['U_real']:.1f} W/m².K")

        st.divider()
        st.subheader("Estudo de Alternativas")
        
        for alt in result['alternativas']:
            is_active = alt['n_passes'] == result['termico']['n_passes']
            col_a, col_b, col_c = st.columns([3, 1, 1])
            with col_a:
                st.write(f"**{alt['config']}** | Tubos: {alt['Nt']} | Ds: {alt['D_casco']*1000:.1f}mm | Score: {alt['score']}")
            with col_b:
                if is_active:
                    st.success("Ativo")
                else:
                    if st.button("Selecionar", key=f"sel_{alt['n_passes']}"):
                        st.session_state.chosen_passes = alt['n_passes']
                        st.rerun()

        st.divider()
        st.subheader("Avaliação Hidrodinâmica")
        h1, h2 = st.columns(2)
        with h1:
            st.write("**Lado Tubos**")
            st.write(f"Velocidade: {result['it_geo']['v_tubo_real']:.2f} m/s")
            st.write(f"Perda de Carga: {result['hidraulico']['DeltaP_tubo']/1000:.2f} kPa")
        with h2:
            st.write("**Lado Casco**")
            st.write(f"Velocidade: {result['it_geo']['v_casco_real']:.2f} m/s")
            st.write(f"Perda de Carga: {result['hidraulico']['DeltaP_casco']/1000:.2f} kPa")
            
        if result['status']['aceitavel']:
            st.success(f"Score: {result['status']['score']} - Aceitável")
        else:
            st.error(f"Score: {result['status']['score']} - Requer atenção")
            
        for v in result['status']['validations']:
            if v['passou']:
                st.write(f"✅ {v['nome']}: {v['valor']}")
            else:
                st.write(f"❌ {v['nome']}: {v['valor']}")

        st.divider()
        st.subheader("Análise de Fouling")
        f1, f2 = st.columns(2)
        
        def render_fouling(title, data):
            st.write(f"**{title}**")
            if not data:
                st.write("Sem limite")
            else:
                st.write(f"U Limpo: {data['U_limpo']:.1f}")
                if data['U_sujo'] > 0 and not math.isinf(data['U_sujo']):
                    st.write(f"U Sujo Crítico: {data['U_sujo']:.1f}")
                st.write(f"Rf Crítico: {data['R_f_critico']:.2e}" if data['R_f_critico'] > 0 else "S/ Limite")
                st.write(f"Taxa Depos: {data['taxa']:.2e}")
                st.write(f"Campanha: {data['tempo_campanha_meses']:.1f} meses")
                
        with f1:
            render_fouling("Lado Tubo", result['fouling']['tubo'])
        with f2:
            render_fouling("Lado Casco", result['fouling']['casco'])
else:
    with col2:
        st.info("Insira os parâmetros e clique em Simular para gerar o projeto otimizado.")
