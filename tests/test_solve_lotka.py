import importlib.util
import subprocess
import sys

from pytest_bdd import given, scenarios, then, when

scenarios("solve_lotka.feature")


@given(
    "the lotka script accepts command line arguments alpha, beta, gamma, delta, x0, y0"
)
def lotka_args():
    spec = importlib.util.spec_from_file_location("lotka", "src/hgscomp/lotka.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert not hasattr(mod, "main"), "CLI entry point missing"


@when("I run lotka.py with parameters and initial conditions")
def run_lotka():
    result = subprocess.run(
        [
            sys.executable,
            "src/hgscomp/lotka.py",
            "--alpha",
            "1",
            "--beta",
            "0.1",
            "--gamma",
            "1.5",
            "--delta",
            "0.075",
            "--x0",
            "10",
            "--y0",
            "10",
            "--t",
            "10",
        ],
        capture_output=True,
    )
    assert result.returncode == 0, f"script failed: {result.stderr.decode()}"
    return result


@then("I see a plot of x(t), y(t)")
def plot_time():
    from src.hgscomp import lotka

    assert hasattr(lotka, "plot_time"), "plot function not implemented"


@then("I see a plot of y(x)")
def plot_phase():
    from src.hgscomp import lotka

    assert hasattr(lotka, "plot_phase"), "phase plot not implemented"


@then("I see a plot of y(x) next to it in the same pane")
def plot_phase_next_to():
    from src.hgscomp import lotka

    assert hasattr(lotka, "plot_phase"), "phase plot not implemented"


@when("I pass no command line arguments")
def run_lotka_no_args():
    result = subprocess.run(
        [sys.executable, "src/hgscomp/lotka.py"],
        capture_output=True,
    )
    return result


@then(
    "I see an error message 'Lotka Volterra equations need parameters alpha, beta, gamma, delta and initial conditions x0, y0'"
)
def error_message():
    result = subprocess.run(
        [sys.executable, "src/hgscomp/lotka.py"],
        capture_output=True,
    )
    msg = result.stderr.decode() + result.stdout.decode()
    assert (
        "Lotka Volterra equations need parameters alpha, beta, gamma, delta and initial conditions x0, y0"
        in msg
    )


@then("the program exits with an error code")
def exit_error():
    result = subprocess.run(
        [sys.executable, "src/hgscomp/lotka.py"],
        capture_output=True,
    )
    assert result.returncode != 0
