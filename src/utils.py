"""
Utilidades generales para el proyecto de clasificación de Alzheimer.
Configuración estética, funciones auxiliares y constantes.
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Configuración estética global
PALETTE_COLORS = {0: "#B0B0B0", 1: "#E0B0FF"}
PALETTE_DIAGNOSIS = {"Sano": "#B0B0B0", "Alzheimer": "#E0B0FF"}
CLASS_NAMES = ["Sano", "Alzheimer"]
RANDOM_SEED = 42


def setup_theme():
    """Configura el tema estético para matplotlib y seaborn."""
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.dpi'] = 100


def get_palette():
    """Retorna la paleta de colores definida para el proyecto."""
    return PALETTE_COLORS


def get_class_names():
    """Retorna los nombres de las clases."""
    return CLASS_NAMES
