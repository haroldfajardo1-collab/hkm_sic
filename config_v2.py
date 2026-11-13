# config_v2.py - SIC HKM Technology Solutions
# Parámetros Operativos y Matriz de Riesgo Universal

# 1. LOGÍSTICA Y MACROECONOMÍA
TRM_DEFAULT = 4200.0                   # Tasa de cambio COP/USD
FLETE_AEREO_DDP_FBA_KG = 9.0            # USD/Kg (China -> Amazon FBA directo)
FLETE_MARITIMO_DDP_FBA_KG = 2.8         # USD/Kg (Carga masiva futura)
FLETE_AEREO_CALI_KG = 20.0              # USD/Kg (China -> Cali DDP)
FLETE_LOCAL_COLOMBIA_COP = 16000.0      # Última milla Servientrega/Coordinadora

# 2. TARIFAS AMAZON FBA (EE. UU.)
AMAZON_REFERRAL_RATE = 0.15             # 15% comisión estándar
FBA_INBOUND_PLACEMENT_FEE = 0.35        # Tarifa de colocación por unidad

def calcular_fba_fulfillment_fee(peso_gramos):
    """Calcula tarifa Pick & Pack FBA según peso estándar."""
    if peso_gramos <= 226:              # < 8 oz
        return 3.45
    elif peso_gramos <= 453:            # 8 oz a 1 lb
        return 4.15
    elif peso_gramos <= 907:            # 1 lb a 2 lb
        return 5.40
    else:                               # > 2 lb
        libras_extra = ((peso_gramos - 907) / 453.59)
        return 6.10 + (libras_extra * 0.40)

# 3. OBJETIVOS COMERCIALES MÍNIMOS
MARGEN_NETO_MINIMO_AMAZON = 25.0        # % utilidad neta mínima en USA
MARGEN_NETO_MINIMO_COLOMBIA = 20.0      # % utilidad neta mínima en Colombia
ACOS_OBJETIVO_AMAZON = 16.0             # % PPC sobre PVP
CPA_OBJETIVO_COLOMBIA_COP = 25000.0     # CPA estimado pauta local

# 4. CATÁLOGO UNIVERSAL DE MITIGACIÓN (ANTI-PARÁLISIS)
CATALOGO_MITIGACIONES = {
    "competencia_dominante": {
        "alerta": "Presencia de marca dominante o Amazon Basics en el segmento medio.",
        "mitigacion": "No competir por precio bajo. Posicionar en segmento Prémium con mejores materiales, kit con valor agregado (Bundle) y empaque superior."
    },
    "ancla_precio_baja": {
        "alerta": "El mercado de destino tiene precios de referencia bajos por copias genéricas.",
        "mitigacion": "Vender solución completa (kit) y destacar garantía local directa para derribar desconfianza."
    },
    "desempeno_critico": {
        "alerta": "Riesgo de quejas en reseñas por fallas mecánicas, térmicas o de batería.",
        "mitigacion": "Exigir componentes de grado industrial a fábrica (chips IC independientes, celdas grado A) e inspección AQL 2.5 en origen."
    },
    "accesorio_ausente": {
        "alerta": "El producto requiere periféricos para funcionar al 100% (fuente de poder, consumibles).",
        "mitigacion": "Incluir el accesorio en el kit de fábrica o advertir de forma explícita en títulos y manuales para evitar reclamos."
    },
    "regulacion_salud": {
        "alerta": "El producto involucra promesas de bienestar, sueño o salud (Riesgo FDA / INVIMA).",
        "mitigacion": "Prohibir claims médicos (no usar palabras como 'cure', 'treatment'). Etiquetar estrictamente como 'Dispositivo de Confort / Asistencia para el Bienestar'."
    },
    "regulacion_electrica": {
        "alerta": "El producto se conecta a la red eléctrica de 110V (Riesgo RETIE / UL).",
        "mitigacion": "Para Colombia: ingresar sólo en corriente continua USB-C (exento de RETIE). Para EE. UU.: exigir reportes vigentes UL/ETL y FCC de fábrica."
    }
}
