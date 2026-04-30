from itertools import product

def normalize(dist):
    total = sum(dist.values())
    return {k: v / total for k, v in dist.items()} if total else dist


def check_match(assign, vars, cond):
    return all(assign[vars.index(k)] == v for k, v in cond.items())

def marginal(dist, vars, cond):
    return sum(p for a, p in dist.items() if check_match(a, vars, cond))


def conditional(dist, vars, A, B):
    num = marginal(dist, vars, {**A, **B})
    den = marginal(dist, vars, B)
    return None if den == 0 else num / den


def bayes(dist, vars, A, B):
    p_b_given_a = conditional(dist, vars, B, A)
    p_a = marginal(dist, vars, A)
    p_b = marginal(dist, vars, B)
    return None if p_b == 0 else (p_b_given_a * p_a) / p_b

def parse(inp):
    if not inp.strip():
        return {}
    return dict(x.strip().split("=") for x in inp.split(","))

def simple():
    ch = input("1.Coins  2.Dice: ")

    if ch == '1':
        outcomes = ['HH','HT','TH','TT']

        while True:
            print("\nCoins Menu:")
            print("1. At least one head")
            print("2. Exactly one head")
            print("3. Both heads")
            print("4. Exit")

            op = input("Choose option: ")

            if op == '1':
                fav = [o for o in outcomes if 'H' in o]

            elif op == '2':
                fav = [o for o in outcomes if o.count('H') == 1]

            elif op == '3':
                fav = [o for o in outcomes if o == 'HH']

            else:
                break

            print("Probability =", len(fav) / len(outcomes))

    else:
        outcomes = list(product(range(1,7), repeat=2))

        while True:
            print("\nDice Menu:")
            print("1. Sum = k")
            print("2. Sum <= k")
            print("3. At least one die shows k")
            print("4. Exactly one die shows k")
            print("5. Exit")

            op = input("Choose option: ")

            if op == '1':
                k = int(input("Enter k: "))
                fav = [o for o in outcomes if sum(o) == k]

            elif op == '2':
                k = int(input("Enter k: "))
                fav = [o for o in outcomes if sum(o) <= k]

            elif op == '3':
                k = int(input("Enter k: "))
                fav = [o for o in outcomes if k in o]

            elif op == '4':
                k = int(input("Enter k: "))
                fav = [o for o in outcomes if o.count(k) == 1]

            else:
                break

            print("Probability =", len(fav) / len(outcomes))


def joint():
    n = int(input("No. of variables: "))
    vars, domains = [], []

    for i in range(n):
        v = input("Var name: ")
        d = input("Values: ").split()
        vars.append(v)
        domains.append(d)

    dist = {}
    for a in product(*domains):
        p = float(input(f"P{a} = "))
        dist[a] = p

    if abs(sum(dist.values()) - 1) > 1e-6:
        dist = normalize(dist)

    return dist, vars


def queries(dist, vars):
    while True:
        ch = input("1.P(A) 2.P(A|B) 3.Bayes 4.Exit: ")

        if ch == '1':
            A = parse(input("Enter A: "))
            print("Ans =", marginal(dist, vars, A))

        elif ch == '2':
            A = parse(input("A: "))
            B = parse(input("B: "))
            print("Ans =", conditional(dist, vars, A, B))

        elif ch == '3':
            A = parse(input("A: "))
            B = parse(input("B: "))
            print("Ans =", bayes(dist, vars, A, B))

        else:
            break

def main():
    while True:
        ch = input("1.Simple 2.Joint 3.Exit: ")

        if ch == '1':
            simple()
        elif ch == '2':
            dist, vars = joint()
            queries(dist, vars)
        else:
            break


if __name__ == "__main__":
    main()
