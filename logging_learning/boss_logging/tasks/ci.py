"""
ci tasks
"""
import os
import logging
from invoke import task
import click
from tasks.utils import get_compose_env

# from tasks.core import clean, execute_sql

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

FILES_TO_CHECK = "main.py application config.py"


@task
def pylint(ctx, loc="local"):
    """
    pylint folder
    Usage: inv ci.pylint
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    ctx.run(
        "pylint --disable=all --enable=F,E --rcfile ./lint-configs-python/python/pylintrc main.py application config.py"
    )


@task
def mypy(ctx, loc="local"):
    """
    mypy folder
    Usage: inv ci.mypy
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    ctx.run("mypy --config-file ./lint-configs-python/python/mypy.ini main.py application config.py")


@task(incrementable=["verbose"])
def black(ctx, loc="local", check=True, debug=False, verbose=0):
    """
    Run black code formatter
    Usage: inv ci.black
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _black_excludes = r"/(\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|_build|buck-out|dist|venv*)/"
    _cmd = ""

    if check:
        _cmd = "black --check --exclude=venv* --verbose main.py application config.py"
    else:
        if verbose >= 1:
            msg = "[black] check mode disabled"
            click.secho(msg, fg="green")
        _cmd = r"black --exclude='{}' --verbose main.py application config.py".format(_black_excludes)

    ctx.run(_cmd)


@task
def isort(ctx, loc="local", check=True, debug=False):
    """
    isort module
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = ""

    if check:
        _cmd = "isort --recursive --check-only --diff --verbose main.py application config.py"
    else:
        _cmd = "isort --recursive --diff --verbose main.py application config.py"

    ctx.run(_cmd)
