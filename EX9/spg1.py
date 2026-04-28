# Input values
units1 = int(input("Enter units produced by Plant 1: "))
defect1 = float(input("Enter defective fraction of Plant 1: "))

units2 = int(input("Enter units produced by Plant 2: "))
defect2 = float(input("Enter defective fraction of Plant 2: "))

units3 = int(input("Enter units produced by Plant 3: "))
defect3 = float(input("Enter defective fraction of Plant 3: "))

num = units1 * defect1
den = (units1 * defect1) + (units2 * defect2) + (units3 * defect3)

result = num / den

# Output (decimal)
print(f"Probability (decimal): {result:.2f}")