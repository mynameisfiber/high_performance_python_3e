#!/usr/bin/env python3

import time

import torch

try:
    profile
except NameError:
    profile = lambda x: x

grid_shape = (512, 512)


@profile
def evolve(conv, grid, dt, out, D=1):
    out = conv(grid)
    out *= D * dt
    out += grid


def run_experiment(num_iterations):
    scratch = torch.zeros([1, 1, *grid_shape])
    grid = torch.zeros([1, 1, *grid_shape])

    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)
    grid[0, 0, block_low:block_high, block_low:block_high] = 0.005

    scratch = scratch.to(device='cuda')
    grid = grid.to(device='cuda')

    kernel = torch.as_tensor(
        [[0., -1., 0.],
          [-1., 4., -1.],
          [0., -1., 0.]]
    ).broadcast_to([1, 1, 3, 3]).to(device='cuda')
    conv = torch.nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, bias=False, padding_mode='zeros', padding=1).to(device='cuda')
    conv.weight = torch.nn.Parameter(kernel)

    start = time.time()
    for i in range(num_iterations):
        evolve(conv, grid, 0.1, scratch)
        grid, scratch = scratch, grid
    return time.time() - start


if __name__ == "__main__":
    print(run_experiment(5000))
