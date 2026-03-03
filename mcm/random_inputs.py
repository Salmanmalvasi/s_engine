import random

SIZES = [5, 10, 15, 20, 25, 30, 40, 50]

for n in SIZES:
    filename = f"random_{n}.txt"
    with open(filename, "w") as fp:
        fp.write(f"{n} ")
        for _ in range(n):
            dim = random.randint(1, 100)
            fp.write(f"{dim} ")
