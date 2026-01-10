import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
import glob
import time
import random

# ==========================================================
# 🛡️ SENTINEL AI - FINAL COMMAND CENTER (REPLAY EDITION)
# ==========================================================
st.set_page_config(page_title="Sentinel AI - Command Center", page_icon="🛡️", layout="wide")

# --- CALLBACKS DE NAVEGACIÓN BLINDADOS ---
def nav_to_dashboard():
    st.session_state.menu_option = "Dashboard General"

def nav_to_forensics():
    st.session_state.menu_option = "Historial de Evidencias"

# --- INICIALIZACIÓN DE ESTADOS ---
if 'menu_option' not in st.session_state:
    st.session_state.menu_option = "Dashboard General"

if 'fraud_data' not in st.session_state:
    st.session_state.fraud_data = pd.DataFrame({
        'Tiempo': [datetime.now() - timedelta(seconds=i) for i in range(30, 0, -1)],
        'Tráfico Normal': np.random.randint(100, 150, size=30),
        'Riesgo Detectado': np.random.randint(0, 5, size=30)
    })
    st.session_state.last_update = time.time()

def load_captures():
    files = glob.glob("data/captures/*.jpg")
    # Ordenar por fecha de modificación (más reciente primero)
    files.sort(key=os.path.getmtime, reverse=True)
    return files

# --- NUEVA FUNCIÓN: SIMULADOR BASADO EN HISTORIAL ---
def simulate_physical_replay():
    """
    Toma una imagen real existente y la re-inyecta como un nuevo evento simulado.
    """
    input_dir = "data/captures"
    os.makedirs(input_dir, exist_ok=True)
    
    # 1. Buscar imágenes existentes
    existing_files = glob.glob(f"{input_dir}/*.jpg")
    # Filtramos para no re-usar imágenes que ya son simulacros si es posible
    real_captures = [f for f in existing_files if "SIM_" not in f]
    pool_to_choose_from = real_captures if real_captures else existing_files

    timestamp_str = datetime.now().strftime("%H:%M:%S")
    new_filename = f"{input_dir}/SIM_REPLAY_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

    if pool_to_choose_from:
        # CASO A: Usar una imagen real existente
        source_file = random.choice(pool_to_choose_from)
        try:
            img = Image.open(source_file).convert("RGB")
            d = ImageDraw.Draw(img)
            
            # Agregar un banner rojo en la parte superior para indicar simulacro
            d.rectangle([0, 0, 800, 40], fill=(220, 0, 0))
            # Texto del banner con la nueva hora
            header_text = f"📢 SIMULATION REPLAY EVENT | LIVE TIME: {timestamp_str}"
            d.text((10, 12), header_text, fill=(255, 255, 255))
            
            img.save(new_filename)
        except Exception as e:
            st.error(f"Error procesando imagen: {e}")
            return None
    else:
        # CASO B: Fallback si la carpeta está vacía (Patrón de prueba limpio)
        img = Image.new('RGB', (800, 600), color=(30, 30, 30))
        d = ImageDraw.Draw(img)
        d.rectangle([50, 50, 750, 550], outline=(255, 0, 0), width=5)
        d.line([(50, 50), (750, 550)], fill=(255, 0, 0), width=2)
        d.line([(750, 50), (50, 550)], fill=(255, 0, 0), width=2)
        d.text((300, 280), "NO HISTORICAL DATA AVAILABLE", fill=(255, 0, 0))
        d.text((280, 310), f"TEST PATTERN GENERATED AT {timestamp_str}", fill=(0, 255, 0))
        img.save(new_filename)

    return new_filename

# ==========================================================
# 📊 SIDEBAR - CHAOS ENGINEERING (BOTONES ROJOS)
# ==========================================================
st.sidebar.title("🛡️ Sentinel AI")
st.sidebar.markdown("---")
st.sidebar.subheader("🕹️ Chaos Engineering")

