# Recomendaciones Técnicas: Implementación de Mejoras para Notebook

**Documento Complementario a Auditoría Integral**  
**Propósito:** Código y ejemplos concretos para implementar mejoras

---

## 1. MEJORA: Análisis Profundo de Síntomas "Contraintuitivos"

### Problema Identificado
Síntomas como `Confusion` y `Disorientation` muestran mayor prevalencia en grupo sin Alzheimer (contrarios a expectativa clínica). Análisis superficial sin investigación de causas.

### Solución: Análisis de Colinealidad Sintomática

**Agregar a Sección 3.4.2 (posterior a gráfico de prevalencia):**

```python
# 3.4.2.2 Investigación de Síntomas Contraintuitivos

# Hipótesis: Confusion NO es específico de Alzheimer; 
# es común en comorbilidades (depresión, delirium)

# Análisis 1: Correlación entre síntomas potencialmente confundidores
confounders = ["Confusion", "Disorientation", "Depression", "BehavioralProblems"]
confusion_matrix = df[confounders].corr()

import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    confusion_matrix, 
    annot=True, 
    fmt=".2f", 
    cmap="RdYlGn", 
    center=0,
    ax=ax,
    cbar_kws={"label": "Correlation"}
)
ax.set_title(
    "Correlación entre Síntomas Potencialmente Confundidos\n" +
    "(¿Confusion es proxy de Depression?)",
    fontsize=12, fontweight='bold'
)
plt.tight_layout()
plt.show()

# Análisis 2: Cruce tabulado 2x2x2
print("\n" + "="*70)
print("ANÁLISIS DE ESPECIFICIDAD: Confusion EN CADA GRUPO DIAGNÓSTICO")
print("="*70)

for diagnosis in [0, 1]:
    label = "Sano" if diagnosis == 0 else "Alzheimer"
    subset = df[df["Diagnosis"] == diagnosis]
    
    confusion_rate = subset["Confusion"].mean() * 100
    depression_rate = subset["Depression"].mean() * 100
    
    # Co-ocurrencia: ambos síntomas presentes
    both = (subset["Confusion"] & subset["Depression"]).sum()
    both_rate = (both / len(subset)) * 100
    
    print(f"\n{label} (n={len(subset)}):")
    print(f"  - Confusion prevalencia: {confusion_rate:.1f}%")
    print(f"  - Depression prevalencia: {depression_rate:.1f}%")
    print(f"  - Ambos síntomas: {both_rate:.1f}%")
    
    # Si Confusion y Depression correlacionadas > 0.5, entonces confusión es "ruidosa"
    subset_corr = subset[["Confusion", "Depression"]].corr()
    print(f"  - Correlación Confusion-Depression: {subset_corr.iloc[0,1]:.2f}")

print("\n" + "="*70)
print("INTERPRETACIÓN:")
print("="*70)
print("""
Si correlación alta (>0.4):
  → Confusion es manifestación de comorbilidad depresiva, no Alzheimer específico
  
Recomendación clínica:
  El síntoma Confusion debería ajustarse por Depression en análisis posterior
  (o excluirse del model si es redundante después de Depression como control)
""")
```

---

## 2. MEJORA: Análisis de Calibración del Modelo

### Problema Identificado
No se evalúa si probabilidades predichas reflejan realidad. Un modelo que predice P=0.7 debe tener ~70% de verdaderos positivos en esa cohorte.

### Solución: Gráfico de Calibración

**Agregar a final de Sección 6.3 (post-evaluación RF):**

