# At-Risk Student Prediction Model

## Overview
I designed this project to explore how machine learning can be applied to support early intervention for students who may be at risk of not meeting developmental goals. Developed as the capstone project for our data management intern, it was completed in collaboration with our programmer analyst. I led the design of the project specifications, timeline, data sources, and data-cleaning methodology, ensuring the intern was involved in each stage of development. The resulting Phase 1 implementation demonstrates a complete machine learning workflow for predicting whether a student record is “on track” or “at risk” for meeting learning outcomes for children ages 0–5. Model results were visualized in Power BI to translate predictions into actionable insights for educators and program staff. My aim was to implement this project by breaking it into 3 different phases:

**Phase 1 — Exploratory Development:**
Focused on building the initial machine learning prototype and verifying the feasibility of the approach.
This phase emphasized data exploration, identifying inconsistencies, and shaking out bugs in preprocessing and model training workflows.

**Phase 2 — Refinement and Enhancement:**
A more polished and optimized version of the workflow.
Improvements included refined feature engineering, better handling of missing data, and structural corrections based on insights from Phase 1.

**Phase 3 — Field Implementation and Evaluation:**
The finalized model will be deployed at a selected site to evaluate how teachers and staff interact with predictions in real-world settings.
This phase assesses the model’s usability, accuracy, and impact on early intervention decision-making.

## Problem Addressed
Early intervention programs often rely on static reporting or small-scale A/B testing to identify children who may need additional support. These methods can miss subtle patterns or combined risk factors across attendance, health, and family variables. This project explores how machine learning can improve early identification by capturing complex, nonlinear relationships among multiple indicators, enabling more proactive and data-informed support for children and families.


The project showcases:
- **Data preprocessing**  
- **Model training** (Decision Tree or Neural Network)  
- **Evaluation and visualization** of model performance  

> ⚠️ **Note:**  
> This project is for **demonstration and portfolio purposes only.**  
> The scripts are illustrative and will not run without private datasets.

## Methodology

A crucial part of this project was ensuring a high quality dataframe to begin with. At the time, we had to rely on generated reports through our database rather than query out the data since we did not have access. By doing so, our cleaning process took much longer than expected as we had to clean out PDF style reports on Excel. As the domain knowledge expert on the database, I was comfortable with transforming data reports into a clean table format to get it prepped for data modeling in PowerBI, so I provided guidance on what reports to use and which reports held the datapoints that were applicable for this project. This cleaning and transforming step included re-structuring the data from the reports on two separate databases, with many reports having a different format and structure which meant each report type needed it's own process of cleaning and transforming the data into clean tables. Once we had the cleaned datasets, we consolidated all the datasets by using the child's ID as a primary key and transformed the datasets into one big dataframe. We applied binary options where needed and converted certain values to text or the raw number, depending on the column and if it made sense to do so. We then 
---

## Key Scripts

| File | Description |
|------|--------------|
| `data_preprocessing.py` | Cleans raw data, handles missing values, encodes categoricals, prepares feature and label sets. |
| `model_training.py` | Trains Decision Tree or Random Forest models using scikit-learn. |
| `nn_trainer.py` | Implements a compact PyTorch neural network with BatchNorm, Dropout, and early stopping. |
| `model_evaluation.py` | Calculates accuracy, confusion matrix, and classification report across folds. |
| `model_selector.py` | Optional Tkinter dialog for choosing model interactively (UI showcase). |
| `main.py` | Orchestrates the complete workflow (data → model → evaluation). |

---

## Workflow Diagram
<img width="549" height="676" alt="Updated ML Flowchart" src="https://github.com/user-attachments/assets/cf4dfbc5-ed5f-4c3c-81c8-c3b39cdcae6d" />

---
## PowerBI Dashboard
> ⚠️ **Note:**  
> The student ID's have been renamed and site information has been blurred out for **demonstration and portfolio purposes only.**
<img width="705" height="416" alt="Cleaned ML Project Screenshot" src="https://github.com/user-attachments/assets/45a1fa09-402f-4614-98eb-2a20e878b2c3" />


---
## Pipeline Overview
1. **Data** – Created tabular datasets (e.g. attendance, demographics, program data) by cleaning and transforming generated reports on Excel.  
2. **Preprocessing** – Cleaned, normalized, and encoded features.  
3. **K-Fold Cross Validation** – Ensured balanced and fair model evaluation.  
4. **Model Training** – Trained Decision Trees / Random Forests or Neural Networks with early stopping (PyTorch).  
5. **Evaluation** – Produced accuracy metrics, confusion matrices and evaluated F1 scores.  
6. **Reporting** – Illustrated how results could be displayed in dashboards.

---

## Tech Stack

- **Language:** Python  
- **Core Libraries:** `pandas`, `numpy`, `scikit-learn`, `imblearn`, `matplotlib`  
- **Deep Learning:** `PyTorch`  
- **Utilities:** `joblib`, `openpyxl`, `tkinter`

---
