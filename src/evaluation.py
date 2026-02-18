"""
Funciones para evaluación de modelos y métricas de performance.
Incluye: confusion matrix, classification report, ROC, validación cruzada, comparación de modelos, etc.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score,
    RocCurveDisplay
)
from sklearn.model_selection import cross_validate, cross_val_predict
import matplotlib.pyplot as plt
import seaborn as sns


def get_predictions_and_probabilities(model, X_test):
    """
    Obtiene predicciones y probabilidades del modelo.
    
    Parameters
    ----------
    model : sklearn model
        Modelo entrenado.
    X_test : pd.DataFrame
        Datos de prueba.
    
    Returns
    -------
    tuple
        (y_pred, y_proba)
    """
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    return y_pred, y_proba


def print_classification_report(y_test, y_pred, class_names=None):
    """
    Imprime el reporte de clasificación.
    
    Parameters
    ----------
    y_test : array-like
        Valores reales.
    y_pred : array-like
        Valores predichos.
    class_names : list
        Nombres de las clases.
    """
    if class_names is None:
        class_names = ['Sano', 'Alzheimer']
    
    print("\n" + "="*53)
    print("REPORTES DE CLASIFICACIÓN")
    print("="*53)
    print(classification_report(y_test, y_pred, target_names=class_names))


def get_confusion_matrix(y_test, y_pred):
    """
    Calcula la matriz de confusión.
    
    Parameters
    ----------
    y_test : array-like
        Valores reales.
    y_pred : array-like
        Valores predichos.
    
    Returns
    -------
    array
        Matriz de confusión.
    """
    return confusion_matrix(y_test, y_pred)


def get_roc_auc_score(y_test, y_proba):
    """
    Calcula el score ROC AUC.
    
    Parameters
    ----------
    y_test : array-like
        Valores reales.
    y_proba : array-like
        Probabilidades predichas.
    
    Returns
    -------
    float
        ROC AUC score.
    """
    return roc_auc_score(y_test, y_proba)


def get_pr_auc_score(y_test, y_proba):
    """
    Calcula el score PR AUC (Average Precision).
    
    Parameters
    ----------
    y_test : array-like
        Valores reales.
    y_proba : array-like
        Probabilidades predichas.
    
    Returns
    -------
    float
        PR AUC score.
    """
    return average_precision_score(y_test, y_proba)


def plot_roc_curve(y_test, y_proba, title="Curva ROC"):
    """
    Plotea la curva ROC.
    
    Parameters
    ----------
    y_test : array-like
        Valores reales.
    y_proba : array-like
        Probabilidades predichas.
    title : str
        Título del gráfico.
    """
    RocCurveDisplay.from_predictions(y_test, y_proba)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def evaluate_model(model, X_test, y_test, model_name="Modelo", class_names=None):
    """
    Realiza una evaluación completa del modelo.
    
    Parameters
    ----------
    model : sklearn model
        Modelo entrenado.
    X_test : pd.DataFrame
        Datos de prueba.
    y_test : array-like
        Valores reales.
    model_name : str
        Nombre del modelo para imprimir.
    class_names : list
        Nombres de las clases.
    
    Returns
    -------
    dict
        Diccionario con métricas calculadas.
    """
    if class_names is None:
        class_names = ['Sano', 'Alzheimer']
    
    # Obtener predicciones
    y_pred, y_proba = get_predictions_and_probabilities(model, X_test)
    
    # Calcular métricas
    roc_auc = get_roc_auc_score(y_test, y_proba)
    pr_auc = get_pr_auc_score(y_test, y_proba)
    cm = get_confusion_matrix(y_test, y_pred)
    
    # Imprimir reportes
    print("=" * 60)
    print(f"{'MÉTRICAS DE DESEMPEÑO: ' + model_name.upper():^60}")
    print("=" * 60)
    print_classification_report(y_test, y_pred, class_names)
    
    print("-" * 60)
    print(f"{'Métricas de Área bajo la Curva (AUC)':^60}")
    print("-" * 60)
    print(f"ROC AUC Score: {roc_auc:>34.4f}")
    print(f"PR AUC Score (Average Precision): {pr_auc:>20.4f}")
    print("=" * 60)
    
    return {
        'y_pred': y_pred,
        'y_proba': y_proba,
        'roc_auc': roc_auc,
        'pr_auc': pr_auc,
        'confusion_matrix': cm
    }


def get_feature_importance(model, feature_names):
    """
    Extrae la importancia de features del modelo.
    
    Parameters
    ----------
    model : sklearn model
        Modelo entrenado (ej: RandomForest).
    feature_names : list
        Nombres de los features.
    
    Returns
    -------
    pd.DataFrame
        DataFrame con importancias ordenadas.
    """
    importances = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    return importances


def get_logistic_regression_coefficients(model, feature_names):
    """
    Extrae los coeficientes de una regresión logística.
    
    Parameters
    ----------
    model : LogisticRegression
        Modelo entrenado.
    feature_names : list
        Nombres de los features.
    
    Returns
    -------
    pd.DataFrame
        DataFrame con coeficientes ordenados.
    """
    coef_df = pd.DataFrame({
        "Feature": feature_names,
        "Coefficient": model.coef_[0]
    }).sort_values(by="Coefficient", ascending=False)
    
    return coef_df


def perform_cross_validation(model, X, y, cv=5, scoring=None):
    """
    Realiza validación cruzada en un modelo.
    
    Parameters
    ----------
    model : sklearn model
        Modelo a evaluar.
    X : pd.DataFrame
        Features.
    y : array-like
        Target.
    cv : int
        Número de folds.
    scoring : dict or None
        Diccionario de métricas. Si None, usa defaults.
    
    Returns
    -------
    dict
        Resultados de validación cruzada.
    """
    if scoring is None:
        scoring = {
            'accuracy': 'accuracy',
            'precision': 'precision',
            'recall': 'recall',
            'f1': 'f1',
            'roc_auc': 'roc_auc'
        }
    
    cv_results = cross_validate(
        model, X, y,
        cv=cv,
        scoring=scoring,
        return_train_score=True,
        n_jobs=-1
    )
    
    return cv_results


def summarize_cross_validation(cv_results, model_name="Modelo"):
    """
    Obtiene resumen de validación cruzada.
    
    Parameters
    ----------
    cv_results : dict
        Resultados de validación cruzada.
    model_name : str
        Nombre del modelo.
    
    Returns
    -------
    pd.DataFrame
        Resumen de métricas.
    """
    # Extraer solo test scores
    test_scores = {key: value for key, value in cv_results.items() if key.startswith('test_')}
    
    # Renombrar y calcular promedio y desv estándar
    summary = {}
    for metric, scores in test_scores.items():
        clean_name = metric.replace('test_', '')
        summary[f'{clean_name}_mean'] = np.mean(scores)
        summary[f'{clean_name}_std'] = np.std(scores)
    
    return pd.DataFrame([summary])


def plot_cross_validation_results(cv_results, metrics=['accuracy', 'precision', 'recall', 'f1', 'roc_auc']):
    """
    Plotea resultados de validación cruzada con barras agrupadas por métrica.
    
    Cada métrica tiene un grupo de barras (una por fold), organizadas horizontalmente.
    La altura de cada barra representa el score en ese fold. Se muestra una línea
    roja con el promedio para referencia visual.
    
    Parameters
    ----------
    cv_results : dict
        Resultados de validación cruzada (proveniente de cross_validate).
        Contiene claves como 'test_accuracy', 'test_precision', etc.
    metrics : list, default=['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        Métricas a graficar (deben existir como claves en cv_results).
    """
    n_metrics = len(metrics)
    n_folds = len(cv_results['test_accuracy'])
    
    # Dimensiones de figura: más ancha para acomodar claramente n_folds barras por métrica
    fig_width = max(14, 10 + n_folds * 0.5)
    fig, ax = plt.subplots(figsize=(fig_width, 7))
    
    # Posiciones base para cada grupo de métricas
    x = np.arange(n_metrics)
    
    # Ancho total disponible por grupo y ancho individual de cada barra
    total_width = 0.75  # Ancho total para el grupo de barras (deja espacio entre grupos)
    bar_width = total_width / n_folds
    
    # Paleta de colores: púrpura invertida para mayor contraste entre folds
    colors = sns.color_palette("Purples_r", n_folds)
    
    # Graficar cada fold como conjunto de barras
    for fold in range(n_folds):
        fold_scores = [cv_results[f'test_{metric}'][fold] for metric in metrics]
        
        # Desplazamiento dinámico que centra el grupo de barras sobre cada métrica
        # Fórmula: coloca las barras simétricamente alrededor de la posición x
        offset = (fold - (n_folds - 1) / 2) * bar_width
        
        ax.bar(x + offset, fold_scores, bar_width,
               label=f'Fold {fold + 1}', color=colors[fold], alpha=0.85, 
               edgecolor='white', linewidth=0.8)
    
    # Línea de promedio: se traza por encima de todas las barras
    mean_scores = [np.mean(cv_results[f'test_{metric}']) for metric in metrics]
    ax.plot(x, mean_scores, 'o-', color='red', linewidth=2.5, markersize=8,
            label='Promedio', zorder=15)
    
    # Configuración de ejes y etiquetas
    ax.set_xlabel('Métrica', fontsize=13, fontweight='bold')
    ax.set_ylabel('Score', fontsize=13, fontweight='bold')
    ax.set_title('Validación Cruzada: Desempeño por Fold y Métrica',
                 fontsize=14, fontweight='bold', pad=20)
    
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11)
    ax.tick_params(axis='y', labelsize=10)
    
    # Límites del eje Y: deja espacio inferior y superior
    ax.set_ylim([0, 1.12])
    
    # Grid horizontal sutil para mejor legibilidad
    ax.grid(axis='y', alpha=0.25, linestyle='--', linewidth=0.7)
    ax.set_axisbelow(True)
    
    # Leyenda
    ax.legend(title="Folds", fontsize=10, title_fontsize=11,
              loc='upper right', framealpha=0.95, edgecolor='gray')
    
    # Estilo limpio
    sns.despine()
    plt.tight_layout()
    plt.show()


def compare_models(models_dict, X_train, X_test, y_train, y_test, cv=5):
    """
    Compara múltiples modelos en train y test.
    
    Parameters
    ----------
    models_dict : dict
        Diccionario {nombre: modelo_estimador}.
    X_train : pd.DataFrame
        Datos de entrenamiento.
    X_test : pd.DataFrame
        Datos de test.
    y_train : array-like
        Target de entrenamiento.
    y_test : array-like
        Target de test.
    cv : int
        Número de folds para validación cruzada.
    
    Returns
    -------
    dict
        Resultados comparativos de todos los modelos.
    """
    results = {}
    
    for model_name, model in models_dict.items():
        print(f"\n{'='*60}")
        print(f"Evaluando: {model_name}")
        print(f"{'='*60}")
        
        # Entrenar modelo
        model.fit(X_train, y_train)
        
        # Test set evaluation
        y_pred_test = model.predict(X_test)
        y_proba_test = model.predict_proba(X_test)[:, 1]
        
        test_metrics = {
            'accuracy': (y_pred_test == y_test).mean(),
            'precision': classification_report(y_test, y_pred_test, output_dict=True)['1']['precision'],
            'recall': classification_report(y_test, y_pred_test, output_dict=True)['1']['recall'],
            'f1': classification_report(y_test, y_pred_test, output_dict=True)['1']['f1-score'],
            'roc_auc': roc_auc_score(y_test, y_proba_test),
            'pr_auc': average_precision_score(y_test, y_proba_test)
        }
        
        # Cross-validation evaluation
        cv_results = perform_cross_validation(model, X_train, y_train, cv=cv)
        
        cv_summary = {
            'accuracy_cv_mean': np.mean(cv_results['test_accuracy']),
            'accuracy_cv_std': np.std(cv_results['test_accuracy']),
            'precision_cv_mean': np.mean(cv_results['test_precision']),
            'precision_cv_std': np.std(cv_results['test_precision']),
            'recall_cv_mean': np.mean(cv_results['test_recall']),
            'recall_cv_std': np.std(cv_results['test_recall']),
            'f1_cv_mean': np.mean(cv_results['test_f1']),
            'f1_cv_std': np.std(cv_results['test_f1']),
            'roc_auc_cv_mean': np.mean(cv_results['test_roc_auc']),
            'roc_auc_cv_std': np.std(cv_results['test_roc_auc']),
        }
        
        # Combinar resultados
        results[model_name] = {
            'test_metrics': test_metrics,
            'cv_results': cv_results,
            'cv_summary': cv_summary,
            'model': model
        }
        
        # Imprimir resumen
        print(f"\nTest Set Performance:")
        print(f"  Accuracy: {test_metrics['accuracy']:.4f}")
        print(f"  Precision: {test_metrics['precision']:.4f}")
        print(f"  Recall: {test_metrics['recall']:.4f}")
        print(f"  F1-Score: {test_metrics['f1']:.4f}")
        print(f"  ROC AUC: {test_metrics['roc_auc']:.4f}")
        print(f"\nCross-Validation (Train Set):")
        print(f"  Accuracy CV: {cv_summary['accuracy_cv_mean']:.4f} ± {cv_summary['accuracy_cv_std']:.4f}")
        print(f"  ROC AUC CV: {cv_summary['roc_auc_cv_mean']:.4f} ± {cv_summary['roc_auc_cv_std']:.4f}")
    
    return results


def plot_model_comparison(comparison_results, metric='roc_auc'):
    """
    Plotea comparación de modelos.
    
    Parameters
    ----------
    comparison_results : dict
        Resultados de comparación de modelos.
    metric : str
        Métrica a comparar ('accuracy', 'precision', 'recall', 'f1', 'roc_auc').
    """
    models = list(comparison_results.keys())
    test_scores = [comparison_results[m]['test_metrics'][metric] for m in models]
    cv_means = [comparison_results[m]['cv_summary'][f'{metric}_cv_mean'] for m in models]
    cv_stds = [comparison_results[m]['cv_summary'][f'{metric}_cv_std'] for m in models]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(models))
    width = 0.35
    
    # Test set scores
    bars1 = ax.bar(x - width/2, test_scores, width, label='Test Set', color='#9370DB', alpha=0.8)
    
    # Cross-validation means with error bars
    bars2 = ax.bar(x + width/2, cv_means, width, label='CV Mean (Train)', 
                   color='#E0B0FF', alpha=0.8, yerr=cv_stds, capsize=5)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Modelo', fontsize=12)
    ax.set_ylabel(f'{metric.capitalize()} Score', fontsize=12)
    ax.set_title(f'Comparación de Modelos: {metric.upper()}', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylim([0, 1])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def create_comparison_table(comparison_results):
    """
    Crea tabla comparativa de modelos.
    
    Parameters
    ----------
    comparison_results : dict
        Resultados de comparación.
    
    Returns
    -------
    pd.DataFrame
        Tabla comparativa.
    """
    data = []
    
    for model_name, results in comparison_results.items():
        test = results['test_metrics']
        cv = results['cv_summary']
        
        data.append({
            'Modelo': model_name,
            'Test Accuracy': f"{test['accuracy']:.4f}",
            'Test Precision': f"{test['precision']:.4f}",
            'Test Recall': f"{test['recall']:.4f}",
            'Test F1': f"{test['f1']:.4f}",
            'Test ROC AUC': f"{test['roc_auc']:.4f}",
            'CV Accuracy': f"{cv['accuracy_cv_mean']:.4f} ± {cv['accuracy_cv_std']:.4f}",
            'CV ROC AUC': f"{cv['roc_auc_cv_mean']:.4f} ± {cv['roc_auc_cv_std']:.4f}",
        })
    
    return pd.DataFrame(data)
