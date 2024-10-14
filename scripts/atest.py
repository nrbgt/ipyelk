"""Run acceptance tests with robot framework"""

# Copyright (c) 2024 ipyelk contributors.
# Distributed under the terms of the Modified BSD License.

# pylint: disable=broad-except
import os
import shutil
import sys
import time
from pathlib import Path

import robot
from pabot import pabot

from . import project as P

PROCESSES = int(os.environ.get("ATEST_PROCESSES", "4"))
RETRIES = int(os.environ.get("ATEST_RETRIES", "0"))


def get_stem(attempt, extra_args):
    """Make a directory stem with the run type, python and os version"""
    stem = "_".join([P.PLATFORM, str(attempt)]).replace(".", "_").lower()

    if "--dryrun" in extra_args:
        stem = f"dry_run_{stem}"

    return stem


def which(path: str) -> str | None:
    """Resolve a binary to a POSIX path."""
    for extension in ["", ".exe", ".bat"]:
        exe = shutil.which(f"{path}{extension}")
        if exe:
            return Path(exe).as_posix()
    return None


def atest(attempt, extra_args):
    """Perform a single attempt of the acceptance tests"""
    stem = get_stem(attempt, extra_args)
    firefox = which("firefox")
    geckodriver = which("geckodriver")
    if None in [firefox, geckodriver] and "--dryrun" not in extra_args:
        raise RuntimeError(f"Unable to find browser: {firefox}  {geckodriver}")
    if attempt != 1:
        previous = P.ATEST_OUT / f"{get_stem(attempt - 1, extra_args)}" / "output.xml"
        print(f"Attempt {attempt} will try to re-run tests from {previous}")

        if previous.exists():
            extra_args += ["--rerunfailed", previous]
        else:
            print(f"... can't re-run failed, missing: {previous}")

    out_dir = P.ATEST_OUT / stem

    args = [
        *["--name", f"{P.PLATFORM}"],
        *["--outputdir", out_dir],
        *["--log", out_dir / "log.html"],
        *["--report", out_dir / "report.html"],
        *["--xunit", out_dir / "xunit.xml"],
        *["--variable", f"OS:{P.PLATFORM}"],
        *["--variable", f"IPYELK_EXAMPLES:{P.EXAMPLES}"],
        *["--variable", f"FIREFOX:{firefox}"],
        *["--variable", f"GECKODRIVER:{geckodriver}"],
        *["--randomize", "all"],
        *(extra_args or []),
        *(os.environ.get("ATEST_ARGS", "").split()),
    ]

    if out_dir.exists():
        print(f"trying to clean out {out_dir}")
        try:
            shutil.rmtree(out_dir)
        except Exception as err:
            print(f"Error deleting {out_dir}, hopefully harmless: {err}")
    out_dir.mkdir(parents=True)
    os.chdir(out_dir)

    if "--dryrun" in extra_args or PROCESSES == 1:
        run_robot = robot.run_cli
        fake_cmd = "robot"
    else:
        run_robot = pabot.main
        fake_cmd = "pabot"

        # pabot args must come first
        args = [
            *["--processes", PROCESSES],
            "--artifactsinsubfolders",
            *["--artifacts", "png,log,svg"],
            *args,
        ]

    args += [P.ATEST]

    print(f"[{fake_cmd} test root]\n", P.ATEST)
    print(f"[{fake_cmd} arguments]\n", " ".join(list(map(str, args))))

    try:
        run_robot(list(map(str, args)))
        return 0
    except SystemExit as err:
        print(run_robot.__name__, "exited with", err.code)
        return err.code


def attempt_atest_with_retries(*extra_args):
    """Retry the robot tests a number of times"""
    attempt = 0
    error_count = -1

    is_real = "--dryrun" not in extra_args

    if is_real and P.ATEST_CANARY.exists():
        P.ATEST_CANARY.unlink()

    while error_count != 0 and attempt <= RETRIES:
        attempt += 1
        print(f"attempt {attempt} of {RETRIES + 1}...")
        start_time = time.time()
        error_count = atest(attempt=attempt, extra_args=list(extra_args))
        print(error_count, "errors in", int(time.time() - start_time), "seconds")

    if is_real and not error_count:
        P.ATEST_CANARY.touch()

    return error_count


if __name__ == "__main__":
    sys.exit(attempt_atest_with_retries(*sys.argv[1:]))