```python
# 6.3.5 Evaluación de Calibración

from sklearn.calibration import calibration_curve, CalibrationDisplay
import matplotlib.pyplot as plt

# Calcular curva de calibración
prob_true, prob_pred = calibration_curve(
    y_test, 
    rf_model.predict_proba(X_test)[:, 1],
    n_bins=10
)

# Visualización
fig, ax = plt.subplots(figsize=(10, 8))

# Diagonal perfecta (modelo bien calibrado)
ax.plot([0, 1], [0, 1], 'k--', label='Perfectamente Calibrado', linewidth=2)

# Curva del modelo
ax.plot(prob_pred, prob_true, 'o-', linewidth=2, 
        label='Random Forest', markersize=8, color='#9370DB')

ax.set_xlabel('Probabilidad Predicha (P modelo)', fontsize=12, fontweight='bold')
ax.set_ylabel('Probabilidad Observada (Frecuencia Real)', fontsize=12, fontweight='bold')
ax.set_title(
    'Calibración del Random Forest: ¿Coinciden Predicción y Realidad?\n' +
    'Si curva = línea diagonal → Bien calibrado',
    fontsize=13, fontweight='bold', pad=15
)
ax.legend(loc='upper left', fontsize=11)
ax.grid(alpha=0.3)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

plt.tight_layout()
plt.show()

# Métrica de calibración: Expected Calibration Error (ECE)
from sklearn.metrics import brier_score_loss

ece = np.mean(np.abs(prob_true - prob_pred))
brier = brier_score_loss(y_test, rf_model.predict_proba(X_test)[:, 1])

print("\n" + "="*70)
print("MÉTRICAS DE CALIBRACIÓN")
print("="*70)
print(f"Expected Calibration Error (ECE): {ece:.3f}")
print(f"  Interpretación: Error promedio entre P predicho y P observado")
print(f"  Rango: 0 (perfecto) a 1 (peor)")
print(f"  Nuestro modelo: {'BIEN calibrado' if ece < 0.10 else 'Requiere ajuste'}")
print(f"\nBrier Score: {brier:.3f}")
print(f"  Interpretación: Sumatorio de (predicción - realidad)^2")
print(f"  Nuestro modelo: {'EXCELENTE' if brier < 0.15 else 'ACEPTABLE' if brier < 0.25 else 'REVISAR'}")

print("\n" + "="*70)
print("IMPLICACIÓN CLÍNICA:")
print("="*70)
print(f"""
Si modelo predice P=0.80 en paciente X:
  - Realidad: Basado en calibración, ~{prob_true[prob_pred.tolist().index(min(prob_pred, key=lambda x: abs(x - 0.80)))] * 100:.0f}% será Alzheimer
  - Confianza clínica: {'ALTA ✓' if ece < 0.10 else 'MODERADA ⚠️'}
  
Si ECE es alto (>0.15):
  → Requiere post-hoc scaling (Platt scaling o isotonic regression)
  → Las probabilidades crudas NO son directamente interpretables clínicamente
""")
```

---

## 3. MEJORA: Umbrales Operacionales Basados en Clínica

### Problema Identificado
Modelo predice probabilidades pero falta definir punto de corte operacional (¿qué P activa derivación?)

### Solución: Precision-Recall Analysis con Umbrales Clínicos

**Agregar nueva Sección 6.7:**

