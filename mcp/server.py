from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fastmcp import FastMCP

from hgscomp import lotka

mcp = FastMCP("LotkaSolver")


@mcp.tool(name="lotkavolterra")
def solve_lotka(
    alpha=1.0,
    beta=0.1,
    gamma=1.5,
    delta=0.075,
    x0=0.0,
    y0=0.0,
    t_end=10.0,
    n_points=100,
    output="output",
):
    """Solve the Lotka-Volterra model and save Matplotlib plots.

    Args:
        alpha (float, optional): Prey growth parameter. Defaults to 1.0.
        beta (float, optional): Prey-predator interaction parameter. Defaults to 0.1.
        gamma (float, optional): Predator death parameter. Defaults to 1.5.
        delta (float, optional): Predator-prey interaction parameter. Defaults to 0.075.
        x0 (float, optional): Prey initial condition. Defaults to 0.0.
        y0 (float, optional): Predator initial condition. Defaults to 0.0.
        t_end (float, optional): time duration to simulate. Defaults to 10.0.
        n_points (int, optional): Number of time points to record. Defaults to 100.
        output (str, optional): Directory for PNG plots. Defaults to ``output``.

    Returns:
        Paths to the saved time-series and phase-diagram plots.
    """
    t, x, y = lotka.solve_lotkavolterra(
        alpha, beta, gamma, delta, x0, y0, t_end, n_points
    )
    output_dir = Path(output).expanduser()
    if not output_dir.is_absolute():
        output_dir = Path(__file__).resolve().parents[1] / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    time_series_path = output_dir / "lotka_timeseries.png"
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.plot(t, x, label="Prey")
    axis.plot(t, y, label="Predator")
    axis.set(xlabel="Time", ylabel="Population", title="Lotka-Volterra time series")
    axis.legend()
    figure.tight_layout()
    figure.savefig(time_series_path, dpi=150)
    plt.close(figure)

    phase_path = output_dir / "lotka_phase.png"
    figure, axis = plt.subplots(figsize=(6, 5))
    axis.plot(x, y)
    axis.set(
        xlabel="Prey population",
        ylabel="Predator population",
        title="Lotka-Volterra phase diagram",
    )
    figure.tight_layout()
    figure.savefig(phase_path, dpi=150)
    plt.close(figure)

    return {
        "time_series_plot": str(time_series_path.resolve()),
        "phase_plot": str(phase_path.resolve()),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio", show_banner=True)
