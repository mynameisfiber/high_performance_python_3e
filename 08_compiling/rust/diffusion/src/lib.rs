use numpy::{
    ndarray::{ArrayView2, ArrayViewMut2},
    PyArray2, PyArrayMethods, PyReadonlyArray2, PyUntypedArrayMethods,
};
use pyo3::prelude::*;

fn evolve(grid: ArrayView2<f64>, mut out_write: ArrayViewMut2<f64>, D: f64, dt: f64) {
    let shape = grid.shape();
    assert_eq!(shape, out_write.shape());
    for i in 1..(shape[0] - 1) {
        for j in 1..(shape[1] - 1) {
            let laplacian =
                grid[(i + 1, j)] + grid[(i - 1, j)] + grid[(i, j + 1)] + grid[(i, j - 1)]
                    - 4.0 * grid[(i, j)];
            out_write[(i, j)] = grid[(i, j)] + D * dt * laplacian;
        }
    }
}

#[pyfunction(name = "evolve")]
#[pyo3(signature = (grid, dt, D=1.0))]
fn evolve_py<'py>(
    py: Python<'py>,
    grid: PyReadonlyArray2<'py, f64>,
    dt: f64,
    D: f64,
) -> PyResult<Bound<'py, PyArray2<f64>>> {
    let shape = grid.shape();
    // Create a new 2D float64 array filled with zeroes with the same shape as
    // the grid:
    let out_arr = PyArray2::<f64>::zeros_bound(py, [shape[0], shape[1]], false);

    evolve(
        // Pass in a read-only view of the grid:
        grid.as_array(),
        // Pass in a writable view of the output array:
        out_arr.readwrite().as_array_mut(),
        D,
        dt
    );
    Ok(out_arr)
}

/// A Python module implemented in Rust.
#[pymodule]
fn diffusion(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(evolve_py, m)?)?;
    Ok(())
}
