import json
import pandas as pd
import os
import numpy as np
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE



# This class will store the methods and attributes needed to produce our clean dataframe
class DataFrameProcessor:
    def __init__(self, excel_file, dropped_columns = None, sampling_technique = None,mapping_file="mappings.json"):
        self.excel_file = excel_file
        self.mapping_file = mapping_file
        self.sampling_technique = sampling_technique
        self.df = None
        self.df_X = None
        self.df_y = None
        self.encoding_maps = {}
        self.dropped_columns = dropped_columns
        self.child_names = None


    def process(self):
        self.load_data()
        self.clean_data()
        if self.dropped_columns is not None:
            self.drop_columns()

        # Encoding the categorical columns might be harmful for the decision tree and we commented it out later
        self.encode_categorical_columns()

        self.df = self.df.fillna(0)

        self.separate_features_and_labels()

        return self.df_X, self.df_y


    # Load data from excel file and save it as a df in the class
    def load_data(self):
        self.df = pd.read_excel(self.excel_file, engine="openpyxl")

    # Performs simple cleaning on the dataframe that is general for all model types
    def clean_data(self):

        # Drop rows with more than three column values missing
        self.df = self.df.dropna(thresh=len(self.df.columns) - 3)

        self.child_names = self.df.iloc[:, 0]
        # Remove first column
        self.df = self.df.iloc[:, 1:]

        # Fix BMI column (Remove whitespace, newlines, and tab characters)
        for i in self.df.index:
            original_string = self.df['BMI_Weight_Cat'][i]
            if type(original_string) is str:
                remove_whitespace = original_string.replace(" ", "")
                remove_newline = remove_whitespace.replace("\n", "")
                remove_tabs = remove_newline.replace("\t", "")
                self.df.at[i, 'BMI_Weight_Cat'] = remove_tabs

    # Will load JSON file that maps the string values to numbers
    # This JSON is created by encode_categorical_columns to maintain consistency of how we represent our string values
    def load_encoding_maps(self):
        if os.path.exists(self.mapping_file):
            try:
                with open(self.mapping_file, "r") as f:
                    self.encoding_maps = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.encoding_maps = {}
        else:
            self.encoding_maps = {}

    # This function will check if dataframe string data is already encoded by checking a json file.
    # If not, it will create a new dictionary and then write to mappings.json
    def encode_categorical_columns(self):
        self.load_encoding_maps()

        # Go through the dataframe one column at a time
        for col in self.df.columns:
            # Checking for empty column (Edge case)
            non_null_values = self.df[col].dropna()
            if non_null_values.empty:
                continue

            # Skip if the column appears to be numeric
            if isinstance(non_null_values.iloc[0], (int, float, np.int64)):
                continue

            # Ensure a mapping dictionary exists for the column
            # If not, it will append to the dict
            if col not in self.encoding_maps:
                self.encoding_maps[col] = {}

            # Start mapping from the next available integer
            unique_values = non_null_values.unique()
            max_index = max(self.encoding_maps[col].values(), default=-1) + 1
            for val in unique_values:
                if val not in self.encoding_maps[col]:
                    self.encoding_maps[col][val] = max_index
                    max_index += 1

            # Map the column values to integers using the encoding
            self.df[col] = self.df[col].map(self.encoding_maps[col])

        # Save the updated mappings back to the file
        with open(self.mapping_file, "w") as f:
            json.dump(self.encoding_maps, f, indent=4)
        return self.df

    def drop_columns(self):
        self.df = self.df.drop(columns=self.dropped_columns)

    def separate_features_and_labels(self):
        self.df_X = self.df.iloc[:, :-1]
        self.df_y = self.df.iloc[:, -1]


########################################################################################################################

# SMOTE is an oversampling technique that utilizes clustering on the dataset we wish to "blow up". It will pick points
# within the bounds of the cluster to generate new rows
# https://imbalanced-learn.org/dev/references/generated/imblearn.over_sampling.SMOTE.html
def smote_over_sampling(train_x, train_y, rand=None):
    #print("Length before resampling: " + str(len(train_x)))
    sm = SMOTE(random_state=rand)
    train_resample_x, train_resample_y = sm.fit_resample(train_x, train_y)
    #print("Length after resampling: " + str(len(train_resample_x)))
    return train_resample_x, train_resample_y

# Naive Oversampling (Duplicating records)
def over_sampling(train_x, train_y):

    # Combine feature and label set (Only way for resample method to work)
    combined = pd.concat([train_x, train_y], axis=1)

    # Separate majority and minority classes
    df_majority = combined[combined['Learning_Outcome_Status'] == 1]
    df_minority = combined[combined['Learning_Outcome_Status'] == 0]


    #Upsample minority class
    df_minority_upsampled = resample(df_minority,
                                     replace=True,  # sample with replacement
                                     n_samples=len(df_majority),  # to match majority class
                                     random_state=123)  # reproducible results

    # Combine majority class with upsampled minority class
    df_upsampled = pd.concat([df_majority, df_minority_upsampled])

    # Separate this df into feature and label set
    resampled_features = df_upsampled.drop(columns=['Learning_Outcome_Status'])
    resampled_labels = df_upsampled['Learning_Outcome_Status']

    return resampled_features, resampled_labels

# Naive Undersampling function
def under_sampling(train_x, train_y):

    # Combine dataframes for resample
    combined = pd.concat([train_x, train_y], axis=1)

    class_counts = combined['Learning_Outcome_Status'].value_counts()
    min_class_count = class_counts.min()  # Find the minority class count

    # Perform under sampling
    combined = combined.groupby('Learning_Outcome_Status', group_keys=False).apply(lambda x: x.sample(n=min_class_count, random_state=42))

    # Shuffle the dataset (optional)
    #df_undersampled = df_undersampled.sample(frac=1, random_state=42).reset_index(drop=True)

    # Separate this df into feature and label set
    resampled_features = combined.drop(columns=['Learning_Outcome_Status'])
    resampled_labels = combined['Learning_Outcome_Status']

    return resampled_features, resampled_labels

