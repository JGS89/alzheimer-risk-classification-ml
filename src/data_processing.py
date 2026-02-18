"""
Funciones para procesamiento y exploración de datos.
Incluye: análisis de valores faltantes, distribución del target, resúmenes, etc.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def load_alzheimer_data(data_path):
    """
    Carga el dataset de Alzheimer.
    
    Parameters
    ----------
    data_path : str
        Ruta al archivo CSV.
    
    Returns
    -------
    pd.DataFrame
        DataFrame con los datos cargados.
    """
    df = pd.read_csv(data_path)
    return df


def analyze_missing_values(df):
    """
    Analiza valores faltantes en el dataset.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a analizar.
    
    Returns
    -------
    pd.DataFrame
        Resumen de valores faltantes.
    """
    missing_counts = df.isna().sum()
    missing_percentage = (missing_counts / len(df)) * 100

    missing_summary = pd.DataFrame({
        "missing_count": missing_counts,
        "missing_percentage": missing_percentage
    }).sort_values(by="missing_percentage", ascending=False)

    return missing_summary


def analyze_target_distribution(df, target="Diagnosis"):
    """
    Analiza la distribución de la variable objetivo.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos.
    target : str
        Nombre de la columna objetivo.
    
    Returns
    -------
    pd.DataFrame
        Resumen de distribución del target.
    """
    target_counts = df[target].value_counts().sort_index()
    target_percentage = df[target].value_counts(normalize=True).sort_index() * 100

    target_distribution = pd.DataFrame({
        "count": target_counts,
        "percentage": target_percentage
    })

    return target_distribution


def analyze_binary_prevalence(df, variables, target="Diagnosis"):
    """
    Calcula prevalencia de variables binarias por grupo de diagnóstico.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos.
    variables : list
        Lista de variables binarias.
    target : str
        Nombre de la columna objetivo.
    
    Returns
    -------
    pd.DataFrame
        Resumen de prevalencia.
    """
    summary = (
        df.groupby(target)[variables]
        .mean()
        .T * 100
    )

    summary = summary.reset_index()
    summary.columns = ["Variable", "% en Diag. Negativo", "% en Diag. Positivo"]
    summary['Dif_Absoluta'] = (summary["% en Diag. Positivo"] - summary["% en Diag. Negativo"]).round(2)

    return summary.sort_values(by="Dif_Absoluta", ascending=False)


def prepare_features_and_target(df, selected_features, target="Diagnosis"):
    """
    Prepara features y target para modelado.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos.
    selected_features : list
        Lista de features a seleccionar.
    target : str
        Nombre de la columna objetivo.
    
    Returns
    -------
    tuple
        (X, y) - Features y target.
    """
    X = df[selected_features]
    y = df[target]
    
    return X, y


def split_train_test(X, y, test_size=0.2, random_state=42):
    """
    Divide datos en train y test de forma estratificada.
    
    Parameters
    ----------
    X : pd.DataFrame
        Features.
    y : pd.Series
        Target.
    test_size : float
        Proporción de datos para test.
    random_state : int
        Semilla aleatoria.
    
    Returns
    -------
    tuple
        (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    
    return X_train, X_test, y_train, y_test


def scale_numeric_features(X_train, X_test, numeric_features):
    """
    Escala features numéricas usando StandardScaler.
    
    Parameters
    ----------
    X_train : pd.DataFrame
        Datos de entrenamiento.
    X_test : pd.DataFrame
        Datos de prueba.
    numeric_features : list
        Lista de features numéricas a escalar.
    
    Returns
    -------
    tuple
        (X_train_scaled, X_test_scaled, scaler)
    """
    scaler = StandardScaler()

    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()

    X_train_scaled[numeric_features] = scaler.fit_transform(X_train[numeric_features])
    X_test_scaled[numeric_features] = scaler.transform(X_test[numeric_features])

    return X_train_scaled, X_test_scaled, scaler