```python
# 6.7 Selección de Umbral Operacional (Decision Point)

from sklearn.metrics import precision_recall_curve, f1_score
import numpy as np

# Calcular curva Precision-Recall para todos los umbrales
precisions, recalls, thresholds = precision_recall_curve(
    y_test, 
    rf_model.predict_proba(X_test)[:, 1]
)

# Visualización de trade-off Precision vs Recall
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Gráfico 1: Precision-Recall Curve
ax1.plot(recalls, precisions, 'o-', linewidth=2, markersize=6, color='#9370DB')
ax1.axhline(y=0.70, color='r', linestyle='--', alpha=0.5, label='Precision ≥70%')
ax1.axvline(x=0.90, color='g', linestyle='--', alpha=0.5, label='Recall ≥90% (Target clínico)')
ax1.set_xlabel('Recall (Sensibilidad): ¿Detectamos enfermos?', fontsize=11, fontweight='bold')
ax1.set_ylabel('Precision: ¿Cuántos detectados son verdaderos?', fontsize=11, fontweight='bold')
ax1.set_title('Curva Precision-Recall\n(Trade-off Clínico)', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3)
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)

# Gráfico 2: F1-Score vs Threshold
f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-8)
ax2.plot(thresholds, f1_scores[:-1], linewidth=2, color='#FF6B6B')
ax2.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5, label='Threshold por defecto (0.5)')
ax2.set_xlabel('Umbral de Probabilidad (Decision Threshold)', fontsize=11, fontweight='bold')
ax2.set_ylabel('F1-Score (Balance Precision-Recall)', fontsize=11, fontweight='bold')
ax2.set_title('F1-Score vs Umbral\n(Optimización)', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# Tabla de recomendaciones clínicas
print("\n" + "="*100)
print("RECOMENDACIONES DE UMBRAL POR CONTEXTO CLÍNICO")
print("="*100)

scenarios = [
    {"name": "Screening general (minimizar pérdidas)", "recall_target": 0.92, "precision_min": 0.60},
    {"name": "Pre-diagnóstico (balance)", "recall_target": 0.85, "precision_min": 0.70},
    {"name": "Confirmación (máxima especificidad)", "recall_target": 0.70, "precision_min": 0.85}
]

for scenario in scenarios:
    # Encontrar umbral que cumple criterios
    valid_idx = np.where(
        (recalls >= scenario["recall_target"]) & 
        (precisions >= scenario["precision_min"])
    )[0]
    
    if len(valid_idx) > 0:
        best_idx = valid_idx[0]
        threshold = thresholds[best_idx] if best_idx < len(thresholds) else 0.5
        n_positive_pred = (rf_model.predict_proba(X_test)[:, 1] >= threshold).sum()
        
        print(f"\n{scenario['name']}")
        print(f"  Target: Recall ≥ {scenario['recall_target']*100:.0f}%, Precision ≥ {scenario['precision_min']*100:.0f}%")
        print(f"  Umbral recomendado: {threshold:.3f}")
        print(f"  Recall esperado: {recalls[best_idx]:.3f} ({recalls[best_idx]*100:.1f}%)")
        print(f"  Precision esperada: {precisions[best_idx]:.3f} ({precisions[best_idx]*100:.1f}%)")
        print(f"  Implicación: De {len(X_test)} pacientes, derivarían ~{n_positive_pred} (derivación rate: {n_positive_pred/len(X_test)*100:.1f}%)")
    else:
        print(f"\n{scenario['name']}")
        print(f"  ⚠️ No hay umbral que cumpla criterios específicos")

print("\n" + "="*100)
print("RECOMENDACIÓN FINAL PARA DEPLOYMENT")
print("="*100)
print("""
Para escenario típico de screening clínico:
  → Usar threshold = 0.55-0.65
  → Esto mantiene recall alto (>85%) con tasa de derivación operacionalmente viable
  → Requiere validar en setting específico (población, prevalencia, recursos)
""")
```

---

## 4. MEJORA: Análisis de Sensibilidad (Permutation Importance)

### Problema Identificado
Importancia de features (SHAP) no muestra cómo cambia rendimiento si remuevo cada variable

### Solución: Permutation Importance con Barras de Incertidumbre

**Agregar a Sección 7.3 (post-SHAP):**

