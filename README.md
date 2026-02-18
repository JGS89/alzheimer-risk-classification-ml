# Alzheimer Risk Classification — Interpretable Machine Learning

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Latest-orange.svg)](https://scikit-learn.org/)
[![SHAP](https://img.shields.io/badge/Interpretability-SHAP-green.svg)](https://shap.readthedocs.io/)

## 📝 Overview
This project presents an **end-to-end Machine Learning pipeline** for binary classification of Alzheimer’s disease. Developed as a portfolio and training project, it emphasizes **interpretability, methodological rigor, and clinical reasoning** over raw predictive performance.

The analysis simulates a realistic clinical decision support scenario, where the objective is to prioritize patients at higher risk based on demographic, clinical, cognitive, and functional variables.

> [!WARNING]
> **Important Disclaimer:** This project is strictly educational. The model does not provide clinical diagnoses and is not intended for real-world medical use.

---

## 🎯 Project Goals
* **Formulate** a supervised classification problem in a healthcare context.
* **Build** an interpretable baseline model suitable for clinical environments.
* **Compare** linear (Logistic Regression) and non-linear (Random Forest) approaches.
* **Evaluate** models using metrics robust to class imbalance (Recall, Precision, ROC-AUC).
* **Apply** model explainability techniques (**SHAP**) to validate coherence with clinical knowledge.
* **Demonstrate** good practices in reproducible data science.

---

## 📊 Dataset
* **Source:** [Alzheimer’s Disease Dataset — Kaggle (2024)](https://www.kaggle.com/)
* **Author:** Rabie El Kharoua
* **Nature:** Synthetic / curated dataset for educational purposes.
* **Target Variable:** `Diagnosis` (0 = No Alzheimer, 1 = Alzheimer).

The dataset simulates clinical, demographic, cognitive, functional, and lifestyle information. *Note: It does not represent a validated clinical cohort.*

---

## 📁 Repository Structure
```text
alzheimer-risk-classification-ml/
│
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   ├── .gitignore
│   └── alzheimers_disease_data.csv
├── notebook/
│   ├── .gitignore
│   └── ml_alzheimer_classification.ipynb
└── src/
    ├── README.md
    ├── __init__.py
    ├── data_processing.py
    ├── evaluation.py
    ├── modeling.py
    ├── plotting.py
    ├── utils.py
    └── __pycache__/
        ├── __init__.cpython-310.pyc
        ├── data_processing.cpython-310.pyc
        ├── evaluation.cpython-310.pyc
        ├── modeling.cpython-310.pyc
        ├── plotting.cpython-310.pyc
        └── utils.cpython-310.pyc

```

Nota: Esta lista refleja los archivos actualmente rastreados en `HEAD`.
