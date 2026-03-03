import random
import string

SIZES = [100, 500, 1000, 2000, 3000, 5000]

def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

for n in SIZES:
    filename = f"random_{n}.txt"
    with open(filename, "w") as fp:
        s1 = random_string(n)
        s2 = random_string(n)
        fp.write(f"{s1}\n{s2}\n")
