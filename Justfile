set dotenv-load := true

@_default:
    just --list

bootstrap:
    python -m pip install --editable '.[dev]'

# ----------------------------------------------------------------------
# DEPENDENCIES
# ----------------------------------------------------------------------

pup:
    python -m pip install --upgrade pip

update:
    @just pup
    @just bootstrap

# ----------------------------------------------------------------------
# TESTING/TYPES
# ----------------------------------------------------------------------

test:
    python -m nox --reuse-existing-virtualenvs --session "test"

testall:
    python -m nox --reuse-existing-virtualenvs --session "tests"

coverage:
    python -m nox --reuse-existing-virtualenvs --session "coverage"

types:
    python -m nox --reuse-existing-virtualenvs --session "mypy"

# ----------------------------------------------------------------------
# DJANGO
# ----------------------------------------------------------------------

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

    settings.configure(INSTALLED_APPS=["django_simple_nav"])
    execute_from_command_line(sys.argv + "{{ COMMAND }}".split(" "))

alias mm := makemigrations

makemigrations *APPS:
    @just manage makemigrations {{ APPS }}

migrate *ARGS:
    @just manage migrate {{ ARGS }}

# ----------------------------------------------------------------------
# DOCS
# ----------------------------------------------------------------------

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

# ----------------------------------------------------------------------
# UTILS
# ----------------------------------------------------------------------

# format justfile
fmt:
    just --fmt --unstable

# run pre-commit on all files
lint:
    pre-commit run --all-files

# ----------------------------------------------------------------------
# COPIER
# ----------------------------------------------------------------------

# create a copier answers file
copier-copy TEMPLATE_PATH DESTINATION_PATH=".":
    pipx run copier copy {{ TEMPLATE_PATH }} {{ DESTINATION_PATH }}

# update the project using a copier answers file
copier-update ANSWERS_FILE *ARGS:
    pipx run copier update --answers-file {{ ANSWERS_FILE }} {{ ARGS }}

# loop through all answers files and update the project using copier
@copier-update-all *ARGS:
    for file in `ls .copier-answers/`; do just copier-update .copier-answers/$file "{{ ARGS }}"; done
