"""
local tasks
"""
import logging
from invoke import task, call
import os

# from sqlalchemy.engine.url import make_url
import click
from tasks.utils import get_compose_env, is_venv

from .utils import (
    COLOR_WARNING,
    COLOR_DANGER,
    COLOR_SUCCESS,
    COLOR_CAUTION,
    COLOR_STABLE,
)

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

@task(incrementable=["verbose"])
def get_env(ctx, loc="local", verbose=0):
    """
    Get environment vars necessary to run flask
    Usage: inv local.get-env
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = False

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    for key in env:
        print("{0}={1}".format(key, env[key]))


@task(incrementable=["verbose"])
def get_python_path(ctx, loc="local", verbose=0):
    """
    Get environment vars necessary to run flask
    Usage: inv local.get-python-path
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = 'python -c "import sys; print(sys.executable)"'
    ctx.run(_cmd)


@task(incrementable=["verbose"])
def detect_os(ctx, loc="local", verbose=0):
    """
    detect what type of os we are using
    Usage: inv local.detect-os
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    res_os = ctx.run("uname -s")
    ctx.config["run"]["env"]["OS"] = "{}".format(res_os.stdout)

    if ctx.config["run"]["env"]["OS"] == "Windows_NT":
        ctx.config["run"]["env"]["DETECTED_OS"] = "Windows"
    else:
        ctx.config["run"]["env"]["DETECTED_OS"] = ctx.config["run"]["env"]["OS"]

    if verbose >= 1:
        msg = "[detect-os] Detected: {}".format(ctx.config["run"]["env"]["DETECTED_OS"])
        click.secho(msg, fg=COLOR_SUCCESS)

    if ctx.config["run"]["env"]["DETECTED_OS"] == "Darwin":
        ctx.config["run"]["env"]["ARCHFLAGS"] = "-arch x86_64"
        ctx.config["run"]["env"][
            "PKG_CONFIG_PATH"
        ] = "/usr/local/opt/libffi/lib/pkgconfig"
        ctx.config["run"]["env"]["LDFLAGS"] = "-L/usr/local/opt/openssl/lib"
        ctx.config["run"]["env"]["CFLAGS"] = "-I/usr/local/opt/openssl/include"

@task(pre=[call(detect_os, loc="local")], incrementable=["verbose"])
def pip_deps(ctx, loc="local", verbose=0, cleanup=False):
    """
    lock flask pip dependencies
    Usage: inv local.pip_deps
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    if verbose >= 1:
        msg = "[pip-deps] Create virtual environment, initialize it, install packages, and remind user to activate after make is done"
        click.secho(msg, fg=COLOR_SUCCESS)

    _cmd = r"""
pip install pip-tools pipdeptree wheel || true
pip-compile --output-file requirements.txt requirements.in --upgrade
    """

    if verbose >= 1:
        msg = "[pip-deps] Install dependencies: "
        click.secho(msg, fg=COLOR_SUCCESS)

        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    ctx.run(_cmd)


@task(pre=[call(detect_os, loc="local")], incrementable=["verbose"])
def bootstrap(ctx, loc="local", verbose=0, cleanup=False):
    """
    start up flask application
    Usage: inv local.serve
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    if verbose >= 1:
        msg = "[install] Create virtual environment, initialize it, install packages, and remind user to activate after make is done"
        click.secho(msg, fg=COLOR_SUCCESS)

    # pip install pre-commit
    # pre-commit install -f --install-hooks
    _cmd = r"""
pip install -r requirements.txt
    """

    if verbose >= 1:
        msg = "[install] Install dependencies: "
        click.secho(msg, fg=COLOR_SUCCESS)

        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    ctx.run(_cmd)

