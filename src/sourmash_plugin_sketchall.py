#! /usr/bin/env python
"""
@@
"""
import os
import subprocess
import sys
import argparse
import sourmash
from sourmash import sourmash_args, plugins


class Command_SketchAll(plugins.CommandLinePlugin):
    command = 'sketchall'
    description = "sketch many genomes"

    def __init__(self, p):
        super().__init__(p)
        p.add_argument('directory')
        p.add_argument('-j', '-c', '--cores', type=int, default=4)

    def main(self, args):
        super().main(args)
        directory = args.directory

        run_snakemake(config_params=[f"dir={args.directory}",])


def get_snakefile_path(name):
    thisdir = os.path.dirname(__file__)
    snakefile = os.path.join(thisdir, name)
    return snakefile


def run_snakemake(*,
    snakefile_name="sketchall.snakefile",
    config_params=[],
    extra_args=[],
    subprocess_args=None
):
    # find the Snakefile relative to package path
    snakefile = get_snakefile_path(snakefile_name)

    # basic command
    cmd = ["snakemake", "-s", snakefile]

    # snakemake sometimes seems to want a default -j; set it to 1 for now.
    # can overridden later on command line. #@CTB
    cmd += ["-j", "1", '-k']

    # add rest of snakemake arguments
    cmd += list(extra_args)

    # add config params, and --outdir
    config_params = list(config_params)

    if config_params:
        cmd += ["--config", *config_params]

    print("final command:", cmd)

    # runme
    if subprocess_args is None:
        subprocess_args = {}
    return subprocess.run(cmd, **subprocess_args)
