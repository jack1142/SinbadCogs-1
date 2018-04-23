import resource
import subprocess
import sys
import pathlib
import shlex
import functools


def setlimits(*, timeout: int=60, memlimit: int=50):
    resource.setrlimit(resource.RLIMIT_CPU, (timeout, timeout))
    mb_as_b = memlimit * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_MEMLOCK, (mb_as_b, mb_as_b))


def run_jailed(expr: str, *, timeout: int=60, memlimit: int=60):
    file_str = str(pathlib.Path(__file__).parent / 'jailed_calc.py')
    run_args = [sys.executable, file_str]
    run_args.extend(shlex.quote(expr).split())
    prexec = functools.partial(setlimits, timeout=timeout, memlimit=memlimit)
    p = subprocess.Popen(
        run_args,
        preexec_fn=prexec,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    p.wait()

    if p.returncode == 0:
        return p.stdout
    else:
        return None
