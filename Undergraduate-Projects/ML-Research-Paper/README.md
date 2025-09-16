# Music Genre Classification (GTZAN) — Course Project

*Classical ML baseline with feature selection. Original course submission (kept intact) + notes on suggested improvements.*

**Tech:** R • GTZAN • MFCC • Chroma • Logistic Regression • Random Forest • kNN
---

## Overview
This project explores music genre classification on the GTZAN dataset using classical machine-learning models.  
The focus is on feature engineering (MFCC & Chroma), simple baselines (Logistic Regression, Random Forest, kNN),  
and feature selection (RFE, Boruta).

**Status:** The repo preserves the **original course code** (graded at 94%).  
A short **Suggested Improvements** section documents what I’d fix in a future pass.
---

## Dataset
- **GTZAN:** 10 genres, ~100 clips/genre (30-sec WAV files).  
- **Access:** Not included in this repo. Download separately and update `data_path` in the script(s).  
- **Use:** Research/education only. Please respect the dataset license.
---

## Features
- **Basic:** `tempo` and `spectral_centroid` as implemented in the original code.  
- **Engineered:** MFCC (13 coefficients) and Chroma (12 bins), summarized as **means per track**.  
- **Selection:** Recursive Feature Elimination (RFE) and Boruta for feature importance.  

> **Heads-up (transparency):** In the original code, `tempo` returns the audio **sample rate** (not BPM),  
> and `spectral_centroid` is approximated via mean FFT magnitude.  
> See **Suggested Improvements** for how I’d fix this.

![Project Workflow](<img width="888" height="572" alt="image" src="https://github.com/user-attachments/assets/4edb9d8b-7f5a-4586-984a-84e5483a1d0d" />
)


---
## Models
- **Logistic Regression** (multinomial)  
- **Random Forest**  
- **k-Nearest Neighbors** (kNN)  

### Example: Logistic Regression (original)
```r
library(caret)
library(nnet)

set.seed(42)
train_index <- createDataPartition(feature_data$genre, p = 0.7, list = FALSE)
train_data  <- feature_data[train_index, ]
test_data   <- feature_data[-train_index, ]

model_logreg <- multinom(genre ~ tempo + spectral_centroid, data = train_data)
pred <- predict(model_logreg, newdata = test_data)
acc  <- mean(pred == test_data$genre)
cat("Accuracy:", acc, "\n")
```

### Example: MFCC + Chroma (summary features)
```r
# After computing MFCC/Chroma vectors per file:
feature_data_summary <- feature_data %>%
  mutate(
    mean_mfcc   = purrr::map_dbl(mfcc, mean),
    mean_chroma = purrr::map_dbl(chroma, mean)
  ) %>%
  select(genre, mean_mfcc, mean_chroma) %>%
  na.omit()

set.seed(42)
idx <- createDataPartition(feature_data_summary$genre, p = 0.8, list = FALSE)
tr  <- feature_data_summary[idx,  ] %>% mutate(genre = as.factor(genre))
te  <- feature_data_summary[-idx, ] %>% mutate(genre = as.factor(genre))

library(randomForest)
m_rf   <- randomForest(genre ~ mean_mfcc + mean_chroma, data = tr, ntree = 50, maxnodes = 10)
predRF <- predict(m_rf, newdata = te)
mean(predRF == te$genre)
```

---

## Evaluation
- **Splits:** Train/test **70/30** (and **80/20** for MFCC/Chroma).  
- **Metrics:** Accuracy, per-class **F1**, Confusion Matrix.  
- **Feature Selection:** RFE (RF estimator) and **Boruta**.  

Use `caret::confusionMatrix` for confusion matrices and the included plotting code  
to compare RFE vs Boruta feature rankings.

---

## Results (snapshot)

| Model               | Features                  | Accuracy |
|----------------------|---------------------------|---------:|
| Logistic Regression  | tempo + spectral_centroid |   29%    |
| Random Forest        | tempo + spectral_centroid |   28%    |
| kNN                  | tempo + spectral_centroid |   26%    |
| Logistic Regression  | mean(MFCC) + mean(Chroma) |   33%    |
| Random Forest        | mean(MFCC) + mean(Chroma) |   35%    |
| kNN                  | mean(MFCC) + mean(Chroma) |   58%    |

**Takeaways:**
- MFCC + Chroma substantially improved model performance.  
- kNN benefited most, rising from ~26% to ~58%.  
- Boruta highlighted **mean_chroma, mean_mfcc, spectral_centroid** as important; tempo was deemed unimportant.  
- RFE favored tempo + spectral centroid, showing how feature selection methods can disagree.
- These results are consistent with prior research, which has also found MFCC and Chroma features to be strong predictors of musical genre.

![Feature Rankings: RFE vs Boruta](<img width="459" height="414" alt="image" src="https://github.com/user-attachments/assets/243232eb-22c6-4478-9c5f-591f1ee47f2e" />)

---

## Limitations and Future Improvements
- Re-calculate tempo accurately: I treated sample rate as “tempo” but next time I’d use a true BPM tracker like `librosa.beat.beat_track` or `seewave::tempo()`.
- Spectral centroid error: I used the average FFT magnitude but in the future I’d switch to `seewave::specprop`.  
- Exploded rows vs. widened columns: my `combined_features` expanded rows instead of widening columns. Next time I’d fix this with `tidyr::unnest_wider()`.  
- Limited features: I only used a few descriptors but I’d add more like zero-crossing rate and spectral rolloff.  
- No hyperparameter tuning: Instead of defaults, I would try tuning kNN neighbors and RF depth which could improve results.  
- Evaluation method: I used a single split but next time I’d apply stratified k-fold cross-validation.  
- Dataset issues: I didn’t handle GTZAN’s duplicates/noise, in the future I’d clean it up more.  
- Advanced models: I stayed with classical ML but I’d explore CNNs/RNNs on spectrograms for stronger results.








