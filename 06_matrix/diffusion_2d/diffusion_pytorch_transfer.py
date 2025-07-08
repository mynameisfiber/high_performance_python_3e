#!/usr/bin/env python3

import time

import torch

try:
    profile
except NameError:
    profile = lambda x: x

grid_shape = (512, 512)


def laplacian(grid, out):
    out.copy_(grid)
    out *= -4
    out += torch.roll(grid, +1, 0)
    out += torch.roll(grid, -1, 0)
    out += torch.roll(grid, +1, 1)
    out += torch.roll(grid, -1, 1)


@profile
def evolve(grid, dt, out, D=1):
    laplacian(grid, out=out)
    out *= D * dt
    out += grid


def run_experiment(num_iterations):
    scratch = torch.zeros(grid_shape)
    grid = torch.zeros(grid_shape)

    block_low = int(grid_shape[0] * 0.4)
    block_high = int(grid_shape[0] * 0.5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    start = time.time()
    scratch = scratch.to(device='cuda')
    grid = grid.to(device='cuda')
    for i in range(num_iterations):
        evolve(grid, 0.1, scratch)
        grid, scratch = scratch, grid
    grid = scratch.to(device="cpu")
    return time.time() - start


if __name__ == "__main__":
    print(run_experiment(1000))

