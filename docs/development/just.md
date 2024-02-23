# Justfile

This project uses [Just](https://github.com/casey/just) as a command runner.

The following commands are available:

<!-- [[[cog
import subprocess
import cog

help = subprocess.run(['just', '--summary'], stdout=subprocess.PIPE)

for command in help.stdout.decode('utf-8').split(' '):
    command = command.strip()
    cog.outl(
        f"- [{command}](#{command})"
    )
]]] -->
- [bootstrap](#bootstrap)
- [copier-copy](#copier-copy)
- [copier-update](#copier-update)
- [copier-update-all](#copier-update-all)
- [coverage](#coverage)
- [docs-build](#docs-build)
- [docs-install](#docs-install)
- [docs-serve](#docs-serve)
- [fmt](#fmt)
- [lint](#lint)
- [makemigrations](#makemigrations)
- [manage](#manage)
- [migrate](#migrate)
- [pup](#pup)
- [test](#test)
- [testall](#testall)
- [types](#types)
- [update](#update)
<!-- [[[end]]] -->

## Commands

```{code-block} shell
:class: copy

$ just --list
```
<!-- [[[cog
import subprocess
import cog

list = subprocess.run(['just', '--list'], stdout=subprocess.PIPE)
cog.out(
    f"```\n{list.stdout.decode('utf-8')}\n```"
)
]]] -->
```
Available recipes:
    bootstrap
    copier-copy TEMPLATE_PATH DESTINATION_PATH="." # apply a copier template to project
    copier-update ANSWERS_FILE *ARGS # update the project using a copier answers file
    copier-update-all *ARGS # loop through all answers files and update the project using copier
    coverage
    docs-build LOCATION="docs/_build/html"
    docs-install
    docs-serve
    fmt                     # format justfile
    lint                    # run pre-commit on all files
    makemigrations *APPS
    mm *APPS                # alias for `makemigrations`
    manage *COMMAND
    migrate *ARGS
    pup
    test *ARGS
    testall *ARGS
    types
    update

```
<!-- [[[end]]] -->

<!-- [[[cog
import subprocess
import cog

summary = subprocess.run(['just', '--summary'], stdout=subprocess.PIPE)

for command in summary.stdout.decode('utf-8').split(' '):
    command = command.strip()
    cog.outl(
        f"### {command}\n"
    )
    cog.outl(
        f"```{{code-block}} shell\n"
        f":class: copy\n"
        f"\n$ just {command}\n"
        f"```\n"
    )
    command_show = subprocess.run(['just', '--show', command], stdout=subprocess.PIPE)
    cog.outl(
        f"```{{code-block}} shell\n{command_show.stdout.decode('utf-8')}```\n"
    )
]]] -->
### bootstrap

```{code-block} shell
:class: copy

$ just bootstrap
```

```{code-block} shell
bootstrap:
    python -m pip install --editable '.[dev]'
```

### copier-copy

```{code-block} shell
:class: copy

$ just copier-copy
```

```{code-block} shell
# apply a copier template to project
copier-copy TEMPLATE_PATH DESTINATION_PATH=".":
    copier copy {{ TEMPLATE_PATH }} {{ DESTINATION_PATH }}
```

### copier-update

```{code-block} shell
:class: copy

$ just copier-update
```

```{code-block} shell
# update the project using a copier answers file
copier-update ANSWERS_FILE *ARGS:
    copier update --trust --answers-file {{ ANSWERS_FILE }} {{ ARGS }}
```

### copier-update-all

```{code-block} shell
:class: copy

$ just copier-update-all
```

```{code-block} shell
# loop through all answers files and update the project using copier
@copier-update-all *ARGS:
    for file in `ls .copier/`; do just copier-update .copier/$file "{{ ARGS }}"; done
```

### coverage

```{code-block} shell
:class: copy

$ just coverage
```

```{code-block} shell
coverage:
    python -m nox --reuse-existing-virtualenvs --session "coverage"
```

### docs-build

```{code-block} shell
:class: copy

$ just docs-build
```

```{code-block} shell
@docs-build LOCATION="docs/_build/html":
    just _cog
    sphinx-build docs {{ LOCATION }}
```

### docs-install

```{code-block} shell
:class: copy

$ just docs-install
```

```{code-block} shell
@docs-install:
    python -m pip install '.[docs]'
```

### docs-serve

```{code-block} shell
:class: copy

$ just docs-serve
```

```{code-block} shell
@docs-serve:
    #!/usr/bin/env sh
    just _cog
    if [ -f "/.dockerenv" ]; then
        sphinx-autobuild docs docs/_build/html --host "0.0.0.0"
    else
        sphinx-autobuild docs docs/_build/html --host "localhost"
    fi
```

### fmt

```{code-block} shell
:class: copy

$ just fmt
```

```{code-block} shell
# format justfile
fmt:
    just --fmt --unstable
```

### lint

```{code-block} shell
:class: copy

$ just lint
```

```{code-block} shell
# run pre-commit on all files
lint:
    python -m nox --reuse-existing-virtualenvs --session "lint"
```

### makemigrations

```{code-block} shell
:class: copy

$ just makemigrations
```

```{code-block} shell
makemigrations *APPS:
    @just manage makemigrations {{ APPS }}
```

### manage

```{code-block} shell
:class: copy

$ just manage
```

```{code-block} shell
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
```

### migrate

```{code-block} shell
:class: copy

$ just migrate
```

```{code-block} shell
migrate *ARGS:
    @just manage migrate {{ ARGS }}
```

### pup

```{code-block} shell
:class: copy

$ just pup
```

```{code-block} shell
pup:
    python -m pip install --upgrade pip
```

### test

```{code-block} shell
:class: copy

$ just test
```

```{code-block} shell
test *ARGS:
    python -m nox --reuse-existing-virtualenvs --session "test" -- "{{ ARGS }}"
```

### testall

```{code-block} shell
:class: copy

$ just testall
```

```{code-block} shell
testall *ARGS:
    python -m nox --reuse-existing-virtualenvs --session "tests" -- "{{ ARGS }}"
```

### types

```{code-block} shell
:class: copy

$ just types
```

```{code-block} shell
types:
    python -m nox --reuse-existing-virtualenvs --session "mypy"
```

### update

```{code-block} shell
:class: copy

$ just update
```

```{code-block} shell
update:
    @just pup
    @just bootstrap
```

<!-- [[[end]]] -->
