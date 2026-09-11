import numpy as np
from scipy.integrate import solve_ivp


def lotka(t, x, alpha, beta, gamma, delta):
    """
    right hand side of lotka-volterra equations
    t = time scalar
    x = state vector [x, y]
    """

    return [alpha * x[0] - beta * x[0] * x[1], delta * x[0] * x[1] - gamma * x[1]]


def solve_lotka(t_span, y0, alpha, beta, gamma, delta, **kwargs):
    return solve_ivp(
        lambda t, x: lotka(t, x, alpha, beta, gamma, delta), t_span, y0, **kwargs
    )


def lotka_trajectory(alpha, beta, gamma, delta, y0, t_span, t_eval=None):
    sol = solve_ivp(
        lambda t, x: lotka(t, x, alpha, beta, gamma, delta),
        t_span,
        y0,
        t_eval=t_eval,
        dense_output=True,
    )
    t = np.array(sol.t)
    y = np.array(sol.y)
    return t, y


if __name__ == "__main__":
    alpha = 1.0
    beta = 0.2
    gamma = 0.1
    delta = 0.05
    y0 = [0.1, 0.2]

    t, y = lotka_trajectory(
        alpha, beta, gamma, delta, y0, (0.0, 10.0), t_eval=np.linspace(0, 15, 300)
    )
    print(t, y)
