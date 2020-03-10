## For easier local testing, place your single rule at the bottom

import subprocess
import os
import tempfile
import shutil
import pytest
import sys

def run(wrapper, cmd, check_log=None):
    origdir = os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        dst = os.path.join(d, "master", wrapper)
        os.makedirs(dst, exist_ok=True)
        copy = lambda src: shutil.copy(os.path.join(wrapper, src), dst)
        success = False
        for ext in ("py", "R", "Rmd"):
            script = "wrapper." + ext
            if os.path.exists(os.path.join(wrapper, script)):
                copy(script)
                success = True
                break
        assert success, "No wrapper.{py,R,Rmd} found"

        copy("environment.yaml")
        testdir = os.path.join(wrapper, "test")
        # switch to test directory
        os.chdir(testdir)
        if os.path.exists(".snakemake"):
            shutil.rmtree(".snakemake")
        cmd = cmd + ["--wrapper-prefix", "file://{}/".format(d)]
        subprocess.check_call(["snakemake", "--version"])

        try:
            subprocess.check_call(cmd)
        except Exception as e:
            # go back to original directory
            os.chdir(origdir)
            logfiles = [
                os.path.join(d, f)
                for d, _, files in os.walk(os.path.join(testdir, "logs"))
                for f in files
            ]
            for path in logfiles:
                with open(path) as f:
                    msg = "###### Logfile: " + path + " ######"
                    print(msg, "\n")
                    print(f.read())
                    print("#" * len(msg))
            if check_log is not None:
                for f in logfiles:
                    check_log(open(f).read())
            else:
                raise e
        finally:
            # go back to original directory
            os.chdir(origdir)


## write out your test here, and run it (following for example)
#def test_samtools_depth():
#    run(
#        "bio/samtools/depth",
#        ["snakemake", "depth.txt", "--use-conda", "-F"],
#    )
#
#test_samtools_depth()
