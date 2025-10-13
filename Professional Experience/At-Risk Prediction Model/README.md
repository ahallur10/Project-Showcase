# 🧠 At-Risk Student Prediction (Illustrative Machine Learning Project)

## 📋 Overview
This repository demonstrates a full **machine learning workflow** for predicting whether a student (or record) is **“on-track”** or **“at-risk.”**

It showcases:
- **Data preprocessing**  
- **Model training** (Decision Tree, Random Forest, or Neural Network)  
- **Evaluation and visualization** of model performance  

> ⚠️ **Note:**  
> This project is for **demonstration and portfolio purposes only.**  
> The scripts are illustrative and will not run without private datasets.

---

## 🧩 Workflow Diagram

![Workflow Diagram]

**Pipeline Overview:**
1. 📂 **Data** – Collected tabular datasets (e.g., attendance, demographics, program data).  
2. 🧹 **Preprocessing** – Cleaned, normalized, and encoded features.  
3. ✂️ **K-Fold Cross Validation** – Ensured balanced and fair model evaluation.  
4. 🌳 **Model Training** – Trained Decision Trees / Random Forests or  
   🧠 Neural Networks with early stopping (PyTorch).  
5. 📊 **Evaluation** – Produced accuracy metrics, confusion matrices, and reports.  
6. 📝 **Reporting** – Illustrated how results could be displayed in dashboards.

---

## ⚙️ Key Scripts

| File | Description |
|------|--------------|
| `data_preprocessing.py` | Cleans raw data, handles missing values, encodes categoricals, prepares feature and label sets. |
| `model_training.py` | Trains Decision Tree or Random Forest models using scikit-learn. |
| `nn_trainer.py` | Implements a compact PyTorch neural network with BatchNorm, Dropout, and early stopping. |
| `model_evaluation.py` | Calculates accuracy, confusion matrix, and classification report across folds. |
| `model_selector.py` | Optional Tkinter dialog for choosing model interactively (UI showcase). |
| `main.py` | Orchestrates the complete workflow (data → model → evaluation). |

---

## 🧰 Tech Stack

- **Language:** Python  
- **Core Libraries:** `pandas`, `numpy`, `scikit-learn`, `imblearn`, `matplotlib`  
- **Deep Learning:** `PyTorch`  
- **Utilities:** `joblib`, `openpyxl`, `tkinter`
