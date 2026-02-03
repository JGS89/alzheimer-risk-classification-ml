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
├── notebook/
│   └── ml_alzheimer_classification.ipynb   # Main analysis and modeling
│
├── data/
│   └── alzheimers_disease_data.csv          # Dataset file
│
└── README.md                               # Project documentation
