# Módulos del Proyecto - Clasificación Predictiva de Alzheimer

Este directorio contiene los módulos Python reutilizables para el pipeline de Machine Learning orientado a la clasificación predictiva de riesgo de Alzheimer.

## Estructura de módulos

### `utils.py`
Utilidades generales y configuración estética.

**Funciones principales:**
- `setup_theme()`: Configura matplotlib y seaborn
- `get_palette()`: Retorna paleta de colores del proyecto
- `get_class_names()`: Retorna nombres de clases

**Constantes:**
- `PALETTE_COLORS`: Diccionario con colores (#B0B0B0 negativo, #E0B0FF positivo)
- `CLASS_NAMES`: ["Sano", "Alzheimer"]
- `RANDOM_SEED`: 42 (reproducibilidad)

---

### `data_processing.py`
Funciones para carga, exploración y preparación de datos.

**Funciones principales:**
- `load_alzheimer_data(data_path)`: Carga CSV
- `analyze_missing_values(df)`: Analiza valores faltantes
- `analyze_target_distribution(df)`: Distribución de la variable objetivo
- `analyze_binary_prevalence(df, variables)`: Prevalencia por grupo diagnóstico
- `prepare_features_and_target(df, selected_features)`: Separación X, y
- `split_train_test(X, y)`: Split estratificado
- `scale_numeric_features(X_train, X_test, numeric_features)`: StandardScaler

---

### `plotting.py`
Funciones de visualización profesionales y reutilizables.

**Funciones principales:**
- `plot_cognitive_features(df, features)`: Boxplots + KDEs de variables cognitivas
- `plot_continuous_comparison(df, feature)`: Comparación de variable continua por grupos
- `plot_clinical_features_grid(df, features)`: Grid de boxplots clínicos
- `plot_binary_symptoms_prevalence(summary_df)`: Barplot de prevalencia de síntomas
- `plot_correlation_heatmap(corr_matrix, short_names, title)`: Heatmap de correlaciones
- `plot_confusion_matrix(cm, class_names)`: Matriz de confusión
- `plot_model_coefficients(coef_df, title)`: Coeficientes de RL
- `plot_feature_importance(importances_df, title)`: Importancia de features (RF)

---

### `modeling.py`
Funciones para entrenar modelos.

**Funciones principales:**
- `train_logistic_regression(X_train, y_train, penalty="l2")`: Regresión Logística baseline
- `train_random_forest(X_train, y_train, n_estimators=300)`: Random Forest

---

### `evaluation.py`
Funciones para evaluación y métricas de performance.

**Funciones principales:**
- `get_predictions_and_probabilities(model, X_test)`: Retorna predicciones y probabilidades
- `print_classification_report(y_test, y_pred)`: Imprime reporte de clasificación
- `get_confusion_matrix(y_test, y_pred)`: Matriz de confusión
- `get_roc_auc_score(y_test, y_proba)`: ROC AUC
- `get_pr_auc_score(y_test, y_proba)`: PR AUC
- `plot_roc_curve(y_test, y_proba, title)`: Plotea ROC
- `evaluate_model(model, X_test, y_test)`: Evaluación completa e integrada
- `get_feature_importance(model, feature_names)`: Feature importance (RF)
- `get_logistic_regression_coefficients(model, feature_names)`: Coeficientes (RL)

---

## Uso desde el notebook

```python
# Importar módulos
from src import utils, plotting, data_processing, evaluation, modeling

# Configurar tema
utils.setup_theme()

# Cargar datos
df = data_processing.load_alzheimer_data("../data/alzheimers_disease_data.csv")

# Análisis exploratorio
df[numeric_features].describe()
plotting.plot_cognitive_features(df, ["MMSE", "ADL", "FunctionalAssessment"])

# Preparación de datos
X_train_scaled, X_test_scaled, scaler = data_processing.scale_numeric_features(
    X_train, X_test, numeric_features
)

# Modelado
model = modeling.train_logistic_regression(X_train_scaled, y_train)

# Evaluación
results = evaluation.evaluate_model(model, X_test_scaled, y_test)
```

---

## Beneficios de esta estructura

✓ **Reutilización**: Funciones parametrizadas y generalizables  
✓ **Mantenibilidad**: Código centralizado, fácil de actualizar  
✓ **Reproducibilidad**: Parámetros consistentes (seeds, paletas)  
✓ **Claridad**: Notebook enfocado en lógica, no en detalles técnicos  
✓ **Escalabilidad**: Nuevas funciones se agregan sin afectar el notebook  
✓ **Documentación**: Docstrings en todas las funciones  

---

## Notas importantes

1. Los módulos están diseñados para ejecutarse desde el notebook ubicado en `../notebook/`
2. Las rutas de datos usan rutas relativas (ej: `../data/`)
3. Se mantiene coherencia estética con la paleta de colores definida
4. Todas las semillas aleatorias usan `RANDOM_SEED = 42`