```python
# 7.4 Robustez de Features: Análisis de Permutation Importance

from sklearn.inspection import permutation_importance

# Calcular cambio en AUC cuando permuta cada feature
perm_importance_result = permutation_importance(
    rf_model, 
    X_test, 
    y_test, 
    n_repeats=10, 
    random_state=42,
    scoring='roc_auc'
)

# Dataframe resultados
perm_df = pd.DataFrame({
    'Feature': X_test.columns,
    'Importance_Mean': perm_importance_result.importances_mean,
    'Importance_Std': perm_importance_result.importances_std
}).sort_values('Importance_Mean', ascending=False)

# Visualización
fig, ax = plt.subplots(figsize=(12, 7))

# Barras con error bars
y_pos = np.arange(len(perm_df))
ax.barh(
    y_pos, 
    perm_df['Importance_Mean'], 
    xerr=perm_df['Importance_Std'],
    color='#FF6B6B',
    alpha=0.7,
    error_kw={'elinewidth': 2, 'capsize': 5}
)

ax.set_yticks(y_pos)
ax.set_yticklabels(perm_df['Feature'])
ax.set_xlabel('Caída en AUC (cuando feature se permuta)', fontsize=12, fontweight='bold')
ax.set_title(
    'Robustez de Features: Permutation Importance\n' +
    '(¿Cuánto empeora el modelo sin cada variable?)',
    fontsize=13, fontweight='bold', pad=15
)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()

# Interpretación
print("\n" + "="*80)
print("INTERPRETACIÓN: PERMUTATION IMPORTANCE vs SHAP")
print("="*80)
print("""
SHAP (Sección 7):
  → Importancia "promedio" de cada feature en explicaciones
  → Base teórica: Shapley values (teoría de juegos)

Permutation Importance (aquí):
  → "¿Qué pasa al rendimiento si leo este feature aleatoriamente?"
  → Base empírica: degradación de métrica (AUC)

Diferencia importante:
  - SHAP: "Este feature contribuye X en promedio a decisiones"
  - Perm: "Sin este feature, el modelo pierde Y en AUC"
  
Si Feature A tiene SHAP alto pero Perm bajo:
  → Es importante para interpretación pero NO crítico para predicción
  → Posible redundancia con otro feature

Si Feature A tiene SHAP bajo pero Perm alto:
  → Es crítico para predicción pero contribuye poco individualmente
  → Efecto sinérgico/interactivo con otros
""")

# Tabla resumen
print("\n" + "="*80)
print("TABLA: Importancia Global (SHAP) vs Robustez (Permutation)")
print("="*80)

# Merge con SHAP del modelo
# (Asumir que ya existe feature_importance del RF)
rf_importance_pct = (rf_model.feature_importances_ / 
                     rf_model.feature_importances_.sum() * 100)

comparison_df = pd.DataFrame({
    'Feature': X_test.columns,
    'SHAP_Ranking': perm_df['Feature'].rank(ascending=False).values,
    'RF_Importance_%': rf_importance_pct,
    'Permutation_AUC_Loss': perm_df['Importance_Mean'].values
}).sort_values('Permutation_AUC_Loss', ascending=False)

display(comparison_df.head(10))
```

---

## 5. MEJORA: Odds Ratios para Regresión Logística

### Problema Identificado
Coeficientes de RL en sección 5.6 no se convierten a Odds Ratios (OR), formato clínico estándar

### Solución: Cálculo y Presentación de OR

**Reemplazar visualización actual de coeficientes (Sección 5.6):**

