# 🛡️ Sentinel AI

**Sentinel AI es una pieza de portafolio / demostración técnica que reúne tres módulos independientes de "seguridad con IA" bajo un mismo dashboard.** Muestra, en un solo proyecto, capacidad en visión por computadora, machine learning para detección de fraude y construcción de interfaces de monitoreo.

> ⚠️ **Importante (honestidad técnica):** es un **showcase**, no un producto en producción. Los tres módulos funcionan por separado pero **no están conectados entre sí**, y parte del dashboard usa datos simulados. Ver la sección [Qué es real y qué es demo](#-qué-es-real-y-qué-es-demo) antes de evaluarlo.

## Los tres módulos

### 1. Vision Sentinel (el más sólido)
Detector de intrusión perimetral con **YOLOv8**: vigila un stream de webcam o RTSP, define una **zona prohibida poligonal** y, cuando una persona entra en ella (se evalúa el punto de los pies con `cv2.pointPolygonTest`), guarda una captura de evidencia en `data/captures/` con un *cooldown* de 3 segundos para no saturar el disco. Código funcional y coherente.
→ `src/vision/detector.py`

### 2. Anti-Fraud Engine
Clasificador de fraude con **Random Forest + SMOTE** (para balancear la clase minoritaria). Entrena, predice y reporta métricas correctamente, pero **solo sobre datos sintéticos** generados con `make_classification` (~1% de fraude). No ingiere transacciones reales.
→ `src/fraud/engine.py` · demo en `notebooks/test_fraud_engine.py`

### 3. Command Center (dashboard Streamlit)
Interfaz de monitoreo que muestra el feed de visión, un historial de evidencias y un "Replay Forense" que re-inyecta imágenes reales del historial. Incluye una simulación de ataque que agrega filas a una tabla en sesión.
→ `src/api/app.py` (es una app **Streamlit**, no una API HTTP)

## 🛠️ Tech Stack (real)

- **Python 3.10+**
- **Visión:** Ultralytics YOLOv8 (`yolov8n.pt`), OpenCV, NumPy. PyTorch llega de forma transitiva vía `ultralytics` (no está pinned en `requirements.txt`).
- **Fraude / ML:** scikit-learn (RandomForestClassifier), imbalanced-learn (SMOTE), pandas.
- **Frontend:** Streamlit + Pillow.
- **Persistencia:** ninguna base de datos; la evidencia son archivos `.jpg` en `data/captures/`.

## ▶️ Uso

```bash
pip install -r requirements.txt

# Dashboard
streamlit run src/api/app.py

# Demo del motor de fraude (entrena sobre datos sintéticos)
python notebooks/test_fraud_engine.py
```

## 🔍 Qué es real y qué es demo

**Real / funcional:**
- Detección de intrusión en ROI poligonal y guardado de evidencia (`VisionSentinel`).
- Entrenamiento y métricas del `FraudDetector` (sobre datos sintéticos).
- El "Replay Forense" re-inyecta imágenes reales del historial.

**Simulado / cosmético (no calculado en vivo):**
- El gráfico de "pulso transaccional en tiempo real" se alimenta de `np.random`, no del motor de fraude.
- Las métricas del dashboard ("Salud del Modelo 99.2%", "Precisión 0.97", "Recall 0.99", "F1 0.98") son **literales hardcodeados**.
- "Capital Protegido" es una fórmula fija (`$13950 + nº_capturas × 500`), no un cálculo basado en eventos reales.
- El refresco "asíncrono" es en realidad síncrono (`time.sleep(1)` + `st.rerun()`).
- El motor de fraude **no se importa** en el dashboard: las dos piezas están desconectadas.

## 🧩 Arquitectura (ideas reutilizables)

- Separación modular limpia por dominio: `src/vision`, `src/fraud`, `src/api`.
- `FraudDetector` bien encapsulado (estado `is_trained`, reutiliza el modelo y el SMOTE, logging en el core).
- Patrón de evidencia con *cooldown* temporal (`save_evidence`) para no saturar disco.
- ROI por polígono usando el punto base del bounding box (los pies del intruso) — buena decisión geométrica para detección perimetral.

> ⚠️ `src/vision/detector.py` aplica un monkeypatch global `torch.load = partial(torch.load, weights_only=False)`, que desactiva la protección de PyTorch 2.6+. Funciona para cargar YOLO, pero es un riesgo si alguna vez se cargaran pesos no confiables.

## 📌 Cómo continuar

1. **Conectar las piezas:** alimentar el dashboard con métricas reales del `FraudDetector` y eventos reales del `VisionSentinel` en lugar de datos `np.random` y literales.
2. **Datos reales de fraude:** reemplazar `make_classification` por un dataset real (o al menos uno público realista).
3. **Pinnear dependencias:** declarar `torch` explícitamente y quitar el monkeypatch usando pesos confiables.
4. **Tests reales:** `notebooks/test_fraud_engine.py` es un script de demo, no pruebas unitarias.

## Licencia

Proyecto de portafolio — **Félix Lezama**.
