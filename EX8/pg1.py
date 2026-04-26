import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def process_splits(splits_input):
    splits = []
    labels = []
    for s in splits_input.split(","):
        try:
            train_p, test_p = map(int, s.split("-"))
            if train_p + test_p != 100:
                print(f"Invalid split {s}, skipping...")
                continue
            splits.append(test_p / 100)
            labels.append(s)
        except:
            print(f"Invalid format {s}, skipping...")
    return splits, labels

def evaluate_model(X, y, splits, labels, n_trees, m):
    results = []
    for split, label in zip(splits, labels):
        print(f"\nProcessing split: {label}")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=split, random_state=42
        )
        if m == 1:
            model = RandomForestClassifier(n_estimators=n_trees,criterion='entropy', random_state=42)
        else:
            model = RandomForestClassifier(n_estimators=n_trees, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()
        print(cm)
        results.append((label, acc, prec, rec, f1, tn, fp, fn, tp))
    return results

def display_results(results):
    print("\n\nPerformance Table: ")
    i = 1
    for label, acc, prec, rec, f1, tn, fp, fn, tp in results:
        print(f"{'Split '}{i}{':'} {label:<20}")
        #print(f"{tn:<5} {fp:<5} {fn:<5} {tp:<5}")
        print(f"Accuracy: {acc:.4f}, Precision: {prec:.4f}\n Recall: {rec:.4f}, F1: {f1:.4f}")
        print("-" * 50)
        i += 1

def main():
    dataset_name = input("Enter dataset CSV file name (with .csv): ")
    n_trees = int(input("Enter number of decision trees: "))
    splits_input = input("Enter splits (e.g., 60-40,75-25,80-20): ")

    splits, labels = process_splits(splits_input)
    if not splits:
        print("No valid splits provided!")
        return

    data = pd.read_csv(dataset_name)

    data = data.replace('?', np.nan)
    data = data.dropna()
    data = data.apply(pd.to_numeric)

    data = data.replace('?', np.nan).dropna().apply(pd.to_numeric)

    print("1.Entropy   2. Gini Impurity\n")
    m = int(input("Enter 1 or 2: "))

    print("\nColumns in dataset:", list(data.columns))
    target_col = input("Enter target column name: ")

    if target_col not in data.columns:
        print("Invalid target column!")
        return

    X = data.drop(columns=[target_col])
    y = data[target_col]

    results = evaluate_model(X, y, splits, labels, n_trees, m)
    display_results(results)

if __name__ == "__main__":
    main()
