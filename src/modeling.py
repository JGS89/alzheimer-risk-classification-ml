"""
Funciones para entrenar y configurar modelos.
Incluye: LogisticRegression, RandomForest, etc.
"""

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


def train_logistic_regression(X_train, y_train, penalty="l2", random_state=42):
    """
    Entrena un modelo de Regresión Logística.
    
    Parameters
    ----------
    X_train : pd.DataFrame
        Datos de entrenamiento.
    y_train : array-like
        Target de entrenamiento.
    penalty : str
        Tipo de regularización ('l2' para Ridge).
    random_state : int
        Semilla aleatoria.
    
    Returns
    -------
    LogisticRegression
        Modelo entrenado.
    """
    model = LogisticRegression(
        penalty=penalty,
        class_weight="balanced",
        solver="liblinear",
        random_state=random_state
    )
    
    model.fit(X_train, y_train)
    
    return model


def train_random_forest(X_train, y_train, n_estimators=300, random_state=42):
    """
    Entrena un modelo de Random Forest.
    
    Parameters
    ----------
    X_train : pd.DataFrame
        Datos de entrenamiento.
    y_train : array-like
        Target de entrenamiento.
    n_estimators : int
        Número de árboles.
    random_state : int
        Semilla aleatoria.
    
    Returns
    -------
    RandomForestClassifier
        Modelo entrenado.
    """
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=None,
        min_samples_split=10,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    return model