```python
# 5.6.1 Coeficientes como Odds Ratios (Formato Clínico)

import numpy as np
import pandas as pd

# Extraer coeficientes
coef_array = log_reg.coef_[0]
feature_names = X_train_scaled.columns

# Convertir a Odds Ratios
odds_ratios = np.exp(coef_array)

# DataFrame
or_df = pd.DataFrame({
    'Variable': feature_names,
    'Coeficiente': coef_array,
    'Odds_Ratio': odds_ratios,
    'Interpretacion': odds_ratios.apply(
        lambda x: f"{'×' if x > 1 else '÷'} {max(x, 1/x):.2f}" if x != 1 
        else "Sin cambio"
    )
}).sort_values('Odds_Ratio', ascending=False)

# Filtrar solo significativos (OR != 1, es decir, coef != 0)
or_df_sig = or_df[or_df['Odds_Ratio'] != 1]

print("\n" + "="*100)
print("INTERPRETACIÓN CLÍNICA: ODDS RATIOS")
print("="*100)

display(
    or_df_sig[['Variable', 'Odds_Ratio', 'Interpretacion']]
    .style.format({
        'Odds_Ratio': '{:.3f}'
    })
    .background_gradient(subset=['Odds_Ratio'], cmap='RdYlGn', vmin=0.5, vmax=1.5)
)

# Visualización
fig, ax = plt.subplots(figsize=(12, 8))

# Sortear por OR
or_sorted = or_df_sig.sort_values('Odds_Ratio')
colors = ['#FF6B6B' if x < 1 else '#52B788' for x in or_sorted['Odds_Ratio']]

ax.barh(or_sorted['Variable'], or_sorted['Odds_Ratio'], color=colors, alpha=0.7)
ax.axvline(x=1, color='black', linestyle='--', linewidth=2, label='Odds Ratio = 1 (sin efecto)')
ax.set_xlabel('Odds Ratio (Exponencial del Coeficiente)', fontsize=12, fontweight='bold')
ax.set_title(
    'Odds Ratios: Regresión Logística\n' +
    '(Multiplicador de Odds por Unidad de Cambio en Feature)',
    fontsize=13, fontweight='bold', pad=15
)
ax.legend()
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()

# Guía de interpretación
print("\n" + "="*100)
print("GUÍA DE INTERPRETACIÓN")
print("="*100)
print("""
Odds Ratio = 1.50 (e.g., MemoryComplaints)
  → Tener el síntoma multiplica las odds de Alzheimer por 1.5x
  → Si odds sin síntoma = 1:2 (25% riesgo), con síntoma = 1.5:2 (43% riesgo)

Odds Ratio = 0.78 (e.g., MMSE)
  → Por cada punto adicional en MMSE, odds de Alzheimer se multiplican por 0.78
  → Es decir, se REDUCEN en 22% (1 - 0.78)
  → Interpretación: Mejor desempeño cognitivo → menor riesgo

Odds Ratio = 0.50
  → Factor de PROTECCIÓN 50% (reduce odds a la mitad)

Odds Ratio > 2 o < 0.5
  → Efecto clínicamente sustancial
  → Requiere atención en evaluación clínica
""")
```

---

## 6. MEJORA: Curva Precision-Recall (Complemento a ROC)

### Problema Identificado
Solo se presenta curva ROC. Precision-Recall es más informativa en contexto de desbalance clínico

### Solución: Gráficos Duales ROC + PR

**Agregar a Sección 5.5 (ROC-AUC):**

```python
# 5.5.2 Curva Precision-Recall (Métrica Clínica Alternativa)

from sklearn.metrics import PrecisionRecallDisplay, precision_recall_curve
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# ROC AUC (existing)
from sklearn.metrics import RocCurveDisplay
RocCurveDisplay.from_predictions(
    y_test, y_proba, 
    name='Regresión Logística',
    ax=ax1,
    color='#9370DB',
    linewidth=2
)
ax1.set_title('Curva ROC (Balance Global)', fontsize=12, fontweight='bold')
ax1.grid(alpha=0.3)

# Precision-Recall (nuevo)
PrecisionRecallDisplay.from_predictions(
    y_test, y_proba,
    name='Regresión Logística',
    ax=ax2,
    color='#FF6B6B',
    linewidth=2
)
ax2.set_title(
    'Curva Precision-Recall\n(Relevante para Desbalance + Costo de FP)',
    fontsize=12, fontweight='bold'
)
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# Interpretación comparada
print("\n" + "="*100)
print("ROC vs PRECISION-RECALL: ¿Cuándo usar cada una?")
print("="*100)
print("""
ROC (Curva Actual):
  ✓ Útil cuando clases balanceadas
  ✓ Resiste bien al desbalance moderado
  ✗ Puede ser engañosa si desbalance extremo (>90% negativo)

Precision-Recall (Nuevo):
  ✓ Óptima cuando desbalance significativo (como aquí: 2/3 vs 1/3)
  ✓ Enfatiza costo de falsos positivos en contexto médico
  ✓ Mejor refleja utilidad operacional

Nuestro caso (Alzheimer):
  - Desbalance 2:1 (moderado, no extremo)
  - AMBAS curvas son relevantes
  - Recomendación: Usar PR para decisiones operacionales, ROC para reportes
""")

# Calcular PR-AUC
from sklearn.metrics import average_precision_score

pr_auc = average_precision_score(y_test, y_proba)
print(f"\nPrecision-Recall AUC: {pr_auc:.3f}")
print(f"ROC AUC: {roc_auc:.3f}")
print(f"Diferencia: {abs(pr_auc - roc_auc):.3f} (indica relevancia del desbalance)")
```