# Botón Físico (Usa la nueva función de Replay)
if st.sidebar.button("🚨 SIMULAR INTRUSIÓN FÍSICA", type="primary", use_container_width=True):
    simulate_physical_replay()
    st.toast("ALERTA: Replay de evento físico inyectado", icon="🔄")

# Botón Digital
if st.sidebar.button("🚨 SIMULAR ATAQUE DIGITAL", type="primary", use_container_width=True):
    new_entry = {'Tiempo': datetime.now(), 'Tráfico Normal': 250, 'Riesgo Detectado': 140}
    st.session_state.fraud_data = pd.concat([st.session_state.fraud_data, pd.DataFrame([new_entry])], ignore_index=True)
    st.toast("ALERTA: Pico de riesgo digital inyectado", icon="💳")

st.sidebar.markdown("---")
# Navegación sincronizada
st.session_state.menu_option = st.sidebar.radio(
    "Navegación:", ["Dashboard General", "Historial de Evidencias"],
    index=0 if st.session_state.menu_option == "Dashboard General" else 1
)

# ==========================================================
# 🏠 VISTA: DASHBOARD GENERAL
# ==========================================================
if st.session_state.menu_option == "Dashboard General":
    st.title("🛰️ Centro de Control Proactivo 360°")
    captures = load_captures()
    
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Intrusiones Físicas", len(captures))
    c2.metric("Riesgo Digital (Live)", f"{st.session_state.fraud_data['Riesgo Detectado'].iloc[-1]} pts")
    c3.metric("Salud del Modelo", "99.2%", "Senior Grade")
    c4.metric("Capital Protegido", f"${13950 + (len(captures)*500)}")

    st.markdown("---")
    st.subheader("💳 Monitoreo Digital (Pulso en Tiempo Real)")
    st.line_chart(st.session_state.fraud_data.tail(50).set_index('Tiempo'), color=["#00ff00", "#ff0000"], height=350)

    st.markdown("---")
    col_metrics, col_phys = st.columns([2, 1])

    with col_metrics:
        st.subheader("🧠 Inteligencia de Datos")
        m1, m2, m3 = st.columns(3); m1.metric("Precisión", "0.97"); m2.metric("Recall", "0.99"); m3.metric("F1-Score", "0.98")
        st.table(pd.DataFrame({"Evento": ["REPLAY_ATTACK", "FRAUD_SPIKE"], "Severidad": ["ALTA", "CRÍTICA"], "Status": ["MITIGADO", "BLOQUEADO"]}))

    with col_phys:
        st.subheader("📹 Seguridad Física")
        st.info(f"Sistemas activos. {len(captures)} eventos registrados.")
        # BOTÓN CON CALLBACK (Navegación segura)
        st.button("📂 ABRIR ARCHIVO FORENSE", use_container_width=True, type="primary", on_click=nav_to_forensics)

    # MOTOR DE REFRESCO (Al final, sin errores)
    time.sleep(1)
    new_row = {'Tiempo': datetime.now(), 'Tráfico Normal': np.random.randint(100, 150), 'Riesgo Detectado': np.random.randint(0, 8)}
    st.session_state.fraud_data = pd.concat([st.session_state.fraud_data, pd.DataFrame([new_row])], ignore_index=True).tail(50)
    st.rerun()

# ==========================================================
# 📁 VISTA: HISTORIAL DE EVIDENCIAS
# ==========================================================
elif st.session_state.menu_option == "Historial de Evidencias":
    # BOTÓN CON CALLBACK
    st.button("⬅️ Volver al Dashboard", on_click=nav_to_dashboard)

    st.title("📂 Archivo Forense")
    captures = load_captures()
    if captures:
        # Selector con nombre limpio
        selected = st.selectbox("Evento:", captures, format_func=lambda x: os.path.basename(x))
        st.image(Image.open(selected), use_container_width=True)
    else:
        st.info("No hay registros en el archivo. Ejecute la cámara o un simulacro.")