"""
Funciones de visualización para el análisis de Alzheimer.
Incluye: boxplots, KDEs, barplots, heatmaps, etc.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from .utils import PALETTE_COLORS, PALETTE_DIAGNOSIS, CLASS_NAMES


def plot_cognitive_features(df, features, target="Diagnosis"):
    """
    Plotea distribuciones de features cognitivas con boxplots y KDEs.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos.
    features : list
        Lista de variables cognitivas a visualizar.
    target : str
        Nombre de la columna objetivo.
    """
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.dpi'] = 100
    
    fig, axes = plt.subplots(2, len(features), figsize=(5*len(features), 10))
    if len(features) == 1:
        axes = axes.reshape(-1, 1)
    axes_flat = axes.flatten()

    for i, feature in enumerate(features):
        # Boxplots
        sns.boxplot(
            data=df,
            x=target,
            y=feature,
            hue=target,
            palette=PALETTE_COLORS,
            linewidth=1.5,
            fliersize=0,
            width=0.4,
            dodge=False,
            ax=axes_flat[i]
        )
        sns.stripplot(
            data=df, x=target, y=feature,
            color=".2", alpha=0.2, size=2, jitter=True, ax=axes_flat[i]
        )
        axes_flat[i].set_title(f"Distribución de {feature}", fontsize=12, fontweight='bold')
        axes_flat[i].set_xlabel("Diagnóstico (0: No, 1: Sí)")
        if axes_flat[i].get_legend():
            axes_flat[i].get_legend().remove()

        # KDE Plots
        sns.kdeplot(
            data=df,
            x=feature,
            hue=target,
            palette=PALETTE_COLORS,
            common_norm=False,
            fill=True,
            alpha=0.5,
            linewidth=2,
            ax=axes_flat[i + len(features)]
        )
        axes_flat[i + len(features)].set_title(f"Densidad de {feature}", fontsize=12, fontweight='bold')
        axes_flat[i + len(features)].set_xlabel(feature)
        axes_flat[i + len(features)].set_ylabel("Densidad")

    sns.despine()
    plt.tight_layout()
    plt.show()


def plot_continuous_comparison(df, feature, target="Diagnosis"):
    """
    Plotea un feature continuo comparando grupos (boxplot + KDE).
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos.
    feature : str
        Nombre de la variable continua.
    target : str
        Nombre de la columna objetivo.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Boxplot
    sns.boxplot(
        data=df,
        x=target,
        y=feature,
        hue=target,
        palette=PALETTE_COLORS,
        linewidth=1.5,
        fliersize=4,
        width=0.4,
        dodge=False,
        ax=axes[0]
    )
    axes[0].set_title(f'{feature} vs Diagnóstico', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Diagnóstico (0: No, 1: Sí)')
    axes[0].set_ylabel(feature)
    if axes[0].get_legend():
        axes[0].get_legend().remove()

    # KDE plot
    sns.kdeplot(
        data=df,
        x=feature,
        hue=target,
        palette=PALETTE_COLORS,
        common_norm=False,
        fill=True,
        alpha=0.5,
        linewidth=2,
        ax=axes[1]
    )
    axes[1].set_title(f'Densidad de Probabilidad de {feature}', fontsize=12, fontweight='bold')
    axes[1].set_xlabel(feature)
    axes[1].set_ylabel('Densidad')

    sns.despine()
    plt.tight_layout()
    plt.show()


def plot_clinical_features_grid(df, features, target="Diagnosis"):
    """
    Plotea un grid de features clínicas con boxplots + stripplots.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos.
    features : list
        Lista de variables clínicas.
    target : str
        Nombre de la columna objetivo.
    """
    n_features = len(features)
    n_rows = (n_features + 1) // 2
    
    fig, axes = plt.subplots(n_rows, 2, figsize=(10, 7*n_rows))
    axes_flat = axes.flatten() if n_rows > 1 else [axes[0], axes[1]]

    for i, var in enumerate(features):
        sns.boxplot(
            data=df,
            x=target,
            y=var,
            hue=target,
            palette=PALETTE_COLORS,
            linewidth=1.5,
            fliersize=0,
            width=0.4,
            dodge=False,
            ax=axes_flat[i]
        )
        sns.stripplot(
            data=df,
            x=target,
            y=var,
            color=".3",
            alpha=0.2,
            size=3,
            jitter=True,
            ax=axes_flat[i]
        )
        axes_flat[i].set_title(f"Distribución de {var}", fontsize=12, fontweight='bold', pad=10)
        axes_flat[i].set_xlabel("Diagnóstico (0: No, 1: Sí)")
        axes_flat[i].set_ylabel(var)
        if axes_flat[i].get_legend():
            axes_flat[i].get_legend().remove()

    # Ocultar subplots vacíos si es necesario
    for j in range(i + 1, len(axes_flat)):
        axes_flat[j].set_visible(False)

    sns.despine()
    plt.tight_layout()
    plt.show()


def plot_binary_symptoms_prevalence(summary_df):
    """
    Plotea la prevalencia de síntomas binarios en formato de barplot.
    
    Parameters
    ----------
    summary_df : pd.DataFrame
        DataFrame con columnas: Variable, % en Diag. Negativo, % en Diag. Positivo
    """
    resumen_plot = summary_df.melt(
        id_vars="Variable",
        value_vars=["% en Diag. Negativo", "% en Diag. Positivo"],
        var_name="Grupo",
        value_name="Porcentaje"
    )

    palette_sintomas = {
        "% en Diag. Negativo": "#B0B0B0",
        "% en Diag. Positivo": "#E0B0FF"
    }

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(
        data=resumen_plot,
        x="Variable",
        y="Porcentaje",
        hue="Grupo",
        palette=palette_sintomas
    )

    plt.title("Prevalencia de Síntomas según Diagnóstico", fontsize=14, fontweight='bold', pad=20)
    plt.ylabel("Pacientes con el síntoma (%)")
    plt.xlabel("Variable de Síntoma")
    plt.xticks(rotation=45)
    plt.ylim(0, resumen_plot["Porcentaje"].max() + 15)
    plt.legend(title="Grupo de Diagnóstico", loc='upper right')

    sns.despine()
    plt.tight_layout()
    plt.show()


def plot_correlation_heatmap(corr_matrix, short_names, title):
    """
    Plotea una matriz de correlación en formato heatmap.
    
    Parameters
    ----------
    corr_matrix : pd.DataFrame
        Matriz de correlación.
    short_names : dict
        Diccionario de nombres cortos para las variables.
    title : str
        Título del heatmap.
    """
    corr_visual = corr_matrix.rename(columns=short_names, index=short_names)

    plt.figure(figsize=(5, 4))
    sns.heatmap(
        corr_visual,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        cbar_kws={'label': 'Coeficiente de Pearson'}
    )

    plt.title(title, fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plot_confusion_matrix(cm, class_names=None):
    """
    Plotea la matriz de confusión.
    
    Parameters
    ----------
    cm : array-like
        Matriz de confusión.
    class_names : list
        Nombres de las clases.
    """
    if class_names is None:
        class_names = CLASS_NAMES

    plt.figure(figsize=(4, 2))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Purples',
        xticklabels=class_names,
        yticklabels=class_names,
        cbar=False,
        annot_kws={"size": 14, "weight": "bold"}
    )

    plt.title('Matriz de Confusión', fontsize=14, pad=20, fontweight='bold')
    plt.ylabel('Real', fontsize=9)
    plt.xlabel('Predicción', fontsize=9)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11, rotation=0)

    plt.tight_layout()
    plt.show()