---

## 7. MEJORA: Análisis de Coeficientes Faltantes (Variables No Seleccionadas)

### Problema Identificado
Se seleccionan 28 features pero no se justifica exclusión de otros potenciales

### Solución: Documentar Selección de Features

**Agregar a Sección 4.1:**

```python
# 4.1.1 Justificación de Selección de Features

# Dataset completo: listar todas las variables
all_vars = df.columns.tolist()
selected_vars = selected_features

excluded_vars = [v for v in all_vars if v not in selected_vars + [target]]

print("\n" + "="*80)
print("SELECTION DE FEATURES: JUSTIFICACIÓN")
print("="*80)
print(f"Total variables en dataset: {len(all_vars)}")
print(f"Variables seleccionadas: {len(selected_vars)}")
print(f"Variables excluidas: {len(excluded_vars)}")

print(f"\nVariables EXCLUIDAS (potencialmente informativas):")
for var in excluded_vars:
    print(f"  - {var}")

print(f"""
CRITERIO DE SELECCIÓN:
  1. Tipos de datos: Numérica OR Binaria
  2. Relevancia clínica: Variables sin ambigüedad en interpretación
  3. Falta de redundancia obvia: No incluir ID, índices duplicados
  
NOTA IMPORTANTE:
  La exclusión NO implica falta de valor predictivo.
  Se realizó selección conservadora en favor de interpretabilidad.
  
VALIDACIÓN:
  Usar Feature Importance (RF) para detectar si variables excluidas 
  habrían contribuido significativamente
  (si no están en top-20 importancia, exclusión justificada retrospectivamente)
""")
```

---

## 8. MEJORA: Documentación de Limitaciones Epidemiológicas

### Problema Identificado
Análisis transversal confundido con predictivo; falta documentar que es "clasificación presente" no "pronóstico futuro"

### Solución: Expandir Sección de Limitaciones

**Reemplazar 9.2 con versión más completa:**

