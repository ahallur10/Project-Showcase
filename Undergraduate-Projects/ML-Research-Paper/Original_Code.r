library(tidyverse)
library(dplyr)
library(fs)
library(class)
library(imputeTS)


data_path <- "/Users/anshulhallur/Documents/Machine Learning spring 23/Data/genres_original"
genre_folders <- dir(data_path)

# Initialize empty dataframe
music_data <- data.frame()

# Iterate through genre folders
for (genre in genre_folders) {
  genre_path <- file.path(data_path, genre)
  files <- dir(genre_path, full.names = TRUE)
  
  # Read genre information and create a dataframe
  genre_df <- tibble(
    file_path = files,
    genre = genre
  )
  
  # Append to the main dataframe
  music_data <- bind_rows(music_data, genre_df)
}

# Import libraries
library(tuneR)
library(purrr)

# Function to calculate tempo
calculate_tempo <- function(file_path) {
  wav_file <- readWave(file_path)
  return(wav_file@samp.rate)
}

# Function to calculate spectral centroid
calculate_spectral_centroid <- function(file_path) {
  wav_file <- readWave(file_path)
  wav_data <- wav_file@left
  return(mean(abs(fft(wav_data))))
}

# Extract features for all files and create a dataframe
feature_data <- music_data %>%
  mutate(
    tempo = map_dbl(file_path, calculate_tempo),
    spectral_centroid = map_dbl(file_path, calculate_spectral_centroid)
  )

# Install library caret
library(caret)

# Split training/test 70/30 ratio for model log reg model
set.seed(42)
train_index <- createDataPartition(feature_data$genre, p = 0.7, list = FALSE)
train_data <- feature_data[train_index,]
test_data <- feature_data[-train_index,]
# Install nnet if needed
library(nnet)
# Logistic Regression for 2 features
model_logreg <- multinom(genre ~ tempo + spectral_centroid, data = train_data)

# Install ggplot2 library for plotting GTZAN genre distribution
library(ggplot2)

ggplot(feature_data, aes(x = genre)) +
  geom_bar() +
  theme_minimal() +
  labs(title = "Distribution of Genres in GTZAN Dataset",
       x = "Genre",
       y = "Count")

plot_GTZAN <- recordPlot()

#########################


library(caret)

# Make predictions
predicted_genres <- predict(model_logreg, newdata = test_data)

# Calculate accuracy
accuracy <- mean(predicted_genres == test_data$genre)
cat("Accuracy:", accuracy, "\n")

# Calculate confusion matrix for logistic regression
unique_genres <- unique(c(levels(predicted_genres), levels(test_data$genre)))
predicted_genres_factor <- factor(predicted_genres, levels = unique_genres)
test_data_genre_factor <- factor(test_data$genre, levels = unique_genres)
conf_matrix <- confusionMatrix(predicted_genres_factor, test_data_genre_factor)

# Calculate F1-score
f1_score <- function(cm) {
  # Calculate precision, recall, and F1-score for each class
  precision <- cm$byClass[, "Precision"]
  recall <- cm$byClass[, "Recall"]
  f1 <- 2 * (precision * recall) / (precision + recall)
  return(f1)
}

f1_scores <- f1_score(conf_matrix)
cat("F1-scores:\n")
print(f1_scores)

# Install and load the randomForest package
library(randomForest)

# Convert the 'genre' column to a factor in both train_data and test_data
train_data$genre <- as.factor(train_data$genre)
test_data$genre <- as.factor(test_data$genre)


# Train the random forest model
model_rf <- randomForest(genre ~ tempo + spectral_centroid, data = train_data)

# Make predictions
predicted_genres_rf <- predict(model_rf, newdata = test_data)

# Calculate accuracy for random forest
accuracy_rf <- mean(predicted_genres_rf == test_data$genre)
cat("Accuracy (Random Forest):", accuracy_rf, "\n")

# Calculate confusion matrix for random forest
unique_genres_rf <- unique(c(levels(predicted_genres_rf), levels(test_data$genre)))
predicted_genres_rf_factor <- factor(predicted_genres_rf, levels = unique_genres_rf)
test_data_genre_rf_factor <- factor(test_data$genre, levels = unique_genres_rf)
conf_matrix_rf <- confusionMatrix(predicted_genres_rf_factor, test_data_genre_rf_factor)

