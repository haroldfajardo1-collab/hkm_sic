# app_v2.py - Panel de Control Universal del SIC

import streamlit as st
import pandas as pd
import config_v2 as cfg

st.set_page_config(
    page_title="SIC • HKM Technology Solutions",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONTROL DE ACCESO SEGURO ---
def verificar_acceso():
    if st.session_state.get("autenticado", False):
        return True
    
    st.title("🔒 Acceso Restringido • SIC HKM")
    clave = st.text_input("Ingresa tu clave de acceso:", type="password")
    if st.button("Ingresar", type="primary"):
        clave_correcta = st.secrets.get("APP_PASSWORD", "HKM2026")
        if clave == clave_correcta:
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("❌ Clave incorrecta.")
    return False

if not verificar_acceso():
    st.stop()
# --------------------------------

st.title("⚡ SIC • HKM Technology Solutions")
st.caption("Sistema Integral de Comercialización • Evaluador Universal de Oportunidades v2.0")

# PARÁMETROS EN BARRA LATERAL (Ajustables en vivo)
st.sidebar.header("⚙️ Parámetros Globales")
trm_actual = st.sidebar.number_input("TRM (COP / USD):", value=cfg.TRM_DEFAULT, step=50.0)
flete_aereo_fba = st.sidebar.number_input("Flete Aéreo a FBA (USD/kg):", value=cfg.FLETE_AEREO_DDP_FBA_KG, step=0.5)
flete_aereo_cali = st.sidebar.number_input("Flete Aéreo a Cali (USD/kg):", value=cfg.FLETE_AEREO_CALI_KG, step=1.0)

tab_evaluador, tab_criterios = st.tabs(["🛠️ Evaluador de Oportunidad", "📋 Criterios Operativos"])

with tab_evaluador:
    st.subheader("1. Ficha del Producto / Kit Integral")
    
    col_n, col_m = st.columns([2, 1])
    with col_n:
        prod_nombre = st.text_input("Nombre de la Oferta / Referencia:", placeholder="Ej: Dispositivo Inteligente con Kit de Accesorios")
    with col_m:
        mercado_target = st.selectbox("Mercado de Análisis:", ["Amazon EE. UU. (FBA)", "Colombia (B2C / Local)"])

    st.markdown("##### Estructura de Costos del Producto y Accesorios")
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.markdown("**1. Dispositivo / Módulo Principal**")
    with c2:
        fob_base = st.number_input("Costo FOB Base ($ USD):", value=12.00, step=0.5)
    with c3:
        peso_base = st.number_input("Peso Base (g):", value=200, step=10)

    # Accesorio opcional
    tiene_accesorio = st.checkbox("¿Incluye Accesorio Crítico o Fuente de Poder (Kit/Bundle)?", value=True)
    fob_acc = 0.0
    peso_acc = 0
    if tiene_accesorio:
        c4, c5, c6 = st.columns([2, 1, 1])
        with c4:
            st.caption("Accesorio complementario / Cargador / Repuestos")
        with c5:
            fob_acc = st.number_input("Costo FOB Accesorio ($ USD):", value=3.00, step=0.2)
        with c6:
            peso_acc = st.number_input("Peso Accesorio (g):", value=80, step=5)

    # Empaque
    c7, c8, c9 = st.columns([2, 1, 1])
    with c7:
        st.caption("Empaque Primario / Caja Retail / Manual")
    with c8:
        fob_emp = st.number_input("Costo FOB Empaque ($ USD):", value=0.80, step=0.1)
    with c9:
        peso_emp = st.number_input("Peso Empaque (g):", value=60, step=5)

    # Totales del Kit
    fob_total = fob_base + fob_acc + fob_emp
    peso_total_g = peso_base + peso_acc + peso_emp
    peso_total_kg = peso_total_g / 1000.0

    st.info(f"📦 **Totales:** Costo FOB Total: **${fob_total:.2f} USD** | Peso Bruto Total: **{peso_total_g} g** ({peso_total_kg:.3f} kg)")

    st.markdown("---")
    st.subheader("2. Proyección Comercial y de Pauta")
    
    col_pvp, col_ads = st.columns(2)
    if mercado_target == "Amazon EE. UU. (FBA)":
        with col_pvp:
            pvp_amz = st.number_input("PVP Objetivo en Amazon ($ USD):", value=59.99, step=1.0)
        with col_ads:
            acos_est = st.slider("% Publicidad Amazon PPC (ACOS):", 5.0, 35.0, cfg.ACOS_OBJETIVO_AMAZON)
    else:
        with col_pvp:
            pvp_col = st.number_input("PVP Objetivo en Colombia ($ COP):", value=149900.0, step=1000.0)
        with col_ads:
            cpa_col = st.number_input("CPA Estimado Pauta Meta/TikTok ($ COP):", value=cfg.CPA_OBJETIVO_COLOMBIA_COP, step=1000.0)

    st.markdown("---")
    st.subheader("3. Banderas de Riesgo y Auditoría")
    
    r_comp = st.checkbox("Competidor dominante presente en el rango medio de precio.")
    r_falla = st.checkbox("Historial de fallas críticas en reseñas de 1 estrella de competidores.")
    r_salud = st.checkbox("Producto involucra bienestar corporal, descanso o salud (Riesgo FDA / INVIMA).")
    r_elec = st.checkbox("Producto se conecta a la red eléctrica de 110V (Riesgo RETIE / UL).")

    if st.button("🚀 EJECUTAR AUDITORÍA FINANCIERA Y OPERATIVA", type="primary"):
        st.markdown("---")
        
        if mercado_target == "Amazon EE. UU. (FBA)":
            flete_int = peso_total_kg * flete_aereo_fba
            comision_amz = pvp_amz * cfg.AMAZON_REFERRAL_RATE
            fee_fba = cfg.calcular_fba_fulfillment_fee(peso_total_g)
            fee_inbound = cfg.FBA_INBOUND_PLACEMENT_FEE
            costo_ppc = pvp_amz * (acos_est / 100.0)
            
            costo_total = fob_total + flete_int + comision_amz + fee_fba + fee_inbound + costo_ppc
            neto_usd = pvp_amz - costo_total
            margen_pct = (neto_usd / pvp_amz) * 100.0
            roi_pct = (neto_usd / (fob_total + flete_int)) * 100.0

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("PVP Amazon", f"${pvp_amz:.2f} USD")
            m2.metric("Costo Total FBA", f"${costo_total:.2f} USD")
            m3.metric("Utilidad Neta", f"${neto_usd:.2f} USD")
            m4.metric("Margen Neto", f"{margen_pct:.1f}%")

            if margen_pct >= cfg.MARGEN_NETO_MINIMO_AMAZON:
                st.success(f"🟢 **PRODUCTO VIABLE (ROI Inventario: {roi_pct:.1f}%)**")
            elif margen_pct >= 15.0:
                st.warning(f"🟡 **VIABILIDAD CONDICIONADA (Margen: {margen_pct:.1f}%)** - Optimizar flete o PPC.")
            else:
                st.error(f"🔴 **MARGEN INSUFICIENTE ({margen_pct:.1f}%)** - No absorbe comisiones.")

            df_res = pd.DataFrame({
                "Rubro": ["FOB Kit", "Flete Aéreo DDP", "Comisión Amazon (15%)", "FBA Pick & Pack", "Inbound Placement", "Publicidad PPC", "TOTAL COSTO", "UTILIDAD NETA"],
                "USD": [f"${fob_total:.2f}", f"${flete_int:.2f}", f"${comision_amz:.2f}", f"${fee_fba:.2f}", f"${fee_inbound:.2f}", f"${costo_ppc:.2f}", f"${costo_total:.2f}", f"${neto_usd:.2f}"]
            })
            st.table(df_res)

        else:
            fob_cop = fob_total * trm_actual
            flete_int_cop = (peso_total_kg * flete_aereo_cali) * trm_actual
            arancel_iva_cop = (fob_cop + flete_int_cop) * 0.29
            landed_cali = fob_cop + flete_int_cop + arancel_iva_cop
            costo_total_col = landed_cali + cpa_col + cfg.FLETE_LOCAL_COLOMBIA_COP
            neto_cop = pvp_col - costo_total_col
            margen_col_pct = (neto_cop / pvp_col) * 100.0

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("PVP Colombia", f"${pvp_col:,.0f} COP")
            m2.metric("Landed Cost Cali", f"${landed_cali:,.0f} COP")
            m3.metric("Utilidad Neta", f"${neto_cop:,.0f} COP")
            m4.metric("Margen Neto", f"{margen_col_pct:.1f}%")

            if margen_col_pct >= cfg.MARGEN_NETO_MINIMO_COLOMBIA:
                st.success(f"🟢 **VIABLE EN COLOMBIA (Margen: {margen_col_pct:.1f}%)**")
            else:
                st.error(f"🔴 **RIESGO FINANCIERO ({margen_col_pct:.1f}%)** - Costo operativo supera el mercado.")

        st.subheader("🛡️ Matriz de Mitigación Requerida")
        alertas = []
        if r_comp: alertas.append(cfg.CATALOGO_MITIGACIONES["competencia_dominante"])
        if r_falla: alertas.append(cfg.CATALOGO_MITIGACIONES["desempeno_critico"])
        if r_salud: alertas.append(cfg.CATALOGO_MITIGACIONES["regulacion_salud"])
        if r_elec: alertas.append(cfg.CATALOGO_MITIGACIONES["regulacion_electrica"])

        if alertas:
            for item in alertas:
                with st.expander(f"⚠️ {item['alerta']}", expanded=True):
                    st.write(item["mitigacion"])
        else:
            st.success("No se activaron banderas de riesgo operativas.")

with tab_criterios:
    st.markdown("""
    ### Principios Rectores del SIC (HKM Technology Solutions)
    1. **Modelo Universal:** No nos casamos con ningún producto; evaluamos la asimetría matemática del mercado.
    2. **Anti-Parálisis:** Las dificultades no implican descartar, sino estructurar la **estrategia de mitigación** adecuada.
    3. **Enfoque FBA:** Priorizar productos con márgenes netos en dólares superiores al 25% tras todos los costos fijos.
    """)
