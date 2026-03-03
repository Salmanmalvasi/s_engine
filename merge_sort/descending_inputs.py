SIZES = [1000, 5000, 25000, 50000, 100000]

for n in SIZES:
    filename = f"descending_{n}.txt"
    with open(filename, "w") as fp:
        fp.write(f"{n} ")
        for i in range(n, 1, -1):
            fp.write(f"{i} ")
        fp.write("1")
