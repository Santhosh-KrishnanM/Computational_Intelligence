import csv
import math
from collections import Counter

def calculate_entropy(labels):
    total = len(labels)
    if total == 0:
        return 0
    counts = Counter(labels)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def main():
    filename = "income.csv".strip()
    
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            columns = reader.fieldnames
            if not data:
                print("Error: No data found!")
                return
    except FileNotFoundError:
        print(f"Error: '{filename}' is not found.")
        return
    target_col = columns[-1]
    attributes = columns[:-1]
    total_rows = len(data)

    target_values = [row[target_col] for row in data]
    parent_entropy = calculate_entropy(target_values)
    counts = Counter(target_values)
    print("--" * 10) 
    print(f"STEP 1: INITIAL ENTROPY CALCULATION")
    print("--" * 10)
    print(f"Target Column: {target_col}")
    #print(f"Formula: Entropy(S) = Sum [ -p_i * log2(p_i) ]")

    parts = [f"-({c}/{total_rows})*log2({c}/{total_rows})" for c in counts.values()]
    print(f"Calculation: {' + '.join(parts)}")
    print(f"Parent Entropy [S] = {parent_entropy:.4f}\n")

    print("--" * 10)
    print(f"STEP 2: CALCULATING ENTROPY & GAIN PER ATTRIBUTE")
    print("--" * 10)
    results = []

    for attr in attributes:
        print(f"\n\t Analyzing Attribute: '{attr}'")

        subsets = {}
        for row in data:
            val = row[attr]
            if val not in subsets:
                subsets[val] = []
            subsets[val].append(row[target_col])

        weighted_entropy = 0
        print(f"  a) Individual Entropy for '{attr}' values:")

        calculation_steps = []
        for val, subset_labels in subsets.items():
            s_entropy = calculate_entropy(subset_labels)
            weight = len(subset_labels) / total_rows
            weighted_entropy += weight * s_entropy

            print(f"     - Value: '{val:10}' | Count: {len(subset_labels)} | Entropy: {s_entropy:.4f}")
            calculation_steps.append(f"({len(subset_labels)}/{total_rows} * {s_entropy:.4f})")

        gain = parent_entropy - weighted_entropy

        print(f"  b) Final Result for '{attr}':")
        print(f"     Weighted Entropy (E_new) = {' + '.join(calculation_steps)}")
        print(f"     E_new = {weighted_entropy:.4f}")
        print(f"     Information Gain = {parent_entropy:.4f} - {weighted_entropy:.4f}")
        print(f"     Gain({attr}) = {gain:.4f}")

        results.append({
            'attribute': attr,
            'gain': gain
        })

    results.sort(key=lambda x: x['gain'], reverse=True)
    print("--" * 10)
    print(f"STEP 3: ATTRIBUTE RANKING")
    print("--" * 10)
    print(f"{'Rank':<5} | {'Attribute':<15} | {'Information Gain':<15}")
    print("-" * 45)

    max_v = 0
    for i, res in enumerate(results, 1):
        if max_v < res['gain']:
           max_v = res['gain']
        continue
    for i, res in enumerate(results, 1):
        if max_v == res['gain']:
           print(f"{i:<5} | {res['attribute']:<15} | {res['gain']:.4f}", end= "")
           print(" <-- Root Node")
           continue
        print(f"{i:<5} | {res['attribute']:<15} | {res['gain']:.4f}")

    print(f"\nThe Root Node is '{results[0]['attribute']}'\n")

if __name__ == "__main__":
    main()
