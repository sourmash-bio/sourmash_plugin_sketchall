#! /usr/bin/env python
"""
@@

IDEAS:
- support taking in a CSV or file list instead?
- support ignoring or limiting to a particular extension
"""
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import screed
import sourmash
from sourmash import plugins
from sourmash.logging import debug_literal, notify
from sourmash.command_sketch import _signatures_for_sketch_factory
from sourmash.command_compute import add_seq
from sourmash import sourmash_args


class Command_SketchAll(plugins.CommandLinePlugin):
    command = 'sketchall'
    description = "sketch many genomes"

    def __init__(self, p):
        super().__init__(p)
        p.add_argument('location')
        p.add_argument('-j', '-c', '--cores', type=int, default=4,
                       help="number of processes/cores to use")

    def main(self, args):
        super().main(args)
        debug_literal(f"sketchall main: location is {args.location}")

        debug = 1 if args.debug else 0

        # build params obj
        sig_factory = _signatures_for_sketch_factory([], 'dna')

        # find all files that don't end in .sig.gz or .sig, run on 'em
        FILES = []
        for root, dirs, files in os.walk(args.location, topdown=False):
            for name in files:
                if not name.endswith('.sig') and not name.endswith('.sig.gz'):
                    filename = os.path.join(root, name)
                    #FILES.append(filename + '.sig.gz')
                    FILES.append(filename)

        debug_literal(f"found {len(FILES)} files.")

        with ProcessPoolExecutor(max_workers=args.cores) as executor:
            for filename in FILES:
                executor.submit(compute_sig, sig_factory, filename)


def compute_sig(factory, filename):
    sigfile = filename + '.sig.gz'

    with screed.open(filename) as screed_iter:
        if not screed_iter:
            notify(f"no sequences found in '{filename}'?!")
            return

        sigs = factory()

        for n, record in enumerate(screed_iter):
            if n % 10000 == 0:
                if n:
                    notify('\r...{} {}', filename, n, end='')

            try:
                add_seq(sigs, record.sequence, False, False)
            except ValueError as exc:
                error(f"ERROR when reading from '{filename}' - ")
                error(str(exc))
                return

            notify('...{} {} sequences', filename, n, end='')
        notify(f'calculated {len(sigs)} signatures for {n+1} sequences in {filename}')

        with sourmash_args.SaveSignaturesToLocation(sigfile) as save_sig:
            for ss in sigs:
                save_sig.add(ss)
