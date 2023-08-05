__all__ = ["ProjectDevelopMixin"]

import os
import subprocess

from typing import Collection, Iterable, Iterator, Optional

import packaging.markers
import packaging.requirements

from .build import BuildEnv
from .hook import ProjectPEP517HookCallerMixin
from .setup import ProjectSetupMixin


def _evaluate_marker(
    marker: Optional[packaging.markers.Marker], extras: Collection[str]
) -> bool:
    if not marker:
        return True
    if marker.evaluate({"extra": ""}):
        return True
    return any(marker.evaluate({"extra": e}) for e in extras)


def _iter_requirements(
    f: Iterator[str], key: str, extras: Collection[str]
) -> Iterator[str]:
    """Hand-rolled implementation to read ``*.dist-info/METADATA``.

    I don't want to pull in distlib for this (it's not even good at this). The
    wheel format is quite well-documented anyway. This is almost too simple
    and I'm quite sure I'm missing edge cases, but let's fix them when needed.
    """
    key = key.lower()
    for line in f:
        if ":" not in line:  # End of metadata.
            break
        k, v = line.strip().split(":", 1)
        if k.lower() != key:
            continue
        try:
            r = packaging.requirements.Requirement(v)
        except ValueError:
            continue
        if not r.marker or _evaluate_marker(r.marker, extras):
            yield v


class ProjectDevelopMixin(ProjectPEP517HookCallerMixin, ProjectSetupMixin):
    def iter_metadata_for_development(self, env: BuildEnv) -> Iterator[str]:
        """Generate metadata for development install.

        Since PEP 517 does not cover this yet, we fall back to use wheel
        metadata instead. This is good enough because we only use this for
        one of the followings:

        * Requires-Dist
        * Name

        Please keep the list updated if you call this function.

        Generated metadata are stored in the build environment, so it is more
        easily ignored and cleaned up.
        """
        requirements = self.hooks.get_requires_for_build_wheel()
        self.install_build_requirements(env, requirements)

        container = env.root.joinpath("setl-wheel-metadata")
        container.mkdir(parents=True, exist_ok=True)
        target = self.hooks.prepare_metadata_for_build_wheel(container)
        with container.joinpath(target, "METADATA").open(encoding="utf8") as f:
            yield from f

    def install_run_requirements(self, env: BuildEnv, reqs: Iterable[str]):
        if not reqs:
            return
        args = [os.fspath(env.interpreter), "-m", "pip", "install", *reqs]
        subprocess.check_call(args)

    def install_for_development(self, env: BuildEnv):
        """Install the project for development.

        This is a mis-mash between `setup.py develop` and `pip install -e .`
        because we want to have the best of both worlds. Setuptools installs
        egg-info distributions, which is less than ideal. pip, on the other
        hand, does not let us reuse our own build environment, and also
        creates ``pip-wheel-metadata`` ("fixed" in pip 20.0, but still).

        Our own solution...

        1. Installs build requirements (see next step).
        2. Build metadata to know what run-time requirements this project has.
        3. Install run-time requirements with pip, so they are installed as
           modern distributions (dist-info).
        4. Call `setup.py develop --no-deps` so we install the package itself
           without pip machinery.
        """
        metadata = self.iter_metadata_for_development(env)
        requirements = _iter_requirements(metadata, "requires-dist", [])
        self.install_run_requirements(env, requirements)
        self.setuppy(env, "develop", "--no-deps")
