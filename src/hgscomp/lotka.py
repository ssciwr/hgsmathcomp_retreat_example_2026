import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp


FloatArray = NDArray[np.float64]


def solve_lotkavolterra(
    alpha: float = 1.0,
    beta: float = 0.1,
    gamma: float = 1.5,
    delta: float = 0.075,
    x0: float = 0.0,
    y0: float = 0.0,
    t_end: float = 10.0,
    n_points: int = 100,
) -> tuple[FloatArray, FloatArray, FloatArray]:
    """Solve the Lotka-Volterra predator-prey model.

    The model is defined by ``dx/dt = alpha*x - beta*x*y`` and
    ``dy/dt = delta*x*y - gamma*y``, where ``x`` is the prey population and
    ``y`` is the predator population.

    Args:
        alpha: Intrinsic prey growth rate.
        beta: Predation-rate coefficient.
        gamma: Predator mortality rate.
        delta: Predator reproduction-rate coefficient.
        x0: Initial prey population.
        y0: Initial predator population.
        t_end: Final integration time.
        n_points: Number of evenly spaced output time points.

    Returns:
        A tuple containing the time values, prey populations, and predator
        populations, respectively.
    """

    def rhs(t: float, state: FloatArray) -> list[float]:
        return lotka(t, state, alpha, beta, gamma, delta)

    t_eval = np.linspace(0, t_end, n_points)
    sol = solve_ivp(rhs, [0, t_end], [x0, y0], t_eval=t_eval, method="RK45")
    return sol.t, sol.y[0], sol.y[1]


def plot_time(t: FloatArray, x: FloatArray, y: FloatArray) -> None:
    """Plot prey and predator populations against time.

    Args:
        t: Time values.
        x: Prey population values corresponding to ``t``.
        y: Predator population values corresponding to ``t``.
    """
    plt.plot(t, x, label="x")
    plt.plot(t, y, label="y")
    plt.legend()
    plt.show()


def plot_phase(x: FloatArray, y: FloatArray) -> None:
    """Plot the predator-prey phase trajectory.

    Args:
        x: Prey population values.
        y: Predator population values corresponding to ``x``.
    """
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


def lotka(
    t: float,
    x: FloatArray,
    alpha: float,
    beta: float,
    gamma: float,
    delta: float,
) -> list[float]:
    """Evaluate the right-hand side of the Lotka-Volterra equations.

    Args:
        t: Current time. The autonomous model does not use it directly.
        x: State vector whose first and second entries are prey and predator
            populations, respectively.
        alpha: Intrinsic prey growth rate.
        beta: Predation-rate coefficient.
        gamma: Predator mortality rate.
        delta: Predator reproduction-rate coefficient.

    Returns:
        The prey and predator derivatives at ``(t, x)``.
    """
    return [alpha * x[0] - beta * x[0] * x[1], delta * x[0] * x[1] - gamma * x[1]]


if __name__ == "__main__":
    import argparse
    import sys

    if len(sys.argv) <= 1:
        sys.stderr.write(
            "Lotka Volterra equations need parameters alpha, beta, gamma, delta and initial conditions x0, y0\n"
        )
        sys.exit(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha", type=float, required=True)
    parser.add_argument("--beta", type=float, required=True)
    parser.add_argument("--gamma", type=float, required=True)
    parser.add_argument("--delta", type=float, required=True)
    parser.add_argument("--x0", type=float, required=True)
    parser.add_argument("--y0", type=float, required=True)
    parser.add_argument("--t", type=float, required=True)
    args = parser.parse_args()
    t, x, y = solve_lotkavolterra(
        alpha=args.alpha,
        beta=args.beta,
        gamma=args.gamma,
        delta=args.delta,
        x0=args.x0,
        y0=args.y0,
        t_end=args.t,
    )
    plot_time(t, x, y)
    plot_phase(x, y)