# Calculate F1-score for random forest
f1_scores_rf <- f1_score(conf_matrix_rf)
cat("F1-scores (Random Forest):\n")
print(f1_scores_rf)

# Calculate the mean of the features in the training data
preprocessor <- preProcess(train_data[, c("tempo", "spectral_centroid")], method = c("center", "scale", "knnImpute"))

# Impute missing values in the training and testing data using the calculated mean
train_data_imputed <- predict(preprocessor, train_data[, c("tempo", "spectral_centroid")])
test_data_imputed <- predict(preprocessor, test_data[, c("tempo", "spectral_centroid")])

# Choose the number of neighbors (k)
k <- 5

# Train the kNN model and make predictions
predicted_genres_knn <- knn(train_data_imputed, test_data_imputed, cl = train_data$genre, k = k)

# Calculate accuracy for kNN
accuracy_knn <- mean(predicted_genres_knn == test_data$genre)
cat("Accuracy (k-Nearest Neighbors):", accuracy_knn, "\n")

# Calculate confusion matrix for kNN
unique_genres_knn <- unique(c(levels(predicted_genres_knn), levels(test_data$genre)))
predicted_genres_knn_factor <- factor(predicted_genres_knn, levels = unique_genres_knn)
test_data_genre_knn_factor <- factor(test_data$genre, levels = unique_genres_knn)
conf_matrix_knn <- confusionMatrix(predicted_genres_knn_factor, test_data_genre_knn_factor)

# Calculate F1-score for kNN
f1_scores_knn <- f1_score(conf_matrix_knn)
cat("F1-scores (k-Nearest Neighbors):\n")
print(f1_scores_knn)

##################################

# Load the necessary libraries
library(caret)

# Create a binary target variable for hip hop songs
feature_data$hip_hop <- ifelse(feature_data$genre == "hiphop", 1, 0)

# Split the data into training and testing sets
set.seed(42)
train_index <- createDataPartition(feature_data$hip_hop, p = 0.7, list = FALSE)
train_data_hh <- feature_data[train_index,]
test_data_hh <- feature_data[-train_index,]

# Set up the control parameters for RFE
control <- rfeControl(functions = rfFuncs,
                      method = "repeatedcv",
                      repeats = 3,
                      verbose = FALSE)

# Perform RFE using random forest as the model
rfe_results <- rfe(train_data_hh[, c("tempo", "spectral_centroid")],
                   train_data_hh$hip_hop,
                   sizes = 1:2,  # Use 1 to the total number of features
                   rfeControl = control)

# Show the results of RFE
print(rfe_results)


#########################################

library(tuneR)
library(seewave)
library(audio)
library(purrr)
library(reticulate)

librosa <- import("librosa")

# Function to calculate MFCCs
calculate_mfcc <- function(file_path) {
  wav_file <- readWave(file_path)
  wav_data <- wav_file@left / 2^(wav_file@bit - 1) # Scale the audio samples
  wav_file@left <- wav_data # Update the left channel in wav_file
  mfcc_features <- tuneR::melfcc(wav_file, wav_file@samp.rate, numcep = 13)
  return(colMeans(mfcc_features))
}

# Function to calculate Chroma features
calculate_chroma <- function(file_path) {
  wav_file <- readWave(file_path)
  tmp_file <- tempfile(fileext = ".wav")
  writeWave(wav_file, tmp_file)
  y <- librosa$load(tmp_file, sr = NULL)
  chroma_features <- librosa$feature$chroma_stft(y = y[[1]], sr = y[[2]])
  return(colMeans(chroma_features))
}

feature_data <- music_data %>%
  mutate(
    mfcc = map(file_path, calculate_mfcc),
    chroma = map(file_path, calculate_chroma)
  )


# Combine 'mfcc' and 'chroma' lists
feature_data <- feature_data %>%
  mutate(
    combined_features = map2(mfcc, chroma, ~ c(.x, .y))
  )

# Unnest the combined_features list
combined_data <- feature_data %>% unnest(combined_features)

# Add unique column names for each feature
feature_colnames <- c(
  paste0("mfcc_", seq_along(feature_data$mfcc[[1]])),
  paste0("chroma_", seq_along(feature_data$chroma[[1]]))
)

