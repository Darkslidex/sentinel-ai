import torch
import cv2
import logging
import numpy as np
import functools
import os
import time
from datetime import datetime
from ultralytics import YOLO

# ==========================================================
# 🛡️ SENTINEL AI - SEGURIDAD Y CARGA (2026)
# ==========================================================
torch.load = functools.partial(torch.load, weights_only=False)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VisionSentinel:
    def __init__(self, model_path: str = 'yolov8n.pt'):
        try:
            self.model = YOLO(model_path)
            # Configuración de evidencias
            self.output_dir = "data/captures"
            os.makedirs(self.output_dir, exist_ok=True) # Crea la carpeta si no existe
            
            # Control de capturas para no saturar el disco
            self.last_capture_time = 0
            self.capture_cooldown = 3  # Segundos entre fotos de evidencia
            
            logging.info(f"--- ✅ MOTOR SENTINEL ONLINE | Evidencias en: {self.output_dir} ---")
        except Exception as e:
            logging.error(f"Error crítico: {e}")
            raise

    def save_evidence(self, frame):
        """
        Guarda una captura de pantalla con marca de tiempo.
        """
        current_time = time.time()
        if current_time - self.last_capture_time > self.capture_cooldown:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{self.output_dir}/INTRUSION_{timestamp}.jpg"
            
            # Guardamos la imagen
            cv2.imwrite(filename, frame)
            self.last_capture_time = current_time
            logging.warning(f"📸 EVIDENCIA GUARDADA: {filename}")

    def is_inside_roi(self, box, roi_points):
        x1, y1, x2, y2 = box
        base_point = (int((x1 + x2) / 2), int(y2))
        result = cv2.pointPolygonTest(np.array(roi_points, np.int32), base_point, False)
        return result >= 0

    def process_stream(self, rtsp_url: str, roi_points: list):
        source = rtsp_url if rtsp_url != "" else 0
        cap = cv2.VideoCapture(source)
        
        while True:
            ret, frame = cap.read()
            if not ret: break

            results = self.model.predict(source=frame, classes=[0], conf=0.4, verbose=False)
            cv2.polylines(frame, [np.array(roi_points, np.int32)], True, (255, 0, 0), 2)

            for box in results[0].boxes:
                coords = box.xyxy[0].tolist()
                x1, y1, x2, y2 = int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])

                if self.is_inside_roi(coords, roi_points):
                    # ALERTA EVIDENCIA
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(frame, "!!! INTRUSO !!!", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    
                    # Llamamos al guardado automático
                    self.save_evidence(frame)
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.imshow('Sentinel AI - Vigilancia con Evidencia', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = VisionSentinel()
    
    # URL: "" para Webcam
    HIKVISION_URL = "" 
    # HIKVISION_URL = "rtsp://usuario:contraseña@IP:PUERTO/Streaming/Channels/101"
    
    # Zona Prohibida (puedes volver al cuadrado o seguir con el corazón)
    ZONA_PROHIBIDA = [(150, 150), (450, 150), (450, 450), (150, 450)]
    
    detector.process_stream(HIKVISION_URL, ZONA_PROHIBIDA)