# Changelog
RESUMEN

🔹 Fase 1: Inteligencia de Datos y Anti-Fraude (v0.1.0 - v0.3.2)
    -Fundación: Estructura modular senior y entorno de desarrollo profesional.
    -Motor Anti-Fraude: Implementación de Random Forest con balanceo de datos mediante SMOTE, logrando un Recall del 99% en entornos desbalanceados.

🔹 Fase 2: Visión Artificial y Seguridad Perimetral (v0.4.0 - v0.7.0)
    -Core de Visión: Integración de YOLOv8 para detección de intrusos vía RTSP/Webcam.
    -Geometría Avanzada: Detección en Zonas de Interés (ROI) no lineales (polígonos complejos y paramétricos).
    -Evidencia Forense: Sistema de capturas automáticas con lógica de enfriamiento para optimización de recursos.

🔹 Fase 3: Command Center y Experiencia de Usuario (v1.0.0 - v1.8.0)
    -Dashboard 360°: Interfaz de observabilidad en tiempo real con Streamlit, unificando métricas físicas y digitales.
    -Optimización Live-Ops: Gráficas de pulso transaccional con refresco de 1s y navegación interna blindada mediante callbacks.

🔹 Fase 4: Resiliencia y Chaos Engineering (v2.0.0 - v2.1.0)
    -Simulacro de Estrés: Implementación de disparadores de ataque (Físico/Digital) para validación de respuesta de sistemas.
    -Replay Forense: Tecnología de re-inyección de evidencias reales con metadatos dinámicos para auditorías.



## [0.1.0] - 2024-05-22
### Añadido
- Creación del entorno virtual de desarrollo (venv).
- Inicialización de la estructura modular del proyecto (`src/`, `tests/`, `docs/`).
- Archivos base de documentación: README y CHANGELOG.

## [0.2.0] - 2024-05-22
### Añadido
- Módulo `src/fraud/engine.py` con la clase `FraudDetector`.
- Implementación de técnica SMOTE para balanceo de datos.
- Sistema de logging para monitoreo de entrenamiento.

## [0.3.0] - 2024-05-22
### Añadido
- Script de validación `notebooks/test_fraud_engine.py`.
- Generación de datasets sintéticos desbalanceados para pruebas de estrés.
- Comparativa de métricas Precision/Recall para demostrar efectividad de SMOTE.


## [0.3.1] - 2024-05-22
### Corregido
- Error de ruta de archivo (No such file or directory) mediante la creación manual de la estructura de directorios en Windows PowerShell.
- Verificación de la integridad de la carpeta `notebooks/`.

## [0.3.2] - 2024-05-22
### Organizado
- Refactorización de la estructura de pruebas: se prioriza `notebooks/` para demostraciones de métricas y se limpia `tests/` para futuras pruebas unitarias.
- Sincronización de archivos guardados para asegurar la ejecución del intérprete.

## [0.4.0] - 2024-05-22
### Añadido
- Módulo `src/vision/detector.py` para detección de personas.
- Integración con YOLOv8 (Ultralytics) para análisis de video.
- Funcionalidad de prueba en vivo via Webcam.

## [0.5.0] - 2024-05-22
### Añadido
- Soporte para flujos de video RTSP (Cámaras IP/Hikvision).
- Lógica de Zona de Interés (ROI) mediante polígonos.
- Sistema de alertas visuales para intrusiones detectadas dentro del ROI.

## [0.5.1] - 2026-01-09
### Añadido
- Implementación del punto de entrada (`__main__`) en el módulo de visión.
- Configuración de parámetros RTSP para despliegue inmediato con hardware Hikvision.

## [0.5.2] - 2026-01-09
### Corregido
- Error de sintaxis `IndentationError` en el punto de entrada del módulo de visión.
- Alineación de bloques lógicos según el estándar PEP 8.

## [0.5.3] - 2026-01-09
### Corregido
- NameError: reestructuración de la jerarquía de archivos para asegurar que la clase VisionSentinel esté definida antes de su instanciación.
- Verificación de márgenes de ejecución según PEP 8.

## [0.5.4] - 2026-01-09
### Corregido
- WeightsUnpickler Error: Se implementó `add_safe_globals` para compatibilidad con políticas de seguridad de PyTorch 2.6+.
### Añadido
- Selector dinámico de fuente (Webcam/RTSP) para facilitar pruebas rápidas.

## [0.5.5] - 2026-01-09
### Corregido
- WeightsUnpickler (Sequential): Ampliación de la lista de globales seguros para incluir capas estructurales de PyTorch (Conv2d, SiLU, Sequential).
- Estabilización del proceso de deserialización para modelos YOLOv8.

## [0.5.6] - 2026-01-09
### Corregido
- WeightsUnpickler (Conv/Concat/C2f): Se implementó una Whitelist Maestra de componentes de Ultralytics y PyTorch para cumplir con los estándares de seguridad de 2026.
- Estabilización del núcleo de inferencia para despliegues en entornos con políticas de ejecución restrictivas.

## [0.5.7] - 2026-01-09
### Corregido
- WeightsUnpickler Master Fix: Se implementó la importación explícita de submódulos de Ultralytics para satisfacer la validación de tipos de PyTorch 2.6.
- Estabilización del núcleo de carga para evitar errores secuenciales de deserialización.

