#! /usr/bin/env python
"""\
sketch many genomes efficiently using multiple threads.

By default, 'sketchall' ignores files ending in '.sig', '.sig.gz',
'.zip', '.sqldb', and attempts to sketch all other files.
"""

usage="""
   sourmash scripts sketchall <directory>
"""

epilog="""
See https://github.com/sourmash-bio/sourmash_plugin_sketchall for examples.

Need help? Have questions? Ask at http://github.com/sourmash/issues!
"""

#IDEAS:
#- support taking in a CSV or file list instead?
#- support ignoring or limiting to a particular extension

import os
import sys
import argparse
import pathlib
from concurrent.futures import ThreadPoolExecutor

import screed
import sourmash
from sourmash import plugins
from sourmash.logging import debug_literal, notify, error
from sourmash.command_sketch import _signatures_for_sketch_factory
from sourmash.command_compute import add_seq, set_sig_name
from sourmash import sourmash_args


class Command_SketchAll(plugins.CommandLinePlugin):
    command = 'sketchall'
    description = ""

    description = __doc__
    usage = usage
    epilog = epilog
    formatter_class = argparse.RawTextHelpFormatter

    def __init__(self, p):
        super().__init__(p)
        p.add_argument('directory',
                       help="directory to @CTB xyz")
        p.add_argument('-j', '-c', '--cores', type=int, default=4,
                       help="number of processes/cores to use")
        p.add_argument('--extension', default='zip',
                       choices={ "sig", "sig.gz", "zip", "sqldb" })
        p.add_argument('--pattern', default='*',
                       help="wildcard pattern to match for input files")
        p.add_argument('-p', '--param-string', default=['dna'],
                       help='signature parameters to use.', action='append')
        p.add_argument('-o', '--outdir', '--output-directory',
                       help="put created files under this location, instead of in place")
        p.add_argument('-v', '--verbose', action='store_true',
                       help='turn on verbose reporting')

    def main(self, args):
        super().main(args)
        debug_literal(f"sketchall main: location is {args.directory}")

        debug = 1 if args.debug else 0

        # build params obj & sketching factories
        factories = []
        for p in args.param_string:
            f = _signatures_for_sketch_factory(args.param_string, 'dna')
            factories.append(f)

        # find all files that are not sketches, run 'em
        FILES = []
        ignore_exts = { '.sig', '.sig.gz', '.zip', '.sqldb' }

        toplevel = args.directory
        dirpaths = ['']
        notify(f"finding all input files under '{toplevel}' with pattern '{args.pattern}'")
        for filepath in pathlib.Path(toplevel).rglob(args.pattern):
            if filepath.is_dir():
                # track directories we may need to create under output.
                dirpaths.append(filepath.relative_to(toplevel).as_posix())
            elif filepath.is_file():
                relpath = filepath.relative_to(toplevel)
                relpath = relpath.as_posix()

                keep = True
                for ext in ignore_exts:
                    if relpath.endswith(ext):
                        keep = False
                        break

                if keep:
                    FILES.append((toplevel, relpath))

        debug_literal(f"found {len(FILES)} files.")

        # @CTB break out/error out if nothing there

        # create hierarchy of subdirectories if needed.
        outdir = args.outdir
        if outdir:
            for dirpath in sorted(dirpaths):
                dp = os.path.join(args.outdir, dirpath)
                if os.path.exists(dp):
                    continue
                try:
                    debug_literal(f"trying to make {dp}")
                    os.mkdir(dp)
                except:
                    error(f"Cannot make output directory '{dp}'; exiting.")
                    sys.exit(-1)

        notify(f"Starting to sketch {len(FILES)} files with {args.cores} threads.")
        # run things in parallel:
        if args.cores > 1:
            with ThreadPoolExecutor(max_workers=args.cores) as executor:
                for (toplevel, relpath) in FILES:
                    executor.submit(compute_sig, factories, toplevel, relpath,
                                    extension=args.extension,
                                    outdir=outdir, verbose=args.verbose)
        else:
            notify(f"NOTE: running in serial mode, not parallel, because cores={args.cores}")
            for (toplevel, relpath) in FILES:
                compute_sig(factories, toplevel, relpath,
                            extension=args.extension, outdir=outdir,
                            verbose=args.verbose)

        # @CTB number sketched?


def compute_sig(factories, toplevel, relpath, *, extension='zip', outdir=None,
                verbose=False):
    "Build a set of sketches for the given filename."
    sigfile = relpath + '.' + extension
    if outdir:
        sigfile = os.path.join(outdir, sigfile)
    else:
        sigfile = os.path.join(toplevel, sigfile)

    filename = os.path.join(toplevel, relpath)
    if verbose:
        notify(f"sketching '{filename}' => '{sigfile}'")

    name = None
    try:
        with screed.open(filename) as screed_iter:
            if not screed_iter:
                if verbose:
                    notify(f"no sequences found in '{filename}'; skipping.")
                return

            sigslist = [ f() for f in factories ]

            for n, record in enumerate(screed_iter):
                if n % 10000 == 0:
                    if n and verbose:
                        notify('\r...{} {}', filename, n, end='')

                try:
                    for sigs in sigslist:
                        add_seq(sigs, record.sequence, False, False)

                    name = record.name
                except ValueError as exc:
                    error(f"ERROR when reading from '{filename}' - ")
                    error(str(exc))
                    return

            if verbose:
                notify('...{} {} sequences', filename, n + 1)

    except ValueError:
        return

    with sourmash_args.SaveSignaturesToLocation(sigfile) as save_sig:
        for sigs in sigslist:
            set_sig_name(sigs, filename, name)
            for ss in sigs:
                save_sig.add(ss)

    debug_literal(f'saved {len(save_sig)} sketch(es) for {filename} to {sigfile}')