# Update the column names only for the MFCC and Chroma features
names(combined_data)[(ncol(feature_data) - 1 + 1):(ncol(feature_data) - 1 + length(feature_colnames))] <- feature_colnames

# Update feature_data with the new combined_data
feature_data <- combined_data


##########################################

# Set up the control parameters for RFE
control <- rfeControl(functions = rfFuncs,
                      method = "repeatedcv",
                      repeats = 3,
                      verbose = FALSE)

# Combine the tempo, spectral centroid, MFCC, and Chroma features
train_data <- train_data_hh[, c("tempo", "spectral_centroid", grep("mfcc_|chroma_", names(train_data_hh), value = TRUE))]
test_data <- test_data_hh[, c("tempo", "spectral_centroid", grep("mfcc_|chroma_", names(test_data_hh), value = TRUE))]

# Perform RFE using random forest as the model
rfe_results <- rfe(train_data,
                   train_data_hh$hip_hop,
                   sizes = 1:ncol(train_data),
                   rfeControl = control)

# Show the results of RFE using tempo, spectral centroid, MFCC, and Chroma features
print(rfe_results)


######################################################
# Create new df with average MFCC and Chroma
feature_data_summary <- feature_data %>%
  mutate(mean_mfcc = map_dbl(mfcc, mean),
         mean_chroma = map_dbl(chroma, mean)) %>%
  select(genre, mean_mfcc, mean_chroma)

# Clean dataset
feature_data_clean <- na.omit(feature_data_summary)
# Start training/test 80/20 split
set.seed(42)
train_indices <- createDataPartition(feature_data_clean$genre, p = 0.8, list = FALSE)
train_data <- feature_data_clean[train_indices,]
test_data <- feature_data_clean[-train_indices,]

# Now, I run the models again:

# Logistic Regression
model_logreg_mfcc_chroma <- multinom(genre ~ mean_mfcc + mean_chroma, data = train_data)
predicted_genres_mfcc_chroma <- predict(model_logreg_mfcc_chroma, newdata = test_data)
accuracy_mfcc_chroma <- mean(predicted_genres_mfcc_chroma == test_data$genre)
cat("Accuracy (Logistic Regression - MFCC and Chroma features):", accuracy_mfcc_chroma, "\n")

# Convert the genre column to a factor
train_data$genre <- as.factor(train_data$genre)
test_data$genre <- as.factor(test_data$genre)

# Random Forest with fewer trees and smaller depth
model_rf_mfcc_chroma <- randomForest(genre ~ mean_mfcc + mean_chroma, data = train_data, ntree = 50, maxnodes = 10)
predicted_genres_rf_mfcc_chroma <- predict(model_rf_mfcc_chroma, newdata = test_data)
accuracy_rf_mfcc_chroma <- mean(predicted_genres_rf_mfcc_chroma == test_data$genre)
cat("Accuracy (Random Forest - MFCC and Chroma features):", accuracy_rf_mfcc_chroma, "\n")

# k-Nearest Neighbors
library(kknn)
library(dplyr)
# Train on smaller sample as it is computationally expensive
train_data_sample <- train_data %>%
  sample_n(500)

model_knn_mfcc_chroma <- train.kknn(genre ~ mean_mfcc + mean_chroma, data = train_data_sample, kmax = 10, distance = 1)
predicted_genres_knn_mfcc_chroma <- predict(model_knn_mfcc_chroma, newdata = test_data)
accuracy_knn_mfcc_chroma <- mean(predicted_genres_knn_mfcc_chroma == test_data$genre)
cat("Accuracy (k-Nearest Neighbors - MFCC and Chroma features):", accuracy_knn_mfcc_chroma, "\n")

#################################################

# Create a new dataframe with the selected columns
new_feature_data <- music_data %>%
  mutate(
    tempo = map_dbl(file_path, calculate_tempo),
    spectral_centroid = map_dbl(file_path, calculate_spectral_centroid),
    mfcc = map(file_path, calculate_mfcc),
    chroma = map(file_path, calculate_chroma),
    mean_mfcc = map_dbl(mfcc, mean),
    mean_chroma = map_dbl(chroma, mean)
  ) %>%
  select(file_path, genre, tempo, spectral_centroid, mean_mfcc, mean_chroma)
###################################################

install.packages("Boruta")
library(Boruta)

