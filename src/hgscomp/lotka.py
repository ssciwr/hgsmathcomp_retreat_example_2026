import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import argparse


def lotka(t, x, alpha, beta, gamma, delta):
    """
    right hand side of lotka-volterra equations
    t = time scalar
    x = state vector [x, y]
    """

    return [alpha * x[0] - beta * x[0] * x[1], delta * x[0] * x[1] - gamma * x[1]]


def plot_solution(t, x):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    ax[0].plot(t, x[0], label="prey")
    ax[0].plot(t, x[1], label="predator")
    ax[0].set_xlabel("t")
    ax[0].set_ylabel("population")
    ax[0].legend()
    ax[0].grid(True)
    ax[1].plot(x[0], x[1])
    ax[1].set_xlabel("prey")
    ax[1].set_ylabel("predator")
    ax[1].grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--alpha", type=float, default=1.0)
    p.add_argument("--beta", type=float, default=0.1)
    p.add_argument("--gamma", type=float, default=1.5)
    p.add_argument("--delta", type=float, default=0.075)
    p.add_argument("--x0", type=float, default=10)
    p.add_argument("--y0", type=float, default=5)
    args = p.parse_args()
    sol = solve_ivp(
        lambda t, x: lotka(t, x, args.alpha, args.beta, args.gamma, args.delta),
        [0, 15],
        [args.x0, args.y0],
        dense_output=True,
        max_step=0.01,
    )
    t = np.linspace(0, 15, 300)
    z = sol.sol(t)
    plot_solution(t, z)