## [0.5.8] - 2026-01-09
### Corregido
- WeightsUnpickler (Critical Fix): Implementación de una Whitelist exhaustiva para PyTorch 2.6 que cubre toda la arquitectura de capas de Ultralytics.
- Estabilización del arranque del motor de visión bajo políticas Zero-Trust.

## [0.5.9] - 2026-01-09
### Corregido
- WeightsUnpickler Critical Failure: Implementación de monkeypatching en `torch.load` para forzar la carga de modelos YOLOv8 bajo PyTorch 2.6.
- Se eliminó la dependencia de whitelisting manual por ser ineficiente ante arquitecturas de red complejas.

## [0.5.10] - 2026-01-09
### Añadido
- Prueba de concepto de ROI (Region of Interest) no lineal.
- Implementación de zona de detección con forma de corazón mediante ecuaciones paramétricas.
- Validación de la robustez del algoritmo `pointPolygonTest` ante polígonos cóncavos.

## [0.6.0] - 2026-01-10
### Añadido
- Módulo de Evidencia Digital con guardado automático en formato JPG.
- Lógica de Cooldown (3s) para optimización de almacenamiento.
- Gestión automática de directorios de captura en `data/captures/`.

## [0.7.0] - 2026-01-10
### Concluido
- Finalización del MVP (Producto Mínimo Viable) del Módulo de Visión.
- Integración exitosa de captura de evidencia con motor de detección YOLOv8.
- Preparación de entorno para pruebas de campo y demostración técnica.

## [1.0.0] - 2026-01-10
### Añadido
- Lanzamiento de Sentinel AI Command Center (Dashboard Web).
- Interfaz de observabilidad en tiempo real con Streamlit.
- Sistema de visualización de evidencias y KPIs de negocio.
- Integración visual de métricas de IA y Anti-Fraude.

## [1.1.0] - 2026-01-10
### Corregido
- Error de compatibilidad `TypeError` en `st.image` mediante el uso de `use_column_width`.
### Añadido
- Sistema de navegación interactiva entre Dashboard y Evidencias.
- Layout de inspección detallada en el historial de capturas.
- Gestión de estado de sesión para experiencia de usuario mejorada.

## [1.2.0] - 2026-01-10
### Rediseñado
- Dashboard General transformado en un Centro de Mando 360°.
- Integración de métricas digitales (Fraude) y físicas (Cámaras) en la vista principal.
### Añadido
- Gráfico de actividad transaccional en tiempo real en la página de inicio.
- Navegación bidireccional desde el Dashboard hacia módulos de detalle.

## [1.3.0] - 2026-01-10
### Corregido
- UX/UI: Se eliminó la rotación de etiquetas en gráficas mediante la categorización explícita de datos.
### Añadido
- Módulo de "Log de Anomalías" para desglosar métricas agregadas.
- Etiquetas descriptivas de tipos de fraude (Fuerza Bruta, GPS, Montos).
- Mejora en la visualización de KPIs de negocio.

## [1.4.0] - 2026-01-10
### Añadido
- UX: Botón "Volver al Dashboard" en las vistas de detalle (Evidencias y Fraude).
- Navegación mejorada mediante la persistencia del estado de sesión.
### Corregido
- Flujo de usuario: Eliminación de "callejones sin salida" en la interfaz de usuario.

## [1.5.0] - 2026-01-10
### Añadido
- Módulo de "Chaos Engineering": Botón de simulación de ataque en la barra lateral.
- Generador automático de evidencias sintéticas para pruebas de estrés de UI.
- Notificaciones en tiempo real (Toasts) ante eventos de seguridad detectados.


## [1.7.0] - 2026-01-10
### Corregido
- Depreciación de UI: Migración de `use_column_width` a `use_container_width` (Adiós nota verde).
### Rediseñado
- Dashboard Ejecutivo: Simplificación de la sección física para priorizar KPIs digitales y gráficos de pulso.
- Navegación: Centralización del acceso a evidencias mediante botón de acción directa.

## [1.8.0] - 2026-01-10
### Corregido
- UX: Reparación del flujo de navegación entre Dashboard y Archivo Forense.
- Estabilidad: Implementación de Session State Sync para evitar bucles de refresco infinito.
### Añadido
- Identificadores únicos (Keys) para todos los elementos interactivos de la interfaz.

## [2.0.0] - 2026-01-10
### Concluido
- Lanzamiento de Sentinel AI v2.0: Ecosistema Unificado de Seguridad.
- Optimización de UX: Navegación instantánea mediante el desacoplamiento del motor de refresco.
- Integración Estratégica: Consolidación de métricas de Inteligencia de Datos en el panel principal.
- Refactorización de Código: Eliminación de warnings de depreciación y mejora de la estabilidad de sesión.

## [2.1.0] - 2026-01-10
### Añadido
- **Simulador de Replay:** Nueva lógica que utiliza capturas reales del historial para simular ataques físicos, añadiendo banners de metadatos en tiempo real.
- **Doble Trigger de Caos:** Botones independientes para simulación física (Cámaras) y digital (Fraude) con estilos visuales diferenciados.
- **Navegación Blindada:** Implementación de *callbacks* en Streamlit para garantizar que el cambio de página sea instantáneo a pesar del refresco de la gráfica.

### Mejorado
- **Diseño de Interfaz:** Reubicación de la seguridad física al pie de página para priorizar el análisis de datos masivos.
- **Gráfica de Pulso:** Optimización del motor de refresco automático (1s) para visualización fluida de riesgos.