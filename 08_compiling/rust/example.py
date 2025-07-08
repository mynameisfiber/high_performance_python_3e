import numpy as np
from diffusion import evolve as evolve_rust
from cffi_diffusion import evolve as evolve_cffi

for _ in range(100):
    for dt in (1, 1.5, 2):
        for D in (0.1, 0.2, 1.0):
            arr = np.random.random((512, 512))
            result_rust = evolve_rust(arr, dt, D=D)
            out_cffi = np.empty((512, 512), dtype=np.float64)
            evolve_cffi(arr, dt, out_cffi, D=D)
            difference = np.abs(result_rust - out_cffi).sum()
            assert difference < 1e-250, difference
