import pandas as pd
import logging
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Configuración de Logging para trazabilidad profesional
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FraudDetector:
    """
    Clase de alto nivel para la detección de anomalías y fraude transaccional.
    Implementa balanceo de datos mediante SMOTE para mitigar el sesgo de clase.
    """
    
    def __init__(self, random_state: int = 42):
        self.model = RandomForestClassifier(n_estimators=100, random_state=random_state)
        self.smote = SMOTE(random_state=random_state)
        self.is_trained = False
        logging.info("Motor Anti-Fraude inicializado correctamente.")

    def balance_data(self, X: pd.DataFrame, y: pd.Series):
        """
        Aplica SMOTE para equilibrar la clase minoritaria (fraude).
        Matemáticamente, SMOTE interpola puntos entre vecinos cercanos:
        $x_{new} = x_i + \lambda (x_{zi} - x_i)$
        """
        logging.info("Iniciando balanceo de datos con SMOTE...")
        X_resampled, y_resampled = self.smote.fit_resample(X, y)
        logging.info(f"Balanceo completado. Nuevas dimensiones: {X_resampled.shape}")
        return X_resampled, y_resampled

    def train(self, X: pd.DataFrame, y: pd.Series):
        """
        Entrena el modelo robusto después de balancear los datos.
        SMOTE se aplica solo al conjunto de entrenamiento: el conjunto de prueba
        conserva la distribución original para que las métricas no se inflen.
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        X_train_bal, y_train_bal = self.balance_data(X_train, y_train)
        
        logging.info("Entrenando Random Forest Classifier...")
        self.model.fit(X_train_bal, y_train_bal)
        self.is_trained = True
        
        # Evaluación técnica
        predictions = self.model.predict(X_test)
        report = classification_report(y_test, predictions)
        logging.info("Entrenamiento finalizado. Reporte de métricas:")
        print(report)
        
        return report

    def predict_risk(self, transaction_data: pd.DataFrame) -> float:
        """
        Calcula la probabilidad de que una transacción sea fraude.
        """
        if not self.is_trained:
            raise Exception("El modelo debe ser entrenado antes de realizar predicciones.")
        
        # Retorna la probabilidad de la clase positiva (fraude)
        probability = self.model.predict_proba(transaction_data)[:, 1]
        return probability