import joblib
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt


class DecisionTreeLabelGenerator:

    def __init__(self, train_x, train_y, test_x, test_y):
        self.Train_X = train_x
        self.Train_y = train_y
        self.Test_X = test_x
        self.Test_y = test_y
        self.model = None

    # Main function for the class
    # It will train the decision tree, plot it (optional), and return the generated and actual labels
    def run(self):
        self.train_model()
        # tree.plot_tree(self.model)
        # plt.show()
        return self.generate_labels()

    def train_model(self):
        self.model = tree.DecisionTreeClassifier()
        # self.model = RandomForestClassifier()
        self.model.fit(self.Train_X, self.Train_y)

    # Return two lists (generated vs actual)
    def generate_labels(self):
        if self.model is None:
            raise ValueError("Model not trained. Please call train_model() first.")

        generated_labels = self.model.predict(self.Test_X)
        return generated_labels, self.Test_y

    def save_model(self, file_path):
        joblib.dump(self.model, file_path)
        print(f"Decision Tree model saved to {file_path}")
