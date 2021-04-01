
import pyximport; pyximport.install()

import pandas as pd
import numpy as np
import numba as nb
from numba import jit, njit
from time import perf_counter, perf_counter_ns
from subseq import is_subseq_py, is_subseq_rs
from cy_subseq import find_loop_cy

import cython

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
    return False

find_loop_jit = jit(forceobj=True, cache=True)(find_loop)
find_loop_njit = njit(cache=True)(find_loop)

subseq = ['dd', 'ee']
seq = ['a', 'b', 'c'] * 100 + subseq


np_seq = np.array(seq)
np_subseq = np.array(subseq)

pd_seq = pd.Series(seq).astype("string").values
pd_subseq = pd.Series(subseq).astype("string").values


cat_seq = pd.Series(seq).astype("category").values.codes
cat_subseq = pd.Series(subseq).astype("category").values.codes


if __name__ == "__main__":

    fcn_map = {
        "py": lambda: find_loop(seq, subseq),
        "cy": lambda: find_loop_cy(seq, subseq),
        "rs": lambda: is_subseq_rs(seq, subseq),
        "rs_py": lambda: is_subseq_py(seq, subseq),
        "py_np": lambda: find_loop(np_seq, np_subseq),
        "py_pd": lambda: find_loop(pd_seq, pd_subseq),
        "jit": lambda: find_loop_jit(pd_seq, pd_subseq),
        "njit": lambda: find_loop_njit(np_seq, np_subseq),
    }

    for k, fcn in fcn_map.items():
        result = fcn()
        print(f"{k}: {result}")

    n = 1000

    for k, fcn in fcn_map.items():
        dt = 0
        for i in range(n):
            t0 = perf_counter_ns()
            fcn()
            t1 = perf_counter_ns()
            dt += t1 - t0
        print(f"{k}: {dt / n}")
