import random

SIZES = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]

for n in SIZES:
    filename = f"random_{n}.txt"
    with open(filename, "w") as fp:
        fp.write(f"{n}\n")
        # Prices usually increase with length, but can be non-monotonic for the problem
        # Let's use simple random prices or slightly increasing prices
        prices = []
        for i in range(1, n + 1):
            # Arbitrary pricing strategy
            price = random.randint(1, 10) * i + random.randint(-5, 5)
            if price <= 0: price = 1
            prices.append(price)
        fp.write(" ".join(map(str, prices)) + "\n")
