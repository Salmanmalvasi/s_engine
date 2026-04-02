import random
sizes = [1000, 5000, 10000, 20000, 50000]
print("Generating smaller inputs...")
for n in sizes:
    with open(f"random_{n}.txt", "w") as f:
        f.write(f"{n}\n")
        for _ in range(n):
            pts = [str(random.randint(0, 1000)) for _ in range(8)]
            f.write(" ".join(pts) + "\n")
print(f"Generated test cases: {sizes}")
