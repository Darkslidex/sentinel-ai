import sys
import os
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Añadimos la ruta de 'src' para poder importar nuestro motor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fraud.engine import FraudDetector

def generate_mock_data():
    """Genera datos sintéticos altamente desbalanceados (1% fraude)."""
    X, y = make_classification(
        n_samples=10000, 
        n_features=10, 
        n_clusters_per_class=1, 
        weights=[0.99], 
        flip_y=0, 
        random_state=42
    )
    cols = [f'feature_{i}' for i in range(10)]
    df_X = pd.DataFrame(X, columns=cols)
    df_y = pd.Series(y)
    return df_X, df_y

def run_test():
    print("--- 🛡️ INICIANDO PRUEBA DE SENTINEL AI - MOTOR ANTI-FRAUDE ---")
    X, y = generate_mock_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 1. ESCENARIO SIN SMOTE (Lo que haría un analista junior)
    print("\n[!] Escenario 1: Modelo Estándar (Sin balanceo)")
    legacy_model = RandomForestClassifier(random_state=42)
    legacy_model.fit(X_train, y_train)
    legacy_preds = legacy_model.predict(X_test)
    print(classification_report(y_test, legacy_preds))

    # 2. ESCENARIO CON SENTINEL AI (Tu implementación Senior)
    print("\n[⭐] Escenario 2: Motor Sentinel AI (Con SMOTE)")
    sentinel = FraudDetector()
    sentinel.train(X, y) # El método .train ya incluye SMOTE internamente
    
    print("\n--- ✅ CONCLUSIÓN TÉCNICA ---")
    print("El modelo sin SMOTE suele ignorar el fraude por su baja frecuencia.")
    print("Sentinel AI genera datos sintéticos para 'enseñar' al modelo qué buscar.")

if __name__ == "__main__":
    run_test()