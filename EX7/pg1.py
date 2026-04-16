def activation(yin, theta):
    if yin > theta:
        return 1
    elif yin < -theta:
        return -1
    else:
        return 0

data = []
try:
    filename = input("Enter file name: ")
    with open(filename, "r") as file:
        for line in file:
            row = list(map(float, line.strip().split()))
            if row:
                data.append(row)
except FileNotFoundError:
    print("Error: data.txt not found.")
    exit()

num_features = len(data[0]) - 1

epochs = int(input("Enter max epochs: "))
alpha = float(input("Enter learning rate (alpha): "))
theta = float(input("Enter threshold (theta): "))
weights = []
for i in range(num_features):
   weights.append(float(input(f"w{i+1}: ")))
#weights = [0.0] * num_features
bias = float(input("Enter the bias value: "))

for epoch in range(epochs):
    converged = True
    print(f"\nEpoch {epoch + 1}:")
 
    print(f"{'Inputs':<30}{'Target':<10}{'Y':<5}{'Yin':<10}{'Weights & Bias':<58}{'Status':<10}")
    print("-" * 90)
    for row in data:
        inputs = row[:-1]
        target = row[-1]

        yin = bias + sum(x * w for x, w in zip(inputs, weights))
        y = activation(yin, theta)

        old_weights = weights.copy()
        old_bias = bias

        if y != target:
            converged = False
            for i in range(num_features):
                weights[i] += alpha * target * inputs[i]
            bias += alpha * target
            status = "Updated"
        else:
            status = "No Change"

        wb = f"W={['{:.2f}'.format(w) for w in weights]}, B={bias:.2f}"

        print(f"{str(inputs):<20}{target:<10}{y:<5}{yin:<10.2f}{wb:<35}{status:<10}")

    print("-" * 90)

    if converged:
        print(f"Convergence reached! Stopping at Epoch {epoch + 1}.")
        break

print("\nFinal Result")
print("-" * 30)
for i, w in enumerate(weights):
    print(f"Weight W{i+1}: {w:.4f}")
print(f"Bias: {bias:.4f}")
