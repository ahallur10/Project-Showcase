import sys

from sklearn.model_selection import StratifiedKFold
import numpy as np
import construct_df as cd
import decision_tree as dtree
import accuracy
import neural_network as nn
import pandas as pd
import dialogbox as dbox
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Set pandas display options
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    # Get clean, overall dataframe
    # It comes in two parts (the feature set,df_X, and the label set, df_y)
    processor = cd.DataFrameProcessor(excel_file="DataFrame", dropped_columns=None)
    df_X, df_y = processor.process()
    print(df_X)
    print(df_y)

    # Use a dialog box to select the model
    user_choice = dbox.choose_model()
    print(f"Selected Model: {user_choice}")

    # Specify the amount of splits for K-Fold Cross Validation
    # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html
    skf = StratifiedKFold(n_splits=5)
    skf.get_n_splits(np.array(df_X), np.array(df_y))
    StratifiedKFold(n_splits=5, random_state=None, shuffle=False)


    # Run the appropriate model based on the user's selection
    # It will create n amount of models and display the accuracy measures in a table format
    # empty label list will store all generated and actual list pairs from all runs
    labels = []
    if user_choice == "Decision Tree":
        for i, (train_index, test_index) in enumerate(skf.split(df_X, df_y)):
            child_names = processor.child_names[test_index]
            # Get actual data from the indices from the enumeration
            train_x, train_y, test_x, test_y = df_X.iloc[train_index], df_y.iloc[train_index], df_X.iloc[test_index], df_y.iloc[test_index]
            # Comment out the bottom line to remove SMOTE
            train_x, train_y = cd.smote_over_sampling(train_x, train_y, rand=None)
            # Run the decision tree
            decision_tree_algo = dtree.DecisionTreeLabelGenerator(train_x, train_y,
                                                                  test_x, test_y)
            # Get list of labels and append to our list
            generated_labels, actual_labels = decision_tree_algo.run()
            labels.append([generated_labels, actual_labels, child_names])

        # print out accuracy measures for k-fold approach
        # Input is in format:
        # [[[generated label model 1, generated model 1, ...], [actual model 1, ...]], [[generated model 2, ...], [actual model 2, ...]], ...]
        # Will print out a table of these accuracies and the averages
        accuracy.get_accuracy(labels)

    # NN will display the error rate vs the number of epochs in a graph at the end
    # It will plot n amount of lines on a single graph with a legend to clarify model number
    elif user_choice == "Neural Network":
        loss_curves = []  # list to hold the curves for each fold
        for i, (train_index, test_index) in enumerate(skf.split(df_X, df_y)):
            child_names = processor.child_names[test_index]
            train_x, train_y, test_x, test_y = df_X.iloc[train_index], df_y.iloc[train_index], df_X.iloc[test_index], df_y.iloc[test_index]
            # (optional) Comment out the bottom line to remove SMOTE
            train_x, train_y = cd.smote_over_sampling(train_x, train_y, rand=None)

            # Train the NN
            trainer = nn.NeuralNetworkTrainer(train_x, train_y, test_x, test_y, epochs=150, early_stopping_patience=25, early_stopping_min_delta=0.00001,
                                              lr=0.001)

            # Get the labels and append to list
            generated_labels, actual_labels = trainer.run()
            labels.append([generated_labels, actual_labels, child_names])


            # Append losses to be graphed
            loss_curves.append({
                "train_loss": trainer.train_loss_curve,
                "val_loss": trainer.test_loss_curve
            })


        # Print accuracy table
        accuracy.get_accuracy(labels)

        # Plotting the loss curves for each fold
        plt.figure(figsize=(20, 12))
        for i, curves in enumerate(loss_curves):
            epochs = range(1, len(curves["train_loss"]) + 1)
            plt.plot(epochs, curves["train_loss"], label=f"Fold {i + 1} Train", linestyle=":")
            plt.plot(epochs, curves["val_loss"], label=f"Fold {i + 1} Test")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.title("Training and Validation Loss Curves Across Folds")
        plt.legend()
        plt.show()
    else:
        print("No valid algorithm selected. Exiting...")
        sys.exit(1)

    # Optionally, save the model to a file if it performs well.
    #trainer.save_model("trained_neural_net_model.pth")
    #decision_tree_algo.save_model("trained_decision_tree_model.joblib")

