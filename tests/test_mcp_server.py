import importlib.util
from pathlib import Path


def load_server_module():
    server_path = Path(__file__).parents[1] / "mcp" / "server.py"
    spec = importlib.util.spec_from_file_location("lotka_mcp_server", server_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_solve_lotka_saves_matplotlib_plots(tmp_path):
    server = load_server_module()

    result = server.solve_lotka(
        alpha=0.8,
        beta=0.2,
        gamma=1.2,
        delta=0.08,
        x0=0.1,
        y0=0.05,
        output=str(tmp_path),
    )

    for plot_path in result.values():
        path = Path(plot_path)
        assert path.is_file()
        assert path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