train_data_boruta <- new_feature_data %>%
  select(genre, tempo, spectral_centroid, mean_mfcc, mean_chroma)

# Convert the 'genre' column to a binary variable for hip hop songs
train_data_boruta$hip_hop <- ifelse(train_data_boruta$genre == "hip_hop", 1, 0)
train_data_boruta$hip_hop <- as.factor(train_data_boruta$hip_hop)

# Remove rows with missing values
train_data_boruta_clean <- na.omit(train_data_boruta)

# Perform Boruta feature selection with the cleaned data
set.seed(42)
boruta_result <- Boruta(hip_hop ~ tempo + spectral_centroid + mean_mfcc + mean_chroma,
                        data = train_data_boruta_clean, 
                        doTrace = 0)

# Print the result
print(boruta_result)


train_data$hip_hop <- ifelse(train_data$genre == "hip_hop", 1, 0)
train_data$classical <- ifelse(train_data$genre == "classical", 1, 0)
train_data$country <- ifelse(train_data$genre == "country", 1, 0)
train_data$pop <- ifelse(train_data$genre == "pop", 1, 0)
train_data$jazz <- ifelse(train_data$genre == "jazz", 1, 0)


install.packages("Boruta")
install.packages("nnet")
library(Boruta)
library(nnet)

# Remove rows with missing values
train_data_clean <- na.omit(train_data)

# Perform Boruta feature selection with the cleaned data
set.seed(42)
boruta_result <- Boruta(as.factor(genre) ~ tempo + spectral_centroid + mean_mfcc + mean_chroma,
                        data = train_data_boruta_clean, 
                        doTrace = 0, classifier = multinom)

# Print the result
print(boruta_result)



# Load necessary libraries
library(caret)
library(Boruta)
library(nnet)

# RFE
control <- rfeControl(functions = rfFuncs, method = "cv", number = 10)
rfe_results <- rfe(train_data_hh, train_data_hh$hip_hop, sizes = 1:ncol(train_data), rfeControl = control)

# Boruta
boruta_result <- Boruta(as.factor(genre) ~ tempo + spectral_centroid + mean_mfcc + mean_chroma,
                         data = train_data_boruta_clean, 
                         doTrace = 0, classifier = multinom)

# Extract rankings from RFE and Boruta
rfe_rank <- rfe_results$ranking
boruta_rank <- as.integer(rownames(boruta_result$ImpHistory[order(as.integer(rownames(boruta_result$ImpHistory))),]))

# Get confirmed important features
boruta_important <- getSelectedAttributes(boruta_result, withTentative = F)

# Get the importance values for the confirmed important features
boruta_importance <- boruta_result$ImpHistory[as.integer(boruta_important), ncol(boruta_result$ImpHistory)]

# Create a named vector for Boruta importance with feature names
boruta_importance_named <- setNames(boruta_importance, boruta_important)


# Rank the importance values
boruta_rank <- rank(-boruta_importance_named)

# Sample features vector
features <- c("tempo", "spectral_centroid", "mean_mfcc", "mean_chroma")

# Initialize a boruta_rank_full vector with NAs
boruta_rank_full <- rep(NA, length(features))

# Check the content of boruta_rank_full
print(boruta_rank_full)
``

# Initialize a boruta_rank_full vector with NAs
boruta_rank_full <- rep(NA, length(features))

# Assign the ranks to the corresponding feature names
boruta_rank_full[which(features %in% names(boruta_rank))] <- boruta_rank

# Get the RFE ranks
rfe_rank_full <- c(1, rfe_rank)

# Combine rankings into a data frame
rank_data <- data.frame(features, rfe_rank = rfe_rank_full, boruta_rank = boruta_rank_full)


# Create the bar chart and display it

# Load ggplot2 package
library(ggplot2)

# Remove rows with missing values from rank_data
rank_data <- na.omit(rank_data)

# Reshape rank_data to a long format
rank_data_long <- rank_data %>%
  gather(key = "Algorithm", value = "Ranking", -features)

# Create bar chart
bar_chart <- ggplot(rank_data_long, aes(x = features, y = Ranking, fill = Algorithm)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Feature Rankings: RFE vs Boruta",
       x = "Features",
       y = "Ranking",
       fill = "Algorithm") +
  theme_minimal()

# Display the bar chart
print(bar_chart)
