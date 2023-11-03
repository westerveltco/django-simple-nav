from __future__ import annotations

import os
from pathlib import Path

import nox

PY38 = "3.8"
PY39 = "3.9"
PY310 = "3.10"
PY311 = "3.11"
PY312 = "3.12"
PY_VERSIONS = [PY38, PY39, PY310, PY311, PY312]
PY_DEFAULT = PY38

DJ32 = "3.2"
DJ41 = "4.1"
DJ42 = "4.2"
DJMAIN = "main"
DJMAIN_MIN_PY = PY310
DJ_VERSIONS = [DJ32, DJ41, DJ42, DJMAIN]
DJ_DEFAULT = DJ32


def version(ver: str) -> tuple[int, ...]:
    """Convert a string version to a tuple of ints, e.g. "3.10" -> (3, 10)"""
    return tuple(map(int, ver.split(".")))


def should_skip(python: str, django: str) -> tuple[bool, str | None]:
    """Return True if the test should be skipped"""
    if django == DJMAIN and version(python) < version(DJMAIN_MIN_PY):
        return True, f"Django {DJMAIN} requires Python {DJMAIN_MIN_PY}+"

    if django == DJ32 and version(python) >= version(PY312):
        return True, f"Django {DJ32} requires Python < {PY312}"

    return False, None


@nox.session(python=PY_VERSIONS)
@nox.parametrize("django", DJ_VERSIONS)
def tests(session, django):
    skip = should_skip(session.python, django)
    if skip[0]:
        session.skip(skip[1])

    session.install(".[dev]")

    if django == DJMAIN:
        session.install("https://github.com/django/django/archive/refs/heads/main.zip")
    else:
        session.install(f"django=={django}")

    session.run("python", "-m", "pytest")


@nox.session
def coverage(session):
    session.install(".[dev]")
    session.run("python", "-m", "pytest", "--cov=simple_nav")

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
    session.install(".[lint]")
    session.run("python", "-m", "pre_commit", "run", "--all-files")


@nox.session
def mypy(session):
    session.install(".[dev]")
    session.run("python", "-m", "mypy", ".")