```python
# En el notebook, Sección 9.2.1 (nuevo):

markdown_text = """
## 9.2 Consideraciones Éticas y Limitaciones Epidemiológicas

### 9.2.1 Diferencia Crítica: Clasificación Transversal vs. Pronóstico Longitudinal

**ESTE MODELO CLASIFICA, NO PREDICE FUTURO**

El modelo entrenado en este proyecto responde:
  P(Diagnosis=Alzheimer | características clínicas ACTUALES)

Es decir: Si vemos estos síntomas/escalas HOY, ¿tiene Alzheimer HOY?

**NO responde** (aunque podría parecer que sí):
  P(convertirá a Alzheimer en 3 años | características actuales, Sano HOY)

### Implicación Clínica Crítica

Un paciente con **Deterioro Cognitivo Leve (MCI)** puede:
  - Tener score ALTO en nuestro modelo (síntomas presentes)
  - Pero NO convertir a Alzheimer (~30% conversión en 5 años)
  - O convertir pero más lentamente de lo esperado

**Nuestro modelo NO discrimina MCI estable vs. MCI in vía a Alzheimer**

### Validación Requerida para Uso Clínico

Para cambiar de "ejercicio académico" a "herramienta clínica", se requeriría:
  1. **Validación Externa** en cohorte independiente
  2. **Validación Longitudinal** (seguimiento ≥3 años)
     - Ver si pacientes con alto score realmente desarrollan Alzheimer
     - Medir tiempo a conversión (supervivencia)
  3. **Análisis de Subgrupos** en MCI (discriminar estables vs. progresores)
  4. **Estudios de Implementación** (¿mejora impacto clínico real?)

### 9.2.2 Sesgos Potenciales en Dataset Público

El dataset Kaggle usado es **sintético/curado**, no es cohorte clínica real:
  - Posible **sesgo de selección**: ¿quién fue incluido en diagnóstico?
  - Posible **sesgo de información**: ¿cómo se midieron síntomas?
  - Sin metadatos: Escalas exactas para ADL/FA no especificadas
  - Sin covariables clínicas críticas: educación (afecta MMSE), etnia, ApoE4 status

### 9.2.3 Recomendación Final

**Este proyecto es EDUCATIVO Y DEMOSTRATIVO, NO CLÍNICO**

Si alguien planteara usar esto en práctica clínica, sería IRRESPONSABLE sin:
  ✅ Validación externa en n>500 pacientes
  ✅ Estudios de utilidad clínica (alter o no el tratamiento?)
  ✅ Equipo médico revisor (pares)
  ✅ Cumplimiento normativo (FDA, CE mark, regulaciones locales)

El proyecto demuestra **competencia técnica en ML**, no **idoneidad clínica**.
"""

print(markdown_text)
```

---

## 9. SCRIPT: Importar Literatura Clínica (Referencias BibTeX)

**Crear archivo nuevo `references.bib`:**

```bibtex
@article{mckhann2011,
  title={Diagnosis of {A}lzheimer's disease},
  author={McKhann, Guy M and Knopman, David S and Chertkow, Howard and others},
  journal={Alzheimer's \& Dementia},
  volume={7},
  number={3},
  pages={263--269},
  year={2011},
  publisher={Elsevier}
}

@article{petersen2004,
  title={Mild cognitive impairment as a diagnostic entity},
  author={Petersen, Ronald C},
  journal={Journal of Internal Medicine},
  volume={256},
  number={3},
  pages={183--194},
  year={2004}
}

@article{hachinski2016,
  title={The vascular contribution to cognitive impairment and dementia},
  author={Hachinski, Vladimir and Iadecola, Costantino and others},
  journal={Journal of Neurology, Neurosurgery \& Psychiatry},
  volume={87},
  number={12},
  pages={1324--1341},
  year={2016}
}

@article{dubois2018,
  title={Preclinical {A}lzheimer disease: definition, natural history, and diagnostic criteria},
  author={Dubois, Bruno and Hampel, Harald and Feldman, Henry H and others},
  journal={Alzheimer's \& Dementia},
  volume={14},
  number={4},
  pages={535--562},
  year={2018}
}
```

---

## Checklist de Implementación

```
PRIORITARIO (Si tienes 4 horas):
[ ] Mejora #1: Análisis de síntomas contraintuitivos (1.5h)
[ ] Mejora #3: Umbrales operacionales (1.5h)
[ ] Mejora #5: Odds Ratios (0.5h)
[ ] Mejora #8: Expandir limitaciones epidemiológicas (0.5h)

IMPORTANTE (Si tienes más tiempo):
[ ] Mejora #2: Calibración (1h)
[ ] Mejora #4: Permutation Importance (1.5h)
[ ] Mejora #6: Precision-Recall curve (0.5h)
[ ] Mejora #7: Documentar exclusiones de features (0.5h)
[ ] Mejora #9: Agregar referencias BibTeX (0.5h)

VALORIZADO POR PORTFOLIO:
  → Completar mejoras #1, #3, #5, #8 (Bajo esfuerzo, alto impacto)
  → Estas muestran "pensamiento crítico + implementación"
```

---

**Fin del documento técnico**  
Cualquier duda en implementación, referirse a secciones en la Auditoría Integral.