def plot_model_coefficients(coef_df, title="Coeficientes del Modelo"):
    """
    Plotea los coeficientes de un modelo lineal.
    
    Parameters
    ----------
    coef_df : pd.DataFrame
        DataFrame con columnas 'Feature' y 'Coefficient'.
    title : str
        Título del gráfico.
    """
    coef_df = coef_df.sort_values(by="Coefficient", ascending=False)

    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=coef_df,
        x='Coefficient',
        y='Feature'
    )

    plt.axvline(0, color='black', linestyle='-', linewidth=1)
    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Magnitud del Coeficiente', fontsize=12)
    plt.ylabel('Variables', fontsize=12)

    for i, row in enumerate(coef_df.itertuples()):
        if abs(row.Coefficient) > 0.5:
            plt.text(row.Coefficient, i, f' {row.Coefficient:.2f}',
                     va='center', fontsize=10, fontweight='bold')

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.show()


def plot_feature_importance(importances_df, title="Ranking de Importancia de Variables"):
    """
    Plotea la importancia de features.
    
    Parameters
    ----------
    importances_df : pd.DataFrame
        DataFrame con columnas 'Feature' e 'Importance', ordenado descendentemente.
    title : str
        Título del gráfico.
    """
    plt.figure(figsize=(10, 9))
    sns.set_theme(style="white")

    ax = sns.barplot(
        data=importances_df,
        x='Importance',
        y='Feature',
        palette='Purples_r',
        edgecolor=".2"
    )

    for p in ax.patches:
        width = p.get_width()
        ax.text(
            width + 0.002,
            p.get_y() + p.get_height() / 2,
            f'{width:.2f}',
            va='center',
            fontsize=10,
            fontweight='bold',
            color='#4B0082'
        )

    plt.title(title, fontsize=15, fontweight='bold', pad=25)
    plt.xlabel('Importancia Relativa (Gini Impurity Reduction)', fontsize=12, labelpad=10)
    plt.ylabel('Variables Predictoras', fontsize=12)
    plt.xlim(0, importances_df['Importance'].max() * 1.15)

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.show()
