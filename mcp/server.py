from fastmcp import FastMCP
from prefab_ui.app import PrefabApp
from prefab_ui.components import Grid
from prefab_ui.components.charts import ChartSeries, LineChart

from hgscomp import lotka

mcp = FastMCP("LotkaSolver")


@mcp.tool(name="solve_lotkavolterra")
def solve_lotka(
    alpha=1.0,
    beta=0.1,
    gamma=1.5,
    delta=0.075,
    x0=0.0,
    y0=0.0,
    t_end=10.0,
    n_points=100,
):
    """Solve the lotka volterra model for the given parameters and visualize them.

    Args:
        alpha (float, optional): Prey growth parameter. Defaults to 1.0.
        beta (float, optional): Prey-predator interaction parameter. Defaults to 0.1.
        gamma (float, optional): Predator death parameter. Defaults to 1.5.
        delta (float, optional): Predator-prey interaction parameter. Defaults to 0.075.
        x0 (float, optional): Prey initial condition. Defaults to 0.0.
        y0 (float, optional): Predator initial condition. Defaults to 0.0.
        t_end (float, optional): time duration to simulate. Defaults to 10.0.
        n_points (int, optional): numper of time points to record. Defaults to 100.
    """
    t, x, y = lotka.solve_lotkavolterra(
        alpha, beta, gamma, delta, x0, y0, t_end, n_points
    )

    time_data = [
        {"time": float(time), "prey": float(prey), "predator": float(predator)}
        for time, prey, predator in zip(t, x, y, strict=True)
    ]

    phase_data = [
        {"prey": float(prey), "predator": float(predator)}
        for prey, predator in zip(x, y, strict=True)
    ]

    with PrefabApp(title="Visualization"), Grid(columns=[1, 2], gap=4):
        LineChart(
            id="timeseries",
            data=time_data,
            series=[
                ChartSeries(dataKey="prey", label="Prey"),
                ChartSeries(dataKey="predator", label="Predator"),
            ],
            xAxis="time",
        )

        LineChart(
            id="phasediagram",
            data=phase_data,
            series=[
                ChartSeries(dataKey="prey", label="Prey"),
                ChartSeries(dataKey="predator", label="Predator"),
            ],
            xAxis="prey",
        )


if __name__ == "__main__":
    mcp.run(transport="stdio", show_banner=True)
