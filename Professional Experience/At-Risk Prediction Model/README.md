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

## Methodology

A crucial first step in this project was ensuring the creation of a high-quality, analysis-ready dataframe. Since we did not have direct database access at the time, we relied on program-generated reports rather than SQL queries. This meant the cleaning process was manual and time-consuming that included ransforming PDF-style reports into structured Excel tables.

As the domain expert on the database, I guided the data sourcing process by identifying which reports contained relevant variables for modeling and how they related across systems. We consolidated data from two separate databases, each with differing formats and structures, requiring individualized cleaning workflows for each report type.

After standardizing the datasets, we merged them using the Child ID as the primary key to form a single unified dataframe. Data transformations included encoding categorical values, converting text or numeric fields as appropriate, and applying binary flags where necessary. Once the dataset reached a stable structure, we compared several model architectures and selected Random Forest and a Neural Network (PyTorch) for testing.

Model performance was validated using K-Fold Cross Validation to ensure fairness and robustness across data splits. Results were visualized in Power BI to demonstrate how model predictions could be interpreted by educators and administrators in an actionable way.

## Findings

Model evaluation produced encouraging results, achieving an average accuracy of 85% across K-fold validations. This established a strong baseline for further development.
Feature importance analysis revealed that the top three predictors for identifying “at-risk” students were:

. Attendance

. Disability indicators

. Adult income levels

These findings provided valuable early insight into which variables most strongly correlate with risk outcomes. However, the analysis also revealed a class imbalance within the dataset since most students were classified as “not at risk,” leading to slight bias in the model’s predictions. Despite this, the prototype successfully demonstrated how predictive modeling could support early identification and proactive decision-making for student intervention and satisfied the reqruiements I had set out for Phase 1.

## Challenges

The most significant challenge was the data cleaning and preparation process, which took nearly two months from start to finish. Because raw data came in non-tabular formats (PDF-style reports exported from our primary database and others), extensive manual cleaning and restructuring were required.

Additional challenges included:

. **Lack of direct database access** which limited the ability to automate data retrieval.

. **Inconsistent report formats between systems** which required customized cleaning scripts per report type.

. **Missing or incomplete student records** that forced the removal of several rows to maintain data integrity.

. **Class imbalance** for the majority of students labeled “not at risk,” which introduced bias in model training.

These constraints slowed development but offered valuable lessons in data engineering, feature design, and practical machine learning within our data environments.

## Future Enhancements

Future iterations of this project will focus on strengthening both the data foundation and the predictive accuracy of the model. Key next steps include:

. **Direct database querying** to replace manual report extraction and streamline data preparation.

. **Improved handling of missing data** by dropping features with insufficient records rather than entire student entries.

. **Expanding predictive features** such as enrollment status, kindergarten continuation tracking, and other relevant trends.

. **Re-labeling risk outcomes** by using more comprehensive definitions of “at-risk” and “on-track” aligned with program criteria.

These enhancements aim to improve both the usability and impact of the model, setting the stage for broader implementation across additional program years or counties.

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

> ⚠️ **Note:**  
> This project is for **demonstration and portfolio purposes only.**  
> The scripts are illustrative and will not run without private datasets.

---

## Workflow Diagram
<img width="549" height="676" alt="Updated ML Flowchart" src="https://github.com/user-attachments/assets/cf4dfbc5-ed5f-4c3c-81c8-c3b39cdcae6d" />

---
## PowerBI Dashboard
> ⚠️ **Note:**  
> The student ID's have been renamed and site information has been blurred out for **demonstration and portfolio purposes only.**
<img width="705" height="416" alt="Cleaned ML Project Screenshot" src="https://github.com/user-attachments/assets/45a1fa09-402f-4614-98eb-2a20e878b2c3" />

---

## Tech Stack

- **Language:** Python  
- **Core Libraries:** `pandas`, `numpy`, `scikit-learn`, `imblearn`, `matplotlib`  
- **Deep Learning:** `PyTorch`  
- **Utilities:** `joblib`, `openpyxl`, `tkinter`

---
