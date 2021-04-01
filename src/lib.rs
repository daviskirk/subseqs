use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::types::PyList;


#[pyfunction]
fn is_subseq_rs(seq: Vec<String>, subseq: Vec<String>) -> bool {
    is_subseq(&seq, &subseq)
}

#[pyfunction]
fn is_subseq_py(seq: &PyList, subseq: &PyList) -> bool {
    let n = seq.len() as isize;
    let m = subseq.len() as isize;
    if m > n {
        return false;
    }
    let mut found = true;
    for i in 0..(n - m + 1) {
        found = true;
        for j in 0..m {
            if seq.get_item(i + j) != subseq.get_item(j) {
                found = false;
                break;
            }
        }
        if found {
            break;
        }
    }
    found
}



/// A Python module implemented in Rust.
#[pymodule]
fn subseq(_: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(is_subseq_rs, m)?)?;
    m.add_function(wrap_pyfunction!(is_subseq_py, m)?)?;

    Ok(())
}


fn is_subseq<T>(seq: &Vec<T>, subseq: &Vec<T>) -> bool
where
    T: std::cmp::PartialEq,
{
    let n = seq.len();
    let m = subseq.len();
    if m > n {
        return false;
    }
    let mut found = true;
    for i in 0..(n - m + 1) {
        found = true;
        for j in 0..m {
            if seq[i + j] != subseq[j] {
                found = false;
                break;
            }
        }
        if found {
            break;
        }
    }
    found
}

