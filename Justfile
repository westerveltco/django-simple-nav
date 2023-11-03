set dotenv-load := true

@_default:
    just --list

##################
#  DEPENDENCIES  #
##################

bootstrap:
    python -m pip install --editable '.[dev]'

pup:
    python -m pip install --upgrade pip

update:
    @just pup
    @just bootstrap

venv PY_VERSION="3.11":
#!/usr/bin/env python
    from __future__ import annotations

    import subprocess
    from pathlib import Path

    PY_VERSION = (
        subprocess.run(
            ["pyenv", "latest", "{{ PY_VERSION }}"], capture_output=True, check=True
        )
        .stdout.decode()
        .strip()
    )
    name = f"nav-{PY_VERSION}"

    home = Path.home()

    pyenv_version_dir = home / ".pyenv" / "versions" / PY_VERSION
    pyenv_virtualenv_dir = home / ".pyenv" / "versions" / name

    if not pyenv_version_dir.exists():
        subprocess.run(["pyenv", "install", PY_VERSION], check=True)

    if not pyenv_virtualenv_dir.exists():
        subprocess.run(["pyenv", "virtualenv", PY_VERSION, name], check=True)

    (python_version_file := Path(".python-version")).write_text(name)

##################
#  TESTING/TYPES #
##################

test:
    python -m nox --reuse-existing-virtualenvs

coverage:
    python -m nox --reuse-existing-virtualenvs --session "coverage"

types:
    python -m mypy .

##################
#     DJANGO     #
##################

manage *COMMAND:
    #!/usr/bin/env python
    import sys

    try:
        from django.conf import settings
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    settings.configure(INSTALLED_APPS=["simple_nav"])
    execute_from_command_line(sys.argv + "{{ COMMAND }}".split(" "))

alias mm := makemigrations

makemigrations *APPS:
    @just manage makemigrations {{ APPS }}

migrate *ARGS:
    @just manage migrate {{ ARGS }}

shell:
    @just manage shell

##################
#     DOCS       #
##################

@docs-install:
    python -m pip install '.[docs]'

@docs-serve:
    #!/usr/bin/env sh
    if [ -f "/.dockerenv" ]; then
        sphinx-autobuild docs docs/_build/html --host "0.0.0.0"
    else
        sphinx-autobuild docs docs/_build/html --host "localhost"
    fi

@docs-build LOCATION="docs/_build/html":
    sphinx-build docs {{ LOCATION }}

##################
#     UTILS      #
##################

lint:
    python -m nox --reuse-existing-virtualenvs --session "lint"

mypy:
    python -m nox --reuse-existing-virtualenvs --session "mypy"
