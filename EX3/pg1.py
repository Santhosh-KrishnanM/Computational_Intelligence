import math
import csv
import random

def distance(p1, p2, metric):
    if metric == "euclidean":
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
    else:
        return sum(abs(a - b) for a, b in zip(p1, p2))

def normalize(data, query):
    cols = len(query)
    norm_data = [row[:] for row in data]
    norm_query = query[:]

    mins = [min(row[i] for row in norm_data) for i in range(cols)]
    maxs = [max(row[i] for row in norm_data) for i in range(cols)]

    for row in norm_data:
        for i in range(cols):
            if maxs[i] != mins[i]:
                row[i] = (row[i] - mins[i]) / (maxs[i] - mins[i])

    for i in range(cols):
        if maxs[i] != mins[i]:
            norm_query[i] = (query[i] - mins[i]) / (maxs[i] - mins[i])

    return norm_data, norm_query, mins, maxs

def predict_knn(train_data, query, k, metric):
    distances = []

    for features, label in train_data:
        d = distance(features, query, metric)
        distances.append((d, label))

    distances.sort(key=lambda x: x[0])
    neighbors = distances[:k]

    votes = {}
    for _, label in neighbors:
        votes[label] = votes.get(label, 0) + 1

    return max(votes, key=votes.get)

def knn():

    print("\n\tK-Nearest Neighbor Program\n")

    feature_names = ["Pregnancies","Glucose","BloodPressure",
                     "SkinThickness","Insulin","BMI",
                     "DiabetesPedigreeFunction","Age"]

    dataset = []

    try:
        with open("diabetes.csv") as f:
            csv_reader = csv.reader(f)
            next(csv_reader)

            for row in csv_reader:
                if not row or len(row) < 2:
                   continue
                features = list(map(float, row[:-1]))
                label = int(row[-1])
                dataset.append([features, label])

    except FileNotFoundError:
        print("Error: diabetes.csv not found.")
        return

    count_0 = sum(1 for row in dataset if row[1] == 0)
    count_1 = sum(1 for row in dataset if row[1] == 1)

    print("Full Dataset Distribution:")
    print(f"Class 0 (Non-Diabetic): {count_0}")
    print(f"Class 1 (Diabetic): {count_1}")
    print(f"Total Records: {len(dataset)}\n")


    random.shuffle(dataset)
    split = int(0.8 * len(dataset))
    train_set = dataset[:split]
    test_set = dataset[split:]


    class_0 = [row for row in dataset if row[1] == 0]
    class_1 = [row for row in dataset if row[1] == 1]

    half = 10
    sampled_0 = random.sample(class_0, half)
    sampled_1 = random.sample(class_1, half)

    dataset = sampled_0 + sampled_1
    random.shuffle(dataset)


    print("Available Features:")
    for i, name in enumerate(feature_names):
        print(i, "-", name)

    n = int(input("\nEnter number of features: "))
    idx = list(map(int, input("Enter feature indices: ").split()))
    sel_names = [feature_names[i] for i in idx]

    query = []
    print("\nEnter query values:")
    for i in idx:
        query.append(float(input(f"{feature_names[i]}: ")))

    metric = input("\nDistance metric (euclidean/manhattan): ").lower()
    norm = input("Apply normalization? (yes/no): ").lower()

    selected_orig = [[row[0][i] for i in idx] for row in dataset]
    labels = [row[1] for row in dataset]

    print("\nMinimum and Maximum Values")
    print("----------------------------------------")
    for col in range(len(idx)):
        col_values = [row[col] for row in selected_orig]
        print(f"{sel_names[col]} -> Min: {min(col_values)} | Max: {max(col_values)}")


    features_to_use = selected_orig[:]
    query_to_use = query[:]

    if norm == "yes":
        features_to_use, query_to_use, mins, maxs = normalize(features_to_use, query_to_use)


    # Build table
    table_data = []

    for i in range(len(dataset)):
        d = distance(features_to_use[i], query_to_use, metric)
        table_data.append({
            'orig': selected_orig[i],
            'norm': features_to_use[i],
            'dist': d,
            'label': labels[i]
        })

    sorted_by_dist = sorted(table_data, key=lambda x: x['dist'])

    COL_WIDTH = 16

    headers = sel_names[:]
    if norm == "yes":
        headers += ["Norm_" + name[:3] for name in sel_names]

    headers += ["Distance", "Rank"]

    row_format = ""
    for _ in headers:
        row_format += "{:<16}"

    print("\n" + row_format.format(*headers))
    print("-" * (COL_WIDTH * len(headers)))

    for item in table_data:
        rank = sorted_by_dist.index(item) + 1

        values = []

        for val in item['orig']:
            values.append(f"{val:.1f}")

        if norm == "yes":
            for val in item['norm']:
                values.append(f"{val:.3f}")

        values.append(f"{item['dist']:.4f}")
        values.append(str(rank))

        print(row_format.format(*values))

    while True:

        k = int(input("\nEnter K value: "))
        while k % 2 == 0:
            print("K must be odd.")
            k = int(input("Enter K value: "))

        vote_type = input("Voting method (weighted/unweighted): ").lower()

        neighbors = sorted_by_dist[:k]

        print("\nNEAREST NEIGHBORS\n")

        headers2 = sel_names + ["Distance", "Class"]
        if vote_type == "weighted":
            headers2 += ["Weight(1/d^2)"]

        row_format2 = ""
        for _ in headers2:
            row_format2 += "{:<16}"

        print(row_format2.format(*headers2))
        print("-" * (16 * len(headers2)))

        score = {}

        for nbr in neighbors:
            weight = 1 if vote_type == "unweighted" else 1/(nbr['dist']**2 + 0.0001)
            score[nbr['label']] = score.get(nbr['label'], 0) + weight

            values = []
            for val in nbr['orig']:
                values.append(f"{val:.1f}")

            values.append(f"{nbr['dist']:.4f}")
            values.append(str(nbr['label']))

            if vote_type == "weighted":
                values.append(f"{weight:.6f}")

            print(row_format2.format(*values))

        result = max(score, key=score.get)

        print(f"\nFinal Classification: {result}")

        TP = TN = FP = FN = 0

        for features, actual in test_set:
            prediction = predict_knn(train_set, features, k, metric)

            if actual == 1 and prediction == 1:
                TP += 1
            elif actual == 0 and prediction == 0:
                TN += 1
            elif actual == 0 and prediction == 1:
                FP += 1
            elif actual == 1 and prediction == 0:
                FN += 1

        print("\nConfusion Matrix")
        print("-------------------------")
        print("          Predicted")
        print("        0        1")
        print(f"Actual 0  {TN}       {FP}")
        print(f"Actual 1  {FN}       {TP}")

        accuracy = (TP + TN) / (TP + TN + FP + FN)
        precision = TP / (TP + FP) if (TP + FP) else 0
        recall = TP / (TP + FN) if (TP + FN) else 0

        print("\nPerformance Metrics")
        print("-------------------------")
        print(f"Accuracy  : {accuracy:.4f}")
        print(f"Precision : {precision:.4f}")
        print(f"Recall    : {recall:.4f}")

        ch = int(input("\nContinue? (1=Yes, 0=No): "))
        if ch == 0:
            break


if __name__ == "__main__":
    knn()
