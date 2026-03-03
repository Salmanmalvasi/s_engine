import random
import string

SIZES = [10, 50, 100, 500, 1000, 5000, 10000]

for n in SIZES:
    filename = f"random_{n}.txt"
    with open(filename, "w") as fp:
        # Generate n unique characters (using extended ASCII if needed)
        if n <= 26:
            chars = list(string.ascii_lowercase[:n])
        elif n <= 52:
            chars = list(string.ascii_lowercase + string.ascii_uppercase)[:n]
        else:
            # Use numbers as character representations for larger sets
            chars = [str(i) for i in range(n)]
        
        # Random frequencies between 1 and 1000
        freqs = [random.randint(1, 1000) for _ in range(n)]
        
        fp.write(f"{n}\n")
        fp.write(" ".join(chars) + "\n")
        fp.write(" ".join(map(str, freqs)) + "\n")
