from __future__ import annotations

import os
from pathlib import Path

import nox

nox.options.default_venv_backend = "uv|virtualenv"
nox.options.reuse_existing_virtualenvs = True

PY38 = "3.8"
PY39 = "3.9"
PY310 = "3.10"
PY311 = "3.11"
PY312 = "3.12"
PY_VERSIONS = [PY38, PY39, PY310, PY311, PY312]
PY_DEFAULT = PY_VERSIONS[0]
PY_LATEST = PY_VERSIONS[-1]

DJ32 = "3.2"
DJ42 = "4.2"
DJ50 = "5.0"
DJMAIN = "main"
DJMAIN_MIN_PY = PY310
DJ_VERSIONS = [DJ32, DJ42, DJ50, DJMAIN]
DJ_LTS = [DJ32, DJ42]
DJ_DEFAULT = DJ_LTS[0]
DJ_LATEST = DJ_VERSIONS[-2]


def version(ver: str) -> tuple[int, ...]:
    """Convert a string version to a tuple of ints, e.g. "3.10" -> (3, 10)"""
    return tuple(map(int, ver.split(".")))


def should_skip(python: str, django: str) -> bool:
    """Return True if the test should be skipped"""

    if django == DJMAIN and version(python) < version(DJMAIN_MIN_PY):
        # Django main requires Python 3.10+
        return True

    if django == DJ32 and version(python) >= version(PY312):
        # Django 3.2 requires Python < 3.12
        return True

    if django == DJ50 and version(python) < version(PY310):
        # Django 5.0 requires Python 3.10+
        return True

    return False


@nox.session
def test(session):
    session.notify(f"tests(python='{PY_DEFAULT}', django='{DJ_DEFAULT}')")


@nox.session
@nox.parametrize(
    "python,django",
    [
        (python, django)
        for python in PY_VERSIONS
        for django in DJ_VERSIONS
        if not should_skip(python, django)
    ],
)
def tests(session, django):
    session.install("django-simple-nav[dev] @ .")

    if django == DJMAIN:
        session.install(
            "django @ https://github.com/django/django/archive/refs/heads/main.zip"
        )
    else:
        session.install(f"django=={django}")

    session.run("python", "-m", "pytest")


@nox.session
def coverage(session):
    session.install("django-simple-nav[dev] @ .")
    session.run("python", "-m", "pytest", "--cov=django_simple_nav")

    try:
        summary = os.environ["GITHUB_STEP_SUMMARY"]
        with Path(summary).open("a") as output_buffer:
            output_buffer.write("")
            output_buffer.write("### Coverage\n\n")
            output_buffer.flush()
            session.run(
                "python",
                "-m",
                "coverage",
                "report",
                "--skip-covered",
                "--skip-empty",
                "--format=markdown",
                stdout=output_buffer,
            )
    except KeyError:
        session.run(
            "python", "-m", "coverage", "html", "--skip-covered", "--skip-empty"
        )

    session.run("python", "-m", "coverage", "report")


@nox.session
def lint(session):
    session.install("django-simple-nav[lint] @ .")
    session.run("python", "-m", "pre_commit", "run", "--all-files")


@nox.session
def mypy(session):
    session.install("django-simple-nav[dev] @ .")
    session.run("python", "-m", "mypy", ".")


@nox.session
def demo(session):
    addrport = session.posargs[0] if session.posargs else "localhost:8000"

    session.install("django-simple-nav[dev] @ .")
    session.run("python", "example/demo.py", "runserver", addrport)
