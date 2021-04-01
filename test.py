import timeit
from typing import *
from subseq import is_subseq_py, is_subseq_rs


seq = ['a', 'b', 'c'] * 100
subseq = ['dd', 'ee']

joined_seq = "," + ",".join(seq) + ","
joined_subseq = "," + ",".join(subseq) + ","

def find_loop(seq, subseq):
    n = len(seq)
    m = len(subseq)
    for i in range(n - m + 1):
        found = True
        for j in range(m):
            if seq[i + j] != subseq[j]:
                found = False
                break
        if found:
            return True

def is_subseq_str(seq, subseq):
    return subseq in seq

is_subseq_py(seq, subseq)

n = 10000
timer = timeit.Timer("is_subseq(seq, subseq)", globals={"is_subseq": is_subseq_rs, "seq": seq, "subseq": subseq})
t = timer.timeit(number=n)
print(f"rust (rust): {t*10**9/n}")

timer = timeit.Timer("is_subseq(seq, subseq)", globals={"is_subseq": is_subseq_py, "seq": seq, "subseq": subseq})
t = timer.timeit(number=n)
print(f"rust (py): {t*10**9/n}")


timer = timeit.Timer("is_subseq(seq, subseq)", globals={"is_subseq": find_loop, "seq": seq, "subseq": subseq})
t = timer.timeit(number=n)
print(f"python: {t*10**9/n}")


timer = timeit.Timer("is_subseq(seq, subseq)", globals={"is_subseq": is_subseq_str, "seq": seq, "subseq": subseq})
t = timer.timeit(number=n)
print(f"python str: {t*10**9/n}")
