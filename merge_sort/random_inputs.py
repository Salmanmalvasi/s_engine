import random

SIZES = [1000, 5000, 25000, 50000, 100000]

for n in SIZES:
    filename = f"random_{n}.txt"
    with open(filename, "w") as fp:
        fp.write(f"{n} ")
        for _ in range(1, n):
            value = int(random.random() * n)
            fp.write(f"{value} ")
        value = int(random.random() * n)
        fp.write(f"{value}")
