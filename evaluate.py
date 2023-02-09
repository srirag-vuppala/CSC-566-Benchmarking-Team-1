# Imports
import sys
import dill
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, f1_score
from sklearn.model_selection import cross_val_score
import timeit

if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        if (i == 0):
            continue

        X = None
        y = None

        if arg == "1":
            df = pd.read_csv("https://raw.githubusercontent.com/srirag-vuppala/CSC-566-Benchmarking-Team-1/main/linearly_seperable_classification_10pcnt", index_col = 0)
            X, y = df.drop(columns="y"), df["y"]
            X, y = X.values, y.values
        elif arg == "2":
            df = pd.read_csv("https://raw.githubusercontent.com/srirag-vuppala/CSC-566-Benchmarking-Team-1/main/hotel_10_test.csv", index_col = 1, header = 0)
            df = df.iloc[:,1:].dropna(axis=0, how='any', subset=None, inplace=False)
            X, y = df.drop(columns="booking_status"), df["booking_status"]

            # One hot encode the categorical variables in the training data
            X_enc = pd.get_dummies(X, columns=X.select_dtypes(exclude=np.number).columns)
            # standardize the training data
            X = (X_enc - X_enc.mean()) / X_enc.std()

            y = y.replace(to_replace = ['Not_Canceled', 'Canceled'], value = [-1.0, 1.0]).astype(np.double)
            X, y = X.values, y.values
        elif arg == "3":
            df = pd.read_csv("https://raw.githubusercontent.com/srirag-vuppala/CSC-566-Benchmarking-Team-1/main/sleep_10_test.csv", index_col = 0, header = 0)
            df = df.iloc[:,1:].dropna(axis=0, how='any', subset=None, inplace=False)
            X, y = df.drop(columns="y"), df["y"]
        else:
            print(f"Error: Invalid argument {arg}")
            continue


        sys.path.append(f"./model_src_compiled_challenge{arg}.zip")
        with open(f'model_challenge{arg}.pkl','rb') as file:
            model_test = dill.load(file)

            # Time prediction
            print("Time to train: ", timeit.timeit(lambda: model_test.predict(X), number=1))

            if arg == "3":
                print(f"Model {arg} evaluation")
                print("Mean absolute error:", mean_absolute_error(y, model_test.predict(X)))
                print("R2 score:", r2_score(y, model_test.predict(X)))
                print("Root mean squared error:", mean_squared_error(y, model_test.predict(X), squared=False))
            else:
                print(f"Model {arg} evaluation")
                print("Accuracy Score:", accuracy_score(y, model_test.predict(X)))
                print("F1 Score:", f1_score(y, model_test.predict(X)))

            print("Time to fit:", timeit.timeit(lambda: model_test.fit(X, y), number=1))