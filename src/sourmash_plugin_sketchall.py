#! /usr/bin/env python
"""
@@

IDEAS:
- support taking in a CSV or file list instead?
- support ignoring or limiting to a particular extension
"""
import os
import subprocess
import sys
import sourmash
from sourmash import plugins
from sourmash.logging import debug_literal


class Command_SketchAll(plugins.CommandLinePlugin):
    command = 'sketchall'
    description = "sketch many genomes"

    def __init__(self, p):
        super().__init__(p)
        p.add_argument('location')
        p.add_argument('-j', '-c', '--cores', type=int, default=4,
                       help="number of processes/cores to use")
        p.add_argument('-n', '--dry-run', '--dryrun', action='store_true',
                       help="only print out what would be run, do not execute")

    def main(self, args):
        super().main(args)
        debug_literal(f"sketchall main: location is {args.location}")
        print(sys.executable)

        debug = 1 if args.debug else 0

        run_snakemake(config_params=[f"location={args.location}",
                                     f"debug={debug}"],
                      cores=args.cores, dry_run=args.dry_run)


def get_snakefile_path(name):
    thisdir = os.path.dirname(__file__)
    snakefile = os.path.join(thisdir, name)
    return snakefile


def run_snakemake(*,
                  snakefile_name="sketchall.snakefile",
                  config_params=[],
                  extra_args=[],
                  subprocess_args=None,
                  cores=1,
                  dry_run=False,
):
    # find the Snakefile relative to package path
    snakefile = get_snakefile_path(snakefile_name)

    # basic command
    cmd = [sys.executable, "-m", "snakemake", "-s", snakefile]

    cmd += ["-j", str(cores), '-k']

    # add rest of snakemake arguments
    cmd += list(extra_args)

    # add config params
    config_params = list(config_params)

    if config_params:
        cmd += ["--config", *config_params]

    debug_literal(f"sketchall: snakemake command is {repr(cmd)}")

    # runme
    if subprocess_args is None:
        subprocess_args = {}
    return subprocess.run(cmd, **subprocess_args)
