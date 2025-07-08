# From https://github.com/mynameisfiber/high_performance_python_2e/blob/master/07_compiling/cffi/diffusion_2d_cffi_inline.py
from cffi import FFI, verifier

import numpy as np

grid_shape = (512, 512)

ffi = FFI()
ffi.cdef("void evolve(double **in, double **out, double D, double dt);")
lib = ffi.verify(
    r"""
void evolve(double in[][512], double out[][512], double D, double dt) {
    int i, j;
    double laplacian;
    for (i=1; i<511; i++) {
        for (j=1; j<511; j++) {
            laplacian = in[i+1][j] + in[i-1][j] + in[i][j+1] + in[i][j-1] - 4 * in[i][j];
            out[i][j] = in[i][j] + D * dt * laplacian;
        }
    }
}
""",
    extra_compile_args=["-O3"],  # <1>
)


def evolve(grid, dt, out, D=1.0):
    pointer_grid = ffi.cast("double**", grid.ctypes.data)
    pointer_out = ffi.cast("double**", out.ctypes.data)
    lib.evolve(pointer_grid, pointer_out, D, dt)
