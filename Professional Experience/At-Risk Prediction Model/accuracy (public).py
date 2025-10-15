# This script will take our model's output and compare it against the true labels
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import pandas as pd

# Get accuracy measures and print to console
def get_accuracy(labels):

    all_children = []
    all_generated = []
    all_actual = []

    for i in labels:
        # Calculate accuracy
        accuracy = accuracy_score(i[1], i[0])
        print(f"Model Accuracy: {accuracy:.2f}")  # Prints as percentage

        # Compute confusion matrix
        conf_matrix = confusion_matrix(i[1], i[0])

        # Display the matrix
        print("Confusion Matrix:\n", conf_matrix)

        # Generate a detailed performance report
        report = classification_report(i[1], i[0], zero_division=0)
        print("Classification Report:\n", report)


        cn = i[2].values.tolist()
        actual = i[1].values.tolist()
        for j in range(0, len(cn)):
            all_children.append(cn[j])
            all_generated.append(str(i[0][j]))
            all_actual.append(str(actual[j]))

    final_output = pd.DataFrame(
        {'Child Name': all_children,
         'Generated Label': all_generated,
         'Actual Label': all_actual
         })

    with pd.ExcelWriter('Model_Output.xlsx', engine='openpyxl') as writer:
        final_output.to_excel(writer, sheet_name='Model Output')

