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
Early intervention programs often rely on static reporting or small-scale A/B testing to identify children who may need additional support. These methods can miss subtle patterns or combined risk factors across attendance, health, and family variables. This project explores how machine learning can improve early identification by capturing complex, nonlinear relationships among multiple indicators, enabling more proactive and data-informed support for children and families. The key question was whether predictive modeling could reliably flag at-risk children early enough to inform staff intervention.

## Methodology

A crucial first step in this project was ensuring the creation of a high-quality, analysis-ready dataframe. Since we did not have direct database access at the time, we relied on program-generated reports rather than SQL queries. This meant the cleaning process was manual and time-consuming that included transforming PDF-style reports into structured Excel tables.

As the domain expert on the database, I guided the data sourcing process by identifying which reports contained relevant variables for modeling and how they related across systems. We consolidated data from two separate databases, each with differing formats and structures, requiring individualized cleaning workflows for each report type.

After standardizing the datasets, we merged them using the Child ID as the primary key to form a single unified dataframe. Data transformations included encoding categorical values, converting text or numeric fields as appropriate, and applying binary flags where necessary. Once the dataset reached a stable structure, we compared several model architectures and selected Random Forest and a Neural Network (PyTorch) for testing.

Model performance was validated using K-Fold Cross Validation to ensure fairness and robustness across data splits. Results were visualized in Power BI to demonstrate how model predictions could be interpreted by educators and administrators in an actionable way.

## Findings

We evaluated a **Decision Tree** (implemented in scikit-learn, with the option to scale into a Random Forest) and a **Neural Network** to predict whether a student was *Meeting/Exceeding expectations* or *Below expectations*.

The **Decision Tree** achieved an average **accuracy of 78%** and a **weighted F1-score of 0.78**, performing reliably for the majority (*Meeting/Exceeding*) class but struggling to correctly identify the minority *Below* category (**Recall = 0.15**, **Precision = 0.18**).

The **Neural Network** outperformed it with **86% accuracy** and a **weighted F1-score of 0.81**, demonstrating stronger overall learning but showing clear bias toward the majority class. This imbalance is evident in the low recall and precision (**Recall = 0.04, Precision = 0.40**) for at-risk students, indicating the model’s tendency to misclassify most *Below* cases as *Meeting*.

Despite these limitations, both models successfully learned meaningful patterns within the data, confirming that the dataset contains predictive signals when properly cleaned and structured, which forms a key improvement vector for **Phase 2**.The disparity between **macro F1 (0.52)** and **weighted F1 (0.80)** further evidences imbalance, showing that accuracy alone overstates model performance.

In summary, both models favor the majority class, yielding optimistic accuracy scores. The **Neural Network** generalizes better overall but sacrifices minority recall, while the **Decision Tree** provides clearer interpretability of which features drive predictions at the cost of performance. Feature importance analysis identified the **top three predictors** for at-risk classification as **Attendance**, **Disability indicators**, and **Adult income levels**.

These findings provide valuable early insight into which variables most strongly correlate with risk outcomes. While the dataset’s imbalance led to bias in predictions, the prototype successfully demonstrated how predictive modeling can support early identification and proactive decision-making for student intervention, meeting the objectives set for **Phase 1**.

### Model Performance Summary

| Metric | Decision Tree | Neural Network | Interpretation |
|--------|----------------|----------------|----------------|
| **Accuracy** | 0.78 | 0.86 | NN improves overall accuracy |
| **Precision (Below / Class 0)** | 0.18 | 0.40 | NN nearly doubles precision for minority class |
| **Recall (Below / Class 0)** | 0.15 | 0.04 | NN nearly ignores “Below” cases |
| **F1-Score (Below / Class 0)** | 0.17 | 0.08 | DT slightly better at catching "Below" cases |
| **Precision (Meeting / Class 1)** | 0.86 | 0.87 | Both strong on majority class |
| **Recall (Meeting / Class 1)** | 0.89 | 0.99 | NN nearly perfect recall on majority class |
| **Macro F1** | 0.52 | 0.52 | Highlights class imbalance in both models |
| **Weighted F1** | 0.78 | 0.81 | High overall score hides bias toward majority |
| **Key Takeaway** | – | – | Both models learn meaningful patterns, but the NN sacrifices minority recall for higher overall accuracy |

## Challenges

The most significant challenge was the data cleaning and preparation process, which took nearly two months from start to finish. Because raw data came in non-tabular formats (PDF-style reports exported from our primary database and others), extensive manual cleaning and restructuring were required.

Overall challenges included:

- **Lack of direct database access** which limited the ability to automate data retrieval.

- **Inconsistent report formats between systems** which required customized cleaning scripts per report type.

- **Missing or incomplete student records** that forced the removal of several rows to maintain data integrity.

- **Class imbalance** for the majority of students labeled “not at risk,” which introduced bias in model training.

These constraints slowed development but offered valuable lessons in data engineering, feature design, and practical machine learning within our data environments.

## Future Enhancements

Future iterations of this project will focus on strengthening both the data foundation and the predictive accuracy of the model. Key next steps include:

- **Direct database querying** to replace manual report extraction and streamline data preparation.

- **Improved handling of missing data** by dropping features with insufficient records rather than entire student entries.

- **Expanding predictive features** such as enrollment status, kindergarten continuation tracking, and other relevant trends.

- **Re-labeling risk outcomes** by using more comprehensive definitions of “at-risk” and “on-track” aligned with program criteria.

- **Address underlying issues** such as imbalanced labels, accuracy of labeling and feature quality

- **Balance the dataset** by continuing to use SMOTE or class weights to improve recall for the NN

These enhancements aim to improve both the usability and impact of the model, setting the stage for broader implementation across additional program years or counties.

---

### Repository File Overview

| File | Description |
|------|--------------|
| `construct_df (public).py` | Builds and cleans a structured dataframe from our cleaned Excel Dataframe. Handles missing values, normalization, and one-hot encoding. |
| `Decision_Tree (public).py` | Trains a Random Forest classifier using scikit-learn. Includes model persistence options. |
| `Neural Net (public).py` | Implements `NNTrainer`, a PyTorch-based MLP with BatchNorm, Dropout, and early stopping for binary classification tasks. |
| `accuracy (public).py` | Evaluates model performance using accuracy, confusion matrix, and classification reports. Aggregates K-fold results. |
| `Dialog_box (public).py` | Provides a simple Tkinter GUI allowing manual model selection (“Decision Tree” or “Neural Network”). Used for interactive demonstration. |
| `main_pipeline (public).py` | Orchestrates the full pipeline: preprocessing, model training (Decision Tree / Random Forest and Neural Net), K-fold validation, and evaluation reporting. |


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
